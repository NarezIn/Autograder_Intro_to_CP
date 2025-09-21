def grade(filepath):
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(",")
    scores = []
    student_results = []
    valid_lines = 0
    invalid_lines = 0

    with open(filepath, 'r') as file:
        lines = file.readlines()
        
    print()
    print("**** ANALYZING ****")
    print()
    for line in lines:
        line = line.strip() 
        data = line.split(",")  

        if len(data) != 26:
            print("Invalid line of data: does not contain exactly 26 values:\n{}".format(line))
            print()
            invalid_lines += 1
            continue

        student_id = data[0]
        if not (student_id.startswith("N") and len(student_id) == 9 and student_id[1:].isdigit()):
            print("Invalid line of data: N# is invalid:\n{}".format(line))
            print()
            invalid_lines += 1
            continue

        valid_lines += 1

        student_answers = data[1:]
        score = 0
        for i in range(len(answer_key)):
            if i < len(student_answers):
                answer = student_answers[i]
                correct_answer = answer_key[i]
                if answer == correct_answer:
                    score += 4  
                elif answer == "":
                    score += 0  
                else:
                    score -= 1

        scores.append(score)
        student_results.append(student_id + "," + str(score))

    if invalid_lines == 0:
        print("No errors found!")

    if scores:
        mean_score = sum(scores) / len(scores)
        highest_score = max(scores)
        lowest_score = min(scores)
        score_range = highest_score - lowest_score
        scores.sort()  
        n = len(scores)
        
        if n % 2 == 1:  
            median_score = scores[n // 2]
        else: 
            median_score = (scores[n // 2 - 1] + scores[n // 2]) / 2

    else:
        mean_score = highest_score = lowest_score = score_range = median_score = 0
    print()
    print("**** REPORT ****")
    print()
    print("Total valid lines of data: {}".format(valid_lines))
    print("Total invalid lines of data: {}".format(invalid_lines))
    print()
    print("Mean (average) score: {:.2f}".format(mean_score))
    print("Highest score: {}".format(highest_score))
    print("Lowest score: {}".format(lowest_score))
    print("Range of scores: {}".format(score_range))
    print("Median score: {:.2f}".format(median_score))

    output_filename = filepath.replace(".txt", "_grades.txt")
    with open(output_filename, 'w') as output_file:
        for result in student_results:
            output_file.write(result + "\n")

def main(): #tutor add this.
    filename = input("Enter a class file to grade (e.g., class1 for class1.txt): ") + ".txt"
    try:
        grade(filename)
    except FileNotFoundError:
        print("File cannot be found. Please try again.")