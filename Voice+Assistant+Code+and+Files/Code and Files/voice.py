import win32com.client ## for the ai to speak, using the text to speech built into Windows
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
import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen3.5:9b"  # any model from `ollama list` works here

##Importing the voice for AI
# We talk to Windows' speech system (SAPI) directly. pyttsx3 2.99 only spoke the first sentence.
engine = win32com.client.Dispatch("SAPI.SpVoice")
voices = engine.GetVoices()
engine.Voice = voices.Item(0) #Male voice represent 0

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

SYSTEM_PROMPT = {"role": "system", "content": "You are Dave, a voice assistant. Your answers are read out loud, so reply in two or three short sentences of plain text with no lists or formatting."}
chat_history = []  # past questions and answers, so follow-ups like "tell me more" work

def ask_ollama(question):
    # Send the question, plus the last few exchanges, to the local Ollama model
    new_message = {"role": "user", "content": question}
    data = {
        "model": OLLAMA_MODEL,
        "messages": [SYSTEM_PROMPT] + chat_history[-10:] + [new_message],  # last 5 questions and answers
        "stream": False,
        "think": False,  # skip step-by-step reasoning so answers come back fast
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        answer = json.loads(response.read())["message"]["content"]

    # Only remember the exchange once it worked
    chat_history.append(new_message)
    chat_history.append({"role": "assistant", "content": answer})
    return answer

##speak function which will convert the text to speech
def speak(audio):
    engine.Speak(audio) ## speaks and waits until it's done

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
    if voices.Count < 2:
        speak("Sorry, only one voice is installed on this computer.")
        return
    if engine.Voice.Id == voices.Item(0).Id:  # Male voice
        engine.Voice = voices.Item(1)  # Female voice
        speak("Voice changed to female.")
    else:
        engine.Voice = voices.Item(0)  # Male voice
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

        elif 'instagram' in query:
            speak("Opening Instagram.")
            webbrowser.open("https://www.instagram.com/")

        elif 'google' in query:
            if 'search' in query:
                speak("What would you like to search for?")
                search_query = command()
                if search_query != "None":
                    webbrowser.open(f"https://www.google.com/search?q={search_query}")
            else:
                speak("Opening Google.")
                webbrowser.open("https://www.google.com/")

        elif 'weather' in query:
            speak("Here's the weather.")
            webbrowser.open("https://www.msn.com/en-ca/weather/forecast/in-Ottawa,Ontario?loc=eyJsIjoiT3R0YXdhIiwiciI6Ik9udGFyaW8iLCJyMiI6Ik90dGF3YSIsImMiOiJDYW5hZGEiLCJpIjoiQ0EiLCJnIjoiZW4tY2EiLCJ4IjoiLTc1LjY5MjQiLCJ5IjoiNDUuNDIwNCJ9&weadegreetype=C&ocid=winp2fptaskbar&cvid=36cb0e19ac7644dba33c69f30bec5a63&content=TeaserDayTempChange_wxnwtsdtr2t111/")

        elif 'play music' in query or 'spotify' in query:
            webbrowser.open("https://open.spotify.com/")
            speak("Opening Spotify.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'youtube' in query:
            if 'search' in query:
                speak("What would you like to search for?")
                search_query = command()
                if search_query != "None":
                    webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
            else:
                speak("Opening YouTube.")
                webbrowser.open("https://www.youtube.com/")

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

        elif 'start over' in query or 'new conversation' in query:
            chat_history.clear()
            speak("Okay, I've forgotten our conversation.")

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye, Sir!")
            break

        else:
            # Not a built-in command, so let the local AI model answer it
            print("Thinking...")
            try:
                answer = ask_ollama(query)
            except Exception:
                speak("Sorry, I couldn't reach Ollama. Make sure it's running.")
            else:
                print(answer)
                speak(answer)



