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


def eval_kwargs(itemToCheck, evalItemTruth = False, **kwargs)->bool:
    if kwargs is dict and "args" in kwargs.keys() and itemToCheck in kwargs.keys() and (evalItemTruth == False or kwargs["args"][itemToCheck] == True ):
        return True
    else:
        return False


# Singleton/ClassVariableSingleton.py
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

class TestPoly():
    def __new__(cls, **kwargs):
        cls.test_poly="test"
        return object.__new__(cls)

class PolymorphicGate(SingleTone,TestPoly):
    ObjectOverrides: dict = {
        "singleton" : SingleTone,
        "testpoly" : TestPoly
    }

    def __polymorphic_evolution(self,**kwargs)->tuple:
        types=kwargs['kwargs']["polymorphic_evolution"] if "kwargs" in kwargs.keys() and "polymorphic_evolution" in kwargs['kwargs'].keys() else None

        if types is None:
            return object.__new__(self)
        elif "singleton" not in types:
            t = (object.__new__(self),)
        elif self.ping_singleton(self):
            t = tuple()
        else:
            return (self.get_singleton(self),)


        for type in types:
            if type in PolymorphicGate.ObjectOverrides.keys():
                t = t + (PolymorphicGate.ObjectOverrides[type].__new__(PolymorphicGate.ObjectOverrides[type], **kwargs),)
        return t

    def __new__(cls, **kwargs):
        additional_args= cls.__polymorphic_evolution(cls, kwargs=kwargs["args"])
        polymorphicTuple: tuple = (additional_args,)
        return polymorphicTuple
class Test(PolymorphicGate):

    def __new__(cls, **kwargs):
        super(Test,cls).__new__(cls, **kwargs)
        print("blah")
        return cls.__init__(cls,args=kwargs)


    def __init__(self, args:{}):
        print("singleton test")
        super(Test,self).__init__(args)
        print("blah")
        return self



t=Test(args={"polymorphic_evolution" : ["singleton", "testpoly"]})
print(t)
t.test_poly="bla blah blah"
t2=Test(args={"polymorphic_evolution" : ["singleton", "testpoly"]})
t3=Test(args={"polymorphic_evolution" : [ "testpoly"]})
print(hex(id(t)))
print(hex(id(t2)))
print(hex(id(t3)))
t3.test_poly = "hey there"
print(isinstance(t3,SingleTone))
print(isinstance(t,SingleTone))
print(isinstance(t2,SingleTone))
exit(0)
