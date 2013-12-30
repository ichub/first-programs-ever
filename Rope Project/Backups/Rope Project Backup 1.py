import pygame, sys, random, math
from pygame.locals import *
screen_size_x = 640
screen_size_y = 480

class Rope:
    def __init__(self):
        self.links = []
        self.thickness = 10
        self.link_size = 1
        self.rope_length = 500
    def CreateLinks(self):
        for i in range(0, self.rope_length / self.link_size, 1):
            self.links.append(((100, i * self.link_size + 20), (0, 0)))
    def MoveLinks(self):
        self.mx, self.my = pygame.mouse.get_pos()
        self.main_position, self.main_velocity = self.links[0]
        self.main_px, self.main_py = self.main_position
        self.main_position = pygame.mouse.get_pos()
        self.links[0] = self.main_position, self.main_velocity
        for i in range(1, len(self.links), 1):
            self.position, self.velocity = self.links[i]
            self.px, self.py = self.position
            self.vx, self.vy = self.velocity
            self.px += self.vx
            self.py += self.vy
            self.position = (self.px, self.py)
            self.velocity = (self.vx, self.vy)
            self.links[i] = (self.position, self.velocity)
    def LockLinks(self):
        for i in range(1, len(self.links), 1):
            self.position, self.velocity = self.links[i]
            self.px, self.py = self.position
            self.position2, self.velocity2 = self.links[i - 1]
            self.px2, self.py2 = self.position2
            self.distance_x = self.px2 - self.px
            self.distance_y = self.py2 - self.py
            self.distance = math.pow((self.distance_x * self.distance_x + self.distance_y * self.distance_y), 0.5)
            self.new_x = (self.distance_x / self.distance) * self.link_size
            self.new_y = (self.distance_y / self.distance) * self.link_size
            self.px = self.px2 - self.new_x
            self.py = self.py2 - self.new_y
            self.position = self.px, self.py
            self.links[i] = self.position, self.velocity
    def DrawLinks(self, type_of_line):
        if type_of_line == 1:
            for i in range(0, len(self.links) - 1, 1):
                self.position, self.velocity = self.links[i]
                self.px, self.py = self.position
                self.position2, self.velocity2 = self.links[i + 1]
                pygame.draw.line(screen, (0, 0, 0), self.position, self.position2, self.thickness)
        elif type_of_line == 2:
            for i in range(0, len(self.links), 1):
                self.position, self.velocity = self.links[i]
                self.px, self.py = self.position
                pygame.draw.rect(screen, (0, 0, 0), (self.px, self.py, self.thickness, self.thickness))
        elif type_of_line == 3:
            for i in range(0, len(self.links), 1):
                self.position, self.velocity = self.links[i]
                pygame.draw.circle(screen, (0, 0, 0), self.position, self.thickness)
        elif type_of_line == 4:
            for i in range(0, len(self.links) - 1, 1):
                self.position, self.velocity = self.links[i]
                self.position2, self.velocity2 = self.links[i + 1]
                pygame.draw.aaline(screen, (0, 0, 0), self.position, self.position2, 10)
                

rope = Rope()
rope.CreateLinks()
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_size_x, screen_size_y), 0, 32)
while True:
    clock.tick(60)
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    rope.MoveLinks()
    rope.LockLinks()
    rope.DrawLinks(4)
    pygame.display.update()

"""

self.distance_x = self.mx - self.px
self.distance_y = self.my - self.py
self.divisor = math.pow((self.distance_x * self.distance_x + self.distance_y * self.distance_y), 0.5)
self.speed_x = self.distance_x / self.divisor
self.speed_y = self.distance_y / self.divisor
self.vx += self.speed_x
self.vy += self.speed_y
"""

