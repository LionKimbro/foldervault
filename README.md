# Folder Vault

A near infinite vault of folders, identified by UUID...

#### Installation

"pip install foldervault"

### Introduction

Imagine an extremely long hallway, lined with columns of filing
cabinets to your left and to your right, stretching the length of the
hallway all the way to the horizon.

This is the folder vault.

Each folder has a GUID.  There are more GUIDs than ...  I mean, you
could subdivide the entire surface of the Earth into square inches,
and on each of those square inches, place a miniature globe of the
Earth.  And then repeat the subdivision the same way on that miniature
globe.  And now on each square inch equivalent on that miniature
globe, you can place 500 GUIDs.  That's roughly the scale that we're
talking about here.

I wrote this because...

I write a lot of programs.  And I've even started making swarms of
programs -- lots of simple programs that talk to each other.  Kind of
like Unix programs, but they stay alive and talk amongst each other in
complex ways.  Every single one of these programs needs a folder.  And
they can't all have the same name.  And the name of the folder doesn't
even matter, anyways.  But I can't have them conflicting with one
another.  I don't want to bug the user with "hey, could you spare a
folder for this poor process, ..."  I just want it to be automatic.

Did I mention that I write a lot of programs?  And I want them to
casually have disk storage.  I never ever want to think about the
folder name any more for its persistent data.  I want that to all be
automatic.

So here we are.  An infinitely long hallway, lined with columns of
filing cabinets.  Just pick a folder at random, claim it as your own,
and go from there.

![(image of an infinitely long hallway of doors, marked by GUID)](img/guildhallway.png)


### Scenic Introduction

Assuming you've pip installed the foldervault, follow along in the
interpreter with me.

Let's start with some imports:

```
from pathlib import Path
from pprint import pprint as pp
```

Everything in the folder vault is based on the `pathlib.Path`, so I've
loaded it here.  Don't try and use bare strings containing paths.
Only pathlib.Path objects.

Also, I want to share with you some of the internals, so that you know
what it's doing.  So I imported pprint.pprint here, and shortcutted it
to `pp`.

Now a few more imports, directly from the `foldervault` package.

```
from foldervault.words import *
import foldervault.foldervault as vault
from foldervault.foldervault import g
```


### Symbols

Now "words" collects what I call "symbols" -- all caps variables, that
point to string values that have the same value.  (I should rename
this to "symbols" ...)

Here's an example, as seen in the interpreter:

```
>>> UUID
'UUID'
>>>
```

I use a lot of dictionary keys, see, and fixed string values in my
code, as you will see.  I use these symbols to help make the code more
consistent.  It helps me prevent errors.

Look:

```
>>> D = {UUID: "foo"}
>>> D
{'UUID': 'foo'}
>>> D = {UIUD: "foo"}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'UIUD' is not defined
>>>
```

See?  UUID gets a pass, but UIUD is "not defined."

If I was (mis-)typing in `D["UIUD"] = "foo"`, it would have been given
a pass.  So that's what the "words" module is about -- it just defines
the words that I use.

NOT VERY IMPORTANT.


#### "vault", and "g"

Let's look at the `from foldervault.foldervault as vault` import.

`vault` is the folder vault itself.

And `g` is a dictionary that keeps global variables in it.  There are
a lot of global variables here.

I put global variables in `g`, so that I can avoid Python's `global`
statement.

Now if you call `pp(g)`, you'll see a display of the global state of
the system.


#### Setting Up

Oh, but it's not set up yet -- there's nothing to see.

```
vault.setup()
vault.reset()
```

`setup()` is for one-time setup, and `reset()` is for re-performable
setup.  It's a general pattern in my code, and I use it for automated
testing.

Now if you call `pp(g)`, you should see an output like:

```
{'DESC': {'DATA': {},
          'DESC': '',
          'STORAGEPRIORITY': [],
          'TAGS': [],
          'TITLE': ''},
 'FWD': None,
 'LEASE': {'EXPIRES': None, 'LASTUPDATED': 1701376423},
 'PATH': None,
 'UUID': None}
```

