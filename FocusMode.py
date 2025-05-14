import subprocess
import psutil
import os
import time
import pyttsx3



APP_PATHS = {
    "chrome": r"C:\Users\Deenah Fatima\OneDrive\Desktop\Google Chrome.lnk",
    "notepad": r"C:\Users\Deenah Fatima\OneDrive\Desktop\Notepad.lnk",
    "paint": r"C:\Users\Deenah Fatima\OneDrive\Desktop\Paint.lnk",
    "amazon":r"C:\Users\Deenah Fatima\OneDrive\Desktop\Amazon.com.lnk",
    "whatsapp":r"C:\Users\Deenah Fatima\OneDrive\Desktop\WhatsApp.lnk",
    
}

closed_apps = []
focus_start_time = None




engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id) 
rate = engine.setProperty("rate",200)  


    
def speak(text):
    print("Jarvis:", text)  
    engine.say(text)
    engine.runAndWait()

def stop_apps(app_names):
    global closed_apps, focus_start_time
    closed_apps = []  # Reset list
    focus_start_time = time.time()
    for app in app_names:
        for proc in psutil.process_iter(['pid', 'name']):
            if app.lower() in proc.info['name'].lower():
                try:
                    subprocess.run(["taskkill", "/F", "/PID", str(proc.info['pid'])], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    closed_apps.append(app)
                    print(f"Closed: {app}")
                    break
                except Exception as e:
                    print(f"Could not close {app}: {e}")

def start_apps():
    global focus_start_time
    for app in closed_apps:
        if app in APP_PATHS:
            try:
                os.startfile(APP_PATHS[app])
                print(f"Reopened: {app}")
                time.sleep(1)
            except Exception as e:
                print(f"Could not reopen {app}: {e}")
    closed_apps.clear()
    
    if focus_start_time:
        duration = round((time.time() - focus_start_time) / 60, 2) 
        save_focus_time(duration)

def save_focus_time(duration):
    try:
        with open("focus.txt", "a") as file:
            file.write(f"{duration},")
        print(f"Focus session recorded: {duration} minutes")
    except Exception as e:
        print(f"Error writing to file: {e}")

def show_focus_graph():
    try:
        with open("focus.txt", "r") as file:
            content = file.read().strip(",").split(",")
            values = [float(val) for val in content]
        last_focus = values[-1] if values else 0
        speak(f"You focused for {last_focus} minutes in your last session.")
        
    except Exception as e:
        print(f"Could not generate graph: {e}")

