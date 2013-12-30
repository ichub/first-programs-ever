import pygame, sys, random, math
from pygame.locals import *
screen_size_x = 640
screen_size_y = 480

class RippleHandler:
    def __init__(self):
        self.boxes = []
        self.size = 20
    def CreateBoxes(self):
        for i in range(0, screen_size_x + self.size, self.size):
            for j in range(0, screen_size_y + self.size, self.size):
                self.r = 255.0 / screen_size_y * j
                self.g = 255.0 / screen_size_x * i
                self.b = j or i
                if self.r >= 255: self.r = 255
                if self.g >= 255: self.g = 255
                if self.b >= 255: self.b = 255
                self.boxes.append(((i, j), (self.r, self.g, self.b)))
    def DrawBoxes(self):
        for i in range(0, len(self.boxes), 1):
            self.position, self.color = self.boxes[i]
            self.px, self.py = self.position
            self.r, self.g, self.b = self.color
            self.adjust = self.size / 2
            pygame.draw.rect(screen, (self.r, self.g, self.b), (self.px - self.adjust, self.py - self.adjust, self.size, self.size))
Ripples = RippleHandler()
Ripples.CreateBoxes()
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_size_x, screen_size_y), 0, 32)
pygame.display.set_caption("Shading Project")
while True:
    clock.tick(60)
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    Ripples.DrawBoxes()
    pygame.display.update()
