import wolframalpha
import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
rate = engine.setProperty("rate",200)

def speak(audio):
    print("Jarvis:", audio)  
    engine.say(audio)
    engine.runAndWait()


def WolfRamAlpha(query):
    apikey = "AUGTGK-R658K728RT"
    requester = wolframalpha.Client(apikey)
    requested = requester.query(query)

    try:
        answer = next(requested.results).text
        return answer
    except:
        speak("The value is not answerable")
        return None

def Calc(query):
    Term = str(query)
    Term = Term.replace("jarvis","")
    Term = Term.replace("multiply","*")
    Term = Term.replace("plus","+")
    Term = Term.replace("minus","-")
    Term = Term.replace("divide","/")


    Final = str(Term)
    try:
        result = WolfRamAlpha(Final)
        if result:
            print(f"Result: {result}")
            speak(f"The result is {result}")
        else:
            print("No answer found.")
    except:
        speak("The value is not answerable")

