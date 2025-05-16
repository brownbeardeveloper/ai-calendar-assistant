"""
Chat history model for the Calendar Assistant.
Handles storage and retrieval of chat messages.
"""

import json
import os
from pathlib import Path
from datetime import datetime


class ChatModel:
    """Model for chat history data storage and operations."""

    def __init__(self, history_file=None):
        """Initialize the chat model with history file path."""
        self.history_file = history_file or "data/chat_history.json"
        self.messages = []
        pass

    def load_history(self):
        """Load chat history from storage."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r") as f:
                    self.messages = json.load(f)
            return self.messages
        except Exception as e:
            print(f"Error loading chat history: {e}")
            return []
        pass

    def save_history(self):
        """Save chat history to storage."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)

            with open(self.history_file, "w") as f:
                json.dump(self.messages, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving chat history: {e}")
            return False
        pass

    def add_message(self, sender, content):
        """Add a message to the chat history."""
        message = {
            "sender": sender,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        }

        self.messages.append(message)
        self.save_history()
        return message
        pass

    def get_messages(self, limit=None):
        """Get chat messages, optionally limited to a count."""
        if limit and limit > 0:
            return self.messages[-limit:]
        return self.messages
        pass

    def clear_history(self):
        """Clear the chat history."""
        self.messages = []
        self.save_history()
        return True
        pass

    def search_messages(self, query):
        """Search messages for a query string."""
        results = []

        for message in self.messages:
            content = message.get("content", "").lower()
            if query.lower() in content:
                results.append(message)

        return results
        pass

    def get_context_for_ai(self, message_count=10):
        """Get recent message context formatted for AI processing."""
        recent_messages = self.get_messages(limit=message_count)

        # Format messages for AI context
        formatted_context = []
        for message in recent_messages:
            sender = message.get("sender", "")
            content = message.get("content", "")
            role = "user" if sender.lower() == "user" else "assistant"

            formatted_context.append({"role": role, "content": content})

        return formatted_context
        pass
