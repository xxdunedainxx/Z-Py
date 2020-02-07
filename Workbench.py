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
    method = globals()[override]()