The most important item here is `g[UUID]`, at the bottom.


#### Configuring Disk Space

But before we get there, we need to tell the system about how where on
your computer's disk you want folders to be.

Now, on my computer, I do this with:

```
vault.configure({
    CHEAP: Path(r"F:\vault"),
    AUTOBACKUP: Path(r"F:\bigfiles\onedrive2022\OneDrive\origins\2023\autobackup_vault"),
    DEFAULT: Path(r"F:\vault"),
})
```

On your computer, you'll do something different.

You can that definition to fit your own computer, and make the folders
to back it up.  This step, you have to do manually.  But you will not
have to make folders any more, after this.

You can use these keys to designate disk spaces:

* `CHEAP`  -- inexpensive disk space you don't mind filling up
* `FAST`  -- your fastest access disk space
* `PLENTIFUL`  -- disk with the most space available
* `AUTOBACKUP`  -- disk space that is automatically backed up
* `NETWORK`  -- disk space that is stored over the network
* `DEFAULT`  -- disk space of last resort

You can use any or all of these, but you absolutely MUST specify the path to DEFAULT space.

(Incidentally, if you want to peek at the configured mapping, you'll find it in `vault.mapping`.)

HOWEVER -- for the purpose of this tutorial, do this:

```
import os
os.mkdir("eraseme")
vault.configure({DEFAULT: Path("eraseme")})
```

Just remember to erase the `eraseme` folder when you see it, when
you're all done here.

This means, "Just use this `eraseme/` folder to store stuff in."

OK, that was exciting.  Now let's make a folder!


#### Creating a Folder

```
vault.new_uuid()
```

Now if you look at `pp(g)`, you should see:

```
{'DESC': {'DATA': {},
          'DESC': '',
          'STORAGEPRIORITY': [],
          'TAGS': [],
          'TITLE': ''},
 'FWD': None,
 'LEASE': {'EXPIRES': None, 'LASTUPDATED': 1701376808},
 'PATH': None,
 'UUID': '3593c5a2-39ed-4c4f-8582-719e36bf1134'}
```

The function `vault.new_uuid()` just populates the UUID field with a new UUID.

If you want to make your execution match what I'm doing here exactly
though, just manually set the UUID:

```
g[UUID] = "3593c5a2-39ed-4c4f-8582-719e36bf1134"
```

Don't be too afraid to mess around -- my system here is very
transparent in its operations.  There shouldn't be too many surprises.

Now, tell the system to create the directory.

```
vault.create_path()
```

That actually creates the path.

It might look like this, if you look at it in a file browser:

```
 Directory of C:\Users\Lion\Desktop\working_factory23v2\eraseme\3593c5a2-39ed-4c4f-8582-719e36bf1134

11/30/2023  11:38 PM    <DIR>          .
11/30/2023  11:38 PM    <DIR>          ..
11/30/2023  11:38 PM    <DIR>          data
11/30/2023  11:38 PM    <DIR>          locks
               0 File(s)              0 bytes
               4 Dir(s)  12,569,329,664 bytes free
```

It's a start, but it's not fully prepared.  We'll describe it's
contents in a moment, but for now, just go with this.

```
vault.save()
```

Now it looks like this:

```
 Directory of C:\Users\Lion\Desktop\working_factory23v2\eraseme\3593c5a2-39ed-4c4f-8582-719e36bf1134

11/30/2023  11:39 PM    <DIR>          .
11/30/2023  11:39 PM    <DIR>          ..
11/30/2023  11:38 PM    <DIR>          data
11/30/2023  11:39 PM                72 desc.json
11/30/2023  11:39 PM                44 lease.json
11/30/2023  11:38 PM    <DIR>          locks
               2 File(s)            116 bytes
               4 Dir(s)  12,567,539,712 bytes free
```


#### Understanding Folder Contents

When you call "vault.save()", what it does is it takes `g[DESC]` and
writes it to `desc.json`, and it takes the lease (`g[LEASE`]) and
writes it to `lease.json`.

