from random import randint
import pygame

from gameobjects.vector2 import Vector2
from ant_fighting.ant import Ant
from ant_fighting.global_var import *
from ant_fighting.leaf import Leaf
from ant_fighting.spider import Spider
from ant_fighting.world import World
from pygame.locals import *


def run():
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    world = World()
    w, h = SCREEN_SIZE
    clock = pygame.time.Clock()

    ant_image = pygame.image.load("resources/images/ant.png").convert_alpha()
    leaf_image = pygame.image.load("resources/images/leaf.png").convert_alpha()
    spider_image = pygame.image.load("resources/images/spider.png").convert_alpha()

    for ant_no in range(ANT_COUNT):
        ant = Ant(world, ant_image)
        ant.location = Vector2(randint(0, w), randint(0, h))
        ant.brain.set_state('exploring')
        world.add_entity(ant)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # 这个可以的
                return
        time_passed = clock.tick(61) / 1000
        if randint(1, 10) == 1:
            leaf = Leaf(world, leaf_image)
            leaf.location = Vector2(randint(0, w), randint(0, h))
            world.add_entity(leaf)

        if randint(1, 100) == 1:
            spider = Spider(world, spider_image)
            spider.location = Vector2(-50, randint(0, h))
            spider.destination = Vector2(w + 50, randint(0, h))
            world.add_entity(spider)

        world.process(time_passed)
        world.render(screen)

        pygame.display.update()


if __name__ == '__main__':
    run()
