#! /usr/bin/env python
"""
talking about more or less precise time stepping techniques and force laws ...

... if we want to make some comparisons, these are some options
a) comparing the different programs we have dealt with so far
   danger: overlooking other differences
b) switching code blocks on and off, e.g.
    #f = g*n/r**2      # gravitation
    f = g*n*r          # rubber band
    problem: inconvenient, code looks dirty and is not nice to read
c) setting up switches
d) class definitions where the switches are internals of an object

here let's go along (c)

definitions:
having a function f(x,t) we call df/dx fprime and df/dt fdot. So here we are
talking about trajectories in space and call them x(t), then the speed is
v = dx/dt = xdot, and the acceleration is a = xdotdot.

For using the general-purpose Runge-Kutta steps below, the 2nd order ODE
has to be rewritten as 2 ODEs of 1st order:
f = ma = -kx --> f/m = a = -k/m * x
gets recast into thes two equations with two variables v(t) and x(t)
vdot = -kx/m
xdot = v

This doesn't work yet, still have to find out why. Sorry.
"""
import numpy as np
from numpy import sqrt
from numpy import array, hstack
import matplotlib.pyplot as plt
from matplotlib import patches, animation

def RK4step(tn,fn,fdot,dt):
    """
    Calculate t and f(t) for the next time step; availbale for the task are the
    old values tn and fn, the size of the time step dt (sorry, I find writing
    delta_t is too long), and the derivative fdot(). fdot(t,f) must be a callable
    function.
    for background information see here:
    http://de.wikipedia.org/wiki/Runge-Kutta-Verfahren
    http://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods
    http://rosettacode.org/wiki/Runge-Kutta_method
    """
    df1 = dt * fdot(tn,fn)
    df2 = dt * fdot(tn+0.5*dt,fn+0.5*df1)
    df3 = dt * fdot(tn+0.5*dt,fn+0.5*df2)
    df4 = dt * fdot(tn+dt,fn+df3)
    tnext = tn + dt
    fnext = fn + 1./6. * (df1+2*df2+2*df3+df4)
    return tnext,fnext

def RK1step(tn,fn,fdot,dt):
    """
    first order Runge-Kutta is same as Euler forward, see here:
    http://de.wikipedia.org/wiki/Runge-Kutta-Verfahren
    http://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods
    """
    #print 'fn: ',fn
    df1 = dt * fdot(tn,fn); #print 'df1: ',df1
    tnext = tn + dt
    fnext = fn + df1
    return tnext,fnext

def aRK4step(tn,fn,fdot,dt):
    """alternative formulae"""
    k1 = fdot(tn,fn)
    k2 = fdot(tn+0.5*dt,fn+dt*0.5*k1)
    k3 = fdot(tn+0.5*dt,fn+dt*0.5*k2)
    k4 = fdot(tn+dt,fn+dt*k3)
    tnext = tn + dt
    fnext = fn + dt/6. * (k1+2*k2+2*k3+k4)
    return tnext,fnext
        
def aRK1step(tn,fn,fdot,dt):
    """alternative formulae"""
    k1 = fdot(tn,fn)
    tnext = tn + dt
    fnext = fn + dt*k1
    return tnext,fnext
        

m = 1.     # the mass
k = 1.     # the spring constant
g = 1.     # the gravitation constant
x = array([0.,1.])     # the initial position in 2D space
c = array([0.,0.])     # the center, the sun, the location where the force is pointing at
t = 0.     # start time
dt = 0.05  # the time step, try out 0.1, 0.2, 0.005
N = 100    # how many steps to calculate
v = array([0.6,0.])     # velocity

force_law = 'gravitation' # implemented: 'gravitation' and 'rubber'
stepping = 'new_speed'        # implemented: 'new_speed', 'Euler' and 'RK'
RK_order = 1

blit_interval = 25 # time in milliseconds until screen is refreshed

xdata = []
ydata = []

fig =plt.figure()
ax=plt.axes()
track, = ax.plot(xdata,ydata,'g-')
circ = patches.Circle( (0., 0.), 0.08, fc='cyan',ec='blue') # fc and ec are facecolor and edgecolor
ax.add_patch(circ)
sun = patches.Circle( (0., 0.), 0.12, fc='yellow',ec='red') # fc and ec are facecolor and edgecolor
ax.add_patch(sun)
plt.xlim(-3,3)
plt.ylim(-2,2)
plt.axhline(y=0,color='grey')
plt.axvline(x=0,color='grey')

def one_step(dummyarg):
    global t,x,v  # so these variables don't become local ones when redefined in here
    r = sqrt(x[0]**2+x[1]**2)
    n = (c-x)/r   # vector of unit length pointing at c
    if force_law == 'gravitation':
        f = g*n/r**2      # the force at the moment
    elif force_law == 'rubber':
        f = k*n*r      # the force at the moment
    a = f/m       # acceleration
    v = v + a*dt      # new speed modified by accceleration acting during the time of one time step
    x = x + v*dt      # using the newly calculated speed
    t = t+dt
    circ.center = x[0], x[1]
    xdata.append(x[0])
    ydata.append(x[1])
    track.set_data(xdata,ydata)
    return circ,track

