# coding=utf-8
import pygame
from gameobjects.vector2 import Vector2

from game.plane_war.game_entity import GameEntity
from game.plane_war.global_var import *

plane_front_im = pygame.image.load(PROJECT_PATH + '/game/plane_war/resources/images/plane_front.png')
plane_back_im = pygame.image.load(PROJECT_PATH + '/game/plane_war/resources/images/plane_back.png')


class Plane(GameEntity):
    def __init__(self, name, speed):
        GameEntity.__init__(self, name, speed)
        self.pos = Vector2(SCREEN_SIZE[0] / 2 - 32, SCREEN_SIZE[1] / 2 - 40)
        self.image = plane_front_im
        self.hp = 5

    def move(self, time_passed, dist=Vector2(1, 1)):
        if dist is not None:
            move_distance = self.speed * time_passed * dist
            if dist[1] > -1:
                self.image = plane_back_im
            else:
                self.image = plane_front_im
            self.pos += move_distance

    def border_check(self):
        w, h = SCREEN_SIZE
        x, y = self.pos
        if x <= 0:
            self.pos[0] = 0
        elif x >= w - HERO_SIZE[0]:
            self.pos[0] = w - HERO_SIZE[0]
        if y <= 0:
            self.pos[1] = 0
        elif y >= h - HERO_SIZE[1]:
            self.pos[1] = h - HERO_SIZE[1]

    def crash(self):
        self.hp -= 1
