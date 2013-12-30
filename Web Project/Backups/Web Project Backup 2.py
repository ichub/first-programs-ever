import pygame, sys, random, math
from pygame.locals import *
class WebHandler:
  def __init__(self):
    self.points = []
    self.connections = []
  def CreatePoints(self):
    self.amount = 10
    self.frame_amount = len(self.points)
    for i in range(0, self.amount, 1):
      self.mx, self.my = pygame.mouse.get_pos()
      self.px = random.randint(self.mx - 100, self.mx + 100)
      self.py = random.randint(self.my - 100, self.my + 100)
      self.chosen = []
      for j in range(0, self.amount / 2, 1):
        self.choice = random.randint(self.frame_amount, self.frame_amount + self.amount - 1)
        if not self.choice in self.chosen:
          self.chosen.append(self.choice)
      for j in range(0, len(self.chosen), 1):
        self.new_connection = len(self.points), self.chosen[j], 10
        if not self.new_connection in self.connections:
          self.connections.append(self.new_connection)
      self.points.append(((self.px, self.py), (0, 0)))    
  def Draw(self):
      self.size = 4
      for i in range(0, len(self.points), 1):
        self.pos_1, self.vel_1 = self.points[i]
        self.px, self.py = self.pos_1
        self.px -= self.size / 2
        self.py -= self.size / 2
        pygame.draw.rect(Simulation.screen, (0, 0, 0), (self.px, self.py, self.size, self.size))
      for i in range(0, len(self.connections), 1):
        self.point_1, self.point_2, self.distance = self.connections[i]
        self.pos_1, self.vel_1 = self.points[self.point_1]
        self.pos_2, self.vel_2 = self.points[self.point_2]
        pygame.draw.line(Simulation.screen, (0, 0, 0), self.pos_1, self.pos_2)
class Program:
  def __init__(self):
    pygame.init()
    self.screen_size_x = 640
    self.screen_size_y = 480
    self.screen_size = self.screen_size_x, self.screen_size_y
    self.clock = pygame.time.Clock()
    self.screen = pygame.display.set_mode(self.screen_size, 0, 32)
    pygame.display.set_caption("Web Project")
  def Update(self):
    self.Webs = WebHandler()
    while True:
      self.clock.tick(60)
      self.screen.fill((255, 255, 255))
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
        if event.type == MOUSEBUTTONDOWN:
          self.Webs.CreatePoints()
      self.Webs.Draw()
      pygame.display.update()
Simulation = Program()
Simulation.Update()
