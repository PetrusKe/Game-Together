from ant_fighting.game_entity import GameEntity


class Leaf(GameEntity):
    def __init__(self, world, image):
        GameEntity.__init__(self, world, 'leaf', image)
