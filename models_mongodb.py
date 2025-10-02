"""
MongoDB Models for OrbitX Digital Marketing Website

This file replaces the SQLAlchemy models with MongoDB document structure.
Using PyMongo for database operations.
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from bson import ObjectId
import json

class MongoModel:
    """Base class for MongoDB document models"""

    def __init__(self, collection_name: str, mongo_db):
        self.collection_name = collection_name
        self.collection = mongo_db[collection_name]

    def insert_one(self, document: dict) -> str:
        """Insert a single document and return the ID"""
        if 'created_at' not in document:
            document['created_at'] = datetime.utcnow()

        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def find_one(self, filter_dict: dict) -> Optional[dict]:
        """Find a single document"""
        if '_id' in filter_dict and isinstance(filter_dict['_id'], str):
            filter_dict['_id'] = ObjectId(filter_dict['_id'])

        doc = self.collection.find_one(filter_dict)
        if doc:
            doc['id'] = str(doc['_id'])
        return doc

    def find(self, filter_dict: dict = None, limit: int = None, sort_by: str = None, sort_order: int = -1) -> List[dict]:
        """Find multiple documents"""
        if filter_dict is None:
            filter_dict = {}

        cursor = self.collection.find(filter_dict)

        if sort_by:
            cursor = cursor.sort(sort_by, sort_order)

        if limit:
            cursor = cursor.limit(limit)

        documents = []
        for doc in cursor:
            doc['id'] = str(doc['_id'])
            documents.append(doc)

        return documents

    def update_one(self, filter_dict: dict, update_dict: dict) -> bool:
        """Update a single document"""
        if '_id' in filter_dict and isinstance(filter_dict['_id'], str):
            filter_dict['_id'] = ObjectId(filter_dict['_id'])

        update_dict['updated_at'] = datetime.utcnow()
        result = self.collection.update_one(filter_dict, {'$set': update_dict})
        return result.modified_count > 0

    def delete_one(self, filter_dict: dict) -> bool:
        """Delete a single document"""
        if '_id' in filter_dict and isinstance(filter_dict['_id'], str):
            filter_dict['_id'] = ObjectId(filter_dict['_id'])

        result = self.collection.delete_one(filter_dict)
        return result.deleted_count > 0

    def count_documents(self, filter_dict: dict = None) -> int:
        """Count documents matching filter"""
        if filter_dict is None:
            filter_dict = {}
        return self.collection.count_documents(filter_dict)

class ServiceModel(MongoModel):
    """Service model for MongoDB"""

    def __init__(self, mongo_db):
        super().__init__('services', mongo_db)

    def create_service(self, name: str, description: str, short_description: str = None,
                      icon_class: str = None, price_range: str = None, is_active: bool = True) -> str:
        """Create a new service"""
        service_doc = {
            'name': name,
            'description': description,
            'short_description': short_description,
            'icon_class': icon_class,
            'price_range': price_range,
            'is_active': is_active,
            'created_at': datetime.utcnow()
        }
        return self.insert_one(service_doc)

    def get_active_services(self, limit: int = None) -> List[dict]:
        """Get all active services"""
        return self.find({'is_active': True}, limit=limit)

    def get_by_id(self, service_id: str) -> Optional[dict]:
        """Get service by ID"""
        return self.find_one({'_id': service_id})

class ContactInquiryModel(MongoModel):
    """Contact Inquiry model for MongoDB"""

    def __init__(self, mongo_db):
        super().__init__('contact_inquiries', mongo_db)

    def create_inquiry(self, name: str, email: str, message: str, phone: str = None,
                      service_interested: str = None, status: str = 'new') -> str:
        """Create a new contact inquiry"""
        inquiry_doc = {
            'name': name,
            'email': email,
            'phone': phone,
            'service_interested': service_interested,
            'message': message,
            'status': status,
            'created_at': datetime.utcnow()
        }
        return self.insert_one(inquiry_doc)

class QuoteRequestModel(MongoModel):
    """Quote Request model for MongoDB"""

    def __init__(self, mongo_db):
        super().__init__('quote_requests', mongo_db)

    def create_quote_request(self, client_name: str, email: str, project_description: str,
                           phone: str = None, company_name: str = None, services_requested: str = None,
                           budget_range: str = None, timeline: str = None,
                           additional_requirements: str = None, status: str = 'pending') -> str:
        """Create a new quote request"""
        quote_doc = {
            'client_name': client_name,
            'email': email,
            'phone': phone,
            'company_name': company_name,
            'services_requested': services_requested,
            'project_description': project_description,
            'budget_range': budget_range,
            'timeline': timeline,
            'additional_requirements': additional_requirements,
            'status': status,
            'created_at': datetime.utcnow()
        }
        return self.insert_one(quote_doc)

    def get_by_id(self, quote_id: str) -> Optional[dict]:
        """Get quote request by ID"""
        return self.find_one({'_id': quote_id})

class TestimonialModel(MongoModel):
    """Testimonial model for MongoDB"""

    def __init__(self, mongo_db):
        super().__init__('testimonials', mongo_db)

    def create_testimonial(self, client_name: str, testimonial_text: str, company: str = None,
                          rating: int = None, project_type: str = None, client_image_url: str = None,
                          is_featured: bool = False) -> str:
        """Create a new testimonial"""
        testimonial_doc = {
            'client_name': client_name,
            'company': company,
            'testimonial_text': testimonial_text,
            'rating': rating,
            'project_type': project_type,
            'client_image_url': client_image_url,
            'is_featured': is_featured,
            'created_at': datetime.utcnow()
        }
        return self.insert_one(testimonial_doc)

    def get_featured(self, limit: int = None) -> List[dict]:
        """Get featured testimonials"""
        return self.find({'is_featured': True}, limit=limit)

class BlogPostModel(MongoModel):
    """Blog Post model for MongoDB"""

    def __init__(self, mongo_db):
        super().__init__('blog_posts', mongo_db)

    def create_post(self, title: str, slug: str, content: str, excerpt: str = None,
                   featured_image_url: str = None, author: str = None, is_published: bool = False,
                   tags: str = None) -> str:
        """Create a new blog post"""
        post_doc = {
            'title': title,
            'slug': slug,
            'content': content,
            'excerpt': excerpt,
            'featured_image_url': featured_image_url,
            'author': author,
            'is_published': is_published,
            'tags': tags,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return self.insert_one(post_doc)

    def get_published(self, limit: int = None) -> List[dict]:
        """Get published blog posts"""
        return self.find({'is_published': True}, limit=limit, sort_by='created_at', sort_order=-1)

    def get_by_slug(self, slug: str) -> Optional[dict]:
        """Get blog post by slug"""
        return self.find_one({'slug': slug, 'is_published': True})

class PortfolioModel(MongoModel):
    """Portfolio model for MongoDB"""

    def __init__(self, mongo_db):
        super().__init__('portfolio', mongo_db)

    def create_portfolio_item(self, title: str, service_id: str, description: str = None,
                            image_url: str = None, client_name: str = None, project_date: date = None,
                            tags: str = None, is_featured: bool = False, challenge: str = None,
                            solution: str = None, results: str = None, client_testimonial: str = None,
                            before_image_url: str = None, after_image_url: str = None) -> str:
        """Create a new portfolio item"""
        portfolio_doc = {
            'title': title,
            'description': description,
            'service_id': service_id,
            'image_url': image_url,
            'client_name': client_name,
            'project_date': project_date.isoformat() if project_date else None,
            'tags': tags,
            'is_featured': is_featured,
            'challenge': challenge,
            'solution': solution,
            'results': results,
            'client_testimonial': client_testimonial,
            'before_image_url': before_image_url,
            'after_image_url': after_image_url,
            'created_at': datetime.utcnow()
        }
        return self.insert_one(portfolio_doc)

    def get_featured(self, limit: int = None) -> List[dict]:
        """Get featured portfolio items"""
        return self.find({'is_featured': True}, limit=limit)

    def get_by_service(self, service_id: str, limit: int = None) -> List[dict]:
        """Get portfolio items by service"""
        return self.find({'service_id': service_id}, limit=limit)

    def get_case_studies(self) -> List[dict]:
        """Get portfolio items that have case study data"""
        return self.find({
            'challenge': {'$ne': None, '$exists': True},
            'solution': {'$ne': None, '$exists': True}
        })

    def get_tags_list(self, portfolio_item: dict) -> List[str]:
        """Get tags as a list from a portfolio item"""
        if portfolio_item.get('tags'):
            return [tag.strip() for tag in portfolio_item['tags'].split(',')]
        return []

class ChatConversationModel(MongoModel):
    """Chat Conversation model for MongoDB"""

    def __init__(self, mongo_db):
        super().__init__('chat_conversations', mongo_db)

    def create_conversation(self, conversation_id: str, user_session_id: str = None,
                          user_name: str = None, user_email: str = None, user_phone: str = None,
                          status: str = 'active', context_data: str = None,
                          quote_request_id: str = None) -> str:
        """Create a new chat conversation"""
        conversation_doc = {
            '_id': conversation_id,  # Use provided conversation_id as _id
            'user_session_id': user_session_id,
            'user_name': user_name,
            'user_email': user_email,
            'user_phone': user_phone,
            'status': status,
            'context_data': context_data,
            'quote_request_id': quote_request_id,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        # For conversations, we manage the _id manually
        result = self.collection.insert_one(conversation_doc)
        return conversation_id

class ChatMessageModel(MongoModel):
    """Chat Message model for MongoDB"""

    def __init__(self, mongo_db):
        super().__init__('chat_messages', mongo_db)

    def create_message(self, conversation_id: str, sender: str, message: str,
                      message_type: str = 'text', message_metadata: str = None) -> str:
        """Create a new chat message"""
        message_doc = {
            'conversation_id': conversation_id,
            'sender': sender,
            'message': message,
            'message_type': message_type,
            'message_metadata': message_metadata,
            'created_at': datetime.utcnow()
        }
        return self.insert_one(message_doc)

    def get_by_conversation(self, conversation_id: str, limit: int = None) -> List[dict]:
        """Get messages by conversation ID"""
        return self.find({'conversation_id': conversation_id}, limit=limit,
                        sort_by='created_at', sort_order=1)  # Ascending for chat history

# Database Models Manager
class DatabaseModels:
    """Manager class for all MongoDB models"""

    def __init__(self, mongo_db):
        self.mongo_db = mongo_db

        # Initialize all models
        self.services = ServiceModel(mongo_db)
        self.contact_inquiries = ContactInquiryModel(mongo_db)
        self.quote_requests = QuoteRequestModel(mongo_db)
        self.testimonials = TestimonialModel(mongo_db)
        self.blog_posts = BlogPostModel(mongo_db)
        self.portfolio = PortfolioModel(mongo_db)
        self.chat_conversations = ChatConversationModel(mongo_db)
        self.chat_messages = ChatMessageModel(mongo_db)

    def get_service_by_id(self, service_id: str) -> Optional[dict]:
        """Get service by ID - compatibility method"""
        return self.services.get_by_id(service_id)

    def create_indexes(self):
        """Create necessary indexes for better performance"""
        try:
            # Services indexes
            self.services.collection.create_index([("name", 1)])
            self.services.collection.create_index([("is_active", 1)])

            # Contact inquiries indexes
            self.contact_inquiries.collection.create_index([("email", 1)])
            self.contact_inquiries.collection.create_index([("status", 1)])
            self.contact_inquiries.collection.create_index([("created_at", -1)])

            # Quote requests indexes
            self.quote_requests.collection.create_index([("email", 1)])
            self.quote_requests.collection.create_index([("status", 1)])
            self.quote_requests.collection.create_index([("created_at", -1)])

            # Blog posts indexes
            self.blog_posts.collection.create_index([("slug", 1)], unique=True)
            self.blog_posts.collection.create_index([("is_published", 1)])
            self.blog_posts.collection.create_index([("created_at", -1)])

            # Portfolio indexes
            self.portfolio.collection.create_index([("service_id", 1)])
            self.portfolio.collection.create_index([("is_featured", 1)])

            # Chat indexes
            self.chat_conversations.collection.create_index([("user_session_id", 1)])
            self.chat_messages.collection.create_index([("conversation_id", 1)])
            self.chat_messages.collection.create_index([("created_at", 1)])

            print("MongoDB indexes created successfully!")

        except Exception as e:
            print(f"Error creating indexes: {e}")