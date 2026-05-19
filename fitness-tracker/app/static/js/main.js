// Utility functions
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString();
}

function formatTime(dateString) {
    return new Date(dateString).toLocaleTimeString();
}

// Animation utilities
function animateElement(element, animationClass, duration = 300) {
    element.classList.add(animationClass);
    setTimeout(() => element.classList.remove(animationClass), duration);
}

// Progress bar animation
function animateProgressBar(element, targetValue) {
    element.style.width = '0%';
    setTimeout(() => {
        element.style.width = `${targetValue}%`;
    }, 100);
}

// Real-time form validation
function setupRealTimeValidation(form) {
    const inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            validateField(input);
        });
        input.addEventListener('blur', () => {
            validateField(input);
        });
    });
}

function validateField(field) {
    const isValid = field.value.trim() !== '';
    field.classList.toggle('border-red-500', !isValid);
    field.classList.toggle('border-green-500', isValid && field.value.trim() !== '');
    
    const feedback = field.nextElementSibling;
    if (feedback && feedback.classList.contains('validation-feedback')) {
        feedback.textContent = isValid ? '✓' : 'This field is required';
        feedback.className = `validation-feedback ${isValid ? 'text-green-500' : 'text-red-500'}`;
    }
}

// Interactive charts
function initializeCharts() {
    const chartElements = document.querySelectorAll('[data-chart]');
    chartElements.forEach(element => {
        const type = element.dataset.chart;
        const data = JSON.parse(element.dataset.chartData || '{}');
        
        switch(type) {
            case 'progress':
                createProgressChart(element, data);
                break;
            case 'activity':
                createActivityChart(element, data);
                break;
            case 'nutrition':
                createNutritionChart(element, data);
                break;
        }
    });
}

// Toast notifications
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Slide in
    setTimeout(() => {
        toast.style.transform = 'translateY(0)';
    }, 100);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        toast.style.transform = 'translateY(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Interactive modals
function setupModals() {
    const modalTriggers = document.querySelectorAll('[data-modal-trigger]');
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const modalId = trigger.dataset.modalTarget;
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.remove('hidden');
                modal.classList.add('fade-in');
            }
        });
    });

    // Close modal on backdrop click
    document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
        backdrop.addEventListener('click', (e) => {
            if (e.target === backdrop) {
                backdrop.parentElement.classList.add('hidden');
                backdrop.parentElement.classList.remove('fade-in');
            }
        });
    });
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all interactive features
    setupRealTimeValidation(document.querySelectorAll('form'));
    initializeCharts();
    setupModals();
    
    // Form validation with enhanced feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!validateForm(form.id)) {
                e.preventDefault();
                showToast('Please fill in all required fields', 'error');
            }
        });
    });

    // Enhanced mobile menu
    const menuButton = document.querySelector('[data-menu-button]');
    const mobileMenu = document.querySelector('[data-mobile-menu]');
    
    if (menuButton && mobileMenu) {
        menuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            animateElement(mobileMenu, 'slide-in');
        });
    }

    // Interactive progress bars
    document.querySelectorAll('.progress-bar').forEach(bar => {
        const targetValue = bar.dataset.progress;
        if (targetValue) {
            animateProgressBar(bar, targetValue);
        }
    });

    // Enhanced image loading
    document.querySelectorAll('img').forEach(img => {
        img.classList.add('image-loading');
        
        img.addEventListener('load', function() {
            this.classList.remove('image-loading');
            animateElement(this, 'fade-in');
        });
        
        img.addEventListener('error', function() {
            this.classList.remove('image-loading');
            handleImageError(this);
        });
    });
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('border-red-500');
        } else {
            field.classList.remove('border-red-500');
        }
    });

    return isValid;
}

// Flash message handling
function showFlashMessage(message, type = 'success') {
    const flashContainer = document.createElement('div');
    flashContainer.className = `mb-4 p-4 rounded ${type === 'error' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`;
    flashContainer.textContent = message;
    
    const main = document.querySelector('main');
    main.insertBefore(flashContainer, main.firstChild);

    setTimeout(() => {
        flashContainer.remove();
    }, 5000);
}

// Add this function at the top of the file
function handleImageError(img) {
    img.onerror = null; // Prevent infinite loop
    
    // Get the image type from the src path
    const src = img.src;
    let fallbackImage;
    
    if (src.includes('/activities/')) {
        fallbackImage = '/static/images/activity-icon.png';
    } else if (src.includes('/nutrition/')) {
        fallbackImage = '/static/images/nutrition-icon.png';
    } else if (src.includes('/goals/')) {
        fallbackImage = '/static/images/goals-icon.png';
    } else {
        fallbackImage = '/static/images/placeholder.png';
    }
    
    img.src = fallbackImage;
}