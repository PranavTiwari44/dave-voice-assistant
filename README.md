<div align="center">
  <h1>🎙️ Dave</h1>
  <p><strong>A voice assistant for Windows, written in Python.</strong></p>

  ![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
  ![Windows](https://img.shields.io/badge/Windows-only-0078D4)
</div>

## About

Talk to Dave and he'll look things up, open sites and apps, take notes, and tell you the time. Ask him anything else and a local AI model answers, running on your own PC through Ollama, and he remembers the conversation so you can ask follow-ups. He greets you when he starts and answers out loud.

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
| "set alarm" | Asks how many minutes, then beeps when time's up. You can keep talking to Dave in the meantime |
| "change voice" | Switches between male and female voices, if your PC has both installed |
| "start over" | Makes Dave forget the conversation so far |
| "exit" or "quit" | Closes Dave |
| Anything else | A local AI model answers through [Ollama](https://ollama.com), and you can ask follow-up questions |

## Run it locally

You'll need Windows, Python, a microphone and an internet connection. For questions, install [Ollama](https://ollama.com) and run `ollama pull qwen3.5:9b`.

```bash
git clone https://github.com/PranavTiwari44/AI_Assistant-main.git
cd "AI_Assistant-main/Voice+Assistant+Code+and+Files/Code and Files"
pip install pyttsx3 SpeechRecognition wikipedia pyautogui pyaudio
python voice.py
```

Stay quiet for a second after starting. Dave listens to the room first so he can tell your voice apart from background noise.

## To do

- Get the weather for any city
- Text mode: run `python voice.py --text` to type to Dave instead of talking
- Connect to [TrailSense](https://github.com/PranavTiwari44/trailsense-ai) so Dave can answer "how tough is this trail?"
  - TrailSense: add a `POST /ask` endpoint that takes a question and returns the agent's answer
  - Dave: send questions that mention "trail" or "hike" to that endpoint and speak the answer
