This is the autograder for assignments in the course Introduction to Computer Programming, CSCI-UA 2, with Prof. Joshua Clayton as the Instructor. If you are a grader and you would like to use this program to help you grade, please know that assignments may differ from semester to semester. Feel free to make adjustments according to the current assignment instructions.

#### Author: Zeran Ni (Simon)
    His Words:
        Hi! I was a student in Prof. Clayton's section of Introduction to Computer Programming in 2023 Fall. I became a tutor for this course from 2024 Spring until now (2024 Fall), and took the role of grader for Prof. Clayton in 2024 Fall. I found tutor is a more interesting postition compared to grader as tutors can interact with students and instructors, where as grader is more like a "office job" that you just do it while sitting for hours. On Nov. 25, 2024, I asked Prof. Clayton that why this class does not use Gradescope to grade students' assignments, and he said that Gradescope depends on functions calls, which would not be covered at the later part of this course. I guess this is the obstacle that I should conquer in this automated grader program. With me luck.

#### Course Info:
    Course Name: CSCI-UA.0002-011
    Semester: 2024 Fall
    Instructor: Prof. Joshua Clayton

#### General Grading rules:
    They are just my empirical rules that can apply to grading all assignments.
    1. About Late Submission: For each class period that the homework is late, 10% of the grade will be deducted. For example, if the homework is due on this Monday, but the student make their submission next Tuesday, 30% percent of the grade of this assignment should be deducted, as this submission is late for three periods of class.
    2. If the student's program incorporates python concepts that are clearly prohibited in the instructions, deduct 1 point of the grade for the the specific part of the assignment. If that part of the assignment already worths very little, make the deduction less based on your own judgment.
    3. It is pretty much your own call to make deductions on students' assignments. Honestly, each grader has their own grading criteria, even though there is a grading rubric in each assignments. For example, some grader might deduct 0.1 points if a student did not add the thousand separator in the format function, whereas the other might deduct 0.25 points.
    4. I personally hate students who used generative AI to write the code without even trying to understand the code. Sometimes it is hard to tell and make the conviction, but I would deduct more points on assignments that I suspect incorporating code written by AI. Usually, if a student still uses concepts (custom functions, etc.) that are prohibited in the next assignment after I warned this student to not to use them in the grading comment of this assignment, I would suspect that this student used AI to write the code as they might be more willing to get deductions rather than really putting effort to think and write the code on their own. So I always grant their wishes.
    *5. I haven't found any students plagarized others' work. Maybe this autograder program can be a little help to better detect plagarism.

#### Discovered Issues, Solutions, and Notes:
    About this Autograder:
        1. Grading Rubric for each assignment is not settled and depends on the specific assignment. You can also make nuances about the number of points you want to deduct.
            Solution: Learn about stdout and utilize it: A program's output would be generated to the stdout stream in default, so we can just redirec the output to a specific file instead of the stdout steam.
        2. python os and datetime module can be used to determine if the student turns their work late.
    About Manually Grading:
        1. It would be better if every grader has the same grading criteria, because it would be fairer to all students.
        2. Add more maybe, if applicable.########//////

Directory Structure: (fix this later)
autograder_intro_to_cp
    │──.venv (not sure if I need this)
    │
    └──autograder_intro_to_cp_24Fall
        │── autograder_A8
        │       │── data_files
        |       |       |
        |       |       |──expected_output (has lots of files showing expected output)
        |       |       |
        │       │       └──Hua_Benji_8.py
        │       │       
        │       │
        │       └── test_A8.py
        │       
        │
        └──README.md
        
Some Notes that I don't know hwo to organize:
1. In Grade_Comments.txt of each assignment, I use the ✅ character to record if I have graded this file on the grading web. I use **** to mask.
3. Make sure you delete/mask all information of students before you upload them somewhere.
4. Make a directory structure generater?
