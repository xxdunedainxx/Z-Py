from .IConnector import IConnector
from ...conf.ServiceConfig import ServiceConfig
class Connector(IConnector):

    def __init__(self,connectorConfig: ServiceConfig):
        super().__init__(connectorConfig=connectorConfig)

