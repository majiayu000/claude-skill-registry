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

> **⚠️ TREIDO PROJECT:** This project uses **Tailwind v4** with CSS variables.
> Use `min-h-(--spacing-touch-md)` NOT `min-h-[44px]`.
> See [globals.css](app/globals.css) for all tokens.

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

---

## 🎯 TREIDO PROJECT: Tailwind v4 Token Syntax

**This project uses Tailwind v4 with CSS variables.** Do NOT use arbitrary values.

### Touch Target Tokens (from globals.css)

```css
--spacing-touch-xs: 2rem;      /* 32px - minimum WCAG */
--spacing-touch-sm: 2.25rem;   /* 36px - compact */
--spacing-touch: 2.5rem;       /* 40px - default */
--spacing-touch-md: 2.75rem;   /* 44px - Apple minimum */
--spacing-touch-lg: 3rem;      /* 48px - bottom nav */
```

### Correct Tailwind v4 Syntax

```tsx
// ❌ WRONG - Arbitrary values (v3/generic style)
<button className="min-h-[44px] min-w-[44px] px-4 py-3">

// ✅ CORRECT - Tailwind v4 CSS variable syntax
<button className="min-h-(--spacing-touch-md) px-4 py-3">

// For square touch targets
<button className="size-(--spacing-touch-md)">
```

### Treido-Specific Patterns

| Component | Token | Class |
|-----------|-------|-------|
| Bottom nav items | 48px | `h-(--spacing-touch-lg)` |
| Header icons | 44px | `size-(--spacing-touch-md)` |
| Buttons | 44px | `h-(--spacing-button)` |
| Small buttons | 36px | `h-(--spacing-button-sm)` |
| Input fields | 44px | `h-(--spacing-input)` |
| Category pills | 40px | `min-h-(--spacing-touch)` |
| Compact list items | 36px | `min-h-(--spacing-touch-sm)` |

### Full Touch-Friendly Example

```tsx
// Touch-friendly button with proper tokens
<button 
  className="
    min-h-(--spacing-touch-md) 
    min-w-(--spacing-touch-md)
    px-4 
    rounded-lg
    active:opacity-80
    transition-opacity
  "
>
  Tap me
</button>

// Touch-friendly link with padding
<Link 
  href="/page" 
  className="inline-flex items-center min-h-(--spacing-touch-md) px-4"
>
  Link text
</Link>
```

---

### Generic Reference (Non-Treido Projects)

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
// components/BottomNav.tsx - Treido Pattern
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
    <nav className="fixed bottom-0 left-0 right-0 bg-background border-t border-border pb-safe">
      <div className="flex justify-around">
        {navItems.map(({ href, icon: Icon, label }) => {
          const isActive = pathname === href || pathname.startsWith(`${href}/`);
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex flex-col items-center justify-center",
                "h-(--spacing-touch-lg)",           // 48px height
                "min-w-(--spacing-touch-lg)",       // 48px min width
                "px-3",
                "active:opacity-80 transition-opacity",
                isActive ? 'text-primary' : 'text-muted-foreground'
              )}
            >
              <Icon className="size-(--size-icon)" /> {/* 24px icon */}
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
        className="absolute inset-0 bg-overlay-dark backdrop-blur-sm"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Drawer - Use Treido token for width */}
      <div
        className="
          absolute left-0 top-0 h-full 
          w-(--width-sheet-mobile)
          bg-background shadow-xl 
          transform transition-transform
          animate-slide-in-left
        "
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

**Note:** Treido uses vaul Drawer component from `components/ui/drawer.tsx` for production.

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
// Skeleton that matches final content layout - Treido pattern
function MeetingCardSkeleton() {
  return (
    <div className="p-4 bg-muted rounded-lg animate-pulse">
      <div className="h-4 bg-muted-foreground/20 rounded w-3/4 mb-2" />
      <div className="h-3 bg-muted-foreground/20 rounded w-1/2 mb-4" />
      <div className="flex gap-2">
        <div className="h-6 w-16 bg-muted-foreground/20 rounded" />
        <div className="h-6 w-16 bg-muted-foreground/20 rounded" />
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

**Note:** Treido uses `components/ui/skeleton.tsx` for production skeletons.

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

// Treido pattern: Mobile-only vs Desktop-only
<nav className="md:hidden fixed bottom-0 left-0 right-0">
  <BottomNav />
</nav>
<aside className="hidden md:flex w-(--layout-sidebar-w)">
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

| Issue | Solution (Treido Tailwind v4) |
|-------|-------------------------------|
| Content cut off at bottom | Use `min-h-dvh` (not `100vh`) |
| Notch overlaps content | Add `pt-safe` / `pb-safe` |
| Touch targets too small | `min-h-(--spacing-touch-md)` (44px) |
| Bottom nav height | `h-(--spacing-touch-lg)` (48px) |
| Scroll locked | Check `overflow: hidden` on body |
| Keyboard covers input | Use `visualViewport` API |
| Janky scrolling | Use `will-change: transform` |
| Double-tap zoom | Add `touch-action: manipulation` |
| Icon sizing | `size-(--size-icon)` (24px) |
| Button height | `h-(--spacing-button)` (44px) |

## References

See `/references/` for detailed guides:
- `keyboard-handling.md` - Virtual keyboard and form UX
- `animations.md` - Touch-friendly animations
- `accessibility.md` - Mobile a11y requirements
