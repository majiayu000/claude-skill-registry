---
name: pellicola
description: "Generate cinematic case study pages for films, documentaries, photography portfolios, and creative projects — film-frame hero images, structured crew credit grids, dark footage galleries, festival award sections, scroll-choreographed reveals via data-attribute animation orchestration. Warm cream palette with analog typography. Single-file HTML, zero build step. Triggers on film case study, documentary showcase, filmmaker portfolio, production company website, film credits page, creative project case study, director portfolio, photography case study."
argument-hint: [--mode case-study|hero|credits|gallery] [film title or project name]
---

Build cinematic case study pages — the kind you see on film production company sites, documentary showcases, and photographer portfolios. Warm analog palette, domain-specific components, scroll-choreographed reveals. Single-file HTML, zero build step.

"Pellicola" is Italian for film — literally "little skin," the celluloid stock.

## Creative Direction

The aesthetic is **analog cinema on the web** — warm cream backgrounds like unbleached paper stock, deep ink-black text, a single red accent reserved exclusively for the play button. Typography pairs a dramatic display serif (headlines, names) with a precise geometric sans (labels, navigation). Every image is framed like a film still — cream padding, rounded corners, subtle shadow creating a polaroid/celluloid look.

If the `minoan-frontend-design` skill is available, read it for broader aesthetic principles. Pellicola encodes those principles into a concrete design system for the cinematic case study genre. Pages built with Pellicola should score 16+/20 on `/design-audit` and 28+/40 on `/design-critique`.

Name the conceptual direction before coding. Default: "analog screening room." Override with project-specific direction when appropriate — "70mm documentary," "festival press kit," "darkroom portfolio."

## Quick Start

```bash
# Generate a full case study page
python3 scripts/pellicola_generator.py --mode case-study --title "Taboo" --output taboo.html

# Generate just the hero section
python3 scripts/pellicola_generator.py --mode hero --title "Ana Maxim" --output hero.html

# Generate a credits grid
python3 scripts/pellicola_generator.py --mode credits --output credits.html

# Generate a dark footage gallery
python3 scripts/pellicola_generator.py --mode gallery --output gallery.html

# Validate a pellicola page
python3 scripts/validate_pellicola.py output.html
```

Or let Claude generate directly from the templates and references.

## Modes

| Mode | Template | What it generates |
|------|----------|-------------------|
| `case-study` | `assets/templates/case-study.html` | Full page: hero + credits + footage gallery + prizes + investors + next-project |
| `hero` | `assets/templates/hero-section.html` | Film-frame hero + title overlay + play button only |
| `credits` | `assets/templates/credits-grid.html` | Credit grid + director portrait card only |
| `gallery` | `assets/templates/footage-gallery.html` | Dark gallery section only (reusable dark image grid) |

## Components (9)

| Component | Class Prefix | What it renders |
|-----------|-------------|-----------------|
| `pel-hero` | `.pel-hero` | Film-frame image with title overlay, genre label, play button, down arrow |
| `pel-credit-grid` | `.pel-credits` | Role/name pairs in bordered grid (2-3 columns), tracked small caps roles |
| `pel-director-card` | `.pel-director` | Cropped portrait with dark overlay, display serif name, small caps role |
| `pel-context-widget` | `.pel-widget` | Sticky top-right nav: thumbnail, title, metadata tags, dropdown |
| `pel-play-button` | `.pel-play` | Red circle + play triangle + text reveal on hover |
| `pel-gallery` | `.pel-gallery` | Dark-background masonry image grid with hover scale + brightness shift |
| `pel-prizes` | `.pel-prizes` | Festival award logos + names in grid layout |
| `pel-next-project` | `.pel-next` | Large typography + image preview for adjacent case study navigation |
| `pel-section-divider` | `.pel-divider` | Labeled line divider between content sections |

Copy-paste HTML snippets for every component: `references/component-catalog.md`.

