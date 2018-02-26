from problem import Problem

class Reader:
    """
    Reads a problem and stores it into Problem object
    """
    def __init__(self):
        pass

    def read(self):
        raise Exception("Need to implement 'read' method")

class ConsoleReader(Reader):
    """
    Reads from console
    """
    def read(self):
        """
        :rtype: Problem
        """
        raise Exception("Need to implement 'read' method")

class FileReader(ConsoleReader):
    """
    Reads from file
    """
    def __init__(self, file_name):
        ConsoleReader.__init__(self)
        self.file_name = file_name

    def read(self):
        """
        :rtype: Problem
        """
        raise Exception("Need to implement 'read' method")
