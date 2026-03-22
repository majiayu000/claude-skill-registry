---
name: html-css-guide
description: |
  HTML and CSS guardrails, patterns, and best practices for AI-assisted development.
  Use when working with HTML/CSS files (.html, .css, .scss, .less), or when the user mentions HTML/CSS.
  Provides semantic HTML guidelines, accessibility standards, modern CSS patterns,
  and responsive design conventions specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: html-css
  extensions: ".html,.htm,.css,.scss,.less,.sass"
---

# HTML/CSS Guide

> Applies to: HTML5, CSS3, SCSS/LESS, Responsive Design, WCAG 2.1 AA

## Core Principles

1. **Semantic First**: Use HTML elements for their meaning, not their appearance; style with CSS
2. **Accessible by Default**: Every page must be navigable by keyboard, screen reader, and assistive technology
3. **Progressive Enhancement**: Build a solid HTML foundation, then layer on CSS and JavaScript
4. **Mobile First**: Design for the smallest viewport, then enhance with `min-width` media queries
5. **Performance Budget**: Minimize render-blocking resources; prefer system fonts, modern image formats, and critical CSS inlining

## Guardrails

### Semantic HTML

- Use `<main>` once per page; `<header>`, `<footer>`, `<nav>`, `<aside>` for landmarks
- Use `<article>` for self-contained content; `<section>` for thematic groups with a heading
- Use `<figure>`/`<figcaption>` for captioned media; `<time datetime="...">` for dates
- Headings (`<h1>`-`<h6>`) must follow a logical outline; never skip levels for styling
- Use `<button>` for actions and `<a>` for navigation; never `<div onclick>`
- Lists (`<ul>`, `<ol>`, `<dl>`) for groups of related items; not `<div>` sequences

```html
<article>
  <header>
    <h2>Deploying with Zero Downtime</h2>
    <time datetime="2025-03-15">March 15, 2025</time>
  </header>
  <section aria-labelledby="prereqs">
    <h3 id="prereqs">Prerequisites</h3>
    <ul>
      <li>Container runtime (Docker or Podman)</li>
      <li>Load balancer with health checks</li>
    </ul>
  </section>
</article>
```

### Accessibility (WCAG 2.1 AA)

- Every `<img>` must have `alt`; decorative images use `alt=""`
- All form inputs must have associated `<label>` elements (use `for`/`id`)
- Color contrast: 4.5:1 for normal text, 3:1 for large text (18px+ bold or 24px+)
- Focus indicators must be visible; never `outline: none` without a replacement
- Skip-to-content link as the first focusable element on every page
- All interactive elements must be keyboard-operable
- Use `aria-live="polite"` for dynamic updates; `role="alert"` for immediate announcements
- Use `aria-expanded`, `aria-controls`, `aria-haspopup` for disclosure widgets
- Do not rely on color alone to convey information (add icons, text, or patterns)

```html
<a href="#main" class="skip-link">Skip to main content</a>

<form aria-labelledby="signup-heading">
  <h2 id="signup-heading">Create Account</h2>
  <label for="email">Email</label>
  <input id="email" type="email" required autocomplete="email"
         aria-describedby="email-hint" />
  <p id="email-hint" class="hint">We will never share your email.</p>
  <button type="submit">Create Account</button>
</form>
```

### CSS Architecture

- One component per file; file name matches component (`card.css`, `nav.css`)
- Use `@layer` for specificity control: reset, base, layout, components, utilities
- Prefer BEM (`.block__element--modifier`) or utility-first -- pick one, stay consistent
- Never use `!important` outside utility overrides; fix specificity instead
- Max 3 levels of nesting (native or preprocessor)
- Custom properties for all theme values (colors, spacing, typography, radii)
- No inline styles unless dynamically computed by JavaScript

```css
@layer reset, base, layout, components, utilities;

@layer base {
  :root {
    --color-primary: oklch(55% 0.22 265);
    --color-surface: oklch(98% 0.005 265);
    --color-text: oklch(20% 0.02 265);
    --space-sm: 0.5rem;
    --space-md: 1rem;
    --space-lg: 2rem;
    --radius-md: 0.5rem;
    --font-body: system-ui, -apple-system, sans-serif;
  }
}

@layer components {
  .card { background: var(--color-surface); border-radius: var(--radius-md); padding: var(--space-md); }
  .card__title { font-size: 1.25rem; color: var(--color-text); }
  .card--featured { border: 2px solid var(--color-primary); }
}
```

### Performance

- Inline critical CSS in `<head>` for first contentful paint
- Use `font-display: swap` for web fonts; prefer system font stacks
- Modern image formats: AVIF > WebP > JPEG; use `<picture>` with fallbacks
- Animate only `transform` and `opacity` to avoid layout reflows
- Use `content-visibility: auto` for off-screen sections
- Set `width`/`height` or `aspect-ratio` on media to prevent layout shift

