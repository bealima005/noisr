import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 600
PARTICLE_RADIUS = 10
NUM_PARTICLES = 30
MAX_SPEED = 2

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Particle class
class Particle:
    def __init__(self, x, y, is_tracer=False):
        self.x = x
        self.y = y
        self.radius = PARTICLE_RADIUS
        self.color = RED
        self.speed = random.uniform(1, MAX_SPEED)
        self.angle = random.uniform(0, 2 * math.pi)
        self.is_tracer = is_tracer
        self.path = []

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.path.append((int(self.x), int(self.y)))

        if (self.x - self.radius <= 0 or self.x + self.radius >= WIDTH):
            self.angle = math.pi - self.angle
        if (self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT):
            self.angle = -self.angle

        for other_particle in particles:
            if self.check_collision(other_particle) and other_particle != self:
                angle1 = math.atan2(other_particle.y - self.y, other_particle.x - self.x) # angulo de colisão entre as partículas 

                self_speed_x = other_particle.speed * math.cos(other_particle.angle - angle1)*math.cos(angle1) + self.speed*math.sin(self.angle - angle1)*math.cos(angle1 + math.pi/2)
                self_speed_y = other_particle.speed * math.cos(other_particle.angle - angle1)*math.sin(angle1) + self.speed*math.sin(self.angle - angle1)*math.sin(angle1 + math.pi/2)

                op_speed_x = self.speed * math.cos(self.angle - angle1)*math.cos(angle1) + other_particle.speed*math.sin(other_particle.angle - angle1)*math.cos(angle1 + math.pi/2) # op significa otherp particle
                op_speed_y = self.speed * math.cos(self.angle - angle1)*math.sin(angle1) + other_particle.speed*math.sin(other_particle.angle - angle1)*math.sin(angle1 + math.pi/2)

                self.speed, other_particle.speed = (other_particle.speed, self.speed)
                self.angle = math.atan2(self_speed_y, self_speed_x)
                other_particle.angle = math.atan2(op_speed_y, op_speed_x)

                overlap = self.radius + other_particle.radius - math.sqrt((self.x - other_particle.x)**2 + (self.y - other_particle.y)**2)
                self.x -= overlap * math.cos(angle1)
                self.y -= overlap * math.sin(angle1)
                other_particle.x += overlap * math.cos(angle1)
                other_particle.y += overlap * math.sin(angle1)

            if self.x - self.radius <= 0 :
                self.x = self.radius
            elif self.x + self.radius >= WIDTH:
                self.x = WIDTH - self.radius
            if self.y - self.radius <= 0:
                self.y = self.radius
            elif self.y + self.radius >= HEIGHT:
                self.y = HEIGHT - self.radius
                
    def check_collision(self, other_particle):
        distancia = (self.x - other_particle.x)**2 + (self.y - other_particle.y)**2
        radius = (self.radius + other_particle.radius)**2

        if distancia < radius:
            return True

# Create particles
particles = [Particle(random.randint(PARTICLE_RADIUS, WIDTH - PARTICLE_RADIUS), random.randint(PARTICLE_RADIUS, HEIGHT - PARTICLE_RADIUS)) for _ in range(NUM_PARTICLES)]

# Choose one particle as a tracer
tracer_index = random.randint(0, NUM_PARTICLES - 1)
particles[tracer_index].is_tracer = True
particles[tracer_index].color = BLUE

# Set up Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brownian Motion Simulation")
clock = pygame.time.Clock()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move particles and check collisions
    for particle in particles:
        particle.move()

    # Draw particles and paths
    screen.fill(WHITE)
    for particle in particles:
        pygame.draw.circle(screen, particle.color, (int(particle.x), int(particle.y)), particle.radius)

        # Draw path for the tracer
        if particle.is_tracer and len(particle.path) >= 2:
            pygame.draw.lines(screen, particle.color, False, particle.path, 2)

    pygame.display.flip()
    clock.tick(FPS)