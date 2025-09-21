#!/usr/bin/env python3
"""
Direct SMS test to verify Twilio functionality
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment
load_dotenv()

def test_sms_direct():
    """Test SMS functionality directly"""

    print("=== DIRECT SMS TEST ===")

    # Check credentials
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_PHONE_NUMBER')
    to_number = os.getenv('TARGET_PHONE_NUMBER')

    print(f"Account SID: {account_sid[:10]}...")
    print(f"From Number: {from_number}")
    print(f"To Number: {to_number}")

    if not all([account_sid, auth_token, from_number, to_number]):
        print("[FAIL] Missing Twilio credentials")
        return False

    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)

        # Test message
        message = """TEST - OrbitX SMS System

This is a test of the AI-enhanced quote notification system.

System Status: OPERATIONAL
Test Time: Just now
Features: AI Analysis + SMS Notifications

If you received this, the system is working perfectly!"""

        print("Sending test SMS...")

        # Send SMS
        sms = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )

        print(f"[PASS] SMS sent successfully!")
        print(f"Message SID: {sms.sid}")
        print(f"Status: {sms.status}")
        print(f"To: {sms.to}")
        print(f"From: {sms.from_}")

        return True

    except Exception as e:
        print(f"[FAIL] SMS sending failed: {e}")
        return False

if __name__ == "__main__":
    success = test_sms_direct()
    if success:
        print("\n[SUCCESS] SMS system is working perfectly!")
        print("Check your phone for the test message.")
    else:
        print("\n[FAILURE] SMS system has issues.")