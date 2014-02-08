#!/usr/bin/env python
"""
nobody needs to understand a Laplace transformation for being able to
productively tinker around with a filter from scipy.signal

Why spend hours inventing special filters if others have already spent years
on it? Programming is communal work. Software gets better very fast, because
not every new programmer has to begin from scratch at stoneage level. You can
build on top of what others have already accomplished.

So it is all about a good mixture between deciding to invent something and
deciding to use other people's work. If you try to reinvent everything, then
you are slow, but if you never force yourself to not google and to find own
solutions, then you learn nothing. After you have learnt the basics you will
more and more often experience situations when googling takes more time than
the writing of own code fitting nicely to your needs.

Now look at the extensive libraries at www.scipy.org where they collect basic
tools for crunching numbers and vast data sets which are programmed to be
general and convenient to use and optimised for fast execution time.

Below we're going to use the functions butter() and filtfilt() from the
scipy.signal section of the scipy code library.
"""

from numpy import array, arange, zeros, pi, sin, mean, where
from numpy.random import rand, randint
import scipy.signal as sps
import matplotlib.pyplot as plt

N = 400
t = 6*pi*arange(N,dtype=float)/N # the time scale
w = 1.                           # the frequency
s = sin(w*t)                     # a sine signal, it spans the interval [-1,+1]
noise = 2*rand(N) - 1            # random values also covering [-1,+1]
snr = 0.2                        # the signal-to-noise ratio
#y = snr*s + (1-snr)*noise        # the final signal for testing the filter
y = where(s>0, 1, -1)            # an alternative signal

## and some more degradation of the signal
## how can the filter be modified to make the filtered signal look smoother?
#outliers = randint(N,size=5)
#for idx in outliers:
#    y[idx]=5

showme='part_1'

if showme == 'part_1':
    print 'what is the stuff that is produced by sps.butter()?'
    result = sps.butter(2,0.5)
    print 'type(result) = {}'.format(type(result))
    print 'len(result) = {}'.format(len(result))
    b,a = result
    print 'at order 2 this is b: {}'.format(b)
    print 'at order 2 this is a: {}'.format(a)
    b,a = sps.butter(4,0.5)
    print 'at order 4 this is b: {}'.format(b)
    print 'at order 4 this is a: {}'.format(a)
    print 'The function sps.filtfilt(blist,alist,signal) can make something of'
    print "these two coefficient lists even if we don't. See what happens next."
    plt.plot(t,y,label='original signal')
    plt.plot(t,sps.filtfilt(b,a,y),label='filtered signal')
    plt.legend()
    plt.show()
    

elif showme == 'part_2':
    order=2
    cutoffs = [1.0, 0.5, 0.1, 0.05, 0.02, 0.01, 0.005]
    colors = ['b','c','r','g','y','orange','grey']
    plt.plot(t,y,'k-')
    
    for i,cutoff in enumerate(cutoffs):
        b,a = sps.butter(order,cutoff)
        plt.plot(t, sps.filtfilt(b,a,y), linestyle='-', color=colors[i], lw=2, label='cutoff {}'.format(cutoff))

    plt.legend()    
    plt.show()


"""
Task A:
We saw how the result looks if the same signal is treated with the filter under
different cutoff settings. Next, make plots showing how different signals come
out under given cutoff settings. Try different signals, but make sure when
experimenting with periodic signals to also vary the frequency.

Task B:
on the first encounter one doesn't have to understand all about these types of
filters, but the term Nyquist frequency is quite important, it also shows up in
the online documentation ...
http://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html#scipy.signal.butter
... Try to find out what that term stands for. There is e.g. an article on
Wikipedia.

Task C:
Characterise one filter thouroughly, proove to yourself for one setting that
the frequency cutoff really happens where you assume it to be by automatically
examining signals with many different frequencies, and by aggregating analysis
data for one telling plot. Does your final script still work when you change
the length N of the signal array?
"""
