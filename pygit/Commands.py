#commands class to handle the commands and execution of commands

#imports


class Commands:
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
    def __str__(self):
        return ('Commands {} {}'.format(self.name,self.dir) )

    def __init__(self, argumnets):
        self.arguments = argumnets
        Commands.recognize_commands(self.arguments)
    def recognize_commands(self, arguments):
        self.arguments = arguments
        print('here')
    @staticmethod
    def push():
        pass

