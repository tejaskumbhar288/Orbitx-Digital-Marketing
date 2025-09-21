#!/usr/bin/env python3
"""
Simple test for AI WhatsApp functionality
"""

import requests

# Test data
quote_data = {
    "client_name": "Test AI Client",
    "email": "test@ai.com",
    "phone": "1234567890",
    "company_name": "AI Test Company",
    "services_requested": "logo-design",
    "project_description": "Need a modern AI-themed logo for our tech startup",
    "budget_range": "15000-25000",
    "timeline": "urgent"
}

print("Testing AI-enhanced WhatsApp functionality...")

try:
    response = requests.post("http://127.0.0.1:5000/quote", data=quote_data)
    print(f"Response status: {response.status_code}")

    if response.status_code in [200, 302]:
        print("SUCCESS: Quote submitted and AI analysis should be running")
        print("Check Flask logs for AI analysis results")
        print("WhatsApp Web should have opened automatically")
    else:
        print("ERROR: Quote submission failed")

except Exception as e:
    print(f"ERROR: {e}")