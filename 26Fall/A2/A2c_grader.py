import os
import subprocess
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Get the parent directory of the current file, to import utility_functions module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import utility_functions as uf

# Load environment variables from .env file
load_dotenv()

chat = ChatOpenAI(
    model="gpt-5", 
    temperature=0.0,
    openai_api_key = os.getenv("OPENAI_API_KEY")
)

template_string = """You are a code grader. \
You will be given student's code submission ```{student_code}``` \
and its output ```{student_output}```, and the rubric of that assignment ```{rubric}```. \
Only follow the rubric for deductions. \
If the rubric does not cover something, output "Need Human Check!" explicitly.\
Format the grading comment according to ```{grade_comment_template}``` only."""

prompt_template = ChatPromptTemplate.from_template(template_string)

# consider put this in the utility_functions
def get_submission_dir(hw_name):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of this script
    return os.path.join(BASE_DIR, "stu_submissions", hw_name)

def readReturn(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

def getOutErr(filepath, mock_inputs, timeout=5):
    result = subprocess.run([sys.executable, filepath], input=mock_inputs, capture_output=True, text=True, timeout=timeout)
    return [result.stdout, result.stderr]

def writeInComments(filepath, student_grade_comment):
    comment = open("mapped_grade_comments.txt", "a")
    comment.write(filepath + "::::" + "\n")
    comment.write(student_grade_comment + "\n" + "\n")
    comment.close()

def has_comments(stu_code):
    return '"""' in stu_code or "'''" in stu_code or "#" in stu_code

def uses_format_or_fstring(stu_code):
    return "format(" in stu_code or "f\"" in stu_code or "f'" in stu_code

def grade(n_limit = None):
    print("Running...")
    count = 0
    target_dir = get_submission_dir("HW2c")
    rubric = readReturn(os.path.abspath("A2/rubrics/A2c_rubric.txt"))
    grade_comment_template = readReturn(os.path.abspath("A2/grade_comment_template.txt"))
    for filename in sorted(os.listdir(target_dir), key=str.lower):
        filepath = os.path.join(target_dir, filename)
        count += 1
        if filename.endswith(".py"):
            mock_inputs = "600\n"
            [stu_out, stu_err] = getOutErr(filepath, mock_inputs)
            if stu_err.strip():
                writeInComments(filename, ": Need Human Check!")
                continue
            stu_code = readReturn(os.path.abspath(filepath))
            student_bundle = uf.create_student_bundle(prompt_template, stu_code, stu_out + "\n" + stu_err, rubric, grade_comment_template)
            student_grade_comment = chat.invoke(student_bundle["messages"])
            if (not has_comments(stu_code)):
                student_grade_comment.content += "\n-1, No comments in the code."
            if (not uses_format_or_fstring(stu_code)):
                student_grade_comment.content += "\nDoes not use format() or f-string."

            writeInComments(filename, student_grade_comment.content)
        if n_limit is not None and count >= n_limit:
            break
    print("Program ends.")
            
grade()