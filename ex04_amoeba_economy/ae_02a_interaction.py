#! /usr/bin/env python
"""
Once we can create moving circles with pygame, we can use that to start working
on simulations of populations of moving and interacting little things.

Now finally, something going on in the simulation, predator amoebae strolling
around and eating the green little amoebae.
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
        self.dt=0.06
        self.damp=0.999
        self.r=0.05 # scaling factor for random walk
        self.direc=2*pi*rand() # wants to move in that direction
        self.wankelmut=0.3
        self.drive=0.02
        self.radius=radius
        self.color=color_mpl2pg(cm.cool(0.5*rand()))
        self.color2=color_mpl2pg(cm.cool(0.8+0.2*rand()))
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
        self.direc += self.wankelmut*randn()
        if self.direc >= 2*pi:
            self.direc -=2*pi
        if self.direc < 0:
            self.direc -=2*pi

    def amoeba_drive(self):
        self.pondering_about_direction()
        self.f += self.drive * rand() * array([cos(self.direc),sin(self.direc)])
    
    def wall_repulsion(self):
        dlim=0.2 # distance limit below which wall repulsion kicks in
        strength=0.01
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

class Food(Amoeb):

    def __init__(self):
        pos = [4.8*rand()-2.4, 3.6*rand()-1.8]
        self.iniradius=0.03
        self.endradius=0.13
        Amoeb.__init__(self,pos,self.iniradius)
        self.wankelmut=0.1
        self.drive=0.01
        self.color=[0,0,0]
        self.update_color()
        self.counter=0

    def ageing(self):
        self.counter+=1
        if self.counter == 200:
            self.radius += 0.02
            if self.radius > self.endradius:
                self.radius = self.endradius
            self.counter = 0

    def update_color(self):
        cparam = (self.radius-self.iniradius) / (self.endradius-self.iniradius)
        self.color[:]=color_mpl2pg(cm.YlGn(cparam))

    def one_step(self):
        Amoeb.one_step(self)
        self.ageing()
        self.update_color()

class Predator(Amoeb):

    def __init__(self):
        pos = [4.8*rand()-2.4, 3.6*rand()-1.8]
        self.iniradius=0.1
        self.endradius=0.3
        Amoeb.__init__(self,pos,self.iniradius)
        self.wankelmut=0.3
        self.drive=0.06
        self.color=[0,0,0]
        self.update_color()
        self.counter=0
        self.update_mass()

    def update_color(self):
        cparam = (self.radius-self.iniradius) / (self.endradius-self.iniradius)
        self.color[:]=color_mpl2pg(cm.Oranges(cparam))

    def update_mass(self):
        self.m = 30*pi*self.radius**2

    def one_step(self):
        self.update_mass()
        Amoeb.one_step(self)
        encounters = self.world.am_i_alone(self)
        for thing in encounters:
            if isinstance(thing,Food):
                self.eat(thing)
        self.update_color()

    def eat(self,thing):
        area = pi*thing.radius**2
        delta_r = area / 2*pi*self.radius
        self.radius += delta_r   # added area is roughly circumference times delta_r
        if self.radius > self.endradius:
            self.radius = self.endradius
        self.world.food_eaten(thing)

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
    
    def am_i_alone(self,inhab):
        answer = []
        for thing in self.inhabitants:
            if not thing is inhab:
                dist = sqrt(np.sum((thing.x-inhab.x)**2))
                if dist <= thing.radius+inhab.radius:
                    answer.append(thing)
        return answer
    
    def one_step(self):
        stop = False
        self.events = pg.event.get()
        for event in self.events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                stop = True
        self.grow_food()
        for thing in self.inhabitants:
            thing.one_step()
        self.canvas.fill(self.BG_colour)
        self.draw_inhabitants()
        pg.display.flip()
        return stop
    
    def grow_food(self):
        if rand() < 0.05:
            self.add_inhabitants(Food())
    
    def food_eaten(self,inhab):
        idx = self.get_index(inhab)
        self.inhabitants.pop(idx)
        del inhab

    def get_index(self,inhab):
        for i,thing in enumerate(self.inhabitants):
            if thing is inhab:
                return i
        
    
w = World()

for i in xrange(10):
    dot = Predator()
    w.add_inhabitants(dot)

stop_flag = False
while not stop_flag:
    stop_flag = w.one_step()

"""
You see the simulation slows down the more balls are flying around. The main
problem is the collision check, the computation time for that grows exponen-
tially with the number of balls. Find and discuss ideas to do it more
efficiently, and if you want, start coding and experimenting.
"""


