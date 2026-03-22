---
name: html-generator
description: Use when generating branded HTML pages and components from a design system. Creates standalone HTML components and composes them into full pages with embedded CSS, responsive design, and brand integration.
version: 2.9.0
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: false
---

# HTML Generator Skill

Create distinctive, branded HTML pages and standalone components from a design system.

## The Critical Understanding

HTML page creation is **design-system-driven composition**, not template filling. Each component is a standalone design artifact that works independently AND as part of a composed page. Every section should feel crafted by a senior designer — intentional, distinctive, unforgettable.

**What you receive**: A design system (canvas-philosophy.md + design-system.md) with design tokens, component catalog, and brand identity.
**What you create**: Standalone HTML components + a composed single-file HTML page.
**The standard**: Work that makes the viewer stop scrolling. Bold, distinctive, never generic.

---

## When Called

This skill is invoked by `/html-page` and `/html-page-quick` commands. It receives:

1. **Design system files** — canvas-philosophy.md + design-system.md from the project
2. **Brand philosophy** — brand-philosophy.md (or sub-identity overrides)
3. **Component selections** — which components to include (hero, features, CTA, etc.)
4. **Existing components** — any reusable components from `components/` directory
5. **Content** — text, headings, descriptions for each section
6. **Style constraints** — from `references/web-style-constraints.md`

---

## Two Output Modes

### Mode 1: Component Generation

Generate individual standalone components. Each component:
- Is a complete HTML fragment with embedded `<style>`
- References design tokens via CSS custom properties
- Includes prop/slot metadata comments for future conversion
- Can be viewed independently in a browser (with token fallback values)

### Mode 2: Page Composition

Assemble components into a single `.html` file:
- Shared CSS custom properties (design tokens) in `:root`
- Responsive wrapper with meta viewport
- Components assembled in order with consistent spacing
- Navigation at top, footer at bottom
- Single embedded `<style>` block (deduplicated from components)
- Minimal `<script>` when style requires it (scroll triggers, parallax)

---

## Part 1: Design Thinking Process

Before writing any HTML, internalize the design system:

0. **Verify brand exists** — if no `design-system.md` in the project, STOP and suggest `/design-html` first. If no `brand-philosophy.md`, suggest `/brand-extract` first. Never proceed with default/example values.
1. **Read the canvas philosophy** — absorb its aesthetic movement, not just rules
2. **Load design tokens** — colors, fonts, spacing become CSS custom properties
3. **Understand the style** — read enforcement blocks from `references/web-style-constraints.md`
4. **Consider the content** — what is the page's purpose? Who sees it? What should they feel?
5. **Plan differentiation** — what makes THIS page visually memorable vs. generic?

### The Differentiation Test

Before generating, ask: "Could this page belong to any brand?" If yes, push harder. Then ask: **"What is the ONE thing someone will remember about this page?"** — a dramatic type scale, a surprising color moment, an unexpected layout break. If you cannot name it, the design is not distinctive enough.

Incorporate:
- The canvas philosophy's unique movement name and spirit
- Unexpected layout choices (asymmetry, overlap, grid-breaking)
- Typography as art (size contrasts, weight mixing, letter-spacing play)
- Atmosphere (gradient meshes, noise textures, patterns, shadows with depth)
- The brand's personality expressed through micro-interactions (hover states, transitions)

### Intentionality Over Intensity

**Match implementation complexity to the aesthetic vision.** Maximalist designs need elaborate code with extensive animations and layered effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. The key is intentionality, not intensity — a Swiss design executed with mathematical precision is as powerful as a Memphis design executed with wild energy. Never apply "bold" uniformly; calibrate to the style.

---

## Part 2: Brand Integration

### Design Tokens → CSS Custom Properties

Read the project's `design-system.md` and map ALL token sections to `:root` custom properties. This includes:

- **Colors** — `--color-primary`, `--color-secondary`, `--color-accent`, `--color-bg`, `--color-bg-alt`, `--color-text`, `--color-text-muted`
- **Typography** — `--font-heading`, `--font-body`, `--font-size-*` scale
- **Spacing** — `--space-xs` through `--space-2xl`
- **Layout** — `--max-width`, `--border-radius`, `--min-tap-target`
- **Interaction** — `--timing-fast`, `--timing-base`, `--timing-slow`, `--easing-default`
- **Forms** (if page has forms) — `--color-error`, `--color-success`, field/label/error styling

