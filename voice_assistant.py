import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import psutil
import threading
import tkinter as tk
import sys

# ------------------- Text to Speech -------------------
engine = pyttsx3.init()
engine.setProperty("rate", 155)

def speak(text):
    status_label.config(text=text)
    engine.say(text)
    engine.runAndWait()

# ------------------- Speech Input -------------------
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand")
        return ""
    except sr.RequestError:
        speak("Speech service unavailable")
        return ""

# ------------------- Assistant Logic -------------------
def assistant_loop():
    speak("Voice assistant started. Press escape to stop.")
    while listening:
        command = listen_command()

        if not command:
            continue

        if "time" in command:
            speak("The time is " + datetime.datetime.now().strftime("%I:%M %p"))

        elif "date" in command:
            speak("Today's date is " + datetime.datetime.now().strftime("%B %d, %Y"))

        elif "open notepad" in command:
            speak("Opening notepad")
            os.system("notepad")

        elif "open browser" in command:
            speak("Opening browser")
            webbrowser.open("https://www.google.com")

        elif "search for" in command:
            query = command.replace("search for", "")
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")

        elif "battery" in command:
            battery = psutil.sensors_battery()
            speak(f"Battery is {battery.percent} percent")

        elif "exit" in command or "stop" in command:
            speak("Assistant stopped")
            stop_listening()
            return

        else:
            speak("Command not recognized")

# ------------------- Control Functions -------------------
def start_listening():
    global listening
    if not listening:
        listening = True
        threading.Thread(target=assistant_loop, daemon=True).start()

def stop_listening():
    global listening
    listening = False
    speak("Listening stopped")

# ------------------- GUI Setup -------------------
root = tk.Tk()
root.title("Accessible Voice Assistant")
root.geometry("400x300")

listening = False

title_label = tk.Label(root, text="Voice Assistant", font=("Arial", 18))
title_label.pack(pady=10)

status_label = tk.Label(root, text="Press Start to speak", font=("Arial", 12))
status_label.pack(pady=10)

start_button = tk.Button(
    root, text="Start Listening",
    font=("Arial", 14),
    height=2,
    command=start_listening
)
start_button.pack(pady=10)

stop_button = tk.Button(
    root, text="Stop",
    font=("Arial", 14),
    height=2,
    command=stop_listening
)
stop_button.pack(pady=10)

# Keyboard Accessibility
root.bind("<Return>", lambda e: start_listening())
root.bind("<Escape>", lambda e: stop_listening())

speak("Interface loaded. Press Enter to start listening")

root.mainloop()
