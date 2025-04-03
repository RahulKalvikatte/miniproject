import tkinter as tk
from tkinter import scrolledtext, ttk
import subprocess
import sys

class ChatWindow:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Chat with AI")
        self.root.geometry("500x600")

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12))
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # User input field
        self.user_input = tk.Entry(self.root, font=("Arial", 14))
        self.user_input.pack(pady=5, padx=10, fill=tk.X)

        # Send button
        send_button = ttk.Button(self.root, text="Send", command=self.process_user_input)
        send_button.pack(pady=5)

        # Return button
        return_button = ttk.Button(self.root, text="↩ Return to Assistant", command=self.return_to_main)
        return_button.pack(pady=5)

    def process_user_input(self):
        """Handles user input in the chat window."""
        user_text = self.user_input.get().strip()
        if user_text:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"You: {user_text}\n", "user")
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)
            self.user_input.delete(0, tk.END)

            # Simulating AI response
            response = f"AI: I'm thinking about '{user_text}'..."
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, response + "\n", "ai")
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)

    def return_to_main(self):
        """Closes the chat window and returns to the main assistant."""
        self.root.destroy()  # Close chat window
        subprocess.Popen([sys.executable, "main.py"])  # Open main assistant

def main():
    root = tk.Tk()
    app = ChatWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
