#! /usr/bin/env python
"""
going from springs to gravitation --> planetary orbits
"""
from numpy import sqrt
from numpy import array, zeros, roll
import pygame as pg

#from pygame import display, draw # using this allows you to make the code below shorter
#from pygame import *  # allows also short code, but the reader then has to know or needs
# time to discover that QUIT, K_ESCAPE, draw etc. come from pygame
# if all stuff from both, numpy and pygame is imported with *, then understanding the code
# becomes much more tedious for somebody not familiar with the libraries
# and it becomes problematic if both libraries have functions with identical names

m = 1.     # the mass
g = 1.     # the gravitation constant
x = array([0.,1.])     # the initial position in 2D space
c = array([0.,0.])     # the center, the sun, the location where the force is pointing at
t = 0.     # start time
dt = 0.005 # the time step, try out the setting of pend_02a.py
N = 100    # how many steps to calculate
v = array([0.6,0.])     # velocity

def one_step():
    global t,x,v  # so these variables don't become local ones when redefined in here
    r = sqrt(x[0]**2+x[1]**2)
    n = (c-x)/r   # vector of unit length pointing at c
    f = g*n/r**2  # the force at the moment
    a = f/m       # acceleration
    v = v + a*dt  # new speed modified by accceleration acting during the time of one time step
    x = x + v*dt
    t = t+dt


pg.init()
BG_colour = (0,0,0)
planet_colour = (120,120,255)
width, height = 480, 360
pgcenterx, pgcentery = width/2, height/2
screen = pg.display.set_mode((width, height))

def to_pg_coords(vec):
    xx,yy = vec # local variables
    # x,y = vec # if I had written this there would be no way to get hold of the global x and y inside this function
    pgx = pgcenterx + int(100*xx) # one unit in the physics coordinate system is 100 pixels
    pgy = pgcentery - int(100*yy) # why the minus sign? --> in the pygame canvas the origin is in the upper left corner
    return pgx,pgy

pg.draw.circle(screen, (255,200,100), to_pg_coords([0,0]), 15)
pg.draw.circle(screen, planet_colour, to_pg_coords(x), 8)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False

    one_step()

    screen.fill(BG_colour)
    pg.draw.circle(screen, (255,200,100), to_pg_coords([0,0]), 15)
    pg.draw.circle(screen, planet_colour, to_pg_coords(x), 8)
    pg.display.flip()


"""
Right now the computer works of one command after the other in a tight sequence.
Nowhere are we telling it to wait for a certain time. You see that this version
is much faster than the other version using matplotlib, a library that has been
programmed with other purposes in mind as speed.

Perhaps you already see the problem which is arising from this: as more work is
added inside the while loop (more planets, more complicated graphics like nice
spaceship pictures instead of circles, player interaction, cannonballs flying
around etc.) the simulation gets slower and you would have to tune the time
step to keep the desired simulation speed. This may bring the simulation into
a regime where it becomes unrealistic because of a too large time step. On the
other hand, running the same thing on a better computer makes it faster, and
the simulation or game may suddenly be too fast to be useful or fun. So, in
the future we will need better ways of controlling the simulation speed and the
canvas framerate separately.

The other problem: in the way the code is written now, adding more planets
means adding more variables, and they all need new names. and it is impossible
to create new moving things like missiles during the game run. This will be
solved with object-orientation. There you define classes of things, of which
it is easy to create ever new instances or to erase them.

Challenge inspirations:
 - make the planet colour speed-dependent
 - modify the version with the trace below: turn the planet into a comet
   (e.g. three traces small angles apart, the middle trace longer, not only
   direction, but also brightness and length depend on the distance from and
   the direction of the sun)
 - make the sun moveable by arrow keys (requires a look into the pygame documentation)
(but don't waste too much time here; wasting a bit of time here is useful to
let you feel the contrast of how much better it is to work with the object-
oriented version)

the pygame documentation:
http://www.pygame.org
"""

"""
# below: same but planet leaves a little trace

m = 1.     # the mass
g = 1.     # the gravitation constant
x = array([0.,1.])     # the initial position in 2D space
c = array([0.,0.])     # the center, the sun, the location where the force is pointing at
t = 0.     # start time
dt = 0.005 # the time step, try out the setting of pend_02a.py
N = 100    # how many steps to calculate
v = array([0.6,0.])     # velocity

ntrace=10  # how many points to save for the trace drawn by the planet
trace=zeros((ntrace,2),dtype=int) # integer, because we want to save the pygame coordinates which are pixel numbers

def one_step():
    global t,x,v  # so these variables don't become local ones when redefined in here
    r = sqrt(x[0]**2+x[1]**2)
    n = (c-x)/r   # vector of unit length pointing at c
    f = g*n/r**2  # the force at the moment
    a = f/m       # acceleration
    v = v + a*dt  # new speed modified by accceleration acting during the time of one time step
    x = x + v*dt
    t = t+dt


pg.init()
BG_colour     = (0,0,0)
planet_colour = (120,120,255)
trace_colour  = (200,200,200)
width, height = 480, 360
pgcenterx, pgcentery = width/2, height/2
screen = pg.display.set_mode((width, height))

def to_pg_coords(vec):
    xx,yy = vec # local variables
    # x,y = vec # if I had written this there would be no way to get hold of the global x and y inside this function
    pgx = pgcenterx + int(100*xx) # one unit in the physics coordinate system is 100 pixels
    pgy = pgcentery - int(100*yy) # why the minus sign? --> in the pygame canvas the origin is in the upper left corner
    return pgx,pgy

pg.draw.circle(screen, (255,200,100), to_pg_coords([0,0]), 15)
pg.draw.circle(screen, planet_colour, to_pg_coords(x), 8)

# What are the following two lines for?
#for i in xrange(ntrace):
#    trace[i,:] = to_pg_coords(x)

counter = 0
trace_update_interval = 10
running = True
while running:
    counter+=1
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False

    one_step()
    
    if counter % trace_update_interval == 0:
        trace[:,:]=roll(trace,1,axis=0)
        trace[0,:]=to_pg_coords(x)

    screen.fill(BG_colour)
    pg.draw.circle(screen, (255,200,100), to_pg_coords([0,0]), 15)
    pg.draw.circle(screen, planet_colour, to_pg_coords(x), 8)
    pg.draw.aalines(screen, trace_colour, False, trace)
    pg.display.flip()
"""