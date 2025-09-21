#!/usr/bin/env python3
"""
Create chatbot database tables
"""

from app import app, db
from models import ChatConversation, ChatMessage

def create_chatbot_tables():
    """Create the chatbot tables"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("SUCCESS: Created chatbot database tables:")
            print("   - chat_conversations")
            print("   - chat_messages")
            print("\nChatbot database setup complete!")

        except Exception as e:
            print(f"ERROR: Creating tables failed: {e}")
            return False

        return True

if __name__ == '__main__':
    create_chatbot_tables()