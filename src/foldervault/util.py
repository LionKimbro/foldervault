
import time
import shutil
import json


def timestamp():
    return int(time.time())

def write_json(p, data):
    p.write_text(json.dumps(data), "utf-8")

def read_json(p):
    return json.loads(p.read_text("utf-8"))

def mkdir(p):
    p.mkdir(parents=False, exist_ok=False)

def nuke_folder(p):
    shutil.rmtree(p)
