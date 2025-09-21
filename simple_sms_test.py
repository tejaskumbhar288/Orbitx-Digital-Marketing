#!/usr/bin/env python3
"""
Simple SMS test without emoji issues
"""

import requests

# Test quote data
quote_data = {
    "client_name": "SMS Test Client",
    "email": "smstest@example.com",
    "phone": "9999999999",
    "company_name": "SMS Test Co",
    "services_requested": "logo-design",
    "project_description": "Need a premium logo for luxury brand startup",
    "budget_range": "10000+",
    "timeline": "urgent"
}

print("TESTING SMS WORKFLOW")
print("Submitting quote to trigger AI analysis and SMS...")

try:
    response = requests.post("http://127.0.0.1:5000/quote/simple", json=quote_data)

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print("SUCCESS: Quote submitted!")
            print(f"Quote ID: {result.get('quote_id')}")
            print("")
            print("BACKGROUND PROCESS:")
            print("1. AI analyzing quote...")
            print("2. Sending SMS to +919518536672...")
            print("")
            print("CHECK YOUR PHONE for SMS in 1-2 minutes!")
        else:
            print(f"ERROR: {result.get('error')}")
    else:
        print("Failed to submit quote")

except Exception as e:
    print(f"Error: {e}")

print("")
print("Check Flask logs for SMS status")