#! /usr/bin/env python
"""
going from springs to gravitation --> planetary orbits
... but now in object-oriented style

doesn't yet work, but will soon
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
    g=1.
    k=1.
    dt=0.05
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
        self.force_law='gravitation'
    
    def set_attractor(self,target):
        self.attractor=target
        
    def set_velocity(self,v):
        self.v[:]=v
    
    def one_step(self):
        c = self.attractor.x
        r = sqrt(np.sum(self.x**2))
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
            self.ax.add_patch(thing)

    def blit_init(self):
        print 'hello1'
        for thing in self.inhabitants:
            thing.patch.center = 42., 0.
        print 'hello2'
        return [thing.patch for thing in self.inhabitants]

    def one_step(self,dummyarg):
        print 'hello3'
        for thing in self.inhabitants:
            thing.one_step()
            thing.update_patch()
        print 'hello4'
        return [thing.patch for thing in self.inhabitants]

w = World()
s = Sun([0,0],0.2)
s.initialize_patch()
w.add_inhabitants(s)

#p1 = Planet(0.05,'k','grey')
#p2 = Planet(0.1,'b','c')
#p3 = Planet(0.2,'g','y')
#
#p1.set_velocity([0.,1.2])
#p2.set_velocity([0.,0.7])
#p3.set_velocity([0.2,0.6])
#
#for p in [p1,p2,p3]:
#    p.set_attractor(s)
#    p.initialize_patch()
#    w.add_inhabitants(p)

ani = animation.FuncAnimation(w.fig, w.one_step, init_func=w.blit_init,
    interval=25, blit=True)
plt.show()


