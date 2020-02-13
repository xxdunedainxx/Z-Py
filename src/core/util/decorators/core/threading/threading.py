#region @threaded
def threaded(method: any, *args, **kwargs):
    def wrap(method):
        def thread_logic(*args, **kwargs):
            from threading import Thread
            Thread = Thread(target=method, args=(args, kwargs))
        return thread_logic()
    return wrap
#endregion