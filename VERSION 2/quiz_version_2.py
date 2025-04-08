# This is the 2nd version of the quiz program, which includes improvements and additional features.

# Import necessary modules
import time
import sys
import csv
from datetime import datetime
import random
import matplotlib.pyplot as plt
from pathlib import Path
import easygui as gui

# Define script directory and results file
script_dir = Path(__file__).parent
results_file = script_dir / 'quiz_results_2.csv'

class QuizGame:
    def __init__(self):
        self.score = 0
        self.name = ""
        # Age range constants
        self.MIN_AGE = 12
        self.MAX_AGE = 18
        # Questions and answers dictionary
        self.questions_answers = {
            "What is the capital of France?": ("Paris", ["Paris", "London", "Berlin", "Madrid"]),
            "What is the capital of Japan?": ("Tokyo", ["Tokyo", "Seoul", "Beijing", "Bangkok"]),
            "What is the capital of Brazil?": ("Brasília", ["Brasília", "Rio de Janeiro", "São Paulo", "Buenos Aires"]),
            "What is the capital of Australia?": ("Canberra", ["Canberra", "Sydney", "Melbourne", "Perth"]),
            "What is the capital of Egypt?": ("Cairo", ["Cairo", "Alexandria", "Luxor", "Aswan"]),
            "What is the capital of India?": ("New Delhi", ["New Delhi", "Mumbai", "Bangalore", "Chennai"])
        }
        self.num_questions = 5
        self.initialize_results_file()

    def initialize_results_file(self):
        # Initialize the results CSV file if it doesn't exist
        if not results_file.exists():
            with open(results_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Score', 'Percentage', 'Date'])

    def validate_name(self):
        # Get and validate user's name using easygui
        while True:
            name = gui.enterbox(
                msg = "Please enter your name:",
                title = "Quiz Registration"
            )
            if name is None:  # User clicked Cancel
                if gui.ynbox("Do you want to quit?", "Confirm Quit"):
                    sys.exit()
                continue
            if name and not name.isspace() and len(name) >= 2 and not name.isdigit():
                return name
            gui.msgbox("Please enter a valid name (at least 2 characters, no numbers1).", "Invalid Input")

    def validate_age(self):
        """Validate user's age using GUI"""
        while True:
            age = gui.integerbox(
                msg = "Please enter your age:",
                title = "Age Verification",
                lowerbound = 1,
                upperbound = 100
            )
            if age is None:  # User clicked Cancel
                if gui.ynbox("Do you want to quit?", "Confirm Quit"):
                    sys.exit()
                continue
            if self.MIN_AGE <= age <= self.MAX_AGE:
                gui.msgbox("Age verified! You can proceed with the quiz.", "Verification Successful")
                return age
            gui.msgbox(f"Sorry, this quiz is only for participants aged {self.MIN_AGE}-{self.MAX_AGE}.", "Age Restriction")
            sys.exit()

    def display_welcome(self):
        # Display welcome message using GUI
        gui.msgbox(
            msg = "Welcome to the Capital Cities Quiz!\n\n"
                "Test your knowledge of world capitals!",
            title = "Welcome"
        )
        
        self.name = self.validate_name()
        self.validate_age()
        
        gui.msgbox(
            msg = f"You will be asked {self.num_questions} multiple choice questions.\n"
                "For each correct answer, you'll receive 1 point.\n"
                "Choose your answer by clicking the correct option.",
            title = "Quiz Rules"
        )

    def ask_question(self, question, answer_data):
        """Ask a multiple choice question using GUI"""
        correct_answer, options = answer_data
        random.shuffle(options)  # Randomize option order
        
        user_answer = gui.buttonbox(
            msg = question,
            title = "Quiz Question",
            choices = options
        )
        
        if user_answer is None:  # User clicked Cancel
            if gui.ynbox("Do you want to quit the quiz?", "Confirm Quit"):
                sys.exit()
            return self.ask_question(question, answer_data)
        
        if user_answer == correct_answer:
            gui.msgbox("✓ Correct! You earned a point.", "Result")
            return True
        else:
            gui.msgbox(f"✗ Incorrect. The correct answer is: {correct_answer}", "Result")
            return False

    def run_quiz(self):
         # Run the main quiz logic
        questions = list(self.questions_answers.items())
        random.shuffle(questions)
        selected_questions = questions[:self.num_questions]
        
        for question, answer_data in selected_questions:
            if self.ask_question(question, answer_data):
                self.score += 1

        self.percentage = (self.score / self.num_questions) * 100
        gui.msgbox(
            f"Quiz complete!\n\nYour score is {self.score} out of {self.num_questions} ({self.percentage:.1f}%).",
            "Quiz Results"
        )

    def save_results(self):
        """Save quiz results to CSV file"""
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(results_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.name, self.score, self.percentage, current_date])

    def plot_results_comparison(self):
        """Create and display results comparison graph"""
        names, scores, dates = [], [], []
        with open(results_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                names.append(row['Name'])
                scores.append(float(row['Percentage']))
                dates.append(row['Date'] if 'Date' in row else '')

        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(names)), scores)
        
        for i, (name, score) in enumerate(zip(names, scores)):
            if name == self.name and score == self.percentage:
                bars[i].set_color('green')
            
        plt.xlabel('Participants')
        plt.ylabel('Score (%)')
        plt.title('Quiz Results Comparison')
        plt.xticks(range(len(names)), names, rotation=45)
        plt.axhline(y=sum(scores)/len(scores), color='r', linestyle='--', label='Average Score')
        plt.legend()
        plt.tight_layout()
        
        # Save the plot to a temporary file and show it using easygui
        temp_plot = script_dir / 'temp_results.png'
        plt.savefig(temp_plot)
        plt.close()
        
        gui.msgbox(
            msg="Here are the quiz results comparison:",
            title="Results Comparison",
            image=str(temp_plot)
        )
        
        # Clean up temporary file
        temp_plot.unlink()

def main():
    quiz = QuizGame()
    quiz.display_welcome()
    quiz.run_quiz()
    quiz.save_results()
    quiz.plot_results_comparison()

if __name__ == "__main__":
    main()