```html
<picture>
  <source srcset="hero.avif" type="image/avif" />
  <source srcset="hero.webp" type="image/webp" />
  <img src="hero.jpg" alt="Dashboard overview" width="1200" height="630"
       loading="lazy" decoding="async" />
</picture>
```

### Responsive Design

- Mobile-first: base styles for small screens, add complexity with `min-width` queries
- Use `rem`/`em` for sizing; reserve `px` for borders and fine details only
- Fluid typography with `clamp()`: `font-size: clamp(1rem, 0.5rem + 1.5vw, 1.5rem)`
- Container queries (`@container`) for component-level responsiveness
- Test at 320px, 768px, 1024px, 1440px, and with 200% browser zoom
- Touch targets: at least 44x44px on mobile

## Key Patterns

### Grid (2D) vs Flexbox (1D)

Use CSS Grid for page layouts with rows and columns; use Flexbox for single-axis alignment.

```css
/* Grid: 2D page layout */
.page {
  display: grid;
  grid-template: "header header" auto "sidebar main" 1fr "footer footer" auto / 16rem 1fr;
  min-height: 100dvh;
}

/* Flexbox: 1D navigation */
.nav { display: flex; align-items: center; gap: var(--space-md); }
.nav__logo { margin-right: auto; }
```

### Container Queries

```css
.card-container { container-type: inline-size; container-name: card; }

@container card (min-width: 30rem) {
  .card { flex-direction: row; align-items: center; }
}
```

### The :has() Selector

```css
.field:has(input:focus) { outline: 2px solid var(--color-primary); }
.card:has(img) { padding: 0; }
form:has(:invalid) button[type="submit"] { opacity: 0.5; pointer-events: none; }
```

### Cascade Layers (@layer)

```css
@layer reset, base, layout, components, utilities;

@layer reset { *, *::before, *::after { box-sizing: border-box; margin: 0; } }
@layer utilities {
  .visually-hidden {
    clip: rect(0 0 0 0); clip-path: inset(50%); height: 1px;
    overflow: hidden; position: absolute; white-space: nowrap; width: 1px;
  }
}
```

### Dark Mode and User Preferences

```css
:root { color-scheme: light dark; --color-bg: oklch(98% 0.005 265); }
@media (prefers-color-scheme: dark) { :root { --color-bg: oklch(15% 0.02 265); } }
[data-theme="dark"] { --color-bg: oklch(15% 0.02 265); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important; transition-duration: 0.01ms !important;
  }
}
```

## Accessibility Checklist (WCAG 2.1 AA)

**Perceivable**
- [ ] All images have descriptive `alt` (or `alt=""` for decorative)
- [ ] Color contrast: 4.5:1 body text, 3:1 large text
- [ ] Information not conveyed by color alone
- [ ] Text resizable to 200% without content loss
- [ ] Captions for video; transcripts for audio

**Operable**
- [ ] All functionality keyboard-accessible (Tab, Enter, Escape, arrows)
- [ ] Logical focus order; visible focus indicators
- [ ] No keyboard traps; modals return focus on close
- [ ] Skip navigation link as first focusable element
- [ ] Touch targets at least 44x44px

**Understandable**
- [ ] `<html lang="...">` set correctly
- [ ] Form inputs have visible labels and descriptive error messages
- [ ] Consistent navigation across pages

**Robust**
- [ ] Valid HTML (W3C validator)
- [ ] ARIA roles, states, and properties match widget behavior
- [ ] Tested with screen reader (VoiceOver, NVDA, or JAWS)
- [ ] Tested with 200% browser zoom

## Tooling

```bash
npx stylelint "**/*.css"                      # CSS lint
npx stylelint "**/*.css" --fix                # CSS lint auto-fix
npx htmlhint "**/*.html"                      # HTML validation
npx prettier --check "**/*.{html,css,scss}"   # Format check
npx prettier --write "**/*.{html,css,scss}"   # Format fix
npx lighthouse http://localhost:3000 --output html --view  # Audit
npx @axe-core/cli http://localhost:3000       # Accessibility check
npx pa11y http://localhost:3000               # Accessibility test
```

### Stylelint Configuration

```json
{
  "extends": ["stylelint-config-standard"],
  "rules": {
    "declaration-no-important": true,
    "selector-max-specificity": "0,3,0",
    "max-nesting-depth": 3,
    "color-function-notation": "modern",
    "selector-class-pattern": "^[a-z][a-z0-9]*(__[a-z0-9-]+)?(--[a-z0-9-]+)?$"
  }
}
```

## References

For detailed layout examples, accessibility patterns, and modern CSS features, see:

- [references/patterns.md](references/patterns.md) -- Grid/Flexbox layouts, modal dialogs, fluid typography, scroll animations

## External References

- [MDN HTML Reference](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [CSS Tricks Guide to Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [CSS Tricks Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [Every Layout](https://every-layout.dev/)
- [Modern CSS Solutions](https://moderncss.dev/)
- [web.dev Learn CSS](https://web.dev/learn/css/)
- [Can I Use](https://caniuse.com/)
