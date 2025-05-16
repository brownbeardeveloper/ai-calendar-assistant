"""
Chat controller for the Calendar Assistant.
Handles interactions between UI and chat history model.
"""

from calendar_assistant.models.chat_model import ChatModel


class ChatController:
    """Controller for managing chat operations."""

    def __init__(self, model=None):
        """Initialize the chat controller with a model."""
        self.model = model or ChatModel()
        self.model.load_history()
        pass

    def add_user_message(self, content):
        """Add a user message to chat history."""
        if not content or not content.strip():
            return {"success": False, "error": "Message content cannot be empty"}

        message = self.model.add_message("user", content)
        return {"success": True, "message": message}
        pass

    def add_assistant_message(self, content):
        """Add an assistant message to chat history."""
        if not content or not content.strip():
            return {"success": False, "error": "Message content cannot be empty"}

        message = self.model.add_message("assistant", content)
        return {"success": True, "message": message}
        pass

    def get_conversation_history(self, limit=None):
        """Get conversation history, optionally limited."""
        messages = self.model.get_messages(limit)
        return {"success": True, "messages": messages, "count": len(messages)}
        pass

    def clear_conversation(self):
        """Clear the conversation history."""
        success = self.model.clear_history()
        return {"success": success}
        pass

    def search_conversation(self, query):
        """Search conversation for a query string."""
        if not query or not query.strip():
            return {"success": False, "error": "Search query cannot be empty"}

        results = self.model.search_messages(query)
        return {"success": True, "messages": results, "count": len(results)}
        pass

    def get_ai_context(self, message_count=10):
        """Get formatted conversation context for AI processing."""
        context = self.model.get_context_for_ai(message_count)
        return {"success": True, "context": context}
        pass

    def process_conversation(self, user_message, ai_processor):
        """Process a user message through the conversation flow."""
        # Add user message to history
        self.add_user_message(user_message)

        # Get conversation context for AI
        context_result = self.get_ai_context()

        if not context_result["success"]:
            return {"success": False, "error": "Failed to get conversation context"}

        # Process with AI
        ai_response = ai_processor(context_result["context"], user_message)

        # Add AI response to history
        self.add_assistant_message(ai_response)

        return {
            "success": True,
            "user_message": user_message,
            "assistant_response": ai_response,
        }
        pass
