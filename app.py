from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from models import db, Service, ContactInquiry, QuoteRequest, Testimonial, BlogPost, Portfolio, ChatConversation, ChatMessage
from forms import ContactForm, QuoteForm
import os
from datetime import datetime
import logging
from dotenv import load_dotenv
import urllib.parse
import webbrowser
import asyncio
import openai
from twilio.rest import Client
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration from environment variables
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration with fallback
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

# For Render deployment, use in-memory SQLite if no DATABASE_URL
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Create instance directory if it doesn't exist
    instance_dir = os.path.join(basedir, "instance")
    os.makedirs(instance_dir, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_dir, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER') or os.environ.get('MAIL_USERNAME')

# File upload configuration
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

# Initialize extensions
db.init_app(app)
mail = Mail(app)

# Initialize OpenAI client
openai_client = None
try:
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key.strip() and not api_key.startswith('REPLACE_WITH'):
        # Initialize with minimal configuration to avoid proxy/environment conflicts
        openai_client = openai.OpenAI(
            api_key=api_key.strip(),
            timeout=30.0
        )
        print("OpenAI client initialized successfully")
    else:
        print("OPENAI_API_KEY not found or is placeholder - chatbot will not work")
        openai_client = None
except Exception as e:
    print(f"Failed to initialize OpenAI client: {e}")
    # Try alternative initialization without extra parameters
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and not api_key.startswith('REPLACE_WITH'):
            import openai as openai_alt
            openai_client = openai_alt.OpenAI(api_key=api_key.strip())
            print("OpenAI client initialized successfully (fallback)")
    except Exception as e2:
        print(f"Fallback OpenAI initialization also failed: {e2}")
        openai_client = None

# Initialize Twilio client
twilio_client = None
if os.getenv('TWILIO_ACCOUNT_SID') and os.getenv('TWILIO_AUTH_TOKEN'):
    twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

# AI Analysis Functions
def analyze_quote_with_ai(quote_data):
    """Analyze quote with OpenAI for priority and value estimation"""
    if not openai_client:
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

        response = openai_client.chat.completions.create(
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
        app.logger.error(f"AI analysis error: {e}")
        return {"priority": 5, "estimated_value": "Rs 5,000-15,000", "strategy": "Standard response"}

async def generate_ai_enhanced_whatsapp_message(quote_data, analysis):
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

def send_sms_notification(quote_data, analysis):
    """Send SMS notification via Twilio"""
    if not twilio_client:
        app.logger.warning("Twilio not configured - SMS notification skipped")
        return False

    try:
        # Generate concise SMS message
        priority_text = "HIGH PRIORITY" if analysis['priority'] >= 8 else "MEDIUM" if analysis['priority'] >= 6 else "STANDARD"

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

        # Send SMS
        sms = twilio_client.messages.create(
            body=message,
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            to=os.getenv('TARGET_PHONE_NUMBER')
        )

        app.logger.info(f"SMS sent successfully - SID: {sms.sid}, Status: {sms.status}")
        return True

    except Exception as e:
        app.logger.error(f"Failed to send SMS: {e}")
        return False

# Routes
@app.route('/')
def index():
    """Homepage with featured services and portfolio items"""
    services = Service.query.filter_by(is_active=True).limit(6).all()
    portfolio_items = Portfolio.query.filter_by(is_featured=True).limit(8).all()
    testimonials = Testimonial.query.filter_by(is_featured=True).limit(3).all()
    return render_template('index.html',
                         services=services,
                         portfolio_items=portfolio_items,
                         testimonials=testimonials)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/services')
def services():
    """Services listing page"""
    services = Service.query.filter_by(is_active=True).all()
    return render_template('services.html', services=services)

@app.route('/service/<int:service_id>')
def service_detail(service_id):
    """Individual service detail page"""
    service = Service.query.get_or_404(service_id)
    related_portfolio = Portfolio.query.filter_by(service_id=service_id).limit(6).all()
    return render_template('service_detail.html', service=service, related_portfolio=related_portfolio)

@app.route('/portfolio')
def portfolio():
    """Portfolio gallery with filtering"""
    service_filter = request.args.get('service', 'all')

    if service_filter == 'all':
        portfolio_items = Portfolio.query.all()
    else:
        try:
            service_id = int(service_filter)
            portfolio_items = Portfolio.query.filter_by(service_id=service_id).all()
        except ValueError:
            portfolio_items = Portfolio.query.all()

    services = Service.query.filter_by(is_active=True).all()
    return render_template('portfolio.html',
                         portfolio_items=portfolio_items,
                         services=services,
                         current_filter=service_filter)

@app.route('/case-studies')
def case_studies():
    """Case studies listing"""
    case_studies = Portfolio.query.filter(
        Portfolio.challenge.isnot(None),
        Portfolio.solution.isnot(None)
    ).all()
    return render_template('case_studies.html', case_studies=case_studies)

@app.route('/case-study/<int:case_study_id>')
def case_study_detail(case_study_id):
    """Individual case study detail"""
    case_study = Portfolio.query.get_or_404(case_study_id)
    return render_template('case_study_detail.html', case_study=case_study)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form handling"""
    form = ContactForm()

    if form.validate_on_submit():
        # Create contact inquiry
        inquiry = ContactInquiry(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            service_interested=form.service_interested.data,
            message=form.message.data,
            status='new'
        )

        try:
            db.session.add(inquiry)
            db.session.commit()

            # Send email notification
            if app.config['MAIL_USERNAME']:
                try:
                    msg = Message(
                        subject=f"New Contact Inquiry from {form.name.data}",
                        recipients=[app.config['MAIL_USERNAME']],
                        body=f"""
New contact inquiry received:

Name: {form.name.data}
Email: {form.email.data}
Subject: {form.subject.data}

Message:
{form.message.data}

Reply to this inquiry as soon as possible.
                        """
                    )
                    mail.send(msg)
                except Exception as e:
                    app.logger.error(f"Failed to send email: {e}")

            flash('Thank you for your message! We\'ll get back to you within 24 hours.', 'success')
            return redirect(url_for('contact'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Database error: {e}")
            flash('Sorry, there was an error submitting your message. Please try again.', 'error')

    return render_template('contact.html', form=form)

@app.route('/quote', methods=['GET', 'POST'])
def quote():
    """Quote request page"""
    form = QuoteForm()

    if request.method == 'POST':
        # Create quote request from raw form data
        quote_request = QuoteRequest(
            client_name=request.form.get('client_name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            company_name=request.form.get('company_name'),
            services_requested=request.form.get('services_requested'),
            project_description=request.form.get('project_description'),
            budget_range=request.form.get('budget_range'),
            timeline=request.form.get('timeline'),
            additional_requirements=request.form.get('additional_requirements'),
            status='pending'
        )

        try:
            db.session.add(quote_request)
            db.session.commit()

            # Send AI-enhanced WhatsApp notification
            try:
                # Prepare quote data for AI analysis
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

                # Run AI analysis and generate enhanced message
                def run_ai_analysis():
                    try:
                        # Analyze quote with AI
                        analysis = analyze_quote_with_ai(quote_data)

                        # Generate AI-enhanced message
                        ai_message = asyncio.run(generate_ai_enhanced_whatsapp_message(quote_data, analysis))

                        # URL encode the message for WhatsApp
                        encoded_message = urllib.parse.quote(ai_message)
                        whatsapp_url = f"https://wa.me/{os.getenv('TARGET_WHATSAPP_NUMBER', '919518536672')}?text={encoded_message}"

                        # Open WhatsApp Web
                        webbrowser.open(whatsapp_url)

                        app.logger.info(f"AI-enhanced WhatsApp URL opened for {quote_request.client_name} - Priority: {analysis['priority']}/10")

                    except Exception as e:
                        app.logger.error(f"AI analysis failed: {e}")
                        # Fallback to basic message
                        basic_message = f"NEW QUOTE REQUEST - OrbitX\nClient: {quote_request.client_name}\nEmail: {quote_request.email}\nService: {quote_request.services_requested}"
                        encoded_message = urllib.parse.quote(basic_message)
                        whatsapp_url = f"https://wa.me/{os.getenv('TARGET_WHATSAPP_NUMBER', '919518536672')}?text={encoded_message}"
                        webbrowser.open(whatsapp_url)

                # Run AI analysis in background thread
                from threading import Thread
                Thread(target=run_ai_analysis, daemon=True).start()

            except Exception as e:
                app.logger.error(f"Failed to process AI-enhanced WhatsApp: {e}")

            flash('Thank you! We\'ve received your quote request. Our team will contact you within 2 hours via WhatsApp/Email with a detailed proposal.', 'success')
            return redirect(url_for('quote'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Database error: {e}")
            flash('Sorry, there was an error submitting your request. Please try again.', 'error')

    return render_template('quote.html', form=form)

@app.route('/quote-simple')
def simple_quote():
    """Simple quote form without complex validation"""
    return render_template('simple_quote.html')

@app.route('/quote/simple', methods=['POST'])
def simple_quote_submission():
    """Simple quote submission endpoint for direct testing"""
    try:
        # Create quote request from JSON or form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        quote_request = QuoteRequest(
            client_name=data.get('client_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            company_name=data.get('company_name'),
            services_requested=data.get('services_requested'),
            project_description=data.get('project_description'),
            budget_range=data.get('budget_range'),
            timeline=data.get('timeline'),
            additional_requirements=data.get('additional_requirements'),
            status='pending'
        )

        db.session.add(quote_request)
        db.session.commit()

        # Process with AI-enhanced messaging
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

        # Background AI processing with SMS
        def process_quote():
            try:
                # AI analysis
                analysis = analyze_quote_with_ai(quote_data)

                # Send SMS notification
                sms_sent = send_sms_notification(quote_data, analysis)

                if sms_sent:
                    app.logger.info(f"SMS quote notification sent for {quote_request.client_name} - Priority: {analysis['priority']}/10")
                else:
                    app.logger.warning(f"SMS failed for {quote_request.client_name} - using fallback")
                    # Fallback to WhatsApp if SMS fails
                    ai_message = asyncio.run(generate_ai_enhanced_whatsapp_message(quote_data, analysis))
                    import urllib.parse
                    encoded_message = urllib.parse.quote(ai_message)
                    whatsapp_url = f"https://wa.me/{os.getenv('TARGET_WHATSAPP_NUMBER', '919518536672')}?text={encoded_message}"
                    import webbrowser
                    webbrowser.open(whatsapp_url)
                    app.logger.info(f"WhatsApp fallback used for {quote_request.client_name}")

            except Exception as e:
                app.logger.error(f"Quote processing failed: {e}")

        from threading import Thread
        Thread(target=process_quote, daemon=True).start()

        return jsonify({
            "success": True,
            "message": "Quote submitted successfully",
            "quote_id": quote_request.id
        })

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Simple quote submission error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/admin/whatsapp/<int:quote_id>')
def admin_whatsapp_quote(quote_id):
    """Admin route to open WhatsApp with quote details"""
    quote_request = QuoteRequest.query.get_or_404(quote_id)

    # Prepare WhatsApp message
    whatsapp_message = f"""🎯 NEW QUOTE REQUEST - OrbitX

👤 Client: {quote_request.client_name}
📧 Email: {quote_request.email}
📱 Phone: {quote_request.phone or 'Not provided'}
🏢 Company: {quote_request.company_name or 'Not provided'}

🛠️ Service: {quote_request.services_requested}
💰 Budget: {quote_request.budget_range or 'Not specified'}
⏰ Timeline: {quote_request.timeline or 'Not specified'}

📝 Project Description:
{quote_request.project_description}

📋 Additional Requirements:
{quote_request.additional_requirements or 'None specified'}

⚡ Action Required: Prepare and send detailed quote to {quote_request.email}"""

    # URL encode the message for WhatsApp
    encoded_message = urllib.parse.quote(whatsapp_message)
    whatsapp_url = f"https://wa.me/919518536672?text={encoded_message}"

    return redirect(whatsapp_url)

@app.route('/blog')
def blog():
    """Blog listing page"""
    posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post"""
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('blog_post.html', post=post)

# API endpoints for AJAX requests
@app.route('/api/portfolio/<int:item_id>')
def api_portfolio_item(item_id):
    """API endpoint for portfolio item details"""
    item = Portfolio.query.get_or_404(item_id)
    return jsonify({
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'image_url': item.image_url,
        'client_name': item.client_name,
        'tags': item.tags
    })

# Favicon route
@app.route('/favicon.ico')
def favicon():
    """Handle favicon requests"""
    return app.send_static_file('favicon.ico')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Chatbot API endpoints
@app.route('/api/chatbot/message', methods=['POST'])
def chatbot_message():
    """Handle chatbot messages"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id') or str(uuid.uuid4())
        user_info = data.get('user_info', {})

        if not user_message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400

        # Import chatbot here to avoid circular imports
        from chatbot import get_chatbot
        chatbot = get_chatbot()

        # Process message
        result = chatbot.process_message(conversation_id, user_message, user_info)

        return jsonify(result)

    except Exception as e:
        app.logger.error(f"Chatbot API error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'bot_response': "I apologize, but I'm experiencing technical difficulties. Please try again or contact us directly."
        }), 500

@app.route('/api/chatbot/history/<conversation_id>')
def chatbot_history(conversation_id):
    """Get conversation history"""
    try:
        from chatbot import get_chatbot
        chatbot = get_chatbot()

        history = chatbot.get_conversation_history(conversation_id)

        return jsonify({
            'success': True,
            'conversation_id': conversation_id,
            'messages': history
        })

    except Exception as e:
        app.logger.error(f"Chatbot history error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chatbot/services')
def chatbot_services():
    """Get available services for chatbot"""
    try:
        services = Service.query.filter_by(is_active=True).all()
        return jsonify({
            'success': True,
            'services': [
                {
                    'id': service.id,
                    'name': service.name,
                    'description': service.short_description or service.description[:100],
                    'price_range': service.price_range,
                    'icon': service.icon_class
                }
                for service in services
            ]
        })
    except Exception as e:
        app.logger.error(f"Services API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/chatbot/portfolio')
def chatbot_portfolio():
    """Get portfolio items for chatbot"""
    try:
        portfolio_items = Portfolio.query.filter_by(is_featured=True).limit(6).all()
        return jsonify({
            'success': True,
            'portfolio': [
                {
                    'id': item.id,
                    'title': item.title,
                    'description': item.description[:100] if item.description else '',
                    'client_name': item.client_name,
                    'service': item.service.name if item.service else '',
                    'image_url': item.image_url,
                    'tags': item.get_tags_list()
                }
                for item in portfolio_items
            ]
        })
    except Exception as e:
        app.logger.error(f"Portfolio API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Context processors for global template variables
@app.context_processor
def inject_globals():
    return {
        'current_year': datetime.now().year,
        'site_name': 'OrbitX'
    }

# Create database tables on startup - always run this
try:
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

        # Initialize comprehensive data if database is empty
        if not Service.query.first():
            print("Initializing comprehensive website data...")
            # Import and run the comprehensive data population
            try:
                from populate_data import populate_all_data
                populate_all_data()
                print("Comprehensive data initialization completed!")
            except Exception as populate_error:
                print(f"Error with comprehensive data population: {populate_error}")
                # Fallback to basic services if comprehensive population fails
                print("Falling back to basic service creation...")
                basic_services = [
                    Service(name='Logo Design', description='Professional logo design', icon_class='fas fa-palette', price_range='₹2,000 - ₹15,000', is_active=True),
                    Service(name='Website Design', description='Modern website development', icon_class='fas fa-laptop-code', price_range='₹10,000 - ₹50,000', is_active=True),
                    Service(name='Social Media Design', description='Social media graphics', icon_class='fas fa-share-alt', price_range='₹5,000 - ₹20,000', is_active=True)
                ]
                for service in basic_services:
                    db.session.add(service)
                db.session.commit()
        else:
            print("Database already has data, skipping initialization")

except Exception as e:
    print(f"Database initialization error: {e}")

if __name__ == '__main__':
    # Run app based on environment
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    else:
        app.run(debug=True)