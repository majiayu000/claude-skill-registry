---
name: mobile-first-designer
description: Expert responsive design mentor focused on modern mobile UI patterns, touch-friendly interactions, and performance optimization. Reviews layouts for mobile-first best practices, identifies accessibility issues, validates touch targets, checks responsive breakpoints, and suggests PWA enhancements. Use when designing or reviewing mobile interfaces, responsive layouts, touch interactions, or when users mention mobile design, responsive web design, PWA, or accessibility.
---

# Mobile-First Designer

## Overview

This skill provides expert guidance on creating mobile-first, responsive designs that prioritize usability, performance, and accessibility across all devices. It enforces industry standards for touch interactions, responsive layouts, and progressive web app capabilities.

**Core Philosophy**: Design for mobile constraints first, then progressively enhance for larger screens. This ensures optimal experiences on the devices most users rely on.

---

## Critical Mobile-First Standards

### Touch Target Requirements

**Minimum Size: 44x44 pixels** (Apple HIG standard)
- All interactive elements (buttons, links, inputs) must meet this minimum
- Provides comfortable tap area for various finger sizes
- Prevents accidental taps and user frustration

**Spacing: Minimum 8px between interactive elements**
- Prevents accidental activation of adjacent controls
- Improves accuracy and reduces user errors
- Critical for forms, navigation menus, and action buttons

**Examples**:
```css
/* Good - Meets minimum touch target */
.button {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 24px;
}

/* Good - Adequate spacing */
.action-buttons {
  display: flex;
  gap: 8px; /* Minimum spacing */
}

/* Bad - Too small for touch */
.small-link {
  font-size: 10px;
  padding: 2px;
}
```

---

## Mobile-First CSS Architecture

### Start with Base Mobile Styles

Write CSS for mobile devices first, then use `min-width` media queries to enhance for larger screens:

```css
/* Base styles for mobile (320px+) */
body {
  font-size: 16px; /* Never go below 16px to prevent zoom on iOS */
  line-height: 1.5;
  padding: 16px;
}

.container {
  width: 100%;
  max-width: 100%;
}

/* Tablet enhancement (768px+) */
@media (min-width: 768px) {
  body {
    font-size: 18px;
    padding: 24px;
  }
  
  .container {
    max-width: 720px;
    margin: 0 auto;
  }
}

/* Desktop enhancement (1024px+) */
@media (min-width: 1024px) {
  body {
    font-size: 20px;
  }
  
  .container {
    max-width: 960px;
  }
}
```

### Key Breakpoints (2025 Standards)

- **320px**: Small phones (base)
- **480px**: Large phones (landscape)
- **768px**: Tablets (portrait)
- **1024px**: Tablets (landscape) / Small desktops
- **1280px**: Desktops
- **1920px**: Large screens

---

## Typography Standards

### Font Sizing

**Mobile Requirements**:
- **Body text**: Minimum 16px (prevents iOS auto-zoom on input focus)
- **Headings**: Scale proportionally (1.25-2x body size)
- **Line height**: 1.5 for body text, 1.2-1.3 for headings
- **Line length**: Maximum 65 characters per line for readability

```css
/* Mobile typography */
body {
  font-size: 16px;
  line-height: 1.5;
}

h1 { font-size: 32px; line-height: 1.2; }
h2 { font-size: 28px; line-height: 1.25; }
h3 { font-size: 24px; line-height: 1.3; }

.content {
  max-width: 65ch; /* Optimal readability */
}

/* Scale up for larger screens */
@media (min-width: 768px) {
  body { font-size: 18px; }
  h1 { font-size: 40px; }
}
```

---

## Responsive Layout Patterns

### Fluid Grid System

Use flexible, percentage-based layouts that adapt naturally:

```css
/* Flexbox approach */
.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.grid-item {
  flex: 1 1 100%; /* Mobile: full width */
  min-width: 0; /* Prevents overflow */
}

@media (min-width: 768px) {
  .grid-item {
    flex: 1 1 calc(50% - 8px); /* Tablet: 2 columns */
  }
}

@media (min-width: 1024px) {
  .grid-item {
    flex: 1 1 calc(33.333% - 12px); /* Desktop: 3 columns */
  }
}
```

### Responsive Images

Serve appropriately sized images for different devices:

```html
<!-- Responsive image with srcset -->
<img 
  src="image-320w.jpg" 
  srcset="image-320w.jpg 320w,
          image-640w.jpg 640w,
          image-1280w.jpg 1280w"
  sizes="(max-width: 480px) 100vw,
         (max-width: 768px) 50vw,
         25vw"
  alt="Description"
>

<!-- Modern image formats -->
<picture>
  <source srcset="image.webp" type="image/webp">
  <source srcset="image.avif" type="image/avif">
  <img src="image.jpg" alt="Fallback">
</picture>
```

---

## Navigation Patterns

### Mobile-Optimized Navigation

