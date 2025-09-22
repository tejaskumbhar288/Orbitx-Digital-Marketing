import json
import uuid
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from flask import current_app
from models import db, ChatConversation, ChatMessage, QuoteRequest, Service, Portfolio
import openai
import re

class OrbitXChatbot:
    def __init__(self, openai_client):
        self.openai_client = openai_client
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

Current conversation context: {context}
"""

    def get_ai_response(self, user_message: str, conversation_context: Dict) -> str:
        """Get AI response using OpenAI"""
        try:
            context_str = json.dumps(conversation_context, indent=2)

            messages = [
                {"role": "system", "content": self.system_prompt.format(context=context_str)},
                {"role": "user", "content": user_message}
            ]

            # Add recent conversation history
            if 'recent_messages' in conversation_context:
                for msg in conversation_context['recent_messages'][-6:]:  # Last 6 messages
                    role = "assistant" if msg['sender'] == 'bot' else "user"
                    messages.insert(-1, {"role": role, "content": msg['message']})

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            current_app.logger.error(f"OpenAI API error: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again in a moment or contact us directly."

    def extract_intent_and_entities(self, message: str) -> Dict:
        """Extract user intent and relevant entities from message"""
        message_lower = message.lower()

        # Service type detection
        services = {
            'logo': ['logo', 'brand mark', 'company logo'],
            'website': ['website', 'web design', 'site', 'web development'],
            'social_media': ['social media', 'instagram', 'facebook', 'twitter', 'social'],
            'branding': ['branding', 'brand identity', 'brand package'],
            'packaging': ['packaging', 'product packaging', 'box design'],
            'print': ['print', 'brochure', 'flyer', 'poster', 'business card']
        }

        detected_services = []
        for service, keywords in services.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_services.append(service)

        # Intent detection
        intents = {
            'get_quote': ['quote', 'price', 'cost', 'how much', 'pricing'],
            'start_project': ['start', 'begin', 'create', 'need', 'want'],
            'get_info': ['what', 'how', 'tell me', 'information', 'about'],
            'check_status': ['status', 'progress', 'update'],
            'portfolio': ['portfolio', 'examples', 'work', 'previous']
        }

        detected_intent = 'general'
        for intent, keywords in intents.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_intent = intent
                break

        # Extract budget if mentioned
        budget_match = re.search(r'₹?(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:k|thousand|lakh)?', message_lower)
        budget = budget_match.group(1) if budget_match else None

        return {
            'intent': detected_intent,
            'services': detected_services,
            'budget': budget,
            'entities': {
                'has_timeline': any(word in message_lower for word in ['urgent', 'asap', 'quickly', 'soon', 'week', 'month']),
                'has_company': any(word in message_lower for word in ['company', 'business', 'startup', 'brand'])
            }
        }

    def process_message(self, conversation_id: str, user_message: str, user_info: Dict = None) -> Dict:
        """Process user message and return bot response"""
        try:
            # Get or create conversation
            conversation = ChatConversation.query.get(conversation_id)
            if not conversation:
                conversation = ChatConversation(
                    id=conversation_id,
                    user_session_id=user_info.get('session_id') if user_info else None,
                    user_name=user_info.get('name') if user_info else None,
                    user_email=user_info.get('email') if user_info else None,
                    user_phone=user_info.get('phone') if user_info else None,
                    context_data=json.dumps({})
                )
                db.session.add(conversation)

            # Save user message
            user_msg = ChatMessage(
                conversation_id=conversation_id,
                sender='user',
                message=user_message,
                message_type='text'
            )
            db.session.add(user_msg)

            # Get conversation context
            context_data = json.loads(conversation.context_data or '{}')

            # Get recent messages for context
            recent_messages = db.session.query(ChatMessage).filter_by(
                conversation_id=conversation_id
            ).order_by(ChatMessage.created_at.desc()).limit(10).all()

            context_data['recent_messages'] = [
                {
                    'sender': msg.sender,
                    'message': msg.message,
                    'timestamp': msg.created_at.isoformat()
                }
                for msg in reversed(recent_messages)
            ]

            # Extract intent and entities
            analysis = self.extract_intent_and_entities(user_message)
            context_data['last_intent'] = analysis['intent']

            # Combine current and previously detected services
            current_services = analysis['services']
            previous_services = context_data.get('detected_services', [])

            # Also extract services from recent conversation history
            conversation_services = []
            for msg in context_data.get('recent_messages', []):
                if msg['sender'] == 'user':
                    msg_analysis = self.extract_intent_and_entities(msg['message'])
                    conversation_services.extend(msg_analysis['services'])

            all_services = list(set(current_services + previous_services + conversation_services))
            context_data['detected_services'] = all_services
            analysis['services'] = all_services  # Update analysis with combined services

            # Update user info if provided in request
            if user_info:
                for key, value in user_info.items():
                    if value:
                        context_data[f'user_{key}'] = value

            # Extract user info from current message
            extracted_info = self.extract_user_info_from_message(user_message)
            for key, value in extracted_info.items():
                if value and not context_data.get(f'user_{key}'):  # Only update if not already set
                    context_data[f'user_{key}'] = value

            # Check for quote confirmation keywords
            quote_confirmation_words = ['yes', 'create quote', 'proceed', 'go ahead', 'confirm', 'approve', 'finalize']
            if any(word in user_message.lower() for word in quote_confirmation_words):
                if context_data.get('user_name') and context_data.get('user_email') and (analysis['services'] or context_data.get('detected_services')):
                    context_data['quote_confirmed'] = True

            # Also check if AI response suggests creating a quote and user agreed
            if analysis['intent'] == 'get_quote' and any(word in user_message.lower() for word in ['yes', 'confirm', 'proceed']):
                context_data['quote_confirmed'] = True

            # Generate AI response
            bot_response = self.get_ai_response(user_message, context_data)

            # Check if we should create a quote request or guide user for missing info
            should_create_quote = self._has_sufficient_quote_info(context_data, analysis)
            missing_info = self._get_missing_quote_info(context_data, analysis)

            quote_request_id = None
            if should_create_quote:
                current_app.logger.info(f"🚀 Creating quote for: {context_data.get('user_name')} - Services: {analysis['services']}")
                quote_request_id = self._create_quote_request(conversation, context_data, analysis)
                bot_response += "\n\n✅ I've created a quote request for you! Our team will review your requirements and send you a detailed proposal within 2 hours."

                # Send SMS notification immediately (without background thread)
                try:
                    quote_request = QuoteRequest.query.get(quote_request_id)
                    if quote_request:
                        current_app.logger.info(f"📞 Attempting to send SMS for quote ID: {quote_request_id}")
                        sms_success = self._send_sms_directly(quote_request, analysis)
                        if sms_success:
                            current_app.logger.info(f"📱 SMS notification sent successfully for: {quote_request.client_name}")
                        else:
                            current_app.logger.warning(f"❌ SMS failed for: {quote_request.client_name}")
                    else:
                        current_app.logger.error(f"❌ Quote request not found with ID: {quote_request_id}")
                except Exception as e:
                    current_app.logger.error(f"💥 SMS sending error: {e}")
            elif missing_info and (analysis['intent'] == 'get_quote' or 'quote' in user_message.lower()):
                # Guide user to provide missing information
                bot_response += f"\n\n{missing_info}"
            else:
                current_app.logger.info(f"❌ Quote not created - insufficient info or not confirmed")
                current_app.logger.info(f"   - Has name: {bool(context_data.get('user_name'))}")
                current_app.logger.info(f"   - Has email: {bool(context_data.get('user_email'))}")
                current_app.logger.info(f"   - Has services: {analysis['services']}")
                current_app.logger.info(f"   - Quote confirmed: {context_data.get('quote_confirmed', False)}")

            # Save bot response
            bot_msg = ChatMessage(
                conversation_id=conversation_id,
                sender='bot',
                message=bot_response,
                message_type='text',
                message_metadata=json.dumps({
                    'intent': analysis['intent'],
                    'services': analysis['services'],
                    'quote_created': quote_request_id is not None
                })
            )
            db.session.add(bot_msg)

            # Update conversation context
            conversation.context_data = json.dumps(context_data)
            conversation.updated_at = datetime.utcnow()
            if quote_request_id:
                conversation.quote_request_id = quote_request_id

            db.session.commit()

            return {
                'success': True,
                'bot_response': bot_response,
                'conversation_id': conversation_id,
                'intent': analysis['intent'],
                'services': analysis['services'],
                'quote_created': quote_request_id is not None
            }

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Chatbot processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'bot_response': "I apologize, but I encountered an error. Please try again or contact us directly."
            }

    def _has_sufficient_quote_info(self, context_data: Dict, analysis: Dict) -> bool:
        """Check if we have enough information to create a quote"""
        required_fields = ['user_name', 'user_email']
        has_required = all(context_data.get(field) for field in required_fields)
        has_service = len(analysis['services']) > 0 or context_data.get('detected_services')

        # Also check if user explicitly confirmed quote creation
        user_confirmed = context_data.get('quote_confirmed', False)

        return has_required and has_service and user_confirmed

    def _get_missing_quote_info(self, context_data: Dict, analysis: Dict) -> str:
        """Generate helpful prompt for missing information"""
        missing_items = []

        if not context_data.get('user_name'):
            missing_items.append("**your name**")

        if not context_data.get('user_email'):
            missing_items.append("**your email address**")

        has_service = len(analysis['services']) > 0 or context_data.get('detected_services')
        if not has_service:
            missing_items.append("**which service you need** (logo design, website, social media, etc.)")

        user_confirmed = context_data.get('quote_confirmed', False)
        if not user_confirmed and missing_items:
            # If missing basic info, ask for it first
            if len(missing_items) == 1:
                return f"To create your quote, I just need {missing_items[0]}. Could you please provide that?"
            elif len(missing_items) == 2:
                return f"To create your quote, I need {missing_items[0]} and {missing_items[1]}. Could you please provide those details?"
            else:
                items_text = ", ".join(missing_items[:-1]) + f", and {missing_items[-1]}"
                return f"To create your quote, I need {items_text}. Could you please provide those details?"
        elif not user_confirmed and not missing_items:
            # Has all info but needs confirmation
            return "I have all the details for your quote. Should I go ahead and create it for you? Just say **'yes'** or **'create the quote'** to confirm!"

        return ""

    def extract_user_info_from_message(self, message: str) -> Dict:
        """Extract user information from a message"""
        import re

        info = {}
        message_lower = message.lower()

        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, message)
        if emails:
            info['email'] = emails[0]

        # Extract names - various patterns
        name_patterns = [
            r'my name is\s+([A-Za-z\s]+)',
            r'i am\s+([A-Za-z\s]+)',
            r'i\'m\s+([A-Za-z\s]+)',
            r'name:\s*([A-Za-z\s]+)',
            r'call me\s+([A-Za-z\s]+)',
        ]

        for pattern in name_patterns:
            match = re.search(pattern, message_lower)
            if match:
                name = match.group(1).strip().title()
                # Remove common words that might be captured
                name_words = name.split()
                if len(name_words) <= 3 and all(word.isalpha() for word in name_words):
                    info['name'] = name
                    break

        # Also check if the entire message might be a name (when asked "What's your name?")
        if not info.get('name') and len(message.split()) <= 3 and message.replace(' ', '').isalpha():
            # Likely a name response
            info['name'] = message.strip().title()

        return info

    def _create_quote_request(self, conversation: ChatConversation, context_data: Dict, analysis: Dict) -> int:
        """Create a quote request from conversation data"""
        try:
            # Determine primary service
            services = analysis.get('services', []) or context_data.get('detected_services', [])
            primary_service = services[0] if services else 'General Design'

            # Create quote request
            quote_request = QuoteRequest(
                client_name=context_data.get('user_name', 'Chatbot User'),
                email=context_data.get('user_email', ''),
                phone=context_data.get('user_phone', ''),
                company_name=context_data.get('user_company', ''),
                services_requested=', '.join(services) if services else primary_service,
                project_description=self._generate_project_description(context_data, analysis),
                budget_range=analysis.get('budget') or context_data.get('budget_range', 'To be discussed'),
                timeline=context_data.get('timeline', 'Standard'),
                additional_requirements=context_data.get('additional_requirements', ''),
                status='pending'
            )

            db.session.add(quote_request)
            db.session.flush()  # Get the ID

            # Trigger SMS/WhatsApp notification in background
            self._send_quote_notifications(quote_request, analysis)

            return quote_request.id

        except Exception as e:
            current_app.logger.error(f"Quote creation error: {e}")
            raise

    def _send_quote_notifications(self, quote_request: QuoteRequest, analysis: Dict):
        """Send SMS/WhatsApp notifications for new quote request"""
        try:
            # Prepare quote data for existing notification system
            quote_data = {
                'client_name': quote_request.client_name,
                'email': quote_request.email,
                'phone': quote_request.phone,
                'company_name': quote_request.company_name,
                'services_requested': quote_request.services_requested,
                'project_description': quote_request.project_description,
                'budget_range': quote_request.budget_range,
                'timeline': quote_request.timeline,
                'additional_requirements': quote_request.additional_requirements
            }

            # Import notification functions from app
            from app import analyze_quote_with_ai, send_sms_notification, generate_ai_enhanced_whatsapp_message
            import webbrowser
            import urllib.parse
            import os
            import asyncio
            from threading import Thread

            def send_notifications():
                try:
                    # Run AI analysis
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                    try:
                        ai_analysis = loop.run_until_complete(analyze_quote_with_ai(quote_data))

                        # Add chatbot-specific context
                        ai_analysis['source'] = 'AI Chatbot'
                        ai_analysis['conversation_id'] = getattr(quote_request, 'id', 'Unknown')

                        # Send SMS notification
                        sms_sent = send_sms_notification(quote_data, ai_analysis)

                        if sms_sent:
                            print(f"[SUCCESS] SMS sent for chatbot quote: {quote_request.client_name} - Priority: {ai_analysis['priority']}/10")
                        else:
                            # Fallback to WhatsApp if SMS fails
                            ai_message = loop.run_until_complete(generate_ai_enhanced_whatsapp_message(quote_data, ai_analysis))
                            ai_message += f"\n\n[AI Chatbot] Source: AI Chatbot Conversation"

                            encoded_message = urllib.parse.quote(ai_message)
                            whatsapp_url = f"https://wa.me/{os.getenv('TARGET_WHATSAPP_NUMBER', '919518536672')}?text={encoded_message}"
                            webbrowser.open(whatsapp_url)

                            print(f"[WHATSAPP] Fallback used for chatbot quote: {quote_request.client_name}")

                    finally:
                        loop.close()

                except Exception as e:
                    print(f"[ERROR] Quote notification error: {e}")

            # Run in background thread
            Thread(target=send_notifications, daemon=True).start()
            print(f"[BACKGROUND] SMS notification started for: {quote_request.client_name}")

        except Exception as e:
            current_app.logger.error(f"Failed to setup quote notifications: {e}")

    def _send_sms_directly(self, quote_request: QuoteRequest, analysis: Dict):
        """Send SMS notification directly without background thread"""
        try:
            # Prepare quote data for existing notification system
            quote_data = {
                'client_name': quote_request.client_name,
                'email': quote_request.email,
                'phone': quote_request.phone,
                'company_name': quote_request.company_name,
                'services_requested': quote_request.services_requested,
                'project_description': quote_request.project_description,
                'budget_range': quote_request.budget_range,
                'timeline': quote_request.timeline,
                'additional_requirements': quote_request.additional_requirements
            }

            # Import notification functions from app
            from app import analyze_quote_with_ai, send_sms_notification

            # Run AI analysis
            ai_analysis = await analyze_quote_with_ai(quote_data)

            # Add chatbot-specific context
            ai_analysis['source'] = 'AI Chatbot'
            ai_analysis['conversation_id'] = quote_request.id

            # Send SMS notification
            sms_sent = send_sms_notification(quote_data, ai_analysis)

            if sms_sent:
                current_app.logger.info(f"✅ SMS sent for chatbot quote: {quote_request.client_name} - Priority: {ai_analysis['priority']}/10")
                return True
            else:
                current_app.logger.warning(f"❌ SMS failed for chatbot quote: {quote_request.client_name}")
                return False

        except Exception as e:
            current_app.logger.error(f"Direct SMS sending error: {e}")
            return False

    def _generate_project_description(self, context_data: Dict, analysis: Dict) -> str:
        """Generate project description from conversation context"""
        services = analysis.get('services', []) or context_data.get('detected_services', [])

        description_parts = [
            f"Project initiated through AI chatbot conversation.",
            f"Services requested: {', '.join(services) if services else 'General design services'}."
        ]

        if context_data.get('user_company'):
            description_parts.append(f"Company: {context_data['user_company']}")

        if analysis.get('budget'):
            description_parts.append(f"Budget mentioned: ₹{analysis['budget']}")

        # Add recent messages as context
        if 'recent_messages' in context_data:
            user_messages = [
                msg['message'] for msg in context_data['recent_messages'][-5:]
                if msg['sender'] == 'user'
            ]
            if user_messages:
                description_parts.append(f"User requirements: {' | '.join(user_messages)}")

        return ' '.join(description_parts)

    def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """Get conversation message history"""
        messages = db.session.query(ChatMessage).filter_by(
            conversation_id=conversation_id
        ).order_by(ChatMessage.created_at.asc()).all()

        return [
            {
                'id': msg.id,
                'sender': msg.sender,
                'message': msg.message,
                'type': msg.message_type,
                'timestamp': msg.created_at.isoformat(),
                'metadata': json.loads(msg.message_metadata or '{}')
            }
            for msg in messages
        ]

# Initialize chatbot instance
def get_chatbot():
    """Get chatbot instance with OpenAI client"""
    from app import openai_client
    if not openai_client:
        raise Exception("OpenAI client not configured")
    return OrbitXChatbot(openai_client)