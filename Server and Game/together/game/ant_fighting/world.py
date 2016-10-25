import copy

import pygame
from gameobjects.vector2 import Vector2
from ant_fighting.global_var import *


class World:
    def __init__(self):
        self.entities = {}
        self.entity_id = 0
        # 绘制蚁穴
        self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill((255, 255, 255))
        pygame.draw.circle(self.background, (200, 255, 200), NEST_POSITION, int(NEST_SIZE))

    def add_entity(self, entity):
        # 增加一个新的实体
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):
        # 删除一个实体
        del self.entities[entity.id]

    def get(self, entity_id):
        # 通过给出的id找到对应的实体
        if entity_id in self.entities:  # self.entities.keys()?
            return self.entities[entity_id]
        else:
            return None

    def process(self, time_passed):
        # 处理世界中每一个实体
        copy_e = copy.copy(self.entities)
        for entity in copy_e.values():
            entity.process(time_passed)

    def render(self, surface):
        # 绘制背景和每一个实体
        surface.blit(self.background, (0, 0))
        for entity in self.entities.values():
            entity.render(surface)

    def get_close_entity(self, name, location, range=100):
        # 获得一个范围内的所有实体
        location = Vector2(location)
        for entity in self.entities.values():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
                if distance < range:
                    return entity
        return None
