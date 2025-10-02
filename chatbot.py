import json
import uuid
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from flask import current_app
from models_mongodb import DatabaseModels
import openai
import re

class OrbitXChatbot:
    def __init__(self, openai_client, db_models):
        self.openai_client = openai_client
        self.db_models = db_models
        self.system_prompt = """You are OrbitX AI Assistant, a helpful and professional chatbot for OrbitX Design - a digital marketing and design agency.

Your capabilities:
- Help users start design projects (logos, websites, social media, branding, etc.)
- Provide service information and pricing estimates
- Collect project requirements step by step
- Generate quotes efficiently with minimal back-and-forth
- Guide users through the design process
- Answer questions about OrbitX services

Key Guidelines:
1. Be conversational, friendly, and professional
2. Guide users efficiently through quote creation in 2-3 messages maximum
3. For quotes, collect these essentials quickly: name, email, service type, basic requirements
4. Once you have the basics (name, email, service), ask if they want a quote created
5. Keep responses concise and action-oriented
6. Use a structured approach to gather information quickly
7. Always offer to create a quote when you have sufficient info
8. NEVER mention payment methods, deposits, or bank details - quotes are created for review only
9. After creating quotes, mention that the team will contact them via WhatsApp for next steps

Available Services:
- Logo Design (₹2,000-15,000)
- Website Design (₹10,000-50,000)
- Social Media Design (₹5,000-20,000)
- Branding Package (₹15,000-75,000)
- Packaging Design (₹8,000-30,000)
- Print Design (₹3,000-25,000)

CRITICAL QUOTE CREATION WORKFLOW:
1. If missing name: Ask "What's your name?"
2. If missing email: Ask "What's your email address?"
3. If missing service details: Ask about specific requirements
4. Once you have name, email, and service type: Ask "Should I create a quote for this project?"
5. When user says "yes" or "create quote": Confirm quote creation
6. NEVER mention payments - only mention that team will contact via WhatsApp

Key phrases that trigger quote creation:
- "quote", "price", "cost", "how much", "estimate", "proposal"
- Service names: "logo", "website", "branding", "social media", etc.

Response Style:
- Use emojis sparingly and professionally: 👋 💡 ✨ 🎨 📧
- Keep responses under 100 words when possible
- Use bullet points for clarity when listing options
- Always end with a clear next step or question

Remember: Your goal is to efficiently convert conversations into quote requests while providing excellent customer service."""

        # Service keywords for detection
        self.service_keywords = {
            'logo': ['logo', 'brand mark', 'brand identity'],
            'website': ['website', 'web design', 'site', 'online presence'],
            'social media': ['social media', 'instagram', 'facebook', 'social posts'],
            'branding': ['branding', 'brand package', 'brand identity', 'visual identity'],
            'packaging': ['packaging', 'product packaging', 'box design'],
            'print': ['print', 'brochure', 'flyer', 'business card', 'stationery']
        }

        # Quote trigger keywords
        self.quote_keywords = [
            'quote', 'price', 'pricing', 'cost', 'how much', 'estimate',
            'proposal', 'budget', 'charge', 'fee', 'rates'
        ]

    def _detect_intent(self, message: str, context: Dict) -> Dict:
        """Detect user intent from message"""
        message_lower = message.lower()

        intent = {
            'type': 'general',
            'confidence': 0.5,
            'services': [],
            'wants_quote': False,
            'has_contact_info': False
        }

        # Service type detection
        for service_type, keywords in self.service_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                intent['services'].append(service_type)
                intent['type'] = 'service_inquiry'
                intent['confidence'] = 0.8

        # Quote intent detection
        if any(keyword in message_lower for keyword in self.quote_keywords):
            intent['wants_quote'] = True
            intent['type'] = 'quote_request'
            intent['confidence'] = 0.9

        # Contact info detection
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(email_pattern, message) or '@' in message:
            intent['has_contact_info'] = True

        return intent

    def process_message(self, conversation_id: str, user_message: str, user_info: Dict = None) -> Dict:
        """Process user message and return bot response"""
        try:
            # Get or create conversation
            conversation = self.db_models.chat_conversations.find_one({'_id': conversation_id})
            if not conversation:
                self.db_models.chat_conversations.create_conversation(
                    conversation_id=conversation_id,
                    user_session_id=user_info.get('session_id') if user_info else None,
                    user_name=user_info.get('name') if user_info else None,
                    user_email=user_info.get('email') if user_info else None,
                    user_phone=user_info.get('phone') if user_info else None,
                    context_data=json.dumps({})
                )
                # Re-fetch to get the created conversation
                conversation = self.db_models.chat_conversations.find_one({'_id': conversation_id})

            # Save user message
            self.db_models.chat_messages.create_message(
                conversation_id=conversation_id,
                sender='user',
                message=user_message,
                message_type='text'
            )

            # Get conversation context
            context_data = json.loads(conversation.get('context_data', '{}'))

            # Get recent messages for context
            recent_messages = self.db_models.chat_messages.get_by_conversation(conversation_id, limit=10)

            # Detect intent
            intent = self._detect_intent(user_message, context_data)

            # Update context with extracted information
            context_data = self._update_context(user_message, context_data, intent)

            # Generate response
            messages_for_ai = self._prepare_messages_for_ai(recent_messages, context_data)

            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages_for_ai,
                    max_tokens=300,
                    temperature=0.7
                )
                bot_response = response.choices[0].message.content
            except Exception as e:
                current_app.logger.error(f"OpenAI API error: {e}")
                bot_response = "I'm having some technical difficulties. Let me connect you with our team directly. Please share your contact details and project requirements."

            # Handle quote creation
            quote_request_id = None
            if self._should_create_quote(user_message, context_data, intent):
                try:
                    analysis = self._analyze_user_intent(user_message, context_data)
                    quote_request_id = self._create_quote_request(conversation, context_data, analysis)

                    if quote_request_id:
                        current_app.logger.info(f"🚀 Creating quote for: {context_data.get('user_name')} - Services: {analysis['services']}")

                        # Get created quote for notifications
                        quote_request = self.db_models.quote_requests.get_by_id(quote_request_id)
                        if quote_request:
                            try:
                                self._send_quote_notifications(quote_request, analysis)
                            except Exception as notification_error:
                                current_app.logger.error(f"Quote notification failed: {notification_error}")

                        bot_response += f"\n\n✅ Perfect! I've created quote #{quote_request_id} for your project. Our team will review your requirements and contact you via WhatsApp within 2 hours with a detailed proposal."

                except Exception as quote_error:
                    current_app.logger.error(f"Quote creation failed: {quote_error}")
                    bot_response += "\n\n⚠️ I encountered an issue creating your quote, but don't worry! Our team has been notified and will contact you directly."

            # Save bot response
            self.db_models.chat_messages.create_message(
                conversation_id=conversation_id,
                sender='bot',
                message=bot_response,
                message_type='text',
                message_metadata=json.dumps({
                    'intent': intent,
                    'quote_request_id': quote_request_id
                }) if quote_request_id else None
            )

            # Update conversation context
            self.db_models.chat_conversations.update_one(
                {'_id': conversation_id},
                {'context_data': json.dumps(context_data)}
            )

            return {
                'success': True,
                'bot_response': bot_response,
                'conversation_id': conversation_id,
                'quote_request_id': quote_request_id,
                'intent': intent
            }

        except Exception as e:
            current_app.logger.error(f"Chatbot error: {e}")
            return {
                'success': False,
                'error': str(e),
                'bot_response': "I apologize, but I'm experiencing technical difficulties. Please try again or contact us directly."
            }

    def _update_context(self, message: str, context: Dict, intent: Dict) -> Dict:
        """Update conversation context with extracted information"""
        message_lower = message.lower()

        # Extract name if not present
        if not context.get('user_name'):
            name_patterns = [
                r"my name is (\w+)",
                r"i'm (\w+)",
                r"i am (\w+)",
                r"call me (\w+)"
            ]
            for pattern in name_patterns:
                match = re.search(pattern, message_lower)
                if match:
                    context['user_name'] = match.group(1).title()
                    break

        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, message)
        if email_match:
            context['user_email'] = email_match.group()

        # Extract phone
        phone_patterns = [
            r'(\+91[\s\-]?\d{10})',
            r'(\d{10})',
            r'(\d{3}[\s\-]?\d{3}[\s\-]?\d{4})'
        ]
        for pattern in phone_patterns:
            match = re.search(pattern, message)
            if match:
                context['user_phone'] = match.group()
                break

        # Update services
        if intent['services']:
            if 'services_interested' not in context:
                context['services_interested'] = []
            for service in intent['services']:
                if service not in context['services_interested']:
                    context['services_interested'].append(service)

        # Store project description
        if len(message.split()) > 10:  # Longer messages might be descriptions
            context['project_description'] = message

        return context

    def _should_create_quote(self, message: str, context: Dict, intent: Dict) -> bool:
        """Determine if a quote should be created"""
        # Must have minimum required info
        has_name = bool(context.get('user_name'))
        has_email = bool(context.get('user_email'))
        has_service = bool(context.get('services_interested'))

        # User explicitly requests quote
        quote_confirmations = ['yes', 'create quote', 'generate quote', 'proceed', 'go ahead']
        wants_quote = any(phrase in message.lower() for phrase in quote_confirmations)

        return has_name and has_email and has_service and (wants_quote or intent['wants_quote'])

    def _analyze_user_intent(self, message: str, context: Dict) -> Dict:
        """Analyze user intent for quote creation"""
        return {
            'user_name': context.get('user_name', 'Unknown'),
            'user_email': context.get('user_email', ''),
            'services': context.get('services_interested', []),
            'description': context.get('project_description', message),
            'priority': 7 if context.get('user_email') else 5
        }

    def _create_quote_request(self, conversation: dict, context_data: Dict, analysis: Dict) -> str:
        """Create a quote request in the database"""
        try:
            # Create quote request
            quote_request_id = self.db_models.quote_requests.create_quote_request(
                client_name=analysis.get('user_name', 'Unknown'),
                email=analysis.get('user_email', ''),
                phone=context_data.get('user_phone', ''),
                company_name=context_data.get('company_name', ''),
                services_requested=', '.join(analysis.get('services', [])),
                project_description=analysis.get('description', ''),
                budget_range=context_data.get('budget_range', ''),
                timeline=context_data.get('timeline', ''),
                additional_requirements=f"Created via AI chatbot. Priority: {analysis.get('priority', 5)}/10",
                status='pending'
            )

            # Update conversation with quote request ID
            self.db_models.chat_conversations.update_one(
                {'_id': conversation['id']},
                {'quote_request_id': quote_request_id}
            )

            return quote_request_id

        except Exception as e:
            current_app.logger.error(f"Failed to create quote request: {e}")
            raise

    def _send_quote_notifications(self, quote_request: Dict, analysis: Dict):
        """Send notifications for new quote request"""
        try:
            import os
            import urllib.parse
            import webbrowser
            from threading import Thread

            def send_notification():
                try:
                    # Generate WhatsApp message
                    message = f"""🤖 NEW AI CHATBOT QUOTE - OrbitX

👤 Client: {quote_request.get('client_name')}
📧 Email: {quote_request.get('email')}
📱 Phone: {quote_request.get('phone') or 'Not provided'}

🛠️ Services: {quote_request.get('services_requested')}
📝 Description: {quote_request.get('project_description')}

🤖 AI Priority: {analysis.get('priority', 5)}/10
💡 Created via: AI Chatbot

⚡ Action: Send detailed quote to {quote_request.get('email')}"""

                    # URL encode for WhatsApp
                    encoded_message = urllib.parse.quote(message)
                    whatsapp_url = f"https://wa.me/{os.getenv('TARGET_WHATSAPP_NUMBER', '919518536672')}?text={encoded_message}"

                    # Open WhatsApp (in development)
                    if os.getenv('FLASK_ENV') != 'production':
                        try:
                            webbrowser.open(whatsapp_url)
                        except:
                            pass  # Fail silently if can't open browser

                    current_app.logger.info(f"📱 WhatsApp notification sent for quote {quote_request.get('id')}")

                except Exception as e:
                    current_app.logger.error(f"Notification sending failed: {e}")

            # Send in background thread
            Thread(target=send_notification, daemon=True).start()

        except Exception as e:
            current_app.logger.error(f"Failed to setup notifications: {e}")

    def _prepare_messages_for_ai(self, recent_messages: List[Dict], context_data: Dict) -> List[Dict]:
        """Prepare messages for OpenAI API"""
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add context information
        if context_data:
            context_summary = f"User context: {json.dumps(context_data, indent=2)}"
            messages.append({"role": "system", "content": context_summary})

        # Add recent conversation history
        for msg in recent_messages[-6:]:  # Last 6 messages for context
            role = "user" if msg.get('sender') == 'user' else "assistant"
            messages.append({
                "role": role,
                "content": msg.get('message', '')
            })

        return messages

    def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """Get conversation history"""
        try:
            messages = self.db_models.chat_messages.get_by_conversation(conversation_id)
            return [
                {
                    'id': msg.get('id'),
                    'sender': msg.get('sender'),
                    'message': msg.get('message'),
                    'created_at': msg.get('created_at').isoformat() if msg.get('created_at') else None,
                    'message_type': msg.get('message_type', 'text')
                }
                for msg in messages
            ]
        except Exception as e:
            current_app.logger.error(f"Failed to get conversation history: {e}")
            return []

# Initialize chatbot instance
def get_chatbot():
    """Get chatbot instance with OpenAI client and db_models"""
    from app import openai_client, db_models
    if not openai_client:
        raise Exception("OpenAI client not configured")
    return OrbitXChatbot(openai_client, db_models)