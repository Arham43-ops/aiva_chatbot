/**
 * UI Animations and Interactions
 * Handles smooth animations and micro-interactions
 */

// Fade in elements on scroll
const observeElements = () => {
    const elements = document.querySelectorAll('[data-animate]');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const animationType = entry.target.dataset.animate || 'fade-in-up';
                entry.target.classList.add(`animate-${animationType}`);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    elements.forEach(el => observer.observe(el));
};

// Typing effect for bot messages
const typeMessage = (element, text, speed = 30) => {
    return new Promise((resolve) => {
        let i = 0;
        element.textContent = '';

        const type = () => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            } else {
                resolve();
            }
        };

        type();
    });
};

// Smooth scroll to element
const smoothScrollTo = (element, duration = 300) => {
    const start = element.scrollTop;
    const target = element.scrollHeight;
    const change = target - start;
    const startTime = performance.now();

    const animateScroll = (currentTime) => {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function
        const easeInOutCubic = progress < 0.5
            ? 4 * progress * progress * progress
            : 1 - Math.pow(-2 * progress + 2, 3) / 2;

        element.scrollTop = start + change * easeInOutCubic;

        if (progress < 1) {
            requestAnimationFrame(animateScroll);
        }
    };

    requestAnimationFrame(animateScroll);
};

// Add ripple effect to buttons
const addRippleEffect = () => {
    document.querySelectorAll('.btn, .sidebar-link').forEach(button => {
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');

            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });
};

// Add CSS for ripple effect
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
    
    .btn, .sidebar-link {
        position: relative;
        overflow: hidden;
    }
`;
document.head.appendChild(rippleStyle);

// Parallax effect for background
const addParallaxEffect = () => {
    let ticking = false;

    document.addEventListener('mousemove', (e) => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const x = e.clientX / window.innerWidth;
                const y = e.clientY / window.innerHeight;

                const canvas = document.getElementById('particles-canvas');
                if (canvas) {
                    canvas.style.transform = `translate(${x * 10}px, ${y * 10}px)`;
                }

                ticking = false;
            });

            ticking = true;
        }
    });
};

// Initialize all animations
document.addEventListener('DOMContentLoaded', () => {
    observeElements();
    addRippleEffect();
    addParallaxEffect();

    // Add smooth scroll to chat window
    const chatWindow = document.getElementById('chat-window');
    if (chatWindow) {
        const scrollToBottom = () => smoothScrollTo(chatWindow);

        // Observe new messages
        const observer = new MutationObserver(scrollToBottom);
        observer.observe(chatWindow, { childList: true });
    }
});

// Export functions for use in other scripts
window.UIAnimations = {
    typeMessage,
    smoothScrollTo,
    observeElements
};
