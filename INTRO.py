import os
import tkinter as tk
import threading
import sys
from PIL import Image, ImageTk, ImageSequence
import time
from chatbot import get_response
from jarvis_main import run_jarvis

import json
from tkinter import filedialog, messagebox

USER_DB = "users.json"

def load_users():
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)



class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):
        pass
    
    
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        
        self.root.resizable(True, True)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        
        bg_image = Image.open("bg4.jpg")
        bg_image = bg_image.resize((screen_width, screen_height))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)


    

        self.label = tk.Label(root, text="Jarvis Login", font=("Arial", 40), bg="white", fg="navy")
        self.label.pack(pady=(100,50))
        

        self.username_entry = tk.Entry(root, width=30)
        tk.Label( text="Profile ID", fg="white", bg="black", width=20 , height=2).pack()
        self.username_entry.insert(0, "")
        self.username_entry.pack(pady=20)

        self.password_entry = tk.Entry(root, width=30, show="*")
        tk.Label(text="Password", fg="white", bg="black", width=20, height=2).pack()
        self.password_entry.insert(0, "")
        self.password_entry.pack(pady=20)

        self.login_btn = tk.Button(root, text="Login", command=self.login, bg="green", fg="white", width=20, height=2)
        self.login_btn.pack(pady=10)
        self.message_label = tk.Label(root, text="", bg="black", fg="red")
        self.message_label.pack(pady=10)

        self.signup_btn = tk.Button(root, text="Create Account", command=self.open_signup, bg="black", fg="cyan" ,width=30, height=3)
        self.signup_btn.pack(pady=10)


    def login(self):
        profile_id = self.username_entry.get()
        password = self.password_entry.get()
        users = load_users()

        if profile_id in users and users[profile_id]["password"] == password:
            messagebox.showinfo("Success", "Login Successful!")

           

            self.root.destroy()
            root = tk.Tk()
            root.selected_avatar_path = users[profile_id].get("avatar", "")
            app = JarvisGUI(root)
            root.mainloop()
        else:
            self.message_label.config(text="Incorrect Profile ID or Password!", fg="red")





    def open_signup(self):
        self.signup_window = tk.Toplevel(self.root)
        self.signup_window.title("Sign Up")
    
        self.signup_window.resizable(True, True)

        screen_width = self.signup_window.winfo_screenwidth()
        screen_height = self.signup_window.winfo_screenheight()
        self.signup_window.geometry(f"{screen_width}x{screen_height}")

        bg_image = Image.open("bg6.jpg")
        bg_image = bg_image.resize((screen_width, screen_height))
        self.bg_photo_signup = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self.signup_window, image=self.bg_photo_signup)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()

        signup_label = tk.Label(self.signup_window, text="Jarvis Sign Up", font=("Arial", 40), bg="white", fg="navy")
        signup_label.pack(pady=(60, 30))

        
        form_frame = tk.Frame(self.signup_window, bg="black")
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        
        tk.Label(self.signup_window, text="Name", fg="white", bg="black").pack()
        self.name_entry = tk.Entry(self.signup_window, width=30)
        self.name_entry.pack(pady=5)

        tk.Label(self.signup_window, text="Profile ID", fg="white", bg="black").pack()
        self.profile_id_entry = tk.Entry(self.signup_window, width=30)
        self.profile_id_entry.pack(pady=5)

        tk.Label(self.signup_window, text="Description", fg="white", bg="black").pack()
        self.desc_entry = tk.Entry(self.signup_window, width=30)
        self.desc_entry.pack(pady=5)

        tk.Label(self.signup_window, text="Password", fg="white", bg="black").pack()
        self.pass_entry = tk.Entry(self.signup_window, width=30, show="*")
        self.pass_entry.pack(pady=5)

        tk.Label(self.signup_window, text="Confirm Password", fg="white", bg="black").pack()
        self.confirm_pass_entry = tk.Entry(self.signup_window, width=30, show="*")
        self.confirm_pass_entry.pack(pady=5)



        self.avatar_path = ""
        tk.Button(self.signup_window, text="Choose Avatar", command=self.select_avatar, bg= "black", fg= "cyan").pack(pady=5)

        tk.Button(self.signup_window, text="Submit", command=self.create_account, bg="green", fg="white").pack(pady=20)

    def select_avatar(self):
        self.avatar_selection_window = tk.Toplevel(self.root)
        self.avatar_selection_window.title("Choose Your Avatar")
        self.avatar_selection_window.geometry("400x400")
        self.avatar_selection_window.configure(bg="white")

        avatar_files = [f"avatar{i}.png" for i in range(1, 10)]
        self.avatar_images = []
        
        row, col = 0, 0
        for avatar_file in avatar_files:
            path = os.path.join("avatars", avatar_file)
            try:
                img = Image.open(path).resize((80, 80))
                photo = ImageTk.PhotoImage(img)
                self.avatar_images.append(photo)

                btn = tk.Button(self.avatar_selection_window, image=photo,
                                command=lambda f=path: self.set_avatar(f))
                btn.grid(row=row, column=col, padx=10, pady=10)
            except:
                continue
            col += 1
            if col == 3:
                col = 0
                row += 1
    def set_avatar(self, avatar_path):
        self.avatar_path = avatar_path
        messagebox.showinfo("Avatar Selected", f"You selected: {os.path.basename(avatar_path)}")
        self.avatar_selection_window.destroy()
        



    def create_account(self):
        name = self.name_entry.get()
        profile_id = self.profile_id_entry.get()
        desc = self.desc_entry.get()
        password = self.pass_entry.get()
        confirm_password = self.confirm_pass_entry.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return


        users = load_users()
        if profile_id in users:
            messagebox.showerror("Error", "Profile ID already exists!")
            return

        users[profile_id] = {
            "name": name,
            "description": desc,
            "password": password,
            "confirm password":password,
            "avatar": self.avatar_path
        }
        save_users(users)
        messagebox.showinfo("Success", "Account created!")
        

        self.signup_window.destroy()
        




        
        


