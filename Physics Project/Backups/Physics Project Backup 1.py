import pygame, sys, random, math
from pygame.locals import *
screen_size_x = 640
screen_size_y = 480

class PhysicsHandler:
    def __init__(self):
        self.objects = []
    def CreateObject(self, points, rotation_angle, radius):
        self.objects.append([])
        self.rand_x = 100
        self.rand_y = 100
        self.origin_point = self.rand_x, self.rand_y
        self.objects[len(self.objects) - 1].append(rotation_angle)
        self.objects[len(self.objects) - 1].append(self.origin_point)
        self.current_angle = rotation_angle - 360 / points
        for i in range(0, points, 1):
            self.current_angle += 360 / points
            self.current_angle = self.current_angle % 360
            self.to_radians = self.current_angle * (math.pi / 180)
            self.px = self.rand_x + radius * math.cos(self.to_radians)
            self.py = self.rand_y + radius * math.sin(self.to_radians)
            self.new_point = self.px, self.py
            self.objects[len(self.objects) - 1].append(self.new_point)
        print self.objects[len(self.objects) - 1]
        print len(self.objects[len(self.objects) - 1])
    def DrawObjects(self):
        for i in range(0, len(self.objects), 1):
            self.points = self.objects[i]
            for j in range(2, len(self.points) - 1, 1):
                self.px, self.py = self.points[j]
                pygame.draw.line(screen, (0, 0, 0), self.points[j], self.points[j + 1], 3)
            pygame.draw.line(screen, (0, 0, 0), self.points[2], self.points[len(self.points) - 1], 3)

Physics = PhysicsHandler()
Physics.CreateObject(10, 0, 50)
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
    Physics.DrawObjects()
    pygame.display.update()
