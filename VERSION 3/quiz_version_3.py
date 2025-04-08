# This is the 3rd version of the quiz program

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
results_file = script_dir / 'quiz_results_3.csv'

class QuizGame:
    def __init__(self):
        self.score = 0
        self.name = ""
        self.MIN_AGE = 12
        self.MAX_AGE = 18
        self.correct_answers = []
        self.wrong_answers = []
        
        # Expanded question bank with different types
        self.questions_bank = {
            "multiple_choice": {
                "What is the capital of France?": ("Paris", ["Paris", "London", "Berlin", "Madrid"]),
                "Which planet is known as the Red Planet?": ("Mars", ["Mars", "Venus", "Jupiter", "Saturn"]),
                "What is the chemical symbol for gold?": ("Au", ["Au", "Ag", "Fe", "Cu"]),
                "Who painted the Mona Lisa?": ("Leonardo da Vinci", ["Leonardo da Vinci", "Michelangelo", "Van Gogh", "Picasso"]),
                "What is the largest mammal on Earth?": ("Blue Whale", ["Blue Whale", "African Elephant", "Giraffe", "Polar Bear"])
            },
            "true_false": {
                "The Great Wall of China is visible from space": ("False", "This is a common myth. The wall is too narrow to be seen from space."),
                "Water boils at 100 degrees Celsius at sea level": ("True", "This is correct at standard atmospheric pressure."),
                "Humans use only 10% of their brains": ("False", "This is a myth. Humans use most of their brain."),
                "Sound travels faster in water than in air": ("True", "Sound indeed travels about 4 times faster in water."),
                "A day on Venus is longer than its year": ("True", "Venus takes longer to rotate on its axis than to orbit the Sun.")
            },
            "numerical": {
                "What is the square root of 144?": ("12", "This is a basic perfect square."),
                "How many bones are in the adult human body?": ("206", "The adult human skeleton consists of 206 bones."),
                "In which year did World War II end?": ("1945", "World War II ended with Japan's surrender in 1945."),
                "What is the atomic number of Carbon?": ("6", "Carbon has 6 protons in its nucleus."),
                "How many planets are in our solar system?": ("8", "Since 2006, when Pluto was reclassified.")
            }
        }

    def initialize_results_file(self):
        if not results_file.exists():
            with open(results_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Score', 'Percentage', 'Questions_Attempted', 'Date'])

    def get_num_questions(self):
        total_questions = sum(len(q) for q in self.questions_bank.values())
        while True:
            num = gui.integerbox(
                msg=f"How many questions would you like to attempt? (1-{total_questions})",
                title="Select Number of Questions",
                lowerbound=1,
                upperbound=total_questions
            )
            if num is None:
                if gui.ynbox("Do you want to quit?", "Confirm Quit"):
                    sys.exit()
                continue
            return num

    def display_welcome(self):
        # Display welcome message using GUI
        gui.msgbox(
            msg="Welcome to the Quiz Game!\n\nTest your knowledge with a variety of questions!",
            title="Welcome"
        )
        
        # Validate name
        while True:
            self.name = gui.enterbox(
                msg="Please enter your name:",
                title="Quiz Registration"
            )
            if self.name and not self.name.isspace() and len(self.name) >= 2:
                break
            gui.msgbox("Please enter a valid name (at least 2 characters).", "Invalid Input")
        
        # Validate age
        while True:
            age = gui.integerbox(
                msg="Please enter your age:",
                title="Age Verification",
                lowerbound=1,
                upperbound=100
            )
            if age is None:
                if gui.ynbox("Do you want to quit?", "Confirm Quit"):
                    sys.exit()
                continue
            if self.MIN_AGE <= age <= self.MAX_AGE:
                gui.msgbox("Age verified! You can proceed with the quiz.", "Verification Successful")
                break
            gui.msgbox(f"Sorry, this quiz is only for participants aged {self.MIN_AGE}-{self.MAX_AGE}.", "Age Restriction")
            sys.exit()

    def ask_multiple_choice(self, question, answer_data):
        correct_answer, options = answer_data
        random.shuffle(options)
        
        user_answer = gui.buttonbox(
            msg=question,
            title="Multiple Choice Question",
            choices=options
        )
        
        return self.process_answer(question, user_answer, correct_answer)

    def ask_true_false(self, question, answer_data):
        correct_answer, explanation = answer_data
        
        user_answer = gui.buttonbox(
            msg=question,
            title="True/False Question",
            choices=["True", "False"]
        )
        
        is_correct = self.process_answer(question, user_answer, correct_answer)
        gui.msgbox(explanation, "Explanation")
        return is_correct

    def ask_numerical(self, question, answer_data):
        correct_answer, explanation = answer_data
        
        user_answer = gui.enterbox(
            msg=question,
            title="Numerical Question"
        )
        
        is_correct = self.process_answer(question, user_answer, correct_answer)
        gui.msgbox(explanation, "Explanation")
        return is_correct

    def process_answer(self, question, user_answer, correct_answer):
        if user_answer is None:
            if gui.ynbox("Do you want to quit the quiz?", "Confirm Quit"):
                sys.exit()
            return False
            
        if str(user_answer).lower() == str(correct_answer).lower():
            self.correct_answers.append((question, user_answer))
            gui.msgbox("✓ Correct!", "Result")
            return True
        else:
            self.wrong_answers.append((question, user_answer, correct_answer))
            gui.msgbox(f"✗ Incorrect. The correct answer is: {correct_answer}", "Result")
            return False

    def generate_summary(self):
        summary = f"Quiz Summary for {self.name}\n\n"
        summary += f"Score: {self.score}/{self.num_questions} ({self.percentage:.1f}%)\n\n"
        
        summary += "Correct Answers:\n"
        for q, a in self.correct_answers:
            summary += f"✓ {q}\n   Your answer: {a}\n\n"
            
        summary += "Incorrect Answers:\n"
        for q, a, c in self.wrong_answers:
            summary += f"✗ {q}\n   Your answer: {a}\n   Correct answer: {c}\n\n"
            
        gui.textbox("Quiz Summary", "Results", summary)

    def save_results(self):
        """Save quiz results to CSV file."""
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(results_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.name, self.score, self.percentage, self.num_questions, current_date])

    def plot_results_comparison(self):
        """Create and display results comparison graph."""
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

    def run_quiz(self):
        self.initialize_results_file()
        self.display_welcome()
        
        self.num_questions = self.get_num_questions()
        all_questions = []
        
        for q_type, questions in self.questions_bank.items():
            for question, answer_data in questions.items():
                all_questions.append((q_type, question, answer_data))
        
        random.shuffle(all_questions)
        selected_questions = all_questions[:self.num_questions]
        
        for q_type, question, answer_data in selected_questions:
            if q_type == "multiple_choice":
                if self.ask_multiple_choice(question, answer_data):
                    self.score += 1
            elif q_type == "true_false":
                if self.ask_true_false(question, answer_data):
                    self.score += 1
            elif q_type == "numerical":
                if self.ask_numerical(question, answer_data):
                    self.score += 1

        self.percentage = (self.score / self.num_questions) * 100
        self.generate_summary()
        self.save_results()
        self.plot_results_comparison()

def main():
    quiz = QuizGame()
    quiz.run_quiz()

if __name__ == "__main__":
    main()
