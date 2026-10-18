/* ============================================
   SHOP HỒNG LOAN - JAVASCRIPT
   Alpine.js extended utilities
   ============================================ */

// ===== GLOBAL UTILITIES =====
document.addEventListener('DOMContentLoaded', () => {
    
    // Format currency Vietnamese style (ví dụ: 360.000 đ)
    window.formatVND = (amount) => {
        const num = Math.round(Number(amount) || 0);
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".") + " đ";
    };
    
    // Intersection Observer for fade-in animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    // Apply fade-in to product cards
    document.querySelectorAll('.product-card, article').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', e => {
            e.preventDefault();
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });
    
    // Phone number formatter
    document.querySelectorAll('input[type="tel"]').forEach(input => {
        input.addEventListener('input', e => {
            let val = e.target.value.replace(/\D/g, '');
            if (val.length > 10) val = val.slice(0, 10);
            e.target.value = val;
        });
    });
    
    // Image lazy loading with blur effect
    document.querySelectorAll('img[loading="lazy"]').forEach(img => {
        img.style.filter = 'blur(5px)';
        img.style.transition = 'filter 0.4s ease';
        img.addEventListener('load', () => {
            img.style.filter = 'none';
        });
    });
    
    // Notification Toast
    window.showToast = (message, type = 'success') => {
        const toast = document.createElement('div');
        const bgColor = type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-gold';
        
        toast.className = `fixed top-24 right-4 z-50 ${bgColor} text-white px-6 py-3 rounded-xl shadow-xl font-medium text-sm transform translate-x-full transition-transform duration-300`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        requestAnimationFrame(() => {
            toast.style.transform = 'translateX(0)';
        });
        
        setTimeout(() => {
            toast.style.transform = 'translateX(150%)';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    };
    
    // Active nav link highlighting
    const currentPath = window.location.pathname;
    document.querySelectorAll('nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('text-gold');
        }
    });
    
    console.log('%c🌸 Shop Hồng Loan', 'color: #C9A84C; font-size: 18px; font-weight: bold; font-family: serif;');
    console.log('%cThời trang trung niên cao cấp', 'color: #4A4A4A; font-size: 12px;');
});


// ===== CSRF TOKEN HELPER =====
function getCsrfToken() {
    const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1].trim() : '';
}


// ===== CATALOG FILTER (without page reload) =====
function filterProducts(categorySlug) {
    const cards = document.querySelectorAll('.product-card, #product-grid article');
    let visibleCount = 0;
    
    cards.forEach((card, i) => {
        const matches = categorySlug === 'all' || card.dataset.category === categorySlug;
        
        if (matches) {
            card.style.display = '';
            card.style.animationDelay = `${i * 0.05}s`;
            card.style.animation = 'none';
            card.offsetHeight; // reflow
            card.style.animation = 'fadeIn 0.4s ease both';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    // Update URL without reload
    const url = new URL(window.location);
    if (categorySlug === 'all') {
        url.searchParams.delete('category');
    } else {
        url.searchParams.set('category', categorySlug);
    }
    history.pushState({}, '', url);
    
    // Update product count
    const countEl = document.querySelector('[data-product-count]');
    if (countEl) countEl.textContent = visibleCount;
}


// ===== SCROLL TO ORDER FORM =====
function scrollToOrder() {
    const form = document.querySelector('[x-data="productDetail()"]');
    if (form) {
        const orderBlock = form.querySelector('form');
        if (orderBlock) {
            orderBlock.scrollIntoView({ behavior: 'smooth', block: 'center' });
            // Flash the order form border
            const border = orderBlock.closest('.border-gold');
            if (border) {
                border.style.boxShadow = '0 0 0 4px rgba(201, 168, 76, 0.3)';
                setTimeout(() => border.style.boxShadow = '', 1500);
            }
        }
    }
}
