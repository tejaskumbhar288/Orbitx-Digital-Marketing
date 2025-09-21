#!/usr/bin/env python3
"""
Direct test of AI functionality
"""

import asyncio
import os
from dotenv import load_dotenv
import openai

# Load environment
load_dotenv()

async def test_ai_analysis():
    """Test AI analysis directly"""

    print("=== TESTING AI ANALYSIS DIRECTLY ===")

    # Check OpenAI key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: No OpenAI API key found")
        return

    print(f"OpenAI API Key: {api_key[:20]}...{api_key[-10:]}")

    # Initialize client
    client = openai.AsyncOpenAI(api_key=api_key)

    # Test quote data
    quote_data = {
        'client_name': 'Test AI Client',
        'services_requested': 'logo-design',
        'budget_range': '15000-25000',
        'project_description': 'Need a modern AI-themed logo for our tech startup with clean design'
    }

    try:
        print("Sending request to OpenAI...")

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
        print(f"AI Response: {result}")

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

        print(f"Extracted Priority: {priority}/10")
        print(f"Extracted Value: {value}")

        # Test emoji selection
        priority_emoji = "🔥" if priority >= 8 else "⭐" if priority >= 6 else "📝"
        print(f"Priority Emoji: {priority_emoji}")

        print("SUCCESS: AI analysis working correctly!")

    except Exception as e:
        print(f"ERROR: AI analysis failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai_analysis())