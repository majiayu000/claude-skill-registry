---
name: responsive-design-patterns
description: Mobile-first responsive design patterns with breakpoints, fluid layouts, and adaptive components
license: MIT
metadata:
  adapted-by: ai-skills
  category: frontend-development
---

# Responsive Design Patterns

Mobile-first patterns for creating adaptive, responsive user interfaces.

## Breakpoint System

```typescript
export const breakpoints = {
  sm: '640px',   // Small devices
  md: '768px',   // Medium devices
  lg: '1024px',  // Large devices
  xl: '1280px',  // Extra large devices
  '2xl': '1536px' // 2X Extra large
};

// Tailwind config
module.exports = {
  theme: {
    screens: breakpoints
  }
};
```

## Mobile-First Approach

```tsx
// Start with mobile, enhance for larger screens
<div className="
  flex flex-col        /* Mobile: stack vertically */
  md:flex-row          /* Tablet+: side by side */
  gap-4
  p-4 md:p-6 lg:p-8   /* Progressive spacing */
">
  <div className="
    w-full               /* Mobile: full width */
    md:w-1/3            /* Tablet+: 1/3 width */
  ">Sidebar</div>
  
  <div className="
    w-full
    md:w-2/3
  ">Main Content</div>
</div>
```

## Fluid Typography

```css
/* Clamp for fluid scaling */
h1 {
  font-size: clamp(1.5rem, 5vw, 3rem);
}

/* Container queries */
@container (min-width: 400px) {
  .card-title {
    font-size: 1.25rem;
  }
}
```

## Responsive Images

```tsx
<picture>
  <source
    media="(min-width: 1024px)"
    srcSet="/images/hero-large.webp"
  />
  <source
    media="(min-width: 640px)"
    srcSet="/images/hero-medium.webp"
  />
  <img
    src="/images/hero-small.webp"
    alt="Hero image"
    loading="lazy"
  />
</picture>
```

## Touch-Friendly Patterns

```tsx
// Minimum touch target: 44x44px
<button className="min-h-[44px] min-w-[44px] p-3">
  <Icon />
</button>

// Swipe gestures
function useSwipe(onSwipeLeft?: () => void, onSwipeRight?: () => void) {
  const [touchStart, setTouchStart] = useState(0);
  const [touchEnd, setTouchEnd] = useState(0);
  
  const minSwipeDistance = 50;
  
  const onTouchStart = (e: TouchEvent) => {
    setTouchEnd(0);
    setTouchStart(e.targetTouches[0].clientX);
  };
  
  const onTouchMove = (e: TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };
  
  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;
    
    if (isLeftSwipe && onSwipeLeft) onSwipeLeft();
    if (isRightSwipe && onSwipeRight) onSwipeRight();
  };
  
  return { onTouchStart, onTouchMove, onTouchEnd };
}
```

## Integration Points

Complements:
- **frontend-design-systems**: For component design
- **accessibility-patterns**: For mobile accessibility
- **webapp-testing**: For responsive testing
