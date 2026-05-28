---
name: html-slides
description: Used when the user asks to "create HTML slides", "generate an HTML presentation", "make animated slides", "build interactive slides", "create web slides", "GSAP presentation", "browser-based slides", "convert PPTX to HTML", "animated deck", "reveal.js slides", or when the output format is HTML for any presentation task. Also triggers on "single-file presentation", "CSS animations in slides", "scroll-based slides", or "web presentation". Generates self-contained, single-file HTML with viewport fitting, CSS/GSAP animations, and curated style presets.
version: 0.2.1
---

# HTML Slides — Animated, Viewport-Fitted Presentations

Generate single-file, self-contained HTML presentations with professional animations, responsive viewport fitting, and curated style presets. Zero external dependencies at runtime — all CSS/JS inline.

## Architecture

Every HTML presentation follows this structure:

1. **Single file** — One `.html` file with inline CSS and JS (no build tools)
2. **Viewport fitted** — Each slide locks to `100vh`/`100dvh` with `overflow: hidden`
3. **CSS custom properties** — All theming via `:root` variables for easy restyling
4. **Semantic HTML** — `<section>` per slide, `<nav>` for controls
5. **Progressive enhancement** — Works without JS, animations enhance with JS

## Mandatory Viewport Rules

Apply the viewport base CSS from `assets/viewport-base.css` to EVERY presentation. Key rules:

- Every slide: `height: 100vh; height: 100dvh; overflow: hidden`
- All typography uses `clamp(min, preferred, max)` for responsive scaling
- Images constrained to `min(50vh, 400px)` max height
- Responsive breakpoints at 700px, 600px, 500px heights
- `prefers-reduced-motion` support included
- Grid fallback: `grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr))`

Never allow scrolling within a slide. If content exceeds capacity, split across multiple slides.

**Edge Case: Negative Clamp Values**
Use `calc(-1 * clamp(...))` when you need negative viewport-edge spacing (e.g., negative margins, negative padding). This pattern preserves the clamp function's responsiveness while inverting the value.

**iOS Safari 100vh Bug**
The `100vh` unit in iOS Safari includes the address bar, causing content to overflow. Always pair `100vh` with `100dvh` (dynamic viewport height) in fallback chains. Modern viewports ignore `100vh` if `100dvh` is present.

## Animation System

### CSS-First Approach (Default)

Use CSS animations as the baseline. Apply `.reveal` class with staggered `transition-delay`:

```css
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s var(--ease-out-expo), transform 0.6s var(--ease-out-expo);
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

Trigger with Intersection Observer adding `.visible` class on viewport entry.

**Easing**: `--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1)` for all entrance animations.

### GSAP Enhancement (When Requested)

For sophisticated animations, load GSAP from CDN and use timeline-based choreography. Consult `references/animation-patterns.md` for detailed GSAP recipes and the [GSAP docs](https://gsap.com/docs/) for API reference. Key integration points:

- Load GSAP + ScrollTrigger from `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js`
- Use `gsap.timeline()` for sequenced slide entrance animations
- Apply `gsap.matchMedia()` for responsive animation behavior
- Respect `prefers-reduced-motion` — disable animations when active

**Timeline Entrance with Position Parameter**
Stagger reveals without explicit delays using the position parameter in timeline. Example:
```javascript
const tl = gsap.timeline();
tl.to('.heading', { opacity: 1, duration: 0.6 })
  .to('.subtitle', { opacity: 1, duration: 0.4 }, '<0.2') // Starts 0.2s before heading ends
  .to('.bullet', { opacity: 1, stagger: 0.1 }, '<0.15');
