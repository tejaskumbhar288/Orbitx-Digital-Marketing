#!/usr/bin/env python3
"""
Test AI-enhanced WhatsApp workflow
"""

import requests
import time
import random

def test_quote_submission():
    """Test the complete AI-enhanced quote workflow"""

    print("=== AI-ENHANCED WHATSAPP WORKFLOW TEST ===\n")

    # Test data
    test_quotes = [
        {
            "client_name": "AI Test Client",
            "email": "aitest@example.com",
            "phone": "1234567890",
            "company_name": "AI Innovations Ltd",
            "services_requested": "logo-design",
            "project_description": "Need a modern AI-themed logo for our tech startup with clean, futuristic design",
            "budget_range": "15000-25000",
            "timeline": "urgent",
            "additional_requirements": "Vector format required, multiple color variations"
        },
        {
            "client_name": "Budget Client",
            "email": "budget@example.com",
            "phone": "9876543210",
            "company_name": "Small Business Co",
            "services_requested": "web-design",
            "project_description": "Simple website for local restaurant",
            "budget_range": "5000-10000",
            "timeline": "flexible",
            "additional_requirements": "Mobile responsive needed"
        }
    ]

    flask_url = "http://127.0.0.1:5000/quote"

    for i, quote_data in enumerate(test_quotes, 1):
        print(f"--- Test {i}: {quote_data['client_name']} ---")

        try:
            # First get the quote page to get CSRF token
            session = requests.Session()
            get_response = session.get(flask_url)

            if get_response.status_code == 200:
                print("[OK] Quote page accessible")

                # Extract CSRF token (simplified - in real scenario would parse HTML)
                # For now, just test with form data

                # Submit quote request
                post_response = session.post(flask_url, data=quote_data)

                if post_response.status_code == 200 or post_response.status_code == 302:
                    print("[OK] Quote submitted successfully")
                    print(f"   Client: {quote_data['client_name']}")
                    print(f"   Budget: {quote_data['budget_range']}")
                    print(f"   Service: {quote_data['services_requested']}")
                    print("   -> AI analysis should be running in background")
                    print("   -> WhatsApp Web should open automatically")
                else:
                    print(f"[ERROR] Quote submission failed: {post_response.status_code}")

            else:
                print(f"[ERROR] Cannot access quote page: {get_response.status_code}")

        except Exception as e:
            print(f"[ERROR] Test failed: {e}")

        print()
        time.sleep(3)  # Wait between tests

    print("EXPECTED RESULTS:")
    print("1. Flask logs should show 'AI-enhanced WhatsApp URL opened'")
    print("2. WhatsApp Web should open with AI-analyzed messages")
    print("3. Messages should include priority scores and estimated values")
    print("4. High-value quotes should have fire emoji")
    print("5. Lower-value quotes should have note emoji")

    print("\nWorkflow test completed!")
    print("Check Flask console logs for AI analysis results.")

if __name__ == "__main__":
    test_quote_submission()