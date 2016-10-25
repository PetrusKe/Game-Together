# coding=utf-8
import re
import socket

from game.plane_war.phone_data import PhoneData
from server.client_thread import ClientThread


class Server:
    def __init__(self):
        """
        Init Server
        """
        self.local_ip = socket.gethostbyname(socket.gethostname())
        self.local_port = 9999
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = 0
        self.client_list = []

    def server_start(self):
        """
        Start server
        :return:
        """
        self.server.bind((self.local_ip, self.local_port))
        self.server.listen(5)

        client_num = 1

        while True:
            print("[*] Listening on %s:%d" % (self.local_ip, self.local_port))
            print('[*] Waiting for connection...')
            client, addr = self.server.accept()
            self.client_list.append(client)
            print('[*] Accepted connection from %s:%d' % (addr[0], addr[1]))
            self.running = 1
            t = ClientThread(self.client_handle, (client,), ('client: %d' % client_num))
            PhoneData.addClientThread(t)
            client_num += 1
            t.start()

    def server_close(self):
        """
        Close server
        :return:
        """
        self.server.close()

    def client_handle(self, client_socket):
        """
        Judge how to control game
        :param client_socket:
        :return:
        """
        # 获取模式信息
        mode_req = client_socket.recv(1024).decode()
        # TODO 不同模式选择不同操作
        mess = ('Mode:' + mode_req).encode()
        print(mess)
        client_socket.send(mess)

        while True:
            if not self.running:
                break
            # 获取游戏数据
            request = client_socket.recv(1024).decode()
            print(request)

            var_x = "x=0.0;"
            var_y = "y=0.0;"
            var_z = "z=0.0;"

            if request:
                ma_x = re.search(r'x=((\d+\.\d+)|(-\d+\.\d+));', request)
                ma_y = re.search(r'y=((\d+\.\d+)|(-\d+\.\d+));', request)
                ma_z = re.search(r'z=((\d+\.\d+)|(-\d+\.\d+));', request)
                if ma_x:
                    now_x = ma_x.group()
                else:
                    now_x = var_x
                if ma_y:
                    now_y = ma_y.group()
                else:
                    now_y = var_y
                if ma_z:
                    now_z = ma_z.group()
                else:
                    now_z = var_z
                var_x = now_x
                var_y = now_y
                var_z = now_z

            num_x = float(var_x[2:-1])
            num_y = float(var_y[2:-1])
            num_z = float(var_z[2:-1])
            PhoneData.setMoveData(num_x, num_y, num_z)


if __name__ == '__main__':
    pass
