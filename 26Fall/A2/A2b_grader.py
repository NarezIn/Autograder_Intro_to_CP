import os
import re
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

def extract_table_values(stu_out):
    """
    Extracts numerical values from the student's output table.
    Returns a list of rows, where each row is [Starting Balance, Interest, Ending Balance].
    If any error occurs during extraction, returns False.
    """
    try:
        lines = stu_out.splitlines()
        # keep only lines that look like table rows (start with a month number)
        table_lines = [ln for ln in lines if re.match(r"\s*\d+\s", ln)]
        table = []
        for line in table_lines:
            # capture numbers with optional commas + decimals
            nums = re.findall(r"[\d,]+\.\d+", line)
            # convert "1,000.00" -> 1000.0
            nums = [float(x.replace(",", "")) for x in nums]
            table.append(nums)
        return table
    except Exception:
        return False

def has_comments(stu_code):
    return '"""' in stu_code or "'''" in stu_code or "#" in stu_code

def uses_format_or_fstring(stu_code):
    return "format(" in stu_code or "f\"" in stu_code or "f'" in stu_code

def grade(n_limit = None):
    print("Running...")
    count = 0# for testing
    target_dir = get_submission_dir("HW2b")
    rubric = readReturn(os.path.abspath("A2/rubrics/A2b_rubric.txt"))
    grade_comment_template = readReturn(os.path.abspath("A2/grade_comment_template.txt"))
    for filename in sorted(os.listdir(target_dir), key=str.lower):
        filepath = os.path.join(target_dir, filename)
        count += 1
        if filename.endswith(".py"):
            mock_inputs = "1000\n0.04\n"
            [stu_out, stu_err] = getOutErr(filepath, mock_inputs)
            if stu_err.strip():
                writeInComments(filename, ": Need Human Check!")
                continue
            table_array = extract_table_values(stu_out)
            table_str = "\n".join([", ".join(map(str, row)) for row in table_array])
            stu_code = readReturn(os.path.abspath(filepath))
            student_bundle = uf.create_student_bundle(prompt_template, stu_code, stu_out + "\n" + stu_err + "\nTable output:" + table_str, rubric, grade_comment_template)
            student_grade_comment = chat.invoke(student_bundle["messages"])
            if (uses_format_or_fstring(stu_code)):
                writeInComments(filename, student_grade_comment.content + "\nHas someways of formatting output.")
            else:
                writeInComments(filename, student_grade_comment.content + "\nProgram should format output using format() or f-strings.")
        if n_limit is not None and count >= n_limit:
            break
    print("Program ends.")
            
grade()