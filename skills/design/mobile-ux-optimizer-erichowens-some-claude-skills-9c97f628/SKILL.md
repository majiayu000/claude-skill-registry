---
name: mobile-ux-optimizer
description: Mobile-first UX optimization for touch interfaces, responsive layouts, and performance. Use for viewport handling, touch targets, gestures, mobile navigation. Activate on mobile, touch, responsive, dvh, viewport, safe area, hamburger menu. NOT for native app development (use React Native skills), desktop-only features, or general CSS (use Tailwind docs).
allowed-tools: Read,Write,Edit,Bash,Grep,Glob
category: Design & Creative
tags:
  - mobile
  - ux
  - touch
  - responsive
  - viewport
  - safe-area
  - navigation
---

# Mobile-First UX Optimization

Build touch-optimized, performant mobile experiences with proper viewport handling and responsive patterns.

## When to Use

✅ **USE this skill for:**
- Viewport issues (`100vh` problems, safe areas, notches)
- Touch target sizing and spacing
- Mobile navigation patterns (bottom nav, drawers, hamburger menus)
- Swipe gestures and pull-to-refresh
- Responsive breakpoint strategies
- Mobile performance optimization

❌ **DO NOT use for:**
- Native app development → use `react-native` or `swift-executor` skills
- Desktop-only features → no skill needed, standard patterns apply
- General CSS/Tailwind questions → use Tailwind docs or `web-design-expert`
- PWA installation/service workers → use `pwa-expert` skill

## Core Principles

### Mobile-First Means Build Up, Not Down

```css
/* ❌ ANTI-PATTERN: Desktop-first (scale down) */
.card { width: 400px; }
@media (max-width: 768px) { .card { width: 100%; } }

/* ✅ CORRECT: Mobile-first (scale up) */
.card { width: 100%; }
@media (min-width: 768px) { .card { width: 400px; } }
```

### The 44px Rule

Apple's Human Interface Guidelines specify **44×44 points** as minimum touch target. Google Material suggests **48×48dp**.

```tsx
// Touch-friendly button
<button className="min-h-[44px] min-w-[44px] px-4 py-3">
  Tap me
</button>

// Touch-friendly link with adequate padding
<a href="/page" className="inline-block py-3 px-4">
  Link text
</a>
```

## Viewport Handling

### The `dvh` Solution

Mobile browsers have dynamic toolbars. `100vh` includes the URL bar, causing content to be cut off.

```css
/* ❌ ANTI-PATTERN: Content hidden behind browser UI */
.full-screen { height: 100vh; }

/* ✅ CORRECT: Responds to browser chrome */
.full-screen { height: 100dvh; }

/* Fallback for older browsers */
.full-screen {
  height: 100vh;
  height: 100dvh;
}
```

### Safe Area Insets (Notches & Home Indicators)

```css
/* Handle iPhone notch and home indicator */
.bottom-nav {
  padding-bottom: env(safe-area-inset-bottom, 0);
}

.header {
  padding-top: env(safe-area-inset-top, 0);
}

/* Full safe area padding */
.safe-container {
  padding: env(safe-area-inset-top)
           env(safe-area-inset-right)
           env(safe-area-inset-bottom)
           env(safe-area-inset-left);
}
```

**Required meta tag:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

### Tailwind Safe Area Classes

```tsx
// Custom Tailwind utilities (add to globals.css)
@layer utilities {
  .pb-safe { padding-bottom: env(safe-area-inset-bottom); }
  .pt-safe { padding-top: env(safe-area-inset-top); }
  .h-screen-safe { height: calc(100dvh - env(safe-area-inset-top) - env(safe-area-inset-bottom)); }
}

// Usage
<nav className="fixed bottom-0 pb-safe bg-leather-900">
  <BottomNav />
</nav>
```

## Mobile Navigation Patterns

### Bottom Navigation (Recommended for Mobile)

```tsx
// components/BottomNav.tsx
'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';

const navItems = [
  { href: '/', icon: HomeIcon, label: 'Home' },
  { href: '/meetings', icon: CalendarIcon, label: 'Meetings' },
  { href: '/tools', icon: ToolsIcon, label: 'Tools' },
  { href: '/my', icon: UserIcon, label: 'My Recovery' },
];

export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-leather-900 border-t border-leather-700 pb-safe">
      <div className="flex justify-around">
        {navItems.map(({ href, icon: Icon, label }) => {
          const isActive = pathname === href || pathname.startsWith(`${href}/`);
          return (
            <Link
              key={href}
              href={href}
              className={`
                flex flex-col items-center py-2 px-3 min-h-[56px] min-w-[64px]
                ${isActive ? 'text-ember-400' : 'text-leather-400'}
              `}
            >
              <Icon className="w-6 h-6" />
              <span className="text-xs mt-1">{label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
```

### Slide-Out Drawer (Side Menu)

