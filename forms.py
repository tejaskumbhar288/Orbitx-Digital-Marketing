from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    service_interested = SelectField('Service Interested', choices=[
        ('', 'Select a service...'),
        ('logo-design', 'Logo Design & Branding'),
        ('business-card', 'Business Card Design'),
        ('flyer-design', 'Flyer Design'),
        ('social-media', 'Social Media Creatives'),
        ('packaging', 'Packaging Design'),
        ('invitation-cards', 'Invitation Card Design'),
        ('powerpoint', 'PowerPoint Presentations'),
        ('campaign-design', 'Campaign Design'),
        ('label-design', 'Label Design'),
        ('other', 'Other')
    ], validators=[Optional()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Message')

class QuoteForm(FlaskForm):
    client_name = StringField('Client Name', validators=[DataRequired(), Length(min=2, max=100)], render_kw={'maxlength': 100})
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)], render_kw={'maxlength': 100})
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=254)], render_kw={'maxlength': 254})
    phone = StringField('Phone', validators=[Optional(), Length(max=20)], render_kw={'maxlength': 20})
    company_name = StringField('Company Name', validators=[Optional(), Length(max=100)], render_kw={'maxlength': 100})
    services_requested = SelectField('Services Requested', choices=[
        ('', 'Select a service...'),
        ('logo-design', 'Logo Design & Branding'),
        ('business-card', 'Business Card Design'),
        ('flyer-design', 'Flyer Design'),
        ('social-media', 'Social Media Creatives'),
        ('packaging', 'Packaging Design'),
        ('invitation-cards', 'Invitation Card Design'),
        ('powerpoint', 'PowerPoint Presentations'),
        ('campaign-design', 'Campaign Design'),
        ('label-design', 'Label Design'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    budget_range = SelectField('Budget Range', choices=[
        ('500-1000', '₹500 - ₹1,000'),
        ('1000-2500', '₹1,000 - ₹2,500'),
        ('2500-5000', '₹2,500 - ₹5,000'),
        ('5000-10000', '₹5,000 - ₹10,000'),
        ('10000+', '₹10,000+'),
        ('discuss', 'Let\'s Discuss')
    ], validators=[Optional()])
    timeline = SelectField('Timeline', choices=[
        ('urgent', 'Urgent (1-2 days)'),
        ('week', 'Within a week'),
        ('two-weeks', '2-3 weeks'),
        ('month', 'Within a month'),
        ('flexible', 'Flexible')
    ], validators=[Optional()])
    project_description = TextAreaField('Project Description', validators=[DataRequired(), Length(min=10, max=2000)], render_kw={'maxlength': 2000})
    additional_requirements = TextAreaField('Additional Requirements', validators=[Optional(), Length(max=1000)], render_kw={'maxlength': 1000})
    reference_files = FileField('Reference Files (Optional)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx'], 'Images and documents only!')
    ])
    subscribe_newsletter = BooleanField('Subscribe to our newsletter for design tips and updates')
    submit = SubmitField('Get Quote')

class NewsletterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')