The design-system.md is the single source of truth for all token values. Do not hardcode values — read them from the file.

### Brand Bias Prevention

Before generating any HTML, verify:

```
□ All colors use CSS custom properties from design-system.md (--color-primary, etc.)
□ No hardcoded hex values except #FFFFFF/#000000 for universal black/white
□ font-family from design-system.md, never "Inter", "Roboto", or "Arial" as defaults
□ If no design-system.md exists: STOP, suggest /design-html first
□ Background colors, accent colors, text colors all traced to design tokens
```

**Never copy hex codes or font names from reference file examples into generated HTML.**
All visual values must flow from: design-system.md → CSS custom properties → component styles.

### Color Dominance Principle

Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Use `--color-primary` as the dominant voice (headings, CTAs, navigation active states), `--color-accent` as the sharp punctuation (links, hover states, highlights), and let `--color-bg` and `--color-text` do the quiet structural work. If the palette feels "even" — one color is not leading — push the primary harder or pull the secondary back.

### Font Loading

Use Google Fonts via `<link>` with system font fallback stack:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=FontName:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

Choose DISTINCTIVE fonts — never default to Inter, Roboto, or Arial. Every design system deserves fonts that match its personality.

---

## Part 3: Component Generation

### Rules for Every Component

1. **Standalone validity** — each component works as a standalone HTML file
2. **Shared tokens** — all components reference the same CSS custom property names
3. **Consistent naming** — `{type}-{variant}.html` (e.g., `hero-centered.html`)
4. **Prop/slot metadata** — HTML comments marking content insertion points
5. **Responsive** — mobile-first, works at all 3 breakpoints
6. **Accessible** — semantic HTML, ARIA labels where needed, focus management
7. **Interactive states** — every clickable/tappable element must define hover, focus, and active styles using the interaction tokens from design-system.md
8. **Touch-ready** — interactive elements meet `--min-tap-target` size with adequate spacing

### Metadata Comments Format (MANDATORY)

Every component MUST include conversion-ready metadata comments. These enable automated conversion to Drupal SDC, React, and other frameworks. Without them, the design-system-converter cannot identify components, props, or slots.

**Component boundaries** — wrap the entire component:
```html
<!-- component: hero variant: centered -->
<section class="hero">
  ...
</section>
<!-- /component: hero -->
```

**Props** — place immediately BEFORE the element they annotate:
```html
<!-- prop: headline type: string -->
<h1 class="hero__title">Your Headline</h1>

<!-- prop: show-badge type: boolean -->
```

**Slots** — wrap repeating or insertable content areas:
```html
<!-- slot: features -->
<div class="feature-grid__list">
  <div class="feature-grid__item">
    <!-- prop: feature-title type: string -->
    <h3>Feature Title</h3>
    <!-- prop: feature-description type: string -->
    <p>Description</p>
  </div>
</div>
<!-- /slot: features -->
```

**Icons** — place before SVG elements:
```html
<!-- icon: rocket -->
<svg>...</svg>
```

**Supported prop types:** `string`, `boolean`

These comments MUST appear in both standalone components AND composed pages. See Part 10 for preservation rules during page composition.

### Component CSS Pattern

Each component scopes its styles using BEM-like class naming:

```css
.hero { /* component root */ }
.hero__title { /* element */ }
.hero__title--large { /* modifier */ }
```

Components reference design tokens (not hardcoded values):
```css
.hero {
  background: var(--color-bg);
  color: var(--color-text);
  padding: var(--space-xl) var(--space-md);
  font-family: var(--font-body);
}
```

---

## Part 3.5: Icon Integration

Lucide icons (1,500+ icons) are available as inline SVG via a CLI script.

### Fetching Icons

```bash
# Get inline SVG for one or more icons
node "$BRAND_CONTENT_DESIGN_DIR/scripts/html-icons.js" get rocket lightbulb shield

# Search by keyword
node "$BRAND_CONTENT_DESIGN_DIR/scripts/html-icons.js" search chart

# List icons in a category
node "$BRAND_CONTENT_DESIGN_DIR/scripts/html-icons.js" category business

# List all categories
node "$BRAND_CONTENT_DESIGN_DIR/scripts/html-icons.js" categories
```

The `get` command outputs each SVG on its own line prefixed with `<!-- icon: {name} -->`.

