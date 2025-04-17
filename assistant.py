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
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from api import genai, model

class VoiceAssistant:
    def __init__(self, wake_word="alexa"):
        self.wake_word = wake_word.lower()
        self.vosk_model_path = "models/vosk-model-small-en-us-0.15"
        self.vosk_model = None
        self.q = queue.Queue()

        if os.path.exists(self.vosk_model_path):
            self.vosk_model = Model(self.vosk_model_path)

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

    def detect_hotword(self):
        if not self.vosk_model:
            return

        def callback(indata, frames, time_info, status):
            if status:
                print(status)
            self.q.put(bytes(indata))

        try:
            device_info = sd.query_devices(None, 'input')
            samplerate = int(device_info['default_samplerate'])

            with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                                   channels=1, callback=callback):
                rec = KaldiRecognizer(self.vosk_model, samplerate)
                

                while True:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text = result.get("text", "").lower()
                        if self.wake_word in text:
                            
                            return
        except Exception as e:
            print(f"[Hotword detection error] {e}")

    def listen_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)
            try:
                query = recognizer.recognize_google(audio, language="en-in")
                print(f"[Google Recognized] {query}")
                return query
            except Exception:
                return ""

    def listen_offline_command(self):
        if not self.vosk_model:
            return ""

        def callback(indata, frames, time_info, status):
            if status:
                print(status)
            self.q.put(bytes(indata))

        try:
            commands = [
                "open", "close", "stop", "exit", "what is your name", "who made you",
                "what can you do", "how are you", "time", "date", "open file"
            ]

            device_info = sd.query_devices(None, 'input')
            samplerate = int(device_info['default_samplerate'])

            with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                                channels=1, callback=callback):
                rec = KaldiRecognizer(self.vosk_model, samplerate, json.dumps(commands))
                print("Listening (offline)...")
                self.speak("Say your command")

                collected = b''
                timeout = time.time() + 8  # Listen up to 8 seconds

                while time.time() < timeout:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text = result.get("text", "").strip()
                        if text:
                            print(f"[Offline Command] {text}")
                            return text
                # Final partial result
                result = json.loads(rec.FinalResult())
                return result.get("text", "").strip()

        except Exception as e:
            print(f"[Offline listen error] {e}")
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

    def is_online(self):
        try:
            import urllib.request
            urllib.request.urlopen("https://www.google.com", timeout=2)
            return True
        except:
            return False

    def handle_offline_command(self, command, display_response):
        command = command.lower()

        if "what is your name" in command:
            response = "I am your voice assistant."
        elif "who made you" in command:
            response = "I was created by my developer using Python."
        elif "what can you do" in command:
            response = "I can open apps, files, tell time and date, and help you offline."
        elif "how are you" in command:
            response = "I’m always ready to help."
        elif "time" in command:
            response = datetime.datetime.now().strftime("It's %I:%M %p.")
        elif "date" in command:
            response = datetime.datetime.now().strftime("Today is %A, %d %B %Y.")
        elif "stop" in command or "exit" in command:
            self.speak("Stopping the assistant. Goodbye!")
            sys.exit()
        elif "open" in command:
            app = command.replace("open ", "").strip()
            self.speak(f"Opening {app}")
            open(app)
            return
        elif "open file" in command:
            file_name = command.replace("open file", "").strip()
            self.open_file(file_name)
            return
        elif "close" in command:
            app_name = command.replace("close", "").strip()
            self.close_application(app_name)
            return
        else:
            response = "Sorry, I didn't understand that command offline."

        self.speak(response)
        display_response(f"[Offline] {response}")

    def handle_command(self, display_response):
        self.detect_hotword()
        self.speak("I'm listening...")

        if self.is_online():
            command = self.listen_command()
        else:
            command = self.listen_offline_command()

        display_response(f"User said: {command}\n")

        if not command:
            self.speak("Please try again...")
            return

        if not self.is_online():
            self.handle_offline_command(command, display_response)
            return

        if "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {now}")
        elif "date" in command:
            today = datetime.datetime.now().strftime("%A, %d %B %Y")
            self.speak(f"Today is {today}")
        elif "start" in command:
            open(command[6:])
        elif "open" in command:
            if "file" in command:
                file_name = command.replace("open file ", "").strip()
                self.open_file(file_name)
            else:
                url = command.replace("open ", "").strip()
                webbrowser.open(f"https://www.{url}.com")
        elif "play" in command:
            webbrowser.open(f"https://www.youtube.com/results?search_query=play+{command}")
        elif "stop assistant" in command:
            self.speak("Stopping the assistant. Thank you, Sir.")
            sys.exit()
        elif "close" in command:
            app_name = command.replace("close ", "").strip()
            self.close_application(app_name)
        elif "search on google" in command:
            search_query = command.replace("search on google", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        else:
            try:
                response = model.generate_content(command)
                full_text = response.text.strip()
                summary_prompt = f"Summarize this in one sentence for speaking aloud:\n\n{full_text}"
                summary = model.generate_content(summary_prompt).text.strip()
                self.speak(summary)
                display_response(full_text)
            except Exception:
                self.handle_offline_command(command, display_response)

    def start_assistant(self, display_response):
        self.speak("Assistant is ready.")
        while True:
            self.handle_command(display_response)