<div align="center">
  <h1>🎙️ Dave</h1>
  <p><strong>A voice assistant for Windows, written in Python.</strong></p>

  ![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
  ![Windows](https://img.shields.io/badge/Windows-only-0078D4)
</div>

## About

Talk to Dave and he'll look things up, open sites and apps, take notes, and tell you the time. He greets you when he starts and answers out loud.

## What you can say

| Say | What happens |
| --- | --- |
| "einstein wikipedia" | Reads a short Wikipedia summary |
| "search on google" | Asks what to search, then opens the results |
| "search on youtube" | Asks what to search, then opens the results |
| "open instagram" | Opens Instagram |
| "play music" or "open spotify" | Opens Spotify |
| "what's the weather" | Opens the Ottawa forecast |
| "what's the time" | Tells you the time |
| "open notepad" | Opens Notepad |
| "take a note" | Types what you say into Notepad |
| "set alarm" | Asks how many minutes, then lets you know when time's up |
| "change voice" | Switches between male and female voices |
| "exit" or "quit" | Closes Dave |

## Run it locally

You'll need Windows, Python, a microphone and an internet connection.

```bash
git clone https://github.com/PranavTiwari44/AI_Assistant-main.git
cd "AI_Assistant-main/Voice+Assistant+Code+and+Files/Code and Files"
pip install pyttsx3 SpeechRecognition wikipedia pyautogui pyaudio
python voice.py
```

## To do

- Get the weather for any city
