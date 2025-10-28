import os
# import subprocess
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Get the parent directory of the current file, to import utility_functions module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import utility_functions as uf

# Load environment variables from .env file
load_dotenv()


def create_student_bundle(prompt_template, stu_code, rubric, grade_comment_template):
    """
    By passing in the prompt_template,
    create a bundle of student code, output, and rubric to be sent to the chat model.
    """
    return {
        "messages": prompt_template.format_messages(
            student_code=stu_code,
            rubric=rubric,
            grade_comment_template=grade_comment_template
        )
    }

def grade(chat, prompt_template, n_limit = None):
    """
    Return a dictionary, key is filename, value is the single block comment
    """
    single_block_comment_dict = {}
    count = 0
    HW_num_str = '4'
    HW_part_str = 'a'
    target_dir = uf.get_sub_dir("25Fall", "A" + HW_num_str, "HW" + HW_num_str +  HW_part_str)
    print("Grading directory:", target_dir)#debug
    rubric = uf.readReturn(os.path.abspath("A" + HW_num_str + "/rubrics/A" + HW_num_str +  HW_part_str +"_rubric.txt"))
    grade_comment_template = uf.readReturn(os.path.abspath("A" + HW_num_str + "/grade_comment_template.txt"))

    for filename in sorted(os.listdir(target_dir), key=str.lower):
        if not filename.endswith(".py"):
            continue
        filepath = os.path.join(target_dir, filename)
        count += 1
        stu_code = uf.readReturn(os.path.abspath(filepath))
        student_bundle = create_student_bundle(prompt_template, stu_code, rubric, grade_comment_template)
        student_grade_comment = chat.invoke(student_bundle["messages"]).content

        single_block_comment_dict[filename] = student_grade_comment
        if n_limit is not None and count >= n_limit:
            break
    print(single_block_comment_dict)
    return single_block_comment_dict

def A4a_grader(n_limit=None):
    chat = ChatOpenAI(
        model="gpt-5", 
        temperature=0.0,
        openai_api_key = os.getenv("OPENAI_API_KEY")
    )

    template_string = """You are a code grader. \
    You will be given the student's Python code submission ```{student_code}```. \
    Do NOT execute the code or rely on runtime output. \
    Evaluate the submission only by inspecting the source code, according to the rubric ```{rubric}```. \
    If the rubric does not cover something, output "Need Human Check!" explicitly. \
    Format the grading comment according to ```{grade_comment_template}``` only."""

    prompt_template = ChatPromptTemplate.from_template(template_string)
    return lambda n_limit=None: grade(chat, prompt_template, n_limit)