## Color System

All components read from `--pel-*` CSS custom properties. Override at `:root` to re-theme:

```css
:root {
  /* Background */
  --pel-cream: oklch(97.5% 0.012 85);
  --pel-cream-deep: oklch(95% 0.015 80);
  --pel-black: oklch(10% 0 0);

  /* Text */
  --pel-ink: oklch(15% 0.005 80);
  --pel-ink-muted: oklch(40% 0.01 80);
  --pel-ink-light: oklch(98% 0 0);

  /* Accent */
  --pel-red: oklch(55% 0.22 25);

  /* Borders */
  --pel-border: oklch(85% 0.01 80);
  --pel-border-dark: oklch(25% 0 0);

  /* Typography */
  --pel-font-display: 'Playfair Display', 'Cormorant Garamond', serif;
  --pel-font-body: 'DM Sans', 'Outfit', sans-serif;

  /* Easing */
  --pel-ease: cubic-bezier(.19, 1, .22, 1);
  --pel-ease-back: cubic-bezier(.175, 0, .77, 1);
  --pel-duration: 0.8s;
  --pel-duration-long: 1.1s;
}
```

Full token reference: `references/design-tokens.md`.
OKLCH palette deep-dive: `references/color-system.md`.

## Typography

Display serif carries the cinematic weight — dramatic, editorial, italic for emphasis. Geometric sans handles navigation, labels, metadata — precise and clean. Never Inter, Roboto, Arial, or system-ui. Follow `minoan-frontend-design` font reflex-reject procedure.

**Primary pairings** (Google Fonts):

| Role | Font | Weight | Usage |
|------|------|--------|-------|
| Display | Playfair Display | 400, 700, 400i | H1, H2, names, pullquotes |
| Body/UI | DM Sans | 400, 500, 700 | Body text, labels, navigation, metadata |

**Alternative pairings**:
- Cormorant Garamond (display) + Outfit (body)
- Lora (display) + Karla (body)

Full pairing guide: `references/typography-pairing.md`.

## Scroll Animation System

Pellicola uses declarative `data-pel` attributes to orchestrate scroll-triggered reveals via IntersectionObserver. No animation library required.

| Attribute | Effect | Default |
|-----------|--------|---------|
| `data-pel="y"` | translateY(40px → 0) + fade in | duration: 0.8s |
| `data-pel="alpha"` | opacity 0 → 1 | duration: 0.6s |
| `data-pel="line"` | scaleX(0 → 1) horizontal line reveal | duration: 0.6s |
| `data-pel="parallax"` | Parallax scroll offset on image | speed: 0.15 |
| `data-pel="stagger"` | Parent: children animate with cascade delay | delay: 0.1s each |
| `data-pel="title"` | Split text into lines, per-line translateY reveal | delay: 0.12s/line |

All animations respect `prefers-reduced-motion` — reduced to instant opacity with no transforms.

Full spec with IntersectionObserver setup and stagger math: `references/animation-system.md`.

## Section Sequence

Case study pages follow a canonical section order. Sections can be omitted but the order is fixed:

1. **Hero** — Film-frame image, title, genre label, play button
2. **Credits** — Director card + credit grid
3. **Footage / Gallery** — Dark-background image grid
4. **Prizes** — Festival awards and selections
5. **Investors / Partners** — Logo grid or text list
6. **Next Project** — Navigation to adjacent case study

Each section separated by a `pel-section-divider` with label text.

Full page architecture: `references/page-architecture.md`.

## Implementation Rules

