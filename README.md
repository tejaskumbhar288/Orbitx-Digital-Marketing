# Sarvesh Kumbhar Design Services Website

A modern, professional digital marketing website built with Flask, featuring a complete design portfolio, service offerings, and client management system. Inspired by Digital Silk's design approach with custom branding and functionality.

## 🚀 Features

### Frontend Features
- **Modern Design**: Digital Silk-inspired design with gradients, animations, and professional layouts
- **Responsive Layout**: Mobile-first design that works on all devices
- **Interactive Portfolio**: Filterable gallery with lightbox functionality
- **Service Showcase**: Detailed service pages with pricing and timelines
- **Contact Forms**: Professional contact and quote request forms
- **Case Studies**: Before/after showcases with success metrics
- **Performance Optimized**: Lazy loading, optimized images, and fast loading times

### Backend Features
- **Flask Framework**: Robust Python web framework
- **Database Management**: SQLAlchemy ORM with SQLite database
- **Form Processing**: Advanced form handling with validation
- **Email Integration**: Automated email notifications for inquiries
- **Admin Interface**: Easy content management
- **File Upload**: Secure file handling for project references
- **SEO Optimized**: Meta tags, structured data, and search-friendly URLs

### Business Features
- **Lead Generation**: Multiple conversion paths and CTAs
- **Quote System**: Detailed project estimation workflow  
- **Client Management**: Track inquiries and project requests
- **Portfolio Management**: Easy addition and categorization of work
- **Testimonial System**: Client feedback and rating system
- **Analytics Ready**: Google Analytics integration points

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Styling**: Bootstrap 5 + Custom CSS
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Inter, Poppins)
- **Animations**: AOS (Animate On Scroll)
- **Forms**: Flask-WTF with validation
- **Email**: Flask-Mail for notifications

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (recommended)

## 🚀 Installation & Setup

### 1. Clone or Download the Project
```bash
# If using Git
git clone <repository-url>
cd digital-marketing-website

# Or download and extract the zip file
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-here-change-this
FLASK_ENV=development
FLASK_DEBUG=True

# Database
DATABASE_URL=sqlite:///instance/database.db

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=sarveshkumbhar10@gmail.com
MAIL_PASSWORD=your-app-password-here
MAIL_DEFAULT_SENDER=sarveshkumbhar10@gmail.com

# File Upload
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=static/uploads
```

### 5. Initialize Database
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database created successfully!')"
```

### 6. Create Required Directories
```bash
mkdir -p static/uploads
mkdir -p static/images/portfolio
mkdir -p static/images/services
mkdir -p instance
```

### 7. Run the Application
```bash
python app.py
```

The website will be available at `http://localhost:5000`

## 📁 Project Structure

```
digital_marketing_website/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── forms.py                    # WTF Forms
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .env                        # Environment variables (create this)
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   └── main.js           # JavaScript functionality
│   ├── images/               # Website images
│   │   ├── logo.png         # Company logo
│   │   ├── services/        # Service images
│   │   └── portfolio/       # Portfolio images
│   └── uploads/             # User uploaded files
├── templates/                  # HTML templates
│   ├── base.html             # Base template
│   ├── index.html            # Homepage
│   ├── about.html            # About page
│   ├── services.html         # Services listing
│   ├── service_detail.html   # Individual service page
│   ├── portfolio.html        # Portfolio gallery
│   ├── case_studies.html     # Case studies
│   ├── contact.html          # Contact page
│   ├── quote.html            # Quote request
│   └── components/           # Template components
│       ├── navbar.html       # Navigation bar
│       └── footer.html       # Footer
└── instance/                  # Instance-specific files
    └── database.db           # SQLite database (auto-generated)
```

## 🎨 Customization Guide

### 1. Branding & Colors
Edit `static/css/style.css` and modify the CSS variables:
```css
:root {
    --primary: #4F46E5;           /* Main brand color */
    --secondary: #F59E0B;         /* Accent color */
    --gradient-primary: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
}
```

### 2. Content Updates
- **Contact Information**: Update in `templates/components/footer.html` and `templates/contact.html`
- **Services**: Modify in `app.py` or add through admin interface
- **About Content**: Edit `templates/about.html`
- **Homepage Hero**: Update `templates/index.html`

