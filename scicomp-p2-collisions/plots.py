"""
Author: Grace Fang
Purpose: Project 2 elastic collision of particles
         plotting average displacement over time on matplotlib
         for Scientific Computing at Olin College
Date: 03/01/2023
"""
import numpy as np
import random 
import math
from itertools import combinations
import matplotlib.pyplot as plt

#details of Pygame window: color and size
background_color = (255, 204, 255)
(width, height) = (500, 500)

#array to hold Particle objects later
all_particles = []

#array to hold Particle positions, for plotting
all_positions = []
x_positions = []
y_positions = []

#average displacement is found with the total displacement
#(sum of individual displacements), divided over the total timestep amount.
#we can plot position over time, and calculate the slope.

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
    velocity will be changed to preserve momentum.
    
    This formula will be used:
    m1u1 + m2u2 = m1v1 + m2v2
    where u1 and u2 are the final velocities
    and v1 and v2 are the initial velocities.
    """
    #check of Particles overlap, then handle collision
    if overlap(p1, p2):
        
        #simplify variables: initial velocities and mass
        v1, v2 = p1.velocity, p2.velocity
        m1, m2 = p1.mass, p2.mass
        
        #find combined mass
        total_mass = m1 + m2
        
        #finding new velocities (u1, u2) with formula
        u1 = ((m1-m2)*v1 + 2*m2*v2) / total_mass
        u2 = ((m2-m1)*v2 + 2*m1*v1) / total_mass
        
        #sets new velocities for Particles
        p1.velocity = u1
        p2.velocity = u2


#creating Particles
n = 0
#set the number of Particles to create
while n in range(1):
    #pick random size within specified range
    #can't be smaller than 1/50th of height's length
    #can't be larger than 1/10th of height's length
    size = random.randint(int(height/50), int(height/10))
    
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

#running through a set number of steps (1000)
#this is to make finding displacement over time easier
current = 0
timesteps = 1000

#while number of steps is not reached
while current < timesteps:
    #moves and displays all Particles
    for p in all_particles:
        p.move()
        #appending each position in array
        all_positions.append(p.position)
        x_positions.append(p.x)
        y_positions.append(p.y)
    #any pair of Particles can collide
    pairs = combinations(range(len(all_particles)), 2)
    for i,j in pairs:
        collide(all_particles[i], all_particles[j])
    #iterate
    current+=1

#to calculate x-displacement
#calculate the difference between each pair of positions
#add all differences to find sum --> total
#divide over timestep --> average
#hold all differences in array to plot later

numx = 0
x_displacement = 0
x_array = []
while numx < (len(x_positions)-1):
    x_displacement += (x_positions[numx+1] - x_positions[numx])
    x_array.append(x_displacement)
    numx += 1

print(f'total x-displacement is: {x_displacement}')

average_x = x_displacement/timesteps
print(f'average x-displacement is: {average_x}')

plt.scatter(range(0,len(x_array)), x_array, color = "green")
plt.xlim(0, len(x_array))
plt.xlabel("total timestep = 1000")
plt.ylabel("x-position")
plt.title("x-position over timestep plot")
plt.show()
plt.close()

#to calculate y-displacement
#calculate the difference between each pair of positions
#add all differences to find sum --> total
#divide over timestep --> average
numy = 0
y_displacement = 0
y_array = []
while numy < (len(y_positions)-1):
    y_displacement += (y_positions[numy+1] - y_positions[numy])
    y_array.append(y_displacement)
    numy += 1

print(f'total y-displacement is: {y_displacement}')

average_y = y_displacement/timesteps
print(f'average y-displacement is: {average_y}')

plt.scatter(range(0,len(y_array)), y_array, color = "blue")
plt.xlim(0, len(y_array))
plt.xlabel("total timestep = 1000")
plt.ylabel("y-position")
plt.title("y-position over timestep plot")
plt.show()
plt.close()

#how to plot displacement for multiple particles?
#instead of a list, use array
#each row/column is a different particle
#plot both row/columns individually
#find the average displacement over time for each row/column
#plot that ^ ?
