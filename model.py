import speech_recognition as sr
import pyttsx3
import api

from api import genai,model

class VoiceAssistant:

    def init_speaker(self):
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  
        engine.setProperty('rate', 170)
        return engine

    def speak(self, text):
        speaker=self.init_speaker()
        speaker.say(text)
        speaker.runAndWait()

    def get_response(self, prompt):
        try:
            response = model.generate_content(prompt)
            return response.text.strip() if response.text else "No response received."
        except Exception as e:
            return f"Gemini Error: {e}"

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("I'm listening...")
            try:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                return recognizer.recognize_google(audio, language="en-in")
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that.")
            except sr.WaitTimeoutError:
                self.speak("No voice input detected.")
            except Exception as e:
                self.speak(f"Error: {e}")
        return ""
