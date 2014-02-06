#!/usr/bin/env python
"""
Now attention: here comes the next advantage of NUMERICAL COMPUTATION:
the computer doesn't complain about loads of stupid work!

You can tell the computer to find the right value for K that will double 100
Euros in 10 years.
"""

c = 100.0       # the start capital: 100 Euros
n = 10          # the time, the number of years
K = 1.03        # 3% interests means each year you multiply with that number

step = 0.005
counter = 0
while True:
    K = K+step
    final = c * K**n
    counter = counter + 1
    if final < 200:
        print "I checked K = {} and it wasn't enough, because the result was {}".format(K,final)
    else:
        print 'This one did it: K = {} yielded {} Euros at the end'.format(K,final)
        print "You had me do that stupid calculation {} times, don't you feel bad?".format(counter)
        break


"""
And here is an more interesting task for you:
Find out the interest rate that will hit the 200 Euros with a precision of less
than one cent?

approach A (do-it-yourself):
 - play with the parameters in this program
 - increase the starting K, make the step smaller

approach B (algorithmic):
 - specify more rules for the computer to proceed
 - let it automatically do what you would have done

Approach A will definitely be quicker and involve less headache. It is the
quick and dirty solution. But should there be any subsequent questions, e.g.

 - What K triples the capital?
 - Which rate turns you into a millionaire within 20 years?

... then the work you put into coming up with a nice algorithm will pay off!

(Actually, to be honest, if you have enough computer power and time, then
the algorithm doesn't have to be that nice at all. But in order to train your
abilities, it definitely makes sense to start a competition in class: which
group comes up with the most efficient algorithm solving that type of question
with the fewest computations (on average) and which is robust and works with
any pair of values in the question.)
"""