It does not engage in any locking behavior, though you can restrict
yourself to only saving when you have a lock on the directory.  We'll
talk more about that later.

Oh, something to know right away -- I generally prefer motorcycles to
cars or tanks.  This is a metaphorical way of saying: "You can shoot
yourself in the foot here."  Which is a metaphorical way of saying: My
code here, and my code in general, will not prevent you from doing
something that you shouldn't be doing, generally speaking.  You have
to know a little about what you are doing.  You can do AMAZING things
with motorcycles that you can't do with cars, but -- you have to be a
bit more sensitive to them.  So, be aware of what you're working with
here.

If you look at those files, ...

```
C:\Users\Lion\Desktop\working_factory23v2\eraseme\3593c5a2-39ed-4c4f-8582-719e36bf1134>more desc.json
{"TITLE": "", "DESC": "", "DATA": {}, "TAGS": [], "STORAGEPRIORITY": []}

C:\Users\Lion\Desktop\working_factory23v2\eraseme\3593c5a2-39ed-4c4f-8582-719e36bf1134>more lease.json
{"EXPIRES": null, "LASTUPDATED": 1701416064}
```

...you see a mirror of the global data.

Let's give our folder a little bit of description.

```
g[DESC][TITLE] = """Test folder."""
g[DESC][DESC] = """I'm just testing the folder system."""
g[DESC][TAGS].extend(["test", "folder", "example"])
```

Now look at the data with `pp(g)`:

```
{'DESC': {'DATA': {},
          'DESC': "I'm just testing the folder system.",
          'STORAGEPRIORITY': [],
          'TAGS': ['test', 'folder', 'example'],
          'TITLE': 'Test folder.'},
 'FWD': None,
 'LEASE': {'EXPIRES': None, 'LASTUPDATED': 1701416064},
 'PATH': WindowsPath('eraseme/3593c5a2-39ed-4c4f-8582-719e36bf1134'),
 'UUID': '3593c5a2-39ed-4c4f-8582-719e36bf1134'}
```

Save it to disk.

```
vault.save()
```

And on disk you should see:

```
C:\Users\Lion\Desktop\working_factory23v2\eraseme\3593c5a2-39ed-4c4f-8582-719e36bf1134>more desc.json
{"TITLE": "Test folder.", "DESC": "I'm just testing the folder system.", "DATA": {}, "TAGS": ["test", "folder", "example"], "STORAGEPRIORITY": []}
```

Let's talk about these for a moment.

* `TITLE` -- this is a human readable title for your folder
* `DESC` -- this is a human readable description for your folder
* `DATA` -- this is a machine readable dictionary that can contain anything you like in it
* `TAGS` -- this is a machine and human readable list of tags for the folder
* `STORAGEPRIORITY` -- this is a declaration of where your folder would like to be


#### About STORAGEPRIORITY

`STORAGEPRIORITY` requires a little bit more note: When you called
`vault.create_path()` to create the folder in the first place, the
code first checked `g[DESC][STORAGEPRIORITY]` to see where on the
filesystem it should place the data.  For example, it might look like:
`[FAST, CHEAP]` -- which would mean: "If you have `FAST` storage, put
this vault folder in there.  But if you didn't have `FAST` storage
defined, look for `CHEAP` storage.  But if neither is there, just go
with the `DEFAULT` storage."  (Note that: this is why you MUST define
`DEFAULT` storage.)

Since you only have `DEFAULT` storage, there's no use for the
`STORAGEPRIORITY`.  But if you defined more spaces when you called
`vault.configure({...})`, you could specify one of those other spaces.

