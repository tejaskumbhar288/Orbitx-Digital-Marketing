from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from models import db, Service, ContactInquiry, QuoteRequest, Testimonial, BlogPost, Portfolio
from forms import ContactForm, QuoteForm
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration from environment variables
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "instance", "database.db")}')
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

    if form.validate_on_submit():
        # Create quote request
        quote_request = QuoteRequest(
            client_name=form.client_name.data,
            email=form.email.data,
            phone=form.phone.data,
            company_name=form.company_name.data,
            services_requested=form.services_requested.data,
            project_description=form.project_description.data,
            budget_range=form.budget_range.data,
            timeline=form.timeline.data,
            additional_requirements=form.additional_requirements.data,
            status='pending'
        )

        try:
            db.session.add(quote_request)
            db.session.commit()

            # Send email notification
            if app.config['MAIL_USERNAME']:
                try:
                    msg = Message(
                        subject=f"New Quote Request from {form.client_name.data}",
                        recipients=[app.config['MAIL_USERNAME']],
                        body=f"""
New quote request received:

Client: {form.client_name.data}
Email: {form.email.data}
Service: {form.services_requested.data}
Budget: {form.budget_range.data}
Timeline: {form.timeline.data}

Project Description:
{form.project_description.data}

Please prepare and send a detailed quote.
                        """
                    )
                    mail.send(msg)
                except Exception as e:
                    app.logger.error(f"Failed to send email: {e}")

            flash('Thank you! We\'ve received your quote request and will send you a detailed proposal within 24 hours.', 'success')
            return redirect(url_for('quote'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Database error: {e}")
            flash('Sorry, there was an error submitting your request. Please try again.', 'error')

    return render_template('quote.html', form=form)

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

# Context processors for global template variables
@app.context_processor
def inject_globals():
    return {
        'current_year': datetime.now().year,
        'site_name': 'Sarvesh Kumbhar Design Services'
    }

if __name__ == '__main__':
    app.run(debug=True)