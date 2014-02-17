#! /usr/bin/env python
"""
going from springs to gravitation --> planetary orbits
"""
from numpy import sqrt
from numpy import array
import matplotlib.pyplot as plt
from matplotlib import patches, animation

m = 1.     # the mass
g = 1.     # the gravitation constant
x = array([0.,1.])     # the initial position in 2D space
c = array([0.,0.])     # the center, the sun, the location where the force is pointing at
t = 0.     # start time
dt = 0.05   # the time step, try out 0.1, 0.2, 0.005
N = 100    # how many steps to calculate
v = array([0.6,0.])     # velocity

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
    f = g*n/r**2      # the force at the moment
    a = f/m       # acceleration
    v = v + a*dt      # new speed modified by accceleration acting during the time of one time step
    x = x + v*dt
    t = t+dt
    circ.center = x[0], x[1]
    xdata.append(x[0])
    ydata.append(x[1])
    track.set_data(xdata,ydata)
    return circ,track

#Init only required for blitting to give a clean slate.
def init():
    circ.center = 42., 0.
    track.set_xdata([])
    track.set_ydata([])
    return circ,track


ani = animation.FuncAnimation(fig, one_step, init_func=init,
    interval=25, blit=True)
plt.show()


"""
Challenge A:
Try out different values for the time step dt. What's the problem? Try out
different initial position and speed vectors. Are there trajectories which are
more problematic than others? Go back to the spring, did we just not notice the
problem there or is there a fundamental difference? (You can also just modify
the force law in this program back to the rubber band law.)

Challenge B:
My two ideas if you want to make a game out of it: add a space ship that also
circulates the sun, but define two keys for acceleration and deceleration of
the tangential speed, the goal is to match orbit with the planet. If some of
your friends has ever played Orbiter or Kerbal Space program, then they will
have useful hints on how you can do that. The other idea would be to install
some good old rocket launchers at the bottom of the plot. What makes the games
more fun, correct or problematic physics?
"""