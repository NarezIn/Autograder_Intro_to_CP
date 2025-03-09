import sys
import os
import subprocess

# Get the parent directory of the current file, to import utility_functions module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utility_functions as uf

def verify_3sides(entire_output, expected):
    """
    A helper function to find the three sides in the output_list, and check if they are expected sides.
    Input1: Entire output of student's submission parsed by "\n" as a list. Need to get the three sides from this long list.
    Input2: Expected sides as a list with 3 floats.
    Returns True if the sides in output_list matches with expected sides, otherwise false.
    """
    output = []#to store the three sides reading from entire_output.
    for i in range(len(entire_output)):#traverse the entire output to find three sides. OPTIMIZE LATER!!??
        item = entire_output[i].lower()
        if "side" in item and ":" in item:
            output.append(float(item[item.find(":") + 1:].strip()))
        if len(output) == 3:
            break
    #Consider using the "re" module and the search() method in it to find the side?!?!
    #Check if student's 3 sides match the expected sides.
    for ii in range(len(expected)):
        if float(output[ii]) != expected[ii]:
            print("Three sides are verified and they do not match.")
            return False

    print("Three sides are verified and they match!")
    return True
    #You were here.

def test_case_1(file_path):
    """
    This is the 1st test case of Assignment 3a.
    Input is the file_path.
    Important local varibles are mock_inputs, stu_output.
    Returns points that should be deducted and corresponding reason.
    """
    #The logic of this test case to check
    #1. if three sides are 100, 100, 100.
    #2. if the type of the triangle is equilateral.
    #3. if student's file have nothing after asking if we would like to enter another set of coordinates.
    mock_inputs = "0\n0\n-50\n50\n86.6\n100\n0\nno"
    stu_output = subprocess.run(["python", file_path], input=mock_inputs, capture_output=True, text=True, check=True)
    output_list = stu_output.stdout.split("\n")
    output_list = output_list[1:]
    #print(output_list) #delete later
    expected_sides = [100.0, 100.0, 100.0] #the order of three sides matters.
    expected_validity = True #the (first) triangle is valid.
    expected_type = "equilateral" #the first triangle is equilateral.
    #Step1: Check if three sides match the expected three sides.
    if verify_3sides(output_list, expected_sides) == False:
        print("Test Case 1: Not Passed. Sides don't match.")
        return False
    #Step2: Check if the triangle validity match.
    for line in output_list:
        if "valid" and "triangle" in line:
            validity = True
            break
        elif "invalid" in line or "not a valid" in line or "not valid" in line:
            validity = False
            break
    if validity != expected_validity:
        print("Test Case 1: Not Passed. Validity doesn't match")
        return False
    #Step3: Check if the triangle type match.
    if expected_validity:
        for line in output_list:
            if "equilateral" in line:
                type = "equilateral"
                break
            elif "isosceles" in line:
                type = "isosceles"
                break
            elif "scalene" in line:
                type = "scalene"
                break
    if type != expected_type:
        print("Test Case 1: Not Passed. Type does't match.")
        return False
    
    #All match.
    print("Test Case 1: Passed")
    return True

def test_case_2(file_path):
    """
    This is the 2nd test case of Assignment 3a.
    Input is the file_path.
    Important local varibles are mock_inputs, stu_output.
    """
    mock_inputs = "-100\n-10\n-1\n0\n0\n0\n100\n100\n0\nyes\n110\n100\n75\n25\n0\n0\nyes\n0\n0\n50\n50\n100\n100\nno"
    stu_output = subprocess.run(["python", file_path], input=mock_inputs, capture_output=True, text=True, check=True)
    #print("Output:\n", stu_output.stdout)  #Modify to sth that actually checks the output.

    output_list = stu_output.stdout.split("\n")[1:]
    #print(output_list) #delete later.
    expected_sides = [100.0, 141.42, 100.0, 82.76, 79.06, 148.66, 70.71, 70.71, 141.42]
    expected_validity = [True, 0, 0, True, 0, 0, False] #the (first) triangle is valid.
    expected_type = ["isosceles", 0, 0, "scalene", 0, 0, ""] #the first triangle is equilateral.
    #Step1: Check if three sides match the expected three sides.
    for i in range(0, len(expected_sides), 3):
        if verify_3sides(output_list, expected_sides[i:i+2]) == False:
            print("Test Case 2: Not Passed. Sides don't match.")
            return False
        #Step2: Check if the triangle validity match.
        for line in output_list:
            if "invalid" in line or "not a valid" in line or "not valid" in line:
                validity = False
                break
            elif "valid triangle" in line:
                validity = True
                break
        if validity != expected_validity[i]:
            print("Test Case 2: Not Passed. Validity doesn't match")
            return False
        #Step3: Check if the triangle type match.
        if expected_validity[i]:
            for line in output_list:
                if "equilateral" in line:
                    type = "equilateral"
                    break
                elif "isosceles" in line:
                    type = "isosceles"
                    break
                elif "scalene" in line:
                    type = "scalene"
                    break
            if type != expected_type[i]:
                print("Test Case 2: Not Passed. Type does't match.")
                return False
        #remove everything about the triangle we looked.
        del output_list[0:output_list.index(line)+1]
        #print(output_list) #delete later
    #All match.
    print("Test Case 2: Passed")
    return True

def check_it_out(file_path):
    #file_path = os.path.join("A3\stu_submissions", file_name)#delete later if ok
    """
    comment = open("Grade_Comments.txt", "a")
    comment.write(file_path + ":" + "\n")
    """
    #Check if the filepath exists. If so, read the code and get the output.
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found!")
    else:
        #Check if this submission is late. 
        #if late.......
        #Read the code literally.
        stu_code = uf.read_code(os.path.abspath(file_path))

        #Get the standard output by running the current code file.
        try:
            pass1 = test_case_1(file_path)
            pass2 = test_case_2(file_path)
            #If this student passes the test case or not, write the info in the comment file.
            """
            if pass1:
                comment.write("Test Case 1: Passed\n")
            else:
                comment.write("Test Case 1: Not Passed. Please Take a look.\n")
            if pass2:
                comment.write("Test Case 2: Passed\n")
            else:
                comment.write("Test Case 2: Not Passed. Please Take a look.\n")"
            """
        except subprocess.CalledProcessError as e:
            print("Error:\n", e.stderr)  #Print errors if the script fail.
            print("It means either this autograder fails or the grader needs to manually grade this student's submission.")
        """comment.close()#close the file"""

def main():
    """
    for filename in os.listdir("A3/stu_submissions"):
        filepath = os.path.join("A3/stu_submissions", filename)
        if os.path.isfile(filepath):  # Ensures it's a file, not a directory
            check_it_out(filepath)"
    """
    check_it_out("A3/stu_submissions/rodrigues_izabella_3a.py")

main()