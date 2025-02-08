import speech_recognition as sr
import subprocess

# Initialize the recognizer
r = sr.Recognizer()

def recognize_speech_from_mic():
    with sr.Microphone() as source:
        print("Listening for activation command...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return None

if __name__ == "__main__":
    while True:
        command = recognize_speech_from_mic()
        if command and ('jarvis' in command or 'roshan' in command):
            print("Activation command detected! Starting main program...")
            subprocess.call(['python', 'JarvisAI.py'])
            break