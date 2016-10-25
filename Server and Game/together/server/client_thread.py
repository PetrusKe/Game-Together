import threading


class ClientThread(threading.Thread):
    def __init__(self, func, args, name=''):
        """
        Init thread
        :param func:
        :param args:
        :param name:
        """
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        """
        Start thread
        :return:
        """
        print("%s thread start...\n" % self.name)
        self.func(*self.args)
