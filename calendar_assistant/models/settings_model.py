"""
Settings model for the Calendar Assistant.
Handles storage and retrieval of application settings.
"""

import json
import os
from pathlib import Path


class SettingsModel:
    """Model for settings data storage and operations."""

    def __init__(self, settings_file=None):
        """Initialize the settings model with settings file path."""
        self.settings_file = settings_file or "data/settings.json"
        self.settings = {
            "theme": "dark",
            "model_name": "gpt-4.1-nano",
            "ui_width": 120,
            "ui_height": 40,
            "api_timeout": 30,
        }
        pass

    def load_settings(self):
        """Load settings from storage."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as f:
                    loaded_settings = json.load(f)
                    # Update settings but keep defaults for missing values
                    self.settings.update(loaded_settings)
            return self.settings
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.settings
        pass

    def save_settings(self):
        """Save settings to storage."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)

            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
        pass

    def get_setting(self, key, default=None):
        """Get a specific setting value."""
        return self.settings.get(key, default)
        pass

    def update_setting(self, key, value):
        """Update a specific setting value."""
        self.settings[key] = value
        self.save_settings()
        return True
        pass

    def reset_to_defaults(self):
        """Reset settings to default values."""
        self.settings = {
            "theme": "dark",
            "model_name": "gpt-4.1-nano",
            "ui_width": 120,
            "ui_height": 40,
            "api_timeout": 30,
        }
        self.save_settings()
        return True
        pass
