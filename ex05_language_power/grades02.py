#! /usr/bin/env python
"""
1) Pupils have grades, a school class has pupils.
2) Some pupils are fearful/inherently honest and learn, others try to betray
   and copy from the neighbour
3) Teachers sometimes discover pupils copying, but if nobody betrays, then the
   teacher stops checking

The code is incomplete and represents only a concept framework.
possible challenges:
a) Under which conditions will all pupils learn and become better on the long term?
   Under which conditions will lazy pupils revert to 100% betrayal on the long term?
b) Can we see feedback cycles? I.e. waves of pupil dishonesty interacting with
   an oscillating check probability on the side of the teacher?
"""
from numpy.random import rand, randn, randint

#--- class definitions

class Pupil(object):
    
    def __init__(self,name):
        self.name=name
        self.math_grades=[]
        self.skill_level=0.
        self.honesty_level=0.5 # let's say 1 is honest and 0 is completely dishonest
    
    def get_personal_average(self,subject):
        """given a subject compute the mean value from all the test grades"""
        raise NotImplementedError('I want to have this function, I will work the details later.')

    def learn(self,hours):
        self.skill_level+=0.2*hours # instead of the value 0.2 there might be individual learning effect rates 
    
    def forget(self,weeks):
        self.skill_level-=0.5*weeks # instead of the value 0.5 there might be individual forget rates
    
    def write_exam(self,copy_from_fellow=None,exam_toughness='neutral'):
        if not copy_from_fellow is None:
            thisgrade=copy_from_fellow.skill_level+randn()
        else:
            thisgrade=self.skill_level+randn()
        if exam_toughness=='easy':
            thisgrade+=1.
        elif exam_toughness=='hard':
            thisgrade-=1.
        self.math_grades.append(thisgrade)

class Schoolclass(object):
    
    def __init__(self,name):
        self.name=name
        self.pupils=[]
        self.size=0
    
    def update_size(self):
        self.size=len(self.pupils)
    
    def write_exam(self,teacher,toughness_level):
        for pupil in self.pupils:
            # will this pupil try to betray and copy?
            # let's decide random-influenced but probability-based
            random_number=rand()
            if random_number < pupil.honesty_level:
                will_try_betrayal=False
            else:
                will_try_betrayal=True
            if will_try_betrayal:
                # copying from who? imagine random seating and choosing the better of two neighbours
                # need to randomly sample two different ones from the list of pupils in the class
                while True:
                    fellowA=self.pupils[randint(self.size)]
                    fellowB=self.pupils[randint(self.size)]
                    if not (fellowA is fellowB):
                        break
                if fellowA.skill_level > fellowB.skill_level:
                    pupil.write_exam(copy_from_fellow=fellowA, exam_toughness=toughness_level)
                else:
                    pupil.write_exam(copy_from_fellow=fellowB, exam_toughness=toughness_level)
                if rand() < teacher.betrayal_check_probability:
                    betrayal_discovered=True
                else:
                    betrayal_discovered=False
                if betrayal_discovered:
                    # what happens then? grade becomes zero? or skill-level minus 3?
                    # discovery should lead to increased fear and honesty next time
                    raise NotImplementedError('This is up to you.')
                else:
                    # what happens then? grade will be influenced by own and fellow's skill level
                    # no discovery should lead to decreased fear less honesty next time
                    raise NotImplementedError('This is up to you.')
            else:
                pupil.write_exam(exam_toughness=toughness_level)
    
class Teacher(object):

    def __init__(self,name):
        self.name=name
        self.betrayal_memory=[]
        self.betrayal_check_probability=0.5 # it the teacher has become lazy, it will be zero
    
    def pose_exam(self,theclass,toughness_level):
        check_success=theclass.write_exam(self,toughness_level)
        self.betrayal_memory.append(check_success)
        self.betrayal_memory=self.betrayal_memory[len(check_success)] # forget old incidences and keep the memory size constant
    
    def update_betrayal_check_probability(self):
        """update based on success rate during the N latest checks"""
        raise NotImplementedError('This is up to you.')
    
# main part of the program

"""
go through multiple rounds of exams in a loop:
   - pupils update their honesty level
   - teachers update their checking laziness level
   - modelling effect of time in between exams, i.e. effects of learning and forgetting
"""

"""
and by the way "gamification" ... after the programming exercise we can discuss
how thinking in terms of statistics, probabilities, and game theory influences
our understanding of the world we live in (keyword: plasticity of the brain).

Can too much practice of thinking in terms of statistics and game theory diminish
our ability to think in terms of virtues and "a better world", "a better society",
i.e. harm the ability of utopian thinking? What do you think of economic theories
based on "rational and informed consumers"? What do you think of political theories
based on everyday polls and things like "nudging"?

And to all you teachers out there: What should an ideal holistic education look
like between the extremes of (a) climate change and evolution denial and
(b) a purely mechanistic world view in combination with a purely carrot-stick
idea of human behaviour/nature?
"""

