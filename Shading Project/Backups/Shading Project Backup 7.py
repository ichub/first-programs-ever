import pygame, sys, random, math, pygame.gfxdraw
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Shading Project")
screen_size_x = 800
screen_size_y = 600

screen = pygame.display.set_mode((screen_size_x, screen_size_y), 0, 32)
class ShadeHandler:
    def __init__(self):
        self.boxes = []
        self.shades = [(100, 100, 100), (300, 300, 200)]
    def CreateBoxes(self, size, gap):
        self.size = size
        self.gap = gap
        for i in range(0, screen_size_x + self.size, self.size + self.gap):
            for j in range(0, screen_size_y + self.size, self.size + self.gap):
                self.r = 255.0 / screen_size_y * (j)
                self.g = 255.0 / screen_size_x * (i)
                self.b = 255.0 / screen_size_x * (screen_size_x - i)
                self.color = self.r, self.g, self.b
                self.boxes.append(((i, j), self.color, self.color, False, self.size, self.size))
    def Recolor(self):
        self.start_color = (0, 0, 0)
        for i in range(0, len(self.boxes), 1):
            self.position, self.color, self.grayscale, self.to_draw, self.or_size, self.new_size = self.boxes[i]
            self.grayscale = self.start_color
            self.boxes[i] = self.position, self.color, self.grayscale, False, self.or_size, self.new_size
        for i in range(0, len(self.shades), 1):
            self.mx, self.my, self.max_distance = self.shades[i]
            for j in range(0, len(self.boxes), 1):
                self.position, self.color, self.grayscale, self.to_draw, self.or_size, self.new_size = self.boxes[j]
                self.px, self.py = self.position
                if not self.mx - self.max_distance > self.px and not self.mx + self.max_distance < self.px:
                    if not self.my - self.max_distance > self.py and not self.my + self.max_distance < self.py:
                        self.distance = math.sqrt(math.pow(self.px - self.mx, 2) + math.pow(self.py - self.my, 2))
                        if self.distance <= self.max_distance:
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
                            self.to_draw = True
                            self.new_color = (self.new_r, self.new_g, self.new_b)
                            self.boxes[j] = self.position, self.color, self.new_color, self.to_draw, self.or_size, self.new_size          
    def Resize(self):
        for i in range(0, len(self.shades), 1):
            self.mx, self.my, self.max_distance = self.shades[i]
            for j in range(0, len(self.boxes), 1):
                self.position, self.color, self.grayscale, self.to_draw, self.or_size, self.new_size = self.boxes[j]
                self.px, self.py = self.position
                if not self.mx - self.max_distance > self.px and not self.mx + self.max_distance < self.px:
                    if not self.my - self.max_distance > self.py and not self.my + self.max_distance < self.py:
                        if self.to_draw == True:
                            self.px, self.py = self.position
                            self.distance = math.sqrt(math.pow(self.px - self.mx, 2) + math.pow(self.py - self.my, 2))
                            if self.distance <= self.max_distance:
                                self.new_size = float(self.or_size) / self.max_distance * (self.max_distance - self.distance)
                                self.boxes[j] = self.position, self.color, self.grayscale, self.to_draw, self.or_size, self.new_size
            
    def DrawBoxes(self):
        for i in range(0, len(self.boxes), 1):
            self.position, self.color, self.grayscale, self.to_draw, self.or_size, self.new_size = self.boxes[i]
            if self.to_draw == True:
                self.r ,self.g, self.b = self.grayscale
                if self.r < 0: self.r = 0
                elif self.r > 255: self.r = 255
                if self.g < 0: self.g = 0
                elif self.g > 255: self.g = 255
                if self.b < 0: self.b = 0
                elif self.b > 255: self.b = 255
                self.grayscale = self.r, self.g, self.b
                self.px, self.py = self.position
                self.adjust = self.new_size / 2
                self.px -= self.adjust
                self.py -= self.adjust
                pygame.draw.rect(screen, self.grayscale, (self.px, self.py, self.new_size, self.new_size))

class Program:
    def __init__(self):
        self.Shades = ShadeHandler()
        self.Shades.CreateBoxes(20, 10)
    def Update(self):
        while True:
            clock.tick(60)
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.Shades.Recolor()
            self.Shades.Resize()
            self.Shades.DrawBoxes()
            pygame.display.update()

Simulation = Program()
Simulation.Update()
