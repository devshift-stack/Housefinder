#!/usr/bin/env python
"""
Quick start script for Housefinder
Run this to setup and test the system
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import HousefinderApp
from src.utils import setup_logger

logger = setup_logger(__name__)


def main():
    """Quick start guide"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🏠 HOUSEFINDER - Automated Accommodation Finder        ║
    ║                                                           ║
    ║   Version 4.0                                            ║
    ║   Step2Job GmbH                                          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Welcome to Housefinder!
    
    This quick start script will help you setup and run the system.
    
    Choose an option:
    
    1. Setup Google Sheets (run once)
    2. Process all employees (one-time run)
    3. Run in scheduled mode (continuous)
    4. Test configuration
    5. Exit
    """)
    
    choice = input("Enter your choice (1-5): ").strip()
    
    app = HousefinderApp()
    
    if choice == "1":
        print("\n🔧 Setting up Google Sheets...")
        try:
            app.setup_sheets()
            print("✅ Google Sheets setup complete!")
            print("\nNext steps:")
            print("1. Open your Google Sheet")
            print("2. Add employee data to the 'Mitarbeiter' tab")
            print("3. Run option 2 to process employees")
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Setup failed: {e}")
    
    elif choice == "2":
        print("\n🔍 Processing all employees (one-time run)...")
        try:
            app.process_all_employees()
            print("✅ Processing complete!")
            print("Check the 'Ergebnisse' tab in your Google Sheet for results.")
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Processing failed: {e}")
    
    elif choice == "3":
        print("\n⏰ Starting scheduled mode...")
        print("The system will run continuously:")
        print("  - Urgent employees: every 2 hours")
        print("  - Normal employees: every 24 hours")
        print("\nPress Ctrl+C to stop")
        try:
            app.run_scheduled()
        except KeyboardInterrupt:
            print("\n\n👋 Stopped by user")
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Scheduled mode failed: {e}")
    
    elif choice == "4":
        print("\n🔍 Testing configuration...")
        test_configuration()
    
    elif choice == "5":
        print("\n👋 Goodbye!")
        sys.exit(0)
    
    else:
        print("❌ Invalid choice. Please run again and choose 1-5.")


def test_configuration():
    """Test if configuration is complete"""
    from src.config import settings
    
    print("\nChecking configuration...\n")
    
    issues = []
    
    # Check Google Sheets
    if not settings.GOOGLE_SHEET_ID:
        issues.append("❌ GOOGLE_SHEET_ID not set")
    else:
        print("✅ Google Sheet ID configured")
    
    if not os.path.exists(settings.GOOGLE_SHEETS_CREDENTIALS_PATH):
        issues.append("❌ Google credentials file not found")
    else:
        print("✅ Google credentials file found")
    
    # Check Email
    if not settings.SENDGRID_API_KEY:
        issues.append("❌ SENDGRID_API_KEY not set")
    else:
        print("✅ SendGrid API key configured")
    
    # Check WhatsApp
    if not settings.WHATSAPP_ACCESS_TOKEN:
        issues.append("⚠️  WhatsApp access token not set (optional)")
    else:
        print("✅ WhatsApp access token configured")
    
    # Check OpenAI
    if not settings.OPENAI_API_KEY:
        issues.append("❌ OPENAI_API_KEY not set")
    else:
        print("✅ OpenAI API key configured")
    
    if issues:
        print("\n⚠️  Configuration issues found:")
        for issue in issues:
            print(f"  {issue}")
        print("\nPlease update your .env file with the required credentials.")
    else:
        print("\n✅ All required configuration is complete!")
        print("You can now run the application.")


if __name__ == "__main__":
    main()
