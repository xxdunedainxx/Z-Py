from ..Connector import Connector
from ....conf.ServiceConfig import ServiceConfig
class DirectorySystem(Connector):

    def __init__(self,connectorConfig: ServiceConfig):
        super().__init__(connectorConfig=connectorConfig)

