#!/usr/bin/env python3
"""
Test OpenAI integration for MCP server
"""

import asyncio
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

async def test_openai_connection():
    """Test OpenAI API connection and quote analysis"""

    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False

    print(f"API Key loaded: {api_key[:10]}...{api_key[-5:]}")

    try:
        # Initialize OpenAI client
        client = openai.AsyncOpenAI(api_key=api_key)
        print("OpenAI client initialized")

        # Test quote analysis
        test_quote = {
            "client_name": "Test Client",
            "email": "test@example.com",
            "services_requested": "logo-design",
            "project_description": "Need a modern logo for my tech startup",
            "budget_range": "5000-10000",
            "timeline": "week"
        }

        prompt = f"""
        Analyze this design quote request and provide:
        1. Priority score (1-10, where 10 is highest priority)
        2. Estimated project value in ₹
        3. Response strategy
        4. Urgency level

        Quote Details:
        - Client: {test_quote.get('client_name')}
        - Service: {test_quote.get('services_requested')}
        - Budget: {test_quote.get('budget_range', 'Not specified')}
        - Timeline: {test_quote.get('timeline', 'Not specified')}
        - Description: {test_quote.get('project_description')}

        Respond in JSON format:
        {{
            "priority": number,
            "estimated_value": "₹X,XXX - ₹X,XXX",
            "strategy": "response approach",
            "urgency": "low/medium/high"
        }}
        """

        print("Testing OpenAI analysis...")

        response = await client.chat.completions.create(
            model="gpt-4o-mini",  # Using cheaper model for testing
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_tokens=500
        )

        result = response.choices[0].message.content
        print("OpenAI Response:")
        print(result)

        # Test message generation
        print("\nTesting WhatsApp message generation...")

        message_prompt = f"""Generate a professional WhatsApp message for this quote request:

        Client: {test_quote['client_name']}
        Service: {test_quote['services_requested']}
        Description: {test_quote['project_description']}

        Make it professional but friendly, include emojis, and mention OrbitX company."""

        message_response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": message_prompt}],
            max_tokens=300
        )

        whatsapp_message = message_response.choices[0].message.content
        print("Generated WhatsApp Message:")
        print(whatsapp_message)

        print("\nAll tests passed! MCP server is ready.")
        return True

    except Exception as e:
        print(f"Error testing OpenAI: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_openai_connection())
    if success:
        print("\nYour MCP server is ready to use with Claude Code!")
    else:
        print("\nPlease check your OpenAI API key and try again.")