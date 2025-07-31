// Tog-Services - JavaScript Épuré et Simple
// Design inspiré du cahier des charges avec fonctionnalités essentielles

document.addEventListener('DOMContentLoaded', function() {
    console.log('📋 Tog-Services System Loading...');
    
    try {
        // Fonctionnalités essentielles seulement
        initMobileMenu();
        initBackToTop();
        initFormEnhancements();
        
        console.log('✅ System Ready');
    } catch (error) {
        console.error('❌ Initialization Error:', error);
    }
});

// Menu mobile simple
function initMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (!mobileMenuBtn || !mobileMenu) return;
    
    let isOpen = false;
    
    const toggleMenu = () => {
        isOpen = !isOpen;
        mobileMenuBtn.classList.toggle('active', isOpen);
        mobileMenu.classList.toggle('active', isOpen);
        
        // Empêcher le scroll
        document.body.style.overflow = isOpen ? 'hidden' : '';
    };
    
    mobileMenuBtn.addEventListener('click', toggleMenu);
    
    // Fermer en cliquant à l'extérieur
    document.addEventListener('click', (e) => {
        if (isOpen && !mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
            toggleMenu();
        }
    });
    
    // Fermer en cliquant sur un lien
    mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            if (isOpen) toggleMenu();
        });
    });
}

// Bouton retour en haut simple
function initBackToTop() {
    const backToTop = document.querySelector('.back-to-top');
    if (!backToTop) return;
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    });
    
    backToTop.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Améliorations des formulaires simples
function initFormEnhancements() {
    const formInputs = document.querySelectorAll('.form-control, .form-input');
    
    formInputs.forEach(input => {
        // Validation simple en temps réel
        input.addEventListener('blur', () => {
            validateField(input);
        });
        
        input.addEventListener('input', () => {
            if (input.classList.contains('error')) {
                validateField(input);
            }
        });
    });
}

// Validation simple des champs
function validateField(input) {
    const value = input.value.trim();
    const type = input.type;
    const required = input.hasAttribute('required');
    
    // Supprimer les classes d'état précédentes
    input.classList.remove('error', 'success');
    
    // Validation selon le type
    let isValid = true;
    
    if (required && !value) {
        isValid = false;
    } else if (type === 'email' && value && !isValidEmail(value)) {
        isValid = false;
    } else if (type === 'tel' && value && !isValidPhone(value)) {
        isValid = false;
    }
    
    // Appliquer la classe appropriée
    if (value) {
        input.classList.add(isValid ? 'success' : 'error');
    }
    
    return isValid;
}

// Validation email simple
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Validation téléphone simple (format togolais)
function isValidPhone(phone) {
    const phoneRegex = /^(\+228)?[0-9]{8}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
}

// Gestion du redimensionnement pour mobile
window.addEventListener('resize', () => {
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    
    if (window.innerWidth > 768) {
        if (mobileMenu && mobileMenuBtn) {
            mobileMenu.classList.remove('active');
            mobileMenuBtn.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
});

// Gestion de l'écran de chargement simple
window.addEventListener('load', () => {
    const loadingScreen = document.querySelector('.loading-screen');
    if (loadingScreen) {
        setTimeout(() => {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.style.display = 'none';
            }, 300);
        }, 500);
    }
});

// Export des fonctions utiles
window.TogServices = {
    validateField,
    isValidEmail,
    isValidPhone
};