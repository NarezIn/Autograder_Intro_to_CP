import os
from datetime import datetime

def readReturn(filepath):
    """
    Input: the filepath to the file.
    Return the exact code of this student's code file.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

def late_submission(filepath):#work on this later.
    """
    Input: the filepath to the file.
    Check if this submission is late by
    comparing the last time this file had been changed with the due date.
    If late, return the number of class session that it passed after the due date.
    """
    t_stp = os.stat(filepath).st_mtime
    date_time = datetime.fromtimestamp(t_stp)
    date = date_time.date()
    time = date_time.time()
    print("Date is", date, "\nand time is", time)
    #then compare date, time with the due date.
    late_num = 1
    return late_num

def check_illegal_forloop(code_content): #Upgrade it if possible?
    """
    Check if this file incorporates for loop by looking if there is "for" in the code.
    """
    #Use python's "ast" module would be a reliable update.
    if "for(" in code_content:
        return "Incorporates for loop which is prohibited to use in this assignment. Graders please check it manually to confirm."
    
def check_illegal_function(code_content): #Upgrade it if possible?
    """
    Check if this file incorporates cunstom functions by looking if there is "def" in the code.
    """
    #Use python's "ast" module would be a reliable update.
    if "def" in code_content:
        return "Incorporates cunstom function(s) which is prohibited to use in this assignment. Graders please check it manually to confirm."
    

if __name__ == "__main__":
    #this line means that the following code would be executed only if we run this file
    #following code would not be executed if this file is imported.
    late_submission("A3/stu_submissions/Richard_Park_3a.py")