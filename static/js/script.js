// Main JavaScript for the application

document.addEventListener('DOMContentLoaded', function() {
    // Close flash messages
    document.querySelectorAll('.close-flash').forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.animation = 'fadeOut 0.5s ease-out';
            setTimeout(() => {
                this.parentElement.remove();
            }, 500);
        });
    });
    
    // Auto-hide flash messages after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.flash').forEach(flash => {
            flash.style.animation = 'fadeOut 0.5s ease-out';
            setTimeout(() => {
                flash.remove();
            }, 500);
        });
    }, 5000);
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add animation to cards when they come into view
    const animateOnScroll = function() {
        const cards = document.querySelectorAll('.feature-card, .about-card, .disclaimer-card');
        
        cards.forEach(card => {
            const cardPosition = card.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (cardPosition < screenPosition) {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }
        });
    };
    
    // Set initial state for animated cards
    document.querySelectorAll('.feature-card, .about-card, .disclaimer-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });
    
    // Run on load and scroll
    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll);
    
    // File upload display
    const fileInput = document.getElementById('file-upload');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileInfo = document.getElementById('file-info');
            if (this.files.length > 0) {
                fileInfo.textContent = this.files[0].name;
            } else {
                fileInfo.textContent = 'No file selected';
            }
        });
    }
});

// Custom fadeOut animation for flash messages
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(style);

// Add to your existing script.js
document.querySelectorAll('.toggle-text-btn').forEach(button => {
    button.addEventListener('click', function() {
        const row = this.closest('tr');
        const fullText = row.querySelector('.full-text');
        const truncated = row.querySelector('.truncated-text');
        
        if (fullText.style.display === 'none') {
            fullText.style.display = '';
            truncated.style.display = 'none';
            this.textContent = 'Show Less';
        } else {
            fullText.style.display = 'none';
            truncated.style.display = '';
            this.textContent = 'Show More';
        }
    });
});