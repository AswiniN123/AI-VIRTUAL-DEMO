import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT_DIR, ".env"))

from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.routes import api
from database.database import init_db

app = Flask(__name__)
CORS(app)
app.register_blueprint(api)

# Serve index.html
@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

# Serve ALL frontend files (css, js)
@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory("frontend", filename)

@app.route("/TalkingHead/<path:filename>")
def talkinghead_files(filename):
    return send_from_directory("TalkingHead", filename)

if __name__ == "__main__":
    init_db()
    print("=" * 40)
    print("  AI Virtual Tutor is starting...")
    print("  Open: http://localhost:5000")
    print("=" * 40)
    app.run(debug=True)
