from .IServiceCore import IService
from ..conf.ServiceConfig import ServiceConfig
from ..util.Logging.LogFactory import LogFactory

class Service(IService):

    def __init__(self, serviceConfig: ServiceConfig = None):
        super().__init__(serviceConfig)
        if serviceConfig is None:
            raise Exception("Service config not provided!!")
        else:
            self._validate_config(config=serviceConfig)
            self._setup_service_logger()
            self.service_output()

    def _validate_config(self,config: ServiceConfig):
        config.initialize_config()
        self._service_config=config

    """
    Sets up logging for a specific Service
    """
    def _setup_service_logger(self):
        if self._service_config.logging_enabled:
            self._log=LogFactory(file=self._service_config.log_file,
                                 log_level=self._service_config.log_level)

    """
    Simple output helper for local debugging 
    """
    def service_output(self):
        if self._service_config.dev_mode_enabled:
            print(f"Service: {self._service_config.svc_name}")
            print(f"Description: {self._service_config.svc_description}")
            print(f"Version: {self._service_config.svc_version}")
            print(f"Namespace: {self._service_config.svc_namespace}")
            print(f"Authors: {str(self._service_config.authors)}")
            print(f"Last updated: {self._service_config.last_update}")
            print(f"{self._service_config.default_output_header}")

    """
    this method is currently not in use
    """
    def credential(self):
        pass

    """
    
    """
    def auto_generate_python_file(self):
        pass