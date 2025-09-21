# WhatsApp MCP Server with OpenAI Integration

Automatically processes quote requests and sends WhatsApp messages using OpenAI GPT-4 for intelligent analysis.

## Features

- 🤖 **OpenAI Integration** - GPT-4 analyzes quotes and suggests responses
- 📱 **WhatsApp Automation** - Sends formatted messages to 9518536672
- 🎯 **Priority Scoring** - AI-powered quote prioritization (1-10)
- 💰 **Value Estimation** - Automatic project value assessment
- ⚡ **Real-time Processing** - Instant quote analysis and messaging

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

3. **Add to Claude Code Configuration**

   Add this to your Claude Code MCP settings:
   ```json
   {
     "mcpServers": {
       "whatsapp-quote-processor": {
         "command": "python",
         "args": ["C:/Users/tejas/OneDrive/Desktop/Digital Mearketing website/whatsapp-mcp-server/server.py"],
         "env": {
           "OPENAI_API_KEY": "your_openai_api_key_here"
         }
       }
     }
   }
   ```

## Available Tools

### 1. `process_quote_request`
Complete quote processing with AI analysis and WhatsApp sending.

**Input:**
```json
{
  "client_name": "John Doe",
  "email": "john@example.com",
  "services_requested": "logo-design",
  "project_description": "Need a modern logo for tech startup"
}
```

### 2. `send_whatsapp_message`
Send direct WhatsApp messages.

**Input:**
```json
{
  "phone_number": "919518536672",
  "message": "Test message"
}
```

### 3. `analyze_quote_priority`
Get AI analysis of quote priority and value.

**Input:**
```json
{
  "quote_data": {
    "client_name": "John Doe",
    "services_requested": "logo-design"
  }
}
```

## Usage in Claude Code

Once configured, you can use these tools directly in Claude Code:

```
Can you process this quote request:
- Client: "Test Company"
- Email: "test@company.com"
- Service: "logo-design"
- Description: "Need professional logo for new business"
```

Claude Code will automatically call the MCP server, which will:
1. Analyze the quote with GPT-4
2. Generate a formatted WhatsApp message
3. Send it to 9518536672
4. Return the analysis and delivery status

## Integration with Flask App

To integrate with your quote form, modify your Flask app:

```python
# In app.py - replace WhatsApp section with MCP call
from mcp.client import create_client

async def process_quote_with_mcp(quote_data):
    async with create_client() as client:
        result = await client.call_tool(
            "process_quote_request",
            quote_data
        )
    return result
```

## Next Steps

1. **Get OpenAI API Key** - Sign up at https://platform.openai.com
2. **WhatsApp Business API** - For production, integrate official WhatsApp Business API
3. **Test Integration** - Verify MCP server works with Claude Code
4. **Production Deployment** - Move to production WhatsApp API

## Cost Estimation

- **OpenAI GPT-4**: ~₹0.75 per quote analysis (very affordable)
- **WhatsApp Business API**: ~₹0.50 per message
- **Total per quote**: ~₹1.25 (extremely cost-effective)