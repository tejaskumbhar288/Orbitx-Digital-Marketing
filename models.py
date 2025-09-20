from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(200))
    icon_class = db.Column(db.String(50))
    price_range = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    portfolio_items = db.relationship('Portfolio', backref='service', lazy=True)

    def __repr__(self):
        return f'<Service {self.name}>'

class ContactInquiry(db.Model):
    __tablename__ = 'contact_inquiries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    service_interested = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ContactInquiry {self.name}>'

class QuoteRequest(db.Model):
    __tablename__ = 'quote_requests'

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    company_name = db.Column(db.String(100))
    services_requested = db.Column(db.Text)
    project_description = db.Column(db.Text, nullable=False)
    budget_range = db.Column(db.String(50))
    timeline = db.Column(db.String(50))
    additional_requirements = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<QuoteRequest {self.client_name}>'

class Testimonial(db.Model):
    __tablename__ = 'testimonials'

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    testimonial_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    project_type = db.Column(db.String(100))
    client_image_url = db.Column(db.String(200))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Testimonial {self.client_name}>'

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(300))
    featured_image_url = db.Column(db.String(200))
    author = db.Column(db.String(100))
    is_published = db.Column(db.Boolean, default=False)
    tags = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<BlogPost {self.title}>'

class Portfolio(db.Model):
    __tablename__ = 'portfolio'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    image_url = db.Column(db.String(200))
    client_name = db.Column(db.String(100))
    project_date = db.Column(db.Date)
    tags = db.Column(db.String(200))
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Case study fields
    challenge = db.Column(db.Text)
    solution = db.Column(db.Text)
    results = db.Column(db.Text)
    client_testimonial = db.Column(db.Text)
    before_image_url = db.Column(db.String(200))
    after_image_url = db.Column(db.String(200))

    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []

    def __repr__(self):
        return f'<Portfolio {self.title}>'