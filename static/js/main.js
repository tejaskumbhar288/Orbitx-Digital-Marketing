/**
 * Main JavaScript file for Sarvesh Kumbhar Design Website
 * Contains all interactive features and functionality
 */

// ===== GLOBAL VARIABLES =====
let currentScrollY = 0;
let ticking = false;

// ===== DOM CONTENT LOADED =====
document.addEventListener('DOMContentLoaded', function() {
    initializeAOS();
    initializeNavbar();
    initializeBackToTop();
    initializeLazyLoading();
    initializeFormValidation();
    initializePortfolioFilters();
    initializeScrollEffects();
    initializeInteractiveElements();
    initializeTypingAnimation();
    initializeCounterAnimation();
});

// ===== AOS ANIMATION INITIALIZATION =====
function initializeAOS() {
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            offset: 100,
            delay: 100
        });
    }
}

// ===== NAVBAR FUNCTIONALITY =====
function initializeNavbar() {
    const navbar = document.getElementById('mainNavbar');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (!navbar) return;
    
    // Handle scroll effects
    function handleScroll() {
        const scrolled = window.scrollY > 50;
        navbar.classList.toggle('scrolled', scrolled);
    }
    
    // Initial check
    handleScroll();
    
    // Throttled scroll listener
    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(function() {
                handleScroll();
                ticking = false;
            });
            ticking = true;
        }
    });
    
    // Close navbar on mobile when clicking links
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992) {
                navbarCollapse.classList.remove('show');
            }
        });
    });
    
    // Smooth scroll for anchor links
    navLinks.forEach(link => {
        if (link.getAttribute('href').startsWith('#')) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    const offsetTop = target.offsetTop - 80;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        }
    });
}

// ===== BACK TO TOP BUTTON =====
function initializeBackToTop() {
    const backToTopBtn = document.getElementById('backToTop');
    
    if (!backToTopBtn) return;
    
    function toggleBackToTop() {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    }
    
    // Initial check
    toggleBackToTop();
    
    // Scroll listener
    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(function() {
                toggleBackToTop();
                ticking = false;
            });
            ticking = true;
        }
    });
    
    // Click handler
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ===== LAZY LOADING =====
function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    
                    img.classList.remove('lazy');
                    img.classList.add('lazy-loaded');
                    
                    // Add fade-in effect
                    img.style.opacity = '0';
                    img.style.transition = 'opacity 0.3s ease';
                    
                    img.onload = function() {
                        img.style.opacity = '1';
                    };
                    
                    imageObserver.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px 0px',
            threshold: 0.1
        });
        
        // Observe all lazy images
        document.querySelectorAll('img[data-src], img.lazy').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// ===== FORM VALIDATION =====
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[data-validate="true"], .contact-form, .quote-form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            // Real-time validation
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });
        
        // Form submission validation
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                const firstInvalid = form.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstInvalid.focus();
                }
            } else {
                // Show loading state
                const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
                if (submitBtn) {
                    const originalText = submitBtn.innerHTML || submitBtn.value;
                    submitBtn.disabled = true;
                    
                    if (submitBtn.tagName === 'BUTTON') {
                        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
                    }
                    
                    // Reset after 3 seconds if form wasn't actually submitted
                    setTimeout(() => {
                        if (submitBtn.disabled) {
                            submitBtn.disabled = false;
                            submitBtn.innerHTML = originalText;
                        }
                    }, 3000);
                }
            }
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const required = field.hasAttribute('required');
    
    // Remove existing validation classes
    field.classList.remove('is-valid', 'is-invalid');
    
    // Check if field is required and empty
    if (required && !value) {
        field.classList.add('is-invalid');
        setFieldError(field, 'This field is required');
        return false;
    }
    
    // Validate email
    if (type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            field.classList.add('is-invalid');
            setFieldError(field, 'Please enter a valid email address');
            return false;
        }
    }
    
    // Validate phone
    if ((field.name === 'phone' || type === 'tel') && value) {
        const phoneRegex = /^[\d\s\+\-\(\)]+$/;
        if (!phoneRegex.test(value) || value.length < 10) {
            field.classList.add('is-invalid');
            setFieldError(field, 'Please enter a valid phone number');
            return false;
        }
    }
    
    // Validate text length
    if (field.minLength && value.length < field.minLength && value.length > 0) {
        field.classList.add('is-invalid');
        setFieldError(field, `Minimum ${field.minLength} characters required`);
        return false;
    }
    
    if (field.maxLength && value.length > field.maxLength) {
        field.classList.add('is-invalid');
        setFieldError(field, `Maximum ${field.maxLength} characters allowed`);
        return false;
    }
    
    // If we get here, field is valid
    if (value) {
        field.classList.add('is-valid');
        clearFieldError(field);
    }
    
    return true;
}

function setFieldError(field, message) {
    clearFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    errorDiv.dataset.fieldError = 'true';
    
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    const existingError = field.parentNode.querySelector('.invalid-feedback[data-field-error="true"]');
    if (existingError) {
        existingError.remove();
    }
}

