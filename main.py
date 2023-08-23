import pygame
import time
import screen
from species import *
from camera import Camera

pygame.init()

window = screen.screenSetup()  # scale: 1 px = 100 ft, animals are 100x scale
cam = Camera()

running = True

cheetahs = [Cheetah(random.randint(20, screen.WORLDWIDTH-20), random.randint(20, screen.WORLDHEIGHT-20), 1, cam) for i in range(10)]
impalas = [Impala(random.randint(20, screen.WORLDWIDTH-20), random.randint(20, screen.WORLDHEIGHT-20), 1, cam) for i in range(150)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    cam.checkMovement()
    window.fill(screen.BG_COLOR)
    cam.drawBounds(window)
    for cheetah in cheetahs:
        if cheetah.dead:
            cheetahs.remove(cheetah)
        cheetah.tick()
        cheetah.render(window)
        cheetah.sprinting = False
        for impala in impalas:
            if cheetah.collision(impala):
                impalas.remove(impala)
                cheetah.food_eaten += 1
            if len(impalas) > 0 and cheetah.canSee(impala):
                cheetah.hunt(impala)
        for c in cheetahs:
            if c == cheetah:
                continue
            if cheetah.collision(c) and cheetah.breedHetero(c):
                cheetahs.append(Cheetah(cheetah.x, cheetah.y, 1, cam))
            if cheetah.canSee(c) and cheetah.ticksSinceMate >= cheetah.ticksToMate and c.ticksSinceMate >= c.ticksToMate:
                cheetah.angle = math.atan2(cheetah.y-c.y, c.x-cheetah.x)
    for impala in impalas:
        if impala.dead:
            impalas.remove(impala)
        for i in impalas:
            if i == impala:
                continue
            if impala.collision(i) and impala.breedHetero(i):
                impalas.append(Impala(impala.x, impala.y, 1, cam))
            if impala.canSee(i) and impala.ticksSinceMate >= impala.ticksToMate and i.ticksSinceMate >= i.ticksToMate:
                impala.angle = math.atan2(impala.y-i.y, i.x-impala.x)
        for cheetah in cheetahs:
            if impala.canSee(cheetah):
                impala.flee(cheetah)
        impala.tick()
        impala.render(window)
    font = pygame.font.SysFont("Arial", 12)
    txt = font.render(f"Cheetahs: {len(cheetahs)}", True, (255, 255, 255))
    txt2 = font.render(f"Impalas: {len(impalas)}", True, (255, 255, 255))
    window.blit(txt, (700, 25))
    window.blit(txt2, (700, 50))
    time.sleep(0.05)
    pygame.display.update()