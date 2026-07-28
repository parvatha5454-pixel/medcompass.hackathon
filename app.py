"""
MedCompass - Automated Voice & Visual Medication Compliance
Compass Crew AI Innovation Challenge 2026 - Track 2 (Healthcare & Social Impact)

A simple Flask app that helps elderly patients manage medication schedules
using voice reminders (gTTS) and simple color-coded visual icons.
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "medcompass.db")
AUDIO_DIR = os.path.join(BASE_DIR, "static", "audio")

os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# Supported languages for voice reminders (gTTS language codes)
LANGUAGES = {
    "ta": "Tamil",
    "hi": "Hindi",
    "en": "English",
    "te": "Telugu",
    "kn": "Kannada",
}

# Simple icon-color mapping so non-readers can identify medicines visually
ICON_COLORS = ["red", "blue", "green", "yellow", "purple", "orange"]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            time TEXT NOT NULL,
            language TEXT NOT NULL,
            icon_color TEXT NOT NULL,
            taken_today INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    medicines = conn.execute(
        "SELECT * FROM medicines ORDER BY time ASC"
    ).fetchall()
    conn.close()
    return render_template("index.html", medicines=medicines, languages=LANGUAGES)


@app.route("/add", methods=["POST"])
def add_medicine():
    name = request.form.get("name", "").strip()
    time = request.form.get("time", "").strip()
    language = request.form.get("language", "en")

    if not name or not time:
        return redirect(url_for("index"))

    conn = get_db()
    count = conn.execute("SELECT COUNT(*) as c FROM medicines").fetchone()["c"]
    icon_color = ICON_COLORS[count % len(ICON_COLORS)]

    conn.execute(
        "INSERT INTO medicines (name, time, language, icon_color, created_at) VALUES (?, ?, ?, ?, ?)",
        (name, time, language, icon_color, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/speak/<int:med_id>", methods=["POST"])
def speak_reminder(med_id):
    """Generate a voice reminder audio file for a medicine using gTTS."""
    conn = get_db()
    med = conn.execute("SELECT * FROM medicines WHERE id = ?", (med_id,)).fetchone()
    conn.close()

    if med is None:
        return jsonify({"error": "Medicine not found"}), 404

    # Build the reminder message in the chosen language
    messages = {
        "ta": f"{med['name']} சாப்பிட நேரம் ஆகிவிட்டது. தயவுசெய்து மருந்தை எடுத்துக் கொள்ளுங்கள்.",
        "hi": f"{med['name']} लेने का समय हो गया है। कृपया अपनी दवा लें।",
        "te": f"{med['name']} తీసుకునే సమయం అయింది. దయచేసి మీ మందు తీసుకోండి.",
        "kn": f"{med['name']} ತೆಗೆದುಕೊಳ್ಳುವ ಸಮಯ ಆಗಿದೆ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಔಷಧಿ ತೆಗೆದುಕೊಳ್ಳಿ.",
        "en": f"It is time to take your medicine, {med['name']}. Please take it now.",
    }
    text = messages.get(med["language"], messages["en"])

    if not GTTS_AVAILABLE:
        return jsonify({"error": "gTTS not installed on this machine. Run: pip install gtts"}), 500

    try:
        filename = f"reminder_{med_id}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        tts = gTTS(text=text, lang=med["language"])
        tts.save(filepath)
        return jsonify({"audio_url": url_for("static", filename=f"audio/{filename}"), "text": text})
    except Exception as e:
        # gTTS needs internet access to reach Google's TTS service
        return jsonify({"error": f"Could not generate voice (check internet connection): {str(e)}"}), 500


@app.route("/mark_taken/<int:med_id>", methods=["POST"])
def mark_taken(med_id):
    conn = get_db()
    conn.execute("UPDATE medicines SET taken_today = 1 WHERE id = ?", (med_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:med_id>", methods=["POST"])
def delete_medicine(med_id):
    conn = get_db()
    conn.execute("DELETE FROM medicines WHERE id = ?", (med_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
