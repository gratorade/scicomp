# scicomp project 2
 
How to run simulation: python3 collisions.py 
How to look at plot: python3 plots.py

Benchmark:
For this project I will try to simulate Brownian motion with visual graphics, specifically modelling the movement of hard-sphere-like particles with elastic collision. My benchmark will be to have the “correct physics”. This entails achieving a slope of 1 (liquid state) when measuring the average displacement of particles, and having the correct velocity and movement of particles when they hit the wall as well as when they collide against each other. Results may include a graphic similar to Figure 3 in the paper (tracking particle movement), a scatter plot of particle locations over time, and a plot for the slope of average displacement.

Computing skill of focus:
My computing skill of focus will be similar to the last project: to deepen my knowledge of Python and learn more about how to plot using matplotlib and similar tools. In order to add on to what I’ve learned in the first project, I will aim to successfully plot “over time”, which I failed at last time. I will also add on to prior learning by implementing classes with different attributes, utilizing data structures such as arrays for different purposes, and plotting said data structures in a visually legible way. 

What works:
Many Particle objects can collide against one another and the wall. I increased the Pygame screen size, and I believe I can have 100 Particles shown without sticking/errors. 

Could be improved:
I'm a little confused about the plotting aspect. I spent a long time figuring out dictionaries and lists and arrays to find the most efficient method to plot displacement over time. 
