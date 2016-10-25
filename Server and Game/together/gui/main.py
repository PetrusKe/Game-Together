# coding=utf-8
import socket
import threading
from tkinter import *
from game.plane_war.run_plane_fight import run

from server.game_server import Server


class GameMenu:

    def __init__(self):
        """
        Init the game menu.
        """
        self.game_win = Tk()
        self.choose_label = Label(self.game_win, text='Choose game:')
        self.plane_war_button = Button(self.game_win, text='Plane War', command=self.start_plane_war)

    def start(self):
        """
        Start the server
        :return:
        """
        self.game_win.title('Together')
        self.game_win.geometry('300x300+300+300')
        mess = 'Server IP:', socket.gethostbyname(socket.gethostname())
        ip_label = Label(self.game_win, text=mess)

        ip_label.pack()
        self.choose_label.pack()
        self.plane_war_button.pack()

        mainloop()

    def start_plane_war(self):
        """
        Start the game
        :return:
        """
        server = Server()
        server_thread = threading.Thread(target=server.server_start)
        game_thread = threading.Thread(target=run, args=(server,))
        server_thread.start()
        game_thread.start()
        prompt_label = Label(self.game_win, text='wait for phone connect...')
        prompt_label.pack()
        self.plane_war_button['state'] = 'disabled'


if __name__ == '__main__':
    game = GameMenu()
    game.start()
