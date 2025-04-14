import datetime
import time
import webbrowser
import speech_recognition as sr
from AppOpener import open
import sys
import pyttsx3
import pygetwindow as gw
import psutil
import os
import google.generativeai as genai
from api import genai,model

class VoiceAssistant:
    def __init__(self, wake_word="alexa"):
        self.wake_word = wake_word.lower()

    def initialize_engine(self):
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', engine.getProperty('rate') - 50)
        engine.setProperty('volume', engine.getProperty('volume') + 0.25)
        return engine

    def speak(self, text):
        speaker = self.initialize_engine()
        speaker.say(text)
        speaker.runAndWait()

    def take_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            active_window=gw.getActiveWindowTitle()
            print(active_window)
            if(active_window=="Voice Assistant"):
                return self.listen_command()
            else:
                while True:
                    try:
                        audio = recognizer.listen(source)
                        query = recognizer.recognize_google(audio, language="en-in").lower()
                        if self.wake_word in query:
                            for w in gw.getAllWindows():
                                if "Voice Assistant" not in w.title:
                                    try:
                                        w.minimize()
                                    except:
                                        pass
                            return self.listen_command()
                    except Exception:
                        continue

    def listen_command(self):
        self.speak("listening...")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
            try:
                query = recognizer.recognize_google(audio, language="en-in")
                print(f"User said: {query}")
                return query
            except Exception:
                return ""

    def open_file(self, file_name):
        try:
            for root, _, files in os.walk("C:/"):
                for file in files:
                    if file_name.lower() in file.lower():
                        file_path = os.path.join(root, file)
                        os.startfile(file_path)
                        self.speak(f"Opened {file}")
                        return
            self.speak(f"File {file_name} not found.")
        except Exception as e:
            self.speak(f"Could not open {file_name}. Error: {str(e)}")

    def handle_command(self, display_response):
        command = self.take_command()
        display_response(f"User said: {command}\n")
        if command=="":
               self.speak("please try again ..")
               self.handle_command()
        else:

            if "start" in command:
                open(command[6:])
            elif "open" in command:
                if "file" in command:
                    file_name = command.replace("open file ", "").strip()
                    self.open_file(file_name)
                else:
                    url = command[5:]
                    webbrowser.open(f"https://www.{url}.com")
            elif "play" in command:
                webbrowser.open(f"https://www.youtube.com/results?search_query=play+{command}")
            elif "stop assistant" in command:
                self.speak("Stopping the assistant. Thank you, Sir.")
                sys.exit()
            elif "close" in command:
                app_name = command.replace("close ", "").strip()
                self.close_application(app_name)
            elif "search on google" in command.lower():
                webbrowser.open(f"https://www.google.com/search?q={command}")    

            else:
                response = model.generate_content(command)
                full_text = response.text.strip()

                # Generate a short spoken summary
                summary_prompt = f"Summarize this in one sentence for speaking aloud:\n\n{full_text}"
                summary = model.generate_content(summary_prompt).text.strip()

                self.speak(summary)
                display_response(full_text)


    def close_application(self, app_name):
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if app_name.lower() in process.info['name'].lower():
                try:
                    os.kill(process.info['pid'], 9)
                    self.speak(f"Closed {app_name}")
                    return
                except Exception as e:
                    self.speak(f"Could not close {app_name}. Error: {str(e)}")
                    return
        self.speak(f"{app_name} is not running.")
    
    def start_assistant(self, display_response):
        self.speak("Assistant is ready.")
        
        while True:
            self.handle_command(display_response)