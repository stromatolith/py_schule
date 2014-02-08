#!/usr/bin/env python
"""
a so-called rolling average is a good way to visualise tendencies, so let's
create some random exam grades and apply the rolling average
"""


from numpy import array, arange
from numpy.random import randint
import matplotlib.pyplot as plt


"""
assume there are 6 written tests per schoolyear and we're looking at 2 years;
1 is the best grade, 6 is the worst, there are grades like 2- or 2-3 or 3+
"""
N = 12 # we want to write 12 tests
grades = randint(16,size=N) # 12 numbers from [0,1,...,15]
grades = array(grades,dtype=float)
grades = 1+grades/4.
#print grades
t=arange(N) # the time axis, here simply the exam number

plt.plot(t,grades,'bo-')
plt.show()

#n = 3      # how many grades shall be involved in the averaging
#ravg = []  # an empty list for storing the rolling average values to be computed below
#
#for i in xrange(N):
#    if i < n-1:
#        pass # i=0,1,2,3, .... if n=3 then only from the third step on can we
#             # look back at enough values to average
#    else:
#        avg = (grades[i-2]+grades[i-1]+grades[i])/3.
#        ravg.append(avg)
#
#plt.plot(t,grades,'bo-',label='grades')
#plt.plot(t[2:],ravg,'go-',lw=2,label='rolling average')
#plt.legend()
#plt.show()


