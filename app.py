import tkinter as tk
import google.generativeai as genai
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from tkinter import ttk
import speech_recognition as sr
import threading
import random
from gtts import gTTS
import os

# Configure GenerativeAI
genai.configure(api_key="your api")
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(
    model_name="gemini-1.0-pro-001",
    generation_config=generation_config,
    safety_settings=safety_settings,
)
convo = model.start_chat()

# Function to send message and receive response
def send_message(event=None):
    user_message = user_input.get()
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "You: " + user_message + "\n", "user")
    response_text = get_response(user_message)
    chat_log.insert(tk.END, "Nexiloop AI: " + response_text + "\n", "model")
    speak(response_text)
    chat_log.config(state=tk.DISABLED)
    user_input.delete(0, tk.END)

# Function to get response from the AI
def get_response(user_message):
    user_message = user_message.lower()
    if "who create you" in user_message or "who made you" in user_message:
        return "I was created by Nexiloop AI and Mohamed Rayen."
    elif "who are you" in user_message:
        return "I am Nexiloop AI, trained by Nexiloop and Mohamed Rayen."
    else:
        try:
            response = convo.send_message(user_message)
            return response.text
        except genai.StopCandidateException as e:
            return "Conversation finished: " + e.finish_reason

# Function to clear chat log
def clear_chat():
    chat_log.config(state=tk.NORMAL)
    chat_log.delete(1.0, tk.END)
    chat_log.config(state=tk.DISABLED)

# Function to save chat history to a file
def save_chat():
    filename = fd.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        with open(filename, "w") as file:
            chat_content = chat_log.get(1.0, tk.END)
            file.write(chat_content)
        mb.showinfo("Success", "Chat history saved successfully.")

# Function to load chat history from a file
def load_chat():
    filename = fd.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        with open(filename, "r") as file:
            chat_content = file.read()
            chat_log.config(state=tk.NORMAL)
            chat_log.delete(1.0, tk.END)
            chat_log.insert(tk.END, chat_content)
            chat_log.config(state=tk.DISABLED)
        mb.showinfo("Success", "Chat history loaded successfully.")

# Function to exit the application
def exit_app():
    if mb.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# Function to change the chat theme
def change_theme():
    color = fd.askcolor()[1]
    root.configure(bg=color)
    chat_log.config(bg=color)
    user_input.config(bg=color)

# Function for voice input using SpeechRecognition library
def voice_input():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something...")
        audio = r.listen(source)

    try:
        user_message = r.recognize_google(audio)
        user_input.delete(0, tk.END)
        user_input.insert(tk.END, user_message)
        send_message()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Function to suggest random emojis
def suggest_emoji():
    emojis = ["😊", "🎉", "👍", "😂", "🤔", "😎", "🥳", "👏"]
    random_emoji = random.choice(emojis)
    user_input.insert(tk.END, random_emoji)

# Function to generate a random joke
def generate_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What did one plate say to the other plate? Dinner's on me!",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
    ]
    random_joke = random.choice(jokes)
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "Nexiloop AI: " + random_joke + "\n", "model")
    speak(random_joke)

# Function to make the AI speak
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    os.system("mpg321 temp.mp3")

# Initialize tkinter window
root = tk.Tk()
root.title("Chat Interface")
root.geometry("800x600")
root.configure(bg="#121212")

# Chat Label
chat_label = tk.Label(root, text="Nexiloop AI", fg="white", bg="#121212", font=("Helvetica", 20, "bold"))
chat_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

# Chat Log
chat_log = tk.Text(root, fg="white", bg="#212121", wrap=tk.WORD, font=("Helvetica", 12), padx=10, pady=10)
chat_log.tag_configure("user", foreground="white")
chat_log.tag_configure("model", foreground="white")
chat_log.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

# Scrollbar for Chat Log
scrollbar = ttk.Scrollbar(root, orient="vertical", command=chat_log.yview)
scrollbar.grid(row=1, column=1, sticky="ns")
chat_log.configure(yscrollcommand=scrollbar.set)

# Input Field
user_input = ttk.Entry(root, font=("Helvetica", 12))
user_input.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

# Send Button
send_button = ttk.Button(root, text="Send", command=send_message)
send_button.grid(row=2, column=1, padx=10, pady=10)

# Clear Button
clear_button = ttk.Button(root, text="Clear", command=clear_chat)
clear_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

# Save Button
save_button = ttk.Button(root, text="Save", command=save_chat)
save_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

# Load Button
load_button = ttk.Button(root, text="Load", command=load_chat)
load_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

# Exit Button
exit_button = ttk.Button(root, text="Exit", command=exit_app)
exit_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# Change Theme Button
theme_button = ttk.Button(root, text="Change Theme", command=change_theme)
theme_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# Voice Input Button
voice_button = ttk.Button(root, text="Voice Input", command=voice_input)
voice_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# Emoji Suggestion Button
emoji_button = ttk.Button(root, text="Suggest Emoji", command=suggest_emoji)
emoji_button.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# Joke Generator Button
joke_button = ttk.Button(root, text="Generate Joke", command=generate_joke)
joke_button.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# Credits Label
credits_label = tk.Label(root, text="Powered by Nexiloop AI", fg="white", bg="#121212", font=("Helvetica", 10))
credits_label.grid(row=8, column=0, columnspan=3, padx=20, pady=5, sticky="e")

# Function to send message when "Enter" key is pressed
def on_enter(event):
    send_message()

# Bind the "Enter" key to the send_message function
root.bind("<Return>", on_enter)

root.mainloop()
