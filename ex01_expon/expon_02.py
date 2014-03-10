#!/usr/bin/env python
"""
Exponential growth is unintuitive. What is the annual interest rate that will
double 100 Euros during 10 years? What rate will multiply it by 100? Without
having ever looked at and remembering the results of such calculations one has
no chance of making good estimates.

With a computer program you can try out several interest rates and see how
the result changes when you play with the parameters. Playing with a computer
program can help you get a feeling quicker than doing the stuff with paper
and calculator. Secondly, you can do plotting and visualisation as well.

So here we have already several advantages of NUMERICAL COMPUTATION.
"""

"""
next thing: plotting
"""
from numpy import zeros
import matplotlib.pyplot as plt

c = 100.0       # the start capital: 100 Euros
n = 10          # the time, the number of years
K1 = 0.98        # 2% inflation means each year you multiply with that number
K2 = 1.03        # 3% interests means each year you multiply with that number

x = 100.0       # I will use this to do a test: does the formula really yield 
                # the same as if one counts in the interests every single year?

rowA=zeros(n)
rowB=zeros(n)
rowC=zeros(n)
row_test=zeros(n)
years=zeros(n)

for i in xrange(n):
    print 'now starting the calculation for year {}'.format(i)
    years[i]=i
    rowA[i] = c * K1**i
    rowB[i] = c * K2**i
    rowC[i] = c * (K1*K2)**i
    # above: the formula with powers
    # below: multiplying each year (purpose: proove validity of formula)
    x = x * K2 # another time you can test witth K1 or else with K1*K2
    row_test[i] = x


plt.plot(years, rowA, color='red', linestyle='-')
plt.plot(years, rowB, color='green', linestyle='-')
plt.plot(years, rowC, color='cyan', linestyle='-')
plt.plot(years, row_test, color='grey', marker='d', linestyle='None')
plt.xlabel('years')
plt.ylabel('Euros')
plt.title('Why are the grey diamonds not on the green line?')
plt.show()

"""
Question:
Can you do something so that the grey diamonds match the corresponding curve?

A more interesting question:
Can playing with the parameters of this program help you to answer this
question: what is the interest rate that will double the 100 Euros in 10 years?
"""

