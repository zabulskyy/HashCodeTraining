from solution import Solution

class Writer:

    def write(self, solution):
        """
        :param solution: Solution to be written
         @type solution: Solution
        :return:
        """
        raise Exception("Need to implement 'write' method")

class ConsoleWriter(Writer):

    def write(self, solution):
        """
        :param solution: Solution to be written
         @type solution: Solution
        :return:
        """
        raise Exception("Need to implement 'write' method")

class FileWriter(Writer):

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, solution):
        """
        :param solution: Solution to be written
         @type solution: Solution
        :return:
        """
        f = open(self.file_name, 'w')
        # TODO: add your soltuion's writing
        f.close()