import pygame, sys, random, math
from pygame.locals import *
pygame.init()
screen_size_x = 640
screen_size_y = 480

class PhysicsHandler:
    def __init__(self):
        self.objects = []
    def CreateObject(self, points, rotation_angle, radius):
        self.objects.append([])
        self.px, self.py = 200, 200
        self.origin = self.px, self.py, (2, 2)
        self.objects[len(self.objects) - 1].append((rotation_angle, 0))
        self.objects[len(self.objects) - 1].append(radius)
        self.objects[len(self.objects) - 1].append(self.origin)
        self.current_angle = rotation_angle - 360 / points
        for i in range(0, points, 1):
            self.current_angle += 360 / points
            self.current_angle = self.current_angle % 360
            self.to_radians = self.current_angle * (math.pi / 180)
            self.px = self.px + radius * math.cos(self.to_radians)
            self.py = self.py + radius * math.sin(self.to_radians)
            self.new_point = self.px, self.py
            self.objects[len(self.objects) - 1].append(self.new_point)
    def RotateObjects(self, rotation):
        for i in range(0, len(self.objects),  1):
            #== Start Unpack Variables ==#
            self.rotation = self.objects[i][0]
            self.radius = self.objects[i][1]
            self.origin = self.objects[i][2]
            self.rotation_angle, self.rotation_velocity = self.rotation
            self.px, self.py, self.v = self.origin
            #== End Unpack Variables ==#
            self.rotation_angle += rotation
            #== Start Pack Variables ==#
            self.rotation = self.rotation_angle, self.rotation_velocity
            self.length = len(self.objects[i]) - 3
            self.objects[i] = [self.rotation, self.radius, self.origin]
            #== End Pack Varibles ==#
            self.current_angle = self.rotation_angle - 360 / self.length 
            for j in range(0, self.length, 1):
                self.current_angle += 360 / self.length
                self.current_angle = self.current_angle % 360
                self.to_radians = self.current_angle * (math.pi / 180)
                self.pox = self.px + self.radius * math.cos(self.to_radians)
                self.poy = self.py + self.radius * math.sin(self.to_radians)
                self.new_point = self.pox, self.poy
                self.objects[i].append(self.new_point)
    def SimulateGravityMovement(self):
        for i in range(0, len(self.objects),  1):
            #== Start Unpack Variables ==#
            self.rotation = self.objects[i][0]
            self.radius = self.objects[i][1]
            self.origin = self.objects[i][2]
            self.rotation_angle, self.rotation_velocity = self.rotation
            self.px, self.py, self.v = self.origin
            self.vx, self.vy = self.v
            #== End Unpack Variables ==#
            self.px += self.vx
            self.py += self.vy
            #== Start Pack Variables ==#
            self.v = self.vx, self.vy
            self.origin = self.px, self.py, self.v
            self.rotation = self.rotation_angle, self.rotation_velocity
            self.length = len(self.objects[i]) - 3
            self.objects[i] = [self.rotation, self.radius, self.origin]
            #== End Pack Varibles ==#
            self.current_angle = self.rotation_angle - 360 / self.length 
            for j in range(0, self.length, 1):
                self.current_angle += 360 / self.length
                self.current_angle = self.current_angle % 360
                self.to_radians = self.current_angle * (math.pi / 180)
                self.pox = self.px + self.radius * math.cos(self.to_radians)
                self.poy = self.py + self.radius * math.sin(self.to_radians)
                if self.pox + self.vx <= 0 and self.vx < 0:
                    self.vx *= -1
                elif self.pox + self.vx >= screen_size_x and self.vx > 0:
                    self.vx *= -1
                if self.poy + self.vy <= 0 and self.vy < 0:
                    self.vy *= -1
                elif self.poy + self.vy >= screen_size_y and self.vy > 0:
                    self.vy *= -1
                self.v = self.vx, self.vy
                self.objects[i][2] = self.px, self.py, self.v 
                self.new_point = self.pox, self.poy
                self.objects[i].append(self.new_point)
    def DrawObjects(self):
        for i in range(0, len(self.objects), 1):
            for j in range(3, len(self.objects[i]) - 1, 1):
                pygame.draw.line(screen, (0, 0, 0), self.objects[i][j], self.objects[i][j + 1], 3)
            pygame.draw.line(screen, (0, 0, 0), self.objects[i][3], self.objects[i][len(self.objects[i]) - 1], 3)
    def Update(self):
        self.RotateObjects(1)
        self.SimulateGravityMovement()
        self.DrawObjects()

Physics = PhysicsHandler()
Physics.CreateObject(5, 0, 50)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_size_x, screen_size_y), 0, 32)
while True:
    clock.tick(60)
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    Physics.Update()
    pygame.display.update()
