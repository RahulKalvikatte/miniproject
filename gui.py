import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
from PIL import Image, ImageTk
import time
from assistant import VoiceAssistant
import subprocess
import sys

class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.assistant = VoiceAssistant()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Voice Assistant")
        self.root.geometry("800x600")
        self.root.state("zoomed")

        # Background setup
        try:
            self.bg_image = Image.open("chatbot.png").resize(
                (self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS
            )
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)

            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()
        except Exception as e:
            print("Error loading background image:", e)
            self.root.configure(bg="#2c3e50")

        # Header
        self.header_frame = tk.Frame(self.root, bg="#34495e")
        self.header_frame.pack(fill=tk.X, pady=10)

        self.title_label = tk.Label(
            self.header_frame, text="AI Assistant", font=("Helvetica", 28, "bold"), bg="#34495e", fg="white"
        )
        self.title_label.pack(pady=10)

        # Main content area
        self.content_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RIDGE)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Response text area
        self.response_text = scrolledtext.ScrolledText(
            self.content_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 14), bg="#ffffff", fg="#2c3e50",
            borderwidth=3, relief=tk.GROOVE, padx=10, pady=10, height=15
        )
        self.response_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Button Styles
        button_style = ttk.Style()
        button_style.configure('TButton', font=('Helvetica', 14, 'bold'))

        # Start Assistant Button
        self.start_button = ttk.Button(self.root, text="🎤 Start", style='TButton', command=self.start_assistant_thread)
        self.start_button.pack(pady=10, ipadx=30, ipady=10)

        # Ask Question Button
        self.ask_button = ttk.Button(self.root, text="💬 Ask Question", style='TButton', command=self.open_chat_window)
        self.ask_button.pack(pady=10, ipadx=20, ipady=10)

    def display_response(self, message):
        self.response_text.config(state=tk.NORMAL)
        self.response_text.insert(tk.END, message + "\n")
        self.response_text.config(state=tk.DISABLED)
        self.response_text.see(tk.END)

    def start_assistant_thread(self):
        threading.Thread(target=self.run_assistant, daemon=True).start()

    def run_assistant(self):
        self.assistant.start_assistant(self.display_response)

    def open_chat_window(self):
       
        self.root.destroy() 
        subprocess.Popen([sys.executable, "chat_window.py"])

def main():
    root = tk.Tk()
    app = AssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
