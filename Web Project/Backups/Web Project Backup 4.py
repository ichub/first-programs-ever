import pygame, sys, random, math
from pygame.locals import *
class WebHandler:
  def __init__(self):
    self.points = []
    self.connections = []
  def CreatePoints(self):
    self.amount = 20
    self.con_amount = 2
    self.frame_amount = len(self.points)
    for i in range(0, self.amount, 1):
      self.mx, self.my = pygame.mouse.get_pos()
      self.chosen = []
      for j in range(0, self.con_amount, 1):
        self.choice = random.randint(self.frame_amount, self.frame_amount + self.amount - 1)
        if not self.choice in self.chosen:
          self.chosen.append(self.choice)
      for j in range(0, len(self.chosen), 1):
        self.new_connection = len(self.points), self.chosen[j], random.randint(10, 200)
        if not self.new_connection in self.connections:
          self.connections.append(self.new_connection)
      self.points.append(((self.mx + random.uniform(-1, 1), self.my + random.uniform(-1, 1)), (0, 0)))
  def MovePoints(self):
    for i in range(0, len(self.connections), 1):
      self.point_1, self.point_2, self.distance = self.connections[i]
      self.pos_1, self.vel_1 = self.points[self.point_1]
      self.pos_2, self.vel_2 = self.points[self.point_2]
      self.px_1, self.py_1 = self.pos_1
      self.vx_1, self.vy_1 = self.vel_1
      self.px_2, self.py_2 = self.pos_2
      self.vx_2, self.vy_2 = self.vel_2
      self.distance_x = self.px_1 - self.px_2
      self.distance_y = self.py_1 - self.py_2
      self.divisor = math.sqrt(math.pow(self.distance_x, 2) + math.pow(self.distance_y, 2)) + 0.0001
      self.vx_1 = self.distance_x / self.divisor
      self.vy_1 = self.distance_y / self.divisor
      self.px_1 += self.vx_1 * ((self.distance - self.divisor) / 10)
      self.py_1 += self.vy_1 * ((self.distance - self.divisor) / 10)
      self.pos_1 = self.px_1, self.py_1
      self.vel_1 = self.vx_1, self.vy_1
      self.points[self.point_1] = self.pos_1, self.vel_1
  def ContainPoints(self):
    for i in range(0, len(self.points), 1):
      self.pos, self.vel = self.points[i]
      self.px, self.py = self.pos
      self.vx, self.vy = self.vel
      self.margin = 5
      if self.px < self.margin: self.px = self.margin
      elif self.px > Simulation.screen_size_x - self.margin: self.px = Simulation.screen_size_x - self.margin
      if self.py < self.margin: self.py = self.margin
      elif self.py > Simulation.screen_size_y - self.margin: self.py = Simulation.screen_size_y - self.margin
      self.pos = self.px, self.py
      self.vel = self.vx, self.vy
      self.points[i] = self.pos, self.vel
  def Draw(self):
      self.size = 4
      for i in range(0, len(self.points), 1):
        self.pos_1, self.vel_1 = self.points[i]
        self.px, self.py = self.pos_1
        self.px -= self.size / 2
        self.py -= self.size / 2
        #pygame.draw.rect(Simulation.screen, (0, 0, 0), (self.px, self.py, self.size, self.size))
      for i in range(0, len(self.connections), 1):
        self.point_1, self.point_2, self.distance = self.connections[i]
        self.pos_1, self.vel_1 = self.points[self.point_1]
        self.pos_2, self.vel_2 = self.points[self.point_2]
        pygame.draw.aaline(Simulation.screen, (0, 0, 0), self.pos_1, self.pos_2)
class Program:
  def __init__(self):
    pygame.init()
    self.screen_size_x = 800
    self.screen_size_y = 600
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
      self.Webs.MovePoints()
      self.Webs.ContainPoints()
      self.Webs.Draw()
      pygame.display.update()
Simulation = Program()
Simulation.Update()
