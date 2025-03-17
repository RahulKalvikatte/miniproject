from logging import exception
import webbrowser
import win32com.client
import os
import speech_recognition as sr
import re
from AppOpener import open
import sys

def takeCommand() :
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold=1
        print("listening")
        audio=recognizer.listen(source)
        try:

            query=recognizer.recognize_google(audio,language="en_in")
            print (f"user said {query}")
            return query
        except Exception as e:
            speaker.Speak("try again ")
            takeCommand()





speaker= win32com.client.Dispatch("SAPI.SpVoice")

if __name__=='__main__':


        
        speaker.Speak("How can i help you ")
        while 1:
            s=takeCommand()
            speaker.Speak(f"s")

            if "start" in s.lower():
                 open(s)

            url =s[5:]
            
            if "open".lower() in s.lower() :
                    url =s[5:]
                    speaker.Speak(f"opening {url} sir")
                    webbrowser.open(f"https://www.{url}.com")


            if "play music".lower() in s.lower():
               webbrowser.open(f"https://www.youtube.com/results?search_query=play+music+")

            if "stop".lower() in s.lower():
                 sys.exit()   
            
        








