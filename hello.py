import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import *
from tkinter import messagebox, ttk
import time
from time import sleep

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 190)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1)

def voice_change(v):
    x = int(v)
    engine.setProperty('voice', voices[x].id)
    speak("done sir")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%H:%M:%S")
    speak("The current time is")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("The current date is")
    speak(day)
    speak(month)
    speak(year)

def checktime(tt):
    hour = datetime.datetime.now().hour
    if ("morning" in tt):
        if (hour >= 6 and hour < 12):
            speak("Good morning sir")
        elif (hour >= 12 and hour < 18):
            speak("it's Good afternoon sir")
        elif (hour >= 18 and hour < 24):
            speak("it's Good Evening sir")
        else:
            speak("it's Goodnight sir")
    elif ("afternoon" in tt):
        if (hour >= 12 and hour < 18):
            speak("it's Good afternoon sir")
        elif (hour >= 6 and hour < 12):
            speak("Good morning sir")
        elif (hour >= 18 and hour < 24):
            speak("it's Good Evening sir")
        else:
            speak("it's Goodnight sir")
    else:
        speak("it's night sir!")

def wishme():
    speak("Welcome Back")
    hour = datetime.datetime.now().hour
    if (hour >= 6 and hour < 12):
        speak("Good Morning sir!")
    elif (hour >= 12 and hour < 18):
        speak("Good afternoon sir")
    elif (hour >= 18 and hour < 24):
        speak("Good Evening sir")
    else:
        speak("Goodnight sir")
    speak("Jarvis at your service, Please tell me how can I help you?")

