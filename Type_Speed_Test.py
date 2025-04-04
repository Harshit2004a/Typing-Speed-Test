# This is a simple typing speed test application using Tkinter.
# It allows users to select a difficulty level and type a sentence.
# The application calculates the typing speed in words per minute (WPM) and accuracy percentage.
# The code is structured to be user-friendly and visually appealing with a dark theme.
# Code by Harshit Kumar :)

import customtkinter as ctk
import time
import random

# Initialize the modern UI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Accuracy Calculation
def calculate_accuracy(typed_text, reference_text):
    typed_words = typed_text.split()
    reference_words = reference_text.split()
    correct_words = sum(1 for i in range(min(len(typed_words), len(reference_words))) if typed_words[i] == reference_words[i])
    accuracy = (correct_words / max(1, len(reference_words))) * 100
    return correct_words, accuracy

# Sentences for different difficulty levels
SENTENCES = {
    "Easy": ["The sun is shining bright today.", "I love reading books in my free time.", "My dog loves to play in the park."] * 10,
    "Medium": ["The quick brown fox jumps over the lazy dog.", "She decided to take a long walk in the forest.", "Cooking is both an art and a science."] * 10,
    "Hard": ["A comprehensive understanding of history requires deep research.", "Quantum mechanics is a fascinating field.", "Artificial intelligence is transforming industries worldwide."] * 10
}

# Global Variables
difficulty = "Easy"
sentence = random.choice(SENTENCES[difficulty])
start_time = None
timer_running = False
test_completed = False
remaining_time = 60

def change_difficulty(new_difficulty):
    global difficulty, sentence
    difficulty = new_difficulty
    sentence = random.choice(SENTENCES[difficulty])
    sentence_label.configure(text=sentence)

def handle_keypress(event):
    global start_time, timer_running
    if text_entry.get() == "Type here...":
        text_entry.delete(0, "end")
        text_entry.configure(text_color="white")
    if not timer_running:
        start_time = time.time()
        timer_running = True
        countdown()

def handle_enter(event):
    if test_completed:
        restart_test()
    else:
        calculate_speed()

def countdown():
    global remaining_time, timer_running
    if remaining_time > 0 and timer_running:
        remaining_time -= 1
        timer_label.configure(text=f"Time: {remaining_time}s")
        progress.set((60 - remaining_time) / 60)
        root.after(1000, countdown)
    elif remaining_time == 0:
        calculate_speed()

def calculate_speed():
    global test_completed, timer_running
    if start_time is None:
        return  
    timer_running = False
    elapsed_time = 60 - remaining_time
    typed_text = text_entry.get()
    correct_words, accuracy = calculate_accuracy(typed_text, sentence)
    wpm = (len(typed_text.split()) / (elapsed_time / 60)) if elapsed_time > 0 else 0
    cpm = len(typed_text) / (elapsed_time / 60) if elapsed_time > 0 else 0
    mistakes = len(typed_text.split()) - correct_words

    # Hide input fields and show results
    sentence_label.pack_forget()
    text_entry.pack_forget()
    submit_button.pack_forget()
    
    test_completed = True
    restart_button.configure(state="normal", fg_color="#00FF00")

    result_label.configure(text=f"Words Per Minute: {wpm:.2f}\nAccuracy: {accuracy:.2f}%\nTime Taken: {elapsed_time}s\nCharacters Per Minute: {cpm:.2f}\nCorrect Words: {correct_words}\nMistakes: {mistakes}")
    result_label.pack(pady=10)

def restart_test():
    global test_completed, start_time, sentence, timer_running, remaining_time
    test_completed = False
    timer_running = False
    remaining_time = 60
    text_entry.configure(state="normal")
    text_entry.delete(0, "end")
    text_entry.insert(0, "Type here...")
    text_entry.configure(text_color="gray")
    sentence = random.choice(SENTENCES[difficulty])
    sentence_label.pack()
    text_entry.pack()
    submit_button.pack()
    result_label.configure(text="")
    restart_button.configure(state="disabled", fg_color="#444444")
    start_time = None
    timer_label.configure(text="Time: 60s")
    progress.set(0)

# Initialize GUI
root = ctk.CTk()
root.title("Typing Speed Test")
root.geometry("850x600")
root.configure(fg_color="#000000")  # Set entire background to black

title_label = ctk.CTkLabel(root, text="Typing Speed Test", font=("Arial", 28, "bold"), text_color="#00FF00", fg_color="#000000")  # Green text
title_label.pack(pady=10)

# Difficulty Selection
difficulty_label = ctk.CTkLabel(root, text="Select Difficulty:", font=("Arial", 14))
difficulty_label.pack()

difficulty_menu = ctk.CTkComboBox(root, values=["Easy", "Medium", "Hard"], command=change_difficulty)
difficulty_menu.set("Easy")
difficulty_menu.pack(pady=5)

# Sentence Display
sentence_label = ctk.CTkLabel(root, text=sentence, wraplength=750, font=("Arial", 16), fg_color="#222", corner_radius=10, padx=15, pady=10)
sentence_label.pack(pady=20, ipadx=10, ipady=5)

# Typing Entry Box
text_entry = ctk.CTkEntry(root, width=600, font=("Arial", 14), fg_color="#333", text_color="gray")
text_entry.insert(0, "Type here...")
text_entry.pack(pady=10, ipadx=5, ipady=5)
text_entry.bind("<Return>", handle_enter)
text_entry.bind("<KeyPress>", handle_keypress)

# Timer
timer_label = ctk.CTkLabel(root, text="Time: 60s", font=("Arial", 14, "bold"), text_color="#FF4500")
timer_label.pack()

# Progress Bar
progress = ctk.CTkProgressBar(root, width=400)
progress.pack(pady=10)

# Submit Button
submit_button = ctk.CTkButton(root, text="Submit", command=calculate_speed, fg_color="#FF4500", font=("Arial", 14, "bold"))
submit_button.pack(pady=8)

# Restart Button
restart_button = ctk.CTkButton(root, text="Restart", command=restart_test, fg_color="#444444", state="disabled", font=("Arial", 14, "bold"))
restart_button.pack(pady=8)

# Result Display
result_label = ctk.CTkLabel(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

root.mainloop()
