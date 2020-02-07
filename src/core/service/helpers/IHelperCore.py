from ..ServiceCore import Service
from ...conf.ServiceConfig import ServiceConfig
class IHelper(Service):

    def __init__(self,helperConfig: ServiceConfig):
        super().__init__(serviceConfig=helperConfig)

