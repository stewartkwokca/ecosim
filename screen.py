import pygame

BG_COLOR = (0, 0, 0)
WIDTH = 800
HEIGHT = 800

WORLDWIDTH = 3000
WORLDHEIGHT = 3000
def screenSetup():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BG_COLOR)

    pygame.display.set_caption('EcoSim')

    pygame.display.flip()

    return screen;

