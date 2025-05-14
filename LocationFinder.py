
import geocoder
import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 200)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def get_country():
    try:
        g = geocoder.ip('me')
        country = g.country
        if country:
            speak(f"You are in {country}.")
        else:
            speak("Sorry, I couldn't determine your country.")
    except Exception as e:
        speak("An error occurred while trying to get your location.")
        print(f"[Location Error] {e}")
