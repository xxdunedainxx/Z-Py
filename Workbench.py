# Override to something
override = "workbench"

# General App Workbench testing
from src.build.ApplicationCLI import DeveloperCLI

def workbench():
    from src.workbench.main.app import ApplicationWorkbench

def run_cli():
    method=globals()[DeveloperCLI.run()]

    method()
if override is None:
    run_cli()
else:
    print("blah")
    #method = globals()[override]()

class ReusablePool:
    """
    Manage Reusable objects for use by Client objects.
    """

    def __init__(self, size):
        self._reusables = [Reusable() for _ in range(size)]

    def acquire(self):
        return self._reusables.pop()

    def release(self, reusable):
        self._reusables.append(reusable)


class Reusable:
    """
    Collaborate with other objects for a limited amount of time, then
    they are no longer needed for that collaboration.
    """

    pass


# Singleton/ClassVariableSingleton.py
class SingleTone(object):
    __instance = None

    def __dispatch_object(self):
        return object.__new__(self)

    def __new__(self, **kwargs):
        if "singleton" in kwargs["args"].keys() and kwargs["args"]["singleton"] == True:
            # Singleton gate
            if SingleTone.__instance is None:
                SingleTone.__instance = self.__dispatch_object(self)
            return SingleTone.__instance
        else:
            return self.__dispatch_object(self)

class TestPoly():
    def __new__(self, **kwargs):
        self.test_poly="test"
        return object.__new__(self)

class PolymorphicGate(SingleTone,TestPoly):
    ObjectOverrides: dict = {
        "singleton" : SingleTone,
        "testpoly" : TestPoly
    }

    def __polymorphic_evolution(self,**kwargs)->tuple:
        t=tuple()
        types=kwargs["polymorphic_evolution"] if "polymorphic_evolution" in kwargs.keys() else None

        if types is None:
            return t

        for type in types:
            if type in PolymorphicGate.ObjectOverrides.keys():
                t = t + (PolymorphicGate.ObjectOverrides[type].__new__(self,kwargs),)
        return t

    def __new__(self, **kwargs):
        polymorphicTuple: tuple = (object.__new__(self), self.__polymorphic_evolution(self,kwargs))
        return polymorphicTuple
class Test(PolymorphicGate):

    def __init__(self, args:{}):
        print("singleton test")



t=Test(args={"polymorphic_evolution" : ["singleton"]})
print(t)
t2=Test(args={"polymorphic_evolution" : ["singleton"]})
t3=Test(args={"singleton" : False})
print(t2)
print(t3)
print(isinstance(t3,SingleTone))
exit(0)
