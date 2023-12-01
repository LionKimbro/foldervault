"""foldervault.py  -- create and delete folders with ease

---------------------------------------------------------------------
Terminology:

  "Root" (path) -- a folder on the filesystem, that has been set aside
                   to contain only vault folders; there can be
                   multiple roots because some disk drives might be
                   very large (PLENTIFUL), some directories might be
                   automatically backed up via DropBox or OneDrive or
                   rsync (AUTOBACKUP), some disk drives might be
                   "cheap" for some meaning of cheap (CHEAP), some
                   drives might be network mapped (NETWORK), some
                   drives might be fast (FAST), -- and you might want
                   a given created folder to have one of these
                   particular attributes.
 
  "vault folder" -- a folder (or directory) on the filesystem, kept
                    within a Root; all vault folders are identified,
                    uniquely by a randomly chosen v4 UUID.


---------------------------------------------------------------------
Functions Reference:

foldervault.setup() -- perform one time setup (presently, does
                       nothing)

foldervault.reset() -- performs repeatable setup (presently,
                       initializes with default values)

configure(map_dictionary) -- establish the root directories,
                             of which DEFAULT must be one

  recommended keys: CHEAP,
                    PLENTIFUL,
                    AUTOBACKUP,
                    FAST,
                    NETWORK

  mandatory key: DEFAULT

  values: pathlib.Path instances, pointing to root directories

locate() -- locate the vault folder identified by g[UUID], and place
            path to it into g[PATH]

create_path() -- create a blank vault folder identified by g[UUID],
                 and place path to it into g[PATH]

  note that g[DESC][STORAGEPRIORITY] will recommend a search order for
  a root directory; for example: [AUTOBACKUP, CHEAP] will first try to
  position beneath the AUTOBACKUP root directory, and if that isn't
  defined, will try to position beneath the CHEAP root directory, and
  if that isn't defined, will go for the mandatory DEFAULT root
  directory

clear() -- clears g[UUID], g[DESC], g[LEASE], and g[FWD]

new_uuid() -- populate g[UUID] with a new UUID

lease(n) -- reset the time-stamp lease

save() -- imprint g[DESC], g[LEASE], and g[FWD] to disk as desc.json,
          lease.json, and fwd.json -- based on g[PATH]

load() -- the reverse of save() -- based on g[PATH]

lock() -- aquire a lock (returns None if you didn't get it, and a
          pathlib.Path to the data directory, if you did)

unlock() -- release the lock

have_lock() -- return True if you have the lock

in_use() -- return True if some other process has the lock
            (PRESENTLY BROKEN)

delete() -- delete the vault folder
"""


import uuid

import lockfolder.lockfolder as lockfolder

from .words import *
from . import util
from .paths import pathfor


g = {}

mapping = {}

search_cache = {}


def setup():
    """Perform one time setup.
    
    Even though this does nothing today, please do call it, so that if
    in the future a one-time setup functionality is required, no
    changes to initialization will be required.
    
    Call reset() after calling setup().
    """
    pass

def reset():
    """Perform resettable setup.
    
    If you are running automated tests, you may need to reset the
    system to its base state, and that's what this will do.
    
    After a reset, you will need to call configure(...) again.
    """
    g[PATH] = None  # last located (or created) path, to the base of the
    mapping.clear()
    search_cache.clear()
    clear()


def configure(map_dictionary):
    """Supply the map dictionary required for use.
    
    Example form:
      {CHEAP: pathlib.Path(...),
       PLENTIFUL: pathlib.Path(...),
       AUTOBACKUP: pathlib.Path(...),
       FAST: pathlib.Path(...),
       NETWORK: pathlib.Path(...),
       DEFAULT: pathlib.Path(...)}
    
    You can make up your own categories, but I recommend using these,
    as a consistent base.
    
    At a minimum, you MUST have a DEFAULT priority.
    """
    assert DEFAULT in map_dictionary, "required: a DEFAULT mapping"
    mapping.clear()
    mapping.update(map_dictionary)


def locate():
    uuid = g[UUID]
    
    if uuid is None:
        raise ValueError("no UUID supplied")

    # PATH <- cache, if possible
    g[PATH] = search_cache.get(uuid)
    if g[PATH]:
        return g[PATH]

    # Not found.  So search:
    for k, root_path in mapping.items():
        p = root_path / uuid
        if p.exists():
            search_cache[uuid] = g[PATH] = p
            return g[PATH]

    # Still not found.  So it doesn't exist.
    g[PATH] = None
    return None


def create_path():
    uuid = g[UUID]
    
    if uuid is None:
        raise ValueError("no UUID supplied")
    
    # Find the first path that can be found in given priorities:
    for pri in g[DESC][STORAGEPRIORITY]:
        root_path = mapping.get(pri)
        if root_path is None:
            continue
        break
    else:
        root_path = mapping[DEFAULT]
    
    # Record the location in the cache, and keep as g[PATH]
    search_cache[uuid] = g[PATH] = root_path / g[UUID]
    
    # Create directory
    util.mkdir(g[PATH])
    
    # Create sub-directories
    for sym in [LOCKS, DATA]:
        util.mkdir(pathfor(sym))
    
    return g[PATH]


def clear():
    t = util.timestamp()
    g[UUID] = None
    g[DESC] = {TITLE: "",
               DESC: "",
               DATA: {},
               TAGS: [],
               STORAGEPRIORITY: []}
    g[LEASE] = {EXPIRES: None,  # default: no expiration
                LASTUPDATED: t}
    g[FWD] = None


def new_uuid():
    g[UUID] = str(uuid.uuid4())


def lease(n):
    """Update the lease for (n) seconds into the future.
    
    ex: lease(24*60*60) -- extend lifespan of data for a day
    ex: lease(None) -- NEVER EXPIRE
    """
    t = util.timestamp()
    if n is None:
        g[LEASE] = {EXPIRES: None,
                    LASTUPDATED: t}
    else:
        g[LEASE] = {EXPIRES: t + n,
                    LASTUPDATED: t}


def save():
    # Store Data
    _savejson("desc.json", DESC)
    _savejson("lease.json", LEASE)
    _savejson("fwd.json", FWD)


def _savejson(filename, datakey):
    """Saves JSON to the file, or deletes it if data is None.
    
    assumption: g[PATH] is sound
    """
    p = g[PATH] / filename
    if g[datakey] is None:
        if p.exists():
            p.unlink()
    else:
        util.write_json(p, g[datakey])


def load():
    _loadjson("desc.json", DESC)
    _loadjson("lease.json", LEASE)
    _loadjson("fwd.json", FWD)

def _loadjson(filename, datakey):
    """
    assumption: g[PATH] is sound
    """
    p = g[PATH] / filename
    if not p.exists():
        g[datakey] = None
    else:
        g[datakey] = util.read_json(p)


def lock():
    """Attempt to aquire a lock on the folder.
    
    Returns True on success, False on failure.
    """
    obtained = lockfolder.lock(pathfor(LOCKS))
    if obtained:
        return pathfor(DATA)
    else:
        return None

def have_lock():
    """Return True if I already have the lock."""
    return lockfolder.have_lock(pathfor(LOCKS))
    
def in_use():
    """Return True if it's already in use (by another process)."""
    return lockfolder.in_use(pathfor(LOCKS))

def unlock():
    """Release lock on the folder."""
    lockfolder.unlock(pathfor(LOCKS))


def delete():
    """Delete the folder, entirely.
    
    Note: you must have the lock.
    """
    assert have_lock(), "I must have the lock, to delete."""
    util.nuke_folder(g[PATH])