### 3. Images
- Add your logo to `static/images/logo.png`
- Add service images to `static/images/services/`
- Add portfolio images to `static/images/portfolio/`
- Update image paths in templates as needed

### 4. Email Configuration
Update email settings in your `.env` file:
- For Gmail: Use App Passwords instead of regular password
- For other providers: Update MAIL_SERVER and MAIL_PORT accordingly

## 📧 Email Setup

### Gmail Setup (Recommended)
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App Passwords
   - Generate password for "Mail"
3. Use the generated password in your `.env` file

### Other Email Providers
Update the mail configuration in `.env`:
```env
# For Outlook/Hotmail
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587

# For Yahoo
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production with Gunicorn
```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

### Environment Variables for Production
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-production-secret-key
```

## 📊 Database Management

### View Database Content
```python
from app import app, db, Service, Portfolio, ContactInquiry, QuoteRequest

with app.app_context():
    # View all services
    services = Service.query.all()
    for service in services:
        print(f"{service.id}: {service.name}")
    
    # View contact inquiries
    inquiries = ContactInquiry.query.all()
    for inquiry in inquiries:
        print(f"{inquiry.name}: {inquiry.email}")
```

### Add Sample Data
```python
from app import app, db, Service, Testimonial

with app.app_context():
    # Add a new service
    service = Service(
        name="Custom Service",
        description="Service description",
        short_description="Brief description",
        icon_class="fas fa-star",
        price_range="₹5,000 - ₹15,000",
        is_active=True
    )
    db.session.add(service)
    db.session.commit()
```

## 🔒 Security Features

- **CSRF Protection**: All forms include CSRF tokens
- **Input Validation**: Server-side validation for all inputs
- **File Upload Security**: Restricted file types and sizes
- **SQL Injection Prevention**: SQLAlchemy ORM protects against SQL injection
- **XSS Protection**: Input sanitization and validation

## 📱 Mobile Responsiveness

The website is fully responsive with:
- Mobile-first CSS design
- Optimized touch interactions
- Responsive navigation menu
- Scalable images and text
- Touch-friendly buttons and forms

## 🎯 SEO Features

- **Meta Tags**: Dynamic meta descriptions for each page
- **Structured Data**: Rich snippets ready
- **Semantic HTML**: Proper heading hierarchy
- **Fast Loading**: Optimized images and code
- **Mobile Friendly**: Google mobile-first indexing ready

## 🔧 Troubleshooting

### Common Issues

1. **Database Errors**
   - Delete `instance/database.db` and run database creation again
   - Check file permissions for the instance folder

2. **Email Not Sending**
   - Verify email credentials in `.env`
   - Check firewall/antivirus blocking SMTP
   - Ensure App Password is used for Gmail

3. **Images Not Loading**
   - Check file paths in templates
   - Verify images exist in static/images/
   - Check file permissions

4. **CSS/JS Not Loading**
   - Hard refresh browser (Ctrl+F5)
   - Check console for errors
   - Verify static file paths

### Performance Optimization

1. **Image Optimization**
   - Compress images before uploading
   - Use appropriate file formats (WebP when possible)
   - Implement lazy loading (already included)

2. **Caching**
   - Enable browser caching for static files
   - Consider implementing Redis for session storage
   - Use CDN for static assets in production

## 📞 Support

For technical support or customization requests:
- **Email**: sarveshkumbhar10@gmail.com
- **Phone**: +91 95187 54011
- **WhatsApp**: [Message on WhatsApp](https://wa.me/919518754011)

## 📄 License

This project is created for Sarvesh Kumbhar Design Services. All rights reserved.

## 🎉 Getting Started Checklist

- [ ] Install Python 3.8+
- [ ] Create virtual environment
- [ ] Install requirements
- [ ] Create .env file with configurations
- [ ] Initialize database
- [ ] Add your logo and images
- [ ] Update contact information
- [ ] Configure email settings
- [ ] Run the application
- [ ] Test all forms and functionality
- [ ] Customize branding and content
- [ ] Deploy to production server

## 🚀 Quick Start Commands

```bash
# Setup (run once)
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Create database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Run application
python app.py
```

---

**Built with ❤️ for Sarvesh Kumbhar Design Services**

Transform your business with professional design solutions that drive results!