#  GUI 
class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis + Chatbot")
        self.root.configure(bg="black")
        self.root.geometry("1080x600")
        self.set_background_gif("3003.gif")

        self.original_stdout = sys.stdout
        self.jarvis_thread = None
        self.chatbot_active = False

        self.setup_widgets()
    def set_background_gif(self, gif_path):
        try:
            self.bg_frames = [
                ImageTk.PhotoImage(img.resize((1920, 1080)))
                for img in ImageSequence.Iterator(Image.open(gif_path))
            ]
            self.bg_index = 0

            self.bg_label = tk.Label(self.root)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            def animate_bg():
                frame = self.bg_frames[self.bg_index]
                self.bg_label.configure(image=frame)
                self.bg_index = (self.bg_index + 1) % len(self.bg_frames)
                self.root.after(100, animate_bg)

            animate_bg()
            self.bg_label.lower()  
        except Exception as e:
            print("⚠️ Error setting background gif:", e)


    def setup_widgets(self):
        
        
        self.ask_label = tk.Label(self.root, text="ASK ME ANYTHING", font=("Algerian", 30, "bold"), fg="white", bg="black")
        self.ask_label.pack(pady=(10))
        avatar_path = getattr(self.root, 'selected_avatar_path', "")
        if avatar_path and os.path.exists(avatar_path):
            try:
                img = Image.open(avatar_path).resize((60, 60))
                self.avatar_image = ImageTk.PhotoImage(img)
                avatar_label = tk.Label(self.root, image=self.avatar_image, bg="black")
                avatar_label.place(relx=0.95, rely=0.05, anchor="ne")  
            except Exception as e:
                print(f"Could not load avatar image: {e}")


        
        self.mode_label = tk.Label(self.root, text="Status: Idle", bg="black", fg="cyan", font=("Aptos Display", 14, "bold"))
        self.mode_label.pack(pady=5)

        
    
        self.chat_log = tk.Text(self.root, bg="black", fg="white", width=109, height=18)
        self.chat_log.pack(pady=(100, 10))
        
    
        
        input_frame = tk.Frame(self.root, bg="black")
        input_frame.pack(pady=(5,0))

        self.entry = tk.Entry(input_frame, width=70, bg="#1e1e1e", fg="white", insertbackground="white")
        self.entry.pack(side=tk.LEFT, padx=10)

        send_btn = tk.Button(input_frame, text="Send 💬", command=self.send_message, bg="#007acc", fg="black")
        send_btn.pack(side=tk.LEFT, padx=5)

        mic_btn = tk.Button(input_frame, text="🎤 Mic", command=self.start_jarvis_thread, bg="#28a745", fg="black")
        mic_btn.pack(side=tk.LEFT, padx=5)
        
        
        self.wave_label = tk.Label(self.root, bg="black")
        self.wave_label.pack(pady=(0, 10))
        self.load_wave_gif("waves.gif") 
        
       

    def update_mode(self, text, color):
        self.mode_label.config(text=f"Status: {text}", fg=color)

    def print_to_gui(self, text):
        self.chat_log.insert(tk.END, text + "\n")
        self.chat_log.see(tk.END)
    def load_wave_gif(self, gif_path):
        try:
            self.wave_frames = [
                ImageTk.PhotoImage(img.resize((600, 300)))
                for img in ImageSequence.Iterator(Image.open(gif_path))
            ]
            self.wave_index = 0

            def animate():
                frame = self.wave_frames[self.wave_index]
                self.wave_label.configure(image=frame)
                self.wave_index = (self.wave_index + 1) % len(self.wave_frames)
                self.root.after(50, animate)

            animate()
        except Exception as e:
            print("⚠️ Error loading wave gif:", e)
            



        
    

    def send_message(self):
        self.chatbot_active = True
        self.update_mode("Chatbot Mode Active", "#007acc")

        if self.jarvis_thread and self.jarvis_thread.is_alive():
            self.print_to_gui("🛑 Stopping Jarvis for chatbot.................")
            sys.stdout = self.original_stdout

        user_input = self.entry.get()
        if user_input.strip() == "":
            return

        self.print_to_gui("You: " + user_input)
        self.entry.delete(0, tk.END)
        response = get_response(user_input)
        self.print_to_gui("Bot: " + response)

    def start_jarvis_thread(self):
        if self.chatbot_active:
            self.print_to_gui("🛑 Chatbot is active. Resetting for Jarvis.............")
            self.chatbot_active = False
            time.sleep(1)

        if self.jarvis_thread and self.jarvis_thread.is_alive():
            self.print_to_gui("⚙️ Jarvis is already running.")
            return

        self.print_to_gui("🎤 Starting Jarvis............")
        self.update_mode("Jarvis Mode Active", "#a1ee80")
        sys.stdout = StdoutRedirector(self.chat_log)

        self.jarvis_thread = threading.Thread(target=self.run_jarvis_wrapper, daemon=True)
        self.jarvis_thread.start()

        



    def run_jarvis_wrapper(self):
        run_jarvis()
        self.chatbot_active = False
        sys.stdout = self.original_stdout
        self.print_to_gui("🛌 Jarvis has stopped..........")
        self.update_mode("Idle", "cyan")
        
    


if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginWindow(root)
    root.mainloop()

