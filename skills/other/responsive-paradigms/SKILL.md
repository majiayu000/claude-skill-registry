---
name: responsive-paradigms
description: Mobile, tablet, and desktop are different interaction paradigms — not the same layout scaled up or down. Sections can be hidden, repositioned, or made sticky on mobile. Navigation and primary actions move. Use when designing responsive layouts, adapting desktop UI for mobile, or deciding what to show on each breakpoint.
metadata:
  priority: 8
  pathPatterns:
    - "**/*.css"
    - "**/*.scss"
    - "**/*.tsx"
    - "**/*.jsx"
    - "tailwind.config.*"
    - "design-system/**"
    - "components/**"
  promptSignals:
    phrases:
      - "responsive"
      - "mobile"
      - "tablet"
      - "breakpoint"
      - "desktop"
      - "adaptive"
      - "bottom nav"
      - "hamburger"
      - "touch"
retrieval:
  aliases:
    - responsive design
    - mobile layout
    - tablet layout
    - breakpoints
    - adaptive UI
    - bottom navigation
    - mobile navigation
  intents:
    - design for mobile
    - adapt desktop layout to mobile
    - decide what to show on each breakpoint
    - design mobile navigation
    - handle layout changes at breakpoints
  examples:
    - how should this sidebar behave on mobile
    - design the mobile version of this dashboard
    - what changes between desktop and mobile for this layout
---

# Responsive Paradigms

Mobile, tablet, and desktop are fundamentally different interaction contexts. The input method, screen real estate, viewing distance, and session intent all differ. Responsive design is not the same layout at different widths — it is a different design decision at each breakpoint.

## The Three Paradigms

### Mobile (< 768px)
- **Input:** Touch — fingers, not a cursor. Tap targets ≥ 44×44px.
- **Navigation:** Bottom tab bar (thumb reachable) or hamburger drawer. Top navigation is hard to reach.
- **Session:** Often interrupted, task-focused, shorter. Show the most important thing first.
- **Content:** Single column. Vertical scroll only. No hover states.
- **Primary action:** Floating action button (FAB) or full-width button at the bottom of the screen.

### Tablet (768px–1024px)
- **Input:** Touch and sometimes keyboard/trackpad. Hybrid paradigm.
- **Navigation:** Can support a persistent sidebar at landscape orientation; collapses to drawer at portrait.
- **Content:** Two-column layouts work. Master-detail patterns (list + detail side by side) are natural.
- **Primary action:** Can be in-line with content, not necessarily floating.

### Desktop (> 1024px)
- **Input:** Mouse with hover states, keyboard shortcuts, precise clicking.
- **Navigation:** Persistent sidebar or top navigation. Both visible simultaneously.
- **Content:** Multi-column, dense information, toolbars, context menus.
- **Primary action:** In-context with content, supported by keyboard shortcuts for power users.

---

## Section Behaviour Across Breakpoints

Not every section needs to appear on every breakpoint at the same position — or at all.

### Sections can be hidden on mobile
Secondary content (related articles, supplementary sidebars, decorative illustrations) can be hidden below a breakpoint. Ask: does a mobile user need this? If no, `display: none` at mobile is correct.

### Sections can be repositioned
A sidebar that sits to the left on desktop logically moves below the main content on mobile, or collapses into an expandable section.

```
Desktop:              Mobile:
[Main] [Sidebar]  →   [Main]
                       [▼ Related]  ← collapsed accordion
```

### Sticky behaviour can change per breakpoint
An element that is `position: sticky` on desktop may need to become a fixed bottom bar on mobile, or be removed from sticky positioning entirely to free up screen space.

```css
.toolbar {
  position: static; /* mobile: inline, not sticky */
}

@media (min-width: 1024px) {
  .toolbar {
    position: sticky;
    top: var(--header-height);
  }
}
```

### Navigation transforms completely
| Desktop | Mobile |
|---|---|
| Persistent top nav or sidebar | Bottom tab bar or hamburger drawer |
| Visible labels + icons | Icons only (bottom nav) or full list (drawer) |
| Hover states on nav items | None — touch only |
| Dropdowns on hover | Tap to expand, full-screen or sheet |

---

## Mobile-First Approach

Design and build mobile first, then enhance for larger screens. Mobile forces prioritisation — what makes it onto mobile is what actually matters.

```css
/* Mobile first: base styles are mobile */
.container { padding: var(--space-4); }

/* Enhance for larger screens */
@media (min-width: 768px) {
  .container { padding: var(--space-8); }
}

@media (min-width: 1024px) {
  .container {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: var(--space-8);
  }
}

/* Ultra-wide protection */
@media (min-width: 1600px) {
  .container {
    max-width: 1440px;
    margin-left: auto;
    margin-right: auto;
  }
}
```

## Max-Width and Ultra-Wide Screens

Responsive design doesn't mean "expand forever." On very large monitors (2K, 4K, and ultra-wide), content must be capped to maintain readability and ergonomic comfort.

- **Ergonomics:** Spreading critical UI elements across the full width of a 4K screen requires excessive neck movement and makes the interface feel "fragmented."
- **Readability:** As noted in typography guidelines, line lengths should not exceed ~75 characters. On a 4K screen without a max-width, a single line of text could span thousands of pixels.
- **The "Safe Zone":** Use a max-width container (typically between **1280px and 1600px**) for all primary content.
- **Full-Bleed Exceptions:** Background colours, decorative images, and secondary footers can remain full-width to maintain the design's "energy" while the content remains centered and contained.

## Review Checklist

- [ ] Does mobile navigation use a bottom tab bar or drawer — not a top nav that requires thumb stretching?
- [ ] Are touch targets ≥ 44×44px on all interactive elements?
- [ ] Are secondary sections hidden or collapsed on mobile rather than just shrunk?
- [ ] Does sticky positioning adapt per breakpoint — not every sticky desktop element stays sticky on mobile?
- [ ] Is the layout built mobile-first with progressive enhancement upward?
- [ ] Are hover-dependent interactions (tooltips, dropdowns) replaced with tap equivalents on touch?
- [ ] Does the primary action remain reachable with one thumb on mobile?
- [ ] Is the primary content capped with a max-width (e.g., 1440px) on ultra-wide/4K monitors?
