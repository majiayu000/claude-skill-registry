---
name: smooth-scroll
description: Add smooth scrolling for same-page anchor links only. Uses JavaScript to handle #anchor clicks while page navigations remain instant. Add to layout once, works across all pages.
---

# Smooth Scroll

Enable smooth scrolling for same-page anchor links only. Page navigations always start at the top instantly.

## Important: Why JavaScript Instead of CSS

CSS `scroll-behavior: smooth` affects ALL scrolling, including Next.js page navigations. This causes unwanted smooth scrolling when changing pages.

**Our approach:** Use JavaScript to handle only `#anchor` link clicks with smooth scroll. Page navigations use browser default (instant to top).

## Workflow

1. **Create SmoothScroll Component** - JavaScript handler for anchor links
2. **Add to Layout** - Include component in locale layout
3. **Update globals.css** - Keep only `scroll-padding-top`, remove `scroll-behavior`
4. **Test** - Verify anchor links smooth scroll, page changes are instant

## Implementation

### Step 1: Create SmoothScroll Component

Create `website/components/ui/smooth-scroll.tsx`:

```tsx
"use client";

import { useEffect } from "react";

export function SmoothScroll() {
  useEffect(() => {
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    const handleClick = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      const anchor = target.closest('a[href^="#"]');

      if (anchor) {
        const href = anchor.getAttribute("href");
        if (href && href.startsWith("#") && href.length > 1) {
          const element = document.querySelector(href);
          if (element) {
            e.preventDefault();
            element.scrollIntoView({
              behavior: prefersReducedMotion ? "auto" : "smooth",
            });
          }
        }
      }
    };

    document.addEventListener("click", handleClick);
    return () => document.removeEventListener("click", handleClick);
  }, []);

  return null;
}
```

### Step 2: Add to Layout

Add SmoothScroll to `app/[locale]/layout.tsx`:

```tsx
import { SmoothScroll } from "@/components/ui/smooth-scroll";

export default function LocaleLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <SmoothScroll />
      {/* rest of layout */}
    </>
  );
}
```

### Step 3: Update globals.css

Ensure globals.css has scroll-padding but NOT scroll-behavior:

```css
@layer base {
    html {
        /* Smooth scroll handled by JS for anchor links only */
        scroll-padding-top: 5rem; /* Offset for fixed navbar */
    }
}
```

**DO NOT add `scroll-behavior: smooth`** - this causes page navigation issues.

## Same-Page Anchor Links

For links that scroll to sections on the same page, use the `#` anchor format:

```tsx
// In navbar or any component
<Link href="#pricing">Pricing</Link>
<Link href="#faq">FAQ</Link>
<Link href="#contact">Contact</Link>

// Target sections need matching IDs
<section id="pricing">...</section>
<section id="faq">...</section>
<section id="contact">...</section>
```

### Adding Section IDs

Each section that should be a scroll target needs an `id` attribute:

```tsx
// Before
<section className="py-16 lg:py-24">

// After
<section id="features" className="py-16 lg:py-24">
```

### Common Section IDs

| Section | ID |
|---------|-----|
| Hero | `hero` |
| Features | `features` |
| Pricing | `pricing` |
| FAQ | `faq` |
| Contact | `contact` |
| About | `about` |
| Portfolio/Projects | `projects` |
| Testimonials | `testimonials` |

## Scroll Offset for Fixed Navbar

The `scroll-padding-top` in globals.css handles the offset:

```css
html {
    scroll-padding-top: 5rem; /* Adjust based on navbar height */
}
```

This is respected by `scrollIntoView()`.

## Behavior Summary

| Action | Scroll Behavior |
|--------|----------------|
| Click `#anchor` link | Smooth scroll to section |
| Navigate to new page | Instant to top (no animation) |
| Browser back/forward | Browser default |
| Reduced motion user | Instant scroll |

## Checklist

- [ ] `SmoothScroll` component created at `components/ui/smooth-scroll.tsx`
- [ ] Component added to `app/[locale]/layout.tsx`
- [ ] `scroll-padding-top` set in globals.css
- [ ] NO `scroll-behavior: smooth` in globals.css
- [ ] Section IDs added to scrollable targets
- [ ] Test: clicking `#anchor` link scrolls smoothly
- [ ] Test: navigating to new page is instant (no scroll animation)
- [ ] Test: reduced motion preference disables smooth scroll

## Output

After running this skill:
- `components/ui/smooth-scroll.tsx` - Anchor link handler
- `app/[locale]/layout.tsx` - Updated with SmoothScroll
- `globals.css` - Only scroll-padding-top, no scroll-behavior
