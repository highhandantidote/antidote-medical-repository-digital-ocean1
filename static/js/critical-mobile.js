/**
 * Critical Mobile Performance Optimizations
 * This script loads immediately to improve Core Web Vitals
 */

// Optimize for mobile performance
(function() {
    'use strict';
    
    // Critical performance optimizations
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js').catch(function() {
            // Silent fail - SW not critical
        });
    }
    
    // Optimize images for mobile
    function optimizeImages() {
        const images = document.querySelectorAll('img[data-src], img[loading="lazy"]');
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            images.forEach(img => imageObserver.observe(img));
        }
    }
    
    // Mobile touch optimizations
    function optimizeMobileTouch() {
        // Add touch-friendly click areas
        const buttons = document.querySelectorAll('button, .btn, a[role="button"]');
        buttons.forEach(btn => {
            if (!btn.style.minHeight) {
                btn.style.minHeight = '44px'; // Apple's recommended touch target size
            }
        });
    }
    
    // Core Web Vitals monitoring
    function measureCoreWebVitals() {
        if ('web-vital' in window) return;
        
        // Mark page as loaded for performance tracking
        window.addEventListener('load', () => {
            const loadTime = performance.now();
            console.log('Mobile page load time:', Math.round(loadTime), 'ms');
            
            // Track to analytics if available
            if (typeof gtag !== 'undefined') {
                gtag('event', 'page_load_time', {
                    event_category: 'Performance',
                    value: Math.round(loadTime),
                    custom_parameter_device_type: 'mobile'
                });
            }
        });
    }
    
    // Initialize optimizations
    document.addEventListener('DOMContentLoaded', function() {
        optimizeImages();
        optimizeMobileTouch();
        measureCoreWebVitals();
    });
    
})();