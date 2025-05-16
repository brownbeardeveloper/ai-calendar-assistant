"""
Settings model for the Calendar Assistant.
Handles storage and retrieval of application settings.
"""

import json
import os


class SettingsModel:
    """Model for settings data storage and operations."""

    def __init__(self, settings_file=None):
        """Initialize the settings model with settings file path."""
        self.settings_file = settings_file or "data/settings.json"
        self.default_settings_file = "data/settings_default.json"
        self.settings = {}
        self.load_settings()

    def load_settings(self):
        """Load settings from storage."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as f:
                    self.settings = json.load(f)
            else:
                print(f"Settings file not found: {self.settings_file}")
            return self.settings
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.settings

    def save_settings(self):
        """Save settings to storage."""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)

            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def get_setting(self, key, default=None):
        """Get a specific setting value."""
        return self.settings.get(key, default)

    def update_setting(self, key, value):
        """Update a specific setting value."""
        self.settings[key] = value
        self.save_settings()
        return True

    def reset_to_defaults(self):
        """Reset settings by loading from the default settings file."""
        try:
            if os.path.exists(self.default_settings_file):
                with open(self.default_settings_file, "r") as f:
                    self.settings = json.load(f)
                # Save the default settings to the current settings file
                self.save_settings()
                print(f"Settings reset to defaults from {self.default_settings_file}")
            else:
                print(f"Default settings file not found: {self.default_settings_file}")
            return True
        except Exception as e:
            print(f"Error resetting settings to defaults: {e}")
            return False
