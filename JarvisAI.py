import speech_recognition as sr
import pyttsx3
import os
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Function to recognize speech from the microphone
def recognize_speech_from_mic(prompt="Listening for command...", timeout=10, phrase_time_limit=10):
    with sr.Microphone() as source:
        print(prompt)
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        try:
            command = r.recognize_google(audio, language="en-IN").lower()
            print(f"You said: {command}")
            speak(command)
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return None

# Function to speak text out loud
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to execute commands based on speech
def execute_command(command):
    if 'open youtube' in command or 'खोलें यूट्यूब' in command:
        open_browser()
        youtube_search_mode()
    elif 'close youtube' in command or 'बंद करें यूट्यूब' in command:
        close_browser('chrome.exe')
        speak("Done. Closing YouTube.")
    elif 'stop' in command or 'exit' in command or 'quit' in command or 'ruk jao' in command or 'jarvis shutdown' in command:
        speak("Stopping the program. Goodbye!")
        if 'driver' in globals():
            driver.quit()
        sys.exit()
    else:
        print("Command not recognized, please try again.")
        speak("Command not recognized, please try again.")

# Browser management functions
def open_browser():
    global driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def close_browser(keyword):
    if os.name == 'nt':
        os.system(f"taskkill /F /IM {keyword}.exe")
    elif os.name == 'posix':
        subprocess.call(["pkill", "-f", keyword])

# YouTube control functions
def youtube_search_mode():
    speak("YouTube opened. What would you like to search or play?")
    while True:
        search_command = recognize_speech_from_mic("Listening for YouTube command...")
        if search_command:
            if 'search' in search_command or 'खोजें' in search_command:
                handle_search(search_command)
            elif 'play' in search_command:
                play_video(driver, search_command)
            elif 'pause' in search_command or 'रोको' in search_command:
                pause_video(driver)
            elif 'continue' in search_command or 'चालू करो' in search_command:
                continue_video(driver)
            elif 'back' in search_command or 'पीछे जाओ' in search_command:
                go_back(driver)
            elif 'skip' in search_command or 'सेकंड' in search_command:
                handle_skip(search_command)
            elif 'volume' in search_command or 'वॉल्यूम' in search_command:
                handle_volume(search_command)
            elif 'full screen' in search_command or 'पूर्ण स्क्रीन' in search_command:
                toggle_fullscreen(driver)
            elif 'speed' in search_command or 'गति' in search_command:
                handle_speed(search_command)
            elif 'stop' in search_command or 'रुक जाओ' in search_command:
                speak("Exiting YouTube mode.")
                return
            else:
                speak("Command not recognized. Please try again.")

def handle_search(command):
    search_query = command.split('search', 1)[1].strip() if 'search' in command else command.split('खोजें', 1)[1].strip()
    search_youtube(driver, search_query)

def search_youtube(driver, query):
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    driver.get(url)
    speak(f"Searching YouTube for {query}")

# Video playback controls
def play_video(driver, command):
    video_number = extract_video_number(command)
    if video_number:
        try:
            video_xpath = f"(//a[@id='video-title'])[{video_number}]"
            driver.find_element(By.XPATH, video_xpath).click()
            speak(f"Playing video number {video_number}")
        except Exception as e:
            print(f"Error playing video: {e}")
            speak("Could not play the video")

def extract_video_number(command):
    number_map = {
        'first': 1, '1st': 1, 'पहला': 1,
        'second': 2, '2nd': 2, 'दूसरा': 2,
        'third': 3, '3rd': 3, 'तीसरा': 3,
        'fourth': 4, '4th': 4, 'चौथा': 4,
        'fifth': 5, '5th': 5, 'पांचवा': 5
    }
    for word, num in number_map.items():
        if word in command:
            return num
    return None

def pause_video(driver):
    execute_video_script(driver, "arguments[0].pause()", "Video paused")

def continue_video(driver):
    execute_video_script(driver, "arguments[0].play()", "Video resumed")

def go_back(driver):
    driver.back()
    speak("Went back to previous page")

# New feature implementations
def handle_skip(command):
    seconds = extract_number(command, r'skip (\d+) seconds?', r'(\d+) सेकंड')
    if seconds:
        skip_video(driver, seconds)

def skip_video(driver, seconds):
    execute_video_script(driver, f"arguments[0].currentTime += {seconds}", f"Skipped {seconds} seconds")

def handle_volume(command):
    percent = extract_number(command, r'volume (\d+)%?', r'(\d+) प्रतिशत')
    if percent:
        set_volume(driver, percent)

def set_volume(driver, percent):
    volume = max(0, min(100, percent)) / 100
    execute_video_script(driver, f"arguments[0].volume = {volume}", f"Volume set to {percent}%")

def toggle_fullscreen(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, 'button.ytp-fullscreen-button').click()
        speak("Toggled fullscreen mode")
    except Exception as e:
        print(f"Fullscreen error: {e}")
        speak("Could not toggle fullscreen")

def handle_speed(command):
    speed = extract_number(command, r'speed (\d+\.?\d*)', r'गति (\d+\.?\d*)', float)
    if speed:
        set_speed(driver, speed)

def set_speed(driver, speed):
    execute_video_script(driver, f"arguments[0].playbackRate = {speed}", f"Speed set to {speed}x")

# Helper functions
def execute_video_script(driver, script, success_message):
    try:
        video = driver.find_element(By.CSS_SELECTOR, 'video')
        driver.execute_script(script, video)
        speak(success_message)
    except Exception as e:
        print(f"Video control error: {e}")
        speak("Could not execute command")

def extract_number(command, *patterns, num_type=int):
    for pattern in patterns:
        match = re.search(pattern, command)
        if match:
            try:
                return num_type(match.group(1))
            except ValueError:
                pass
    speak("Please specify a valid number")
    return None

# Main program loop
if __name__ == "__main__":
    while True:
        command = recognize_speech_from_mic("Awaiting activation...")
        if command and any(keyword in command for keyword in ['jarvis', 'रोशन']):
            speak("How can I assist you?")
            while True:
                command = recognize_speech_from_mic()
                if command and any(keyword in command for keyword in ['stop', 'exit', 'रुक जाओ']):
                    speak("Goodbye!")
                    if 'driver' in globals():
                        driver.quit()
                    sys.exit()
                execute_command(command)
        else:
            speak("Activation keyword not detected")