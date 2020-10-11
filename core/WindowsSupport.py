#imports

class WindowsSupport(object):
    def __init__(self, activate=False):
        self.activate = activate
        if self.activate == False:
            print('Windows Support disabled')