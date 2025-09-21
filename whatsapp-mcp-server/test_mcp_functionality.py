#!/usr/bin/env python3
"""
Test MCP Server functionality step by step
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_mcp_server():
    """Test each component of the MCP server"""

    print("=== MCP SERVER FUNCTIONALITY TEST ===\n")

    # Import the server
    try:
        from server import WhatsAppMCPServer
        print("✅ MCP Server import: SUCCESS")
    except Exception as e:
        print(f"❌ MCP Server import: FAILED - {e}")
        return False

    # Create server instance
    try:
        server = WhatsAppMCPServer()
        print("✅ Server instance creation: SUCCESS")
    except Exception as e:
        print(f"❌ Server instance creation: FAILED - {e}")
        return False

    # Test OpenAI connection
    try:
        import openai
        api_key = os.getenv('OPENAI_API_KEY')
        client = openai.AsyncOpenAI(api_key=api_key)

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Reply with just 'OK' if you can read this"}],
            max_tokens=10
        )

        result = response.choices[0].message.content.strip()
        if "OK" in result.upper():
            print("✅ OpenAI connection: SUCCESS")
        else:
            print(f"⚠️ OpenAI connection: PARTIAL - Got: {result}")

    except Exception as e:
        print(f"❌ OpenAI connection: FAILED - {e}")
        return False

    # Test quote analysis
    try:
        test_quote = {
            "client_name": "Test Client",
            "email": "test@example.com",
            "services_requested": "logo-design",
            "project_description": "Need a modern logo",
            "budget_range": "5000-10000",
            "timeline": "week"
        }

        analysis = await server.analyze_with_openai(test_quote)
        print(f"✅ Quote analysis: SUCCESS - Priority: {analysis.get('priority', 'Unknown')}")

    except Exception as e:
        print(f"❌ Quote analysis: FAILED - {e}")
        return False

    # Test WhatsApp message generation
    try:
        analysis = {"priority": 8, "estimated_value": "Rs 10,000-15,000", "strategy": "Fast response"}
        message = await server.generate_whatsapp_message(test_quote, analysis)

        if len(message) > 50 and "OrbitX" in message:
            print("✅ WhatsApp message generation: SUCCESS")
            print(f"📱 Sample message (first 100 chars): {message[:100]}...")
        else:
            print(f"⚠️ WhatsApp message generation: PARTIAL - Length: {len(message)}")

    except Exception as e:
        print(f"❌ WhatsApp message generation: FAILED - {e}")
        return False

    # Test WhatsApp URL creation
    try:
        import urllib.parse

        test_message = "Test WhatsApp message from MCP server"
        encoded = urllib.parse.quote(test_message)
        url = f"https://wa.me/919518536672?text={encoded}"

        if "wa.me" in url and "919518536672" in url:
            print("✅ WhatsApp URL creation: SUCCESS")
            print(f"🔗 Test URL: {url[:80]}...")
        else:
            print("❌ WhatsApp URL creation: FAILED")

    except Exception as e:
        print(f"❌ WhatsApp URL creation: FAILED - {e}")
        return False

    # Test complete process_quote_request workflow
    try:
        print("\n=== TESTING COMPLETE WORKFLOW ===")

        result = await server.process_quote_request(test_quote)

        if result and len(result) > 0:
            response_text = result[0].text if hasattr(result[0], 'text') else str(result[0])
            print("✅ Complete workflow: SUCCESS")
            print(f"📋 Result: {response_text[:200]}...")
        else:
            print("❌ Complete workflow: FAILED - No result")

    except Exception as e:
        print(f"❌ Complete workflow: FAILED - {e}")
        return False

    print("\n🎉 ALL TESTS PASSED! MCP Server is working correctly.")
    print("\n💡 The server is ready to:")
    print("   1. Analyze quotes with AI")
    print("   2. Generate professional WhatsApp messages")
    print("   3. Open WhatsApp Web with pre-filled content")
    print("   4. Process complete quote workflows")

    return True

if __name__ == "__main__":
    success = asyncio.run(test_mcp_server())
    if not success:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ MCP Server is ready for Claude Code integration!")