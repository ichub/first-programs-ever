import pygame, sys, random, math
from pygame.locals import *
screen_size_x = 640
screen_size_y = 480

class RopeHandler:
    def __init__(self):
        self.ropes = []
        self.thickness = 1
        self.link_size = 1
        self.rope_length = 400
    def CreateRope(self):
        self.ropes.append([])
        for i in range(0, self.rope_length / self.link_size, 1):
            self.ropes[len(self.ropes) -1].append(((len(self.ropes), i * self.link_size + 20), (0, 0)))
    def LockLinks(self):
        for i in range(0, len(self.ropes), 1):
            self.links = self.ropes[i]
            self.position = pygame.mouse.get_pos()
            self.links[0] = self.position, (0, 0)
            for j in range(1, len(self.links), 1):
                self.position, self.velocity = self.links[j]
                self.px, self.py = self.position
                self.position2, self.velocity2 = self.links[j - 1]
                self.px2, self.py2 = self.position2
                self.distance_x = self.px2 - self.px
                self.distance_y = self.py2 - self.py
                self.distance = math.pow((self.distance_x * self.distance_x + self.distance_y * self.distance_y), 0.5)
                self.new_x = (self.distance_x / self.distance) * self.link_size
                self.new_y = (self.distance_y / self.distance) * self.link_size
                self.px = self.px2 - self.new_x
                self.py = self.py2 - self.new_y
                self.position = self.px, self.py
                self.links[j] = self.position, self.velocity
            self.ropes[i] = self.links
    def DrawLinks(self, type_of_line):
        for i in range(0, len(self.ropes), 1):
            self.links = self.ropes[i]
            if type_of_line == 1:
                for i in range(0, len(self.links) - 1, 1):
                    self.position, self.velocity = self.links[i]
                    self.px, self.py = self.position
                    self.position2, self.velocity2 = self.links[i + 1]
                    pygame.draw.aaline(screen, (0, 0, 0), self.position, self.position2, self.thickness)
                    pygame.draw.circle(screen, (100, 100, 100), self.position, 3)
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
                

ropees = RopeHandler()
ropees.CreateRope()
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
    ropees.LockLinks()
    ropees.DrawLinks(4)
    pygame.display.update()
