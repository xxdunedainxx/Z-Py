import random
import string

class RandomStringGenerator():

    rand_string_methods = [
        string.ascii_letters,
        string.hexdigits,
        string.octdigits,
        string.digits
    ]

    def __init__(self):
        pass

    @staticmethod
    def grab_random_character():
        return (random.choice(
                RandomStringGenerator.rand_string_methods[random.randint(0,len(RandomStringGenerator.rand_string_methods) - 1)]
            )
        )

    @staticmethod
    def random_string(strlen = 15):
        rstring=''

        for i in range(strlen):
            rstring+=RandomStringGenerator.grab_random_character()

        return rstring