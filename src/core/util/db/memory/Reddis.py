# Download reddis https://redis.io/download
#pip install redis
# redis-server
# redis-client
# telnetObj=telnetlib.Telnet("localhost",6379)
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.set('foo', 'bar')
r.get('foo')