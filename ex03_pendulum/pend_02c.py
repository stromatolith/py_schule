#! /usr/bin/env python
"""
going from springs to gravitation --> planetary orbits
... but now in object-oriented style

compare with the last version: see how much easier it is to add more and more
planets here.

teacher job (or book): explain "encapsulation", "inheritance", "polymorphism",
"function", "method", "attribute", "superclass", "subclass", ...... 
"""
import numpy as np
from numpy import sqrt
from numpy import array, asfarray
import matplotlib.pyplot as plt
from matplotlib import patches, animation

class Sun(object):

    def __init__(self,position,radius):
        self.x=asfarray(position)
        self.radius=radius
        self.patch=None
        self.fc='y'
        self.ec='r'
    
    def initialize_patch(self):
        self.patch=patches.Circle( self.x, self.radius, fc=self.fc,ec=self.ec)
    
    def update_patch(self):
        self.patch.center = self.x

    def set_position(self,newpos):
        self.x[:]=newpos
    
    def get_position(self):
        return self.x
    
    def get_patch(self):
        return self.patch
    
    def one_step(self):
        pass


class Planet(Sun):
    """
    inherits everything from sun, but some are overwritten, like e.g. __init__()
    """
    g=1. # define it here makes it impossible to have individual gravitation constants for each planet
    k=1.
    dt=0.03
    def __init__(self,mass,facecolor='cyan',edgecolor='blue'):
        self.m=mass
        self.radius = 0.1*mass**0.33
        self.x=array([0.,1.])
        self.v=array([0.,0.])
        self.fc=facecolor
        self.ec=edgecolor
        self.xdata = []
        self.ydata = []
        self.attractor=None
        self.force_law='gravitation' # 'gravitation' or 'rubber'
        #self.g=1.  # defining it here on the other hand leaves the freedom to set it differently for each planet
        #self.k=1.
        #self.dt=0.03
    
    def set_attractor(self,target):
        self.attractor=target
        
    def set_velocity(self,v):
        self.v[:]=v
    
    def one_step(self):
        c = self.attractor.x
        r = sqrt(np.sum((self.x-c)**2))
        n = (c-self.x)/r
        if self.force_law == 'gravitation':
            f = Planet.g*n/r**2
        elif self.force_law == 'rubber':
            f = Planet.k*n*r
        a = f/self.m
        self.v += a * Planet.dt
        self.x += self.v * Planet.dt
        self.patch.center = self.x


class World(object):
    
    def __init__(self):
        self.fig=plt.figure()
        self.ax=plt.axes()
        self.ax.set_xlim(-3,3)
        self.ax.set_ylim(-2,2)
        self.inhabitants=[]
    
    def add_inhabitants(self,new):
        if type(new) == list:
            self.inhabitants += new       # making the method robust, now you can dump several planets at a time
        else:
            self.inhabitants.append(new)  # accepting a single planet

    def draw(self):
        for thing in self.inhabitants:
            self.ax.add_patch(thing.patch)

    def blit_init(self):
        for thing in self.inhabitants:
            thing.patch.center = 42., 0.
        return [thing.patch for thing in self.inhabitants]

    def one_step(self,dummyarg):
        for thing in self.inhabitants:
            thing.one_step()
            thing.update_patch()
        return [thing.patch for thing in self.inhabitants]

w = World()
s = Sun([0,0],0.2)
s.initialize_patch()
w.add_inhabitants(s)

p1 = Planet(0.08,'k','grey')
p2 = Planet(0.2,'b','c')
p3 = Planet(0.3,'g','y')

p1.set_velocity([2.2,0.])
p2.set_velocity([1.6,0.])
p3.set_velocity([1.,0.3])

for p in [p1,p2,p3]:
    p.set_attractor(s)
    #p.force_law='rubber'
    p.initialize_patch()
    w.add_inhabitants(p)

w.draw()

ani = animation.FuncAnimation(w.fig, w.one_step, init_func=w.blit_init,
    interval=25, blit=True)
plt.show()


"""
Challenge A:
The sun does nothing, thats too boring. Modify its method one_step() so it
changes its colour, grows and shrinks, or starts to wander around in the
universe. You could make it sensitive to the arrow keys.

Challenge B:
Make a new class and name e.g. BoostPlanet. Let it behave the same way as a
planet, except that you can continuously boost or slow its tangential speed
while some keys are pressed. Try orbit-matching. Make it a game where you need
to match orbit with three planets one after the other in the shortest time
possible.

Challenge C:
Create an autopilot functionality for the BoostPlanet bringing it back to a
perfectly round home orbit ... but of course only using the tangentially acting
booster rocket engines!

Challenge D:
How could we add the Runge-Kutta time integration?
a) just rewrite Planet.one_step() ... but then switching is not possible
b) let one_step() begin like
   if self.useRK==True do this else do that
c) make a subclass of Planet where one_step() looks different, call it e.g.
   RK4Planet
d) write several external functions
    def propagate_simple(thing):
        ... doing stuff ...
    def propagate_RK(thing):
        ... doing stuff ...
   in the main program there is
    for p in planets: p.propagator=propagate_RK
   to connect the planet instances with one of the propagator functions, or
    p1.propagator=propagate_simple
    p2.propagator=propagate_RK
   and finally in Planet.one_step() the propagator is called
    self.propagator(self)
e) more ideas?
What are the advantages and disadvantages?

"""


"""
How to make a Matplotlib animation sensitive to keys:
http://matplotlib.org/examples/event_handling/keypress_demo.html
"""



