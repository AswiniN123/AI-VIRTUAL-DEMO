# backend/app.py
import sys
import os

# This line tells Python to look in the root ai_tutor folder for modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.routes import api
from database.database import init_db

def create_app():
    app = Flask(__name__,
                static_folder="../frontend",
                template_folder="../frontend")
    CORS(app)
    app.register_blueprint(api)

    @app.route("/")
    def index():
        return send_from_directory("../frontend", "index.html")

    @app.route("/TalkingHead/<path:filename>")
    def talkinghead_files(filename):
        return send_from_directory("../TalkingHead", filename)

    return app

if __name__ == "__main__":
    init_db()
    app = create_app()
    print("AI Tutor running at http://localhost:5000")
    app.run(debug=True)