1. **Vanilla only.** No React, Vue, Svelte, Angular. Plain HTML + CSS + JS.
2. **Single-file output.** Everything in one HTML file. CDN imports for Google Fonts and optional Phosphor Icons only.
3. **Warm-first.** Body background is `--pel-cream`, not white, not dark. The dark gallery is one section, not the whole page.
4. **`--pel-*` tokens everywhere.** Never hardcode colors — always reference custom properties.
5. **`prefers-reduced-motion` required.** Every `data-pel` animation must have a reduced-motion fallback.
6. **`requestAnimationFrame` only** for parallax scroll. Never `setInterval`.
7. **Semantic HTML.** `<article>` for case study, `<section>` for each content block, `<figure>` for images, `<dl>` for credits.
8. **Skip link required.** `<a href="#main" class="pel-skip-link">` as first body child.
9. **Credits are grids, not cards.** Role/name pairs in a CSS grid with border separators — not card containers with shadows.
10. **One accent, one purpose.** `--pel-red` is for the play button only.

## Anti-Patterns

- Never use white (`#FFFFFF`) backgrounds — always `--pel-cream`
- Never use card containers with shadows for credits — use bordered grid cells
- Never use avatar circles for the director portrait — cropped photographic portrait with dark overlay
- Never use Inter, Roboto, or system-ui — follow font reflex-reject
- Never animate on page load without IntersectionObserver — all reveals are scroll-triggered (hero title is the sole exception)
- Never use `--pel-red` for anything except the play button
- Never omit `prefers-reduced-motion` — all `data-pel` animations must respect it
- Never use `height` transitions for panels — use `grid-template-rows: 0fr` → `1fr`
- Never use a dark background for the whole page — dark gallery is one section within cream
- Never generate a case study without the canonical section sequence — order is hero → credits → footage → prizes → investors → next-project

Expanded explanations: `references/anti-patterns.md`.

## Post-Build QA

After building, run these passes in order:

1. `/design-audit` — Technical checks (a11y, performance, responsive, theming, anti-patterns). Target: 16+/20
2. `/design-critique` — UX review (Nielsen's heuristics, cognitive load, persona testing). Target: 28+/40
3. `/design-polish` — Final pass (alignment, spacing, interaction states, transitions)

## Cross-Skill References

| Skill | Cross-ref for | How |
|-------|---------------|-----|
| `grainient` | Lenis smooth scroll, hover-zoom | See `grainient/references/smooth-scroll.md` for setup |
| `rocaille-shader` | Hero parallax depth effect | Optional enhancement, not required |
| `pretext` | Split-text line-by-line reveal | Cross-ref for advanced text animation |
| `minoan-frontend-design` | Creative direction, OKLCH color, font reflex-reject | Read for broader aesthetic principles |
| `component-gallery` | Pattern research for credit grids, sticky nav | Pre-build research, not runtime dependency |

## Generator Script

```bash
python3 scripts/pellicola_generator.py \
  --mode case-study|hero|credits|gallery \
  --title "Film Title" \
  --director "Director Name" \
  --year 2024 \
  --runtime "93 min" \
  --genre "Documentary" \
  --output output.html
```

## Validation

```bash
python3 scripts/validate_pellicola.py output.html
```

Checks: viewport meta, `--pel-*` properties, no framework imports, cream background, `prefers-reduced-motion`, Google Fonts loaded, `data-pel` attributes, semantic HTML, skip link, no Inter/Roboto/system-ui.

## References

| Reference | When to consult |
|-----------|-----------------|
| `references/design-tokens.md` | Building new components or customizing the palette |
| `references/color-system.md` | Understanding OKLCH palette, dark gallery treatment |
| `references/typography-pairing.md` | Choosing fonts, pairing alternatives |
| `references/component-catalog.md` | Need HTML snippets for any component |
| `references/page-architecture.md` | Setting up page structure, section sequence |
| `references/animation-system.md` | Implementing `data-pel` scroll reveals |
| `references/anti-patterns.md` | Checking for common mistakes |

## Attribution

Design patterns deconstructed from [siena.film](https://siena.film/) (Webflow, Apr 2026). Technologies: Lenis (smooth scroll), IntersectionObserver (scroll reveals), CSS Grid (credit layouts), `grid-template-rows` (panel animations).
