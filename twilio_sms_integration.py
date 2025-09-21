#!/usr/bin/env python3
"""
Twilio SMS integration for quote notifications
Much more reliable than WhatsApp Web automation
"""

import os
import asyncio
from dotenv import load_dotenv
import openai
from twilio.rest import Client

# Load environment
load_dotenv()

class AIEnhancedSMS:
    def __init__(self):
        # Twilio configuration
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')  # Your Twilio number
        self.target_phone_number = os.getenv('TARGET_PHONE_NUMBER', '+919518536672')  # Your phone

        # OpenAI configuration
        self.openai_api_key = os.getenv('OPENAI_API_KEY')

        # Initialize clients
        if self.twilio_account_sid and self.twilio_auth_token:
            self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
        else:
            self.twilio_client = None

        if self.openai_api_key:
            self.openai_client = openai.AsyncOpenAI(api_key=self.openai_api_key)
        else:
            self.openai_client = None

    async def analyze_quote_with_ai(self, quote_data):
        """Analyze quote with OpenAI for priority and value estimation"""
        if not self.openai_client:
            return {"priority": 5, "estimated_value": "Rs 5,000-15,000", "strategy": "Standard response"}

        try:
            prompt = f"""Analyze this design quote briefly:
            Client: {quote_data.get('client_name')}
            Service: {quote_data.get('services_requested')}
            Budget: {quote_data.get('budget_range', 'Not specified')}
            Description: {quote_data.get('project_description', '')[:200]}

            Provide priority (1-10) and estimated value in rupees in this format:
            Priority: X/10
            Value: Rs X,XXX-X,XXX"""

            response = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )

            result = response.choices[0].message.content

            # Extract priority and value
            priority = 5
            value = "Rs 5,000-15,000"

            lines = result.split('\n')
            for line in lines:
                if 'Priority:' in line or 'priority:' in line.lower():
                    try:
                        priority = int(line.split(':')[1].split('/')[0].strip())
                    except:
                        pass
                if 'Value:' in line or 'value:' in line.lower():
                    try:
                        value = line.split(':')[1].strip()
                    except:
                        pass

            return {
                "priority": priority,
                "estimated_value": value,
                "strategy": "AI-analyzed response"
            }

        except Exception as e:
            print(f"AI analysis error: {e}")
            return {"priority": 5, "estimated_value": "Rs 5,000-15,000", "strategy": "Standard response"}

    def generate_sms_message(self, quote_data, analysis):
        """Generate enhanced SMS message with AI insights"""

        # Priority indicators
        priority_text = "HIGH PRIORITY" if analysis['priority'] >= 8 else "MEDIUM PRIORITY" if analysis['priority'] >= 6 else "STANDARD"

        # Create concise SMS message (SMS has 160 char limit, so we'll use multiple messages)
        message = f"""NEW QUOTE - OrbitX ({priority_text})

Client: {quote_data.get('client_name')}
Email: {quote_data.get('email')}
Service: {quote_data.get('services_requested')}
Budget: {quote_data.get('budget_range', 'Not specified')}

AI Analysis:
Priority: {analysis['priority']}/10
Est. Value: {analysis['estimated_value']}

Description: {quote_data.get('project_description', '')[:100]}...

Action: Send quote to {quote_data.get('email')}"""

        return message

    def send_sms(self, message):
        """Send SMS via Twilio"""
        if not self.twilio_client:
            return {
                "success": False,
                "error": "Twilio not configured"
            }

        try:
            # Twilio SMS
            sms = self.twilio_client.messages.create(
                body=message,
                from_=self.twilio_phone_number,
                to=self.target_phone_number
            )

            return {
                "success": True,
                "message_sid": sms.sid,
                "status": sms.status
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def process_quote_request(self, quote_data):
        """Complete process: analyze + generate + send SMS"""
        try:
            print("Analyzing quote with AI...")
            analysis = await self.analyze_quote_with_ai(quote_data)

            print("Generating enhanced SMS message...")
            message = self.generate_sms_message(quote_data, analysis)

            print("Sending SMS...")
            sms_result = self.send_sms(message)

            return {
                "success": sms_result["success"],
                "analysis": analysis,
                "message": message,
                "sms_result": sms_result
            }

        except Exception as e:
            print(f"Error processing quote: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Function for easy integration with Flask
async def send_ai_enhanced_sms(quote_data):
    """Simple function to call from Flask app"""
    ai_sms = AIEnhancedSMS()
    return await ai_sms.process_quote_request(quote_data)

# Test the functionality
if __name__ == "__main__":
    test_quote = {
        "client_name": "Test SMS Client",
        "email": "test@sms.com",
        "phone": "1234567890",
        "company_name": "SMS Test Company",
        "services_requested": "logo-design",
        "project_description": "Need a modern logo for our tech startup",
        "budget_range": "10000-20000",
        "timeline": "urgent"
    }

    print("Testing AI-enhanced SMS integration...")
    result = asyncio.run(send_ai_enhanced_sms(test_quote))

    if result['success']:
        print("SUCCESS! AI analysis completed and SMS sent.")
        print(f"Priority: {result['analysis']['priority']}/10")
        print(f"Estimated Value: {result['analysis']['estimated_value']}")
        print(f"SMS Status: {result['sms_result']['status']}")
    else:
        print(f"FAILED: {result['error']}")