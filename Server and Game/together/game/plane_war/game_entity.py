# coding=utf-8
import pygame
from gameobjects.vector2 import Vector2


class GameEntity:
    def __init__(self, name, speed):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = None
        self.speed = speed
        self.pos = Vector2(0, 0)

    def draw(self, surface):
        x, y = self.pos
        surface.blit(self.image, (x, y))

    def move(self, time_passed, dist=Vector2(0, 0)):
        pass
