from ..model import Model
from ....core.service.connectors.db_client.IDBClient import IDBClient
class AuthSources(Model):

    def __init__(self, srcname: str, enabled: int ):
        super().__init__()
        self.srcname= srcname
        self.enabled=enabled

    def serialize(self):
        return {
            "src" : self.srcname,
            "enabled" : self.enabled
        }

    @staticmethod
    def get_all_auth_sources(db: IDBClient):
        authsources=db.executeQuery(
            query="SELECT value,enabled FROM user_source"
        )

        if len(authsources) == 0:
            return None
        else:
            rSources: [AuthSources]=[]
            for src in authsources:
                rSources.append(
                    AuthSources(
                        srcname=src[0],
                        enabled=src[1]
                    )
                )
            return rSources

    @staticmethod
    def check_enabled_auth_source(db: IDBClient, src: str):
        authsources=db.executeQuery(
            "SELECT 1 FROM user_source where enabled=1 and value=%s",
            src
        )

        if len(authsources) == 0:
            return False
        else:
            return True
    @staticmethod
    def get_all_enabled_auth_sources(db: IDBClient):
        authsources=db.executeQuery(
            query="SELECT value,enabled FROM user_source where enabled=1"
        )

        if len(authsources) == 0:
            return None
        else:
            rSources: [AuthSources]=[]
            for src in authsources:
                rSources.append(
                    AuthSources(
                        srcname=src[0],
                        enabled=src[1]
                    )
                )
            return rSources