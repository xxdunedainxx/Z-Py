class SingleTone(object):
    __instance = None

    def __dispatch_object(cls):
        return object.__new__(cls)

    def __new__(cls, **kwargs):

        # Singleton gate
        if "kwargs" in kwargs.keys() and "polymorphic_evolution" in kwargs['kwargs'].keys() and "singleton" in kwargs['kwargs']['polymorphic_evolution']:
            if SingleTone.__instance is None:
                SingleTone.__instance = object.__new__(cls)
            return SingleTone.__instance
        else:
            return object.__new__(cls)

    def ping_singleton(self):
        return SingleTone.__instance is None

    def get_singleton(self):
        return SingleTone.__instance