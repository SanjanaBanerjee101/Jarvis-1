# Jarvis-1 🗣️🤖

Jarvis-1 is a **personal voice assistant** built with **Flask**, **HTML/CSS**, and **Python**.  
It listens to your voice, understands simple commands, and replies back with speech.  
Think of it as your very own mini **J.A.R.V.I.S.** from Iron Man (but lightweight 😉).

---

## 🚀 Features
- 🎤 Voice input via browser microphone  
- 🔊 Flask backend processes commands & replies with speech (`pyttsx3`)  
- 🌐 Simple web interface with HTML/CSS  
- ⚡ Lightweight, extendable, and beginner-friendly  
- 🧩 Can be integrated with APIs (e.g., Gemini, Weather, etc.) for smarter responses  

---

## ⚙️ Setup

```bash
# Clone the repo
git clone https://github.com/SanjanaBanerjee101/Jarvis-1.git
cd Jarvis-1

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py

================
Requirements
================
**Flask
**pyttsx3
**SpeechRecognition (optional, for extra features)
**google-generativeai (optional, for Gemini integration)

================
Future Scope
================
**Integrate with Gemini for AI-powered answers
**Add weather, news, and music commands
**Enhance with a more interactive UI