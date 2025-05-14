import pywhatkit
import pyttsx3
import datetime
import speech_recognition
import webbrowser
from bs4 import BeautifulSoup
from time import sleep
import os 
from datetime import timedelta
from datetime import datetime

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
rate = engine.setProperty("rate",170)

def speak(audio):
    print("Jarvis:", audio)  
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source,0,4)
        

    try:
        print("Understanding..")
        query  = r.recognize_google(audio,language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query

strTime = int(datetime.now().strftime("%H"))
update = int((datetime.now()+timedelta(minutes = 2)).strftime("%M"))

def sendMessage():
    speak("Who do you want to message? Say Person 1 or Person 2.")
    person = takeCommand().lower()
    if "person 1" in person or "one" in person:
        phone_number = "+919912446657"
    elif "person 2" in person or "two" in person:
        phone_number = "+919397037717"
    else:
        speak("I didn't understand the contact name. Please try again.")
        return

    speak("What's the message?")
    message = takeCommand()
    
    if message == "None":
        speak("Sorry, I didn't catch the message. Please try again.")
        return

    pywhatkit.sendwhatmsg(phone_number, message, time_hour=strTime, time_min=update)
    speak("Message scheduled successfully.")