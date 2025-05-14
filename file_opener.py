
import os
import speech_recognition 
import pyttsx3

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




def list_files(folder_path):
    files = os.listdir(folder_path)
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
    return files[:10]  

def open_file_by_voice():
    speak("Which folder should I look in? For example, say Desktop, Documents, Pictures, Music, Videos,  or Downloads.")
    folder_name = takeCommand()

    known_folders = {
        "desktop": "C:\\Users\\Deenah Fatima\\OneDrive\\Desktop",
        "documents": "C:\\Users\\Deenah Fatima\\oneDrive\\Documents",
        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        "pictures": "C:\\Users\\Deenah Fatima\\OneDrive\\Pictures",
        "music": "C:\\Users\\Deenah Fatima\\OneDrive\\Music",
        "videos": "C:\\Users\\Deenah Fatima\\OneDrive\\Videos",
        
    }

    

    folder_path = known_folders.get(folder_name)
    if not folder_path or not os.path.exists(folder_path):
        speak("Sorry, I couldn't find that folder.")
        return

    files = list_files(folder_path)
    if not files:
        speak("There are no files in that folder.")
        return

    speak("Here are the files:")
    for idx, file in enumerate(files):
        speak(f"File {idx + 1}: {file}")

    speak("Please say the number of the file you want to open.")
    number_response = takeCommand()

    try:
        file_index = int([s for s in number_response.split() if s.isdigit()][0]) - 1
        if 0 <= file_index < len(files):
            file_path = os.path.join(folder_path, files[file_index])
            speak(f"Opening file: {files[file_index]}")
            os.startfile(file_path)
        else:
            speak("That number is out of range.")
    except:
        speak("Sorry, I couldn't understand the file number.")
