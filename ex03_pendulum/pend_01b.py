#! /usr/bin/env python
"""
same spring-mass system, but with an animated matplotlib plot
"""
import matplotlib.pyplot as plt
from matplotlib import patches, animation

m = 1.     # the mass
k = 1.     # the spring constant
x = 1.     # the initial displacement
t = 0.     # start time
dt = 0.2  # the time step
N = 100    # how many steps to calculate
x_old = 1. # the position during the last time step

fig =plt.figure()
ax=plt.axes()
circ = patches.Circle( (0., 0.), 0.2, fc='cyan',ec='blue') # fc and ec are facecolor and edgecolor
ax.add_patch(circ)
plt.xlim(-3,3)
plt.ylim(-2,2)
plt.axhline(y=0,color='grey')
plt.axvline(x=0,color='grey')

# adding a rectangle to symbolise the force
rect = patches.Rectangle([0.,0.5],1.,0.3,ec='g',fc='y')
ax.add_patch(rect)

def one_step(dummyarg):
    global t,x,x_old  # so these variables don't become local ones when redefined in here
    f = -k*x      # the force at the moment
    a = f/m       # acceleration
    v_old = (x-x_old)/dt  # measured current speed
    v = v_old + a*dt      # new speed modified by accceleration acting during the time of one time step
    x_old = x
    x = x + v*dt
    t = t+dt
    circ.center = x, 0.
    rect.set_width(f)
    return circ,rect

#Init only required for blitting to give a clean slate.
def init():
    circ.center = 42., 0.
    rect.set_width(0.)
    return circ,rect


ani = animation.FuncAnimation(fig, one_step, init_func=init,
    interval=25, blit=True)
plt.show()

"""
Challenge A:
Give the mass another vertical degree of freedom and a corresponding spring
force. What movement patterns are possible?

Challenge B:
Learning from the matplotlib animation examples (http://matplotlib.org/ and
then go to examples), can you make the mass draw a line along its track?

Challenge C:
Draw a nice spiralling spring connecting the mass with the left plot rim that
gets sqeezed and stretched.

Challenge D:
How about the spring connecting two freely moving masses? How do you want to
treat the case when a mass hits the plot frame? How about a rubber band instead
of a spring?

Challenge E:
How about gravitation instead of springs or rubber bands?

Challenge F:
Try out looking_glass.py in the matplotlib animation examples. It shows you
that you can register mouse clicks and check whether they happen to be inside
a circle patch. So it should in principle be possible to add fixed circles
to our plot which serve as buttons, and when you click, an action could follow,
like e.g. the mass getting an additional kick (added velocity) from the left or
right. Can you make that happen (doesn't matter whether using classes or
not)?
"""

