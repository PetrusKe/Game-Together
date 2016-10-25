# coding=utf-8
from random import randint

import pygame
from gameobjects.vector2 import Vector2

from game.plane_war.game_entity import GameEntity
from game.plane_war.global_var import *

enemy_im = pygame.image.load(PROJECT_PATH + '/game/plane_war/resources/images/enemy.png')


class Enemy(GameEntity):
    def __init__(self, name, speed):
        GameEntity.__init__(self, name, speed)
        self.pos = Vector2(randint(0, SCREEN_SIZE[0] - ENEMY_SIZE[0]), 0)
        self.image = enemy_im

    def move(self, time_passed, dist=Vector2(0, 1)):
        self.pos += time_passed * self.speed * dist
