// JavaScript principal pour Tog-Services

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des tooltips Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Animation des statistiques
    animateStats();

    // Gestion des formulaires HTMX
    setupHTMX();
});

function animateStats() {
    // Animation des chiffres dans la section statistiques
    const stats = document.querySelectorAll('.stats-section .h2');
    stats.forEach(stat => {
        const finalValue = stat.textContent;
        const numericValue = parseInt(finalValue.replace(/\D/g, ''));
        
        if (numericValue) {
            animateNumber(stat, 0, numericValue, 2000);
        }
    });
}

function animateNumber(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current) + '+';
    }, 16);
}

function setupHTMX() {
    // Configuration HTMX personnalisée
    document.body.addEventListener('htmx:beforeRequest', function(evt) {
        // Afficher un indicateur de chargement
        const target = evt.detail.target;
        if (target) {
            target.style.opacity = '0.7';
        }
    });

    document.body.addEventListener('htmx:afterRequest', function(evt) {
        // Masquer l'indicateur de chargement
        const target = evt.detail.target;
        if (target) {
            target.style.opacity = '1';
        }
    });
}

// Fonction pour valider les formulaires
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Fonction pour afficher les messages de succès/erreur
function showMessage(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss après 5 secondes
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
} 