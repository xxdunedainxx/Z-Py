#region Python imports
from threading import Lock
#endregion
#region @lockable_resource
def lockable_resource(mutex: Lock, *args, **kwargs):
    def wrap(method):
        def lock_logic(*args, **kwargs):
            mutex.acquire()
            method(*args, **kwargs)
            mutex.release()
        return lock_logic
    return wrap
#endregion