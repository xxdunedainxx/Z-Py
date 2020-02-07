from ..conf.Configuration import Configuration

class IService():

    def __init__(self, serviceConfig: Configuration=None):
        pass

    def _validate_config(self,config: Configuration):
        pass

    def _setup_service_logger(self):
        pass

    def service_output(self):
        pass

    def dispose(self):
        pass

    def credential(self):
        pass