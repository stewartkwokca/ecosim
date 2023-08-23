import pygame
import time
import screen
from species import *
from camera import Camera

pygame.init()

window = screen.screenSetup()  # scale: 1 px = 100 ft, animals are 100x scale
cam = Camera()

running = True

cheetahs = [Cheetah(200, 200, 1, cam)]
impalas = [Impala(250, 250, 1, cam)]
#cheetahs = [Cheetah(random.randint(20, screen.WORLDWIDTH-20), random.randint(20, screen.WORLDHEIGHT-20), 1, cam) for i in range(6)]
#impalas = [Impala(random.randint(20, screen.WORLDWIDTH-20), random.randint(20, screen.WORLDHEIGHT-20), 1, cam) for i in range(100)]

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
        for impala in impalas:
            if cheetah.collision(impala):
                impalas.remove(impala)
                cheetah.food_eaten += 1
            if cheetah.canSee(impala):
                print(math.degrees(cheetah.angle))
        for c in cheetahs:
            if c != cheetah and cheetah.collision(c) and cheetah.breedHetero(c):
                cheetahs.append(Cheetah(cheetah.x, cheetah.y, 1, cam))
    for impala in impalas:
        if impala.dead:
            impalas.remove(impala)
        for i in impalas:
            if i != impala and impala.collision(i) and impala.breedHetero(i):
                impalas.append(Impala(impala.x, impala.y, 1, cam))
        impala.tick()
        impala.render(window)
    font = pygame.font.SysFont("Arial", 36)
    txt = font.render(str(len(cheetahs)), True, (255, 255, 255))
    txt2 = font.render(str(len(impalas)), True, (255, 255, 255))
    window.blit(txt, (500, 500))
    window.blit(txt2, (500, 600))
    time.sleep(1)
    pygame.display.update()