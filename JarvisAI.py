import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Function to recognize speech from the microphone
def recognize_speech_from_mic(prompt="Listening for command..."):
    with sr.Microphone() as source:
        print(prompt)
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language="en-IN").lower()  # Supports English and Hindi
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
    elif 'open facebook' in command or 'खोलें फेसबुक' in command:
        webbrowser.open('https://www.facebook.com')
        speak("Done. Opening Facebook.")
    elif 'close facebook' in command or 'बंद करें फेसबुक' in command:
        close_browser('chrome.exe')
        speak("Done. Closing Facebook.")
    elif 'open chatgpt' in command or 'खोलें चैटजीपीटी' in command:
        webbrowser.open('https://chat.openai.com')
        speak("Done. Opening ChatGPT.")
    elif 'close chatgpt' in command or 'बंद करें चैटजीपीटी' in command:
        close_browser('chrome.exe')
        speak("Done. Closing ChatGPT.")
    elif 'open whatsapp' in command or 'खोलें व्हाट्सएप' in command:
        open_browser()
        open_whatsapp()
    elif 'stop' in command or 'exit' in command or 'quit' in command or 'ruk jao' in command or 'jarvis shutdown' in command:
        speak("Stopping the program. Goodbye!")
        if 'driver' in globals():
            driver.quit()  # Ensure WebDriver is properly closed
        sys.exit()
    else:
        print("Command not recognized, please try again.")
        speak("Command not recognized, please try again.")

# Function to open the browser
def open_browser():
    global driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Function for YouTube search mode
def youtube_search_mode():
    speak("YouTube opened. What would you like to search or play?")
    while True:
        search_command = recognize_speech_from_mic("Listening for YouTube search query or play command...")
        if search_command:
            if 'search' in search_command or 'खोजें' in search_command:
                search_query = search_command.split('search', 1)[1].strip() if 'search' in search_command else search_command.split('खोजें', 1)[1].strip()
                search_youtube(driver, search_query)
            elif 'play' in search_command:
                play_video(driver, search_command)
            elif 'stop' in search_command or 'exit' in search_command or 'quit' in search_command or 'ruk jao' in search_command or 'रुक जाओ' in search_command:
                speak("Stopping the YouTube search mode.")
                driver.quit()
                break
            else:
                speak("Command not recognized. Please say 'search' or 'खोजें' followed by your query, 'play' to play a specific video, or 'stop' to exit YouTube search mode.")

# Function to search YouTube
def search_youtube(driver, query):
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    driver.get(url)
    speak(f"Searching YouTube for {query}")

# Function to play a specific video on YouTube
def play_video(driver, command):
    video_number = None

    if 'first' in command or '1st' in command or 'पहला' in command or 'play first video' in command:
        video_number = 1
    elif 'second' in command or '2nd' in command or 'दूसरा' in command or 'play second video' in command:
        video_number = 2
    elif 'third' in command or '3rd' in command or 'तीसरा' in command or 'play third video' in command:
        video_number = 3
    elif 'fourth' in command or '4th' in command or 'चौथा' in command or 'play fourth video' in command:
        video_number = 4
    elif 'fifth' in command or '5th' in command or 'पांचवा' in command or 'play fifth video' in command:
        video_number = 5

    if video_number:
        try:
            video_xpath = f"(//a[@id='video-title'])[{video_number}]"
            video_element = driver.find_element(By.XPATH, video_xpath)
            video_element.click()
            speak(f"Playing the {video_number} video.")
        except Exception as e:
            print(f"An error occurred: {e}")
            speak("Sorry, I couldn't play the video. Please try again.")
    else:
        speak("Video number not recognized. Please say 'play first video' or 'play second video'.")

# Function to open WhatsApp and send messages
def open_whatsapp():
    driver.get('https://web.whatsapp.com')
    speak("Please scan the QR code to log in.")
    time.sleep(15)

    while True:
        contact_name = recognize_speech_from_mic("Whom do you want to message?")
        if contact_name:
            try:
                search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='3']")
                search_box.clear()
                search_box.send_keys(contact_name)
                search_box.send_keys(Keys.RETURN)
                speak(f"Opened chat with {contact_name}. What do you want to say?")
                while True:
                    message = recognize_speech_from_mic("Listening for your message...")
                    if message:
                        message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='1']")
                        message_box.send_keys(message)
                        message_box.send_keys(Keys.RETURN)
                        speak("Message sent. Do you want to send another message or stop?")
                        next_command = recognize_speech_from_mic("Listening for next command...")
                        if 'stop' in next_command or 'exit' in next_command or 'quit' in next_command or 'ruk jao' in next_command or 'रुक जाओ' in next_command:
                            speak("Stopping. Goodbye!")
                            driver.quit()
                            break
            except Exception as e:
                print(f"An error occurred: {e}")
                speak("Sorry, I couldn't open the chat. Please try again.")

# Function to close the browser
def close_browser(keyword):
    if os.name == 'nt':
        os.system(f"taskkill /F /IM {keyword}.exe")
    elif os.name == 'posix':
        subprocess.call(["pkill", "-f", keyword])

# Main function to start the program
if __name__ == "__main__":
    while True:
        print("Awaiting activation command...")
        command = recognize_speech_from_mic()
        if command and ('jarvis' in command or 'roshan' in command or 'जार्विस' in command or 'रोशन' in command):
            speak("Yes Sir, how can I assist you?")
            while True:
                command = recognize_speech_from_mic("Listening for your command...")
                if command:
                    if 'stop' in command or 'exit' in command or 'quit' in command or 'ruk jao' in command or 'रुक जाओ' in command:
                        speak("Stopping the program. Goodbye!")
                        if 'driver' in globals():
                            driver.quit()  # Ensure WebDriver is properly closed
                        sys.exit()
                    execute_command(command)
        else:
            print("Activation command not detected. Please try again.")
            speak("Activation command not detected. Please try again.")
