# import pyautogui

# def search_youtube(query):
#     # Open the search results for the query on YouTube
#     url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
#     webbrowser.open(url)
#     speak(f"Searching YouTube for {query}")
    
#     # Wait for a short period to let the page load
#     time.sleep(3)
    
#     # Simulate a click on the first video in the search results to play it
#     try:
#         # Use PyAutoGUI to simulate a click on the first video link
#         pyautogui.click(x=600, y=300)  # Coordinates for the first video (you may need to adjust these based on your screen resolution)
#         speak(f"Playing the first result for {query}.")
#     except Exception as e:
#         print(f"Error while trying to play the video: {e}")
#         speak("Sorry, I couldn't play the video. Please try again.")

# def execute_command(command):
#     if 'open youtube' in command or 'खोलें यूट्यूब' in command or 'jarvis open youtube' in command:
#         webbrowser.open('https://www.youtube.com')
#         speak("Done. Opening YouTube.")
#         while True:
#             search_command = recognize_speech_from_mic("Listening for YouTube search query...")
#             if search_command:
#                 if 'search' in search_command or 'खोजें' in search_command:
#                     search_query = search_command.split('search', 1)[1].strip() if 'search' in search_command else search_command.split('खोजें', 1)[1].strip()
#                     search_youtube(search_query)
#                 elif 'stop' in search_command or 'exit' in search_command or 'quit' in search_command or 'ruk jao' in search_command or 'रुक जाओ' in search_command:
#                     speak("Stopping the YouTube search mode.")
#                     break
#                 else:
#                     speak("Command not recognized. Please say 'search' or 'खोजें' followed by your query, or 'stop' to exit YouTube search mode.")
