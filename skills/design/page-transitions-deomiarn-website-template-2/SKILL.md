---
name: page-transitions
description: Add elegant page transition overlay using 3 staggered color layers. Overlay covers screen during navigation and reveals once new page is loaded. Use during /init or standalone.
---

# Page Transitions

Add an elegant overlay transition with 3 staggered layers. The overlay covers the screen during navigation and only reveals once the new page is fully loaded.

## Prerequisites

- Framer Motion installed (already in project)
- Next.js App Router

## Workflow

1. **Create PageTransition Component** - Create `components/ui/page-transition.tsx`
2. **Update Layout** - Add PageTransition to locale layout (renders above content)
3. **Test Navigation** - Verify overlay stays until page loads
4. **Accessibility** - Ensure reduced-motion preference is respected

## Implementation

### Step 1: Create PageTransition Component

Create `website/components/ui/page-transition.tsx`:

```tsx
"use client";

import { motion, AnimatePresence } from "framer-motion";
import { usePathname } from "next/navigation";
import { useEffect, useState, useRef } from "react";

export function PageTransition() {
  const pathname = usePathname();
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [showOverlay, setShowOverlay] = useState(false);
  const previousPathname = useRef(pathname);

  // 3 layers with staggered delays - solid colors
  const layers = [
    { bg: "bg-muted", delay: 0 },
    { bg: "bg-muted/95", delay: 0.08 },
    { bg: "bg-muted/90", delay: 0.16 },
  ];

  const transitionDuration = 0.4;
  const totalEnterTime = (transitionDuration + 0.16) * 1000; // duration + max delay

  useEffect(() => {
    // When pathname changes, start the transition
    if (pathname !== previousPathname.current) {
      setIsTransitioning(true);
      setShowOverlay(true);

      // Wait for enter animation to complete, then start exit
      const exitTimer = setTimeout(() => {
        setIsTransitioning(false);
        previousPathname.current = pathname;
      }, totalEnterTime + 100); // Small buffer for page render

      // Hide overlay after exit animation completes
      const hideTimer = setTimeout(() => {
        setShowOverlay(false);
      }, totalEnterTime + 100 + (transitionDuration + 0.16) * 1000);

      return () => {
        clearTimeout(exitTimer);
        clearTimeout(hideTimer);
      };
    }
  }, [pathname, totalEnterTime]);

  if (!showOverlay) return null;

  return (
    <div className="pointer-events-none">
      {layers.map((layer, index) => (
        <motion.div
          key={index}
          className={`fixed inset-0 z-[999] ${layer.bg}`}
          initial={{ scaleX: 0 }}
          animate={{ scaleX: isTransitioning ? 1 : 0 }}
          transition={{
            duration: transitionDuration,
            delay: layer.delay,
            ease: [0.4, 0, 0.2, 1],
          }}
          style={{
            originX: isTransitioning ? 0 : 1,
            transformOrigin: isTransitioning ? "left" : "right",
          }}
        />
      ))}
    </div>
  );
}
```

### Step 2: Update Locale Layout

Add PageTransition to `app/[locale]/layout.tsx` - it renders as an overlay, not wrapping content:

```tsx
import { PageTransition } from "@/components/ui/page-transition";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";

export default function LocaleLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <PageTransition />
      <Navbar />
      <main>{children}</main>
      <Footer />
    </>
  );
}
```

**Important:**
- PageTransition is a sibling, NOT a wrapper
- Uses `fixed` positioning with `z-[999]` to overlay everything including modals
- `pointer-events-none` ensures it doesn't block interactions

### Step 3: Accessibility

Add reduced motion support to globals.css:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## How It Works

1. **Navigation detected:** When pathname changes, overlay starts sliding in from left
2. **Cover screen:** All 3 layers animate to full width with staggered timing
3. **Wait for page:** Overlay stays fullscreen while new page renders underneath
4. **Reveal:** Once ready, layers slide out to the right, revealing new page
5. **Cleanup:** Overlay unmounts after exit animation completes

The key difference from basic transitions: **the overlay waits at fullscreen state** until the page is ready, then reveals.

## Configuration Options

### Layer Colors

Adjust the `bg` values for different looks:

```tsx
// Default - solid muted with subtle variations
const layers = [
  { bg: "bg-muted", delay: 0 },
  { bg: "bg-muted/95", delay: 0.08 },
  { bg: "bg-muted/90", delay: 0.16 },
];

// Primary accent
const layers = [
  { bg: "bg-primary", delay: 0 },
  { bg: "bg-primary/95", delay: 0.08 },
  { bg: "bg-primary/90", delay: 0.16 },
];

// Secondary
const layers = [
  { bg: "bg-secondary", delay: 0 },
  { bg: "bg-secondary/95", delay: 0.08 },
  { bg: "bg-secondary/90", delay: 0.16 },
];
```

### Timing

```tsx
// Faster (snappy)
const transitionDuration = 0.3;
delays: [0, 0.06, 0.12]

// Default (balanced)
const transitionDuration = 0.4;
delays: [0, 0.08, 0.16]

// Slower (cinematic)
const transitionDuration = 0.5;
delays: [0, 0.1, 0.2]
```

## Performance Notes

1. **GPU Acceleration:** `transform: scaleX()` is GPU-accelerated
2. **Fixed positioning:** Layers don't affect document flow
3. **Pointer events:** Disabled to prevent blocking interactions
4. **Z-index 999:** High enough to overlay everything including modals and navbars
5. **Conditional render:** Overlay unmounts when not needed

## What This Skill Does NOT Do

- Move or animate the actual page content
- Add loading spinners (overlay IS the loading indicator)
- Handle failed navigations

## Checklist

- [ ] PageTransition component created at `components/ui/page-transition.tsx`
- [ ] `app/[locale]/layout.tsx` includes PageTransition as sibling (not wrapper)
- [ ] PageTransition uses `fixed inset-0 z-[999]`
- [ ] Test: Navigate between pages, see layers slide in from left
- [ ] Test: Overlay stays fullscreen briefly while page loads
- [ ] Test: Layers slide out to right, revealing new page
- [ ] Test: No interaction blocking (pointer-events-none)
- [ ] Test: Reduced motion preference disables animation

## Output

- `components/ui/page-transition.tsx` - Overlay transition component
- `app/[locale]/layout.tsx` - Updated with transition
- Elegant 3-layer curtain transition that waits for page load
