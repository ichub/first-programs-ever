import pygame, sys, random, math
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

Background_Image = "C:\Users\Vanusha\Desktop\Work\Programming\Python\Projects\Finished Projects\Particle Project\Backups\Background.png"
Particle_Image = "C:\Users\Vanusha\Desktop\Work\Programming\Python\Projects\Finished Projects\Particle Project\Backups\Particle.png"
Background = pygame.image.load(Background_Image).convert()
Particle = pygame.image.load(Particle_Image).convert()
particles = []    
x, y = pygame.mouse.get_pos()

def Create_Particles(number):
    """Creates specified amount of particles"""
    if len(particles) >= number:
        return
    for i in range(0, number + 1, 1):
        x = random.randint(0, 640)
        y = random.randint(0, 480)
        x -= x % 5
        y -= y % 5
        particles.append((x, y))
    to_delete = []
    particles.sort()
    for j in range(0, len(particles) - 1, 1):
        if particles[j] == particles[j + 1]:
            to_delete.append(j)
    if len(to_delete) != 0:
        for k in range(0, len(to_delete), 1):
            particles.pop(to_delete[k])
            for l in range(0, len(to_delete), 1):
                to_delete[l] -= 1
    
def Move_Particles():
    """Moves particles toward a point"""
    for i in range(0, len(particles), 1):
        x, y = pygame.mouse.get_pos()
        px, py = particles[i]
        in_range = False
        if px > x - 1:
            if px < x + 1:
                if py > y - 1:
                    if py < y + 1:
                        in_range = True
        
        if in_range == False:
            distance_x = x - px
            distance_y = y - py
            divisor = math.pow((distance_x * distance_x + distance_y * distance_y), 0.5)
            speed_x = distance_x / divisor / 2
            speed_y = distance_y / divisor / 2 
            py += speed_y
            px += speed_x
            particles[i] = (px, py)
        if in_range == True:
            q = random.randint(-250, 250)
            w = random.randint(-250, 250)
            px += q
            py += w
            particles[i] = (px, py)
             
def Show_Particles():
    """Shows particles on screen"""
    if len(particles) != 0:
        for i in range(0, len(particles), 1):
            screen.blit(Particle, particles[i])
    return

Create_Particles(300)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(Background, (0, 0))
    Move_Particles()
    Show_Particles()
    pygame.display.update()
