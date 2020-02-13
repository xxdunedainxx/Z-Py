class IReusable:
    pass

class ReusablePool(object):
    """
    Manage Reusable objects for use by Client objects.
    """

    def __init__(self, size):
        self.__capacity = size
        self.__reusables = [IReusable() for _ in range(size)]

    def acquire(self):
        return self.__reusables.pop()

    def release(self, reusable: IReusable):
        if len(self.__reusables) == self.__capacity:
            raise ("Reusable pool size met")
        else:
            self.__reusables.append(reusable)