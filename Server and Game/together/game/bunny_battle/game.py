import random
import pygame
from sys import exit
import math


def run():
    pygame.init()
    pygame.font.init()
    width, height = 640, 480
    acc = [0, 0]  # 记录射击精确度
    arrows = []  # 记录所有的剑
    screen = pygame.display.set_mode((width, height), 0, 32)
    font = pygame.font.Font(None, 24)

    # 设置计时器，当badtimer=0,生成一个敌人
    badtimer = 100
    badtimer1 = 0
    badguys = [[640, 100]]
    healthvalue = 194

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    # 设置用于保存按键
    keys = [False, False, False, False]
    playerpos = [100, 230]

    player = pygame.image.load('resources/images/dude.png')
    grass = pygame.image.load('resources/images/grass.png')
    castle = pygame.image.load('resources/images/castle.png')
    arrow = pygame.image.load('resources/images/bullet.png')
    badguyimg1 = pygame.image.load('resources/images/badguy.png')
    healthbar = pygame.image.load('resources/images/healthbar.png')
    health = pygame.image.load('resources/images/health.png')
    gameover = pygame.image.load("resources/images/gameover.png")
    youwin = pygame.image.load("resources/images/youwin.png")

    # load music
    hit = pygame.mixer.Sound("resources/audio/explode.wav")
    enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
    shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
    hit.set_volume(0.05)
    enemy.set_volume(0.05)
    shoot.set_volume(0.05)
    pygame.mixer.music.load('resources/audio/moonlight.wav')  # 加载背景音乐
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)

    # 设置一个图片副本
    badguyimg = badguyimg1

    running = 1
    exitcode = 0
    while running:
        screen.fill((0, 0, 0))

        for x in range(int(width / grass.get_width()) + 1):
            for y in range(int(height / grass.get_height()) + 1):
                screen.blit(grass, (x * 100, y * 100))
        screen.blit(castle, (0, 30))
        screen.blit(castle, (0, 135))
        screen.blit(castle, (0, 240))
        screen.blit(castle, (0, 345))

        # 设置兔子旋转角度
        position = pygame.mouse.get_pos()

        angle = math.atan2(position[1] - (playerpos[1] + 32), position[0] - playerpos[0] + 26)

        # 旋转兔子图片
        # atan2 返回弧度化为度数 *360/(2*pi)
        playerrot = pygame.transform.rotate(player, 360 - angle * 360 / (2 * math.pi))

        # 计算兔子的新位置并把它显示在屏幕
        # playerrot.get_rect()获得图片的外接矩形
        playerpos1 = (playerpos[0] - playerrot.get_rect().width / 2, playerpos[1] - playerrot.get_rect().height / 2)
        screen.blit(playerrot, playerpos1)

        for bullet in arrows:
            index = 0
            velx = math.cos(bullet[0]) * 10
            vely = math.sin(bullet[0]) * 10
            bullet[1] += velx
            bullet[2] += vely
            if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
                arrows.pop(index)
            index += 1
            for projectile in arrows:
                arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 360 / (2 * math.pi))
                screen.blit(arrow1, (projectile[1], projectile[2]))

        if badtimer == 0:
            badguys.append([640, random.randint(50, 430)])
            badtimer = 100 - (badtimer1 * 2)
            if badtimer1 >= 35:
                badtimer1 = 35
            else:
                badtimer1 += 5
        index = 0
        for badguy in badguys:
            if badguy[0] <= -64:
                badguys.pop(index)
                continue
            badguy[0] -= 7
            badrect = pygame.Rect(badguyimg.get_rect())  # 获得一个矩形
            badrect.top = badguy[1]
            badrect.left = badguy[0]  # 矩形的左边位置
            if badrect.left < 64:
                hit.play()
                healthvalue -= random.randint(5, 20)
                badguys.pop(index)

            index1 = 0
            for bullet in arrows:
                bullrect = pygame.Rect(arrow.get_rect())
                bullrect.left = bullet[1]
                bullrect.top = bullet[2]
                if badrect.colliderect(bullrect):
                    enemy.play()
                    acc[0] += 1
                    badguys.pop(index)
                    arrows.pop(index1)
                index1 += 1
            index += 1

        for badguy in badguys:
            if badguy:
                screen.blit(badguyimg, badguy)
        badtimer -= 1

        # Draw clock
        survivetext = font.render(str((90000 - pygame.time.get_ticks()) // 60000) + ':' +
                                  str((90000 - pygame.time.get_ticks()) // 1000 % 60).zfill(2), True, (0, 0, 0))
        textRect = survivetext.get_rect()
        textRect.topright = [635, 5]  # 设置时间显示位置
        screen.blit(survivetext, textRect)
        screen.blit(healthbar, (5, 5))
        for health1 in range(healthvalue):
            screen.blit(health, (health1 + 8, 8))  # 位置 = healthbar + (3, 3)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_w:
                    keys[0] = True
                elif event.key == pygame.K_a:
                    keys[1] = True
                elif event.key == pygame.K_s:
                    keys[2] = True
                elif event.key == pygame.K_d:
                    keys[3] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    keys[0] = False
                elif event.key == pygame.K_a:
                    keys[1] = False
                elif event.key == pygame.K_s:
                    keys[2] = False
                elif event.key == pygame.K_d:
                    keys[3] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    shoot.play()
                    position = pygame.mouse.get_pos()
                    acc[1] += 1
                    arrows.append([math.atan2(position[1] - (playerpos1[1] + 32), position[0] - (playerpos1[0] + 26)),
                                   playerpos1[0] + 32, playerpos[1] + 32])

        if keys[0]:
            playerpos[1] -= 5
        elif keys[2]:
            playerpos[1] += 5
        if keys[1]:
            playerpos[0] -= 5
        elif keys[3]:
            playerpos[0] += 5

        if pygame.time.get_ticks() >= 90000:
            running = 0
            exitcode = 1
        if healthvalue <= 0:
            running = 0
            exitcode = 0

    if acc[1] != 0:
        accuracy = acc[0] / acc[1] * 100
    else:
        accuracy = 0

    if exitcode == 0:
        text = font.render('Accuracy: %.2f' % accuracy + '%', True, (255, 0, 0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx  # 设置在屏幕中心
        textRect.centery = screen.get_rect().centery + 24

        screen.blit(gameover, (0, 0))
        screen.blit(text, textRect)
    else:
        text = font.render('Accuracy: %.2f' % accuracy + '%', True, (0, 255, 0))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx  # 设置在屏幕中心
        textRect.centery = screen.get_rect().centery + 24

        screen.blit(youwin, (0, 0))
        screen.blit(text, textRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
        pygame.display.update()


if __name__ == '__main__':
    run()
