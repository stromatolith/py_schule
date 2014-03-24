#! /usr/bin/env python
"""
Once we can create moving circles with pygame, we can use that to start working
on simulations of populations of moving and interacting little things.

Preliminaries, step B:
A different kind of enforcing the domain boundaries: smooth bouncing back. But
first we need inertia. Move the ball with the arrow keys.
"""
import numpy as np
from numpy import pi, exp, sin, cos, sqrt
from numpy import array, asfarray, zeros, zeros_like
from numpy.random import rand
import pygame as pg

class Amoeb(object):

    def __init__(self,position,radius):
        self.x=asfarray(position)
        self.v=zeros(2,dtype=float)
        self.f=zeros(2,dtype=float)
        self.m=1.
        self.dt=0.03
        self.damp=0.999
        self.r=0.0 # scaling factor for random walk
        self.radius=radius
        self.color=(120,120,255)
        self.world=None
        self.active_rocket_engines={'left':False,'right':False,'top':False,'bottom':False}
    
    def set_position(self,newpos):
        self.x[:]=newpos
    
    def get_position(self):
        return self.x
    
    def one_step(self):
        self.v *= self.damp               # drag
        self.f[:]=0                       # reset force
        self.rocket_propulsion()          # adding a force contribution
        a = self.f/self.m                 # computing acceleration
        self.v += a * self.dt             # acceleration due to forces
        self.x += self.v * self.dt        # one step forward
        self.x += self.r * (2*rand(2)-1)  # additional random change of position

    def rocket_propulsion(self):
        strength=0.01
        for event in self.world.events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.active_rocket_engines['right'] = True
                if event.key == pg.K_RIGHT:
                    self.active_rocket_engines['left'] = True
                if event.key == pg.K_UP:
                    self.active_rocket_engines['bottom'] = True
                if event.key == pg.K_DOWN:
                    self.active_rocket_engines['top'] = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    self.active_rocket_engines['right'] = False
                if event.key == pg.K_RIGHT:
                    self.active_rocket_engines['left'] = False
                if event.key == pg.K_UP:
                    self.active_rocket_engines['bottom'] = False
                if event.key == pg.K_DOWN:
                    self.active_rocket_engines['top'] = False
        if self.active_rocket_engines['left'] == True:
            self.f[0] += strength
        if self.active_rocket_engines['right'] == True:
            self.f[0] -= strength
        if self.active_rocket_engines['top'] == True:
            self.f[1] -= strength
        if self.active_rocket_engines['bottom'] == True:
            self.f[1] += strength
    
    def show_up(self):
        pg.draw.circle(self.world.canvas, self.color, self.world.to_canvas_coords(self.x),
                       int(self.radius*self.world.npix))
        x,r = self.x,self.radius
        e1,e2 = array([1.,0.]),array([0.,1.])
        if self.active_rocket_engines['left'] == True:
            p1 = self.world.to_canvas_coords(x-0.8*r*e1)
            p2 = self.world.to_canvas_coords(x-1.5*r*e1 + 0.3*r*e2)
            p3 = self.world.to_canvas_coords(x-1.5*r*e1 - 0.3*r*e2)
            pg.draw.polygon(self.world.canvas,(255,80,20),[p1,p2,p3])
        if self.active_rocket_engines['right'] == True:
            p1 = self.world.to_canvas_coords(x+0.8*r*e1)
            p2 = self.world.to_canvas_coords(x+1.5*r*e1 + 0.3*r*e2)
            p3 = self.world.to_canvas_coords(x+1.5*r*e1 - 0.3*r*e2)
            pg.draw.polygon(self.world.canvas,(255,80,20),[p1,p2,p3])
        if self.active_rocket_engines['top'] == True:
            p1 = self.world.to_canvas_coords(x+0.8*r*e2)
            p2 = self.world.to_canvas_coords(x+1.5*r*e2 + 0.3*r*e1)
            p3 = self.world.to_canvas_coords(x+1.5*r*e2 - 0.3*r*e1)
            pg.draw.polygon(self.world.canvas,(255,80,20),[p1,p2,p3])
        if self.active_rocket_engines['bottom'] == True:
            p1 = self.world.to_canvas_coords(x-0.8*r*e2)
            p2 = self.world.to_canvas_coords(x-1.5*r*e2 + 0.3*r*e1)
            p3 = self.world.to_canvas_coords(x-1.5*r*e2 - 0.3*r*e1)
            pg.draw.polygon(self.world.canvas,(255,80,20),[p1,p2,p3])

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
    
    def boundary_teleport(self,inhab):
        distances = self.wall_distances(inhab.x,canvas_coords=True)
        if distances['left'] < 0:
                inhab.x[0] += self.ww/float(self.npix)
        elif distances['right'] < 0:
                inhab.x[0] -= self.ww/float(self.npix)
        if distances['top'] < 0:
                inhab.x[1] -= self.wh/float(self.npix)
        elif distances['bottom'] < 0:
                inhab.x[1] += self.wh/float(self.npix)

    def one_step(self):
        stop = False
        self.events = pg.event.get()
        for event in self.events:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                stop = True
        for thing in self.inhabitants:
            thing.one_step()
            self.boundary_teleport(thing)
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
