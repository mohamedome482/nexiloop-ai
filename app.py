import tkinter as tk
from tkinter import ttk
import google.generativeai as genai 

genai.configure(api_key="your-api")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat()

def send_message(event=None):
    user_message = user_input.get()
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "User: " + user_message + "\n", "user")
    try:
        response = convo.send_message(user_message)
        chat_log.insert(tk.END, "Nexiloop AI: " + response.text + "\n", "model")
    except genai.StopCandidateException as e:
        chat_log.insert(tk.END, "AI: Conversation has finished with reason: " + e.finish_reason + "\n", "model")
    chat_log.config(state=tk.DISABLED)
    user_input.delete(0, tk.END)

root = tk.Tk()
root.title("Chat Interface")
root.geometry("600x450")
root.configure(bg="#121212")

# Chat Labels
chat_label = tk.Label(root, text="nexiloop ai", fg="white", bg="#121212", font=("Helvetica", 20, "bold"))
chat_label.place(x=20, y=10)

# Chat Log
chat_log = tk.Text(root, fg="white", bg="#212121", wrap=tk.WORD, font=("Helvetica", 12), padx=10, pady=10)
chat_log.tag_configure("user", foreground="white")
chat_log.tag_configure("model", foreground="white")
chat_log.insert(tk.END, "User: hi\n", "user")
chat_log.insert(tk.END, "Nexiloop AI: Hello! I am Nexiloop AI. How can I help you today?\n", "model")
chat_log.config(state=tk.DISABLED)
chat_log.place(x=20, y=50, width=560, height=300)

# Input Field
user_input = ttk.Entry(root, font=("Helvetica", 12))
user_input.place(x=20, y=370, width=480, height=30)
user_input.insert(0, "Type something")
user_input.bind("<Return>", send_message)

# Send Button
send_button = ttk.Button(root, text="Send", command=send_message)
send_button.place(x=510, y=370, width=70, height=30)

root.mainloop()
