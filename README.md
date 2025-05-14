# jarvis-Desktop-Based-Virtual-Assistant
JARVIS (Just A Rather Very Intelligent System) - A Personal Desktop Assistant with Chatbot Integration, an 
intelligent virtual assistant designed to operate on Windows desktops. Jarvis combines both voice and text-based 
interaction to offer a versatile and user-friendly experience. The system is built using Python and integrates 
technologies such as speech recognition, text-to-speech synthesis, machine learning-based intent recognition, and 
generative AI through the Gemini API. 
The assistant is accessible via a custom-built Tkinter graphical user interface (GUI) that features animated visuals, 
a user authentication system with profile and avatar selection, and two primary interaction modes: Jarvis Mode 
(voice-based) and Chatbot Mode (text-based). Jarvis Mode listens for voice commands and performs actions such 
as launching or closing applications, checking emails, managing tasks, playing media, conducting web searches, 
executing utility functions like alarms and screenshots, and interacting with online services like YouTube, Google, 
and Wikipedia. If a query does not match predefined commands, it is forwarded to Gemini for an intelligent 
response. 
The Chatbot Mode uses a Scikit-learn-based Naive Bayes model trained on custom intents defined in a JSON file. 
It predicts user intent from text input and generates responses accordingly. The GUI manages both modes through 
dedicated controls and logs all interactions in real-time. 
This hybrid architecture ensures flexibility, responsiveness, and continuous usability. The integration of machine 
learning and generative AI within a desktop assistant highlights the project's focus on enhancing human-computer 
interaction and productivity through intelligent automat
