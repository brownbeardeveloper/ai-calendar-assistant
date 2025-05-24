#!/usr/bin/env python3
"""
Google Calendar Setup Helper

This script guides you through setting up Google Calendar integration.
Run this once to get your calendar connected.
"""

import os
import sys


def check_credentials():
    """Check for credentials file."""
    print("🔍 Checking for credentials...")

    creds_file = "credentials.json"
    if os.path.exists(creds_file):
        print(f"✓ Found {creds_file}")
        return True
    else:
        print(f"❌ {creds_file} not found")
        return False


def setup_instructions():
    """Provide setup instructions."""
    print("\n📋 Google Calendar Setup Instructions")
    print("=" * 50)

    print("\n1. 🌐 Go to Google Cloud Console")
    print("   https://console.cloud.google.com/")

    print("\n2. 📁 Create or select a project")
    print("   - Click the project dropdown")
    print("   - Create new project or select existing")

    print("\n3. 🔧 Enable Calendar API")
    print("   - Go to 'APIs & Services' > 'Library'")
    print("   - Search for 'Google Calendar API'")
    print("   - Click 'Enable'")

    print("\n4. ⚠️  IMPORTANT: Configure OAuth Consent Screen FIRST")
    print("   - Go to 'APIs & Services' > 'OAuth consent screen'")
    print("   - Choose 'External' (unless you have Google Workspace)")
    print("   - Fill in app name: 'Calendar Assistant'")
    print("   - Add your email as user support email")
    print("   - In 'Scopes', add: ../auth/calendar")
    print("   - In 'Test users', ADD YOUR EMAIL ADDRESS")
    print("   - Save and continue through all steps")

    print("\n5. 🔑 Create OAuth2 Credentials")
    print("   - Go to 'APIs & Services' > 'Credentials'")
    print("   - Click 'Create Credentials' > 'OAuth client ID'")
    print("   - Choose 'Desktop application' (NOT web application)")
    print("   - Give it a name like 'Calendar Assistant'")

    print("\n6. 📥 Download Credentials")
    print("   - Click the download button next to your OAuth client")
    print("   - Save the file as 'credentials.json' in this directory:")
    print(f"   {os.getcwd()}")

    print("\n7. 🚀 Test the integration")
    print("   - Run this script again: python3 setup_google_calendar.py")
    print("   - It will open a browser for authentication")
    print("   - You may see 'This app isn't verified' - click 'Advanced'")
    print("   - Click 'Go to Calendar Assistant (unsafe)'")
    print("   - Grant calendar permissions")

    print("\n💡 Common Issues:")
    print("   - Error 403: Make sure you added your email to test users")
    print("   - 'App in testing mode': Add your email to test users OR publish the app")
    print(
        "   - Detailed troubleshooting: docs/google_calendar_setup_troubleshooting.md"
    )


def handle_auth_error():
    """Provide guidance for authentication errors."""
    print("\n❌ Authentication Error Detected")
    print("=" * 40)

    print("\n🔍 Most Common Cause: OAuth Consent Screen Issues")
    print("\n📋 Quick Fix Steps:")
    print("1. Go to Google Cloud Console")
    print("2. Navigate to 'APIs & Services' > 'OAuth consent screen'")
    print("3. Make sure you added YOUR EMAIL to 'Test users'")
    print("4. OR click 'Publish App' to make it public")
    print("5. Wait 5-10 minutes for changes to take effect")
    print("6. Delete token.json and try again")

    print("\n🆘 If still having issues:")
    print("   Check: docs/google_calendar_setup_troubleshooting.md")
    print("   Or recreate your OAuth credentials from scratch")


def test_integration():
    """Test the Google Calendar integration."""
    print("\n🧪 Testing Google Calendar integration...")

    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from calendar_assistant.models.google_calendar_model import GoogleCalendarModel

        google_cal = GoogleCalendarModel()

        if google_cal.service:
            print("✅ Google Calendar integration is working!")

            # Try to get calendars
            calendars = google_cal.get_calendars()
            print(f"✓ Connected to {len(calendars)} calendar(s)")

            if calendars:
                print("📅 Your calendars:")
                for cal in calendars:
                    primary = " (primary)" if cal.get("primary") else ""
                    print(f"   - {cal.get('name')}{primary}")

            return True
        else:
            print("⚠️  Authentication needed")
            return False

    except Exception as e:
        error_msg = str(e).lower()
        print(f"❌ Error: {e}")

        # Check for common OAuth errors
        if "403" in error_msg or "access_denied" in error_msg:
            handle_auth_error()
        elif "credentials" in error_msg:
            print("\n💡 Try recreating your credentials.json file")

        return False


def main():
    """Main setup flow."""
    print("🎯 Google Calendar Setup Helper")
    print("=" * 40)

    # Check credentials
    has_creds = check_credentials()

    if not has_creds:
        setup_instructions()
        print("\n⏳ After completing the setup, run this script again to test.")
        return

    # Test integration
    if test_integration():
        print("\n🎉 Setup complete! Your Google Calendar is ready to use.")
        print("\nNext steps:")
        print("- Run your calendar assistant")
        print("- Try creating events")
        print("- Your events will sync with Google Calendar")
    else:
        print("\n🔄 Please fix the authentication issue and try again.")

        # Offer to clean up for fresh start
        response = input(
            "\nWould you like to delete token.json for a fresh start? (y/n): "
        )
        if response.lower() in ["y", "yes"]:
            if os.path.exists("token.json"):
                os.remove("token.json")
                print(
                    "✓ Deleted token.json - run this script again to retry authentication"
                )


if __name__ == "__main__":
    main()