def one_step_Euler(dummyarg):
    global t,x,v  # so these variables don't become local ones when redefined in here
    r = sqrt(x[0]**2+x[1]**2)
    n = (c-x)/r   # vector of unit length pointing at c
    if force_law == 'gravitation':
        f = g*n/r**2      # the force at the moment
    elif force_law == 'rubber':
        f = k*n*r      # the force at the moment
    a = f/m       # acceleration
    x = x + v*dt      # using the old speed
    v = v + a*dt      # new speed modified by accceleration acting during the time of one time step
    t = t+dt
    circ.center = x[0], x[1]
    xdata.append(x[0])
    ydata.append(x[1])
    track.set_data(xdata,ydata)
    return circ,track

def qdot_rubber(t,q):
    xx = array(q[:2])
    vv = array(q[2:])
    displacement = xx-c
    f = -k*displacement
    vdot = f/m # acceleration a = f/m
    xdot = vv
    return array([xdot[0],xdot[1],vdot[0],vdot[1]])

def qdot_grav(t,q):
    xx = array(q[:2])
    vv = array(q[2:])
    r = sqrt(np.sum((c-xx)**2))
    n = (c-xx)/r # normal vector pointing towards the sun
    f = g*n/r**2 # acceleration a = f/m
    vdot = f/m # acceleration a = f/m
    xdot = vv
    return hstack([xdot,vdot])   #array([xdot[0],xdot[1],vdot[0],vdot[1]])

#print 'v: ',v
#i=0
def one_step_RK(dummyarg):
    global t,x,v,i
    #print 'v2: ',v
    q = [x[0],x[1],v[0],v[1]]
    #print 'q: ',q
    #i+=1
    #print 'iteration ',i
    if force_law == 'rubber':
        if (stepping == 'RK') and (RK_order == 1):
            t,q = aRK1step(t,q,qdot_rubber,dt)
        elif (stepping == 'RK') and (RK_order == 4):
            t,q = aRK4step(t,q,qdot_rubber,dt)
    elif force_law == 'gravitation':
        if (stepping == 'RK') and (RK_order == 1):
            t,q = aRK1step(t,q,qdot_grav,dt)
        elif (stepping == 'RK') and (RK_order == 4):
            t,q = aRK4step(t,q,qdot_grav,dt)
    x[:] = q[:2]
    v[:] = q[2:]
    #print 'v3: ',v
    circ.center = x[0], x[1]
    xdata.append(x[0])
    ydata.append(x[1])
    track.set_data(xdata,ydata)
    return circ,track
    

#Init only required for blitting to give a clean slate.
def init():
    circ.center = 42., 0. # plotting it somewhere far away so initial canvas is clean
    track.set_xdata([])
    track.set_ydata([])
    return circ,track

if stepping == 'new_speed':
    ani = animation.FuncAnimation(fig, one_step, init_func=init,
        interval=blit_interval, blit=True)
elif stepping == 'Euler':
    ani = animation.FuncAnimation(fig, one_step_Euler, init_func=init,
        interval=blit_interval, blit=True)
elif stepping == 'RK':
    ani = animation.FuncAnimation(fig, one_step_RK, init_func=init,
        interval=blit_interval, blit=True)
plt.show()

"""
Challenge A:
As already suggested, one could add more planets or introduce spaceships, but
better don't do it with this code here. Look at the next one where this is so
much easier.

3 things to take away from looking at this code:

a) When simulating physics, you have to think about numerics. Performance and
   realism have to be bought by paying with computation power and brains. For
   a computer game the simple and unrealistic physics model may be just as fun
   and if something diverges an artificial damping term may do the job. In
   science it is different.

b) Standardisation makes switching easy, the example here are the Runge-Kutta
   functions which have very different capabilities, but behave in the same
   way, seen from the calling entity.

c) Beside point (b) the rest of the code is rather a mess. One messy aspect: it
   is easy to take away the RK functions and use them somewhere else, but you
   can't do that with one_step(), qdot_rubber(), and the other similar
   functions, because they depend on all those global variables. These
   functions rely on their environment. If a friend gives you code like that,
   then you are annoyed that it takes so much time and effort to understand how
   all that environment works. Same if it was your own old code from last year.
   The other point is that if you add a new feature in one place of the code,
   then you might have to modify many if-else branching structures in many
   other places of the code. That's also more annoying than it needs to be.
   Solution: object-oriented programming: define classes of objects where the
   internal logic is consistent and intuitive and where there are low
   requirements for the external environment.
"""


