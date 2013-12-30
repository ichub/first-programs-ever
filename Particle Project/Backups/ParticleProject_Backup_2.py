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
        x = random.randint(6, 640)
        y = random.randint(6, 480)
        x -= x % 5
        y -= y % 5
        vx = random.uniform(0.1, -0.1)
        particles.append((x, y, vx, 0))
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
        px, py, vx, vy = particles[i]
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
            vx, vy = speed_x, speed_y
            px += vx
            py += vy
            particles[i] = (px, py, vx, vy)
        if in_range == True:
            q = random.randint(-250, 250)
            w = random.randint(-250, 250)
            px += q
            py += w
            particles[i] = (px, py, vx, vy)

def Simulate_Gravity(Gravity):
    """Simulates gravity with a given strength"""
    for i in range(0, len(particles), 1):      
        mx, my = pygame.mouse.get_pos()
        px, py, vx, vy = particles[i]
        distance = math.pow(math.pow(px - mx, 2) + math.pow(py - my, 2), 0.5)

        if distance <= 100:
            distance_x = mx - px
            distance_y = my - py
            divisor = math.pow((distance_x * distance_x + distance_y * distance_y), 0.5)
            speed_x = distance_x / divisor / 100
            speed_y = distance_y / divisor / 100
            vx += speed_x
            vy += speed_y
        
        vy += Gravity
        vx += random.uniform(0.001, -0.001)
        if py >= 476:
            py = 476
            vy /= 1.1
            vy *= -1
        elif py <= 1:
            py = 1
            vy /= 1.1
            vy *= -1
        if px >= 636:
            px = 636
            vx /= 1.4
            vx *= -1
        elif px <= 1:
            px = 1
            vx /= 1.4
            vx *= -1
        py += vy
        px += vx
        particles[i] = px, py, vx, vy

def Show_Particles():
    """Shows particles on screen"""
    if len(particles) != 0:
        for i in range(0, len(particles), 1):
            x, y, z, a = particles[i]
            screen.blit(Particle, (x, y))
    return

Create_Particles(300)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    Simulate_Gravity(0.001)
    screen.blit(Background, (0, 0))
    Show_Particles()
    pygame.display.update()
