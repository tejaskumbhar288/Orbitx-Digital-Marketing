#!/usr/bin/env python3
"""
Test complete SMS workflow - quote submission to SMS notification
"""

import requests
import json

def test_sms_quote_workflow():
    """Test the complete workflow: quote submission -> AI analysis -> SMS"""

    print("=== TESTING COMPLETE SMS WORKFLOW ===")

    # High-value test quote to trigger high priority
    quote_data = {
        "client_name": "Premium SMS Client",
        "email": "premium@sms.com",
        "phone": "9876543210",
        "company_name": "Premium SMS Co",
        "services_requested": "logo-design",
        "project_description": "Need a luxury brand logo for high-end fashion startup with premium aesthetics and international appeal",
        "budget_range": "10000+",
        "timeline": "urgent",
        "additional_requirements": "Vector format, multiple variations, complete branding package"
    }

    url = "http://127.0.0.1:5000/quote/simple"

    try:
        print("Submitting high-value quote to trigger SMS...")
        print(f"Client: {quote_data['client_name']}")
        print(f"Budget: {quote_data['budget_range']}")
        print(f"Service: {quote_data['services_requested']}")

        # Send quote request
        response = requests.post(url, json=quote_data)

        print(f"\nResponse Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ SUCCESS: Quote submitted successfully!")
                print(f"📋 Quote ID: {result.get('quote_id')}")
                print("\n🔄 BACKGROUND PROCESS STARTED:")
                print("   1. AI analyzing quote priority and value...")
                print("   2. Generating SMS with AI insights...")
                print("   3. Sending SMS to +919518536672...")
                print("\n📱 CHECK YOUR PHONE: SMS should arrive in 1-2 minutes!")
                print("\nExpected SMS content:")
                print("- Priority level (likely HIGH PRIORITY)")
                print("- Client and project details")
                print("- AI estimated value")
                print("- Action required")
            else:
                print(f"❌ ERROR: {result.get('error')}")
        else:
            print(f"❌ ERROR: HTTP {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"❌ ERROR: {e}")

    print("\n" + "="*50)
    print("📊 MONITORING:")
    print("- Check Flask logs for AI analysis results")
    print("- Check your phone for SMS notification")
    print("- SMS should include AI priority score")

if __name__ == "__main__":
    test_sms_quote_workflow()