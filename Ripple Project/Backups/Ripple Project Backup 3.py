import pygame, sys, random, math
from pygame.locals import *
class RippleHandler():
  def __init__(self):
    self.boxes = []
    self.ripples = []
  def CreateBoxes(self):
    self.size = 14
    self.gap = 1
    self.color = (0, 0, 0)
    self.limit_x = Simulation.screen_size_x / (self.size + self.gap) + 1
    self.limit_y = Simulation.screen_size_y / (self.size + self.gap) + 1
    for i in range(0, self.limit_x, 1):
      for j in range(0, self.limit_y):
        self.px = i * (self.size + self.gap)
        self.py = j * (self.size + self.gap)
        self.position = self.px, self.py
        self.boxes.append((self.position, (self.size, 2), (self.color, self.color)))
  def HandleRipples(self):
    self.pressed = pygame.mouse.get_pressed()
    if self.pressed[0]:
      self.ripples.append((pygame.mouse.get_pos(), 0))
    for i in range(0, len(self.ripples), 1):
      self.position, self.width = self.ripples[i]
      self.width += 1
      self.ripples[i] = self.position, self.width
  def ResizeBoxes(self):
    for i in range(0, len(self.ripples), 1):
      self.r_position, self.r_radius = self.ripples[i]
      self.r_px, self.r_py = self.r_position
      for j in range(0, len(self.boxes), 1):
        self.b_position, self.b_sizes, self.b_colors = self.boxes[j]
        self.b_px, self.b_py = self.b_position
        self.b_orsize, self.b_resize = self.b_sizes
        self.distance = math.sqrt(math.pow(self.b_px - self.r_px, 2) + math.pow(self.b_py - self.r_py, 2))
        if self.distance < (self.r_radius - 40):
          self.new_resize = float(self.b_orsize) / self.r_radius * (self.r_radius - self.distance) + 0.5
          if self.new_resize > self.b_resize: self.b_resize = self.new_resize
          self.b_sizes = self.b_orsize, self.b_resize
        else: self.b_resize = 1
        self.boxes[j] = self.b_position, self.b_sizes, self.b_colors
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
    self.HandleRipples()
    self.ResizeBoxes()
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
