# Collection of static CLI Functions
# TODO : add I/O for modifying config, instead of having ops manually do it, do it through CLI

# CLI For local devs
class DeveloperCLI:

    CLI_Opts: dict = {

    }

    def __init__(self):
        pass



class CLI:

    sep="---------------------------"
    last_modified="3/15/2019"
    company="Zach, Inc."
    authors="Zach McFadden"
    info="This automation monitors BT support channels, which are no longer monitored for support, and re-routes folks in slack to the appropriate channel"

    options_table: {} = {
        "run_automation" : 'stop'
    }

    def __init__(self):
        pass


    @staticmethod
    def author_header():
        print(CLI.sep)
        print(f"Author(s):{CLI.authors}")
        print(f"{CLI.company}")
        print(f"Synopsis:{CLI.info}")
        print(CLI.sep)

    @staticmethod
    def welcome():
        CLI.author_header()
        print("Welcome to ZPy!")
        print("Below are command line options for this automation")

    @staticmethod
    def options(options: dict = options_table):
        print(CLI.sep)
        print("Please select an option below:")
        for op in options.keys():
            print(f"{op}")

    @staticmethod
    def get_input(cliOptions: dict = options_table)->str:
        get_input=True

        while get_input:
            CLI.options(cliOptions)

            cli_input=input("Select an option:")

            if cli_input not in cliOptions.keys():
                print("invalid input!")
            else:
                return cliOptions[cli_input]


    @staticmethod
    def stop()->bool:
        return False



# CLI For local devs
class DeveloperCLI(CLI):

    def __init__(self):
        super().__init__()

    developer_options: dict = {
        "app_workbench": "workbench"
    }

    @staticmethod
    def welcome():
        DeveloperCLI.author_header()
        print("Welcome to ZPy Developer CLI!")
        print("Below are command line options for this automation")

    @staticmethod
    def run():
        DeveloperCLI.welcome()
        return DeveloperCLI.get_input(cliOptions = DeveloperCLI.developer_options)