# coding=utf-8
import pygame
from gameobjects.vector2 import Vector2

from game.plane_war.game_entity import GameEntity
from game.plane_war.global_var import PROJECT_PATH

bullet_im = pygame.image.load((PROJECT_PATH + '/game/plane_war/resources/images/bullet.png'))  # TODO 修改图片


class Bullet(GameEntity):
    def __init__(self, name, shot_pos):
        GameEntity.__init__(self, name, speed=200)
        self.pos = shot_pos
        self.image = bullet_im

    def move(self, time_passed, dist=Vector2(0, -1)):
        self.pos += time_passed * self.speed * dist
