// Product Detail Page JavaScript

// Image Gallery Functionality
function changeImage(thumbnail) {
    const mainImage = document.getElementById('mainImage');
    const thumbnails = document.querySelectorAll('.thumbnail');
    
    // Update main image
    mainImage.src = thumbnail.src;
    
    // Update active thumbnail
    thumbnails.forEach(thumb => thumb.classList.remove('active'));
    thumbnail.classList.add('active');
}

// Size Selection
document.addEventListener('DOMContentLoaded', function() {
    const sizeButtons = document.querySelectorAll('.size-btn');
    
    sizeButtons.forEach(button => {
        button.addEventListener('click', function() {
            sizeButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
});

// Accordion Functionality
function toggleAccordion(header) {
    const item = header.parentElement;
    const isActive = item.classList.contains('active');
    
    // Close all accordion items
    document.querySelectorAll('.accordion-item').forEach(accordionItem => {
        accordionItem.classList.remove('active');
    });
    
    // Open clicked item if it wasn't active
    if (!isActive) {
        item.classList.add('active');
    }
}

// Add to Cart Functionality
document.querySelector('.add-to-cart-btn').addEventListener('click', function() {
    const selectedSize = document.querySelector('.size-btn.active').textContent;
    
    // Add loading state
    this.textContent = 'Adding...';
    this.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        this.textContent = 'Added to Cart!';
        this.style.background = '#28a745';
        
        // Reset after 2 seconds
        setTimeout(() => {
            this.textContent = 'Add to Cart';
            this.style.background = '#333';
            this.disabled = false;
        }, 2000);
    }, 1000);
    
    console.log(`Added to cart: Loose Fit Hoodie, Size: ${selectedSize}`);
});

// Wishlist Functionality
document.querySelector('.wishlist-btn').addEventListener('click', function() {
    const icon = this.querySelector('i');
    const isWishlisted = icon.classList.contains('bxs-heart');
    
    if (isWishlisted) {
        icon.classList.remove('bxs-heart');
        icon.classList.add('bx-heart');
        this.style.color = '#666';
        this.style.borderColor = '#e9ecef';
    } else {
        icon.classList.remove('bx-heart');
        icon.classList.add('bxs-heart');
        this.style.color = '#ff6b6b';
        this.style.borderColor = '#ff6b6b';
    }
});

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Loading states and animations
function addLoadingAnimation() {
    const elements = document.querySelectorAll('.product-detail, .reviews-section, .recommendations');
    
    elements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            el.style.transition = 'all 0.6s ease';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 200);
    });
}

// Initialize animations when page loads
window.addEventListener('load', function() {
    addLoadingAnimation();
});

// Countdown Timer for Delivery
function updateDeliveryTimer() {
    const timerElement = document.querySelector('.delivery-info strong');
    if (!timerElement) return;
    
    const now = new Date();
    const cutoffTime = new Date();
    cutoffTime.setHours(14, 30, 36, 0); // 2:30:36 PM
    
    if (now > cutoffTime) {
        cutoffTime.setDate(cutoffTime.getDate() + 1);
    }
    
    const timeLeft = cutoffTime - now;
    
    if (timeLeft > 0) {
        const hours = Math.floor(timeLeft / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
        
        timerElement.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
}

// Update timer every second
setInterval(updateDeliveryTimer, 1000);
updateDeliveryTimer(); // Initial call
