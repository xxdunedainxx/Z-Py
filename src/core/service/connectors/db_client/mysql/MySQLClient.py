from .....util.db.mysql.client import py_mysql as sql
from ..IDBClient import IDBClient
from .....util.ErrorFactory.GeneralErrors import errorStackTrace
from .....util.Logging.LogFactory import LogFactory
from .....conf.ServiceConfig import ServiceConfig

class MySQLClient(IDBClient):

    def __init__(self, conf: ServiceConfig, autoCommit=False):
        super().__init__(conf)
        if getattr(conf, "conf") is None:
            raise Exception("MySQL Client required a \'conf\' section in the service config")
        else:
            self._conf=conf.conf

        self._client: sql = self.connection(self._conf, conf.auto_commit)
        self._log.write_log(data=f"DB connected!{self.output_db_info()}", level=LogFactory.info)

    def output_db_info(self)->str:
        return f"\nDB INFO |HOST ::{self._conf['host']} | DB :: {self._conf['database']} | "

    def connection(self, conf: {}, autoCommit: bool)->sql:
        return sql(
            config=conf,
            autoCommit=autoCommit
        )

    def kill_connection(self, *args)->None:
        if self._client is None:
            return
        else:
            self._client.killConnection()

    def executeQuery(self,query: str, paramitized: tuple=None, fetchAll: bool=True)->None:
        try:
            return self._client.executeQuery(query, paramitized,fetchAll)
        except Exception as e:
            self._log.write_log(
                data=f"MySQL Client failed with error {errorStackTrace(e)}. query :: {query}",
                level=LogFactory.error
            )
            raise e

    def fetch_client(self)->sql:
        return self._client