### Embedding Pattern

Icons use `currentColor` for stroke and inherit size from the parent container:

```html
<div class="feature-grid__icon" aria-hidden="true">
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <!-- paths from script output -->
  </svg>
</div>
```

### CSS Styling

Control icon size and color through the container:

```css
.feature-grid__icon {
  width: 48px;
  height: 48px;
  color: var(--color-primary);
}
.feature-grid__icon svg {
  width: 100%;
  height: 100%;
}
```

### When to Use Icons

- Use icons when a clear visual metaphor exists (rocket for launch, shield for security)
- Pair icons with text labels — never use icons alone for meaning
- Skip icons when no good match exists; forced icons weaken the design

### Accessibility

- **Decorative icons** (paired with text): `aria-hidden="true"` on the SVG
- **Meaningful icons** (convey info alone): `role="img" aria-label="Description"` on the SVG

---

## Part 4: Style Enforcement

Read `references/web-style-constraints.md` for the selected style and enforce:

- **Per-section limits** — word counts, element counts per section
- **Spacing values** — padding, margin ranges in CSS units
- **Typography rules** — weights, sizes, letter-spacing
- **Color strategy** — how many colors, contrast requirements
- **Layout directives** — CSS Grid/Flexbox patterns required
- **JS allowance** — which styles allow/require minimal JavaScript
- **Anti-patterns** — what NEVER to do with this style

Read the enforcement block and apply it to every component and composed page.

---

## Part 5: Responsive Design

Mobile-first approach with 3 breakpoints:

```css
/* Mobile: 375px (default) */
.component { /* base mobile styles */ }

/* Tablet: 768px */
@media (min-width: 768px) {
  .component { /* tablet overrides */ }
}

/* Desktop: 1200px */
@media (min-width: 1200px) {
  .component { /* desktop overrides */ }
}
```

### Responsive Patterns

- **Navigation**: Hamburger on mobile → horizontal on desktop
- **Hero**: Stacked on mobile → side-by-side on desktop
- **Grids**: 1 col mobile → 2 col tablet → 3-4 col desktop
- **Typography**: Scale down 15-20% on mobile
- **Spacing**: Reduce section padding 30-40% on mobile
- **Images**: Full-width on mobile, constrained on desktop

---

## Part 6: CSS-First Interactivity

Prefer CSS solutions. Use JS only when CSS cannot achieve the effect.

### Motion Hierarchy

Focus the motion budget on **one high-impact moment** per page. One well-orchestrated page load with staggered reveals (`animation-delay`) creates more delight than scattered micro-interactions on every element. Decide: is it the hero entrance, the stats counting up, or the card grid cascading in? Pick one, make it great, and keep the rest subtle.

### CSS-Only Patterns

- **Hover effects**: `transform`, `box-shadow`, `opacity` transitions
- **Accordions**: `<details>` + `<summary>` elements
- **Scroll snap**: `scroll-snap-type` for carousel-like sections
- **Animations**: `@keyframes` for loading, reveals, decorative motion
- **Smooth scroll**: `scroll-behavior: smooth`
- **Focus states**: `:focus-visible` with custom outlines

### Minimal JS (When Required by Style)

Some styles (Kinetic, 3D/Immersive, Parallax effects) need vanilla JS:

```javascript
// Intersection Observer for scroll reveals
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('[data-reveal]').forEach(el => observer.observe(el));
```

Rules for JS:
- Vanilla JS only — no frameworks, no jQuery, no build tools
- Progressive enhancement — page works without JS
- Respect `prefers-reduced-motion` — disable animations when set
- Minimal footprint — under 50 lines when possible

---

## Part 7: Typography as Art

Typography is the primary design tool for HTML pages. Make bold choices:

### Font Pairing Strategy

- **Heading + Body**: Contrasting but harmonious (serif heading + sans body, or vice versa)
- **Weight contrast**: Use the full weight range (300-900) for hierarchy
- **Size contrast**: Headlines should be DRAMATICALLY larger than body (3x-6x)
- **Letter-spacing**: Loose for uppercase headings, tight for large display text
- **Line-height**: Generous for body (1.6-1.8), tighter for headlines (1.0-1.2)

### Never Use

