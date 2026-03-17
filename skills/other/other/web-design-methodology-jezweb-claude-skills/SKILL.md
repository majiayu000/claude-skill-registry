---
name: web-design-methodology
description: "Universal web design implementation methodology — BEM, responsive, accessibility, CSS architecture, spacing systems, dark mode. The HOW of building production-grade HTML/CSS."
---

# Web Design Methodology

Universal patterns for building production-grade HTML/CSS. This skill covers implementation methodology — pair with `web-design-patterns` for specific component designs.

## What You Produce

Production-ready HTML/CSS prototypes with:
- Semantic CSS custom properties (tokens)
- BEM-named components
- Mobile-first responsive design
- Accessible markup
- Optional three-state dark mode

## File Structure

```
prototype/
├── index.html
├── about.html
├── services.html
├── contact.html
├── favicon.svg
├── css/
│   ├── variables.css     # Tokens: colours, typography, spacing
│   ├── styles.css        # All component styles (BEM)
│   └── mobile-nav.css    # Mobile menu styles
├── js/
│   ├── theme.js          # Dark mode toggle (only if requested)
│   └── mobile-menu.js    # Hamburger menu
└── media/
    └── images/
```

**Build order:**
1. `variables.css` — tokens first
2. `favicon.svg` — simple SVG from brand colour
3. `styles.css` — all BEM components
4. `mobile-nav.css` — responsive navigation
5. JS files — from `assets/` templates
6. `index.html` — homepage first
7. Inner pages — about, services, contact
8. Mobile check — verify at 375px

## BEM Naming

Use Block-Element-Modifier naming. No exceptions.

```css
/* Block */
.hero { }
.card { }
.nav { }

/* Element (child of block) */
.hero__title { }
.hero__subtitle { }
.hero__cta { }
.card__image { }
.card__content { }

/* Modifier (variation) */
.hero--split { }
.hero--minimal { }
.card--featured { }
.btn--primary { }
.btn--lg { }
```

**Rules:**
- Blocks are standalone components
- Elements are children, connected with `__`
- Modifiers are variations, connected with `--`
- Never nest more than one level: `.hero__content__title` is wrong
- Never use element without its block: `.card__image` only inside `.card`

## CSS Custom Properties

Use semantic tokens. Never hardcode colours, spacing, or typography values.

See `references/css-variables-template.md` for the complete token template.

```css
/* Always this */
.card {
  background: var(--card);
  color: var(--card-foreground);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  padding: var(--space-6);
}

/* Never this */
.card {
  background: #ffffff;
  color: #333333;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  padding: 24px;
}
```

## Dark Mode (Optional)

Dark mode is **optional** — only add if the brief requests it. Most business sites ship faster as light-only.

**When to include:**
- Brief explicitly requests it
- Tech/developer audiences (expected)
- Portfolio/creative sites (aesthetic choice)

**When to skip:**
- Trades, hospitality, professional services
- When simplicity and fast shipping matter more

### If Adding Dark Mode

Use class-based toggle, never CSS media queries.

```css
/* Light mode (default) */
:root {
  --background: #F9FAFB;
  --foreground: #0F172A;
  --card: #FFFFFF;
  --card-foreground: #1E293B;
}

/* Dark mode (via .dark class on html) */
.dark {
  --background: #0F172A;
  --foreground: #F1F5F9;
  --card: #1E293B;
  --card-foreground: #F1F5F9;
}
```

**Rules:**
- `.dark` class on `<html>`, toggled via JavaScript
- NEVER use `@media (prefers-color-scheme: dark)` — JS handles system preference
- Every background token needs a paired foreground token
- Brand colours get lighter/more saturated in dark mode
- Backgrounds: `#0F172A` to `#1E293B` range (not pure black)
- Every text-on-background combo must pass WCAG AA (4.5:1)

Use `assets/theme-toggle.js` for the three-state toggle implementation.

## Responsive Design

Mobile-first. Design for 375px, enhance upward.

### Breakpoints

```css
/* Base: 375px (mobile) — no media query needed */
@media (min-width: 640px) { /* sm — large phone */ }
@media (min-width: 768px) { /* md — tablet */ }
@media (min-width: 1024px) { /* lg — small desktop */ }
@media (min-width: 1440px) { /* xl — standard desktop */ }
```

