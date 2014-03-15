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
import pygame as pg


class Sun(object):

    def __init__(self,position,radius):
        self.x=asfarray(position)
        self.radius=radius
        self.color=(255,200,100)
    
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
    dt=0.003
    def __init__(self,mass):
        self.m=mass
        self.radius = int(100*0.1*mass**0.33) # multiplication by 100 because of the 100 pixels per physical length unit
        self.x=array([0.,1.])
        self.v=array([0.,0.])
        self.color=(120,120,255)
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

class World(object):
    
    def __init__(self):
        pg.init()
        self.BG_colour = (0,0,0)
        self.ww = 480   # window width
        self.wh = 360   # window height
        self.ox = self.ww/2 # x-coordinate of origin (of ohysics coordinate system inside canvas coordinate system)
        self.oy = self.wh/2 # y-coordinate of origin (of ohysics coordinate system inside canvas coordinate system)
        self.canvas = pg.display.set_mode((self.ww,self.wh))
        self.canvas.fill(self.BG_colour)
        self.inhabitants=[]

    def to_canvas_coords(self,vec):
        x,y = vec
        canvx = self.ox + int(100*x) # one unit in the physics coordinate system is 100 pixels
        canvy = self.oy - int(100*y) # why the minus sign? --> in the pygame canvas the origin is in the upper left corner
        return canvx,canvy
    
    def add_inhabitants(self,new):
        if type(new) == list:
            self.inhabitants += new       # making the method robust, now you can dump several planets at a time
        else:
            self.inhabitants.append(new)  # accepting a single planet

    def draw_inhabitants(self):
        for thing in self.inhabitants:
            newpos=thing.get_position()
            pg.draw.circle(self.canvas, thing.color, self.to_canvas_coords(newpos), thing.radius)

    def one_step(self):
        stop = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                stop = True
        for thing in self.inhabitants:
            thing.one_step()
        self.canvas.fill(self.BG_colour)
        self.draw_inhabitants()
        pg.display.flip()
        return stop
    
w = World()
s = Sun([0,0],8)
w.add_inhabitants(s)

p1 = Planet(0.08)
p2 = Planet(0.2)
p3 = Planet(0.3)

p1.set_velocity([2.2,0.])
p2.set_velocity([1.6,0.])
p3.set_velocity([1.,0.3])

for p in [p1,p2,p3]:
    p.set_attractor(s)
    #p.force_law='rubber'
    w.add_inhabitants(p)

stop_flag = False
while not stop_flag:

    stop_flag = w.one_step()
    print stop_flag
