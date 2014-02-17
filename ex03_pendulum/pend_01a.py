#! /usr/bin/env python
"""
We want to compute the time history of a spring-mass system time step by time
step.

We assume a linear spring, that means if you pull twice as far, you feel the
doubled force. Expressing thewhole thing in mathematical terms, we say the
f(x) = -k*x
where x is the shift of the loose end of the spring and k is the spring
stiffness. Why the minus sign? If you pull the loose spring end to the right,
it wants to go back to the left.
"""
import matplotlib.pyplot as plt

m = 1.     # the mass
k = 1.     # the spring constant
x = 1.     # the initial displacement
t = 0.     # start time
dt = 0.2  # the time step
N = 100    # how many steps to calculate
x_old = 1. # the position during the last time step

tdata=[t]  # an (almost) empty list for storing the time history
xdata=[x]  # an (almost) empty list for storing the displacement history
fdata=[0.] # an (almost) empty list for storing the force history

for i in xrange(N):
    f = -k*x      # the force at the moment
    a = f/m       # acceleration
    v_old = (x-x_old)/dt  # measured current speed
    v = v_old + a*dt      # new speed modified by accceleration acting during the time of one time step
    x_old = x
    x = x + v*dt
    t = t+dt
    
    tdata.append(t)
    xdata.append(x)
    fdata.append(f)

plt.fill_between(tdata,fdata,y2=0,color='g',alpha=0.5)
plt.plot(tdata,fdata,'g-',lw=2,label='force $f$')
plt.plot(tdata,xdata,'bo-',lw=2,label='position $x$')
plt.ylim(-2,2)
plt.legend()
plt.xlabel('time $t$')
plt.show()

"""
Feel free to modify the physical constants the time step, etc..
You can also modify the spring so it has different stiffnesses in the two
directions or make it nonlinear or both.
"""

