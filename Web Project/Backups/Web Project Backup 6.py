import pygame, sys, random, math
from pygame.locals import *
class WebHandler:
  def __init__(self):
    self.points = []
    self.connections = []
    self.selected = []
    self.near = []
  def CreatePoints(self):
    self.mouse_pressed = pygame.mouse.get_pressed()
    if self.mouse_pressed[0]:
      self.mx, self.my = pygame.mouse.get_pos()
      self.points.append(((self.mx, self.my), (0, 0)))
      self.selected = []
  def AttractPoints(self):
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
      self.vx_1 += self.distance_x / self.divisor * ((self.distance - self.divisor) / 10)
      self.vy_1 += self.distance_y / self.divisor * ((self.distance - self.divisor) / 10) 
      self.pos_1 = self.px_1, self.py_1
      self.vel_1 = self.vx_1, self.vy_1
      self.points[self.point_1] = self.pos_1, self.vel_1
  def ConnectPoints(self):
    self.min_size = 50
    self.max_size = 100
    for i in range(0, len(self.points), 1):
      self.pos, self.vel = self.points[i]
      self.px, self.py = self.pos
      self.vx, self.vy = self.vel
      self.mx, self.my = pygame.mouse.get_pos()
      self.mouse_pressed = pygame.mouse.get_pressed()
      self.distance = math.sqrt(math.pow(self.mx - self.px, 2) + math.pow(self.my - self.py, 2))
      if self.distance < 20:
        self.near.append(i)
      if self.distance < 20 and self.mouse_pressed[2] and not i in self.selected:
        self.selected.append(i)
        self.is_on_target = True
      if len(self.selected) > 1:
        self.inside = False
        for i in range(self.min_size, self.max_size, 1):
          if (self.selected[0], self.selected[1], i) in self.connections: self.inside = True; break
          if (self.selected[1], self.selected[0], i) in self.connections: self.inside = True; break
        if self.inside == False:
          self.attraction = random.randint(self.min_size, self.max_size)
          self.connections.append((self.selected[0], self.selected[1], self.attraction))
          self.connections.append((self.selected[1], self.selected[0], self.attraction))
        self.selected = []          
  def ContainPoints(self):
    for i in range(0, len(self.points), 1):
      self.pos, self.vel = self.points[i]
      self.px, self.py = self.pos
      self.vx, self.vy = self.vel
      self.margin = 5
      if self.px < self.margin: self.px = self.margin; self.vx *= -1.1
      elif self.px > Simulation.screen_size_x - self.margin: self.px = Simulation.screen_size_x - self.margin; self.vx *= -1.1
      if self.py < self.margin: self.py = self.margin; self.vy *= -1.1
      elif self.py > Simulation.screen_size_y - self.margin: self.py = Simulation.screen_size_y - self.margin; self.vy *= -1.1
      self.pos = self.px, self.py
      self.vel = self.vx, self.vy
      self.points[i] = self.pos, self.vel
  def MovePoints(self):
    for i in range(0, len(self.points), 1):
      self.pos, self.vel = self.points[i]
      self.px, self.py = self.pos
      self.vx, self.vy = self.vel
      self.px += self.vx
      self.py += self.vy
      self.vel = self.vx, self.vy
      self.pos = self.px, self.py
      self.points[i] = self.pos, self.vel
  def Clean(self):
    self.near = []
    for i in range(0, len(self.points), 1):
      self.pos, self.vel = self.points[i]
      self.px, self.py = self.pos
      self.vx, self.vy = self.vel
      self.vx /= 1.2
      self.vy /= 1.2
      #self.vy += 0.2
      self.vel = self.vx, self.vy
      self.pos = self.px, self.py
      self.points[i] = self.pos, self.vel 
  def Draw(self):
      self.size = 7
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
        pygame.draw.aaline(Simulation.screen, (0, 0, 0), self.pos_1, self.pos_2)
      for i in range(0, len(self.near), 1):
        self.pos, self.vel = self.points[self.near[i]]
        self.px, self.py = self.pos
        self.px -= self.size / 2
        self.py -= self.size / 2
        pygame.draw.rect(Simulation.screen, (255, 0, 0), (self.px, self.py, self.size, self.size))
      for i in range(0, len(self.selected), 1):
        self.pos, self.vel = self.points[self.selected[i]]
        self.px, self.py = self.pos
        self.px -= self.size / 2
        self.py -= self.size / 2
        pygame.draw.rect(Simulation.screen, (0, 0, 255), (self.px, self.py, self.size, self.size))
  def Update(self):
    self.Clean()
    self.ConnectPoints()
    self.AttractPoints()
    self.ContainPoints()
    self.MovePoints()
    self.Draw()
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
      self.Webs.Update()
      pygame.display.update()
Simulation = Program()
Simulation.Update()
