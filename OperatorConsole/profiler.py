class profiler:
    """
    Manages execution time data from various parts of the program. Value is a
    dictionary, where the key is the name of the calling part of the progam
    (or some other relevant label) and the value is the execution time. If the
    key isn't in the dictionary it will be added automatically.
    """
    profiles = {}  # the dictionary storing all the exec time values

    def __init__(self):
        pass

    def add(self, profile):
        try:
            self.profiles.update(profile)
        except:
            pass

    def toString(self):
        msg = ""
        for key in self.profiles:
            msg += "{}: {}ms\n".format(key, float('%.3f' %
                                       (self.profiles[key]*1000.0)))
        return msg
