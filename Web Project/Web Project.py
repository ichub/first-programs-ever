import pygame, sys, random, math, pygame.gfxdraw
from pygame.locals import *
class WebHandler:
  def __init__(self):
    self.points = []
    self.connections = []
    self.selected = []
    self.near = []
    self.paused = []
  def HandleInput(self):
    self.select_distance = 20
    for i in range(0, len(self.points), 1):
      self.pos, self.vel = self.points[i]
      self.px, self.py = self.pos
      self.vx, self.vy = self.vel
      self.mx, self.my = pygame.mouse.get_pos()
      self.distance = math.sqrt(math.pow(self.mx - self.px, 2) + math.pow(self.my - self.py, 2))
      if self.distance < self.select_distance:
        self.near.append(i)
      if self.distance < self.select_distance and pygame.mouse.get_pressed()[2] and not i in self.selected:
        self.selected.append(i)
        if len(self.selected) >= 3:
          self.selected.pop(0)        
  def CreatePoints(self):
    self.mouse_pressed = pygame.mouse.get_pressed()
    if self.mouse_pressed[0]:
      self.points.append((pygame.mouse.get_pos(), (0, 0)))
      self.selected = []
  def ConnectPoints(self):
      if len(self.selected) >= 2:
        self.p1, self.p2 = self.selected
        self.exists = False
        for j in range(0, len(self.connections), 1):
          self.first, self.second, self.distance = self.connections[j]
          if self.first == self.p1 and self.second == self.p2: self.exists = True
          if self.first == self.p2 and self.second == self.p1: self.exists = True
        if self.exists == False:
          self.connections.append((self.selected[0], self.selected[1], 100))
          self.connections.append((self.selected[1], self.selected[0], 100))
        self.selected = []
  def AttractPoints(self):
    for i in range(0, len(self.connections), 1):
      self.p1_index, self.p2_index, self.distance = self.connections[i]
      self.pos_1, self.vel_1 = self.points[self.p1_index]
      self.pos_2, self.vel_2 = self.points[self.p2_index]
      self.px_1, self.py_1 = self.pos_1
      self.vx_1, self.vy_1 = self.vel_1
      self.px_2, self.py_2 = self.pos_2
      self.vx_2, self.vy_2 = self.vel_2
      self.distance_x = self.px_1 - self.px_2
      self.distance_y = self.py_1 - self.py_2
      self.divisor = math.sqrt(math.pow(self.distance_x, 2) + math.pow(self.distance_y, 2)) + 0.0001
      self.vx_1 += self.distance_x / self.divisor * ((self.distance - self.divisor) / 20)
      self.vy_1 += self.distance_y / self.divisor * ((self.distance - self.divisor) / 20) 
      self.pos_1 = self.px_1, self.py_1
      self.vel_1 = self.vx_1, self.vy_1
      self.points[self.p1_index] = self.pos_1, self.vel_1
  def ContainPoints(self):
    for i in range(0, len(self.points), 1):
      self.pos, self.vel = self.points[i]
      self.px, self.py = self.pos
      self.vx, self.vy = self.vel
      self.margin = 15
      self.distance_x_1 = math.copysign(self.px, 1)
      self.distance_x_2 = math.copysign(Simulation.screen_size_x - self.px, 1)
      self.distance_y_1 = math.copysign(self.py, 1)
      self.distance_y_2 = math.copysign(Simulation.screen_size_y - self.py, 1)
      if self.distance_x_1 < self.margin or self.px < self.margin:
        self.vx += math.sqrt(math.pow(self.margin - self.distance_x_1, 2)) 
        self.px = self.margin + 2
      elif self.distance_x_2 < self.margin or self.px > Simulation.screen_size_x:
        self.vx -= math.sqrt(math.pow(self.margin - self.distance_x_2, 2))
        self.px = Simulation.screen_size_x - (self.margin + 2)
      if self.distance_y_1 < self.margin or self.py < self.margin:
        self.vy += math.sqrt(math.pow(self.margin - self.distance_y_1, 2))
        self.py = self.margin + 2
      elif self.distance_y_2 < self.margin or self.py > Simulation.screen_size_y:
        self.vy -= math.sqrt(math.pow(self.margin - self.distance_y_2, 2))
        self.py = Simulation.screen_size_y - (self.margin + 2)
      self.pos = self.px, self.py
      self.vel = self.vx, self.vy
      self.points[i] = self.pos, self.vel
  def FollowMouse(self):
    self.mx, self.my = pygame.mouse.get_pos()
    self.mouse_pressed = pygame.mouse.get_pressed()
    for i in range(0, len(self.points), 1):
      if i not in self.paused and self.mouse_pressed[1] and i in self.near:
        if len(self.paused) == 0: self.paused.append(i)
    for i in range(0, len(self.paused), 1):
      self.pos, self.vel = self.points[self.paused[i]]
      self.pos = self.mx, self.my
      self.vel = 0, 0
      self.points[self.paused[i]] = self.pos, self.vel   
  def MovePoints(self):
    self.resistance = 1.1
    for i in range(0, len(self.points), 1):
      self.pos, self.vel = self.points[i]
      self.px, self.py = self.pos
      self.vx, self.vy = self.vel
      self.px += self.vx
      self.py += self.vy
      self.vx /= self.resistance
      self.vy /= self.resistance
      self.vel = self.vx, self.vy
      self.pos = self.px, self.py
      self.points[i] = self.pos, self.vel
  def Clean(self):
    self.near = []
    if pygame.key.get_pressed()[pygame.K_SPACE]:
      self.points = []
      self.connections = []
      self.selected = []
      self.near = []
      self.paused = []
    if pygame.key.get_pressed()[pygame.K_LCTRL]:
      self.gravity = 2
    if not pygame.mouse.get_pressed()[1]:
      self.paused = []
  def Draw(self):
      self.size = 7
      for i in range(0, len(self.connections), 1):
        self.point_1, self.point_2, self.distance = self.connections[i]
        self.pos_1, self.vel_1 = self.points[self.point_1]
        self.pos_2, self.vel_2 = self.points[self.point_2]
        pygame.draw.aaline(Simulation.screen, (0, 0, 0), self.pos_1, self.pos_2)
      for i in range(0, len(self.points), 1):
        self.pos_1, self.vel_1 = self.points[i]
        self.px, self.py = self.pos_1
        self.px -= self.size / 2
        self.py -= self.size / 2
        if i in self.near and not i in self.selected:
          pygame.draw.rect(Simulation.screen, (255, 0, 0), (self.px, self.py, self.size, self.size))
        elif i in self.selected:
          pygame.draw.rect(Simulation.screen, (0, 0, 255), (self.px, self.py, self.size, self.size))
        else: 
          pygame.draw.rect(Simulation.screen, (0, 0, 0), (self.px, self.py, self.size, self.size))
  def Update(self):
    self.Clean()
    self.HandleInput()
    self.ConnectPoints()
    self.AttractPoints()
    self.ContainPoints()
    self.FollowMouse()
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
      self.clock.tick(120)
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
