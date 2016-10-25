from ant_fighting.game_entity import GameEntity
from ant_fighting.state import *


class Ant(GameEntity):
    def __init__(self, world, image):
        # 执行父类构造方法
        GameEntity.__init__(self, world, 'ant', image)
        # 创建各种状态
        exploring_state = AntStateExploring(self)
        seeking_state = AntStateSeeking(self)
        delivering_state = AntStateDelivering(self)
        hunting_state = AntStateHunting(self)

        self.brain.add_state(exploring_state)
        self.brain.add_state(seeking_state)
        self.brain.add_state(delivering_state)
        self.brain.add_state(hunting_state)
        self.carry_image = None

    def carry(self, image):
        # 搬运物品的贴图
        self.carry_image = image

    def drop(self, surface):
        # 放下carry图像
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x - w, y - h / 2))
            self.carry_image = None

    def render(self, surface):
        # 调用父类方法添加对象贴图
        GameEntity.render(self, surface)
        # 额外绘制carry_image
        if self.carry_image:
            x, y = self.location
            w, h = self.carry_image.get_size()
            surface.blit(self.carry_image, (x - w, y - h / 2))
