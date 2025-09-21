#!/usr/bin/env python3
"""
WhatsApp MCP Server with OpenAI Integration
Automatically processes quote requests and sends WhatsApp messages
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent
import httpx
import openai
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai_client = None

class WhatsAppMCPServer:
    def __init__(self):
        self.server = Server("whatsapp-quote-processor")
        self.setup_tools()

    def setup_tools(self):
        """Register MCP tools"""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="process_quote_request",
                    description="Process a quote request and send WhatsApp message",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "client_name": {"type": "string"},
                            "email": {"type": "string"},
                            "phone": {"type": "string"},
                            "company_name": {"type": "string"},
                            "services_requested": {"type": "string"},
                            "project_description": {"type": "string"},
                            "budget_range": {"type": "string"},
                            "timeline": {"type": "string"},
                            "additional_requirements": {"type": "string"}
                        },
                        "required": ["client_name", "email", "services_requested", "project_description"]
                    }
                ),
                Tool(
                    name="send_whatsapp_message",
                    description="Send a WhatsApp message to specified number",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "phone_number": {"type": "string"},
                            "message": {"type": "string"}
                        },
                        "required": ["phone_number", "message"]
                    }
                ),
                Tool(
                    name="analyze_quote_priority",
                    description="Use OpenAI to analyze quote priority and suggest response",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "quote_data": {"type": "object"}
                        },
                        "required": ["quote_data"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls"""

            if name == "process_quote_request":
                return await self.process_quote_request(arguments)
            elif name == "send_whatsapp_message":
                return await self.send_whatsapp_message(arguments)
            elif name == "analyze_quote_priority":
                return await self.analyze_quote_priority(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")

    async def process_quote_request(self, quote_data: Dict[str, Any]) -> List[TextContent]:
        """Process quote request with OpenAI and send WhatsApp"""
        try:
            # Step 1: Analyze quote with OpenAI
            analysis = await self.analyze_with_openai(quote_data)

            # Step 2: Generate WhatsApp message
            whatsapp_message = await self.generate_whatsapp_message(quote_data, analysis)

            # Step 3: Send WhatsApp message
            result = await self.send_to_whatsapp("919518536672", whatsapp_message)

            return [TextContent(
                type="text",
                text=f"✅ Quote processed successfully!\n\nPriority: {analysis.get('priority', 'N/A')}\nEstimated Value: {analysis.get('estimated_value', 'N/A')}\nWhatsApp Status: {result}\n\nMessage sent:\n{whatsapp_message}"
            )]

        except Exception as e:
            logger.error(f"Error processing quote request: {e}")
            return [TextContent(
                type="text",
                text=f"❌ Error processing quote: {str(e)}"
            )]

    async def analyze_with_openai(self, quote_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze quote using OpenAI GPT-4"""
        try:
            global openai_client
            if not openai_client:
                return {"priority": 5, "estimated_value": "TBD", "strategy": "Standard response"}

            prompt = f"""
            Analyze this design quote request and provide:
            1. Priority score (1-10, where 10 is highest priority)
            2. Estimated project value in ₹
            3. Response strategy
            4. Urgency level

            Quote Details:
            - Client: {quote_data.get('client_name')}
            - Service: {quote_data.get('services_requested')}
            - Budget: {quote_data.get('budget_range', 'Not specified')}
            - Timeline: {quote_data.get('timeline', 'Not specified')}
            - Description: {quote_data.get('project_description')}

            Respond in JSON format:
            {{
                "priority": number,
                "estimated_value": "₹X,XXX - ₹X,XXX",
                "strategy": "response approach",
                "urgency": "low/medium/high"
            }}
            """

            response = await openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=500
            )

            return json.loads(response.choices[0].message.content)

        except Exception as e:
            logger.error(f"OpenAI analysis error: {e}")
            return {"priority": 5, "estimated_value": "TBD", "strategy": "Standard response"}

    async def generate_whatsapp_message(self, quote_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Generate personalized WhatsApp message"""

        # Get urgency emoji
        urgency_emoji = {
            "high": "🔥",
            "medium": "⭐",
            "low": "📝"
        }.get(analysis.get("urgency", "medium"), "📝")

        message = f"""{urgency_emoji} NEW QUOTE REQUEST - OrbitX

👤 Client: {quote_data.get('client_name')}
📧 Email: {quote_data.get('email')}
📱 Phone: {quote_data.get('phone', 'Not provided')}
🏢 Company: {quote_data.get('company_name', 'Not provided')}

🛠️ Service: {quote_data.get('services_requested')}
💰 Budget: {quote_data.get('budget_range', 'Not specified')}
⏰ Timeline: {quote_data.get('timeline', 'Not specified')}

📝 Project Description:
{quote_data.get('project_description')}

📋 Additional Requirements:
{quote_data.get('additional_requirements', 'None specified')}

🤖 AI Analysis:
• Priority: {analysis.get('priority', 'N/A')}/10
• Est. Value: {analysis.get('estimated_value', 'TBD')}
• Strategy: {analysis.get('strategy', 'Standard response')}

⚡ Action Required: Prepare and send detailed quote to {quote_data.get('email')}"""

        return message

    async def send_to_whatsapp(self, phone_number: str, message: str) -> str:
        """Send message via FREE WhatsApp Web (wa.me link)"""
        try:
            import urllib.parse
            import webbrowser

            # URL encode the message for WhatsApp
            encoded_message = urllib.parse.quote(message)
            whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_message}"

            logger.info(f"Opening WhatsApp for {phone_number}: {message[:100]}...")

            # Open WhatsApp Web automatically
            webbrowser.open(whatsapp_url)

            # Wait a moment for the browser to open
            await asyncio.sleep(2)

            return f"✅ WhatsApp opened successfully! URL: {whatsapp_url[:100]}..."

        except Exception as e:
            logger.error(f"WhatsApp send error: {e}")
            return f"❌ Failed to open WhatsApp: {str(e)}"

    async def send_whatsapp_message(self, args: Dict[str, Any]) -> List[TextContent]:
        """Tool handler for sending WhatsApp messages"""
        phone = args.get("phone_number")
        message = args.get("message")

        result = await self.send_to_whatsapp(phone, message)

        return [TextContent(
            type="text",
            text=f"WhatsApp sent to {phone}:\n{result}"
        )]

    async def analyze_quote_priority(self, args: Dict[str, Any]) -> List[TextContent]:
        """Tool handler for quote analysis"""
        quote_data = args.get("quote_data", {})
        analysis = await self.analyze_with_openai(quote_data)

        return [TextContent(
            type="text",
            text=f"Quote Analysis:\n{json.dumps(analysis, indent=2)}"
        )]

async def main():
    """Main server entry point"""
    global openai_client

    # Initialize OpenAI client with API key from environment
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key.startswith("sk-"):
            openai_client = openai.AsyncOpenAI(api_key=api_key)
            logger.info("✅ OpenAI client initialized successfully")
            logger.info(f"🔑 API Key: {api_key[:10]}...{api_key[-5:]}")
        else:
            logger.warning("❌ OPENAI_API_KEY not found or invalid - AI analysis will be disabled")
            logger.info("💡 Make sure your .env file contains: OPENAI_API_KEY=sk-proj-...")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")

    # Create and run MCP server
    whatsapp_server = WhatsAppMCPServer()
    logger.info("🚀 Starting WhatsApp MCP Server...")

    async with stdio_server() as streams:
        await whatsapp_server.server.run(
            streams[0], streams[1], whatsapp_server.server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())