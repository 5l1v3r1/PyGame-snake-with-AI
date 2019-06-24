import random
import sys
import pygame
from pygame.locals import *

screen_size = [1280, 720]


def collide(x1, x2, y1, y2, w1, w2, h1, h2):
    if x1 + w1 > x2 and x1 < x2 + w2 and y1 + h1 > y2 and y1 < y2 + h2:
        return True
    else:
        return False


def die(screen, full_score):
    clock.tick(10)
    print('GAME OVER')
    font = pygame.font.SysFont('Arial', 30)
    text = font.render('GAME OVER', True, (0, 0, 0))
    text2 = font.render('Your score was: ' + str(full_score), True, (0, 0, 0))
    screen.blit(text, (screen_size[0]/2 - 80, screen_size[1]/2 - 20))
    pygame.display.update()
    pygame.time.wait(500)
    screen.blit(text2, (screen_size[0]/2 - 100, screen_size[1]/2 + 20))
    pygame.display.update()
    pygame.time.wait(1300)
    sys.exit(0)


xs = [290, 290, 290, 290, 290]
ys = [290, 270, 250, 230, 210]
dirs = 0
score = 0
applepos = [random.randrange(20, screen_size[0] - 20 + 1, 20), random.randrange(20, screen_size[1] - 20 + 1, 20)]
applepos[0] = applepos[0] - 5
applepos[1] = applepos[1] - 5

pygame.init()

s = pygame.display.set_mode((screen_size[0], screen_size[1]))
pygame.display.set_caption('Snake')

appleimage = pygame.Surface((10, 10))
appleimage.fill((0, 255, 0))

img = pygame.Surface((20, 20))
img.fill((255, 0, 0))

f = pygame.font.SysFont('Arial', 20)
clock = pygame.time.Clock()

speed = 10
z = 0

while True:
    clock.tick(speed)
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit(0)

        elif e.type == KEYDOWN:
            if e.key == K_w and dirs != 0:
                dirs = 2
            elif e.key == K_s and dirs != 2:
                dirs = 0
            elif e.key == K_a and dirs != 1:
                dirs = 3
            elif e.key == K_d and dirs != 3:
                dirs = 1
            elif e.key == K_SPACE:
                z = 1

    i = len(xs) - 1
    while i >= 2:
        if collide(xs[0], xs[i], ys[0], ys[i], 20, 20, 20, 20):
            die(s, score)
        i -= 1

    if collide(xs[0], applepos[0], ys[0], applepos[1], 20, 10, 20, 10):
        score += 1
        speed += 0.5
        xs.append(700)
        ys.append(700)
        applepos = [random.randrange(20, screen_size[0] - 20 + 1, 20), random.randrange(20, screen_size[1] - 20 + 1, 20)]
        applepos[0] = applepos[0] - 5
        applepos[1] = applepos[1] - 5

    if xs[0] < 0 or xs[0] > screen_size[0] - 20 or ys[0] < 0 or ys[0] > screen_size[1] - 20:
        die(s, score)

    i = len(xs) - 1
    while i >= 1:
        xs[i] = xs[i - 1]
        ys[i] = ys[i - 1]
        i -= 1

    if z == 0:
        if dirs == 0:
            ys[0] += 20
        elif dirs == 1:
            xs[0] += 20
        elif dirs == 2:
            ys[0] -= 20
        elif dirs == 3:
            xs[0] -= 20
    else:
        if dirs == 0:
            ys[0] += 0
        elif dirs == 1:
            xs[0] += 0
        elif dirs == 2:
            ys[0] -= 0
        elif dirs == 3:
            xs[0] -= 0

        pygame.time.wait(15000)

        z = 0

    s.fill((255, 255, 255))

    for i in range(0, len(xs)):
        s.blit(img, (xs[i], ys[i]))

    s.blit(appleimage, applepos)
    t = f.render(str(score), True, (0, 0, 0))
    s.blit(t, (10, 10))

    snake_xy = [xs[0], ys[0]]
    apple_xy = [applepos[0] - 5, applepos[1] - 5]
    xys = [xs, ys]

    ### AI ###
    # finder #
    if snake_xy[0] < apple_xy[0] and dirs != 3:
        dirs = 1
    elif snake_xy[0] > apple_xy[0] and dirs != 1:
        dirs = 3
    elif snake_xy[0] == apple_xy[0] and snake_xy[1] != apple_xy[1]:
        if snake_xy[1] < apple_xy[1] and dirs != 2:
            dirs = 0
        elif snake_xy[1] > apple_xy[1] and dirs != 0:
            dirs = 2

    # anti suicide #
    elif (xs[0] + 20 in xs[2:] or xs[0] - 20 in xs[2:]) and dirs != 0 and dirs != 2:
        snake_tail = xs[2:]
        if xs[0] + 20 in xs[2:] and dirs != 1:
            if ys[snake_tail.index(xs[0] + 20)] < snake_xy[1]:
                dirs = 0
            else:
                dirs = 2
        elif xs[0] - 20 in xs[2:] and dirs != 3:
            if ys[snake_tail.index(xs[0] - 20)] < snake_xy[1]:
                dirs = 0
            else:
                dirs = 2

    elif (ys[0] + 20 in ys[2:] or ys[0] - 20 in ys[2:]) and dirs != 1 and dirs != 3:
        snake_tail = ys[2:]
        if ys[0] + 20 in ys[2:] and dirs != 2:
            if xs[snake_tail.index(ys[0] + 20)] < snake_xy[0]:
                dirs = 1
            else:
                dirs = 3
        elif ys[0] - 20 in ys[2:] and dirs != 0:
            if xs[snake_tail.index(ys[0] - 20)] < snake_xy[0]:
                dirs = 1
            else:
                dirs = 3

    # anti lag #
    else:
        if snake_xy[1] < apple_xy[1] and dirs != 2:
            dirs = 0
        elif snake_xy[1] > apple_xy[1] and dirs != 0:
            dirs = 2
        elif snake_xy[1] == apple_xy[1]:
            if snake_xy[0] < apple_xy[0] and dirs != 3:
                dirs = 1
            elif snake_xy[0] > apple_xy[0] and dirs != 1:
                dirs = 3

    # anti wall #
    if apple_xy[0] >= screen_size[0] - 30 or apple_xy[0] <= 30 or apple_xy[1] >= screen_size[1] - 30 or apple_xy[1] <= 30:
        if snake_xy[0] == apple_xy[0] and snake_xy[1] == apple_xy[1]:
            if dirs == 0 or dirs == 2:
                if snake_xy[0] <= screen_size[0]/2 and dirs != 3 and dirs != 1:
                    dirs = 1
                else:
                    dirs = 3
            elif dirs == 1 or dirs == 3:
                if snake_xy[1] <= screen_size[1]/2 and dirs != 2 and dirs != 2:
                    dirs = 0
                else:
                    dirs = 2

    ### AI ###

    pygame.display.update()
