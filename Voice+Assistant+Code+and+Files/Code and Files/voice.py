import pyttsx3 ##for the ai to speak, ## text to speech library
import datetime
import speech_recognition ##for getting input voices   ## speech to text library
import wikipedia #for surfing wikipedia
import os ##for opening local files
import webbrowser ## for surfing the internet
import time
import pyautogui ## controls the mouse and kyboard just like a human
import re
import threading
import winsound

##Importing the voice for AI
engine = pyttsx3.init('sapi5') ##one of the engine present inside this library
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[0].id) #Male voice represent 0

WORD_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "fifteen": 15, "twenty": 20, "thirty": 30, "a": 1, "an": 1,
}

def parse_minutes(text):
    text = text.lower()
    match = re.search(r"\d+", text)      # finds "5" inside "5 minutes"
    if match:
        return int(match.group())
    for word in text.split():            # handles "five"
        if word in WORD_NUMBERS:
            return WORD_NUMBERS[word]
    return None                          # no number found

def ring_alarm(minutes):
    print(f"\n⏰ Alarm: {minutes} minute(s) are up!")
    for _ in range(5):
        winsound.Beep(1000, 500)   # 1000 Hz for 0.5 seconds, 5 times

##speak function which will convert the text to speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait() ##it will basically stop

def greet():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        speak("It is a fine morning sir !")

    elif hour >=12 and hour<18:
        speak("hope you had your brunch, Good Afternoon Sir !")

    else:
        speak("The wind is lovely, Good Evening Sir !")

    speak("Hello How are you? I am your personal AI Assistant Dave! How can I be of service")

# Function to change the AI's voice
def change_voice():
    if len(voices) < 2:
        speak("Sorry, only one voice is installed on this computer.")
        return
    current_voice = engine.getProperty('voice')
    if current_voice == voices[0].id:  # Male voice
        engine.setProperty('voice', voices[1].id)  # Female voice
        speak("Voice changed to female.")
    else:
        engine.setProperty('voice', voices[0].id)  # Male voice
        speak("Voice changed to male.")

##developing differenrt command
r = speech_recognition.Recognizer() ## will convert speech to text
r.pause_threshold = 1.2 ## that is the ai will take 1.2 seconds pause

def calibrate_mic():
    # Measure background noise once at startup instead of before every command
    with speech_recognition.Microphone() as source:
        r.adjust_for_ambient_noise(source)

def command():
    with speech_recognition.Microphone() as source: ## one we are using is recognised google
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-in') ##speech to text
        print(f"You said: {query} \n")
    except Exception as e:
        print("I could not get you, please speak again")
        speak("I could not get you please speak again")
        return "None"
    
    return query

##Writing different tasks for AI to perform
if __name__=="__main__": ## this is the root function
    calibrate_mic()
    greet()
    while True:
        query = command().lower() ##coverting it into lower case
        if query == "none":
            continue  # nothing was heard, command() already asked to repeat

        #Logic for executing taks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            try:
                results = wikipedia.summary(query, sentences=2)
            except wikipedia.DisambiguationError as e:
                options = ", ".join(e.options[:3])
                speak(f"That could mean several things, like {options}. Please be more specific.")
            except wikipedia.PageError:
                speak(f"I couldn't find a Wikipedia page for {query}.")
            except Exception:
                speak("Sorry, I couldn't reach Wikipedia right now.")
            else:
                speak("According to Wikipedia")
                print(results)
                speak(results)

        elif 'open instagram' in query:
            webbrowser.open("https://www.instagram.com/")

        elif 'search on google' in query:
            speak("What would you like to search for?")
            search_query = command()
            if search_query != "None":
                webbrowser.open(f"https://www.google.com/search?q={search_query}")

        elif 'the weather' in query:
            webbrowser.open("https://www.msn.com/en-ca/weather/forecast/in-Ottawa,Ontario?loc=eyJsIjoiT3R0YXdhIiwiciI6Ik9udGFyaW8iLCJyMiI6Ik90dGF3YSIsImMiOiJDYW5hZGEiLCJpIjoiQ0EiLCJnIjoiZW4tY2EiLCJ4IjoiLTc1LjY5MjQiLCJ5IjoiNDUuNDIwNCJ9&weadegreetype=C&ocid=winp2fptaskbar&cvid=36cb0e19ac7644dba33c69f30bec5a63&content=TeaserDayTempChange_wxnwtsdtr2t111/")

        elif 'play music' in query or 'open spotify' in query:
            webbrowser.open("https://open.spotify.com/")
            speak("Opening Spotify.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'search on youtube' in query:
            speak("What would you like to search for?")
            search_query = command()
            if search_query != "None":
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

        elif 'change voice' in query:
            change_voice()

        elif 'open notepad' in query:
            os.startfile("notepad.exe")

        elif 'take a note' in query:
            speak("Opening Notepad for you...")
            os.startfile("notepad.exe")

            time.sleep(2)  # Wait a bit for Notepad to open
            speak("What would you like me to write?")
            note = command()

            if note != "None":
                time.sleep(1)
                pyautogui.write(note, interval=0.05)  # types the note into Notepad
                speak("Your note has been written in Notepad.")

        elif 'set alarm' in query:
            speak("For how many minutes?")
            minutes = parse_minutes(command())
            if minutes is None:
                speak("Sorry, I didn't catch a number. Please say set alarm again.")
            else:
                timer = threading.Timer(minutes * 60, ring_alarm, args=[minutes])
                timer.daemon = True        # lets the program exit even if an alarm is pending
                timer.start()
                speak(f"Alarm set for {minutes} minutes.")

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye, Sir!")
            break

        else:
            speak("I'm sorry, I didn't understand that. Could you please repeat or try another command?")



