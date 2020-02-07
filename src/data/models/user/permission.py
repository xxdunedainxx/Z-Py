from ..model import Model
from ....core.service.connectors.db_client.IDBClient import IDBClient


class Permission(Model):



    PERMISSION_RANKS = {
        "admin" : 1,
        "write" : 2,
        "read" : 3,
        "guest" : 4
    }


    def __init__(self, uid: int, value: str, permissionType: str = "Client"):
        super().__init__()
        self.uid=uid
        self.value=value
        self.permission_type=permissionType

    def serialize(self):
        return {
            "uid" : self.uid,
            "value" : self.value
        }

    @staticmethod
    def deserialize(info):
        return Permission(
            uid=info["uid"] if "uid" in info.keys() else "",
            value=info["value"] if "value" in info.keys() else ""
        )

    @staticmethod
    def get_user_permissions(db: IDBClient, uid: int):
        perms=db.executeQuery(
            "select value from permission where uid=%s",
            uid
        )
        rperms: [Permission] = []
        for p in perms:
            rperms.append(
                Permission(
                    uid=uid,
                    value=p[0]
                )
            )
        return rperms

def permission_rank_check(targetRequirement: Permission, userProvidedPrivileges: [Permission]):
    for permission in userProvidedPrivileges:
        if targetRequirement.value in Permission.PERMISSION_RANKS.keys() and permission.value in Permission.PERMISSION_RANKS.keys() and \
                Permission.PERMISSION_RANKS[permission.value] <= Permission.PERMISSION_RANKS[targetRequirement.value]:
            return True
    return False