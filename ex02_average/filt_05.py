#!/usr/bin/env python

"""
What next? Let's apply filters to lines and columns of pixels in a picture.
"""

from numpy import array, arange, zeros, ones, linspace, hstack, vstack, shape, zeros_like
from numpy import pi, exp, sin, cos, mean, where, amin, amax
from numpy.random import rand, randint
import scipy.signal as sps
import matplotlib.pyplot as plt

def smear_butter(image,channel,direc,cutoff):
    """
    image has 3 layers for rgb coding (the channels); direc is filter direction
    and can be 'horizontal', 'h', or 'vertical', 'v'; cutoff is the filter cutoff
    """
    channelcode = {'r':0, 'g':1, 'b':2}
    if type(channel) == str:
        channel = channelcode[channel]
    b,a=sps.butter(2,cutoff)
    n,m,ch=shape(image)
    if direc in ['horizontal','h']:
        for i in xrange(n):
            image[i,:,channel] = sps.filtfilt(b,a,image[i,:,channel])
    elif direc in ['vertical','v']:
        for i in xrange(m):
            image[:,i,channel] = sps.filtfilt(b,a,image[:,i,channel])

def normalize(img):
    for i in xrange(3):
        layer = img[:,:,i]
        mn,mx = amin(layer),amax(layer)
        #print shape((layer-mn)/(mx-mn))
        img[:,:,i] = (layer-mn)/(mx-mn)

nr,nc = 600,800  # numbers of rows and columns
ncl = 3          # number of colour channels

x = ones((nr,nc),dtype=float)
y = ones((nr,nc),dtype=float)
dat = ones((nr,nc,ncl),dtype=float)

for i in xrange(nr):
    y[i,:]=float(i)/nr

for i in xrange(nc):
    x[:,i]=float(i)/nc

for i in xrange(ncl):
    dat[:,:,i] = where(x+y>0.7, 0, 1) # look up what happens here in the online documentation
    dat[:,:,i] = where(x+y>0.9, 1, dat[:,:,i])
    cx,cy,r = 0.5,0.5,0.1
    dat[:,:,i] = where((x-cx)**2+(y-cy)**2<r**2, 0, dat[:,:,i])

picA = array(dat,copy=True)
smear_butter(picA,'r','v',0.01)

picB = array(picA,copy=True)
normalize(picB)

plt.imshow(dat)
plt.title('raw data')
plt.savefig('dat.png')
plt.close()

plt.imshow(picA)
plt.title('just filtered')
plt.savefig('picA.png')
plt.close()

plt.imshow(picB)
plt.title('filtered and normalized')
plt.savefig('picB.png')
plt.close()

"""
Challenge: make more artwork!

 ... and one interesting tool might be a sobel filter ...
 
    ... and if you wanna mess with an own photo, look here for finding out
        how to import one: http://matplotlib.org/gallery.html
"""