def wishme_end():
    speak("signing off")
    hour = datetime.datetime.now().hour
    if (hour >= 6 and hour < 12):
        speak("Good Morning")
    elif (hour >= 12 and hour < 18):
        speak("Good afternoon")
    elif (hour >= 18 and hour < 24):
        speak("Good Evening")
    else:
        speak("Goodnight.. Sweet dreams")
    quit()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
    except Exception as e:
        print(e)
        speak("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("user-name@xyz.com", "pwd")
    server.sendmail("user-name@xyz.com", to, content)
    server.close()

def screenshot():
    img = pyautogui.screenshot()
    img.save("C:\\Users\\Jarvis-AI-using-python3-\\screenshots\\ss.png")

def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU usage is at ' + usage)
    battery = psutil.sensors_battery()
    speak("Battery is at")
    speak(battery.percent)

def jokes():
    j = pyjokes.get_joke()
    speak(j)

def weather():
    api_key = "YOUR-API_KEY"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("tell me which city")
    city_name = takeCommand()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        r = ("in " + city_name + " Temperature is " +
             str(int(current_temperature - 273.15)) + " degree celsius " +
             ", atmospheric pressure " + str(current_pressure) + " hpa unit" +
             ", humidity is " + str(current_humidiy) + " percent"
             " and " + str(weather_description))
        speak(r)
    else:
        speak(" City Not Found ")

def personal():
    speak("I am Jarvis, version 1.0, I am an AI assistant, I am developed by Praveen on 29 May 2020 in INDIA")
    speak("Now I hope you know me")

def play_youtube(search_query):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(f"https://www.youtube.com/results?search_query={search_query}")
        speak(f"Playing {search_query} on YouTube")
        
        # Adding a wait to ensure the page loads before attempting to find the video
        driver.implicitly_wait(10)
        
        # Attempt to click the first video
        first_video = driver.find_element(By.CSS_SELECTOR, "a#video-title")
        first_video.click()
        
        # Optional: add a wait to ensure the video starts playing
        time.sleep(5)
        
    except Exception as e:
        speak("I could not play the video. Please try again.")
        print(e)
    finally:
        # Keep the browser open for a bit to ensure it doesn't close immediately
        time.sleep(10)  # Adjust as needed
        driver.quit()

def run_jarvis():
    wishme()
    while True:
        query = takeCommand().lower()

        if 'time' in query:
            time()
        elif 'date' in query:
            date()
        elif "tell me about yourself" in query or "about you" in query or "who are you" in query or "yourself" in query:
            personal()
        elif "developer" in query or "tell me about your developer" in query or "father" in query or "who develop you" in query:
            res = open("about.txt", 'r')
            speak("here are the details: " + res.read())
        elif 'wikipedia' in query or 'what' in query or 'who' in query or 'when' in query or 'where' in query:
            speak("searching...")
            query = query.replace("wikipedia", "")
            query = query.replace("search", "")
            query = query.replace("what", "")
            query = query.replace("when", "")
            query = query.replace("where", "")
            query = query.replace("who", "")
            query = query.replace("is", "")
            result = wikipedia.summary(query, sentences=2)
            speak(result)
        elif 'www' in query or 'search' in query or 'open' in query:
            speak("searching...")
            if 'www' in query:
                wb.open(query)
            else:
                search_query = query.replace("search", "").replace("open", "").strip()
                wb.open(f"https://www.google.com/search?q={search_query}")
        elif "send email" in query:
            try:
                speak("What is the message for the email")
                content = takeCommand()
                to = 'reciever@xyz.com'
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                speak("Unable to send email, check the address of the recipient")
        elif "search on google" in query or "open website" in query:
            speak("What should I search or open?")
            chromepath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            search = takeCommand().lower()
            wb.get(chromepath).open_new_tab(f"https://www.google.com/search?q={search}")
        elif "logout" in query:
            os.system("shutdown -l")
        elif "restart" in query:
            os.system("shutdown /r /t 1")
        elif "shut down" in query:
            os.system("shutdown /s /t 1")
        elif "remember that" in query:
            speak("What should I remember?")
            data = takeCommand()
            speak("you said me to remember that " + data)
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()
        elif "do you know anything" in query:
            remember = open("data.txt", "r")
            speak("you said me to remember that " + remember.read())
        elif "screenshot" in query or "take a screenshot" in query:
            screenshot()
            speak("Done")
        elif "cpu" in query:
            cpu()
        elif "joke" in query or "jokes" in query:
            jokes()
        elif "weather" in query or "temperature" in query:
            weather()
        elif "tell me your powers" in query or "help" in query or "features" in query:
            features = ''' I can help you do many things like:
            I can tell you the current time and date,
            I can tell you the current weather,
            I can tell you battery and CPU usage,
            I can create a reminder list,
            I can take screenshots,
            I can send email to your boss or family or your friend,
            I can shut down or logout or hibernate your system,
            I can tell you non-funny jokes,
            I can open any website,
            I can search things on Wikipedia,
            I can change my voice from male to female and vice versa.
            And yes, one more thing, my boss is working on this system to add more features.
            Tell me, what can I do for you?'''
            speak(features)
        elif "hi" in query or "hello" in query or "good morning" in query or "good afternoon" in query or "good night" in query or "morning" in query or "noon" in query or "night" in query:
            query = query.replace("jarvis", "").strip()
            if "morning" in query or "night" in query or "good night" in query or "afternoon" in query or "noon" in query:
                checktime(query)
            else:
                speak("What can I do for you?")
        elif "voice" in query:
            speak("For female say 'female' and for male say 'male'")
            q = takeCommand()
            if "female" in q:
                voice_change(1)
            elif "male" in q:
                voice_change(0)
        elif "male" in query or "female" in query:
            if "female" in query:
                voice_change(1)
            elif "male" in query:
                voice_change(0)
        elif "play" in query and "youtube" in query:
            speak("What should I play on YouTube?")
            search_query = takeCommand()
            play_youtube(search_query)
        elif 'i am done' in query or 'bye bye jarvis' in query or 'go offline jarvis' in query or 'bye' in query or 'nothing' in query:
            wishme_end()

def start_jarvis():
    run_jarvis()

# GUI part
root = Tk()
root.title("Jarvis AI")
root.geometry("400x300")
root.configure(bg='#1f1f1f')

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14), padding=10)
style.configure("TLabel", font=("Helvetica", 16), background='#1f1f1f', foreground='#ffffff')

label = ttk.Label(root, text="Welcome to Jarvis AI")
label.pack(pady=20)

start_button = ttk.Button(root, text="Start", command=start_jarvis)
start_button.pack(pady=20)

exit_button = ttk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=20)

# Voice selection
voice_frame = Frame(root, bg='#1f1f1f')
voice_frame.pack(pady=20)
voice_label = ttk.Label(voice_frame, text="Select Voice:")
voice_label.grid(row=0, column=0, padx=10)

male_button = ttk.Button(voice_frame, text="Male", command=lambda: voice_change(0))
male_button.grid(row=0, column=1, padx=10)

female_button = ttk.Button(voice_frame, text="Female", command=lambda: voice_change(1))
female_button.grid(row=0, column=2, padx=10)

root.mainloop()
