from random import randint

from gameobjects.vector2 import Vector2

from ant_fighting.global_var import *


class State():
    def __init__(self, name):
        self.name = name

    def do_actions(self):
        pass

    def check_conditions(self):
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


class AntStateExploring(State):
    """状态：探索"""

    def __init__(self, ant):
        State.__init__(self, 'exploring')
        self.ant = ant

    # 移动到随机目的地
    def random_destination(self):
        w, h = SCREEN_SIZE
        self.ant.destination = Vector2(randint(0, w), randint(0, h))

    # 随机是否进行移动
    def do_actions(self):
        if randint(1, 20) == 1:
            self.random_destination()

    # 检查状态
    def check_conditions(self):
        leaf = self.ant.world.get_close_entity('leaf', self.ant.location)
        # 如果附近有树叶
        if leaf is not None:
            self.ant.leaf_id = leaf.id
            return 'seeking'
        spider = self.ant.world.get_close_entity('spider', NEST_POSITION, NEST_SIZE)
        # 如果蜘蛛到了巢穴中
        if spider is not None:
            if self.ant.location.get_distance_to(spider.location) < 100:
                self.ant.spider_id = spider.id
                return 'hunting'
        return None

    # 设置速度并让其移动
    def entry_actions(self):
        self.ant.speed = 120 + randint(-30, 30)
        self.random_destination()


class AntStateSeeking(State):
    """
    状态：寻找
    """

    def __init__(self, ant):
        State.__init__(self, 'seeking')
        self.ant = ant
        self.lead_id = None

    def check_conditions(self):
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is None:
            return 'exploring'
        if self.ant.location.get_distance_to(leaf.location) < 5.0:
            self.ant.carry(leaf.image)
            self.ant.world.remove_entity(leaf)
            return 'delivering'
        return None

    def entry_actions(self):
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf is not None:
            self.ant.destination = leaf.location
            self.ant.speed = 160 + randint(-20, 20)


class AntStateDelivering(State):
    """
    状态：运输
    """

    def __init__(self, ant):
        State.__init__(self, 'delivering')
        self.ant = ant

    def check_conditions(self):
        if Vector2(NEST_POSITION).get_distance_to(self.ant.location) < NEST_SIZE:
            if randint(1, 10) == 1:
                self.ant.drop(self.ant.world.background)
                return 'exploring'
        return None

    def entry_actions(self):
        self.ant.speed = 60
        random_offset = Vector2(randint(-20, 20), randint(-20, 20))
        self.ant.destination = Vector2(NEST_POSITION) + random_offset


class AntStateHunting(State):
    """
    状态：攻击
    """

    def __init__(self, ant):
        State.__init__(self, 'hunting')
        self.ant = ant
        self.got_kill = False

    def do_actions(self):
        spider = self.ant.world.get(self.ant.spider_id)
        if spider is None:
            return
        self.ant.destination = spider.location
        if self.ant.location.get_distance_to(spider.location) < 15:
            if randint(1, 5) == 1:
                spider.bitten()
                if spider.health <= 0:
                    self.ant.carry(spider.image)
                    self.ant.world.remove_entity(spider)
                    self.got_kill = True

    def check_conditions(self):
        if self.got_kill:
            return 'delivering'
        spider = self.ant.world.get(self.ant.spider_id)
        if spider is None:
            return 'exploring'
        if spider.location.get_distance_to(NEST_POSITION) > NEST_SIZE * 3:
            return 'exploring'
        return None

    def entry_actions(self):
        self.speed = 160 + randint(0, 50)

    def exit_actions(self):
        self.got_kill = False


class StateMachine():
    def __init__(self):
        self.states = {}  # 存储状态
        self.active_state = None  # 当前有效状态

    def add_state(self, state):
        self.states[state.name] = state

    # 检查当前有效状态并执行
    def think(self):
        if self.active_state is None:
            return
        # 如果有状态，执行
        self.active_state.do_actions()
        # 检查条件
        new_state_name = self.active_state.check_conditions()
        # 如果有状态转换条件
        if new_state_name is not None:
            self.set_state(new_state_name)

    # 设置进入下一个转台
    def set_state(self, new_state_name):
        # 如果当前有状态，退出此状态
        if self.active_state is not None:
            self.active_state.exit_actions()
        # 设置为新的状态
        self.active_state = self.states[new_state_name]
        # 将此状态添加到记录中
        self.active_state.entry_actions()