// ===== PORTFOLIO FILTERS =====
function initializePortfolioFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    const searchInput = document.getElementById('portfolioSearch');
    
    if (!filterButtons.length) return;
    
    // Filter functionality
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.dataset.filter;
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filter items
            portfolioItems.forEach(item => {
                const shouldShow = filter === '*' || item.classList.contains(filter.substring(1));
                
                if (shouldShow) {
                    item.style.display = 'block';
                    item.classList.add('aos-animate');
                } else {
                    item.style.display = 'none';
                }
            });
            
            // Trigger layout recalculation
            setTimeout(() => {
                if (typeof AOS !== 'undefined') {
                    AOS.refresh();
                }
            }, 100);
        });
    });
    
    // Search functionality
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                portfolioItems.forEach(item => {
                    const title = item.querySelector('.portfolio-title')?.textContent.toLowerCase() || '';
                    const client = item.querySelector('.portfolio-client')?.textContent.toLowerCase() || '';
                    const category = item.querySelector('.portfolio-category')?.textContent.toLowerCase() || '';
                    const tags = Array.from(item.querySelectorAll('.tag')).map(tag => tag.textContent.toLowerCase()).join(' ');
                    
                    const searchableText = `${title} ${client} ${category} ${tags}`;
                    const shouldShow = searchableText.includes(searchTerm);
                    
                    if (shouldShow) {
                        item.style.display = 'block';
                        item.classList.add('aos-animate');
                    } else {
                        item.style.display = 'none';
                    }
                });
            }, 300);
        });
    }
}

// ===== SCROLL EFFECTS =====
function initializeScrollEffects() {
    // Parallax effect for hero backgrounds
    const heroSections = document.querySelectorAll('.hero-section, .page-hero');
    
    if (heroSections.length) {
        window.addEventListener('scroll', function() {
            if (!ticking) {
                requestAnimationFrame(function() {
                    const scrolled = window.scrollY;
                    
                    heroSections.forEach(hero => {
                        const rate = scrolled * -0.5;
                        hero.style.transform = `translateY(${rate}px)`;
                    });
                    
                    ticking = false;
                });
                ticking = true;
            }
        });
    }
    
    // Fade in elements on scroll
    const fadeElements = document.querySelectorAll('.fade-on-scroll');
    
    if (fadeElements.length && 'IntersectionObserver' in window) {
        const fadeObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('faded-in');
                    fadeObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        fadeElements.forEach(element => {
            fadeObserver.observe(element);
        });
    }
}

