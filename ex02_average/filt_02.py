#!/usr/bin/env python
"""
the rolling average is in fact a low-pass filter
"""
from numpy import array, arange, zeros, pi, sin, mean, where
from numpy.random import rand, randint
import matplotlib.pyplot as plt

def roll_avg(data,n):
    """
    This is a new thing: a function that does the rolling average on a signal
    of whatever length and averaging over as many n values as desired
    """
    m=len(data)
    out=zeros(m)
    for i in xrange(n,m):
        out[i] = mean(data[i-n:i])
    return out

N = 400
t = 6*pi*arange(N,dtype=float)/N # the time scale
w = 1.                           # the frequency
s = sin(w*t)                     # a sine signal, it spans the interval [-1,+1]
noise = 2*rand(N) - 1            # random values also covering [-1,+1]
snr = 0.2                        # the signal-to-noise ratio
y = snr*s + (1-snr)*noise        # the final signal for testing the filter
#y = where(s>0, 1, -1)            # an alternative signal

## and some more degradation of the signal
## how can the filter be modified to make the filtered signal look smoother?
#outliers = randint(N,size=5)
#for idx in outliers:
#    y[idx]=5


filtered = roll_avg(y,60) # try to find a value n which yields a nice filtered signal

plt.plot(t,y,'k-')
plt.plot(t,filtered,'ro-',lw=2)
plt.ylim(-1.2,1.2)
plt.show()

"""
challenge A:
try to find a good n for the roll_avg() filter

challenge B:
invent three more testing signals and check the filter on them

challenge C:
how can the filter be made better so the signal gets still smoother
(try the initial setting except snr=0.5 and the outliers turned on, that
will show some interesting kinks)

challenge D:
make a useful function which produces a test signal and which can be
called e.g. like this:
y = testfunc_producer(length, parameter1, parameter2)
"""