**Hamburger Menu** (for complex navigation):
```css
/* Mobile: Show hamburger */
.mobile-menu {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: white;
  z-index: 1000;
}

.hamburger {
  display: block;
  width: 44px;
  height: 44px;
  padding: 8px;
}

.mobile-menu.active {
  display: block;
}

/* Desktop: Show full navigation */
@media (min-width: 768px) {
  .hamburger {
    display: none;
  }
  
  .desktop-nav {
    display: flex;
  }
}
```

**Fixed Header** (stays accessible during scroll):
```css
header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

---

## Performance Optimization

### Core Web Vitals Targets (2025)

**Largest Contentful Paint (LCP)**: < 2.5 seconds
- Load critical content first
- Optimize images and fonts
- Minimize render-blocking resources

**First Input Delay (FID)**: < 100 milliseconds
- Reduce JavaScript execution time
- Break up long tasks
- Use web workers for heavy operations

**Cumulative Layout Shift (CLS)**: < 0.1
- Reserve space for images (use aspect-ratio or explicit dimensions)
- Avoid inserting content above existing content
- Use CSS transforms for animations

### Performance Techniques

```css
/* Lazy loading for images */
<img src="image.jpg" loading="lazy" alt="Description">

/* Aspect ratio to prevent layout shift */
.image-container {
  aspect-ratio: 16 / 9;
}

