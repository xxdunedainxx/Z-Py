#region Basic info
# Download reddis https://redis.io/download
#pip install redis
# redis-server
# redis-client
#endregion
#region Python imports
from redis import Redis
import json
#endregion
#region Custom Classes import
from ...Networking.TCP.Telnet import TelnetClient
#endregion
#region RedisClient
class RedisClient(Redis):
    SUPPORTED_TYPES: {} = {
        'json' : 'json_serialize',
        'txt'  : 'txt_serialize'
    }


    #region Constructor and constructor helpers
    def __init__(self,host: str,port: int, db,cacheType: str = 'json', *args, **kwargs):
        self.__cacheType: str = ''
        self.__pre_flight_check(host, port)
        self.__type_check(type=cacheType)
        super().__init__(host, port, db, *args, **kwargs)


    def __pre_flight_check(self, host: str, port: int)->None:
        if TelnetClient.ping(host,port):
            return
        else:
            raise RedisClient.RedisHostNotAvailable(host,port)

    def __type_check(self, type: str)->None:
        if type in RedisClient.SUPPORTED_TYPES.keys():
            self.__cacheType = type
            return
        else:
            raise RedisClient.InvalidCacheType(type)
    #endregion
    #region Serializers
    @staticmethod
    def json_serialize(bs: bytes)->dict:
        return (
            json.loads(
                bs.decode("utf-8")
            )
        )
    @staticmethod
    def txt_serialize(bs: bytes):
        return bs.decode("utf-8")

    def __serialize_by_type(self, bs: bytes):
        serializer = getattr(self, self.SUPPORTED_TYPES[self.__cacheType])
        return serializer(bs)
    #endregion
    #region fetch_object
    def fetch_object(self, key: str):
        find: bytes = self.get(key)
        return self.__serialize_by_type(find)
    #endregion
    #region Errors
    class InvalidCacheType(Exception):
        def __init__(self, type):
            Exception.__init__(self, f"Type \'{type}\' not supported! These are supported: {str(RedisClient.SUPPORTED_TYPES)}")
    class RedisHostNotAvailable(Exception):
        def __init__(self, host, port):
            Exception.__init__(self, f"Host \'{host}\' on {str(port)}, is not available!")
    #endregion
#endregion
#region Examples
"""r = RedisClient(host='localhost', port=6379, db=0)
print(r.ping())
print(r.keys())
r.set('foo', "{\"bar\" : \"something\"}")
js = r.fetch_object('foo')"""
#endregion