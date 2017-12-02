#! /usr/bin/env python
"""
Pupils have grades, a school class has pupils.

These eight words describe a situation you all know. In a second I can tell you
what I am thinking of and you can understand and think the same. Python is a
nice programming language because it allows brief and easily readable code.
You can use the language to put down your conceptual thoughts and later you can
fill in the details
"""
import numpy as np

#--- class definitions

class Pupil(object):
    
    def __init__(self,name):
        self.name=name
        self.math_grades=[]
        self.english_grades=[]
    
    def get_personal_average(self,subject):
        """given a subject compute the mean value from all the test grades"""
        raise NotImplementedError('I want to have this function, I will work the details later.')


class Schoolclass(object):
    
    def __init__(self,name):
        self.name=name
        self.pupils=[]
        self.size=0
    
    def update_size(self):
        self.size=len(self.pupils)
    
    def get_test_average(self,subject,i):
        """compute average of ith written test""" 
        S=0.
        if subject=='math':
            for pupil in self.pupils:
                S=S+pupil.math_grades[i]
        elif subject=='english':
            for pupil in self.pupils:
                S=S+pupil.english_grades[i]
        else:
            raise ValueError('unknown subject identifier "{}"'.format(subject))
        return S/float(self.size)

    def get_alltests_average(self,subject,number_of_tests):
        """compute average of ith written test""" 
        S=0.
        if subject=='math':
            for pupil in self.pupils:
                S+=np.sum(pupil.math_grades)
        elif subject=='english':
            for pupil in self.pupils:
                S+=np.sum(pupil.english_grades)
        else:
            raise ValueError('unknown subject identifier "{}"'.format(subject))
        return S/float(self.size)/float(number_of_tests)


#--- main part of the program

Otto=Pupil('Otto')
Otto.math_grades=[7,8,6,9,7]  # I don't know the grading system of you country, let's say 0 is worst and 10 is best
Otto.english_grades=[4,5,5,6,5]

Anna=Pupil('Anna')
Anna.math_grades=[9,9,6,7,8]
Anna.english_grades=[10,9,9,10,9]

Leila=Pupil('Leila')
Leila.math_grades=[1,2,3,4,5]
Leila.english_grades=[6,8,6,9,7]

Frank=Pupil('Frank')
Frank.math_grades=[7,6,5,4,3]
Frank.english_grades=[7,6,5,4,5]

Toby=Pupil('Toby')
Toby.math_grades=[7,7,8,7,7]
Toby.english_grades=[8,8,7,8,8]

a9=Schoolclass('9a') # a variable name cannot begin with a digit, that's a syntax rule
a9.pupils=[Otto,Anna,Leila,Frank,Toby]
a9.update_size()
math_avg1=a9.get_test_average('math',0)
math_avg5=a9.get_test_average('math',4)
total_english_avg=a9.get_alltests_average('english',5)

print 'average of 1st math test: ',math_avg1
print 'average of 5th math test: ',math_avg5
print 'total average across all english tests: ',total_english_avg

print 'averages of all math tests: ',[a9.get_test_average('math',i) for i in range(5)]
print 'averages of all english tests: ',[a9.get_test_average('english',i) for i in range(5)]