### Mobile Priorities

1. Phone number visible and tappable without scrolling
2. Primary CTA visible without scrolling
3. Navigation works via hamburger menu
4. Touch targets minimum 44x44px
5. No horizontal scrolling ever
6. Images scale properly (no overflow)

### Wide Screen Constraints

```css
.prose { max-width: 65ch; }
.hero__content { max-width: min(640px, 45vw); }
.container {
  max-width: 1280px;
  margin-inline: auto;
  padding-inline: var(--space-4);
}
.section { padding: clamp(3rem, 6vw, 6rem) 0; }
```

Use `assets/mobile-nav.js` for the hamburger menu implementation.

## Typography Rules

1. **Dramatic size contrast.** Headlines 3-4x body size. `clamp(2.5rem, 6vw, 5rem)` for hero titles.
2. **Weight variety.** Mix 300 and 800 weights. Uniform weight is boring.
3. **One display moment per page.** One oversized word, one dramatic headline, one pull quote. Not three.
4. **Left-align body text.** Centre only for heroes and short statements. Never centre paragraphs.
5. **Letter spacing on uppercase.** Add `letter-spacing: 0.05em` minimum.

## Colour Usage

The 80/20 rule:

- 80% neutral tones (backgrounds, text, cards)
- 15% secondary/muted brand tones
- 5% primary brand colour (CTAs, one accent per viewport)

If primary is on every heading, border, icon — nothing stands out.

## Spacing System

Not uniform padding. Sections breathe differently:

```css
/* Tight section (service list, FAQ) */
.section--compact { padding: clamp(2rem, 4vw, 4rem) 0; }

/* Standard section */
.section { padding: clamp(3rem, 6vw, 6rem) 0; }

/* Breathing room (editorial break, testimonial) */
.section--spacious { padding: clamp(4rem, 8vw, 10rem) 0; }
```

## Shadow System

| Element | Shadow |
|---------|--------|
| Cards at rest | `--shadow-sm` |
| Cards on hover | `--shadow-md` |
| Dropdowns | `--shadow-lg` |
| Modals | `--shadow-xl` |

Not everything needs shadow. Use sparingly.

## Icons

Use Lucide icons via inline SVG:
- Size: 24px inline, 32-48px for feature blocks
- Stroke width: 1.5 or 2 (consistent throughout)
- Colour: `currentColor` (inherits text colour)
- Each icon should communicate something specific

## Accessibility

Non-negotiable:

- **Semantic HTML**: `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`
- **Alt text**: Meaningful for content images, empty for decorative
- **Contrast**: 4.5:1 minimum (7:1 preferred)
- **Focus styles**: Visible on all interactive elements
- **Skip link**: First focusable element
- **Form labels**: Associated with inputs
- **ARIA**: `aria-expanded` on toggles, `aria-label` where needed

## Performance

- `loading="lazy"` on images below the fold
- `loading="eager"` on hero image
- `<link rel="preconnect" href="https://fonts.googleapis.com">` in head
- Keep CSS under 50KB total
- No JavaScript frameworks — vanilla JS only

## Anti-AI Patterns

These patterns signal "AI generated this" — avoid:

- Hero → trust bar → 3 cards → features → stats → CTA → footer (the skeleton)
- Every section has identical padding
- All cards same size in perfect 3-column grid
- Everything centred
- Every section: heading + subheading + content (same rhythm)
- Decorative elements with no purpose
- "Learn More" as every CTA
- Inter/Arial/system fonts with no typographic personality

## Quality Checklist

Before marking complete:

- [ ] Direction is clear — can describe aesthetic in one phrase
- [ ] Typography makes a statement — not Inter/system
- [ ] Colour is restrained — primary used sparingly
- [ ] No two adjacent sections look the same
- [ ] CTAs are specific — no "Learn More"
- [ ] Mobile works — tested at 375px
- [ ] Dark mode works (only if enabled) — every section checked
- [ ] No hallucinated images — only real file paths
- [ ] Would a designer claim this as their work?
