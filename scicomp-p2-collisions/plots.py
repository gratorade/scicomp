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

(width, height) = (1400, 750)

#array to hold Particle objects later
all_particles = []
#array to hold all positions
all_pos = []

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
num_particles = 100
#set the number of Particles to create
while n < num_particles:
    #pick random size within specified range
    #can't be smaller than 1/50th of height's length
    #can't be larger than 1/20th of width's length
    size = random.randint(int(height/50), int(width/20))
    #possible locations, as a list
    x_locations = [*range(size, width-size)]
    y_locations = [*range(size, height-size)]
    #creates Gaussian distribution of initial velocities
    #Particles will have initial random velocity from Gaussian distribution
    #0.2 scale since that creates legible speeds
    gauss = np.random.normal(loc=0.0, scale=0.2, size=None)
    #random location within screen
    x = random.choice(x_locations)
    y = random.choice(y_locations)
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

#dictionary to hold Particle positions
#each particle is a key, with 5 values
pos_dict = {}
#while number of steps is not reached
while current <= timesteps:
    #moves and displays all Particles
    for i, p in enumerate(all_particles):
        p.move()
        #only append 0, 1, 10, 100, and 1000 locations
        if current == 0:
            pos_dict[i] = [p.x]
        elif current == 1 or current==10 or current==100 or current==1000:
            pos_dict[i].append(p.x)
    #any pair of Particles can collide   
    pairs = combinations(range(len(all_particles)), 2)
    for i,j in pairs:
        collide(all_particles[i], all_particles[j])
    current+=1

print("positions:")
print(pos_dict)

#to calculate x-displacement
#calculate the difference between 1-0, 10-0, 100-0, 1000-0
#square each calculation --> displacement of 1 particle
#do it 50 times; divide over each particle --> average
#hold all differences in array to plot later

dis_dict = {}
logs = [1, 2, 3, 4]
for i in pos_dict:
    dis_dict[i] = []
    for n in logs:
        displacement = (pos_dict[i][n] - pos_dict[i][0])**2
        dis_dict[i].append(displacement)

print("displacement:")
print(dis_dict)

#find averages for each timestep
averages = []
for n in range(4):
    step = 0
    for i in dis_dict:
        step+=dis_dict[i][n]
    averages.append(step/100)
    
print("averages")
print(averages)


#plotting displacement with time
plt.scatter([1, 10, 100, 1000], averages, color = "red")
plt.yscale("log")
plt.xscale("log")
#plt.xlim(0, len(x_array))
#plt.ylim(0, len(y_array))
plt.xlabel("timestep")
plt.ylabel("position")
plt.title("position over timestep plot")
plt.show()
#plt.savefig("1particle.png")
plt.close()