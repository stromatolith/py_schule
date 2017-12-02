## language and thinking are interdependent
... therefore casting concepts into language can benefit the thinking process.

If you just write down in the language of Python ...
- pupils have maths grades
- pupils have english grades
- a class has several pupils
- computing the average grade means summing up and dividing by the total number of pupils (or tests or both)

... then you have done in a couple minutes 99% of the conceptual work ... of the work of what? ... well, e.g. of programming a grades database and convenience and statistics tool.

Thinking of objects and their abilities is a basic concept in object-oriented programming. Just invent the objects and then write down wish lists of their abilities and ways of interactions. This way you can more easily imagine different ways of interactions and different ability setups, then you decide on the best way to go and complete its implementation.

Should it be `teacher.pose_exam(theclass,subject)` or `theclass.write_exam(teacher, subject)`? Should it be `theclass.compute_average_grade(subject)` or `thepupil.compute_average_grade(subject)` or both? Should it be `teacher.betrayal_check(theclass)` or `[teacher.check_betrayal(pupil) for pupil in theclass]` or `pupil.copy_from(which_fellow,discover_probability=P)`?

Teachers can try to find programming tasks where programming becomes really intuitive, think of `player1.throw_dice()` or `player1.steal_random_card_from(player4)`, i.e. teachers can devise programming tasks where you can simply say: just invent object classes and their abilities in such a way that you can start speaking in sentences which make sense. This way the learners can train thinking techniques which can later be applied to much more abstract challenges.
