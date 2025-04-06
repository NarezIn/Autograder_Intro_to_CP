import sys
import os
import re#new library I imported, good for searching word.
import subprocess

# Get the parent directory of the current file, to import utility_functions module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utility_functions as uf

"""
Rubric: 
"Part B should encode and decode strings with a function to add letters (2 points), 
a function to remove letters (1 point), 
a function to shift characters (1 point), 
and a main() function to encode and decode messages using the other functions (3 points)."
"""

def test_case_1(file_path):
    """
    First test case of A6 part b.
    Mainly testing encoding.
    """
    report = open("A6/Grade_Comments.txt", "a")
    report.write(file_path + ":" + "\n")
    report.close()

    mock_inputs = "e\n3\nPeace and Love\nq"
    expected_output = "Smzuhd}PdjNEf|lkhoDj#OtsdowEqqK]gLGw#zqWOpogr}jKyGl[hqJk"[::4]#we only need to check the shifted characters.
    try:
        result = subprocess.run(["python", file_path], input=mock_inputs, capture_output=True, text=True, check=True)
        stu_output = result.stdout
    except subprocess.CalledProcessError as e:
        # If an error occurs during any run, report it and skip this student.
        # If this error occurs, it would be very likely that there is an error in the student's code.
        with open("A6/Grade_Comments.txt", "a") as report:
            report.write("Test Case 1: Error running this file. Could not complete testing.\n\n")
        return  # Skip the rest and move to next file
    #looking for the first line we want
    match = re.search(r"(?:encoded word is[:\s]*)?([A-Za-z0-9{}\[\]\\|\"#<>\+,.!@^%$*&`~'-]{10,})", stu_output)
    report = open("A6/Grade_Comments.txt", "a")
    if match:
        if expected_output == match.group(1)[::4]:
            report.write("Test Case 1: Passed!\n")
        else:
            report.write("Test Case 1: Not Passed. Please Check.\n")
    else:
        report.write("Test Case 1: Cannot find the line we want. Please Check.\n")
    report.close()

def test_case_2(file_path):
    """
    Second test case of A6 part b.
    Mainly testing decoding.
    """
    mock_inputs = "d\n3\nSmzuhd}PdjNEf|lkhoDj#OtsdowEqqK]gLGw#zqWOpogr}jKyGl[hqJk\nq"
    expected_output = "Peace and Love"
    try:
        result = subprocess.run(["python", file_path], input=mock_inputs, capture_output=True, text=True, check=True)
        stu_output = result.stdout
    except subprocess.CalledProcessError as e:
        # If an error occurs during any run, report it and skip this student.
        # If this error occurs, it would be very likely that there is an error in the student's code.
        with open("A6/Grade_Comments.txt", "a") as report:
            report.write("Test Case 2: Error running this file. Could not complete testing.\n\n")
        return  # Skip the rest and move to next file
    #looking for the first line we want
    stu_output = stu_output.split("\n")
    matched = False
    for line in stu_output:
        if expected_output in line:
            matched = True
            break
    report = open("A6/Grade_Comments.txt", "a")
    if matched:
        report.write("Test Case 2: Passed!\n")
    else:
        report.write("Test Case 2: Not Passed. Please Check.\n")
    report.write("\n")
    report.close()

def main():
    for filename in os.listdir("A6\stu_submissions"):
        filepath = os.path.join("A6\stu_submissions", filename)
        if os.path.isfile(filepath):  # Ensures it's a file, not a directory
            test_case_1(filepath)
            test_case_2(filepath)

def self_test():
    #unrelated to test cases/grading.
    word_unshifted = "Smzuhd}PdjNEf|lkhoDj#OtsdowEqqK]gLGw#zqWOpogr}jKyGl[hqJk"[::4]
    word_shifted = ""
    for i in word_unshifted:
        num = ord(i)
        word_shifted += chr(num-3)
    print(word_unshifted)
    print(word_shifted)

if __name__ == "__main__":
    self_test()