import yaml
from openai import OpenAI
import os
import re
import random
# https://github.com/openai/openai-python
# Function to load the current questions.yaml file
def load_questions(filename='questions.yaml'):
    try:
        with open(filename, 'r') as file:
            return yaml.safe_load(file) or {'questions': []}
    except FileNotFoundError:
        return {'questions': []}

# Function to save questions to questions.yaml file
def save_questions(data, filename='questions.yaml'):
    with open(filename, 'w') as file:
        yaml.safe_dump(data, file)

# Function to generate incorrect answers using OpenAI Chat API
def generate_incorrect_answers(prompt, num_answers=3):
    try:
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"), 
        )
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        print(completion.choices[0].message.content)
        generated_text = completion.choices[0].message.content
        incorrect_answers = generated_text.split("\n")
        cleaned_answers = []
        for answer in incorrect_answers:
        # Remove leading numbers and punctuation
            answer = re.sub(r'^\s*\d+[\.\)]\s*', '', answer).strip()
            if answer:
                cleaned_answers.append(answer)
            if len(cleaned_answers) == num_answers:
                break
        return cleaned_answers
        # return [answer.strip() for answer in incorrect_answers]
    except Exception as e:
        print(f"Error generating incorrect answers: {e}")
        return []

# Function to add a new question
def add_question():
    question_text = input("Enter the question: ").strip()
    correct_answer = input("Enter the correct answer: ").strip()
    explanation = input("Enter the explanation: ").strip()
    incorrect_prompt = (
        f"Generate three plausible but incorrect answers to the following question:\n"
        f"Question: {question_text}\n"
        f"Correct answer: {correct_answer}\n"
        f"Please list each incorrect answer on a new line."
    )
    incorrect_answers = generate_incorrect_answers(incorrect_prompt, num_answers=3)

    if len(incorrect_answers) < 3:
        print("Could not generate enough incorrect answers. Please try again.")
        return

    # Formatting options for YAML file
    options = incorrect_answers + [correct_answer]
    options = sorted(options)  # Sort to randomize order without repeating

    # Add question to questions.yaml
    data = load_questions()
    data['questions'].append({
        'question': question_text,
        'options': [f"{chr(65 + i)}. {option}" for i, option in enumerate(options)],
        'answer': f"{chr(65 + options.index(correct_answer))}",
        'explanation': explanation
    })
    save_questions(data)
    print("Question added successfully!")

# Main function
if __name__ == "__main__":
    add_question()
