import pygame, sys, random, math, pygame.gfxdraw
from pygame.locals import *
class WebHandler:
  def __init__(self):
    self.points = []
    self.connections = []
    self.selected = []
    self.near = []
    self.paused = []
  def CreatePoints(self):
    self.mouse_pressed = pygame.mouse.get_pressed()
    if self.mouse_pressed[0]:
      self.mx, self.my = pygame.mouse.get_pos()
      self.points.append(((self.mx, self.my), (0, 0)))
      self.selected = []
  def AttractPoints(self):
    for i in range(0, len(self.connections), 1):
      self.point_1, self.point_2, self.distance, self.is_active = self.connections[i]
      if self.is_active == True:
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
    self.max_size = 150
    self.select_distance = 40
    for i in range(0, len(self.points), 1):
      self.pos, self.vel = self.points[i]
      self.px, self.py = self.pos
      self.vx, self.vy = self.vel
      self.mx, self.my = pygame.mouse.get_pos()
      self.mouse_pressed = pygame.mouse.get_pressed()
      self.distance = math.sqrt(math.pow(self.mx - self.px, 2) + math.pow(self.my - self.py, 2))
      if self.distance < self.select_distance:
        self.near.append(i)
      if self.distance < self.select_distance and self.mouse_pressed[2] and not i in self.selected:
        self.selected.append(i)
        self.is_on_target = True
      if len(self.selected) > 1:
        self.inside = False
        for i in range(self.min_size, self.max_size, 1):
          if (self.selected[0], self.selected[1], i, False) in self.connections: self.inside = True; break
          if (self.selected[0], self.selected[1], i, True) in self.connections: self.inside = True; break
          if (self.selected[1], self.selected[0], i, False) in self.connections: self.inside = True; break
          if (self.selected[1], self.selected[0], i, True) in self.connections: self.inside = True; break
        if self.inside == False:
          self.attraction = 100
          self.connections.append((self.selected[0], self.selected[1], self.attraction, True))
          self.connections.append((self.selected[1], self.selected[0], self.attraction, True))
        self.selected = []          
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
      self.pos, self.vel = self.points[i]
      self.px, self.py = self.pos
      self.vx, self.vy = self.vel
      self.distance = math.sqrt(math.pow(self.mx - self.px, 2) + math.pow(self.my - self.py, 2))
      if self.mouse_pressed[1] and i in self.near:
        if not i in self.paused and len(self.paused) < 1: self.paused.append(i)
        for j in range(0, len(self.connections), 1):
          self.first, self.second, self.size, self.is_active = self.connections[j]
          if self.first == i: self.is_active = False
          self.connections[j] = self.first, self.second, self.size, self.is_active
      if i in self.paused:
        self.px = self.mx
        self.py = self.my
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
    self.stiffness = 1.1
    self.gravity = 0
    self.keyboard_pressed = pygame.key.get_pressed()
    self.mouse_pressed = pygame.mouse.get_pressed()
    if self.keyboard_pressed[pygame.K_SPACE]:
      self.points = []
      self.connections = []
      self.selected = []
      self.near = []
    if not self.mouse_pressed[1]:
      self.paused = []
    for i in range(0, len(self.points), 1):
      self.pos, self.vel = self.points[i]
      self.px, self.py = self.pos
      self.vx, self.vy = self.vel
      self.vx /= self.stiffness
      self.vy /= self.stiffness
      self.vy += self.gravity
      self.vel = self.vx, self.vy
      self.pos = self.px, self.py
      self.points[i] = self.pos, self.vel
    for i in range(0, len(self.connections), 1):
      self.first, self.second, self.size, self.is_active = self.connections[i]
      self.is_active = True
      self.connections[i] = self.first, self.second, self.size, self.is_active
  def Draw(self):
      self.size = 7
      for i in range(0, len(self.connections), 1):
        self.point_1, self.point_2, self.distance, self.is_active = self.connections[i]
        self.pos_1, self.vel_1 = self.points[self.point_1]
        self.pos_2, self.vel_2 = self.points[self.point_2]
        pygame.draw.aaline(Simulation.screen, (0, 0, 0), self.pos_1, self.pos_2)
      for i in range(0, len(self.points), 1):
        self.pos_1, self.vel_1 = self.points[i]
        self.px, self.py = self.pos_1
        self.px -= self.size / 2
        self.py -= self.size / 2
        pygame.draw.rect(Simulation.screen, (0, 0, 0), (self.px, self.py, self.size, self.size))
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
