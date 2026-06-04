# database/models.py
# This file describes the structure of our database tables

# TABLE 1: sessions
# Stores each chat session (one session = one conversation)
# id          - unique number for each session
# title       - first question asked (used as chat title)
# created_at  - when the chat was started

# TABLE 2: messages
# Stores every single message in every chat
# id          - unique number for each message
# session_id  - which chat this message belongs to
# role        - "user" or "assistant"
# content     - the actual message text
# created_at  - when the message was sent