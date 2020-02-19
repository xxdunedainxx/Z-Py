from ...conf.ServiceConfig import ServiceConfig

class WebFrameworkConfig(ServiceConfig):

    def __init__(self, file):
        self.buildAndRun = True
        super().__init__(file=file)