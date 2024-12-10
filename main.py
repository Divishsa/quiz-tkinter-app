import tkinter as tk
from tkinter import messagebox
import json
import random


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("600x400")
        
        self.questions = []
        self.current_question_index = 0
        self.score = 0
        self.round = 1

        self.load_questions("questions.json")
        self.setup_gui()
        self.load_question()

    def load_questions(self, file_path):
        try:
            with open(file_path, "r") as file:
                self.questions = json.load(file)
                random.shuffle(self.questions)  # Shuffle the questions
        except FileNotFoundError:
            messagebox.showerror("Error", "Questions file not found!")
            self.root.destroy()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format!")
            self.root.destroy()

    def setup_gui(self):
        # Question label
        self.question_label = tk.Label(self.root, text="", wraplength=550, font=("Arial", 14))
        self.question_label.pack(pady=20)

        # Options
        self.options_var = tk.StringVar(value="")
        self.options = []
        for i in range(4):
            option = tk.Radiobutton(self.root, text="", variable=self.options_var, value=f"option{i+1}", font=("Arial", 12))
            option.pack(anchor="w", padx=20)
            self.options.append(option)

        # Submit button
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_answer, font=("Arial", 12))
        self.submit_button.pack(pady=20)

    def load_question(self):
        if self.current_question_index < min(10, len(self.questions)):  # Limit to 10 questions
            question = self.questions[self.current_question_index]
            self.question_label.config(text=f"Q{self.current_question_index + 1}: {question['question']}")
            for i, option_text in enumerate(question['options']):
                self.options[i].config(text=option_text, value=option_text.split(".")[0])  # A/B/C/D
            self.options_var.set("")  # Reset the selection
        else:
            self.end_round()

    def submit_answer(self):
        selected_option = self.options_var.get()
        if not selected_option:
            messagebox.showwarning("Warning", "Please select an answer!")
            return

        correct_answer = self.questions[self.current_question_index]["answer"]
        if selected_option == correct_answer:
            self.score += 1

        self.current_question_index += 1
        self.load_question()

    def end_round(self):
        if self.round == 1:
            messagebox.showinfo("Round 1 Over", f"Your score: {self.score}/10")
            if self.score >= 7:
                self.start_next_round()
            else:
                messagebox.showinfo("Quiz Over", "You did not qualify for the next round. Better luck next time!")
                self.root.destroy()
        elif self.round == 2:
            messagebox.showinfo("Quiz Over", f"Your total score: {self.score}/5")
            self.root.destroy()

    def start_next_round(self):
        self.round = 2
        self.current_question_index = 0
        self.score = 0
        self.load_questions("next_round_questions.json")
        self.load_question()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