```tsx
'use client';

import { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';

interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

export function Drawer({ isOpen, onClose, children }: DrawerProps) {
  // Prevent body scroll when open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  // Close on escape
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  if (!isOpen) return null;

  return createPortal(
    <div className="fixed inset-0 z-50">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Drawer */}
      <div
        className="absolute left-0 top-0 h-full w-[280px] max-w-[80vw]
                   bg-leather-900 shadow-xl transform transition-transform
                   animate-slide-in-left"
        role="dialog"
        aria-modal="true"
      >
        <div className="h-full overflow-y-auto pt-safe pb-safe">
          {children}
        </div>
      </div>
    </div>,
    document.body
  );
}
```

## Touch Gestures

> **Full implementations in `references/gestures.md`**

| Hook | Purpose |
|------|---------|
| `useSwipe()` | Directional swipe detection with configurable threshold |
| `usePullToRefresh()` | Pull-to-refresh with visual feedback and resistance |

**Quick usage:**

```tsx
// Swipe to dismiss
const { handleTouchStart, handleTouchEnd } = useSwipe({
  onSwipeLeft: () => dismiss(),
  threshold: 50,
});

// Pull to refresh
const { containerRef, pullDistance, isRefreshing, handlers } = 
  usePullToRefresh(async () => await refetchData());
```

## Mobile Performance

### Image Optimization

```tsx
import Image from 'next/image';

// Responsive images with proper sizing
<Image
  src="/hero.jpg"
  alt="Hero"
  fill
  sizes="(max-width: 768px) 100vw, 50vw"
  priority // For above-the-fold images
  className="object-cover"
/>

// Lazy load below-fold images
<Image
  src="/feature.jpg"
  alt="Feature"
  width={400}
  height={300}
  loading="lazy"
/>
```

### Reduce Bundle Size

```tsx
// Dynamic imports for heavy components
const HeavyChart = dynamic(() => import('@/components/Chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false, // Skip server render for client-only
});

// Lazy load below-fold sections
const Comments = dynamic(() => import('@/components/Comments'));
```

### Skeleton Screens (Not Spinners)

```tsx
// Skeleton that matches final content layout
function MeetingCardSkeleton() {
  return (
    <div className="p-4 bg-leather-800 rounded-lg animate-pulse">
      <div className="h-4 bg-leather-700 rounded w-3/4 mb-2" />
      <div className="h-3 bg-leather-700 rounded w-1/2 mb-4" />
      <div className="flex gap-2">
        <div className="h-6 w-16 bg-leather-700 rounded" />
        <div className="h-6 w-16 bg-leather-700 rounded" />
      </div>
    </div>
  );
}

// Usage
{isLoading ? (
  <div className="space-y-4">
    {[...Array(5)].map((_, i) => <MeetingCardSkeleton key={i} />)}
  </div>
) : (
  meetings.map(m => <MeetingCard key={m.id} meeting={m} />)
)}
```

## Responsive Patterns

### Tailwind Breakpoint Strategy

```
sm: 640px   - Large phones (landscape)
md: 768px   - Tablets
lg: 1024px  - Small laptops
xl: 1280px  - Desktops
2xl: 1536px - Large screens
```

```tsx
// Mobile: stack, Tablet+: side-by-side
<div className="flex flex-col md:flex-row gap-4">
  <aside className="w-full md:w-64">Sidebar</aside>
  <main className="flex-1">Content</main>
</div>

// Mobile: bottom nav, Desktop: sidebar
<nav className="md:hidden fixed bottom-0 left-0 right-0">
  <BottomNav />
</nav>
<aside className="hidden md:block w-64">
  <SidebarNav />
</aside>
```

### Container Queries (CSS-only Responsive Components)

```css
/* Component responds to its container, not viewport */
@container (min-width: 400px) {
  .card { flex-direction: row; }
}
```

```tsx
<div className="@container">
  <div className="flex flex-col @md:flex-row">
    {/* Responds to parent container width */}
  </div>
</div>
```

## Testing on Real Devices

### Chrome DevTools Mobile Emulation
1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select device or set custom dimensions
4. **Throttle network/CPU** for realistic performance

### Must-Test Scenarios
- [ ] Content doesn't get cut off by notch/home indicator
- [ ] Touch targets are at least 44×44px
- [ ] Scrolling is smooth (no jank)
- [ ] Bottom nav doesn't block content
- [ ] Forms work with virtual keyboard visible
- [ ] Landscape orientation works
- [ ] Pull-to-refresh doesn't fight with scroll

### BrowserStack/Real Device Testing
```bash
# Expose local dev server to internet
npx localtunnel --port 3000
# or
ngrok http 3000
```

## Quick Reference

| Issue | Solution |
|-------|----------|
| Content cut off at bottom | Use `100dvh` instead of `100vh` |
| Notch overlaps content | Add `pt-safe` / `pb-safe` |
| Touch targets too small | Min 44×44px |
| Scroll locked | Check `overflow: hidden` on body |
| Keyboard covers input | Use `visualViewport` API |
| Janky scrolling | Use `will-change: transform` |
| Double-tap zoom | Add `touch-action: manipulation` |

## References

See `/references/` for detailed guides:
- `keyboard-handling.md` - Virtual keyboard and form UX
- `animations.md` - Touch-friendly animations
- `accessibility.md` - Mobile a11y requirements
