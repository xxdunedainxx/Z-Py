from ..Connector import Connector
from ....conf.ServiceConfig import ServiceConfig

class IDBClient(Connector):

    def __init__(self, sqlConfig: ServiceConfig, *args):
        super().__init__(sqlConfig)
        # _client can be 'any'
        self._client=object

    def connection(self, *args):
        pass

    def kill_connection(self, *args):
        pass

    def executeQuery(self,query, *args):
        pass

    def fetch_client(self):
        return self._client