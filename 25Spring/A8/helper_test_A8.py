"""
This program serves as a helper for runnning test_A8. 
Running this program would generate 8 .txt files, named class*_grades.txt, 
"*" stands for from 1 to 8.
so that the test_A8 file can check if the file written by student's program
is the same as the expected class*_grades.txt.
"""

#how to solve the input() problem?
#iterate through 1 to 9.

from data_files import Hua_Benji_8 as student

if __name__ == "__main__":
    student.main()