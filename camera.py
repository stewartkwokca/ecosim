import pygame
import screen

class Camera:
    def __init__(self):
        self.xOffset = 0
        self.yOffset = 0

    def add_xOff(self, offChange):
        self.xOffset += offChange

    def add_yOff(self, offChange):
        self.yOffset += offChange

    def checkMovement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.add_xOff(-20)
        if keys[pygame.K_RIGHT]:
            self.add_xOff(20)
        if keys[pygame.K_UP]:
            self.add_yOff(-20)
        if keys[pygame.K_DOWN]:
            self.add_yOff(20)

    def drawBounds(self, scrn):
        pygame.draw.rect(scrn, (255, 255, 255), (20-self.xOffset, 20-self.yOffset, screen.WORLDWIDTH-40, screen.WORLDHEIGHT-40), width=1, border_radius=3, )