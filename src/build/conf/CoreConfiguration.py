import json
from ...core.util.app.ErrorFactory.build.BuildErrors import MissingConfiguration,RequiredFileNotFound,RootNamespaceNotSpecified
class CoreConfiguration():

    def __init__(self, file: str="./conf/build.json"):
        # supported python version
        self.python_version: str = None

        # Library requirements
        self.library_requirements: [str] = None

        # referenced git submodules
        self.submodules: [] = None

        # Logging Configuration
        self.core_logging_file: str = None
        self.core_logging_level: str = None

        self.service_configs: {} = None
        self.root_namespace: str = None



        self._init_config(file=file)

    def _init_config(self, file: str):
        try:
            get_file=json.load(
                open(file,'r')
            )
            print(get_file['_comments'])

            self.python_version=(get_file['python_version'])

            # Library requirements
            self.library_requirements=get_file['library_requirements']
            self.submodules=get_file["submodules"]
            self.service_configs=get_file["services"]
            self.root_namespace=get_file["services"]["root_namespace"]

            # Logging Configuration
            self.core_logging_file=get_file['logging']['core_logging_file']
            self.core_logging_level=get_file['logging']['core_logging_level']

            


        except KeyError as e:
            raise MissingConfiguration(
                file=file,
                config=str(e.args)
            )
        except FileNotFoundError:
            raise RequiredFileNotFound(
                file=file
            )
        except Exception as e:
            raise e

