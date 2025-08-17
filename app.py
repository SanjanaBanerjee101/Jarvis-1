from flask import Flask, request, render_template, Response
import os
import time
import webbrowser
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai

# ---------- FLASK APP ----------
app = Flask(__name__)

# ---------- GEMINI SETUP ----------
GEMINI_API_KEY = os.getenv("YOUR API KEY")
if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR API KEY":
    genai.configure(api_key=GEMINI_API_KEY)

# Optional music library (dict: {song_name: url})
try:
    import musiclibrary  # file: musiclibrary.py with `music = {"song name": "https://..."}`
except Exception:
    musiclibrary = None

r = sr.Recognizer()

# ---------- SPEAK FUNCTION (server-side safety) ----------
def speak(text: str):
    text = (text or "").replace("*", "").replace("#", "")
    print(f"[TTS] {text}")
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        time.sleep(0.1)
    except Exception:
        # Allow server to run even if TTS backend is unavailable
        pass

# ---------- GEMINI ----------
def ask_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        return "Gemini API key is not set."
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        resp = model.generate_content(prompt)
        return (getattr(resp, "text", "") or "(No response)").strip()
    except Exception as e:
        return f"Error with Gemini: {e}"

# ---------- COMMAND PROCESSING ----------
def process_command(c: str) -> str:
    print(f"[Command] {c}")
    q = (c or "").strip()
    low = q.lower()

    # Quick site opens
    mapping = {
        "open google": "https://google.com",
        "open facebook": "https://facebook.com",
        "open youtube": "https://youtube.com",
        "open instagram": "https://instagram.com",
    }
    for key, url in mapping.items():
        if key in low:
            try:
                webbrowser.open(url)
            except Exception:
                pass
            return f"Opening {url.split('//')[-1]}"

    # Play command (multi-word)
    if low.startswith("play ") or low == "play":
        song = q[5:].strip() if len(q) > 4 else ""
        if not song:
            return "Say 'play' followed by a song name."
        link = None
        if musiclibrary and getattr(musiclibrary, "music", None):
            link = musiclibrary.music.get(song.lower()) or musiclibrary.music.get(song)
        if link:
            try:
                webbrowser.open(link)
            except Exception:
                pass
            return f"Playing {song}"
        return "Sorry, I couldn't find that song."

    # Fallback to Gemini
    return ask_gemini(q)

# ---------- ROUTES ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])  # ✅ Now supports both
def chat():
    try:
        if request.method == "POST":
            message = request.form.get("message", "").strip()
        else:  # GET
            message = request.args.get("message", "").strip()

        if not message:
            return Response("No message received.", mimetype="text/plain", status=400)

        reply = process_command(message)
        return Response(reply, mimetype="text/plain")
    except Exception as e:
        return Response(f"Error: {e}", mimetype="text/plain", status=500)

@app.route("/reset", methods=["POST"])  # also plain text
def reset():
    return Response("OK", mimetype="text/plain")

# Global error handler -> always plain text
@app.errorhandler(Exception)
def handle_exception(e):
    return Response(f"Server error: {e}", mimetype="text/plain", status=500)

# ---------- MAIN ----------
if __name__ == "__main__":
    try:
        speak("Starting Jarvis server...")
    except Exception:
        pass
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)

