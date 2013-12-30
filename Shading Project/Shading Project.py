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
        self.shades = []
    def CreateBoxes(self, size, gap):
        self.size = size
        self.gap = gap
        for i in range(0, screen_size_x + self.size, self.size + self.gap):
            for j in range(0, screen_size_y + self.size, self.size + self.gap):
                self.r = 255.0 / screen_size_y * (j)
                self.g = 255.0 / screen_size_x * (i)
                self.b = 255.0 / screen_size_x * (screen_size_x - i)
                self.color = self.r, self.g, self.b
                self.boxes.append(((i, j), self.color, self.color, False, self.size, 0))
    def CreateShades(self):
        self.buttons = pygame.mouse.get_pressed()
        if self.buttons[0]:
            self.mx, self.my = pygame.mouse.get_pos()
            self.vx = random.uniform(-5, 5)
            self.vy = random.uniform(-5, 5)
            self.radius = random.randint(50, 100)
            self.shades.append(((self.mx, self.my), (self.vx, self.vy), self.radius, 0))
    def Reset(self):
        self.start_color = (0, 0, 0)
        for i in range(0, len(self.boxes), 1):
            self.position, self.color, self.grayscale, self.to_draw, self.or_size, self.re_size = self.boxes[i]
            self.grayscale = (0, 0, 0)
            self.re_size = 0
            self.boxes[i] = self.position, self.color, self.grayscale, False, self.or_size, self.re_size
        self.to_delete = []
        for i in range(0, len(self.shades), 1):
            self.position, self.velocity, self.max_distance, self.count = self.shades[i]
            self.count += 1
            self.shades[i] = self.position, self.velocity, self.max_distance, self.count
            if self.count >= 600:
                self.to_delete.append(i)
        for i in range(0, len(self.to_delete), 1):
            self.shades.pop(self.to_delete[i])
            for j in range(0, len(self.to_delete), 1):
                self.to_delete[j] -= 1                
    def Recolor(self):
        self.start_color = (0, 0, 0)
        for i in range(0, len(self.shades), 1):
            self.position, self.velocity, self.max_distance, self.count = self.shades[i]
            self.mx, self.my = self.position
            for j in range(0, len(self.boxes), 1):
                self.position, self.color, self.grayscale, self.to_draw, self.or_size, self.new_size = self.boxes[j]
                self.px, self.py = self.position
                if not self.mx - self.max_distance > self.px and not self.mx + self.max_distance < self.px:
                    if not self.my - self.max_distance > self.py and not self.my + self.max_distance < self.py:
                        self.distance = math.sqrt(math.pow(self.px - self.mx, 2) + math.pow(self.py - self.my, 2))
                        if self.distance <= self.max_distance:
                            self.start_r, self.start_g, self.start_b = self.start_color
                            self.real_r, self.real_g,  self.real_b = self.color
                            self.g_r, self.g_g, self.g_b = self.grayscale
                            self.new_r = self.real_r - (self.real_r - self.start_r)/ self.max_distance * self.distance
                            self.new_g = self.real_g - (self.real_g - self.start_g)/ self.max_distance * self.distance
                            self.new_b = self.real_b - (self.real_b - self.start_b)/ self.max_distance * self.distance
                            self.new_r -= self.count / 4
                            self.new_g -= self.count / 4
                            self.new_b -= self.count / 4
                            if self.new_r < self.g_r: self.new_r = self.g_r
                            if self.new_g < self.g_g: self.new_g = self.g_g
                            if self.new_b < self.g_b: self.new_b = self.g_b
                            self.new_color = (self.new_r, self.new_g, self.new_b)
                            self.to_draw = True
                            self.boxes[j] = self.position, self.color, self.new_color, self.to_draw, self.or_size, self.new_size                              
    def Resize(self):
        for i in range(0, len(self.shades), 1):
            self.position, self.velocity, self.max_distance, self.count = self.shades[i]
            self.mx, self.my = self.position
            for j in range(0, len(self.boxes), 1):
                self.position, self.color, self.grayscale, self.to_draw, self.or_size, self.re_size = self.boxes[j]
                self.px, self.py = self.position
                if not self.mx - self.max_distance > self.px and not self.mx + self.max_distance < self.px:
                    if not self.my - self.max_distance > self.py and not self.my + self.max_distance < self.py:
                        if self.to_draw == True:
                            self.distance = math.sqrt(math.pow(self.px - self.mx, 2) + math.pow(self.py - self.my, 2))
                            if self.distance <= self.max_distance:
                                self.new_size = float(self.or_size) / self.max_distance * (self.max_distance - self.distance)
                                if self.new_size < self.re_size: self.new_size = self.re_size
                                self.boxes[j] = self.position, self.color, self.grayscale, self.to_draw, self.or_size, self.new_size
    def MoveShades(self):
        for i in range(0, len(self.shades), 1):
            self.gravity = 2
            self.rand_slow = random.uniform(1, 3)
            self.margin = -30
            self.position, self.velocity, self.radius, self.count = self.shades[i]
            self.px, self.py = self.position
            self.vx, self.vy = self.velocity
            self.mx, self.my = pygame.mouse.get_pos()
            if self.py >= screen_size_y - self.radius - self.margin:
                self.py = screen_size_y - self.radius - self.margin - 5
                self.vy /= self.rand_slow
                self.vy *= -1
            elif self.py <= self.radius + self.margin:
                self.py = self.radius + self.margin + 5
                self.vy /= self.rand_slow
                self.vy *= -1
            if self.px >= screen_size_x - self.radius - self.margin:
                self.px = screen_size_x - self.radius - self.margin - 5
                self.vx /= self.rand_slow
                self.vx *= -1
            elif self.px <= self.radius + self.margin:
                self.px = self.radius + self.margin + 5
                self.vx /= self.rand_slow
                self.vx *= -1
            self.py += self.vy
            self.px += self.vx
            self.position = self.px, self.py
            self.velocity = self.vx, self.vy
            self.shades[i] = self.position, self.velocity, self.radius, self.count
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
            self.Shades.Reset()
            self.Shades.CreateShades()
            self.Shades.MoveShades()
            self.Shades.Recolor()
            self.Shades.Resize()
            self.Shades.DrawBoxes()
            pygame.display.update()

Simulation = Program()
Simulation.Update()
"""
self.distance = math.sqrt(math.pow(self.px - self.mx, 2) + math.pow(self.py - self.my, 2))
            self.distance_x = self.mx - self.px
            self.distance_y = self.my - self.py
            self.divisor = math.sqrt(math.pow(self.distance_x, 2) + math.pow(self.distance_y, 2))
            self.speed_x = self.distance_x / self.divisor / 5
            self.speed_y = self.distance_y / self.divisor / 5
            self.vx += self.speed_x
            self.vy += self.speed_y
            self.py += self.gravity
"""
