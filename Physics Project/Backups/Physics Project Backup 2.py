import pygame, sys, random, math
from pygame.locals import *
screen_size_x = 640
screen_size_y = 480

class PhysicsHandler:
    def __init__(self):
        self.objects = []
    def CreateObject(self, points, rotation_angle, radius):
        self.objects.append([])
        self.px = 100
        self.py = 100
        self.origin_point = self.px, self.py
        self.objects[len(self.objects) - 1].append(rotation_angle)
        self.objects[len(self.objects) - 1].append(radius)
        self.objects[len(self.objects) - 1].append(self.origin_point)
        self.current_angle = rotation_angle - 360 / points
        for i in range(0, points, 1):
            self.current_angle += 360 / points
            self.current_angle = self.current_angle % 360
            self.to_radians = self.current_angle * (math.pi / 180)
            self.px = self.px + radius * math.cos(self.to_radians)
            self.py = self.py + radius * math.sin(self.to_radians)
            self.new_point = self.px, self.py
            self.objects[len(self.objects) - 1].append(self.new_point)
    def RotateObjects(self):
        for i in range(0, len(self.objects),  1):
            self.rotation_angle = self.objects[i][0]
            self.radius = self.objects[i][1]
            self.origin = self.objects[i][2]
            self.rotation_angle += 1
            self.px, self.py = self.origin
            self.length = len(self.objects[i]) - 3
            self.objects[i] = [self.rotation_angle, self.radius, self.origin]
            self.current_angle = self.rotation_angle - 360 / self.length 
            for j in range(0, self.length, 1):
                self.current_angle += 360 / self.length
                self.current_angle = self.current_angle % 360
                self.to_radians = self.current_angle * (math.pi / 180)
                self.pox = self.px + self.radius * math.cos(self.to_radians)
                self.poy = self.py + self.radius * math.sin(self.to_radians)
                self.new_point = self.pox, self.poy
                self.objects[i].append(self.new_point)
    def DrawObjects(self):
        for i in range(0, len(self.objects), 1):
            self.points = self.objects[i]
            for j in range(3, len(self.points) - 1, 1):
                self.px, self.py = self.points[j]
                pygame.draw.line(screen, (0, 0, 0), self.points[j], self.points[j + 1], 3)
            pygame.draw.line(screen, (0, 0, 0), self.points[3], self.points[len(self.points) - 1], 3)

Physics = PhysicsHandler()
Physics.CreateObject(5, 0, 100)
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
    Physics.RotateObjects()
    Physics.DrawObjects()
    pygame.display.update()
