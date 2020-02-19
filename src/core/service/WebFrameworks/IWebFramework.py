from ..ServiceCore import Service
from .WebFrameworkConfig import WebFrameworkConfig

class IWebFramework(Service):

    def __init__(self, config: WebFrameworkConfig):
        super().__init__(config)

        if config.buildAndRun:
            self.__build_and_run()
        else:
            self.build()

    def _configure_api_services(self):
        pass

    def _grab_api_services(self):
        pass

    def _configure_security_layer(self):
        pass

    def build(self):
        pass

    def run(self):
        pass

    def __build_and_run(self):
        self.build()

        self.run()