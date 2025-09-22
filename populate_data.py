#!/usr/bin/env python3
"""
Populate database with comprehensive OrbitX data
Based on original website structure and available images
"""

import os
from app import app, db
from models import Service, Portfolio, Testimonial, BlogPost
from datetime import datetime, date

def populate_all_data():
    """Populate all database tables with comprehensive data"""
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        Portfolio.query.delete()
        Testimonial.query.delete()
        Service.query.delete()

        # Create comprehensive services
        print("Creating comprehensive services...")
        services = [
            {
                'name': 'Logo Design & Branding',
                'description': 'Professional logo design and complete branding solutions including brand identity, color palettes, typography, and brand guidelines.',
                'short_description': 'Custom logo design with complete brand identity',
                'icon_class': 'fas fa-palette',
                'price_range': '₹2,000 - ₹15,000'
            },
            {
                'name': 'Social Media Design',
                'description': 'Creative social media graphics, posts, stories, and complete social media branding for all platforms.',
                'short_description': 'Engaging social media visuals and content',
                'icon_class': 'fas fa-share-alt',
                'price_range': '₹3,000 - ₹20,000'
            },
            {
                'name': 'Flyer Design',
                'description': 'Eye-catching flyer designs for events, promotions, and marketing campaigns with print-ready formats.',
                'short_description': 'Professional marketing flyers and promotions',
                'icon_class': 'fas fa-file-image',
                'price_range': '₹1,000 - ₹5,000'
            },
            {
                'name': 'Business Card Design',
                'description': 'Professional business card designs with unique layouts, premium finishes, and brand consistency.',
                'short_description': 'Premium business card designs',
                'icon_class': 'fas fa-address-card',
                'price_range': '₹500 - ₹3,000'
            },
            {
                'name': 'Packaging Design',
                'description': 'Creative packaging design for products including labels, boxes, bottles, and retail packaging.',
                'short_description': 'Professional product packaging solutions',
                'icon_class': 'fas fa-box-open',
                'price_range': '₹5,000 - ₹25,000'
            },
            {
                'name': 'Invitation Card Design',
                'description': 'Beautiful invitation cards for weddings, events, and special occasions with custom designs.',
                'short_description': 'Custom invitation cards for all occasions',
                'icon_class': 'fas fa-envelope-open-text',
                'price_range': '₹800 - ₹4,000'
            },
            {
                'name': 'Label Design',
                'description': 'Product label design for bottles, packages, and retail products with brand compliance.',
                'short_description': 'Professional product label designs',
                'icon_class': 'fas fa-tags',
                'price_range': '₹1,500 - ₹8,000'
            },
            {
                'name': 'PowerPoint Presentations',
                'description': 'Professional presentation design for corporate, business, and educational purposes.',
                'short_description': 'Corporate presentation design services',
                'icon_class': 'fas fa-presentation-screen',
                'price_range': '₹2,000 - ₹10,000'
            }
        ]

        service_objects = []
        for service_data in services:
            service = Service(**service_data, is_active=True)
            db.session.add(service)
            service_objects.append(service)

        db.session.commit()
        print(f"Created {len(services)} services")

        # Create portfolio items
        print("Creating portfolio items...")
        portfolio_items = [
            # Logo Design Portfolio
            {
                'title': 'Gardenia Indoor Plants - Complete Branding',
                'description': 'Complete brand identity design for Gardenia indoor plants including logo, color palette, business cards, and marketing materials.',
                'service_id': service_objects[0].id,  # Logo Design
                'image_url': '/static/images/Gardenia-project/gardenia-main-image.png',
                'client_name': 'Gardenia Indoor Plants',
                'project_date': date(2024, 8, 15),
                'tags': 'branding, logo design, nature, plants',
                'is_featured': True,
                'challenge': 'Create a fresh, natural brand identity that appeals to urban plant enthusiasts',
                'solution': 'Developed a clean, modern logo with natural green tones and botanical elements',
                'results': 'Increased brand recognition by 150% and improved customer engagement'
            },
            {
                'title': 'Miracle Paws - Pet Care Branding',
                'description': 'Complete branding solution for pet care services including logo design, stationery, and merchandise.',
                'service_id': service_objects[0].id,  # Logo Design
                'image_url': '/static/images/Miracle-pows-project/1-miracle-main.png',
                'client_name': 'Miracle Paws',
                'project_date': date(2024, 7, 20),
                'tags': 'pets, veterinary, branding, logo',
                'is_featured': True,
                'challenge': 'Design a trustworthy brand for pet care that appeals to pet owners',
                'solution': 'Created a warm, friendly brand with paw imagery and caring typography',
                'results': 'Enhanced customer trust and improved appointment bookings by 80%'
            },
            # Social Media Portfolio
            {
                'title': 'Festival Social Media Campaign',
                'description': 'Creative social media posts for various Indian festivals including Diwali, Ganesh Chaturthi, and Independence Day.',
                'service_id': service_objects[1].id,  # Social Media Design
                'image_url': '/static/images/social-media-post/diwali.jpg',
                'client_name': 'Various Clients',
                'project_date': date(2024, 10, 15),
                'tags': 'festivals, social media, indian culture, celebrations',
                'is_featured': True
            },
            {
                'title': 'Friendship Day Social Campaign',
                'description': 'Engaging social media graphics for Friendship Day celebration with vibrant colors and modern design.',
                'service_id': service_objects[1].id,  # Social Media Design
                'image_url': '/static/images/social-media-post/friendship day.jpg',
                'client_name': 'Social Media Clients',
                'project_date': date(2024, 8, 1),
                'tags': 'friendship day, social media, celebration, youth',
                'is_featured': False
            },
            # Flyer Design Portfolio
            {
                'title': 'Malabar Restaurant Promotion',
                'description': 'Attractive promotional flyer design for Malabar restaurant featuring authentic Kerala cuisine.',
                'service_id': service_objects[2].id,  # Flyer Design
                'image_url': '/static/images/flyer-design/1-malabar.jpg',
                'client_name': 'Malabar Restaurant',
                'project_date': date(2024, 6, 10),
                'tags': 'restaurant, food, kerala, promotion',
                'is_featured': True
            },
            {
                'title': 'Kerala Tour Package',
                'description': 'Beautiful travel flyer design showcasing Kerala tourism with stunning visuals.',
                'service_id': service_objects[2].id,  # Flyer Design
                'image_url': '/static/images/flyer-design/2-kerala-tour.jpg',
                'client_name': 'Travel Agency',
                'project_date': date(2024, 5, 25),
                'tags': 'travel, kerala, tourism, backwaters',
                'is_featured': True
            },
            {
                'title': 'CakeVilla Bakery Promotion',
                'description': 'Delicious cake promotion flyer with mouth-watering visuals and attractive offers.',
                'service_id': service_objects[2].id,  # Flyer Design
                'image_url': '/static/images/flyer-design/3-cakevilla.png',
                'client_name': 'CakeVilla Bakery',
                'project_date': date(2024, 4, 12),
                'tags': 'bakery, cakes, sweets, promotion',
                'is_featured': False
            },
            # Packaging Design Portfolio
            {
                'title': 'Suhana Biryani Masala Packaging',
                'description': 'Premium spice packaging design with authentic Indian aesthetics and clear product information.',
                'service_id': service_objects[4].id,  # Packaging Design
                'image_url': '/static/images/packaging/1-suhana-biryani-masala.png',
                'client_name': 'Suhana Spices',
                'project_date': date(2024, 3, 8),
                'tags': 'spices, packaging, food, indian',
                'is_featured': True
            },
            {
                'title': 'Haldiram Namkeen Package',
                'description': 'Traditional snack packaging design maintaining brand heritage with modern appeal.',
                'service_id': service_objects[4].id,  # Packaging Design
                'image_url': '/static/images/packaging/2-Haldiram-namkeep.png',
                'client_name': 'Haldiram',
                'project_date': date(2024, 2, 14),
                'tags': 'snacks, traditional, packaging, namkeen',
                'is_featured': False
            },
            # Invitation Cards Portfolio
            {
                'title': 'Elegant Wedding Invitation',
                'description': 'Beautiful wedding invitation card with traditional Indian motifs and modern typography.',
                'service_id': service_objects[5].id,  # Invitation Cards
                'image_url': '/static/images/invitation-card-design/engagement-card-1.jpg',
                'client_name': 'Wedding Client',
                'project_date': date(2024, 1, 20),
                'tags': 'wedding, invitation, traditional, elegant',
                'is_featured': True
            },
            {
                'title': 'Corporate Event Invitation',
                'description': 'Professional corporate event invitation with clean design and company branding.',
                'service_id': service_objects[5].id,  # Invitation Cards
                'image_url': '/static/images/invitation-card-design/hotel-thalikatta.jpg',
                'client_name': 'Corporate Client',
                'project_date': date(2024, 9, 5),
                'tags': 'corporate, event, professional, business',
                'is_featured': False
            }
        ]

        for item_data in portfolio_items:
            portfolio_item = Portfolio(**item_data)
            db.session.add(portfolio_item)

        db.session.commit()
        print(f"Created {len(portfolio_items)} portfolio items")

        # Create testimonials
        print("Creating testimonials...")
        testimonials = [
            {
                'client_name': 'Rajesh Sharma',
                'company': 'Gardenia Indoor Plants',
                'testimonial_text': 'OrbitX delivered an exceptional brand identity for our plant business. Their creative approach and attention to detail helped us stand out in the market. Highly recommended!',
                'rating': 5,
                'project_type': 'Logo Design & Branding',
                'is_featured': True
            },
            {
                'client_name': 'Priya Menon',
                'company': 'CakeVilla Bakery',
                'testimonial_text': 'The flyer designs created by OrbitX were absolutely stunning! They perfectly captured our brand essence and helped increase our sales significantly.',
                'rating': 5,
                'project_type': 'Flyer Design',
                'is_featured': True
            },
            {
                'client_name': 'Amit Patel',
                'company': 'Tech Solutions Pvt Ltd',
                'testimonial_text': 'Professional, creative, and timely delivery. OrbitX created beautiful presentation designs that impressed our clients and helped us win new business.',
                'rating': 4,
                'project_type': 'PowerPoint Presentations',
                'is_featured': True
            },
            {
                'client_name': 'Sneha Reddy',
                'company': 'Fashion Boutique',
                'testimonial_text': 'Amazing social media designs! OrbitX understood our brand perfectly and created content that significantly boosted our online engagement.',
                'rating': 5,
                'project_type': 'Social Media Design',
                'is_featured': False
            },
            {
                'client_name': 'Dr. Vikram Singh',
                'company': 'Miracle Paws Veterinary',
                'testimonial_text': 'The complete branding solution provided by OrbitX was beyond our expectations. Our clinic now has a professional and trustworthy image.',
                'rating': 5,
                'project_type': 'Logo Design & Branding',
                'is_featured': False
            }
        ]

        for testimonial_data in testimonials:
            testimonial = Testimonial(**testimonial_data)
            db.session.add(testimonial)

        db.session.commit()
        print(f"Created {len(testimonials)} testimonials")

        print("Database population completed successfully!")
        print(f"Total items created:")
        print(f"   - {len(services)} Services")
        print(f"   - {len(portfolio_items)} Portfolio Items")
        print(f"   - {len(testimonials)} Testimonials")

if __name__ == '__main__':
    populate_all_data()