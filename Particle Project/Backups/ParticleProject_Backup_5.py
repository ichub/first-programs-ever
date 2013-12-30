import pygame, sys, random, math
from pygame.locals import *
particles = []
screen_size_x = 640
screen_size_y = 480
particle_size = 2

def Create_Particles(number):
    """Creates specified amount of particles"""
    if len(particles) >= number:
        return
    for i in range(0, number, 1):
        x = random.randint(6, 640)
        y = random.randint(6, 480)
        m = random.randint(0, 255)
        n = random.randint(0, 255)
        o = random.randint(0, 255)
        x -= x % 5
        y -= y % 5
        tail = []
        particles.append((x, y, 0, 0, m, n, o, tail))
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
        if mx > 635 or mx < 5 or my > 475 or my < 5:
            mx, my = 1000, 1000
        px, py, vx, vy, m, n, o, tail = particles[i]
        distance = math.pow(math.pow(px - mx, 2) + math.pow(py - my, 2), 0.5)
        if distance <= 200:
            distance_x = mx - px
            distance_y = my - py
            divisor = math.pow((distance_x * distance_x + distance_y * distance_y), 0.5)
            speed_x = distance_x / divisor / 20
            speed_y = distance_y / divisor / 20
            vx += speed_x
            vy += speed_y
        vy += Gravity
        if py >= screen_size_y - particle_size:
            py = screen_size_y - particle_size
            vy /= 2
            vy *= -1
        elif py <= 0 or py + vy <= 0:
            py = 0
            vy /= 2
            vy *= -1
        if px >= screen_size_x - particle_size:
            px = screen_size_x - particle_size
            vx /= 2
            vx *= -1
        elif px <= 0 or px + vx <= 0:
            px = 0
            vx /= 2
            vx *= -1

        vx /= 1.0001
        vy /= 1.0001
        py += vy
        px += vx
        tail.append((px, py))
        if len(tail) > 10:
            tail.pop(0)
        particles[i] = px, py, vx, vy, m, n, o, tail
            
def Show_Particles(tail_type):
    """Shows particles on screen"""
    if len(particles) != 0: 
        screen.lock()
        for i in range(0, len(particles), 1):
            x, y, vx, vy, m, n, o, tail = particles[i]
            if tail_type == 1:
                pygame.draw.line(screen, (m, n, o), tail[0], tail[len(tail) - 1], particle_size)
            if tail_type == 2:
                for j in range(0, len(tail) - 1, 1):
                    pygame.draw.line(screen, (m, n, o), tail[j], tail[j + 1], particle_size)
            if tail_type == 3:
                px, py = tail[0]
                pygame.draw.rect(screen, (m, n, o), (px, py, particle_size, particle_size))
        screen.unlock()    

def Handle_Particles():
    Simulate_Gravity(0.01)
    Show_Particles(2)
    
pygame.init()
screen = pygame.display.set_mode((screen_size_x, screen_size_y), 0, 32)
Create_Particles(200)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((255, 255, 255))
    Handle_Particles()
    pygame.display.update()
