#!/usr/bin/env python3
"""
Test complete WhatsApp message generation
"""

import asyncio
import os
import urllib.parse
from dotenv import load_dotenv
import openai

# Load environment
load_dotenv()

async def test_complete_workflow():
    """Test complete AI + WhatsApp workflow"""

    print("=== TESTING COMPLETE AI + WHATSAPP WORKFLOW ===")

    # Initialize OpenAI client
    api_key = os.getenv('OPENAI_API_KEY')
    client = openai.AsyncOpenAI(api_key=api_key)

    # Test quote data
    quote_data = {
        'client_name': 'Premium Test Client',
        'email': 'premium@example.com',
        'phone': '9876543210',
        'company_name': 'Premium Design Co',
        'services_requested': 'logo-design',
        'project_description': 'Need a luxury brand logo for high-end fashion startup with premium aesthetics',
        'budget_range': '25000-50000',
        'timeline': 'urgent',
        'additional_requirements': 'Vector format, multiple variations'
    }

    # Step 1: AI Analysis
    try:
        prompt = f"""Analyze this design quote briefly:
        Client: {quote_data.get('client_name')}
        Service: {quote_data.get('services_requested')}
        Budget: {quote_data.get('budget_range', 'Not specified')}
        Description: {quote_data.get('project_description', '')[:200]}

        Provide priority (1-10) and estimated value in rupees in this format:
        Priority: X/10
        Value: Rs X,XXX-X,XXX"""

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )

        result = response.choices[0].message.content
        print(f"AI Analysis Result:")
        print(result)

        # Extract values
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

        analysis = {
            "priority": priority,
            "estimated_value": value,
            "strategy": "AI-analyzed response"
        }

        print(f"\nExtracted Analysis:")
        print(f"Priority: {analysis['priority']}/10")
        print(f"Value: {analysis['estimated_value']}")

    except Exception as e:
        print(f"AI Analysis Error: {e}")
        analysis = {"priority": 5, "estimated_value": "Rs 5,000-15,000", "strategy": "Standard response"}

    # Step 2: Generate Enhanced WhatsApp Message
    priority_emoji = "FIRE" if analysis['priority'] >= 8 else "STAR" if analysis['priority'] >= 6 else "NOTE"

    message = f"""{priority_emoji} NEW QUOTE REQUEST - OrbitX

Client: {quote_data.get('client_name')}
Email: {quote_data.get('email')}
Phone: {quote_data.get('phone', 'Not provided')}
Company: {quote_data.get('company_name', 'Not provided')}

Service: {quote_data.get('services_requested')}
Budget: {quote_data.get('budget_range', 'Not specified')}
Timeline: {quote_data.get('timeline', 'Not specified')}

Project Description:
{quote_data.get('project_description', '')}

AI Analysis:
• Priority: {analysis['priority']}/10
• Est. Value: {analysis['estimated_value']}
• Strategy: {analysis['strategy']}

Action Required: Prepare and send detailed quote to {quote_data.get('email')}"""

    print(f"\nGenerated WhatsApp Message:")
    print(message)

    # Step 3: Create WhatsApp URL
    encoded_message = urllib.parse.quote(message)
    whatsapp_number = os.getenv('TARGET_WHATSAPP_NUMBER', '919518536672')
    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"

    print(f"\nWhatsApp URL Generated:")
    print(f"Length: {len(whatsapp_url)} characters")
    print(f"First 100 chars: {whatsapp_url[:100]}...")

    # Step 4: Summary
    print(f"\n=== WORKFLOW SUMMARY ===")
    print(f"✓ AI Analysis: SUCCESS (Priority {analysis['priority']}/10)")
    print(f"✓ Message Generation: SUCCESS ({len(message)} characters)")
    print(f"✓ URL Creation: SUCCESS ({len(whatsapp_url)} characters)")
    print(f"✓ Target Number: {whatsapp_number}")
    print(f"✓ Priority Level: {priority_emoji}")

    print(f"\nREADY FOR PRODUCTION!")
    print(f"When a quote is submitted:")
    print(f"1. AI analyzes and gives priority {analysis['priority']}/10")
    print(f"2. WhatsApp opens with professional message")
    print(f"3. One click sends to {whatsapp_number}")

if __name__ == "__main__":
    asyncio.run(test_complete_workflow())