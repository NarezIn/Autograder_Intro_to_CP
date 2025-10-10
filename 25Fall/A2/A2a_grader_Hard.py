import shutil
#learn about this before A3.
#haven't modify this file for A2 yet.

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

def has_comments(stu_code):
    return '"""' in stu_code or "'''" in stu_code or "#" in stu_code

def uses_format_or_fstring(stu_code):
    return "format(" in stu_code or "f\"" in stu_code or "f'" in stu_code

def dyna_getOutErr(filepath, timeout=10):
    """
    Run a student Python script and adaptively feed inputs based on output prompts.
    Returns [stdout, stderr].
    """
    process = subprocess.Popen(
        [sys.executable, filepath],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output = ""
    error = ""

    try:
        while True:
            # Read one line of stdout
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break

            if line:
                output += line
                lower_line = line.lower()

                # Adaptive inputs based on detected keywords
                if "shirt" in lower_line or "shirts" in lower_line:
                    process.stdin.write("200\n")
                    process.stdin.flush()
                elif "color" in lower_line or "colors" in lower_line:
                    process.stdin.write("3\n")
                    process.stdin.flush()
                # Add more conditions here if other inputs are needed

        # Capture any remaining stdout and stderr after process ends
        remaining_out, remaining_err = process.communicate(timeout=timeout)
        output += remaining_out
        error += remaining_err

    except Exception as e:
        process.kill()
        error += f"\nException during execution: {e}"

    return [output, error]


def grade(chat, prompt_template, n_limit = None):
    """
    Return a dictionary, key is filename, value is the single block comment
    """
    single_block_comment_dict = {}
    count = 0

    target_dir = uf.get_submission_dir("25Fall", "HW2a")
    rubric = uf.readReturn(os.path.abspath("A2/rubrics/A2a_rubric.txt"))
    grade_comment_template = uf.readReturn(os.path.abspath("A2/grade_comment_template.txt"))

    for filename in sorted(os.listdir(target_dir), key=str.lower):
        if not filename.endswith(".py"):
            continue
        filepath = os.path.join(target_dir, filename)
        count += 1
        [stu_out, stu_err] = dyna_getOutErr(filepath)
        if stu_err.strip():
            single_block_comment_dict[filename] = "Need Human Check! (Runtime Error)"
            continue
        stu_code = uf.readReturn(os.path.abspath(filepath))
        student_bundle = uf.create_student_bundle(prompt_template, stu_code, stu_out + "\n" + stu_err, rubric, grade_comment_template)
        student_grade_comment = chat.invoke(student_bundle["messages"]).content

        single_block_comment_dict[filename] = student_grade_comment
        if n_limit is not None and count >= n_limit:
            break
    print("A2a completed")
    return single_block_comment_dict

def A2a_grader():
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
    return lambda n_limit=None: grade(chat, prompt_template, n_limit)