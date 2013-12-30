import pygame, sys, random, math
from pygame.locals import *
class RippleHandler():
  def __init__(self):
    self.boxes = []
    self.ripples = []
  def CreateBoxes(self):
    self.size = 15
    self.gap = 15
    self.color = (0, 0, 255)
    self.limit_x = Simulation.screen_size_x / (self.size + self.gap) + 1
    self.limit_y = Simulation.screen_size_y / (self.size + self.gap) + 1
    for i in range(0, self.limit_x, 1):
      for j in range(0, self.limit_y):
        self.px = i * (self.size + self.gap)
        self.py = j * (self.size + self.gap)
        self.position = self.px, self.py
        self.boxes.append((self.position, (self.size, 2), (self.color, self.color)))
  def CreateRipples(self):
      self.ripples.append((pygame.mouse.get_pos(), 0, random.randint(50, 200)))
  def Refresh(self):
    for i in range(0, len(self.boxes), 1):
      self.b_position, self.b_sizes, self.b_colors = self.boxes[i]
      self.b_orsize, self.b_resize = self.b_sizes
      self.b_orcolor, self.b_recolor = self.b_colors
      self.b_recolor = (0, 0, 0)
      self.b_resize = 2
      self.b_colors = self.b_orcolor, self.b_recolor
      self.b_sizes = self.b_orsize, self.b_resize
      self.boxes[i] = self.b_position, self.b_sizes, self.b_colors
    self.to_delete = []
    for i in range(0, len(self.ripples), 1):
      self.position, self.radius, self.width = self.ripples[i]
      self.radius += 5
      if self.radius > 1000 + self.width: self.to_delete.append(i)
      self.ripples[i] = self.position, self.radius, self.width
    for i in range(0, len(self.to_delete), 1):
      self.ripples.pop(self.to_delete[i])
      for j in range(i, len(self.to_delete) - i, 1):
        self.to_delete[j] -= 1
  def ResizeBoxes(self):
    for i in range(0, len(self.ripples), 1):
      self.r_position, self.r_radius, self.r_width = self.ripples[i]
      self.r_px, self.r_py = self.r_position
      if self.r_width > self.r_radius: self.r_width = self.r_radius
      for j in range(0, len(self.boxes), 1):
        self.b_position, self.b_sizes, self.b_colors = self.boxes[j]
        self.b_px, self.b_py = self.b_position
        self.b_orsize, self.b_resize = self.b_sizes
        self.distance = math.sqrt(math.pow(self.b_px - self.r_px, 2) + math.pow(self.b_py - self.r_py, 2))
        self.r_distance = math.copysign(self.distance - self.r_radius, 1)
        if self.r_distance < self.r_width:
          self.new_resize = float(self.b_orsize) / self.r_width * (self.r_width - self.r_distance) + 0.5
          if self.new_resize > self.b_resize: self.b_resize = self.new_resize
        self.b_sizes = self.b_orsize, self.b_resize
        self.boxes[j] = self.b_position, self.b_sizes, self.b_colors
  def RecolorBoxes(self):
    for i in range(0, len(self.ripples), 1):
      self.r_position, self.r_radius, self.r_width = self.ripples[i]
      self.r_px, self.r_py = self.r_position
      if self.r_width > self.r_radius: self.r_width = self.r_radius
      for j in range(0, len(self.boxes), 1):
        self.b_position, self.b_sizes, self.b_colors = self.boxes[j]
        self.b_px, self.b_py = self.b_position
        self.b_orcolor, self.b_recolor = self.b_colors
        self.b_r, self.b_g, self.b_b = self.b_orcolor
        self.distance = math.sqrt(math.pow(self.b_px - self.r_px, 2) + math.pow(self.b_py - self.r_py, 2))
        self.r_distance = math.copysign(self.distance - self.r_radius, 1)
        if self.r_distance < self.r_width:
          self.new_r = float(self.b_r) / self.r_width * (self.r_width - self.r_distance)
          self.new_g = float(self.b_g) / self.r_width * (self.r_width - self.r_distance)
          self.new_b = float(self.b_b) / self.r_width * (self.r_width - self.r_distance)
          self.new_recolor = self.new_r, self.new_g, self.new_b
          if self.new_recolor > self.b_recolor:
            self.b_recolor = self.new_recolor
        self.b_colors = self.b_orcolor, self.b_recolor
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
    self.Refresh()
    self.ResizeBoxes()
    self.RecolorBoxes()
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
          self.Ripples.CreateRipples()
      self.Ripples.Update()
      pygame.display.flip()
Simulation = Program()
Simulation.Update()