Note also that `STORAGEPRIORITY` is only consulted when you call
`vault.create_path()`.  After that, there is no real value to this
variable -- except for what you provide.  What I mean by "what you
provide", is that you could, if you wanted to, -- relocate the vault
folder manually to a preferred root.  You could write a program that
goes through your vault folders, and relocates them by priority.  Or
just do it by hand.  But in the code I've released in the
`foldervault` project, `STORAGEPRIORITY` is only ever consulted at
`vault.create_path()`.  I kept it in the `desc.json` file, though, so
that you could see where the vault folder wanted to be, and rectify it
yourself later.

By the way -- moving vault folders around?  Should only be done when
nothing is using the system.  What I mean is: When you are using these
vault folders, their positions on the filesystem are cached in the
foldervault module's run-time memory.  You need to know this, because
if you move a vault folder, the system will think it is where it was,
rather than to the root that you moved it to.

Oh, "roots."  Roots: That's the name for the different parts of your
filesystem that you configured it to, when you called
`vault.configure({...})`.  The roots are those paths, and they contain
folders that have guids for labels.  Those folders with guids for
labels, are called "vault folders."  So "roots" contain "vault
folders."  And your DATA, the actual data that you came here to store,
-- that's kept in the `data` directory within the vault folder.  And
you should probably get a lock, before reading or writing data in
there.


#### Obtaining a Lock

Let's do that very quickly.

But oh, we need to initialize the locking module.  Locking is provided
through another package that I wrote, called `lockfolder`.

```
import lockfolder.lockfolder

lockfolder.lockfolder.setup()
```

