# Override to something
override = "workbench"

# General App Workbench testing
from src.build.ApplicationCLI import DeveloperCLI


def workbench():
    from src.workbench.main.app import ApplicationWorkbench

def run_cli():
    method=globals()[DeveloperCLI.run()]

    method()
if override is None:
    run_cli()
else:
    print("blah")
    #method = globals()[override]()

from threading import Thread, Lock


from functools import wraps
from time import sleep
count = 0
def lockable_resource(mutex: Lock, *args, **kwargs):
    def wrap(method):
        def lock_logic(*args, **kwargs):
            mutex.acquire()
            method(*args, **kwargs)
            mutex.release()
        return lock_logic
    return wrap

@lockable_resource(Lock())
def processData(c=""):
    print(f"Do some stuff {c}")

processData("test")
"""while True:
    t = Thread(target=processData, args=(count,))
    t.start()
    t2 = Thread(target=processData, args=(count,))
    t2.start()"""