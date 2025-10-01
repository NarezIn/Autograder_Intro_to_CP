import os
import subprocess
import sys #not sure if I need this
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Get the parent directory of the current file, to import utility_functions module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import utility_functions as uf

# Load environment variables from .env file
load_dotenv()

chat = ChatOpenAI(
    model="gpt-4", 
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

# consider put this in the utility_functions
def get_submission_dir(hw_name):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of this script
    return os.path.join(BASE_DIR, "stu_submissions", hw_name)

def getOutErr(filepath):
    result = subprocess.run([sys.executable, filepath], capture_output=True, text=True)
    return [result.stdout, result.stderr]

def writeInComments(filepath, student_grade_comment):
    comment = open("mapped_grade_comments.txt", "a")
    comment.write(filepath + "::::" + "\n")
    comment.write(student_grade_comment + "\n" + "\n")
    comment.close()

def grade():
    target_dir = get_submission_dir("HW1a")
    # For debugging:
    # print("Looking for:", target_dir)
    # print("Exists?", os.path.exists(target_dir))
    # print("Is dir?", os.path.isdir(target_dir))
    counter = 0
    rubric = uf.readReturn(os.path.abspath("A1/rubrics/A1a_rubric.txt"))
    grade_comment_template = uf.readReturn(os.path.abspath("A1/grade_comment_template.txt"))
    for filename in sorted(os.listdir(target_dir), key=str.lower):
        filepath = os.path.join(target_dir, filename)
        counter += 1
        if os.path.isfile(filepath):  # Ensures it's a file, not a directory
            [stu_out, stu_err] = getOutErr(filepath)
            stu_code = uf.readReturn(os.path.abspath(filepath))
            student_bundle = uf.create_student_bundle(prompt_template, stu_code, stu_out + "\n" + stu_err, rubric, grade_comment_template)
            student_grade_comment = chat(student_bundle)
            writeInComments(filename, student_grade_comment.content)
        if counter >= 2:  #for debugging
            break

grade()