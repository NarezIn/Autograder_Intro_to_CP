from A3a_grader import A3a_grader
from A3b_grader import A3b_grader

import re

def extract_student_id(filename: str) -> str:
    """
    Extracts the student identifier prefix from filenames like 'ni2a.py', 'simon2b.py', etc.
    You can adjust this logic if your filenames differ.
    """
    match = re.match(r"(.+?)3[a-c]\.py$", filename, re.IGNORECASE)
    return match.group(1) if match else filename  # fallback to full name if pattern fails

def write_combined_comments(combined_dict, output_path="mapped_grade_comments.txt"):
    with open(output_path, "w", encoding="utf-8") as f:
        for student_id, parts in sorted(combined_dict.items()):
            f.write(f"{student_id}::::\n")
            for part, comment in sorted(parts.items()):
                f.write(f"[{part}]\n{comment}\n\n")

def main():
    graders = [("3a", A3a_grader()), ("3b", A3b_grader())]
    all_results = {}

    for label, grader_func in graders:
        print(f"Running grader {label}...")
        sub_comments = grader_func()
        for filename, comment in sub_comments.items():
            student_id = extract_student_id(filename)
            if student_id not in all_results:
                all_results[student_id] = {}
            all_results[student_id][label] = comment

    write_combined_comments(all_results)
    print("✅ Combined grading completed!")


if __name__ == "__main__":
    main()