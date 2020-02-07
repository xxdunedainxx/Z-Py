#region Custom Libraries
from .JwtAuth import JwtAuth, JwtAuthMsg
from ..HelperCore import Helper
from ...connectors.db_client.IDBClient import IDBClient
from ...connectors.directory.DirectorySystem import DirectorySystem
from .....data.models.user.permission import Permission, permission_rank_check
from .....data.models.user.user import User
from .....data.models.auth.sources import AuthSources
from ....conf.ServiceConfig import ServiceConfig
from ....util.ErrorFactory.GeneralErrors import errorStackTrace
from ....util.Logging.LogFactory import LogFactory
from ....service.api.IAPICore import IAPI
from ....util.app.ErrorFactory.api.CoreInternalError import AuthenticationRequired
from .SessionHandler import SessionHandler, SessionInfo
from ...IServiceCore import IService
#endregion
#region Python imports
import jwt
from functools import wraps
from flask import request
#endregion
#region AuthDriver Interface
class AuthDriver():
    def __init__(self):
        pass

    def authenticate(self, u: User,targetPermission: Permission):
        pass

    def login(self, uname: str, pw: str):
        pass

#endregion
#region AD - Auth Driver
class AD(AuthDriver):
    def __init__(self, dirSystem: DirectorySystem):
        super().__init__()
        self.__dir_system: DirectorySystem = dirSystem

    def authenticate(self, u: User,argetPermission: Permission):
        if u.is_admin():
            return True
        else:
            return False

    def __grab_relevant_groups(self):
        pass

    def group_access_check(self, user, grp):
        pass

    def login(self, uname: str, pw: str):
        pass
#endregion
#region Local - Auth Driver
class local(AuthDriver):
    def __init__(self, db: IDBClient):
        super().__init__()
        self.__db=db


    def authenticate(self, u: User, targetPermission: Permission):
        if u.is_admin():
            return True
        else:
            return permission_rank_check(targetRequirement=targetPermission,userProvidedPrivileges=u.permissions)

    def login(self, uname: str, pw: str)->User:
        if User.pw_check(db=self.__db,email=uname, password=pw) is True:
            get_user=User.get_user_email(db=self.__db, email=uname)
            permissions=Permission.get_user_permissions(db=self.__db, uid=get_user.uid)
            get_user.init_perms(permissions=permissions)
            return get_user
        else:
            return None
#endregion
#region Authenticator
class Authenticator(Helper):


    def __init__(self, config: ServiceConfig, services: [IService] = None):
        self.__auth_sources: {AuthDriver} = {}
        super().__init__(helperConfig=config)

        if services is not None:
            for svc in services:
                if issubclass(type(svc),IDBClient):
                    self.__db=svc
                    self.__auth_sources["local"] = local(db=svc)
                    self.__ad = svc
                    self.__auth_sources["AD"] = AD(dirSystem=svc)
                else:
                    self._log.write_log(data=f"Type {str(type(svc))} is not a supported auth driver", level=LogFactory.warning)

    def login(self, email: str, password: str):
        src_check=User.src_check(db=self.__db, email=email)
        if src_check in self.__auth_sources.keys() and AuthSources.check_enabled_auth_source(db=self.__db,src=src_check):
            user=self.__auth_sources[src_check].login(
                uname=email,
                pw=password
            )
            if user is not None:
                jtoken=JwtAuth.encode_auth_token(custom_fields={"user_info":user.serialize()})
                SessionHandler.nsession(u=user.serialize(), token=jtoken)
                return jtoken
            else:
                return None
        else:
            raise Exception(f"auth source for user {email} does not exist, or is not enabled :: {src_check}")

    # Custom Auth Check Decorator, ensures they have a valid jwt token && session
    def authenticate(self, token: str = None, permissionReq: Permission = None):
        def auth_check_decorate(api, authcontroller=self):
            @wraps(api)
            def auth( *args, **kwargs):
                try:
                    jtoken: JwtAuthMsg=JwtAuth.decode_auth_token(auth_token=token if token is not None else request.headers.get('X-Authentication'))
                    if jtoken.authd is False:
                        return AuthenticationRequired()

                    uinfo=User.deserialize(jtoken.info["user_info"])
                    if (permissionReq is None or self.__auth_sources[uinfo.source].authenticate(u=uinfo, targetPermission=permissionReq)):
                        return api(*args,**kwargs)
                    else:
                        return AuthenticationRequired()
                except Exception as e:
                    authcontroller._log.write_log(
                        data=f"Auth check failed {errorStackTrace(e)}",
                        level=LogFactory.error
                    )
                    return {"message" : "internal server error"}, 500
            return auth
        return auth_check_decorate
#endregion