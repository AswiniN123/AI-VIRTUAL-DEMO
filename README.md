# AI Virtual Tutor

An AI-powered virtual tutor for real-time student doubt resolution.

## Features
- Text, Voice and Document input
- Talking avatar output (Ms. Aira)
- Chat history with SQLite database
- Explains AI concepts in simple English

## Tech Stack
- Frontend : HTML, CSS, JavaScript
- Backend  : Python, Flask
- AI Model : Groq API (Llama 3.3 70B)
- Database : SQLite
- Voice    : Web Speech API (browser)

## How to Run
1. Install dependencies  : pip install -r requirements.txt
2. Add GROQ_API_KEY in   : .env file
3. Start the server      : python run.py
4. Open in Chrome        : http://localhost:5000      