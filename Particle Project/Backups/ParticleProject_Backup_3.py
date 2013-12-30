import pygame, sys, random, math
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
particles = []    

def Create_Particles(number):
    """Creates specified amount of particles"""
    if len(particles) >= number:
        return
    for i in range(0, number, 1):
        x = random.randint(6, 640)
        y = random.randint(6, 480)
        x -= x % 5
        y -= y % 5
        particles.append((x, y, 0, 0))
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
    
def Simulate_Gravity(Gravity):
    """Simulates gravity with a given strength"""
    for i in range(0, len(particles), 1):      
        mx, my = pygame.mouse.get_pos()
        px, py, vx, vy = particles[i]
        distance = math.pow(math.pow(px - mx, 2) + math.pow(py - my, 2), 0.5)

        if distance <= 150:
            distance_x = mx - px
            distance_y = my - py
            divisor = math.pow((distance_x * distance_x + distance_y * distance_y), 0.5)
            speed_x = distance_x / divisor / 20
            speed_y = distance_y / divisor / 20
            vx += speed_x
            vy += speed_y
        vy += Gravity
        if py >= 477:
            py = 477
            vy /= 2
            vy *= -1
        elif py <= 0:
            py = 0
            vy /= 2
            vy *= -1
        if px >= 637:
            px = 637
            vx /= 2
            vx *= -1
        elif px <= 0:
            px = 0
            vx /= 2
            vx *= -1
        if Gravity != 0:
            vx += random.uniform(0.01, -0.01)
            py += vy
            px += vx 
            particles[i] = px, py, vx, vy
        else:
            vx /= 1.01
            vy /= 1.01
            px += vx
            py += vy
            particles[i] = px, py, vx, vy
            
def Show_Particles():
    """Shows particles on screen"""
    if len(particles) != 0: 
        for i in range(0, len(particles), 1):
            color = i % 255
            x, y, z, a = particles[i]
            screen.lock()
            pygame.draw.rect(screen, (0, 100, 0), (x, y, 3, 3))
            screen.unlock()
    return

Create_Particles(250)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((255, 255, 255))
    Simulate_Gravity(0.01)
    Show_Particles()
    pygame.display.update()
