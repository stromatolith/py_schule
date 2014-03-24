#! /usr/bin/env python
"""
Once we can create moving circles with pygame, we can use that to start working
on simulations of populations of moving and interacting little things.

Evolution: the predator amoebae reproduce inheriting and mutating their drive
variable, and when they encounter each other the faster one steals mass, and
when the speed difference is above a threshold, then the slower one gets killed.
"""
import numpy as np
from numpy import pi, exp, sin, cos, sqrt, mean, fabs
from numpy import array, asfarray, zeros, zeros_like
from numpy import dot
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
        self.iniradius=0.05
        self.endradius=0.15
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
        self.num=None            # identification number
        self.last_encounter=None # remember number of other amoeba met most recently 

    def update_color(self):
        cparam = (self.radius-self.iniradius) / (self.endradius-self.iniradius)
        self.color[:]=color_mpl2pg(cm.Oranges(cparam))

    def update_mass(self):
        self.m = 30*pi*self.radius**2

    def one_step(self):
        self.update_mass()
        self.eventually_divide()
        Amoeb.one_step(self)
        self.check_food()
        self.check_predator_collision()
        self.update_color()

    def check_food(self):
        encounters = self.world.am_i_alone(self,interest='Food')
        for thing in encounters:
            self.eat(thing)

    def check_predator_collision(self):
        encounters = self.world.am_i_alone(self,interest='Predator')
        for thing in encounters:
            if thing.num != self.last_encounter:
                self.gamble_with(thing)

    def eat(self,thing):
        area = pi*thing.radius**2
        delta_r = 5 * area / 2*pi*self.radius
        self.radius += delta_r   # added area is roughly circumference times delta_r
        if self.radius > self.endradius:
            self.radius = self.endradius
        self.world.report_death_of(thing)

    def eventually_divide(self):
        if self.radius > 0.5*self.endradius:
            P = 0.08 * (self.radius-0.5*self.endradius) / (self.endradius)
            #print 'P: ',P
            if rand() < P:
                #print 'division follows'
                self.divide()
    
    def divide(self):
        self.radius /= sqrt(2)
        new = Predator()
        new.radius=self.radius # with scalar numbers there is no memory reference issue
        r = randn(2) # a random vector to shift the new amoeba into a random direction
        new.x[:]=self.x + (self.radius+new.radius)*r/sqrt(np.sum(r**2))*1.1
        #new.v=self.v   # doesn't work, would only create a new reference to the same memory
        new.v[:]=self.v
        new.drive=self.drive # inherit behaviour gene
        if rand()<0.5:
            new.drive*=1.5   # mutate behaviour gene
        else:
            new.drive/=1.5   # mutate behaviour gene
        self.world.add_inhabitants(new)

    def gamble_with(self,other):
        ownspeed = sqrt(np.sum(self.v**2))
        otherspeed = sqrt(np.sum(other.v**2))
        collisionspeed = sqrt(np.sum((self.v-other.v)**2)); #print 'coll v: ',collisionspeed
        if collisionspeed > 0.25:
            # if collision speed above threshold, then with 50% probability
            # the slower one dies
            if rand() < 0.8:
                if ownspeed >= otherspeed:
                    self.world.report_death_of(other)
                    #print 'survival {} and death {}'.format(self.num,other.num)
                else:
                    self.world.report_death_of(self)
                    #print 'survival {} and death {}'.format(other.num,self.num)
        else:
            if ownspeed >= otherspeed:
                win = rand() < 0.7  # win=True with probability 70%
            else:
                win = rand() < 0.3  # win=True with probability 30%
            if win:
                self.radius *= 1.1
                other.radius /= 1.15
                #print 'winner {} and loser {}'.format(self.num,other.num)
            else:
                self.radius /= 1.15
                other.radius *= 1.1
                #print 'winner {} and loser {}'.format(other.num,self.num)
        self.last_encounter=other.num
        other.last_encounter=self.num
        self.collide_with(other)
    
    def collide_with(self,other):
        dvec=other.x-self.x         # vector from self to other
        d=sqrt(np.sum(dvec**2))     # scalar distance
        n=dvec/d                    # normal unit vector
        #meanv=0.5*(self.v+other.v)  # allow me to assume equal masses to simplify the collision physics
        meanv=(self.v*self.m+other.v*other.m)/(self.m+other.m)
        proj=dot(self.v-meanv,n)
        self.v-=2*proj*n
        proj=dot(other.v-meanv,n)
        other.v-=2*proj*n


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
        self.predators=[]
        self.foods=[]
        self.ic=0 # inhabitant counter
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
                self.inhabitants.append(candidate)
                self.ic+=1
                candidate.num=self.ic
                if isinstance(candidate,Food):
                    self.foods.append(new)
                elif isinstance(candidate,Predator):
                    self.predators.append(new)
        else:
            new.world=self
            self.inhabitants.append(new)
            self.ic+=1
            new.num=self.ic
            if isinstance(new,Food):
                self.foods.append(new)
            elif isinstance(new,Predator):
                self.predators.append(new)

    def draw_inhabitants(self):
        for thing in self.inhabitants:
            thing.show_up()
    
    def am_i_alone(self,inhab,interest=None):
        answer = []
        if interest==None:
            searchlist=self.inhabitants
        elif interest=='Food':
            searchlist=self.foods
        elif interest=='Predator':
            searchlist=self.predators
        else:
            raise ValueError('unknown interest keyword')
        for thing in searchlist:
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
        #print 'avg v: ',mean([fabs(thing.v) for thing in self.predators])
        return stop
    
    def grow_food(self):
        if rand() < 0.1:  #0.05:
            self.add_inhabitants(Food())
    
    def report_death_of(self,inhab):
        if isinstance(inhab,Food):
            idx = self.get_index(inhab,self.foods)#; print idx
            self.foods.pop(idx)
        elif isinstance(inhab,Predator):
            idx = self.get_index(inhab,self.predators)#; print idx
            self.predators.pop(idx)
        idx = self.get_index(inhab,self.inhabitants)#; print idx
        self.inhabitants.pop(idx)
        del inhab

    def get_index(self,inhab,thelist):
        for i,thing in enumerate(thelist):
            if thing is inhab:
                return i
        
    
w = World()

for i in xrange(10):
    p = Predator()
    w.add_inhabitants(p)

stop_flag = False
counter=0
while not stop_flag:
    stop_flag = w.one_step()
    counter+=1
    if counter%50 == 0:
        print 'mean value of drive gene: ',mean([p.drive for p in w.predators])

"""
faster predator amoebae should have higher survival probabilities, so
evolution should make them faster ... sometimes it takes a while to happen,
maybe because the initial gene pool is uniform, but that's easy to change, but
sometimes it also happens already in this setup, sometimes sooner, in other
runs later. And sometimes the whole thing crashes when too many amoebae
overlap. Until I find the time to make the simulation better, you'll have to ;)

One more thought: if an amoeba's desired direction has a low temporal
correlation with the velocity, then there is also no selection pressure on
the self.drive gene. (Then the amoeba wants to slow down as often as it wants
to accelerate.) This is an important background thought when looking at
the situation that some amoebae bounce back and forth from wall to wall
probably faster than the time constant of changes in the desired direction.
There are many screws to tweak to change that mischief.

Some statistics recording and plotting might also help in understanding what
goes on.
"""


