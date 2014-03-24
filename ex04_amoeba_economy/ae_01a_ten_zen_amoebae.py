#! /usr/bin/env python
"""
Once we can create moving circles with pygame, we can use that to start working
on simulations of populations of moving and interacting little things.

step A:
amoeba life
"""
import numpy as np
from numpy import pi, exp, sin, cos, sqrt
from numpy import array, asfarray, zeros, zeros_like
from numpy.random import rand, randn
import pygame as pg
from matplotlib import cm

def bounce_force(d,scaling,shift=0.):
    """The force law for repulsion from the domain wall, is implemented as a
    one-dimensional function only depending on the distance d from the wall"""
    d-=shift
    d*=scaling
    if d > 1:
        f = 0.
    elif d < 0:
        f = 10 * exp(-d) / scaling
    else:
        f = cos(0.5*pi*d) * exp(-d) / scaling
    return f

def color_mpl2pg(c):
    """matplotlib works with rgba tuples where each value is in [0,1], but
    pygame want's rgb tuples with the values being integers in [0,255]"""
    return tuple([int(255*val) for val in c[:3]])

class Amoeb(object):

    def __init__(self,position,radius):
        self.x=asfarray(position)
        self.v=zeros(2,dtype=float)
        self.f=zeros(2,dtype=float)
        self.m=1.
        self.dt=0.03
        self.damp=0.999
        self.r=0.05 # scaling factor for random walk
        self.direc=2*pi*rand() # wants to move in that direction
        self.radius=radius
        self.color=(120,120,255)
        self.world=None
    
    def set_position(self,newpos):
        self.x[:]=newpos
    
    def get_position(self):
        return self.x
    
    def one_step(self):
        self.v *= self.damp               # drag
        self.f[:]=0                       # reset force
        self.amoeba_drive()               # adding a force contribution
        self.wall_repulsion()             # adding a force contribution
        a = self.f/self.m                 # computing acceleration
        self.v += a * self.dt             # acceleration due to forces
        self.x += self.v * self.dt        # one step forward

    def pondering_about_direction(self):
        self.direc += 0.3*randn()
        if self.direc >= 2*pi:
            self.direc -=2*pi
        if self.direc < 0:
            self.direc -=2*pi

    def amoeba_drive(self):
        self.pondering_about_direction()
        self.f += 0.01 * rand() * array([cos(self.direc),sin(self.direc)])
    
    def wall_repulsion(self):
        dlim=0.2 # distance limit below which wall repulsion kicks in
        strength=0.001
        distances = self.world.wall_distances(self.x)
        if distances['left'] < dlim:
            self.f[0] += strength*bounce_force(distances['left'],dlim,dlim)
        if distances['right'] < dlim:
            self.f[0] -= strength*bounce_force(distances['right'],dlim,dlim)
        if distances['top'] < dlim:
            self.f[1] -= strength*bounce_force(distances['top'],dlim,dlim)
        if distances['bottom'] < dlim:
            self.f[1] += strength*bounce_force(distances['bottom'],dlim,dlim)
    
    def show_up(self):
        pg.draw.circle(self.world.canvas, self.color, self.world.to_canvas_coords(self.x),
                       int(self.radius*self.world.npix))

class World(object):
    
    def __init__(self):
        pg.init()
        self.BG_colour = (0,0,0)
        self.ww = 480   # window width
        self.wh = 360   # window height
        self.ox = self.ww/2 # x-coordinate of origin (of ohysics coordinate system inside canvas coordinate system)
        self.oy = self.wh/2 # y-coordinate of origin (of ohysics coordinate system inside canvas coordinate system)
        self.npix = 100 # number of pixels in one unit of the coordinate system experienced by the inhabitants
        self.canvas = pg.display.set_mode((self.ww,self.wh))
        self.canvas.fill(self.BG_colour)
        self.inhabitants=[]
        self.events=None

    def to_canvas_coords(self,vec):
        x,y = vec
        canvx = self.ox + int(self.npix*x)
        canvy = self.oy - int(self.npix*y) # why the minus sign? --> in the pygame canvas the origin is in the upper left corner
        return canvx,canvy

    def wall_distances(self,pos,canvas_coords=False):
        x,y = self.to_canvas_coords(pos)
        answer={}
        answer['left']   = x
        answer['right']  = self.ww-x
        answer['top']    = y
        answer['bottom'] = self.wh-y
        if not canvas_coords:
            for key in answer:
                answer[key]/=float(self.npix)
        return answer
    
    def add_inhabitants(self,new):
        if type(new) == list:
            for candidate in new:
                candidate.world=self
            self.inhabitants += new       # making the method robust, now you can dump several planets at a time
        else:
            self.inhabitants.append(new)  # accepting a single planet
            new.world=self

    def draw_inhabitants(self):
        for thing in self.inhabitants:
            thing.show_up()
    
    def one_step(self):
        stop = False
        self.events = pg.event.get()
        for event in self.events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                stop = True
        for thing in self.inhabitants:
            thing.one_step()
        self.canvas.fill(self.BG_colour)
        self.draw_inhabitants()
        pg.display.flip()
        return stop
    
w = World()

for i in xrange(10):
    dot = Amoeb(2*rand(2)-1,0.2*rand())
    dot.color = color_mpl2pg(cm.summer(rand()))  # find other colormaps here: http://matplotlib.org/examples/color/colormaps_reference.html
    w.add_inhabitants(dot)

stop_flag = False
while not stop_flag:
    stop_flag = w.one_step()
