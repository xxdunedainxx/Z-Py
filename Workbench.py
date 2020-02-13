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


import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.set('foo', 'bar')
r.get('foo')
exit(0)