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
Let's start with a simple example:
a) How much of 100 Euros melt away during 10 years if the inflation is at 2%?
b) How much does the capital grow if I get 3% interest from the bank?
c) How does it look with both effects combined?
"""

c = 100.0       # the start capital: 100 Euros
n = 10          # the time, the number of years
K1 = 0.98        # 2% inflation means each year you multiply with that number

print 'after 10 years with 2% inflation: {}'.format(c * K1**n)

K2 = 1.03        # 3% interests means each year you multiply with that number

print 'after 10 years with 3% interest: {}'.format(c * K2**n)

print 'after 10 years with both effects: {}'.format(c * (K1*K2)**n)

print 'Now change the numbers and try out different things.'



