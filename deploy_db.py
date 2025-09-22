#!/usr/bin/env python3
"""
Production database setup script for Render deployment
"""

import os
from app import app, db
from models import *

def create_all_tables():
    """Create all database tables for production"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ All database tables created successfully!")

            # Check if tables exist
            tables = db.engine.table_names()
            print(f"📊 Created tables: {', '.join(tables)}")

            # Create initial data if needed
            create_initial_services()

            print("🚀 Database setup complete for production!")

        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False

        return True

def create_initial_services():
    """Create initial service data"""
    try:
        # Check if services already exist
        if Service.query.first():
            print("📋 Services already exist, skipping initial data creation")
            return

        # Create initial services
        services = [
            {
                'name': 'Logo Design',
                'description': 'Professional logo design and branding services',
                'short_description': 'Custom logo design with unlimited revisions',
                'icon_class': 'fas fa-palette',
                'price_range': '₹2,000 - ₹15,000'
            },
            {
                'name': 'Website Design',
                'description': 'Responsive website design and development',
                'short_description': 'Modern, mobile-friendly websites',
                'icon_class': 'fas fa-laptop-code',
                'price_range': '₹10,000 - ₹50,000'
            },
            {
                'name': 'Social Media Design',
                'description': 'Social media graphics and content creation',
                'short_description': 'Engaging social media visuals',
                'icon_class': 'fas fa-share-alt',
                'price_range': '₹5,000 - ₹20,000'
            },
            {
                'name': 'Print Design',
                'description': 'Flyers, brochures, and print marketing materials',
                'short_description': 'Professional print design services',
                'icon_class': 'fas fa-print',
                'price_range': '₹3,000 - ₹25,000'
            }
        ]

        for service_data in services:
            service = Service(**service_data)
            db.session.add(service)

        db.session.commit()
        print(f"✅ Created {len(services)} initial services")

    except Exception as e:
        print(f"⚠️ Error creating initial services: {e}")
        db.session.rollback()

if __name__ == '__main__':
    # Set production environment
    os.environ['FLASK_ENV'] = 'production'
    create_all_tables()