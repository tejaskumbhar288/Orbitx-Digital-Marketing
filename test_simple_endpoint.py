#!/usr/bin/env python3
"""
Test the simple quote endpoint that bypasses form validation
"""

import requests
import json

def test_simple_quote_endpoint():
    """Test the new simple quote endpoint"""

    print("=== TESTING SIMPLE QUOTE ENDPOINT ===")

    # Test data
    quote_data = {
        "client_name": "Simple Test Client",
        "email": "simple@test.com",
        "phone": "9876543210",
        "company_name": "Simple Test Co",
        "services_requested": "logo-design",
        "project_description": "Need a simple logo test for our startup",
        "budget_range": "10000-20000",
        "timeline": "urgent",
        "additional_requirements": "Vector format needed"
    }

    url = "http://127.0.0.1:5000/quote/simple"

    try:
        print("Sending quote request to simple endpoint...")

        # Send as JSON
        response = requests.post(url, json=quote_data)

        print(f"Response Status: {response.status_code}")
        print(f"Response Data: {response.text}")

        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("SUCCESS: Quote submitted via simple endpoint!")
                print(f"Quote ID: {result.get('quote_id')}")
                print("AI analysis should be running in background")
                print("WhatsApp Web should open automatically")
            else:
                print(f"ERROR: {result.get('error')}")
        else:
            print("ERROR: Failed to submit quote")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_simple_quote_endpoint()