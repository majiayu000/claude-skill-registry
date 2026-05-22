---
name: modern-css
description: Proactively apply when creating design systems, component libraries, or any frontend application. Triggers on CSS Grid, Subgrid, Flexbox, Container Queries, :has(), @layer, @scope, CSS nesting, @property, @function, if(), oklch, color-mix, light-dark, relative color, @starting-style, scroll-driven animations, view transitions, anchor positioning, popover, customizable select, content-visibility, logical properties, text-wrap, interpolate-size, clamp, field-sizing, modern CSS, CSS architecture, responsive design, dark mode, theming, design tokens, cascade layers. Use when writing CSS for any web project, choosing layout approaches, building responsive components, implementing dark mode or theming, creating animations or transitions, styling form elements, or modernizing legacy stylesheets. Modern CSS features and best practices for building interfaces with pure native CSS.
---

# Modern CSS

Pure native CSS for building interfaces — no preprocessors, no frameworks.

## When to Use (and When NOT to)

| Use Freely (Baseline) | Feature-Detect First |
|---|---|
| CSS Grid, Subgrid, Flexbox | `@function`, `if()` (Chrome-only) |
| Container Queries (size + style) | Customizable `<select>` (Chrome-only) |
| `:has()`, `:is()`, `:where()` | Scroll-state queries (Chrome-only) |
| CSS Nesting, `@layer`, `@scope` | `sibling-index()`, `sibling-count()` |
| `@property` (typed custom props) | `::scroll-button()`, `::scroll-marker` |
| `oklch()`, `color-mix()`, `light-dark()` | Typed `attr()` beyond `content` |
| Relative color syntax | `field-sizing: content` |
| `@starting-style`, `transition-behavior` | `interpolate-size` (Chrome-only) |
| Scroll-driven animations | Grid Lanes / masonry (experimental) |
| Anchor positioning, Popover API | `random()` (Safari TP only) |
| `text-wrap: balance`, `linear()` easing | `@mixin` / `@apply` (no browser yet) |
| View Transitions, logical properties | |

## CRITICAL: The Modern Cascade

Understanding how styles resolve is the single most important concept in CSS. The additions of `@layer` and `@scope` fundamentally changed the cascade algorithm.

```
Style Resolution Order (highest priority wins):
┌─────────────────────────────────────────────────┐
│ 1. Transitions (active transition wins)         │
│ 2. !important (user-agent > user > author)      │
│ 3. @layer order (later layer > earlier layer)   │
│ 4. Unlayered styles (beat ALL layers)           │
│ 5. Specificity (ID > class > element)           │
│ 6. @scope proximity (closer root wins)      NEW │
│ 7. Source order (later > earlier)               │
└─────────────────────────────────────────────────┘

Unlayered > Last layer > ... > First layer
           (utilities)        (reset)
```

Cascade layers (`@layer`) and scope proximity (`@scope`) are now more powerful than selector specificity. Define your layer order once (`@layer reset, base, components, utilities;`) and specificity wars disappear. Unlayered styles always beat layered styles — use this for overrides.

## Quick Decision Trees

### "How do I lay this out?"

```
Layout approach?
├─ 2D grid (rows + columns)         → CSS Grid
│  ├─ Children must align across    → Grid + Subgrid
│  └─ Waterfall / masonry           → grid-lanes (experimental)
├─ 1D row OR column                 → Flexbox
├─ Component adapts to container    → Container Query + Grid/Flex
├─ Viewport-based responsiveness    → @media range syntax
└─ Element sized to content         → fit-content / min-content / stretch
```

### "How do I style this state?"

```
Style based on what?
├─ Child/descendant presence        → :has()
├─ Container size                   → @container (inline-size)
├─ Container custom property        → @container style()
├─ Scroll position (stuck/snapped)  → scroll-state() query
├─ Element's own custom property    → if(style(...))
├─ Browser feature support          → @supports
├─ User preference (motion/color)   → @media (prefers-*)
└─ Multiple selectors efficiently   → :is() / :where()
```

### "How do I animate this?"

```
Animation type?
├─ Enter/appear on DOM              → @starting-style + transition
├─ Exit/disappear (display:none)    → transition-behavior: allow-discrete
├─ Animate to/from auto height      → interpolate-size: allow-keywords
├─ Scroll-linked (parallax/reveal)  → animation-timeline: scroll()/view()
├─ Page/view navigation             → View Transitions API
├─ Custom easing (bounce/spring)    → linear() function
└─ Always: respect user preference  → @media (prefers-reduced-motion)
```

## What CSS Replaced JavaScript For

| JavaScript Pattern | CSS Replacement |
|---|---|
| Scroll position listeners | Scroll-driven animations |
| IntersectionObserver for reveal | `animation-timeline: view()` |
| Sticky header shadow toggle | `scroll-state(stuck: top)` |
| Floating UI / Popper.js | Anchor positioning |
| Carousel prev/next/dots | `::scroll-button()`, `::scroll-marker` |
| Auto-expanding textarea | `field-sizing: content` |
| Staggered animation delays | `sibling-index()` |
| `max-height: 9999px` hack | `interpolate-size: allow-keywords` |
| Parent element selection | `:has()` |
| Theme toggle logic | `light-dark()` + `color-scheme` |
| Tooltip/popover show/hide | Popover API + invoker commands |
| Color manipulation functions | `color-mix()`, relative color syntax |