/* Optimize animations */
.animated-element {
  will-change: transform; /* Hint to browser */
  transform: translateX(0); /* Use transform instead of left/margin */
}
```

---

## Progressive Web App (PWA) Enhancements

### Essential PWA Requirements

**1. HTTPS Required**
- PWAs must be served over secure connections
- Use SSL certificates from Let's Encrypt, Cloudflare, etc.

**2. Web App Manifest**
Create `manifest.json` in your root directory:

```json
{
  "name": "Your App Name",
  "short_name": "App",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#007bff",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

**3. Service Worker for Offline Support**
Basic service worker structure:

```javascript
// sw.js
const CACHE_NAME = 'v1';
const urlsToCache = [
  '/',
  '/styles/main.css',
  '/scripts/main.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
```

**4. Add to Home Screen Prompt**
```javascript
// Detect install prompt
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  // Show custom install button
  showInstallButton();
});
```

---

## Accessibility Standards

### WCAG 2.1 AA Compliance

**Color Contrast**:
- Normal text: Minimum 4.5:1 contrast ratio
- Large text (18px+): Minimum 3:1 contrast ratio
- Test with tools like WebAIM Contrast Checker

**Keyboard Navigation**:
- All interactive elements must be keyboard accessible
- Visible focus indicators required
- Logical tab order maintained

```css
/* Clear focus indicators */
button:focus,
a:focus,
input:focus {
  outline: 2px solid #007bff;
  outline-offset: 2px;
}

/* Skip to content link */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: white;
  padding: 8px;
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

**ARIA Labels**:
```html
<!-- Screen reader support -->
<button aria-label="Close menu">
  <span aria-hidden="true">&times;</span>
</button>

<nav aria-label="Main navigation">
  <!-- Navigation items -->
</nav>

<img src="chart.png" alt="Sales increased 25% in Q4 2024">
```

---

## Touch Interaction Guidelines

### Avoid Hover-Dependent Features

Touch devices don't support hover states. Design with tap/press interactions:

**Bad**:
```css
/* Don't rely on hover for essential info */
.tooltip {
  display: none;
}
.element:hover .tooltip {
  display: block;
}
```

**Good**:
```css
/* Use tap/press states */
.element:active .tooltip,
.element:focus .tooltip {
  display: block;
}
```

### Touch Gestures

Support common mobile gestures:
- **Swipe**: Navigation, carousels, dismissing items
- **Pull to refresh**: Content updates
- **Pinch to zoom**: Images, maps (if appropriate)
- **Long press**: Context menus, additional options

```javascript
// Touch event handling
let touchStartX = 0;
let touchEndX = 0;

element.addEventListener('touchstart', e => {
  touchStartX = e.changedTouches[0].screenX;
});

element.addEventListener('touchend', e => {
  touchEndX = e.changedTouches[0].screenX;
  handleSwipe();
});

function handleSwipe() {
  if (touchEndX < touchStartX - 50) {
    // Swipe left
  }
  if (touchEndX > touchStartX + 50) {
    // Swipe right
  }
}
```

---

## Review Checklist

When reviewing mobile designs, verify:

### Layout & Spacing
- [ ] Touch targets minimum 44x44px
- [ ] 8px minimum spacing between interactive elements
- [ ] No horizontal scroll at any breakpoint
- [ ] Content fits viewport without zooming
- [ ] Adequate padding/margins on all sides (16px minimum)

### Typography
- [ ] Body text minimum 16px
- [ ] Line height 1.5 for body text
- [ ] Line length maximum 65 characters
- [ ] Text scales appropriately across breakpoints

### Performance
- [ ] Images optimized and responsive
- [ ] LCP < 2.5 seconds
- [ ] FID < 100 milliseconds
- [ ] CLS < 0.1
- [ ] No render-blocking resources

### Navigation
- [ ] Easy to access and use on mobile
- [ ] Touch-friendly menu items
- [ ] Clear visual hierarchy
- [ ] Hamburger menu for complex navigation
- [ ] Fixed header if needed

### Accessibility
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] All interactive elements keyboard accessible
- [ ] Visible focus indicators
- [ ] ARIA labels where needed
- [ ] Alt text for images

### Touch Interactions
- [ ] No hover-dependent features
- [ ] Touch gestures supported where appropriate
- [ ] Visual feedback for taps/presses
- [ ] Swipe-friendly carousels/galleries

### PWA Considerations
- [ ] HTTPS enabled
- [ ] Web app manifest present
- [ ] Service worker for offline support
- [ ] Installable on home screen
- [ ] Works offline (if applicable)

---

## Common Mobile Design Mistakes

### ❌ Avoid These Patterns

**1. Tiny Touch Targets**
```css
/* BAD - Too small */
.link {
  font-size: 12px;
  padding: 2px 4px;
}
```

**2. Desktop-First Thinking**
```css
/* BAD - Requires override for mobile */
.element {
  width: 1200px; /* Doesn't fit mobile */
}

@media (max-width: 768px) {
  .element {
    width: 100%; /* Unnecessary override */
  }
}
```

**3. Ignoring Touch Interactions**
```css
/* BAD - Hover only */
.dropdown:hover .menu {
  display: block;
}
```

**4. Fixed Widths**
```css
/* BAD */
.container {
  width: 960px;
}

/* GOOD */
.container {
  max-width: 960px;
  width: 100%;
  padding: 0 16px;
}
```

**5. No Viewport Meta Tag**
```html
<!-- Always include this -->
<meta name="viewport" content="width=device-width, initial-scale=1">
```

---

## Testing Recommendations

### Test on Real Devices

**Minimum Test Matrix**:
- iOS (iPhone 13+, iPad)
- Android (Pixel, Samsung Galaxy)
- Various screen sizes (small phone to tablet)
- Different network conditions (3G, 4G, 5G, offline)

### Testing Tools

**Browser DevTools**:
- Chrome DevTools: Device simulation, network throttling
- Firefox Responsive Design Mode
- Safari Web Inspector (for iOS testing)

**Performance Testing**:
- Google PageSpeed Insights
- Lighthouse (in Chrome DevTools)
- WebPageTest
- GTmetrix

**Accessibility Testing**:
- WAVE (Web Accessibility Evaluation Tool)
- axe DevTools
- Color contrast analyzers

**Cross-Browser Testing**:
- BrowserStack
- LambdaTest
- Sauce Labs

---

## Implementation Workflow

### Step-by-Step Process

**1. Start with Mobile Wireframes**
- Design for 320-375px width first
- Focus on essential content and actions
- Establish visual hierarchy

**2. Build Mobile-First CSS**
- Write base styles for mobile
- Add progressive enhancements with min-width media queries
- Test at each breakpoint

**3. Optimize Performance**
- Compress and optimize images
- Minify CSS/JS
- Implement lazy loading
- Test Core Web Vitals

**4. Add Touch Interactions**
- Ensure all buttons meet 44px minimum
- Add appropriate spacing
- Test on actual touch devices

**5. Implement PWA Features** (if applicable)
- Add manifest.json
- Create service worker
- Test offline functionality
- Verify installability

**6. Accessibility Audit**
- Check color contrast
- Test keyboard navigation
- Add ARIA labels
- Verify screen reader compatibility

**7. Cross-Device Testing**
- Test on multiple devices
- Verify responsive breakpoints
- Check performance metrics
- Gather user feedback

---

## Resources & Standards

### Official Guidelines
- **Apple Human Interface Guidelines**: 44pt minimum touch targets
- **Google Material Design**: Touch target guidance
- **W3C Mobile Web Best Practices**: Accessibility and usability
- **WCAG 2.1**: Accessibility standards

### Key Metrics (2025)
- **Mobile traffic**: 60%+ of global web traffic
- **Expected load time**: < 3 seconds (53% abandon otherwise)
- **Touch target size**: 44x44px minimum
- **Font size**: 16px minimum for body text
- **Spacing**: 8px minimum between interactive elements

---

## Summary

Mobile-first design is not optional in 2025—it's essential. By following these guidelines, you'll create experiences that:

✅ Work beautifully on all devices
✅ Load fast and perform smoothly
✅ Are accessible to all users
✅ Convert better and engage more effectively
✅ Rank higher in search results (mobile-first indexing)

Remember: Design for mobile constraints first, then progressively enhance for larger screens. This ensures your design works where it matters most—on the devices most users rely on daily.