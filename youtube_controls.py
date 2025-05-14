
import pyttsx3
import pyautogui

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  
rate = engine.setProperty("rate",200)  


    
def speak(audio):
    print("Jarvis:", audio)  
    engine.say(audio)
    engine.runAndWait()





def control_youtube(action):
    key_map = {
        "pause video": "k",
        "play video": "k",
        "mute": "m",
        "unmute": "m",
        "next video": "shift+n",
        "previous video": "shift+p",
    }

    if action in key_map:
        keys = key_map[action].split("+")
        if len(keys) == 2:
            pyautogui.hotkey(keys[0], keys[1])
        else:
            pyautogui.press(keys[0])
        
        if action in ["pause video", "play video"]:
            speak("Video played" if action == "play video" else "Video paused")
        elif action in ["mute", "unmute"]:
            speak("Video muted" if action == "mute" else "Video unmuted")
        elif action == "next video":
            speak("Playing next video")
        elif action == "previous video":
            speak("Playing previous video")
    else:
        speak("Sorry, I don't recognize that YouTube command.")