(If `lockfolder.lockfolder.setup()` doesn't work, call `lockfolder.lockfolder.init()`.)

This call is crucial, because it causes the process to choose a UUID
for itself, identify its own PID, and identify its CREATED time -- all
essential for the lock aquisition scheme.

See for yourself, with `pp(lockfolder.lockfolder.g)`.

```
>>> pp(lockfolder.lockfolder.g)
{'CREATED': 1701416045,
 'PID': 27688,
 'UUID': '1f895fed-1c29-46ff-9e34-c1aa9d21d5b6'}
```

That UUID is a UUID that represents the running process, and the PID
and the CREATED times are accurate for your process.  These facts form
the basis for your lock.

Now you can call `vault.lock()`.

```
vault.lock()
```

When you call `vault.lock()`, it returns the path to the `data`
directory, if the lock was obtained.  Otherwise, it returns None.

If you look in the locks directory, you'll see it:

```
 Directory of C:\Users\Lion\Desktop\working_factory23v2\eraseme\3593c5a2-39ed-4c4f-8582-719e36bf1134\locks

11/30/2023  11:52 PM    <DIR>          .
11/30/2023  11:52 PM    <DIR>          ..
11/30/2023  11:52 PM                37 1f895fed-1c29-46ff-9e34-c1aa9d21d5b6.json
               1 File(s)             37 bytes
               2 Dir(s)  13,756,710,912 bytes free
```

The file will read like so:

```
{"PID": 27688, "CREATED": 1701416045}
```

Unlocking will delete the lock.

```
vault.unlock()
```

(You can now confirm that the locks directory is empty.)

If you tried to lock what was already locked, `vault.lock()` would
return `None`, rather than the `pathlib.Path` to the `data` directory.

"What happens if I forget to unlock the data?  Or the program is
killed, before I got to unlock it?"  It's okay!  There's "stale
detection."  That means, it'll notice that the PID and CREATED date
refer to a process that doesn't exist, and the lock will be destroyed.
Other programs going for the lock (provided that they are using this
same system,) will work right.

(Post-script:)

There are to more functions you should know about:
* `vault.has_lock()` -- returns True if I have the lock
* `vault.in_use()` -- returns True if anybody else has the lock -- NOTE: PRESENTLY BROKEN; NEED TO FIX


#### Retrieving a folder

OK, we created a new folder.  But what if we were looking for one that
had been made already before?

Now -- I'm talking about *retrieval* here, not search, or searching.
The difference is with retrieval, you already know the name of the
folder you are looking for (it's UUID), whereas search -- that'd be
like saying, "hey, I'm looking for the GUIDs of all folders that have
this tag..."

This program, this code, doesn't actually help you do that.  I want
you to come up with your own solution for that -- for the time being
at least.  It's because this system is intended to support tens of
thousands (x10,000) of folders, maybe even more than that.  Linear
search is a bad idea in that case.  What I'd want, is some kind of
machine that was indexing the folders by tags, and then returning a
rapid response "what you're looking for is in these folders..."

I intend to write such a thing one day, if I like how it is working
with the folder vault.  But putting that into this system right now,
is not something I'm doing.

If you wanted to crawl a small number of files, though, you can make a
list of the UUIDs in a root, and serially retrieve them:

```
from pathlib import Path

def list_folders_in_root(directory):
    """Returns a list of folders present in the given root.

    :param directory: A pathlib.Path object representing the directory.
    :return: A list of pathlib.Path objects, each representing a folder.
    """
    if not directory.is_dir():
        raise ValueError("Provided path is not a directory")

    # List all entries in the directory and filter out those that are directories
    return [entry.name for entry in directory.iterdir() if entry.is_dir()]
```

OK.  But now that you understand the limitations, lets go back to
retrieving a specific folder.

You go like this:

```
g[UUID] = "3593c5a2-39ed-4c4f-8582-719e36bf1134"

vault.locate()

vault.load()
```

That will repopulate all of the data, from that folder.

Here, let's exit, and then run from the top, so you can see the entire
procedure.

```
from pprint import pprint as pp
from pathlib import Path

from foldervault.words import *
import foldervault.foldervault as vault
from foldervault.foldervault import g

import lockfolder.lockfolder as lockfolder

lockfolder.setup()
vault.setup()
vault.reset()

vault.configure({DEFAULT: Path("eraseme")})

# ----------------------------------------------------------------------

g[UUID] = "3593c5a2-39ed-4c4f-8582-719e36bf1134"

vault.locate()

vault.load()
```

Let's look at it a little more carefully -- because it's two steps.

The first step is `vault.locate()`.  What that does, is look through
the different roots, and finds the vault folder identified with the
UUID.  It stores the `pathlib.Path` to that vault folder, in
`g[PATH]`.  That's "locating."

Here's what `pp(g)` will show, after the `locate()` but before the
`load()`:

```
{'DESC': {'DATA': {},
          'DESC': '',
          'STORAGEPRIORITY': [],
          'TAGS': [],
          'TITLE': ''},
 'FWD': None,
 'LEASE': {'EXPIRES': None, 'LASTUPDATED': 1701417860},
 'PATH': WindowsPath('eraseme/3593c5a2-39ed-4c4f-8582-719e36bf1134'),
 'UUID': '3593c5a2-39ed-4c4f-8582-719e36bf1134'}
```

By the way -- never mind THAT lease data -- that's just a remnant from
the last `clear()` performed during the `reset()` -- it defaults to an
indefinite (never-expiring) lease, for safety reasons.  But that's not
actually what's in the located vault folder.

Now we load in the vault folder's metadata.

To get to that, you call `vault.load()`.

Now `pp(g)` will show the `DESC` and `LEASE` info.

```
>>> pp(g)
{'DESC': {'DATA': {},
          'DESC': "I'm just testing the folder system.",
          'STORAGEPRIORITY': [],
          'TAGS': ['test', 'folder', 'example'],
          'TITLE': 'Test folder.'},
 'FWD': None,
 'LEASE': {'EXPIRES': None, 'LASTUPDATED': 1701416064},
 'PATH': WindowsPath('eraseme/3593c5a2-39ed-4c4f-8582-719e36bf1134'),
 'UUID': '3593c5a2-39ed-4c4f-8582-719e36bf1134'}
 ```

Note the earlier timestamp on the `LEASE` this time -- it was loaded
from what's on disk.

And of course, you see that the TITLE, DESC, and TAGS were loaded in
from the disk.


#### Using the Folder

What we came here for, right?  Actually using the folder?

It's easy.  Just take out the lock.

Provided that you get it, you will be returned with the `data` path.

```
data_path = vault.lock()
```

Here's an example of writing text into a file.

```
(data_path / "foo.txt").write_text("test data", encoding="utf-8")
```

When you are done, release the lock.

```
vault.unlock()
```

There you go!


### Odds & Ends

#### What's this about "leasing?"

I haven't implemented it yet, but one day, I will write a program that
trolls through the vault folders, and identifies the lease timeouts
for each one.  When the vault folder times out it's lease, ("lease"
referring to "a lease on the disk space, for a period of time,") it'll
delete that vault folder from the system -- this is called "reaping"
or "harvesting" or "garbage collection" or something like that.

You can update the lease by calling `vault.lease(n)` where `n` is the
number of seconds into the future that you want reaping to happen.  So
for example, if you say `vault.lease(7*24*60*60)`, then that means the
folder will be reserved for 7 days, after which it is subject to
reaping.

You have to remember to call `vault.save()`, too, to actually store the
updated figures to disk.

If you don't want something EVER deleted, call `vault.lease(None)`,
which I sometimes call an "indefinite lease."

If you are using the lease system, always call `vault.lease(n)` before
you call `vault.save()`.  If you call `vault.lease(None)` from the
start, you probably don't need to update it, though you could, to keep
the `LASTUPDATED` current.


#### What's this about FWD?

Maybe you noticed `FWD`.  If you did, ignore it for now.

I'm reserving it for the future -- the capacity to locate the actual
`data` directory OUTSIDE of the folder vault -- for example, if you
want it to show up on the Windows Desktop, or something like that.

It doesn't exist yet.  Don't worry about it, and don't mess with it.


### Reference

Here's a quick reference guide, to the `foldervault.foldervault` module:

* `setup()` -- perform one time setup (presently, does nothing)
* `reset()` -- performs repeatable setup (presently, initializes with default values)
* `configure(map_dictionary)` -- establish the root directories, of which `DEFAULT` must be one
  * recommended keys: `CHEAP`, `PLENTIFUL`, `AUTOBACKUP`, `FAST`, `NETWORK`
  * mandatory key: `DEFAULT`
  * values: `pathlib.Path` instances, pointing to root directories
* `locate()` -- locate the vault folder identified by `g[UUID]`, and place path to it into `g[PATH]`
* `create_path()` -- create a blank vault folder identified by `g[UUID]`, and place path to it into `g[PATH]`
  * note that `g[DESC][STORAGEPRIORITY]` will recommend a search order for a root directory; for example: `[AUTOBACKUP, CHEAP]` will first try to position beneath the `AUTOBACKUP` root directory, and if that isn't defined, will try to position beneath the `CHEAP` root directory, and if that isn't defined, will go for the mandatory `DEFAULT` root directory
* `clear()` -- clears `g[UUID]`, `g[DESC]`, `g[LEASE]`, and `g[FWD]`
* `new_uuid()` -- populate `g[UUID]` with a new UUID
* `lease(n)` -- reset the time-stamp lease
* `save()` -- imprint `g[DESC]`, `g[LEASE]`, and `g[FWD]` to disk as `desc.json`, `lease.json`, and `fwd.json` -- based on `g[PATH]`
* `load()` -- the reverse of `save()` -- based on `g[PATH]`
* `lock()` -- aquire a lock (returns None if you didn't get it, and a `pathlib.Path` to the data directory, if you did)
* `unlock()` -- release the lock
* `have_lock()` -- return True if you have the lock
* `in_use()` -- return True if some other process has the lock (PRESENTLY BROKEN)
* `delete()` -- delete the vault folder


written: 2023-12-01
