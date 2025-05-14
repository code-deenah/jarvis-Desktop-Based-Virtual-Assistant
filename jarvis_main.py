import datetime
import pyttsx3  
import speech_recognition 
import requests
import os
import random
from bs4 import BeautifulSoup
import webbrowser
from plyer import notification
from pygame import mixer
import sys



import google.generativeai as genai
genai.configure(api_key="AIzaSyCZMO1z3A6g5kTw10N9NVg6MBIIpYpb4_s")  
model = genai.GenerativeModel("gemini-1.5-flash")



for i in range(3):
    a = input("Enter Password to open Jarvis :- ")
    pw_file = open("password.txt","r")
    pw = pw_file.read()
    pw_file.close()
    if (a==pw):
        print("WELCOME DEENAH ! PLZ SPEAK [WAKE UP] TO LOAD ME UP")
        break
    elif (i==2 and a!=pw):
        exit()

    elif (a!=pw):
        print("Try Again")
        

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
        r.pause_threshold = 5   
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




def alarm(query):
    timehere = open("Alarmtext.txt","a")
    timehere.write(query)
    timehere.close()
    os.startfile("alarm.py")
    

    
        
    
def get_gemini_response(query):
    try:
        response = model.generate_content(query)  
        return response.text if response and hasattr(response, "text") else "I'm sorry, I couldn't process that request."
    except Exception as e:
        print(f"Error getting Gemini response: {e}")
        return "I'm sorry, I couldn't process that request."
        


