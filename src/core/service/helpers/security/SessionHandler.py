from flask import session
from datetime import datetime
class SessionInfo():

    def __init__(self, u: {}, token: str):
        self.user=u
        self.token=token
        self.when_created=datetime.now()

    def serialize(self):
        return {
            "user" : self.user,
            "token" : self.token,
            "when_created" : self.when_created
        }
class SessionHandler():

    exp_day_policy: int = 7
    exp_seconds_policy: int =0


    def __init__(self):
        pass

    @staticmethod
    def nsession(u: {}, token)->None:
        if SessionHandler.session_exists(uid=u["uid"]):
            SessionHandler.clear_user_session(uid=u["uid"])

        session[u["uid"]]=SessionInfo(u=u, token=token).serialize()

    @staticmethod
    def get_user_session(uid)->SessionInfo:
        if SessionHandler.session_exists(uid):
            return session[str(uid)]
        else:
            return None

    @staticmethod
    def validate_session(uid)->bool:
        return (SessionHandler.session_exists(uid) and SessionHandler.is_timed_out(uid))

    @staticmethod
    def session_exists(uid)->bool:
        if str(uid) in session.keys():
            return True
        else:
            return False
    @staticmethod
    def clear_user_session( uid: int)->None:
        session.pop(str(uid))
        return

    @staticmethod
    def is_timed_out(uid)->bool:
        s=SessionHandler.get_user_session(uid)
        if s is None:
            return True
        else:
            dif = (datetime.now() - s.when_created)
            if (dif.days > SessionHandler.exp_day_policy) and (dif.seconds > SessionHandler.exp_seconds_policy):
                SessionHandler.clear_user_session(uid=uid)
                return True
            else:
                return False