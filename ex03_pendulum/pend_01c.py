#! /usr/bin/env python
"""
the kick button suggested in challenge F
"""
import matplotlib.pyplot as plt
from matplotlib import patches, animation

m = 1.     # the mass
k = 1.     # the spring constant
x = 1.     # the initial displacement
t = 0.     # start time
dt = 0.2  # the time step
N = 100    # how many steps to calculate
v = 0.

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

button1 = patches.Circle( (-1.5, -1.5), 0.15, fc='red')
ax.add_patch(button1)


def one_step(dummyarg):
    global t,x,v  # so these variables don't become local ones when redefined in here
    f = -k*x      # the force at the moment
    a = f/m       # acceleration
    v = v + a*dt      # new speed modified by accceleration acting during the time of one time step
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

def onpress(event):
    global v
    if button1.contains(event)[0]:
        v=v+0.5

fig.canvas.mpl_connect('button_press_event', onpress)


ani = animation.FuncAnimation(fig, one_step, init_func=init,
    interval=25, blit=True)
plt.show()


"""
Challenge A:
Make it a game: the score is the amount of time (or kicks) you need to kick the
spring so far it reaches x=5 or something like that.

Challenge B:
Make the game more interesting and challenging. My first idea would be: the mass
gets a bonus velocity if you manage to click while it passes a coloured zone. 

Or let this be just an inspiration for a different game.

Something important to learn:
In comparison to the last version the variable v for the velocity had to be
made global. There are now two functions that need to modify it. Global
variables for various reasons are not a sign of good programming style. When
programs get a little larger it soon gets very cumbersome to make sure nothing
unintended happens when many functions modify one variable. This is one problem
that gets solved by using classes. All functions within a class can access a
common bowl of variables, and the functions in the class have systematically
ordered functions.... but you will see.
"""