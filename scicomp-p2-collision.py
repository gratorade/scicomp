"""
Author: Grace Fang
Purpose: Project 2- elastic collision of particles for Scientific Computing
"""
import numpy as np
import random 
import pygame
import math

#details of Pygame window
background_color = (255,255,255)
(width, height) = (300, 200)

#Gaussian distribution of initial velocities

class Particle:
    """
    Class for defining attributes of the Particle
    Arrays will keep track of positions and velocities over time
    Arrays will keep track of x-coordinate and y-coordinate displacement
    Sets x- and y- limits of movement
    Method for collision and specifying Particle movement and action
    """
    def __init__(self, x, y, vx, vy, size):
        """
        Method for defining attributes of Particle class
        Particle must have initial position, initial velocity, and angle
        Particle objects will all have the same size (elastic collision)
        """
        #keeps track of position
        self.position = np.array((float(x), float(y)))
        #keeps track of velocity
        self.velocity = np.array((float(vx), float(vy)))
        self.size = size
        self.mass = self.size**2
        self.angle = 0
        #attributes for graphics
        self.color = (0,0,255)
        self.thickness = 1
        
    #setters and getters for convenience
    @property
    def x(self):
        if self.position[0]>0:
            return self.position[0]
        else:
            return abs(self.position[0])
    @x.setter
    def x(self, n):
        self.position[0] = n
    @property
    def y(self):
        if self.position[1]>0:
            return self.position[1]
        else:
            return abs(self.position[1])
    @y.setter
    def y(self, n):
        self.position[1] = n
    @property
    def vx(self):
        return self.velocity[0]
    @vx.setter
    def vx(self, n):
        self.velocity[0] = n
    @property
    def vy(self):
        return self.velocity[1]
    @vy.setter
    def vy(self, n):
        self.velocity[1] = n
   

    def display(self):
        """
        Method for drawing a citcle, which represents a Particle
        """
        pygame.draw.circle(screen, self.color,
                           (self.x, self.y), self.size, self.thickness)
    
    def move(self):
        """
        Method for moving the Particle 
        Particle will bounce off the walls
        Velocity function: v = dx/dt
        Velocity over time equals
        the instantaneous change in position (dx)
        over the instantaneous change in time (dt)
        """
        #Particle's position moves forward in time
        self.position += self.velocity
        
        #What happens when Particle hits a wall
        #1: when Particle hits x-limit on left side
        if self.x - self.size < 0:
            self.x = self.size
            self.vx = -self.vx
        #2: when Particle hits x-limit on right size
        if self.x + self.size > width:
            self.x = width-self.size
            self.vx = -self.vx
        #3: when Particle hits y-limit on bottom
        if self.y - self.size < 0:
            self.y = self.size
            self.vy = -self.vy
        #4: when Particle hits y-limit on top
        if self.y + self.size > height:
            self.y = height-self.size
            self.vy = -self.vy
    

def collide(p1, p2):
    """
    Method to handle collisions between Particles.
    Particles will have elastic collisions:
    since Particles have the same mass,
    velocity will not be changed
    to preserve momentum

    First we have to to check whether two Particles have collided
    We can measure the distance between the Particles
    using its hypotenuse, and check whether this value is
        less than their combined size
    """
    #change in positions
    dx = p1.x - p2.x
    dy = p1.y - p2.y
        
    #distance between Particles
    distance = math.hypot(dx, dy)
        
    #if distance is less than the Particles' combined size
    if distance < p1.size + p2.size:
        #handle collision
        
        #find combined mass
        m1, m2 = p1.mass, p2.mass
        total_mass = m1 + m2
        
        #simplify variables
        r1, r2 = p1.position, p2.position
        v1, v2 = p1.velocity, p2.velocity
        
        d = np.linalg.norm(r1 - r2)**2
        
        u1 = v1 - 2*m2 / total_mass * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
        u2 = v2 - 2*m1 / total_mass * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
        
        p1.velocity = u1
        p2.velocity = u2
        
        #find the tangent of collision
        #tangent = math.atan2(dy, dx)
        #find angle of collision
        #angle = 0.5 * math.pi + tangent
            
        #find angle as it pertains to Particles
        
        #angle1 = 2*tangent - p1.angle
        #angle2 = 2*tangent - p2.angle

        #change angle
        #p1.angle = angle1
        #p2.angle = angle2

        #change x and y vectors with angle
        #p1.x += math.sin(angle)
        #p1.y -= math.cos(angle)
        #p2.x -= math.sin(angle)
        #p2.y += math.cos(angle)

        
#creates Pygame screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Testing')

#tests random Particle
particle1 = Particle(150, 150, 0.2, 0.2, 20)
particle2 = Particle(10, 10, 0.3, 0.3, 20)
particle3 = Particle(10, 10, 0.3, 0.3, 20)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)

    particle1.move()
    particle2.move()
    #particle3.move()
    particle1.display()
    particle2.display()
    #particle3.display()
    collide(particle1, particle2)
    #collide(particle2, particle1)
    #collide(particle1, particle3)

    pygame.display.flip()
