# Scroll-Driven Animations

Three tiers: CSS-native (modern), IntersectionObserver (universal), GSAP ScrollTrigger (optional enhancement).

## Tier 1: CSS Scroll-Driven (Chrome 115+, Edge 115+)

```css
@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: none; }
}

.scroll-reveal {
  animation: fade-in-up linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 30%;
}
```

### `animation-timeline` Values

| Value | Behavior |
|-------|----------|
| `scroll()` | Progress-based, tied to scroll container |
| `view()` | Tied to element entering/exiting viewport |
| `scroll(root)` | Tied to document scroll |
| `scroll(nearest)` | Tied to nearest scrollable ancestor |

### `animation-range` Values

| Range | When it plays |
|-------|---------------|
| `entry 0% entry 100%` | Element entering viewport (bottom edge in → top edge in) |
| `exit 0% exit 100%` | Element exiting viewport |
| `contain 0% contain 100%` | Element fully visible |
| `entry 0% entry 30%` | First 30% of entry — quick reveal |

### Feature Detection

```css
@supports (animation-timeline: view()) {
  .scroll-reveal {
    animation: fade-in-up linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 30%;
  }
}
```

## Tier 2: IntersectionObserver (Universal Fallback)

```javascript
function initScrollReveals(selector, options = {}) {
  const {
    threshold = 0.1,
    rootMargin = '0px 0px -50px 0px',
    stagger = 100,
    once = true
  } = options;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const children = entry.target.querySelectorAll('.reveal-child');
        if (children.length) {
          children.forEach((child, i) => {
            child.style.transitionDelay = `${i * stagger}ms`;
            child.classList.add('is-visible');
          });
        } else {
          entry.target.classList.add('is-visible');
        }
        if (once) observer.unobserve(entry.target);
      }
    });
  }, { threshold, rootMargin });

  document.querySelectorAll(selector).forEach(el => observer.observe(el));
}
```

### Threshold Array for Progress

```javascript
const thresholds = Array.from({ length: 20 }, (_, i) => i / 19);

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    const progress = entry.intersectionRatio;
    entry.target.style.setProperty('--scroll-progress', progress);
  });
}, { threshold: thresholds });
```

Use with CSS:
```css
.parallax-element {
  transform: translateY(calc(var(--scroll-progress, 0) * -30px));
  opacity: var(--scroll-progress, 0);
}
```

## Tier 3: GSAP ScrollTrigger (Optional)

CDN:
```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15/dist/ScrollTrigger.min.js"></script>
```

```javascript
gsap.registerPlugin(ScrollTrigger);

gsap.from('.feature-card', {
  y: 40,
  opacity: 0,
  duration: 0.8,
  stagger: 0.15,
  scrollTrigger: {
    trigger: '.features-section',
    start: 'top 80%',
    toggleActions: 'play none none none'
  }
});
```

### Pin + Scrub (scroll-linked progress)

```javascript
gsap.to('.progress-fill', {
  width: '100%',
  scrollTrigger: {
    trigger: '.progress-section',
    start: 'top center',
    end: 'bottom center',
    scrub: true
  }
});
```

### License Note

GSAP is free for standard websites. SaaS products embedding GSAP require a Business license. For self-contained skill output, this is fine — but document the constraint.

## Progressive Enhancement Strategy

```
Base layer (no-JS / reduced-motion):
  All content visible, no animation

Enhanced layer (IntersectionObserver):
  .scroll-reveal { opacity: 0; transform: translateY(20px); }
  .scroll-reveal.is-visible { opacity: 1; transform: none; }

Premium layer (CSS scroll-driven):
  @supports (animation-timeline: view()) { ... }

Optional layer (GSAP):
  Complex choreography, pin-and-scrub, multi-element timelines
```

Implementation order: always start with the base layer, add IntersectionObserver for universal animation, then layer CSS scroll-driven and GSAP on top.

## Parallax

```javascript
function initParallax(selector, speed = 0.3) {
  const els = document.querySelectorAll(selector);
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  function tick() {
    els.forEach(el => {
      const rect = el.getBoundingClientRect();
      const centerY = rect.top + rect.height / 2;
      const viewCenter = window.innerHeight / 2;
      const offset = (centerY - viewCenter) * speed;
      el.style.transform = `translateY(${offset}px)`;
    });
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
```

Speed values: 0.1 (subtle), 0.3 (medium), 0.5 (dramatic). Negative values reverse direction.

## Reduced Motion

Disable all scroll animations:
```css
@media (prefers-reduced-motion: reduce) {
  .scroll-reveal,
  .parallax-element {
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
    animation: none !important;
  }
}
```

```javascript
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  // Skip all scroll animation initialization
  document.querySelectorAll('.scroll-reveal').forEach(el => {
    el.classList.add('is-visible');
  });
  return;
}
```
