"""
MongoDB Data Population Script for OrbitX Digital Marketing Website

This script populates the MongoDB database with comprehensive sample data.
"""

from datetime import datetime, date

def populate_mongodb_data(db_models):
    """Populate MongoDB with comprehensive website data"""

    print("Creating services...")

    # Create services
    services_data = [
        {
            'name': 'Logo Design',
            'description': 'Professional logo design services that capture your brand essence and create memorable visual identity.',
            'short_description': 'Create memorable brand identity with professional logo design',
            'icon_class': 'fas fa-palette',
            'price_range': '₹2,000 - ₹15,000',
            'is_active': True
        },
        {
            'name': 'Website Design & Development',
            'description': 'Modern, responsive website development using latest technologies. From concept to deployment.',
            'short_description': 'Modern responsive websites built with latest technologies',
            'icon_class': 'fas fa-laptop-code',
            'price_range': '₹10,000 - ₹50,000',
            'is_active': True
        },
        {
            'name': 'Social Media Design',
            'description': 'Eye-catching social media graphics, posts, and campaigns for all major platforms.',
            'short_description': 'Engaging social media graphics and campaign designs',
            'icon_class': 'fas fa-share-alt',
            'price_range': '₹5,000 - ₹20,000',
            'is_active': True
        },
        {
            'name': 'Digital Marketing',
            'description': 'Comprehensive digital marketing strategies including SEO, PPC, and content marketing.',
            'short_description': 'Complete digital marketing solutions for business growth',
            'icon_class': 'fas fa-chart-line',
            'price_range': '₹15,000 - ₹75,000',
            'is_active': True
        },
        {
            'name': 'Brand Identity Design',
            'description': 'Complete brand identity packages including logos, color schemes, typography, and brand guidelines.',
            'short_description': 'Complete brand identity packages with guidelines',
            'icon_class': 'fas fa-eye',
            'price_range': '₹25,000 - ₹100,000',
            'is_active': True
        },
        {
            'name': 'E-commerce Solutions',
            'description': 'Custom e-commerce websites and online stores with payment integration and inventory management.',
            'short_description': 'Custom e-commerce solutions with payment integration',
            'icon_class': 'fas fa-shopping-cart',
            'price_range': '₹30,000 - ₹150,000',
            'is_active': True
        }
    ]

    service_ids = []
    for service_data in services_data:
        service_id = db_models.services.create_service(**service_data)
        service_ids.append(service_id)
        print(f"Created service: {service_data['name']}")

    print("Creating testimonials...")

    # Create testimonials
    testimonials_data = [
        {
            'client_name': 'Rajesh Kumar',
            'company': 'TechStart India',
            'testimonial_text': 'OrbitX delivered an exceptional website that perfectly captured our vision. The team was professional, responsive, and delivered on time. Highly recommended!',
            'rating': 5,
            'project_type': 'Website Development',
            'is_featured': True
        },
        {
            'client_name': 'Priya Sharma',
            'company': 'Fashion Forward',
            'testimonial_text': 'The logo design exceeded our expectations. OrbitX understood our brand personality and created a memorable visual identity.',
            'rating': 5,
            'project_type': 'Logo Design',
            'is_featured': True
        },
        {
            'client_name': 'Amit Patel',
            'company': 'Digital Solutions Ltd',
            'testimonial_text': 'Outstanding digital marketing campaign! Our online presence increased by 300% within 3 months. Great ROI!',
            'rating': 5,
            'project_type': 'Digital Marketing',
            'is_featured': True
        }
    ]

    for testimonial_data in testimonials_data:
        db_models.testimonials.create_testimonial(**testimonial_data)
        print(f"Created testimonial from: {testimonial_data['client_name']}")

    print("Creating portfolio items...")

    # Create portfolio items
    portfolio_data = [
        {
            'title': 'TechStart India Website',
            'description': 'Modern corporate website with responsive design and advanced features.',
            'service_id': service_ids[1],  # Website Design
            'client_name': 'TechStart India',
            'project_date': date(2024, 8, 15),
            'tags': 'web design, responsive, corporate',
            'is_featured': True,
            'challenge': 'Create a modern website that showcases technology services while maintaining professional credibility.',
            'solution': 'Developed a clean, modern design with interactive elements and mobile-first approach.',
            'results': 'Increased online inquiries by 150% and improved user engagement by 200%.'
        },
        {
            'title': 'Fashion Forward Logo',
            'description': 'Elegant logo design for fashion retail brand with modern aesthetics.',
            'service_id': service_ids[0],  # Logo Design
            'client_name': 'Fashion Forward',
            'project_date': date(2024, 7, 10),
            'tags': 'logo, fashion, elegant',
            'is_featured': True,
            'challenge': 'Design a logo that appeals to young fashion-conscious consumers while maintaining elegance.',
            'solution': 'Created a minimalist logo with contemporary typography and subtle fashion elements.',
            'results': 'Brand recognition increased by 80% and social media engagement improved significantly.'
        },
        {
            'title': 'Digital Solutions Marketing Campaign',
            'description': 'Comprehensive digital marketing campaign with SEO and social media strategy.',
            'service_id': service_ids[3],  # Digital Marketing
            'client_name': 'Digital Solutions Ltd',
            'project_date': date(2024, 6, 5),
            'tags': 'digital marketing, SEO, social media',
            'is_featured': True,
            'challenge': 'Increase online visibility and generate quality leads for B2B technology services.',
            'solution': 'Implemented multi-channel digital strategy with targeted content and SEO optimization.',
            'results': 'Generated 300% more qualified leads and improved search rankings for key terms.'
        },
        {
            'title': 'Restaurant Chain Branding',
            'description': 'Complete brand identity for growing restaurant chain.',
            'service_id': service_ids[4],  # Brand Identity
            'client_name': 'Spice Route Restaurants',
            'project_date': date(2024, 9, 1),
            'tags': 'branding, restaurant, identity',
            'is_featured': True
        },
        {
            'title': 'Online Store Development',
            'description': 'Custom e-commerce platform with inventory management.',
            'service_id': service_ids[5],  # E-commerce
            'client_name': 'Craftsman Market',
            'project_date': date(2024, 8, 20),
            'tags': 'e-commerce, online store, shopping',
            'is_featured': True
        },
        {
            'title': 'Social Media Campaign',
            'description': 'Engaging social media graphics and campaign strategy.',
            'service_id': service_ids[2],  # Social Media
            'client_name': 'Fitness First Gym',
            'project_date': date(2024, 7, 25),
            'tags': 'social media, fitness, graphics',
            'is_featured': False
        }
    ]

    for portfolio_item in portfolio_data:
        db_models.portfolio.create_portfolio_item(**portfolio_item)
        print(f"Created portfolio item: {portfolio_item['title']}")

    print("Creating blog posts...")

    # Create blog posts
    blog_posts_data = [
        {
            'title': '10 Essential Web Design Trends for 2024',
            'slug': 'web-design-trends-2024',
            'content': '''Web design continues to evolve rapidly, and staying current with trends is crucial for creating engaging user experiences. Here are the top 10 trends shaping web design in 2024:

1. **Dark Mode Designs**: Dark themes reduce eye strain and save battery life on mobile devices.

2. **Minimalist Layouts**: Clean, uncluttered designs that focus on essential content and functionality.

3. **Micro-Interactions**: Small animations that provide feedback and enhance user engagement.

4. **Voice User Interface**: Integration of voice commands and audio interactions.

5. **3D Elements**: Three-dimensional graphics and interactions for immersive experiences.

6. **Sustainable Design**: Eco-friendly design practices that reduce carbon footprint.

7. **Inclusive Design**: Accessibility-first approach ensuring usability for all users.

8. **AI-Powered Personalization**: Dynamic content adaptation based on user behavior.

9. **Augmented Reality**: AR integration for interactive product demonstrations.

10. **Advanced Typography**: Creative use of fonts and text layouts for visual impact.

Stay ahead of the curve by incorporating these trends thoughtfully into your web projects.''',
            'excerpt': 'Discover the top 10 web design trends that will dominate 2024 and learn how to implement them effectively.',
            'author': 'OrbitX Design Team',
            'is_published': True,
            'tags': 'web design, trends, 2024, UI/UX'
        },
        {
            'title': 'The Ultimate Guide to Logo Design',
            'slug': 'ultimate-logo-design-guide',
            'content': '''Creating a memorable logo is one of the most important investments for any business. A well-designed logo serves as the cornerstone of your brand identity and can significantly impact customer perception.

## What Makes a Great Logo?

**Simplicity**: The best logos are simple and easily recognizable. Think of Apple, Nike, or McDonald's.

**Memorability**: A great logo sticks in people's minds long after they've seen it.

**Timelessness**: Avoid trendy elements that will quickly become outdated.

**Versatility**: Your logo should work across all media and applications.

**Appropriateness**: The design should reflect your industry and target audience.

## The Logo Design Process

1. **Research**: Understand the brand, industry, and competition
2. **Ideation**: Brainstorm concepts and sketch initial ideas
3. **Design**: Create digital versions of promising concepts
4. **Refinement**: Polish and perfect the chosen direction
5. **Testing**: Ensure the logo works in various contexts
6. **Delivery**: Provide final files in all necessary formats

## Common Logo Design Mistakes

- Making it too complex
- Using too many colors
- Following trends blindly
- Not considering scalability
- Ignoring the target audience

Remember, a logo is not just a pretty picture – it's a strategic business tool that should communicate your brand's essence at a glance.''',
            'excerpt': 'Learn the fundamental principles of effective logo design and discover the step-by-step process for creating memorable brand identities.',
            'author': 'OrbitX Design Team',
            'is_published': True,
            'tags': 'logo design, branding, identity, design process'
        }
    ]

    for blog_post in blog_posts_data:
        db_models.blog_posts.create_post(**blog_post)
        print(f"Created blog post: {blog_post['title']}")

    print("Sample data population completed successfully!")
    print(f"Created {len(services_data)} services")
    print(f"Created {len(testimonials_data)} testimonials")
    print(f"Created {len(portfolio_data)} portfolio items")
    print(f"Created {len(blog_posts_data)} blog posts")

    return True

if __name__ == "__main__":
    print("This script should be imported and run within the Flask app context.")