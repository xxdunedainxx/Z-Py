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
mutex = Lock()
count = 0
def lockable_resource(method):
    @wraps(method)
    def lock_logic(*args, **kwargs):
        mutex.acquire()
        try:
            args.c = 1 + args.c

            print("got it")
            if args.c % 2 == 0:
                sleep(3)
            return method
        finally:
            mutex.release()
    return  lock_logic()

@lockable_resource
def processData(c):
    print('Do some stuff')

while True:
    t = Thread(target=processData, args=(count,))
    t.start()
    t2 = Thread(target=processData, args=(count,))
    t2.start()