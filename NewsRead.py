import requests
import json
import speech_recognition
import pyaudio  

import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
rate = engine.setProperty("rate",200)

def speak(audio):
    print("Jarvis:", audio)  
    engine.say(audio)
    engine.runAndWait()
    
import speech_recognition as sr

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()


def latestnews():
    api_dict = {"business": f"https://gnews.io/api/v4/top-headlines?token={"16d47039c8fa3d3ce19104ba8c6d7474"}&topic=business&lang=en&country=in",
                 "entertainment": f"https://gnews.io/api/v4/top-headlines?token={"16d47039c8fa3d3ce19104ba8c6d7474"}&topic=entertainment&lang=en&country=in",
                 "health": f"https://gnews.io/api/v4/top-headlines?token={"16d47039c8fa3d3ce19104ba8c6d7474"}&topic=health&lang=en&country=in",
                 "science": f"https://gnews.io/api/v4/top-headlines?token={"16d47039c8fa3d3ce19104ba8c6d7474"}&topic=science&lang=en&country=in",
                 "sports": f"https://gnews.io/api/v4/top-headlines?token={"16d47039c8fa3d3ce19104ba8c6d7474"}&topic=sports&lang=en&country=in",
                 "technology": f"https://gnews.io/api/v4/top-headlines?token={"16d47039c8fa3d3ce19104ba8c6d7474"}&topic=technology&lang=en&country=in",
                }


    content = None
    url = None
    speak("Which field news do you want, [business] , [health] , [technology], [sports] , [entertainment] , [science]")
    field = takeCommand()
    for key ,value in api_dict.items():
        if key.lower() in field.lower():
            url = value
            print(url)
            print("url was found")
            break
        else:
            url = True
    if url is True:
        print("url not found")

    news = requests.get(url).text
    news = json.loads(news)
    speak("Here is the first news.")

    arts = news["articles"]
    for articles in arts :
        article = articles["title"]
        print(article)
        speak(article)
        news_url = articles["url"]
        print(f"for more info visit: {news_url}")

    
        speak("Say 1 to continue or 2 to stop.")
        a = takeCommand()
        if "one" in a or "1" in a:
            pass
        elif "two" in a or "2" in a or "stop" in a:
            break
        else:
                speak("Invalid input. Please say 1 or 2.")