import sys
import os
import subprocess

# Get the parent directory of the current file, to import utility_functions module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utility_functions as uf

def test_case(file_path):
    """
    The test case of A6 Part a.
    """
    report = open("A6/Grade_Comments.txt", "a")
    report.write(file_path + ":" + "\n")
    report.close()

    mock_inputs = ["my_var", "var123", "_my_var", "123var", "my var", "my-var", "if", "import"]
    expected_output = [True, True, True, False, False, False, False, False]
    stu_output = []
    for ii in range(len(mock_inputs)):
        try:
            result = subprocess.run(["python", file_path], input=mock_inputs[ii], capture_output=True, text=True, check=True)
            each_output = result.stdout
        except subprocess.CalledProcessError as e:
            # If an error occurs during any run, report it and skip this student
            with open("A6/Grade_Comments.txt", "a") as report:
                report.write("Error running this file. Could not complete testing.\n\n")
            return  # Skip the rest and move to next file
        stu_output.append(each_output)
    check_report(file_path, mock_inputs, stu_output, expected_output)
    #return stu_output

def check_report(file_path, inputs, stu_output, expected_output):
    """
    Helper method to check if the stu_output match the expected output.
    If not, report the exact input that has an output that is not matched with the expected.
    """
    report = open("A6/Grade_Comments.txt", "a")
    wrong_num = 0
    for ii in range(len(stu_output)):
        #check the meaning of each output, "not" or "invalid" means False.
        if "not" in stu_output[ii] or "invalid" in stu_output[ii]:
            #check if the expected output is alse False. If not, report
            if expected_output[ii] == True:
                wrong_num += 1
                report.write("Input: " + inputs[ii] + "\n")
                report.write("has an incorrect output. Please Check.\n")
        else:
            if expected_output[ii] == False:
                wrong_num += 1
                report.write("Input: " + inputs[ii] + "\n")
                report.write("has an incorrect output. Please Check.\n")
    if wrong_num == 0:
        report.write("Passed All Test Cases!\n")
    else:
        report.write("Failed " + str(wrong_num) + " Tests.\n")
    report.write("\n")
    report.close()


def main():
    for filename in os.listdir("A6\stu_submissions"):
        filepath = os.path.join("A6\stu_submissions", filename)
        if os.path.isfile(filepath):  # Ensures it's a file, not a directory
            test_case(filepath)

if __name__ == "__main__":
    main()