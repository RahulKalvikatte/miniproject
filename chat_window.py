
import tkinter as tk
from tkinter import scrolledtext, ttk
import subprocess
import sys
from model import VoiceAssistant

class ChatWindow:
    def __init__(self, root):
        self.root = root
        self.assistant = VoiceAssistant()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Chat with AI")
        self.root.geometry("500x600")

        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12))
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.user_input = tk.Entry(self.root, font=("Arial", 14))
        self.user_input.pack(pady=5, padx=10, fill=tk.X)
        self.user_input.bind("<Return>", lambda event: self.process_user_input())

        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        send_btn = ttk.Button(frame, text="Send", command=self.process_user_input)
        send_btn.pack(side=tk.LEFT, padx=5)

        voice_btn = ttk.Button(frame, text="🎤 Speak", command=self.voice_input)
        voice_btn.pack(side=tk.LEFT, padx=5)

        return_btn = ttk.Button(self.root, text="↩ Return to Assistant", command=self.return_to_main)
        return_btn.pack(pady=5)

    def display_message(self, msg, tag=None):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, msg + "\n", tag)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def process_user_input(self):
        query = self.user_input.get().strip()
        if not query:
            return
        self.display_message(f"You: {query}", "user")
        self.user_input.delete(0, tk.END)

        response = self.assistant.get_response(query)
        self.display_message(f"AI: {response}", "ai")
        self.assistant.speak(response)

    def voice_input(self):
        query = self.assistant.listen()
        if query:
            self.user_input.delete(0, tk.END)
            self.user_input.insert(0, query)
            self.process_user_input()

    def return_to_main(self):
        self.root.destroy()
        subprocess.Popen([sys.executable, "gui.py"])

def main():
    root = tk.Tk()
    app = ChatWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