- Inter, Roboto, Arial, Helvetica (unless the brand specifically uses them or the style's Visual DNA specifies them)
- System font stack alone (always include a distinctive Google Font)
- Single weight throughout (exploit the full weight range)
- Uniform sizing (create dramatic scale contrast)

### Anti-Convergence

NEVER converge on the same font choices across different page generations. If you generated a page with Space Grotesk last time, pick a different font this time. Each design system and page should feel independently designed. Vary display fonts, body fonts, weight distributions, and size scales between projects. The goal: if someone lined up 10 generated pages, they should look like they came from 10 different designers.

---

## Part 8: Spatial Composition

### Layout Philosophy

- **Asymmetry over symmetry** — perfect symmetry is boring; controlled asymmetry creates energy
- **Overlap and layering** — elements can overlap (images behind text, decorative shapes)
- **Grid-breaking** — establish a grid, then intentionally break it for key moments
- **Generous negative space** — sections breathe with `var(--space-xl)` to `var(--space-2xl)` padding
- **Full-bleed moments** — some sections should break out of the max-width container

### Background & Atmosphere

- **Gradient meshes** — multi-stop gradients for depth (`background: linear-gradient(135deg, ...)`)
- **Noise/grain textures** — subtle SVG noise for tactile quality
- **Geometric patterns** — CSS-generated shapes, clip-paths for visual interest
- **Depth through shadow** — layered `box-shadow` for elevation
- **Color blocking** — alternating section backgrounds for rhythm

---

## Part 9: Accessibility (MANDATORY)

Every generated page MUST pass these checks:

### Requirements

- **Semantic HTML5**: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`
- **Heading hierarchy**: h1 → h2 → h3, no skipping levels
- **Skip navigation**: Hidden link to main content
- **WCAG AA contrast**: 4.5:1 for normal text, 3:1 for large text
- **Focus indicators**: Visible `:focus-visible` on all interactive elements
- **Alt text**: Descriptive alt text on images (or placeholder comments)
- **ARIA labels**: On navigation, landmarks, interactive elements
- **Reduced motion**: `@media (prefers-reduced-motion: reduce)` disables animations
- **Language attribute**: `<html lang="en">`
- **Viewport meta**: `<meta name="viewport" content="width=device-width, initial-scale=1">`

### Neumorphism Warning

When using Neumorphism style, DOUBLE-CHECK contrast ratios. Soft shadows on similar backgrounds risk failing WCAG AA. Add explicit borders or increase shadow contrast if needed.

---

## Part 10: Page Composition

When assembling components into a full page, every component section MUST retain its metadata comments. This is the **most critical requirement** for framework convertibility.

### Metadata Preservation (CRITICAL — ENFORCE STRICTLY)

**Rules:**
- Place `<!-- component: type variant: variant -->` BEFORE the component's outermost HTML element
- Place `<!-- /component: type -->` AFTER the component's closing tag
- Place `<!-- prop: name type: type -->` immediately BEFORE the element it annotates
- Place `<!-- slot: name -->` / `<!-- /slot: name -->` around slot content areas
- Do NOT strip, summarize, or simplify metadata during page assembly
- Do NOT replace metadata with section divider comments like `<!-- Navigation -->` or `<!-- ====== HERO ====== -->`

**Complete composed page structure:**

```html
<body>
  <a href="#main" class="skip-link">Skip to main content</a>

  <!-- component: nav variant: sticky -->
  <header class="nav" role="banner">
    <!-- prop: site-name type: string -->
    <span class="nav__name">Site Name</span>
    <!-- slot: menu -->
    <nav role="navigation" aria-label="Main navigation">
      <a href="#">Home</a>
    </nav>
    <!-- /slot: menu -->
  </header>
  <!-- /component: nav -->

  <main id="main">
    <!-- component: hero variant: centered -->
    <section class="hero">
      <!-- prop: headline type: string -->
      <h1 class="hero__title">Page Title</h1>
      <!-- prop: subheadline type: string -->
      <p class="hero__subtitle">Subtitle text</p>
    </section>
    <!-- /component: hero -->

    <!-- component: article-card-grid variant: 3-col -->
    <section class="card-grid">
      <!-- prop: section-title type: string -->
      <h2>Latest Articles</h2>
      <!-- slot: cards -->
      <div class="card-grid__list">
        <article class="card">
          <!-- prop: card-image type: string -->
          <img src="image.jpg" alt="Article">
          <!-- prop: card-title type: string -->
          <h3>Card Title</h3>
          <!-- prop: card-excerpt type: string -->
          <p>Excerpt text</p>
        </article>
      </div>
      <!-- /slot: cards -->
    </section>
    <!-- /component: article-card-grid -->
  </main>

  <!-- component: footer variant: simple -->
  <footer class="footer" role="contentinfo">
    <!-- prop: copyright type: string -->
    <p>&copy; 2026 Brand Name</p>
  </footer>
  <!-- /component: footer -->
</body>
```

**Every component in the page must have opening and closing component markers.** No exceptions.

Also see `references/html-technical.md` for the full HTML boilerplate and additional technical specs.

### CSS Organization in Composed Page

1. **CSS Reset** — minimal reset (box-sizing, margin:0, img max-width)
2. **Design Tokens** — `:root` custom properties
3. **Base Typography** — body, headings, links, paragraphs
4. **Utility classes** — `.container`, `.sr-only`, `.skip-link`
5. **Component styles** — each component's CSS block, deduplicated

### Section Spacing

- Consistent section padding: `var(--space-xl) 0` (desktop), `var(--space-lg) 0` (mobile)
- Alternating backgrounds for visual rhythm
- No visible borders between sections (spacing and color changes create separation)

---

## Part 11: Image Handling

Since Claude cannot generate actual images, use smart placeholders:

### CSS Gradient Placeholders

```css
.hero__image-placeholder {
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-accent) 100%);
  aspect-ratio: 16/9;
  border-radius: var(--border-radius);
  /* Replace with actual image:
     background: url('your-image.jpg') center/cover; */
}
```

### Placeholder Strategy

- Use CSS gradients that match the brand palette
- Add `aspect-ratio` to maintain proportions
- Include HTML comments with image replacement instructions
- Use decorative CSS patterns (stripes, dots, shapes) for variety
- For team photos: use initials or icon placeholders

---

## Part 12: Convertibility Structure

Design components for future conversion to Drupal SDC, React, Canvas, and other frameworks. The metadata comments from Part 3 and Part 10 are what make conversion possible.

### How Metadata Maps to Frameworks

| HTML Metadata | Drupal SDC | React | Twig |
|---|---|---|---|
| `<!-- component: hero -->` | Component directory name | Component file name | Template name |
| `<!-- prop: headline type: string -->` | `props.headline` in schema | `props.headline` | `{{ headline }}` |
| `<!-- prop: featured type: boolean -->` | Boolean prop | Conditional render | `{% if featured %}` |
| `<!-- slot: content -->` | `{% block content %}` | `children` | `{% block content %}` |
| `<!-- /component: hero -->` | Template boundary | Component boundary | Template boundary |
| CSS custom properties | SCSS variables | Theme tokens | Twig with attach_library |

### Naming Conventions

- Components use semantic names: `hero`, `feature-grid`, `testimonials`, `cta`
- CSS classes use BEM: `.hero__title`, `.feature-grid__item`
- CSS custom properties for all brand values (map to SCSS variables, CSS modules)
- Data attributes for behavioral hooks: `data-reveal`, `data-parallax`

---

## Anti-Patterns (NEVER)

- **No CSS frameworks** — no Bootstrap, Tailwind, Foundation in output
- **No external JS** — no jQuery, React, Alpine, HTMX in output
- **No broken images** — use CSS placeholders, never `<img src="missing.jpg">`
- **No AI slop** — avoid generic stock photo aesthetics, overused gradients, cliched layouts
- **No wall of text** — respect per-section word limits from style constraints
- **No inline styles** — all CSS in `<style>` block (except CSS custom property overrides)
- **No pixel units for typography** — use rem/em for accessibility
- **No frameworks** in font loading — Google Fonts `<link>` only

---

## References

### Bundled (Plugin-Specific)

Load these reference files when generating:

- `references/html-design-guide.md` — Design system philosophy and content type guide
- `references/web-style-constraints.md` — 21 style enforcement blocks for web
- `references/html-components.md` — 15 component types with HTML/CSS patterns
- `references/html-technical.md` — Technical specs, boilerplate, file format

### Online Dev-Guides (Design Systems)

For design system fundamentals beyond this plugin's visual styles, use the dev-guides-navigator plugin:

Invoke `/dev-guides-navigator` with keywords like "design system recognition", "Bootstrap mapping", "Radix SDC", or "component classification". The navigator handles caching and disambiguation — never fetch dev-guides URLs directly.
