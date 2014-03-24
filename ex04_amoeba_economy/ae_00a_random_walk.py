#! /usr/bin/env python
"""
Once we can create moving circles with pygame, we can use that to start working
on simulations of populations of moving and interacting little things.

Preliminaries, step A:
Let's create one moving dot doing a random walk and make sure it doesn't leave
the box.
"""
import numpy as np
from numpy import pi, exp, sin, cos, sqrt
from numpy import array, asfarray, zeros, zeros_like
from numpy.random import rand
import pygame as pg

class Amoeb(object):

    def __init__(self,position,radius):
        self.x=asfarray(position)
        self.r=0.04 # scaling factor for random walk
        self.radius=radius
        self.color=(255,200,100)
        self.world=None
    
    def set_position(self,newpos):
        self.x[:]=newpos
    
    def get_position(self):
        return self.x
    
    def one_step(self):
        step = self.r * (2*rand(2)-1)  # additional random change of position
        self.x += step
        distances = self.world.wall_distances(self.x)
        # now checking whether any of the distances is negative, which is a
        # sure sign of having breached the boundary
        # if that's the case then we let the wall act as a sort of mirror and
        # the latest step is being bent inwards
        if distances['left'] < 0:
            self.x[0] -= 2*step[0]; print 'pushed back'
        if distances['right'] < 0:
            self.x[0] -= 2*step[0]; print 'pushed back'
        if distances['top'] < 0:
            self.x[1] -= 2*step[1]; print 'pushed back'
        if distances['bottom'] < 0:
            self.x[1] -= 2*step[1]; print 'pushed back'

    def show_up(self):
        pg.draw.circle(self.world.canvas, self.color, self.world.to_canvas_coords(self.x),
                       int(self.radius*100))

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

    def wall_distances(self,pos):
        x,y = self.to_canvas_coords(pos)
        answer={}
        answer['left']   = 0.01*x
        answer['right']  = 0.01*(self.ww-x)
        answer['top']    = 0.01*y
        answer['bottom'] = 0.01*(self.wh-y)
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
dot = Amoeb([0,0],0.14)
w.add_inhabitants(dot)

stop_flag = False
while not stop_flag:
    stop_flag = w.one_step()
