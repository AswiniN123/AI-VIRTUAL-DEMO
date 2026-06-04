# backend/db_service.py
# This file is a bridge between routes.py and database.py
# It makes it easy to call database functions from the backend routes

from database.database import (
    create_session,
    update_session_title,
    save_message,
    get_all_sessions,
    get_messages,
    delete_session,
    delete_all_sessions
)

def new_session(title="New Chat"):
    """Create a new chat session"""
    return create_session(title)

def rename_session(session_id, title):
    """Update the title of a session"""
    update_session_title(session_id, title)

def store_message(session_id, role, content):
    """
    Save a message to the database.
    role must be either 'user' or 'assistant'
    """
    save_message(session_id, role, content)

def fetch_all_sessions():
    """Return all sessions for the history sidebar"""
    return get_all_sessions()

def fetch_messages(session_id):
    """Return all messages for one session (used for AI memory + loading old chats)"""
    return get_messages(session_id)

def remove_session(session_id):
    """Delete one session and all its messages"""
    delete_session(session_id)

def remove_all_sessions():
    """Wipe all chat history from the database"""
    delete_all_sessions()