def run_jarvis():
    while True:
        query = takeCommand().lower()
        if "wake up" in query:
            from GreetMe import greetMe
            greetMe()
            while True:
                query = takeCommand().lower()
                if "go to sleep" in query:
                    speak("Ok Deenah, You can call me anytime")
                    break
                
            
                elif "change password" in query:
                    speak("What's the new password")
                    new_pw = takeCommand().lower()
                    new_password = open("password.txt","w")
                    new_password.write(new_pw)
                    new_password.close()
                    speak("Done DEENAH")
                    speak(f"Your new password is  {new_pw}")
                    
                    
                elif "schedule my day" in query:
                    tasks = []  
                    speak("Do you want to clear old tasks? Please say Yes or No.")
                    query = takeCommand().lower()

                    if "yes" in query:
                        with open("tasks.txt", "w") as file:
                            file.write("")
                        speak("How many tasks do you want to schedule?")
                        try:
                            task_count = int(takeCommand().lower())
                        except:
                            speak("Sorry, I couldn't understand the number. Please try again later.")
                            task_count = 0

                        for i in range(task_count):
                            speak(f"Please tell me task number {i + 1}")
                            task = takeCommand()
                            tasks.append(task)
                            with open("tasks.txt", "a") as file:
                                file.write(f"{i+1}. {task}\n")

                    elif "no" in query:
                        speak("How many new tasks do you want to add?")
                        try:
                            task_count = int(takeCommand().lower())
                        except:
                            speak("Sorry, I couldn't understand the number. Please try again later.")
                            task_count = 0

                        for i in range(task_count):
                            speak(f"Please tell me task number {i + 1}")
                            task = takeCommand()
                            tasks.append(task)
                            with open("tasks.txt", "a") as file:
                                file.write(f"{i+1}. {task}\n")

                    speak("Your tasks have been saved.")

                
                elif "show my schedule" in query:
                    file = open("tasks.txt","r")
                    content = file.read()
                    file.close()
                    mixer.init()
                    mixer.music.load("notification.mp3.wav")
                    mixer.music.play()
                    
                    notification.notify(
                       title = "My schedule :-",
                       message = content,
                       timeout = 15
                       )
                    
                    

                elif "start focus mode" in query:
                    import FocusMode
                    speak("Focus mode activated. Which apps do you want to stop?")
                    app_query = takeCommand().lower()

                    apps_to_stop = []
                    for app_key in FocusMode.APP_PATHS.keys():
                        if app_key in app_query:
                            apps_to_stop.append(app_key)

                    if apps_to_stop:
                        FocusMode.stop_apps(apps_to_stop)
                        speak("The selected apps have been stopped.")
                    else:
                        speak("I couldn't identify any apps to stop.")

                elif "stop focus mode" in query:
                    FocusMode.start_apps()
                    speak("Focus mode exited. Apps have been reopened.")


                    
                    
                elif "show my focus" in query:
                    from FocusMode import show_focus_graph
                    show_focus_graph()
                    
                    
                
                elif "open" in query:   
                    import pyautogui
                    query = query.replace("open","")
                    query = query.replace("jarvis","")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter")   
                 
                 
                
                
                elif "internet speed" in query:
                    try:
                
                        original_stdout = sys.stdout
                        sys.stdout = sys.__stdout__

                        import speedtest
                        wifi = speedtest.Speedtest()
                        wifi.get_best_server()

                        upload_net = round(wifi.upload() / 1048576.0, 2)            
                        download_net = round(wifi.download() / 1048576.0, 2)

                        # Restore GUI stdout
                        sys.stdout = original_stdout

                        print("Wifi Upload Speed is", upload_net, "Mbps")
                        print("Wifi Download Speed is", download_net, "Mbps")
                        speak(f"Wifi download speed is {download_net} megabits per second")
                        speak(f"Wifi upload speed is {upload_net} megabits per second")

                    except Exception as e:
                        sys.stdout = original_stdout
                        print("⚠️ Error measuring internet speed:", e)
                        speak("Sorry, I couldn't check the internet speed right now.")

              
                

                elif "search my location" in query.lower():
                    from LocationFinder import get_country
                    get_country()
                    
                elif "search a file" in query:
                    from file_opener import open_file_by_voice
                    open_file_by_voice()

                elif "check my email" in query:
                    from mail_access import check_email
                    check_email()

                elif "reply to an email" in query:
                    from mail_access import reply_email
                    reply_email()





                elif "play a game" in query:
                    from game import game_play
                    game_play()

                elif "screenshot" in query:
                     import pyautogui 
                     im = pyautogui.screenshot()
                     im.save("ss.jpg")

                elif "click my photo" in query:
                    import pyautogui
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(2)
                    speak("SMILE")
                    pyautogui.press("enter")
                             
                             
                
                
                elif "hello" in query:
                    speak("Hello Deenah, how are you ?")
                elif "i am fine" in query:
                    speak("that's great, Deenah")
                elif "how are you" in query:
                    speak("Perfect, Deenah")
                elif "thank you" in query:
                    speak("you are welcome, Deenah")
               
               
                elif "tired" in query:
                    speak("Playing your favourite songs, Deenah")
                    a = (1,2,3) 
                    b = random.choice(a)
                    if b==1:
                        webbrowser.open('https://www.youtube.com/watch?v=EatzcaVJRMs')
                    elif b==2:
                        webbrowser.open('https://www.youtube.com/watch?v=2208Hn9LyUA')
                    elif b==3:
                        webbrowser.open('https://www.youtube.com/watch?v=wTgrZE9RWNY')
                
                elif "video" in query or "mute" in query or "unmute" in query:
                        from youtube_controls import control_youtube
                        control_youtube(query)

                    
                elif "volume up" in query:
                     from keyboard import volumeup
                     speak("Turning volume up,Deenah")
                     volumeup()
                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, Deenah")
                    volumedown()
            
                    
                elif "open" in query:
                 from Dictapp import openappweb
                 openappweb(query)
                elif "close" in query:
                 from Dictapp import closeappweb
                 closeappweb(query)
    
                elif "google" in query:
                  from SearchNow import searchGoogle
                  searchGoogle(query)
                elif "youtube" in query:
                   from SearchNow import searchYoutube
                   searchYoutube(query)
                elif "wikipedia" in query:
                   from SearchNow import searchWikipedia
                   searchWikipedia(query)
                   
                   
                elif "news" in query:
                    from NewsRead import latestnews
                    latestnews()
                    
                    
                elif "calculate" in query:
                    from Calculatenumbers import WolfRamAlpha
                    from Calculatenumbers import Calc
                    query = query.replace("calculate","")
                    query = query.replace("jarvis","")
                    Calc(query)
                    
                    
                elif "whatsapp" in query:
                     from Whatsapp import sendMessage  #individual msgs
                     sendMessage()
                   
                
                
                   
                elif "weather report" in query:
                    from weather import weather_assistant
                    weather_assistant()

                

                   
                elif "set an alarm" in query:
                    print("input time example:- 10 and 10 and 10")
                    speak("Set the time")
                    a = takeCommand()
                    alarm(a)
                    speak("Done, Deenah")
                   
                   
                elif "the time" in query:
                 strTime = datetime.datetime.now().strftime("%H:%M")    
                 speak(f"Deenah, the time is {strTime}")
                 
                elif "the date" in query:
                    strDate = datetime.datetime.now().strftime("%A, %B %d, %Y")
                    speak(f"Deenah, today's date is {strDate}")

                 
                elif "finally sleep" in query:
                 speak("Going to sleep,Deenah")
                 exit()
                 
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that","")
                    rememberMessage = query.replace("jarvis","")
                    speak("You told me to remember that"+rememberMessage)
                    remember = open("Remember.txt","a")
                    remember.write(rememberMessage)
                    remember.close()
                    
                elif "what do you remember" in query:
                    remember = open("Remember.txt","r")
                    speak("You told me " + remember.read())
                    
                elif "shutdown the system" in query:
                    speak("Are You sure you want to shutdown")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                    if shutdown == "yes":
                        os.system("shutdown /s /t 1")

                    elif shutdown == "no":
                           break
                       
                else:

                    gemini_response = get_gemini_response(query)
                    
                    if gemini_response:
                        gemini_response = gemini_response.replace("*", "") 
                        lines = gemini_response.strip().split("\n")[:2]  
                        trimmed_response = "\n".join(lines)

                        if trimmed_response != "I'm sorry, I couldn't process that request.":
                         speak(trimmed_response) 
                         

if __name__ == "__main__":
    run_jarvis()
