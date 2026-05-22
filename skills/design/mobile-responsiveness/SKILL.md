---
name: mobile-responsiveness
description: Build responsive, mobile-first web applications. Use when implementing responsive layouts, touch interactions, mobile navigation, or optimizing for various screen sizes. Triggers on responsive design, mobile-first, breakpoints, touch events, viewport.
---

# Mobile Responsiveness

Build responsive, mobile-first web applications.

## Mobile-First Breakpoints

```css
/* Mobile first - no media query needed for mobile base */
.container {
  padding: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: 3rem;
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* Large desktop */
@media (min-width: 1280px) {
  .container {
    max-width: 1400px;
  }
}
```

## Tailwind Breakpoints

```tsx
<div className="
  p-4          /* Mobile: padding 1rem */
  md:p-8       /* Tablet 768px+: padding 2rem */
  lg:p-12      /* Desktop 1024px+: padding 3rem */
  xl:max-w-6xl /* Large 1280px+: max-width */
">
  <h1 className="
    text-2xl     /* Mobile */
    md:text-3xl  /* Tablet */
    lg:text-4xl  /* Desktop */
  ">
    Responsive Heading
  </h1>
</div>
```

## Fluid Typography

```css
:root {
  /* Fluid font size: 16px at 320px viewport, 20px at 1200px viewport */
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
  
  /* Fluid heading */
  --font-size-h1: clamp(2rem, 1.5rem + 2.5vw, 4rem);
}

body {
  font-size: var(--font-size-base);
}

h1 {
  font-size: var(--font-size-h1);
}
```

## Touch Interactions

```tsx
import { useState } from 'react';

function SwipeableCard({ onSwipeLeft, onSwipeRight, children }) {
  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);

  const minSwipeDistance = 50;

  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;
    
    if (isLeftSwipe) onSwipeLeft?.();
    if (isRightSwipe) onSwipeRight?.();
  };

  return (
    <div
      onTouchStart={onTouchStart}
      onTouchMove={onTouchMove}
      onTouchEnd={onTouchEnd}
    >
      {children}
    </div>
  );
}
```

## Mobile Navigation

```tsx
import { useState } from 'react';

function MobileNav() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Hamburger button - visible on mobile */}
      <button
        className="md:hidden p-2"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-label="Toggle menu"
      >
        <span className={`hamburger ${isOpen ? 'open' : ''}`} />
      </button>

      {/* Mobile menu */}
      <nav
        className={`
          fixed inset-0 bg-white z-50 transform transition-transform
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
          md:static md:translate-x-0 md:bg-transparent
        `}
      >
        <ul className="flex flex-col md:flex-row gap-4 p-4 md:p-0">
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact</a></li>
        </ul>
      </nav>

      {/* Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
}
```

## Safe Areas (Notch/Home Indicator)

```css
/* Account for iPhone notch and home indicator */
.container {
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
  padding-bottom: env(safe-area-inset-bottom);
}

/* Fixed bottom navigation */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding-bottom: max(1rem, env(safe-area-inset-bottom));
}
```

## Viewport Meta Tag

```html
<meta 
  name="viewport" 
  content="width=device-width, initial-scale=1, viewport-fit=cover"
/>
```

## useMediaQuery Hook

```tsx
import { useState, useEffect } from 'react';

function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    setMatches(media.matches);

    const listener = (e: MediaQueryListEvent) => setMatches(e.matches);
    media.addEventListener('change', listener);
    
    return () => media.removeEventListener('change', listener);
  }, [query]);

  return matches;
}

// Usage
function Component() {
  const isMobile = useMediaQuery('(max-width: 767px)');
  const isTablet = useMediaQuery('(min-width: 768px) and (max-width: 1023px)');
  const isDesktop = useMediaQuery('(min-width: 1024px)');

  return isMobile ? <MobileView /> : <DesktopView />;
}
```

## Resources

- **Responsive Design**: https://web.dev/learn/design/
- **Mobile-First CSS**: https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design
- **Viewport Units**: https://developer.mozilla.org/en-US/docs/Web/CSS/length#viewport-percentage_lengths
