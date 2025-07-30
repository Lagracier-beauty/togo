// Modern SaaS JavaScript - Minimal and Clean

class TogServices {
    constructor() {
        this.init();
    }

    init() {
        this.setupIntersectionObserver();
        this.setupSmoothScrolling();
        this.setupThemeToggle();
        this.setupFormValidation();
        
        // Performance optimization
        this.preloadCriticalResources();
    }

    // Optimized scroll animations
    setupIntersectionObserver() {
        const options = {
            threshold: 0.1,
            rootMargin: '0px 0px -10% 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    // Unobserve after animation to improve performance
                    observer.unobserve(entry.target);
                }
            });
        }, options);

        // Only observe elements that need animation
        document.querySelectorAll('.scroll-animate').forEach(el => {
            observer.observe(el);
        });
    }

    // Smooth scrolling for anchor links
    setupSmoothScrolling() {
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href^="#"]');
            if (!link) return;

            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    }

    // Theme toggle
    setupThemeToggle() {
        // Initialize theme from localStorage or system preference
        const savedTheme = localStorage.getItem('theme') || 
            (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        
        document.body.setAttribute('data-theme', savedTheme);

        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                document.body.setAttribute('data-theme', e.matches ? 'dark' : 'light');
            }
        });
    }

    // Modern form validation
    setupFormValidation() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                // Real-time validation on blur
                input.addEventListener('blur', () => this.validateField(input));
                
                // Clear validation on focus
                input.addEventListener('focus', () => this.clearFieldValidation(input));
            });

            // Enhanced form submission
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                }
            });
        });
    }

    validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let message = '';

        // Required field validation
        if (field.required && !value) {
            isValid = false;
            message = 'Ce champ est requis';
        }

        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                message = 'Adresse email invalide';
            }
        }

        // Phone validation for Togo
        if (field.type === 'tel' && value) {
            const phoneRegex = /^(\+228|00228)?[0-9]{8}$/;
            if (!phoneRegex.test(value.replace(/\s/g, ''))) {
                isValid = false;
                message = 'Numéro de téléphone invalide';
            }
        }

        this.setFieldValidation(field, isValid, message);
        return isValid;
    }

    setFieldValidation(field, isValid, message) {
        // Remove previous validation
        this.clearFieldValidation(field);

        if (!isValid) {
            field.style.borderColor = 'var(--error)';
            
            const errorEl = document.createElement('div');
            errorEl.className = 'field-error';
            errorEl.textContent = message;
            errorEl.style.cssText = `
                color: var(--error);
                font-size: 0.8125rem;
                margin-top: 0.25rem;
                animation: fade-in 0.2s ease;
            `;
            
            field.parentNode.appendChild(errorEl);
        } else {
            field.style.borderColor = 'var(--success)';
        }
    }

    clearFieldValidation(field) {
        field.style.borderColor = '';
        const errorEl = field.parentNode.querySelector('.field-error');
        if (errorEl) {
            errorEl.remove();
        }
    }

    validateForm(form) {
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });

        return isValid;
    }

    // Preload critical resources for better performance
    preloadCriticalResources() {
        const criticalImages = [
            // Add any critical images here
        ];

        criticalImages.forEach(src => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'image';
            link.href = src;
            document.head.appendChild(link);
        });
    }

    // Utility methods
    static showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 1rem;
            right: 1rem;
            background: var(--background);
            color: var(--foreground);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1rem;
            box-shadow: var(--shadow-lg);
            z-index: 1000;
            animation: slide-in 0.3s ease;
            max-width: 400px;
        `;

        document.body.appendChild(notification);

        if (duration > 0) {
            setTimeout(() => {
                notification.style.animation = 'fade-in 0.3s ease reverse';
                setTimeout(() => notification.remove(), 300);
            }, duration);
        }

        return notification;
    }
}

// Global theme toggle function
function toggleTheme() {
    const body = document.body;
    const isDark = body.getAttribute('data-theme') === 'dark';
    const newTheme = isDark ? 'light' : 'dark';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new TogServices();
});

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', () => {
        const perfData = performance.getEntriesByType('navigation')[0];
        if (perfData) {
            console.log(`Page loaded in ${Math.round(perfData.loadEventEnd - perfData.navigationStart)}ms`);
        }
    });
}

// Export for global use
window.TogServices = TogServices; 