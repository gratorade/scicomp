"""
Author: Grace Fang
Consulted:
    1) Christian Hill (xnx on GitHub)
        https://github.com/xnx/collision
        https://scipython.com/blog/two-dimensional-collisions/
    2) Peter Collingridge (petercollingridge on GitHub)
        https://github.com/petercollingridge/code-for-blog/tree/master/pygame%20physics%20simulation
        https://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/collisions/
Purpose: Project 2, elastic collision of particles, for Scientific Computing at Olin College
Date: 02/27/2023
"""
import numpy as np
import random 
import pygame
import math
from itertools import combinations
import matplotlib.pyplot as plt

#details of Pygame window
background_color = (255, 204, 255)
(width, height) = (500, 500)

#array to hold Particle objects later
all_particles = []

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
        self.color = (0,51,0)
        self.thickness = 2
        
    #setters and getters for convenience
    @property
    def x(self):
        return self.position[0]
    @x.setter
    def x(self, n):
        self.position[0] = n
    @property
    def y(self):
        return self.position[1]
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
    
def overlap(p1, p2):
    """
    Method for checking whether Particles overlap
    We can measure the distance between the Particles
    using its hypotenuse, and check whether this value is
    less than their combined size
    
    Useful for collide function
    Also useful for starting positions of Particles
    """
    #change in positions
    dx = p1.x - p2.x
    dy = p1.y - p2.y
        
    #distance between Particles
    distance = math.hypot(dx, dy)
        
    #if distance is less than the Particles' combined size
    if distance < p1.size + p2.size:
        return True

def collide(p1, p2):
    """
    Method to handle collisions between Particles.
    Particles will have elastic collisions:
    since Particles do not have the same mass,
    velocity will be changed to preserve momentum
    
    This formula will be used:
    m1u1 + m2u2 = m1v1 + m2v2
    where u1 and u2 are the final velocities
    and v1 and v2 are the initial velocities
    """
    #check of Particles overlap, then handle collision
    if overlap(p1, p2):
        
        #find combined mass
        m1, m2 = p1.mass, p2.mass
        total_mass = m1 + m2
        
        #simplify variables
        #initial velocities
        v1, v2 = p1.velocity, p2.velocity
        
        #finding new velocities with formula
        u1 = ((m1-m2)*v1 + 2*m2*v2) / total_mass
        u2 = ((m2-m1)*v2 + 2*m1*v1) / total_mass
        
        #sets new velocities
        p1.velocity = u1
        p2.velocity = u2


#creates Pygame screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Testing')

#creating Particles
n = 0
#set the number of Particles to create
while n in range(10):
    #pick random size within specified range
    #can't be smaller than 1/50th of height's length
    #can't be larger than 1/10th of height's length
    size = random.randint(height/50, height/10)
    
    #possible locations, as a list
    locations = [*range(size, width-size)]
    
    #creates Gaussian distribution of initial velocities
    #Particles will have initial random velocity from Gaussian distribution
    #0.2 scale since that creates legible speeds
    gauss = np.random.normal(loc=0.0, scale=0.2, size=None)
    
    #random location within screen
    x = random.choice(locations)
    y = random.choice(locations)
    
    #checks for overlap
    for p2 in all_particles:
        #does not add new Particle if it overlaps with existing one
        if overlap(p2, Particle(x,y,0,0,size)):
            #breaks out of for-loop, back to while loop
            #tries again with a new location
            break
    #if new Particle does not overlap
    #create the Particle and append it to array
    #iterate because now we have placed a new Particle
    else:  
        particle = Particle(x, y, gauss, gauss, size)
        all_particles.append(particle)
        n+=1


#running through a set number of steps
#this is to make finding displacement over time easier
current = 0
total = 1000
#to set frames per second later
clock = pygame.time.Clock()

#while number of steps is not reached
while current < total:
    for event in pygame.event.get():
        #only quits when this is typed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(background_color)
    
    #moves and displays all Particles
    for p in all_particles:
        p.move()
        p.display()

    #any pair of Particles can collide
    pairs = combinations(range(len(all_particles)), 2)
    for i,j in pairs:
        collide(all_particles[i], all_particles[j])
    
    pygame.display.flip()
    
    #sets frame rate for smoothness
    clock.tick(100)
    #iterate
    current+=1
