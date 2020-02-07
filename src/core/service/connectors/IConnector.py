from ..ServiceCore import Service
from ...conf.ServiceConfig import ServiceConfig
class IConnector(Service):

    def __init__(self,connectorConfig: ServiceConfig):
        super().__init__(serviceConfig=connectorConfig)

