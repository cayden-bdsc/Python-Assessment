# This is the 1st version of the quiz program

# Import necessary modules
import sys
import csv
import matplotlib.pyplot as plt
from pathlib import Path
import os

# Get the directory where the script is located
script_dir = Path(__file__).parent
results_file = script_dir / 'quiz_results.csv'

# Define the score
score = 0

# Create results file if it doesn't exist
if not results_file.exists():
    with open(results_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Score', 'Percentage'])

# Define the quiz questions and answers
questions_answers = {
    "What is New Zealand's Capital City?": "Wellington",
    "What is the capital city of France?": "Paris", 
    "What is the capital city of Germany?": "Berlin",
    "What is the capital city of Italy?": "Rome",
    "What is the capital city of Japan?": "Tokyo",
}

# Function to display the quiz
def display_quiz():
    print("\nWelcome to the Quiz Game!")
    
    # Get user's name
    while True:
        name = input("Please enter your name: ").strip()
        if name and not name.isspace() and len(name) >= 2:
                break
        print("Please enter a valid name (at least 2 characters).", "Invalid Input")
    
    
    # Age verification
    while True:
        try:
            age = int(input("Please enter your age: "))
            if 12 <= age <= 18:
                print("\nAge verified! You can proceed with the quiz.")
                break
            else:
                print("\nSorry, this quiz is only for participants aged 12-18.")
                sys.exit()
        except ValueError:
            print("\nPlease enter a valid number for your age.")
    
    print("You will be asked 5 questions.\n")
    return name

def plot_results_comparison(current_name, current_score):
    # Read all results
    names = []
    scores = []
    with open(results_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            names.append(row['Name'])
            scores.append(float(row['Percentage']))
    
    # Create bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(names, scores)
    plt.axhline(y=current_score, color='r', linestyle='--', label='Your Score')
    plt.xlabel('Participants')
    plt.ylabel('Score (%)')
    plt.title('Quiz Results Comparison')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Display the quiz
name = display_quiz()

for k, v in questions_answers.items():
    print("-" * 50)
    while True:
        user_answer = input(f"\n{k}: ").strip()  # Added strip() to remove whitespace
        if not user_answer:  # Check if answer is empty
            print("\nPlease enter an answer. Try again.")
            continue
        if user_answer.lower() == v.lower():
            print("\nCorrect! You earned a point.\n")
            score += 1
            break
        else:
            print(f"\nIncorrect. The correct answer is {v}.\n")
            break

print("-" * 50)
percentage = (score / 5) * 100
print(f"\nQuiz complete! Your score is {score} out of 5 ({percentage:.1f}%).\n")

# Save results to file
with open(results_file, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([name, score, percentage])

# Show comparison graph
plot_results_comparison(name, percentage)