> For non-Baseline features, always feature-detect with `@supports` or use progressive enhancement. Check [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS) or [Baseline](https://web.dev/baseline) for current browser support.

## Anti-Patterns (CRITICAL)

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Overusing `!important` | Specificity arms race | Use `@layer` for cascade control |
| Deep nesting (`.a .b .c .d`) | Fragile, DOM-coupled | Flat selectors, `@scope` |
| IDs for styling (`#header`) | Too specific to override | Classes (`.header`) |
| `@media` for component layout | Viewport-coupled, not reusable | Container queries |
| JS scroll listeners for effects | Janky, expensive | Scroll-driven animations |
| JS for tooltip positioning | Floating UI dependency | Anchor positioning |
| JS for carousel controls | Fragile, a11y issues | `::scroll-button`, `::scroll-marker` |
| JS for auto-expanding textarea | Unnecessary complexity | `field-sizing: content` |
| `max-height: 9999px` for animation | Wrong duration, janky | `interpolate-size: allow-keywords` |
| `margin-left` / `padding-right` | Breaks in RTL/vertical | Logical properties (`margin-inline-start`) |
| `rgba()` with commas | Legacy syntax | `rgb(r g b / a)` space-separated |
| `appearance: none` on selects | Removes ALL functionality | `appearance: base-select` |
| Preprocessor-only variables | Can't change at runtime | CSS custom properties |
| Preprocessor-only nesting | Extra build step dependency | Native CSS nesting |
| Preprocessor color functions | Can't respond to context | `color-mix()`, relative colors |
| `text-wrap: balance` on paragraphs | Performance-heavy | Only headings/short text |
| `content-visibility` above fold | Delays LCP rendering | Only off-screen sections |
| Overusing `will-change` | Wastes GPU memory | Apply only to animating elements |

## Reference Documentation

| File | Purpose |
|------|---------|
| [references/CASCADE.md](references/CASCADE.md) | Nesting, `@layer`, `@scope`, cascade control, and CSS architecture |
| [references/LAYOUT.md](references/LAYOUT.md) | Grid, Subgrid, Flexbox, Container Queries, and intrinsic sizing |
| [references/SELECTORS.md](references/SELECTORS.md) | `:has()`, `:is()`, `:where()`, pseudo-elements, and state-based selection |
| [references/COLOR.md](references/COLOR.md) | OKLCH, `color-mix()`, relative colors, `light-dark()`, and theming |
| [references/TOKENS.md](references/TOKENS.md) | `@property`, `@function`, `if()`, math functions, and design tokens |
| [references/ANIMATION.md](references/ANIMATION.md) | `@starting-style`, `interpolate-size`, `linear()`, view transitions |
| [references/SCROLL.md](references/SCROLL.md) | Scroll-driven animations, scroll-state queries, native carousels |
| [references/COMPONENTS.md](references/COMPONENTS.md) | Customizable `<select>`, popover, anchor positioning, `field-sizing` |
| [references/PERFORMANCE.md](references/PERFORMANCE.md) | `content-visibility`, typography, logical properties, accessibility |
| [references/CHEATSHEET.md](references/CHEATSHEET.md) | Quick reference: browser support, legacy→modern patterns, units |

## Sources

### Official Specifications
- [CSS Snapshot 2025](https://www.w3.org/TR/css-2025/) — W3C
- [CSS Values and Units Level 5](https://www.w3.org/TR/css-values-5/) — `if()`, `random()`, `sibling-index/count()`
- [CSS Functions and Mixins Level 1](https://www.w3.org/TR/css-mixins-1/) — `@function`, `@mixin`
- [CSS Conditional Rules Level 5](https://www.w3.org/TR/css-conditional-5/) — Scroll-state queries
- [CSS Anchor Positioning](https://www.w3.org/TR/css-anchor-position-1/)
- [CSS Overflow Level 5](https://www.w3.org/TR/css-overflow-5/) — Scroll markers/buttons

### Browser Vendor Blogs
- [CSS Wrapped 2025](https://chrome.dev/css-wrapped-2025/) — Chrome DevRel
- [Interop 2025](https://webkit.org/blog/17808/interop-2025-review/) — WebKit
- [What's New in Web UI (I/O 2025)](https://developer.chrome.com/blog/new-in-web-ui-io-2025-recap)

### Reference
- [MDN Web Docs: CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [State of CSS 2025](https://2025.stateofcss.com/en-US/features/)
- [What You Need to Know About Modern CSS (2025)](https://frontendmasters.com/blog/what-you-need-to-know-about-modern-css-2025-edition/)
- [CSS in 2026](https://blog.logrocket.com/css-in-2026/)
