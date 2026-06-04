# backend/routes.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from backend.ai_service import get_ai_response, detect_request_type
from backend.openai_service import generate_architecture
from backend.db_service import (
    new_session, rename_session, store_message,
    fetch_all_sessions, fetch_messages,
    remove_session, remove_all_sessions
)

api = Blueprint("api", __name__)

@api.route("/chat", methods=["POST"])
def chat():
    user_message  = request.form.get("message", "")
    session_id    = request.form.get("session_id", type=int)
    student_name  = request.form.get("student_name", "Student")
    file          = request.files.get("file")

    if not session_id:
        session_id = new_session("New Chat")

    history = fetch_messages(session_id)

    if user_message:
        store_message(session_id, "user", user_message)

    if len(history) == 0 and user_message:
        rename_session(session_id, user_message[:50])

    request_type = detect_request_type(user_message)

    if request_type == "diagram" and user_message:
        try:
            result = generate_architecture(user_message, student_name)
            reply = result.get("explanation") or result.get("title") or "Here is the architecture diagram."
            store_message(session_id, "assistant", reply)
            return jsonify({
                "reply": reply,
                "session_id": session_id,
                "response_type": "diagram",
                "title": result.get("title", ""),
                "explanation": result.get("explanation", ""),
                "mermaid": result.get("mermaid", "")
            })
        except Exception as e:
            reply = f"Sorry, I could not generate the architecture diagram: {str(e)}"
            store_message(session_id, "assistant", reply)
            return jsonify({
                "reply": reply,
                "session_id": session_id,
                "response_type": "text"
            })

    reply = get_ai_response(user_message, history, file, student_name)
    store_message(session_id, "assistant", reply)

    return jsonify({
        "reply": reply,
        "session_id": session_id,
        "response_type": "text"
    })


@api.route("/generate-architecture", methods=["POST"])
def architecture():
    payload = request.get_json(silent=True) or {}
    topic = (payload.get("topic") or "").strip()
    student_name = payload.get("student_name", "Student")

    if not topic:
        return jsonify({"error": "Topic is required."}), 400

    try:
        result = generate_architecture(topic, student_name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/sessions", methods=["GET"])
def get_sessions():
    return jsonify(fetch_all_sessions())

@api.route("/sessions/new", methods=["POST"])
def create_new_session():
    session_id = new_session("New Chat")
    return jsonify({"session_id": session_id})

@api.route("/sessions/<int:session_id>/messages", methods=["GET"])
def get_session_messages(session_id):
    return jsonify(fetch_messages(session_id))

@api.route("/sessions/<int:session_id>", methods=["DELETE"])
def delete_one_session(session_id):
    remove_session(session_id)
    return jsonify({"status": "deleted"})

@api.route("/sessions/all", methods=["DELETE"])
def delete_all():
    remove_all_sessions()
    return jsonify({"status": "cleared"})
