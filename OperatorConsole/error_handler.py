class error_handler:
    """
    manages non-fatal program errors. Errors must be added using errors.add()
    Argument should be a string containing the error message.
    """
    def __init__(self):
        pass

    error_cache = ""

    def add(self, error):
        self.error_cache += "\n"
        self.error_cache += error

    def toString(self):
        if self.isEmpty():
            return("No errors reported")

        return self.error_cache

    def isEmpty(self):
        if self.error_cache == "":
            return True
        else:
            return False
