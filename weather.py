import requests
import pyttsx3
import speech_recognition 

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  
rate = engine.setProperty("rate",200)  


    
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
        audio = r.listen(source, 0, 4)

    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")  
    except Exception as e:
        print("Say that again")
        return "None"
    return query

def get_weather(city, country):
    api_key = "44d1cba428ae376afe9a1321a4be221c"  
    location = f"{city},{country}"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        weather_description = data["weather"][0]["description"]
        return f"The temperature in {city}, {country} is {temperature}°C with {weather_description}."
    else:
        return "I couldn't find that location."

def weather_assistant():
    speak("Which country do you want the weather for?")
    country = takeCommand()
    if not country:
        return

    speak(f"And which city or state in {country}?")
    city = takeCommand()
    if not city:
        return

    weather_info = get_weather(city, country)
    print(weather_info)
    speak(weather_info)


