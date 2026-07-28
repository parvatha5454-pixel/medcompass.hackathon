# 🧭 MedCompass — Automated Voice & Visual Medication Compliance

**Compass Crew AI Innovation Challenge 2026 — Track 2: Healthcare & Social Impact**

## Problem
Elderly patients often miss doses or take the wrong medicine because of complex
schedules, poor eyesight, language barriers, and low tech literacy. Existing
reminder apps are text-heavy and not senior-friendly.

## Solution
MedCompass is a simple web app that helps elderly patients and their caregivers
manage medication schedules through:
- 🔊 **Voice reminders** in the patient's native language (Tamil, Hindi, Telugu, Kannada, English) using gTTS
- 🎨 **Color-coded visual icons** for each medicine so even non-readers can identify them
- ✅ **One-tap "Mark Taken"** confirmation
- 📋 A simple, large-text dashboard designed for elderly users

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite
- **Voice:** gTTS (Google Text-to-Speech)
- **Frontend:** HTML, CSS, JavaScript (no frameworks — kept simple for accessibility)

## Features (Prototype)
- Add a medicine with name, time, and preferred language
- Each medicine gets an auto-assigned color icon
- Click "Remind" to hear a spoken reminder in the chosen language
- Mark medicine as taken for the day
- Delete a medicine from the schedule

## Setup Instructions

```bash
# 1. Clone the repository
git clone <repo-url>
cd MedCompass

# 2. Install dependencies
pip install flask gtts

# 3. Run the app
python app.py

# 4. Open in browser
http://127.0.0.1:5000
```

> **Note:** gTTS requires an active internet connection since it uses Google's
> Text-to-Speech service to generate audio.

## Future Scope
- Voice-based confirmation ("Did you take it?") instead of tap-only
- Caregiver dashboard with SMS/WhatsApp alerts on missed doses
- Integration with pharmacy APIs for refill reminders
- Support for more regional languages
- Offline voice reminders using on-device TTS

## Team
Compass Crew AI Innovation Challenge 2026 — Individual/Team Submission

## Contact
compasscrewnetwork.team@gmail.com
