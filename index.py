import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import subprocess
import pyautogui
import psutil
from youtubesearchpython import VideosSearch
import pygame
import numpy as np
import threading
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

# =============== INIT METHODS

print("Source code initializing...")
print("=========================")
print("=========================")
# Initialize pygame
pygame.init()
# Initialize text-to-speech engine
engine = pyttsx3.init()
# Bot GUI loop state
gui_running = True
assistant_running = True

def on_closing():
    global assistant_running
    assistant_running = False

def create_gui():
    global gui_running

    # Create the main window
    root = tk.Tk()
    root.title("Voice Assistant")

    # Capture the close window event
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Load the GIF
    gif_path = "giphy.gif"
    gif = Image.open(gif_path)
    gif_frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(gif)]

    # Create a label with the image
    label = tk.Label(root)
    label.pack()

    # Function to animate the GIF
    def animate(frame_num):
        label.configure(image=gif_frames[frame_num])
        root.after(50, animate, (frame_num + 1) % len(gif_frames))

    # Start the animation
    animate(0)

    # Run the Tkinter event loop while gui_running flag is True
    while gui_running:
        root.update()

    # Close the Tkinter window
    root.destroy()       

# Function to greet user
def greet_user():    
    print("Starting assistant...")
    print("=========================")
    print("HELLO, HOW CAN I ASSIST YOU TODAY ?")
    print("=========================")
    engine.say("Hello! How can I assist you today?")
    engine.runAndWait()

# Function to recognize voice commands
def recognize_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("Command:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, I'm having trouble accessing the audio API.")
        return ""


# =============== ASSISTANT FEATURES

# Function to get current time and date
def get_time_date():
    current_time = datetime.datetime.now().strftime("%H:%M")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    engine.say(f"The current time is {current_time} and the date is {current_date}")
    engine.runAndWait()

# Function to open browser
def open_browser():
    webbrowser.open("https://www.google.com")

# Function for Wikipedia search
def wikipedia_search(topic):
    webbrowser.open(f"https://en.wikipedia.org/wiki/{topic}")

# Function to open any website
def open_website(url):
    webbrowser.open(url)

# Function to play a video on YouTube
def play_video(query):
    # Search for videos based on the query
    videos_search = VideosSearch(query, limit=5)
    result = videos_search.result()['result']

    if(len(result) > 1):
        video_urls = [video['link'] for video in result]
        webbrowser.open(video_urls[0])

# Function to open/close notepad
def open_close_notepad(action):
    if action == "open":
        os.system("start notepad")
    elif action == "close":
        os.system("taskkill /im notepad.exe /f")

# Function to take a screenshot
def take_screenshot():
    screenshot = pyautogui.screenshot()
    sound = pygame.mixer.Sound('screenshot-sound.mp3')
    sound.play()
    
    screenshot.save("screenshot.png")

# Function to open/close task manager
def open_task_manager(action):
    if action == "open":
        os.system("start taskmgr")
    elif action == "close":
        os.system("taskkill /im taskmgr.exe /f")

# Function to open/close microsoft word
def open_msword(action):
    if action == "open":
        os.system("start Winword")
    elif action == "close":
        os.system("taskkill /im Winword.exe /f")

# Function to open/close microsoft excel
def open_excel(action):
    if action == "open":
        os.system("start excel")
    elif action == "close":
        os.system("taskkill /im excel.exe /f")

# Function to open/close microsoft power pnt
def open_powerpnt(action):
    if action == "open":
        os.system("start powerpnt")
    elif action == "close":
        os.system("taskkill /im powerpnt.exe /f")  

# Function to open/close calculator
def open_calc(action):
    if action == "open":
        os.system("start calc")
    elif action == "close":
        os.system("taskkill /im CalculatorApp.exe /f")

# Function to open media player
def open_media(action):
    if action == "open":
        os.system("start mediaplayer")
    elif action == "close":
        os.system("taskkill /im Microsoft.Media.Player.exe /f")


# =============== MAIN LOOP

if __name__ == "__main__":    
    greet_user()

    # Create a thread for looped playback
    gif_thread = threading.Thread(target=create_gui)

    # Start the thread
    gif_thread.start()

    while True:
        if(not assistant_running):
            engine.say("Goodbye!")
            gui_running = False
            # Wait for the thread to finish
            gif_thread.join()
            
            print("=========================")
            print("Closing assistant...")
            print("=========================")
            engine.runAndWait()
            break

        command = recognize_command()

        if "time" in command:
            get_time_date()
        elif "open browser" in command:
            open_browser()
        elif "wikipedia search" in command:
            topic_arr = command.split("wikipedia search for ")
            if(len(topic_arr) > 1):
                topic = command.split("wikipedia search for ")[1]
                wikipedia_search(topic)
        elif "open website" in command:
            url_arr = command.split("open website ")
            if(len(url_arr) > 1):
                url = command.split("open website ")[1]                          
                open_website(url)
        elif "youtube play" in command: 
            youtube_arr = command.split("youtube play")
            if(len(youtube_arr) > 1):
                youtube_query = command.split("youtube play")[1]
                play_video(youtube_query)
        elif "notepad" in command:
            if "open" in command:
                open_close_notepad("open")
            elif "close" in command:
                open_close_notepad("close")
        elif "screenshot" in command:
            take_screenshot()
        elif "task manager" in command:
            if "open" in command:
                open_task_manager("open")
            elif "close" in command:
                open_task_manager("close")
        elif "microsoft word" in command:
            if "open" in command:
                open_msword("open")
            elif "close" in command:
                open_msword("close")
        elif "microsoft excel" in command:
            if "open" in command:
                open_excel("open")
            elif "close" in command:
                open_excel("close")
        elif "microsoft powerpoint" in command:
            if "open" in command:
                open_powerpnt("open")
            elif "close" in command:
                open_powerpnt("close")                                
        elif "calculator" in command:
            if "open" in command:
                open_calc("open")
            elif "close" in command:
                open_calc("close")
        elif "media player" in command:
            if "open" in command:
                open_media("open")
            elif "close" in command:
                open_media("close")                                
        elif "bye" in command or "exit" in command:
            engine.say("Goodbye!")
            # Set the flag to stop the thread
            gui_running = False
            # Wait for the thread to finish
            gif_thread.join()
            print("=========================")
            print("Closing assistant...")
            print("=========================")
            engine.runAndWait()
            break