# coding=utf-8
class PhoneData:
    """存放和手机端有关的信息"""
    movelist = [0.0, 0.0, 0.0]
    client_threads = []

    @classmethod
    def setMoveData(cls, num_x, num_y, num_z):
        cls.movelist = [num_x, num_y, num_z]

    @classmethod
    def getMoveData(cls):
        return cls.movelist

    @classmethod
    def addClientThread(cls, thread):
        cls.client_threads.append(thread)

    @classmethod
    def getClientThread(cls):
        return cls.client_threads