// ===== INTERACTIVE ELEMENTS =====
function initializeInteractiveElements() {
    // Tooltip initialization
    const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipElements.length && typeof bootstrap !== 'undefined') {
        tooltipElements.forEach(element => {
            new bootstrap.Tooltip(element);
        });
    }
    
    // Accordion enhancements
    const accordions = document.querySelectorAll('.accordion');
    accordions.forEach(accordion => {
        const buttons = accordion.querySelectorAll('.accordion-button');
        
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                const isExpanded = this.getAttribute('aria-expanded') === 'true';
                
                // Add smooth icon rotation
                const icon = this.querySelector('i');
                if (icon) {
                    icon.style.transform = isExpanded ? 'rotate(0deg)' : 'rotate(180deg)';
                }
            });
        });
    });
    
    // Card hover effects
    const hoverCards = document.querySelectorAll('.service-card, .portfolio-card, .testimonial-card');
    hoverCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Button ripple effect
    const rippleButtons = document.querySelectorAll('.btn');
    rippleButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.6);
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `;
            
            // Add ripple to button
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            // Remove ripple after animation
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// ===== TYPING ANIMATION =====
function initializeTypingAnimation() {
    const typingElements = document.querySelectorAll('[data-typing]');
    
    typingElements.forEach(element => {
        const text = element.dataset.typing || element.textContent;
        const speed = parseInt(element.dataset.speed) || 100;
        const delay = parseInt(element.dataset.delay) || 0;
        
        element.textContent = '';
        
        setTimeout(() => {
            typeText(element, text, speed);
        }, delay);
    });
}

function typeText(element, text, speed) {
    let index = 0;
    
    function type() {
        if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            setTimeout(type, speed);
        } else {
            element.classList.add('typing-complete');
        }
    }
    
    type();
}

// ===== COUNTER ANIMATION =====
function initializeCounterAnimation() {
    const counters = document.querySelectorAll('.stat-number, .metric-number, .counter');
    
    if (!counters.length || !('IntersectionObserver' in window)) return;
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

function animateCounter(element) {
    const target = parseInt(element.textContent.replace(/[^\d]/g, '')) || 0;
    const prefix = element.textContent.match(/^[^\d]*/)[0] || '';
    const suffix = element.textContent.match(/[^\d]*$/)[0] || '';
    
    if (target === 0) return;
    
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        
        if (current >= target) {
            element.textContent = prefix + target.toLocaleString() + suffix;
            clearInterval(timer);
            element.classList.add('counter-complete');
        } else {
            element.textContent = prefix + Math.floor(current).toLocaleString() + suffix;
        }
    }, 16);
}

// ===== UTILITY FUNCTIONS =====

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Get element offset
function getOffset(element) {
    const rect = element.getBoundingClientRect();
    return {
        top: rect.top + window.scrollY,
        left: rect.left + window.scrollX
    };
}

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Show loading overlay
function showLoading(element) {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = '<div class="spinner-border text-primary" role="status"></div>';
    overlay.dataset.loadingOverlay = 'true';
    
    element.style.position = 'relative';
    element.appendChild(overlay);
}

// Hide loading overlay
function hideLoading(element) {
    const overlay = element.querySelector('[data-loading-overlay="true"]');
    if (overlay) {
        overlay.remove();
    }
}

// ===== CONTACT FORM ENHANCEMENTS =====
function initializeContactForm() {
    const contactForm = document.querySelector('.contact-form');
    if (!contactForm) return;
    
    // Character counter for message field
    const messageField = contactForm.querySelector('textarea[name="message"]');
    if (messageField) {
        addCharacterCounter(messageField, 1000);
    }
    
    // Auto-resize textarea
    const textareas = contactForm.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        autoResizeTextarea(textarea);
    });
    
    // Phone number formatting
    const phoneField = contactForm.querySelector('input[name="phone"]');
    if (phoneField) {
        phoneField.addEventListener('input', function() {
            this.value = this.value.replace(/[^\d]/g, '');
        });
    }
}

function addCharacterCounter(element, maxLength) {
    const counter = document.createElement('small');
    counter.className = 'character-counter text-muted';
    element.parentNode.appendChild(counter);
    
    function updateCounter() {
        const remaining = maxLength - element.value.length;
        counter.textContent = `${remaining} characters remaining`;
        
        if (remaining < 50) {
            counter.classList.add('text-warning');
            counter.classList.remove('text-muted');
        } else {
            counter.classList.add('text-muted');
            counter.classList.remove('text-warning');
        }
    }
    
    element.addEventListener('input', updateCounter);
    updateCounter();
}

function autoResizeTextarea(textarea) {
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
}

// ===== QUOTE FORM FUNCTIONALITY =====
function initializeQuoteForm() {
    const quoteForm = document.querySelector('.quote-form');
    if (!quoteForm) return;
    
    // Multi-step functionality is handled in the quote.html template JavaScript
    // This is for additional enhancements
    
    // Service selection enhancement
    const serviceCheckboxes = quoteForm.querySelectorAll('input[name="services_requested"]');
    serviceCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const serviceCard = this.closest('.service-option');
            if (serviceCard) {
                serviceCard.classList.toggle('selected', this.checked);
            }
        });
    });
    
    // File upload preview
    const fileInput = quoteForm.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            showFilePreview(this);
        });
    }
}

function showFilePreview(input) {
    const files = Array.from(input.files);
    let previewHTML = '';
    
    if (files.length > 0) {
        previewHTML = '<div class="file-preview">';
        previewHTML += '<h6>Selected Files:</h6>';
        previewHTML += '<ul>';
        
        files.forEach(file => {
            const size = (file.size / 1024 / 1024).toFixed(2);
            previewHTML += `<li>${file.name} (${size} MB)</li>`;
        });
        
        previewHTML += '</ul></div>';
    }
    
    const existingPreview = input.parentNode.querySelector('.file-preview');
    if (existingPreview) {
        existingPreview.remove();
    }
    
    if (previewHTML) {
        const preview = document.createElement('div');
        preview.innerHTML = previewHTML;
        preview.className = 'file-preview mt-2';
        input.parentNode.appendChild(preview.firstChild);
    }
}

// ===== INITIALIZE PAGE-SPECIFIC FUNCTIONS =====
function initializePageSpecific() {
    // Initialize based on current page
    const currentPage = document.body.classList.contains('page-contact') ? 'contact' :
                       document.body.classList.contains('page-quote') ? 'quote' :
                       document.body.classList.contains('page-portfolio') ? 'portfolio' :
                       'default';
    
    switch (currentPage) {
        case 'contact':
            initializeContactForm();
            break;
        case 'quote':
            initializeQuoteForm();
            break;
        case 'portfolio':
            // Portfolio-specific initializations already handled
            break;
        default:
            // Default page initializations
            break;
    }
}

// ===== CSS ANIMATIONS KEYFRAMES (Added via JavaScript) =====
function addCustomAnimations() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            0% {
                transform: scale(0);
                opacity: 1;
            }
            100% {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .loading-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        }
        
        .fade-on-scroll {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        
        .fade-on-scroll.faded-in {
            opacity: 1;
            transform: translateY(0);
        }
        
        .typing-complete::after {
            content: '|';
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        
        .counter-complete {
            animation: counterPulse 0.5s ease;
        }
        
        @keyframes counterPulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
    `;
    document.head.appendChild(style);
}

// ===== FINAL INITIALIZATION =====
// Add custom animations
addCustomAnimations();

// Initialize page-specific functionality after DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(initializePageSpecific, 100);
});

// ===== ERROR HANDLING =====
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    // You can add error reporting here if needed
});

// ===== EXPORT FOR GLOBAL ACCESS =====
window.SarveshWebsite = {
    showLoading,
    hideLoading,
    validateField,
    debounce,
    throttle,
    isInViewport,
    animateCounter
};