#!/usr/bin/env python3
"""
Simple AI-enhanced WhatsApp integration for Flask app
Directly integrates OpenAI analysis with existing WhatsApp functionality
"""

import asyncio
import urllib.parse
import webbrowser
import os
from dotenv import load_dotenv
import openai

# Load environment
load_dotenv()

class SimpleAIWhatsApp:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.target_number = os.getenv('TARGET_WHATSAPP_NUMBER', '919518536672')

        if self.api_key:
            self.client = openai.AsyncOpenAI(api_key=self.api_key)
        else:
            self.client = None

    async def analyze_quote(self, quote_data):
        """Analyze quote with OpenAI (simplified)"""
        if not self.client:
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

            response = await self.client.chat.completions.create(
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

    async def generate_enhanced_message(self, quote_data, analysis):
        """Generate enhanced WhatsApp message with AI insights"""

        priority_emoji = "🔥" if analysis['priority'] >= 8 else "⭐" if analysis['priority'] >= 6 else "📝"

        message = f"""{priority_emoji} NEW QUOTE REQUEST - OrbitX

👤 Client: {quote_data.get('client_name')}
📧 Email: {quote_data.get('email')}
📱 Phone: {quote_data.get('phone', 'Not provided')}
🏢 Company: {quote_data.get('company_name', 'Not provided')}

🛠️ Service: {quote_data.get('services_requested')}
💰 Budget: {quote_data.get('budget_range', 'Not specified')}
⏰ Timeline: {quote_data.get('timeline', 'Not specified')}

📝 Project Description:
{quote_data.get('project_description', '')}

🤖 AI Analysis:
• Priority: {analysis['priority']}/10
• Est. Value: {analysis['estimated_value']}
• Strategy: {analysis['strategy']}

⚡ Action Required: Prepare and send detailed quote to {quote_data.get('email')}"""

        return message

    async def process_and_send(self, quote_data):
        """Complete process: analyze + generate + send WhatsApp"""
        try:
            print("Analyzing quote with AI...")
            analysis = await self.analyze_quote(quote_data)

            print("Generating enhanced WhatsApp message...")
            message = await self.generate_enhanced_message(quote_data, analysis)

            print("Creating WhatsApp URL...")
            encoded_message = urllib.parse.quote(message)
            whatsapp_url = f"https://wa.me/{self.target_number}?text={encoded_message}"

            print("Opening WhatsApp Web...")
            webbrowser.open(whatsapp_url)

            return {
                "success": True,
                "analysis": analysis,
                "message": message,
                "url": whatsapp_url
            }

        except Exception as e:
            print(f"Error processing quote: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Function for easy integration with Flask
async def send_ai_enhanced_whatsapp(quote_data):
    """Simple function to call from Flask app"""
    ai_whatsapp = SimpleAIWhatsApp()
    return await ai_whatsapp.process_and_send(quote_data)

# Test the functionality
if __name__ == "__main__":
    test_quote = {
        "client_name": "Test AI Client",
        "email": "test@ai.com",
        "phone": "1234567890",
        "company_name": "AI Test Company",
        "services_requested": "logo-design",
        "project_description": "Need a modern AI-themed logo for our tech startup",
        "budget_range": "10000-20000",
        "timeline": "urgent"
    }

    print("Testing AI-enhanced WhatsApp integration...")
    result = asyncio.run(send_ai_enhanced_whatsapp(test_quote))

    if result['success']:
        print("SUCCESS! AI analysis completed and WhatsApp opened.")
        print(f"Priority: {result['analysis']['priority']}/10")
        print(f"Estimated Value: {result['analysis']['estimated_value']}")
    else:
        print(f"FAILED: {result['error']}")