import yaml
import random
import argparse

# Load questions from YAML file
def load_questions(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)['questions']

# Quiz Function
def run_quiz(questions, total_questions):
    print("Terraform Associate Exam Simulation\n")
    random.shuffle(questions)
    questions = questions[:total_questions]  # Limit questions to the specified count
    score = 0

    for idx, question in enumerate(questions, 1):
        print(f"Question {idx}: {question['question']}")
        for option in question['options']:
            print(option)
        user_answer = input("Enter the letter of your answer: ").strip().upper()
        if user_answer == question['answer']:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong. The correct answer was: {question['answer']}\n")

    print(f"Your total score: {score}/{len(questions)}")
    print("Thank you for participating!")

# Main Function
def main():
    parser = argparse.ArgumentParser(description="Run a Terraform Associate exam simulation.")
    parser.add_argument('filename', type=str, help="Path to the YAML file containing questions.")
    parser.add_argument('--total_questions', type=int, default=10, help="Total number of questions to ask.")
    args = parser.parse_args()

    questions = load_questions(args.filename)
    if args.total_questions > len(questions):
        print(f"Warning: Requested {args.total_questions} questions, but only {len(questions)} available.")
        args.total_questions = len(questions)

    run_quiz(questions, args.total_questions)

if __name__ == "__main__":
    main()
