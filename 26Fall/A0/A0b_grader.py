import os
import subprocess
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load environment variables from .env file
load_dotenv()

chat = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0.0,
    openai_api_key = os.getenv("OPENAI_API_KEY")
)

template_string = """You are a code grader. \
You will be given student's code submission ```{student_code}``` \
and its output ```{student_output}```, and the rubric of that assignment ```{rubric}```. \
Strictly based on ```{rubric}``` your task is to give a 'grading comment' to each student based on the ```{grade_comment_template}```.\
For each student's grading comment, you need to give a grade after checking their ```{student_code}``` and ```{student_output}```.
For every deduction, you need to have a reason, and this reason must be based on the rubric, \
but if the rubric doesn't have related information, simply label "Need Human Check" after the deduction.\
"""

prompt_template = ChatPromptTemplate.from_template(template_string)

def create_student_bundle(stu_code, stu_out, rubric, grade_comment_template):
    """
    create a bundle of student code, output, and rubric to be sent to the chat model.
    """
    return prompt_template.format_messages(
        student_code = stu_code, #read student code somewhere else as a string
        student_output = stu_out, #do subprocesss run somewhere else
        rubric = rubric, #read rubric somewhere else as a string
        grade_comment_template = grade_comment_template
    )

# consider put this in the utility_functions
def get_submission_dir(hw_name):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of this script
    return os.path.join(BASE_DIR, "stu_submissions", hw_name)

def readReturn(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

def getOutErr(filepath):
    result = subprocess.run([sys.executable, filepath], input="Lily\nLily\nLily\nLily\nLily\nLily\nLily\nLily\nLily\nLily\n", capture_output=True, text=True, timeout=5)
    return [result.stdout, result.stderr]

def writeInComments(filepath, student_grade_comment):
    comment = open("mapped_grade_comments.txt", "a")
    comment.write(filepath + "::::" + "\n")
    comment.write(student_grade_comment + "\n" + "\n")
    comment.close()

def grade():
    count = 0
    target_dir = get_submission_dir("HW1b")
    rubric = readReturn(os.path.abspath("A1/rubrics/A1b_rubric.txt"))
    grade_comment_template = readReturn(os.path.abspath("A1/grade_comment_template.txt"))
    for filename in sorted(os.listdir(target_dir), key=str.lower):
        filepath = os.path.join(target_dir, filename)
        if filename.endswith(".py"):
            [stu_out, stu_err] = getOutErr(filepath)
            # print("STDOUT:", repr(stu_out))
            # print("STDERR:", repr(stu_err))
            stu_code = readReturn(os.path.abspath(filepath))
            student_bundle = create_student_bundle(stu_code, stu_out + "\n" + stu_err, rubric, grade_comment_template)
            student_grade_comment = chat(student_bundle)
            writeInComments(filename, student_grade_comment.content)
            
grade()