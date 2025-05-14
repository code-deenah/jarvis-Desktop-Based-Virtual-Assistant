import pyttsx3
import datetime

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate",200)

def speak(audio):
    print("Jarvis:", audio)  
    engine.say(audio)
    engine.runAndWait()


def greetMe():
    hour  = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning,Deenah")
    elif hour >12 and hour<=18:
        speak("Good Afternoon ,Deenah")

    else:
        speak("Good Evening,Deenah")

    speak("Please tell me, How can I help you ?")
