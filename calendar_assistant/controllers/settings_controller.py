"""
Settings controller for the Calendar Assistant.
Handles interactions between UI and settings data model.
"""

from calendar_assistant.models.settings_model import SettingsModel


class SettingsController:
    """Controller for managing application settings."""

    def __init__(self, model=None):
        """Initialize the settings controller with a model."""
        self.model = model or SettingsModel()
        self.model.load_settings()
        pass

    def get_theme(self):
        """Get the current UI theme setting."""
        theme = self.model.get_setting("theme", "dark")
        return {"success": True, "theme": theme}
        pass

    def set_theme(self, theme):
        """Set the UI theme."""
        if not theme or theme not in ["dark", "light"]:
            return {"success": False, "error": "Invalid theme value"}

        self.model.update_setting("theme", theme)
        return {"success": True, "theme": theme}
        pass

    def get_model_name(self):
        """Get the current AI model name setting."""
        model_name = self.model.get_setting("model_name", "gpt-4.1-nano")
        return {"success": True, "model_name": model_name}
        pass

    def set_model_name(self, model_name):
        """Set the AI model name."""
        if not model_name:
            return {"success": False, "error": "Invalid model name"}

        self.model.update_setting("model_name", model_name)
        return {"success": True, "model_name": model_name}
        pass

    def get_all_settings(self):
        """Get all application settings."""
        settings = self.model.settings
        return {"success": True, "settings": settings}
        pass

    def update_settings(self, settings_dict):
        """Update multiple settings at once."""
        if not isinstance(settings_dict, dict):
            return {"success": False, "error": "Settings must be a dictionary"}

        for key, value in settings_dict.items():
            self.model.update_setting(key, value)

        return {"success": True, "settings": self.model.settings}
        pass

    def reset_settings(self):
        """Reset all settings to default values."""
        self.model.reset_to_defaults()
        return {"success": True, "settings": self.model.settings}
        pass
