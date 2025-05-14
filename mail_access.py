
import webbrowser
import pyttsx3
import speech_recognition 
import time

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

def check_email():
    speak("Opening Gmail.")
    webbrowser.open("https://mail.google.com/")
    time.sleep(2)

def reply_email():
    speak("To whom should I send the email? Please say the email address.")
    recipient = takeCommand().replace(" ", "").replace("at", "@").replace("dot", ".")
    
    speak("What should be the subject?")
    subject = takeCommand()
    
    speak("What message do you want to send?")
    message = takeCommand()


    mailto_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={recipient}&su={subject}&body={message}"
    webbrowser.open(mailto_url)
    speak("Composing your email.")

