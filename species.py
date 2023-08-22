import math
import pygame.draw
import random
import screen

MOVE_ANGLE = math.pi/6
FOOD_TICKS = 1000 # 1 week

## Base Classes ##

class Species():
    def __init__(self, x, y, food, sprintspeed, basesize, size, render_color, cam, hetero=True, food_needed=0):
        self.x = x
        self.y = y
        self.food_species = food
        self.food_needed = food_needed * size
        self.speed = 5*size
        self.sprintspeed = sprintspeed
        self.size = basesize * size
        self.hetero = hetero
        self.render_color = render_color
        self.angle = random.random() * 2 * math.pi

        self.dead = False
        self.cam = cam

        self.renderx = self.x
        self.rendery = self.y

    def move(self):
        self.angle += random.uniform(-1*MOVE_ANGLE, MOVE_ANGLE)
        while self.angle >= 2*math.pi:
            self.angle -= 2*math.pi
        while self.angle < 0:
            self.angle += 2*math.pi

        self.x += self.speed * math.cos(self.angle)
        self.y += -1 * self.speed * math.sin(self.angle)

        self.x = max(min(screen.WORLDWIDTH-20, self.x), 20)
        self.y = max(min(screen.WORLDHEIGHT-20, self.y), 20)

    def collision(self, other, called=False):
        if called:
            return (int(self.x - self.size/2) in range(int(other.x-other.size/2), int(other.x + other.size/2)) or int(self.x - self.size/2) in range(int(other.x-other.size/2), int(other.x + other.size/2))) and (int(self.y-self.size/2) in range(int(other.y-other.size/2), int(other.y + other.size/2)) or int(self.y+self.size/2) in range(int(other.y-other.size/2), int(other.y + other.size/2)))
        else:
            return (other.collision(self, called=True)) or (int(self.x - self.size/2) in range(int(other.x-other.size/2), int(other.x + other.size/2)) or int(self.x - self.size/2) in range(int(other.x-other.size/2), int(other.x + other.size/2))) and (int(self.y-self.size/2) in range(int(other.y-other.size/2), int(other.y + other.size/2)) or int(self.y+self.size/2) in range(int(other.y-other.size/2), int(other.y + other.size/2)))

    def tick(self):
        self.renderx = self.x - self.cam.xOffset
        self.rendery = self.y - self.cam.yOffset

class Plant(Species):
    def __init__(self, x, y, basesize, size, render_color, cam):
        super().__init__(x, y, [], 0, basesize, size, render_color, cam, hetero=False)

    def render(self, scrn):
        if (self.renderx > -1*self.size and self.renderx < screen.WIDTH) and (self.rendery > -1*self.size and self.rendery-self.size < screen.HEIGHT):
            pygame.draw.circle(scrn, self.render_color, (self.renderx, self.rendery), self.size/2)

    def tick(self):
        super().tick()

class Animal(Species):
    def __init__(self, x, y, food, sprintspeed, basesize, size, render_color, cam, food_needed=1, eyesight_angle=180, eyesight_dist=150, ticksToMate=16000):
        super().__init__(x, y, food, sprintspeed, basesize, size, render_color, cam, food_needed=food_needed)
        self.eyesight_angle = eyesight_angle
        self.eyesight_dist = eyesight_dist

        self.food_eaten = 0
        self.ticks_since_full = 0

        self.ticksToMate = ticksToMate
        self.ticksSinceMate = ticksToMate

    def tick(self):
        self.move()
        if self.food_needed > self.food_eaten:
            self.ticks_since_full += 1
        else:
            self.ticks_since_full = 0
            self.food_eaten = 0
        if self.ticks_since_full >= FOOD_TICKS:
            self.dead = True
        if self.ticksSinceMate < self.ticksToMate:
            self.ticksToMate += 1
        super().tick()
    def render(self, scrn):
        if (self.renderx > -1 * self.size and self.renderx - self.size < screen.WIDTH) and (self.rendery > -1 * self.size and self.rendery - self.size < screen.HEIGHT):
            self.renderSight(scrn)
            pygame.draw.rect(scrn, self.render_color, pygame.Rect(self.renderx-self.size/2, self.rendery-self.size/2, self.size, self.size))

    def renderSight(self, scrn):
        eyesight_angle_rad = self.eyesight_angle * math.pi / 180
        pygame.draw.arc(scrn, (255, 255, 255), pygame.Rect(self.renderx-self.size/2-self.eyesight_dist/2, self.rendery-self.size/2-self.eyesight_dist/2, self.size+self.eyesight_dist, self.size+self.eyesight_dist), self.angle-eyesight_angle_rad/2, self.angle+eyesight_angle_rad/2)

    def breedHetero(self, other):
        if self.ticksSinceMate >= self.ticksToMate and other.ticksSinceMate >= other.ticksToMate:
            self.ticksSinceMate = 0
            other.ticksSinceMate = 0
            return True



# Specific Species

class Cheetah(Animal):
    def __init__(self, x, y, size, cam):
        super().__init__(x, y, [Impala], 70, 5, size, (255,0,0), cam, eyesight_angle=210, eyesight_dist=163, ticksToMate=16000)


class Impala(Animal):
    def __init__(self, x, y, size, cam):
        super().__init__(x, y, [], 55, 4, size, (0, 255, 0), cam, food_needed=0, ticksToMate=30000)




