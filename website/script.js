// ===============================================
// Navigation Toggle for Mobile
// ===============================================
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');
const navLinks = document.querySelectorAll('.nav-link');

// Toggle mobile menu
navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    
    // Animate hamburger icon
    const spans = navToggle.querySelectorAll('span');
    if (navMenu.classList.contains('active')) {
        spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
        spans[1].style.opacity = '0';
        spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
    } else {
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
    }
});

// Close mobile menu when clicking on a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        const spans = navToggle.querySelectorAll('span');
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
    });
});

// ===============================================
// Navbar Scroll Effect
// ===============================================
const navbar = document.getElementById('navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    // Add shadow when scrolled
    if (currentScroll > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
});

// ===============================================
// Smooth Scrolling for Anchor Links
// ===============================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        
        // Only handle internal anchor links
        if (href !== '#' && href.length > 1) {
            e.preventDefault();
            const target = document.querySelector(href);
            
            if (target) {
                const navbarHeight = navbar.offsetHeight;
                const targetPosition = target.offsetTop - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        }
    });
});

// ===============================================
// Copy to Clipboard Functionality
// ===============================================
const copyButtons = document.querySelectorAll('.copy-btn');

copyButtons.forEach(button => {
    button.addEventListener('click', async () => {
        const textToCopy = button.getAttribute('data-copy');
        
        try {
            await navigator.clipboard.writeText(textToCopy);
            
            // Visual feedback
            const originalHTML = button.innerHTML;
            button.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M13.5 3.5L5.5 11.5L2 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            `;
            button.style.color = 'var(--success-color)';
            
            setTimeout(() => {
                button.innerHTML = originalHTML;
                button.style.color = '';
            }, 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
            
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = textToCopy;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            document.body.appendChild(textArea);
            textArea.select();
            
            try {
                document.execCommand('copy');
                const originalHTML = button.innerHTML;
                button.innerHTML = '✓';
                button.style.color = 'var(--success-color)';
                
                setTimeout(() => {
                    button.innerHTML = originalHTML;
                    button.style.color = '';
                }, 2000);
            } catch (err) {
                console.error('Fallback copy failed: ', err);
            }
            
            document.body.removeChild(textArea);
        }
    });
});

// ===============================================
// Intersection Observer for Animations
// ===============================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe feature cards, doc cards, and other elements
const animateOnScroll = document.querySelectorAll('.feature-card, .doc-card, .step, .contribute-card');
animateOnScroll.forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(30px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(element);
});

// ===============================================
// Active Navigation Link Highlighting
// ===============================================
const sections = document.querySelectorAll('section[id]');

function highlightNavigation() {
    const scrollPosition = window.pageYOffset;
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');
        
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}

window.addEventListener('scroll', highlightNavigation);

// ===============================================
// Parallax Effect for Hero Section
// ===============================================
const heroSection = document.querySelector('.hero');
const satelliteOrbit = document.querySelector('.satellite-orbit');

window.addEventListener('scroll', () => {
    if (heroSection && satelliteOrbit) {
        const scrolled = window.pageYOffset;
        const heroBottom = heroSection.offsetTop + heroSection.offsetHeight;
        
        if (scrolled < heroBottom) {
            const parallaxSpeed = 0.5;
            satelliteOrbit.style.transform = `translateY(${scrolled * parallaxSpeed}px)`;
        }
    }
});

// ===============================================
// Dynamic Year in Footer
// ===============================================
const updateYear = () => {
    const yearElements = document.querySelectorAll('.footer-bottom p:first-child');
    const currentYear = new Date().getFullYear();
    yearElements.forEach(element => {
        // Replace any 4-digit year with current year
        element.textContent = element.textContent.replace(/\b\d{4}\b/, currentYear);
    });
};

updateYear();

// ===============================================
// Loading Animation
// ===============================================
window.addEventListener('load', () => {
    // Remove any loading overlays or add entrance animations
    document.body.style.opacity = '1';
});

// ===============================================
// Enhanced Accessibility
// ===============================================
// Add keyboard navigation support
document.addEventListener('keydown', (e) => {
    // Close mobile menu on Escape key
    if (e.key === 'Escape' && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
        const spans = navToggle.querySelectorAll('span');
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
    }
});

// Focus management for accessibility
const focusableElements = 'a[href], button, textarea, input, select';
const modal = document.querySelector('.nav-menu');

if (modal) {
    const firstFocusableElement = modal.querySelectorAll(focusableElements)[0];
    const focusableContent = modal.querySelectorAll(focusableElements);
    const lastFocusableElement = focusableContent[focusableContent.length - 1];

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab' && modal.classList.contains('active')) {
            if (e.shiftKey) {
                if (document.activeElement === firstFocusableElement) {
                    lastFocusableElement.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastFocusableElement) {
                    firstFocusableElement.focus();
                    e.preventDefault();
                }
            }
        }
    });
}

// ===============================================
// Performance Optimization
// ===============================================
// Debounce scroll events
function debounce(func, wait = 10, immediate = true) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

// Apply debounce to scroll handlers
const debouncedHighlightNav = debounce(highlightNavigation, 10);
window.addEventListener('scroll', debouncedHighlightNav);

// ===============================================
// Easter Egg: Konami Code
// ===============================================
let konamiCode = [];
const konamiPattern = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    // Normalize key to lowercase for letter keys
    const key = e.key.length === 1 ? e.key.toLowerCase() : e.key;
    konamiCode.push(key);
    konamiCode = konamiCode.slice(-konamiPattern.length);
    
    if (konamiCode.join(',') === konamiPattern.join(',')) {
        // Easter egg activated!
        const satellite = document.querySelector('.satellite');
        if (satellite) {
            satellite.style.animation = 'orbit 2s linear infinite';
            setTimeout(() => {
                satellite.style.animation = 'orbit 10s linear infinite';
            }, 10000);
        }
        console.log('🛰️ Satellite speed boost activated! 🚀');
    }
});

// ===============================================
// Console Message
// ===============================================
console.log('%c🛰️ Starlink DIY', 'font-size: 20px; font-weight: bold; color: #00d4ff;');
console.log('%cAccess to communication is a fundamental right.', 'font-size: 14px; color: #94a3b8;');
console.log('%cInterested in contributing? Check out: https://github.com/AlKhazarof/starlink-diy', 'font-size: 12px; color: #64748b;');
