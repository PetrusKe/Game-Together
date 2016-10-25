# coding=utf-8
from random import randint
import pygame
from pygame.locals import *

from game.plane_war.Bullet import Bullet
from game.plane_war.enemy import Enemy
from game.plane_war.global_var import *
from game.plane_war.plane import Plane
from gameobjects.vector2 import Vector2
from sys import exit
from game.plane_war.phone_data import PhoneData


def run(server):
    while True:
        if server.running:
            break

    # 初始化游戏
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    gameover = 0

    # 主要参数
    w, h = SCREEN_SIZE
    clock = pygame.time.Clock()
    time_font = pygame.font.Font(None, 30)
    text_font = pygame.font.Font(None, 50)

    enemy_list = []
    bullet_list = []
    boom_list = []  # 存储爆炸图像列表

    # 绑定图片
    background_im = pygame.image.load(PROJECT_PATH + '/game/plane_war/resources/images/background.jpg')
    enemy_boom_im = pygame.image.load(PROJECT_PATH + '/game/plane_war/resources/images/enemy_boom.png')
    hero_boom_im = pygame.image.load(PROJECT_PATH + '/game/plane_war/resources/images/hero_boom.png')
    health_bar_image = pygame.image.load(PROJECT_PATH + '/game/plane_war/resources/images/health_bar.png')
    health_image = pygame.image.load(PROJECT_PATH + '/game/plane_war/resources/images/health.png')

    # 实例化对象
    hero = Plane('hero', 100.0)

    while True:
        screen.blit(background_im, (0, 0))
        hero.draw(screen)
        pygame.display.set_caption('Plane War - FPS: --')
        screen.blit(health_bar_image, (10, 10))
        for i in range(hero.hp):
            screen.blit(health_image, (10 + 30 * i, 12))
        starttext = text_font.render('Start by your phone...', True, (0, 0, 0))
        start_rect = starttext.get_rect()
        start_rect.topleft = [(SCREEN_SIZE[0] - start_rect.width) / 2, (SCREEN_SIZE[1] - start_rect.height) / 2]
        screen.blit(starttext, start_rect)
        pygame.display.update()
        if PhoneData.getMoveData()[0] != 0.0:
            break

    # 音乐初始化
    background_music = PROJECT_PATH + '/game/plane_war/resources/music/background_music.mp3'
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(loops=-1, start=0.0)

    wait_time = pygame.time.get_ticks()
    while True:
        time_passed = clock.tick() / 1000

        # 敌机的生成
        if randint(1, 100) == 1 and not gameover:
            e = Enemy('enemy', randint(80, 300))
            enemy_list.append(e)
        # 敌机的越界销毁
        for e in enemy_list:
            if e.pos[1] > h:
                enemy_list.remove(e)
                del e

        # 飞机移动
        movedata = PhoneData.getMoveData()
        move_dir = Vector2(movedata[1], movedata[0])
        hero.border_check()
        if gameover:
            move_dir = Vector2(0, 0)
        hero.move(time_passed, move_dir)

        # 飞机和敌机的碰撞
        hero_rect = pygame.Rect(hero.image.get_rect())
        hero_rect.width -= 20
        hero_rect.top = hero.pos[1]
        hero_rect.left = hero.pos[0] + 10

        for enemy in enemy_list:
            enemy_rect = pygame.Rect(enemy.image.get_rect())
            enemy_rect.width -= 8
            enemy_rect.top = enemy.pos[1]
            enemy_rect.left = enemy.pos[0] + 4
            i = 0
            for bullet in bullet_list:
                bullet_rect = pygame.Rect(bullet.image.get_rect())
                bullet_rect.top = bullet.pos[1]  # fixme 根据图片大小修复
                bullet_rect.left = bullet.pos[0]

                if enemy_rect.colliderect(bullet_rect):
                    boom_list.append([enemy.pos, 0])
                    enemy_list.remove(enemy)
                    bullet_list.remove(bullet)
                    i = 1
                    del bullet
                    break

            if enemy_rect.colliderect(hero_rect):
                hero.crash()
                boom_list.append([enemy.pos, 0])
                enemy_list.remove(enemy)
                i = 1
            if i == 1:
                del enemy
                i = 0

        # 设置时间
        if not gameover:
            minute_text = (pygame.time.get_ticks() - wait_time) // 1000 // 60
            sec_text = (pygame.time.get_ticks() - wait_time) // 1000 % 60
        timetext = time_font.render(str(minute_text).zfill(2) + ':' + str(sec_text).zfill(2), True, (0, 0, 0))
        time_rect = timetext.get_rect()
        time_rect.topright = [SCREEN_SIZE[0] - 15, 10]

        # 图像绘制
        screen.blit(background_im, (0, 0))
        hero.draw(screen)
        for e in enemy_list:
            if gameover:
                e.move(time_passed, Vector2(0, 0))
            else:
                e.move(time_passed)
            e.draw(screen)
        # 绘制子弹图像
        for b in bullet_list:
            if gameover:
                b.move(time_passed, Vector2(0, 0))
            else:
                b.move(time_passed)
            b.draw(screen)
        # 绘制爆炸图像
        for boom in boom_list:
            screen.blit(enemy_boom_im, boom[0])
            if boom[1] > 15:  # 存在15帧
                boom_list.remove(boom)
                del boom
            else:
                boom[1] += 1

        screen.blit(health_bar_image, (10, 10))
        for i in range(hero.hp):
            screen.blit(health_image, (10 + 30 * i, 12))
        screen.blit(timetext, time_rect)
        pygame.display.set_caption('Plane War - FPS: %d' % (1 / time_passed))

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                # 攻击
                if event.key == pygame.K_SPACE:
                    p = Vector2(hero.pos[0], hero.pos[1])
                    bullet = Bullet('bullet', p)
                    if len(bullet_list) <= 10:
                        bullet_list.append(bullet)

        # 游戏结束
        if hero.hp <= 0:
            screen.blit(hero_boom_im, hero.pos)
            failtext = text_font.render('Game over!', True, (0, 0, 0))
            fail_rect = failtext.get_rect()
            fail_rect.topleft = [(SCREEN_SIZE[0] - fail_rect.width) / 2, (SCREEN_SIZE[1] - fail_rect.height) / 2]
            screen.blit(failtext, fail_rect)
            pygame.mixer.music.stop()
            gameover = 1
            server.running = 0

            # server.server_close()

        pygame.display.update()

    return

# if __name__ == '__main__':
#     run(server=None)
