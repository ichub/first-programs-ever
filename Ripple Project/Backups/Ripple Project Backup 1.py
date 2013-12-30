import pygame, sys, random, math
from pygame.locals import *
class RippleHandler():
  def __init__(self):
    self.boxes = []
    self.ripples = []
  def CreateBoxes(self):
    self.size = 20
    self.gap = 5
    self.color = (0, 0, 0)
    self.limit_x = Simulation.screen_size_x / (self.size + self.gap) + 1
    self.limit_y = Simulation.screen_size_y / (self.size + self.gap) + 1
    for i in range(0, self.limit_x, 1):
      for j in range(0, self.limit_y):
        self.px = i * (self.size + self.gap)
        self.py = j * (self.size + self.gap)
        self.position = self.px, self.py
        self.boxes.append((self.position, (self.size, self.size), (self.color, self.color)))
  def DrawBoxes(self):
    for i in range(0, len(self.boxes), 1):
      self.position, self.sizes, self.colors = self.boxes[i]
      self.or_color, self.re_color = self.colors
      self.or_size, self.re_size = self.sizes
      self.px, self.py = self.position
      self.adjust = self.re_size / 2
      self.px -= self.adjust
      self.py -= self.adjust
      pygame.draw.rect(Simulation.screen, self.re_color, (self.px, self.py, self.re_size, self.re_size))
  def Update(self):
    self.DrawBoxes()
    
           
class Program:
  def __init__(self):
    pygame.init()
    self.screen_size_x = 800
    self.screen_size_y = 600
    self.screen_size = self.screen_size_x, self.screen_size_y
    self.clock = pygame.time.Clock()
    self.screen = pygame.display.set_mode(self.screen_size, 0, 32)
    pygame.display.set_caption("Ripple Project")
  def Update(self):
    self.Ripples = RippleHandler()
    self.Ripples.CreateBoxes()
    while True:
      self.clock.tick(60)
      self.screen.fill((255, 255, 255))
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
      self.Ripples.Update()
      pygame.display.flip()
Simulation = Program()
Simulation.Update()
