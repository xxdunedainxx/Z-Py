class RequiredFileNotFound(Exception):
    def __init__(self,file):
        Exception.__init__(self,f"Required File was not found {file}.")
class MissingConfiguration(Exception):
    def __init__(self,file,config):
        Exception.__init__(self,f"Failed to build project. {config} is missing from {file}")

class BuildFailure(Exception):
    def __init__(self,msg):
        Exception.__init__(self,f"Build failed with error {msg}")

class RootNamespaceNotSpecified(Exception):
    def __init__(self):
        Exception.__init__(self,"Root namespace not specified in build json! Under services.root_namespace")