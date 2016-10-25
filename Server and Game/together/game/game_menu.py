import threading

from game.plane_war.run_plane_fight import run
from server.game_server import Server


def choose_game():
    """
    The game choose window
    :return:
    """
    print('请输入选择的游戏编号：')
    print('1.Plane War')
    choose = input('>>>')
    if choose.isdigit():
        game_number = int(choose)
        if game_number == 1:
            server = Server()
            server_thread = threading.Thread(target=server.server_start)
            game_thread = threading.Thread(target=run, args=(server,))
            server_thread.start()
            game_thread.start()