```

**SplitText for Headlines and Word/Char Reveals**
Animate individual words or characters in headlines:
```javascript
gsap.registerPlugin(SplitText);
const split = new SplitText('.headline', { type: 'words,chars' });
gsap.from(split.chars, { 
  opacity: 0, 
  duration: 0.4, 
  stagger: 0.05,
  ease: 'back.out'
});
```

**ScrollTrigger for Slide-by-Slide Navigation**
Tie slide transitions to scroll position for interactive presentations:
```javascript
gsap.registerPlugin(ScrollTrigger);
gsap.to('.slide', {
  scrollTrigger: {
    trigger: '.slide-container',
    pin: true,
    scrub: 1,
    snap: 1 / slideCount
  }
});
```

**Spring Physics Timing from Remotion**
Translate Remotion spring physics into GSAP elastic easing for natural motion:
- **Smooth** (damping: 200) → `elastic.out(1, 0.1)` — subtle bounce, feels polished
- **Snappy** (damping: 20) → `elastic.out(1, 0.35)` — noticeable spring, modern feel
- **Bouncy** (damping: 8) → `elastic.out(1, 0.5)` — playful bounce, energetic

### Animation Inventory

| Animation | CSS Class | Use Case |
|-----------|----------|----------|
| Fade + slide up | `.reveal` | Default entrance for text/cards |
| Scale in | `.reveal-scale` | Images, feature cards |
| Slide from left | `.reveal-left` | Two-column content |
| Blur in | `.reveal-blur` | Background elements, overlays |
| Stagger | `:nth-child(n)` delay | Lists, grid items |

### Animation Guidelines

- **Playful**: Bouncy easing, 400-600ms, staggered reveals
- **Professional**: Subtle fades, 200-300ms, minimal movement
- **Cinematic**: Slow fades 1-1.5s, parallax, scale transitions
- **Technical**: Sharp, fast (150-200ms), no bounce

## Slide Navigation

Include keyboard navigation (arrows, space, Page Up/Down), touch/swipe support, and optional progress indicator. Template in `references/html-template.md`.

## Style Preset Application

Read style preset definitions from the parent `slide-design` skill's `references/style-presets.md`. Each preset maps to CSS custom properties:

```css
:root {
  --bg-primary: #0a0a0a;
  --bg-secondary: #1a1a1a;
  --text-primary: #ffffff;
  --text-secondary: #a0a0a0;
  --accent: #4a9eff;
  --accent-secondary: #ff6b6b;
  --font-heading: 'Clash Display', sans-serif;
  --font-body: 'IBM Plex Sans', sans-serif;
  --title-size: clamp(2rem, 6vw, 5rem);
  --body-size: clamp(0.9rem, 2vw, 1.25rem);
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
}
```

Load fonts from Google Fonts or Fontshare — never rely on system fonts for headings.

## Slide Type Templates

For each slide type, follow the HTML patterns in `references/html-template.md`. Key templates:

- **Title slide** — Full-viewport hero with heading, subtitle, optional background image
- **Content slide** — Heading + bullet list or paragraphs with staggered reveal
- **Two-column** — Side-by-side layout with image + text or code + explanation
- **Image focus** — Full-bleed or centered image with caption overlay
- **Code slide** — Syntax-highlighted code block with Prism.js (CDN loaded)
- **Comparison** — Side-by-side cards or before/after layout
- **Quote** — Centered blockquote with attribution
- **Feature grid** — CSS Grid cards (max 6) with icons/titles/descriptions
- **Timeline** — Horizontal or vertical milestone layout

## Mermaid Diagram Support

For technical presentations, embed Mermaid diagrams:

1. Include Mermaid CDN: `https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.0/mermaid.min.js`
2. Use `<pre class="mermaid">` blocks for diagrams
3. Support flowcharts, sequence diagrams, class diagrams, and ER diagrams
4. Style with theme variables matching the presentation palette

## PDF Export Support

Include an optional print stylesheet for PDF export via browser print:

```css
@media print {
  .slide { page-break-after: always; height: 100vh; }
  .nav, .progress { display: none; }
  .reveal { opacity: 1; transform: none; }
}
```

## Anti-Patterns

Avoid these common mistakes:
- Scrolling within slides (always `overflow: hidden`)
- System fonts for headings (always load web fonts)
- Generic "AI slop" aesthetics (purple gradients, Inter everywhere)
- Inline styles (use CSS custom properties)
- Missing `prefers-reduced-motion` support
- Images without size constraints
- More than 6 items in a feature grid

## Show Don't Tell

Embody the principle of visual communication. Enhance instructions with visual weight and intentionality:

- **"Make it bold"** — Pair font weight increase with size increase AND accent color. A truly bold element dominates the hierarchy.
- **"Make it stand out"** — Combine `z-index` layering, `scale` transformation, AND contrasting color simultaneously. Isolation requires all three.
- **"One idea per slide"** — When content exceeds capacity, split across slides. Never shrink fonts below the minimum size threshold. Cramping is a design failure.
- **Visual hierarchy rule**: The most important element should be **3x the size** of supporting elements. If a headline is 3rem, body text should be ~1rem. Apply this ratio consistently.

## Mixed-Background Decks

Many professional presentations alternate background colors across slide groups. To implement this:

- Define a `data-theme` attribute per `<section>` (e.g., `data-theme="coral"`, `data-theme="dark"`, `data-theme="cream"`)
- Map each theme to CSS custom property overrides via `[data-theme="coral"] { --bg-primary: #E8845C; --text-primary: #fff; }`
- Maintain font and layout consistency even when backgrounds change
- Use contrasting backgrounds to signal section transitions (e.g., black for demo sections, cream for infographics)

## Inline Edit Mode

Generated HTML can include `contenteditable="true"` attributes on text elements, allowing users to edit slides directly in the browser before presenting.

To enable inline editing, add `contenteditable="true"` to text elements:
```html
<h1 contenteditable="true">Edit this headline</h1>
<p contenteditable="true">Edit this paragraph</p>
```

Include this CSS for visual feedback:
```css
[contenteditable]:hover {
  outline: 2px dashed var(--accent);
  cursor: text;
}

[contenteditable]:focus {
  outline: 2px solid var(--accent);
}
```

Users can click any editable element, make changes live, and present without exporting. Disable with `contenteditable="false"` if read-only mode is preferred.

## Additional Resources

### Reference Files

- **`references/html-template.md`** — Complete HTML boilerplate with navigation, all slide type templates
- **`references/animation-patterns.md`** — CSS and GSAP animation recipes with timing and easing

### Asset Files

- **`assets/viewport-base.css`** — Mandatory viewport CSS (include in every presentation)

### Script Files

- **`scripts/extract-pptx.py`** — Extract text, images, and notes from PPTX files to JSON for HTML conversion
