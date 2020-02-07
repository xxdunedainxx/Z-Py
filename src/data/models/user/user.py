from .permission import Permission
from ..model import Model
from datetime import datetime
from ....core.service.connectors.db_client.IDBClient import IDBClient
class User(Model):

    def __init__(self, username: str, email: str, password: str, uid: int, enabled: int, source: str, whenGenerated: datetime, permissions: [Permission]=None):

        super().__init__()

        self.username = username
        self.email=email
        self.password=password
        self.uid=uid
        self.enabled=enabled
        self.source=source
        self.whenGenerated=whenGenerated
        self.__isadmin=False
        if permissions is not None:
            self.init_perms(permissions=permissions)



    def init_perms(self, permissions: [Permission]):
        for p in permissions:
            if p.value == 'admin':  # and p.permission_type == 'Client':
                self.__isadmin = True
            else:
                continue
        self.permissions=permissions
    def serialize(self)->{}:
        serializeP=[]
        for p in self.permissions:
            serializeP.append(p.serialize())
        return {
            "username" : self.username,
            "email" : self.email,
            "uid" : self.uid,
            "enabled" : self.enabled,
            "source" : self.source,
            "whenGenerated" : str(self.whenGenerated),
            "permissions" : serializeP,
            "is_admin" : self.__isadmin
        }

    @staticmethod
    def deserialize(info: {}):
        perms: [Permission] = []
        for p in info["permissions"]:
            perms.append(Permission.deserialize(p))
        return User(
            username=info["username"] if "username" in info.keys() else "",
            email=info["email"] if "email" in info.keys() else "",
            password=info["password"] if "password" in info.keys() else "",
            uid=info["uid"] if "uid" in info.keys() else 0,
            enabled=info["enabled"] if "enabled" in info.keys() else -1,
            source=info["source"] if "source" in info.keys() else "",
            whenGenerated=info["whenGenerated"] if "whenGenerated" in info.keys() else "",
            permissions=perms
        )

    def is_admin(self):
        return self.__isadmin
    #region new_user
    @staticmethod
    def new_user(db: IDBClient, username, email, password, src ):
        if User.get_user_email(db=db, email=email) is None:
            db.executeQuery(
                "INSERT INTO site (username,email, password, source, enabled) VALUES (%s,%s,%s,%s,1)",
                (username,email,password,src)
            )
        else:
            raise Exception(f"account with email {email} already exists.")

    #endregion
    #region get_user
    @staticmethod
    def get_user(db: IDBClient, uid: int):
        u=db.executeQuery(
            "select username,email,password,uid,enabled,source,whengenerated from user where uid=%s and enabled=1",
            (uid)
        )
        if len(u) == 0:
            return None
        else:
            return User(
                username=u[0][0],
                email=u[0][1],
                password=u[0][2],
                uid=u[0][3],
                enabled=u[0][4],
                source=u[0][5],
                whenGenerated=u[0][6],
            )
    #endregion
    #region get_user_email
    @staticmethod
    def get_user_email(db: IDBClient, email: str):
        u=db.executeQuery(
            "select username,email,password,uid,enabled,source,whengenerated from user where email=%s and enabled=1",
            (email)
        )
        if len(u) == 0:
            return None
        else:
            return User(
                username=u[0][0],
                email=u[0][1],
                password=u[0][2],
                uid=u[0][3],
                enabled=u[0][4],
                source=u[0][5],
                whenGenerated=u[0][6],
            )
    #endregion
    #region pw_check
    @staticmethod
    def pw_check(db: IDBClient, email: str, password)->bool:
        u=db.executeQuery(
            f"select 1 from user where email=%s and password=%s",
            (email,password,)
        )
        if u is None:
            return False
        else:
            return True
    #endregion
    #region pw_check
    @staticmethod
    def src_check(db: IDBClient, email: str)->str:
        src=db.executeQuery(
            f"select source from user where email=%s",
            (email,)
        )
        if src is None:
            ""
        else:
            return src[0][0]
    #endregion
    #region get_all_users
    @staticmethod
    def get_all_users(db: IDBClient):
        users=db.executeQuery(
            query="select username,email,password,uid,enabled,source,whengenerated from user"
        )

        if len(users) == 0:
            return None
        else:
            rUsers: [User]=[]
            for u in users:
                rUsers.append(
                    User(
                        username=u[0],
                        email=u[1],
                        password=u[2],
                        uid=u[3],
                        enabled=u[4],
                        source=u[5],
                        whenGenerated=u[6],
                    )
                )
            return rUsers
    #endregion

    """
    #region update_location_by_id
    @staticmethod
    def update_user_by_id(db: IDBClient, id, attributes):
        # allowed attributes to update
        # threshold, phone server, voicemail_server,
        try:
            loc = db.executeQuery(f"SELECT * FROM location WHERE id=%s", (id,))
            if loc is None:
                raise DoesNotExistException("Location doesn't exist")
            valid_att = ['name', 'extension_threshold', 'UC_Phone_Server', 'UC_Voicemail_Server']
            query_string = ""
            esc_tuple = ()
            for attribute in attributes:
                if attribute in valid_att:
                    esc_tuple += (attributes[attribute],)
                    query_string += attribute + "=%s,"
            if query_string != "":
                query_string = query_string[:-1]
                esc_tuple += (id,)
                db.executeQuery(f"UPDATE location SET {query_string} WHERE id=%s", esc_tuple)
            else:
                raise AttributeException("No valid attributes entered")

        except Exception as e:
            raise e
    #endregion"""