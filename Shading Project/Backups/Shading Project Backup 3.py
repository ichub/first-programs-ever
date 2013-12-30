import pygame, sys, random, math
from pygame.locals import *
screen_size_x = 800
screen_size_y = 600

class RippleHandler:
    def __init__(self):
        self.boxes = []
    def CreateBoxes(self):
        self.size = 15
        self.gap = 0
        for i in range(0, screen_size_x + self.size, self.size + self.gap):
            for j in range(0, screen_size_y + self.size, self.size + self.gap):
                self.r = 255.0 / screen_size_y * (j)
                self.g = 255.0 / screen_size_x * (i)
                self.b = 255.0 / screen_size_x * (screen_size_x - i)
                if self.r >= 255: self.r = 255
                elif self.r <= 0: self.r = 0
                if self.g >= 255: self.g = 255
                elif self.g <= 0: self.g = 0
                if self.b >= 255: self.b = 255
                elif self.b <= 0: self.b = 0
                self.color = self.r, self.g, self.b
                self.boxes.append(((i, j), self.color, self.color))
    def RecolorBoxes(self):
        self.max_distance = 200
        self.start_color = (0, 0, 0)
        for i in range(0, len(self.boxes), 1):
            self.position, self.color, self.grayscale = self.boxes[i]
            self.px, self.py = self.position
            self.mx, self.my = pygame.mouse.get_pos()
            self.distance = math.sqrt(math.pow(self.px - self.mx, 2) + math.pow(self.py - self.my, 2))
            self.start_r, self.start_g, self.start_b = self.start_color
            self.real_r, self.real_g,  self.real_b = self.color
            if self.distance <= self.max_distance:
                self.new_r = self.real_r - (self.real_r - self.start_r)/ self.max_distance * self.distance
                self.new_g = self.real_g - (self.real_g - self.start_g)/ self.max_distance * self.distance
                self.new_b = self.real_b - (self.real_b - self.start_b)/ self.max_distance * self.distance
            else:
                self.new_r = self.start_r
                self.new_g = self.start_g
                self.new_b = self.start_b
                
            if self.new_r >= 255: self.new_r = 255
            elif self.new_r <= 0: self.new_r = 0
            if self.new_g >= 255: self.new_g = 255
            elif self.new_g <= 0: self.new_g = 0
            if self.new_b >= 255: self.new_b = 255
            elif self.new_b <= 0: self.new_b = 0
            self.new_color = (self.new_r, self.new_g, self.new_b)
            self.boxes[i] = self.position, self.color, self.new_color
            
    def DrawBoxes(self):
        for i in range(0, len(self.boxes), 1):
            self.position, self.color, self.grayscale = self.boxes[i]
            self.px, self.py = self.position
            self.adjust = self.size / 2
            pygame.draw.rect(screen, self.grayscale, (self.px - self.adjust, self.py - self.adjust, self.size, self.size))
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
    Ripples.RecolorBoxes()
    Ripples.DrawBoxes()
    pygame.display.update()
