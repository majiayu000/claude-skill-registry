---
name: grainient
description: "16 composable dark-mode visual effects as reusable single-file HTML pages: WebGL2 shader gradients (aurora/nebula via GLSL simplex noise FBM), cinematic vignette overlays, 9-layer box shadow systems, Lenis-style smooth scroll (vanilla JS lerp), spring animations (cubic-bezier presets), hover-zoom reveals, vertical ticker marquees, glassmorphism (backdrop-filter blur tiers), 3D perspective card flips, bento grids, gradient CTAs, SVG gradient icons, inset borders, grid pattern overlays, custom scrollbars, and responsive clamp typography. Dark-mode-first with lime green (#C2F13C) accent, --grn-* CSS custom property system. This skill should be used when building dark-mode landing pages, product showcases, SaaS marketing sites, or any UI needing cinematic depth, glow effects, or dark-on-dark elevation."
argument-hint: [--mode hero|bento|ticker|page|catalog] [description or effect name]
---

# Grainient Effects Skill

16 composable dark-mode effects spanning WebGL2 shaders, CSS surfaces, JS-driven motion, and layout patterns. Single-file HTML output, no build step, no framework dependencies.

## Quick Start

```bash
# Generate a hero section with aurora shader
python3 scripts/grainient_generator.py --mode hero --output hero.html

# Generate a full landing page
python3 scripts/grainient_generator.py --mode page --output landing.html

# Custom accent color
python3 scripts/grainient_generator.py --mode bento --accent "#FF6B35" --output showcase.html

# Interactive effects catalog
python3 scripts/grainient_generator.py --mode catalog --output catalog.html
```

Or let Claude generate directly from the templates and references.

## Effects Catalog

| # | Effect | Tier | Tech | Reference |
|---|--------|------|------|-----------|
| 1 | WebGL Shader Gradient | Hero | WebGL2+GLSL | `references/shader-gradient.md` |
| 2 | Vignette Overlay | Hero | CSS | `references/vignette-system.md` |
| 3 | 9-Layer Box Shadows | Hero | CSS | `references/shadow-system.md` |
| 4 | Smooth Scroll | Motion | JS | `references/smooth-scroll.md` |
| 5 | Spring Animations | Motion | CSS/JS | `references/spring-animations.md` |
| 6 | Hover Image Zoom | Motion | CSS | `references/hover-zoom.md` |
| 7 | Vertical Ticker Marquee | Motion | JS | `references/ticker-marquee.md` |
| 8 | Glassmorphism | Surface | CSS | `references/surface-effects.md` |
| 9 | 3D Perspective Card Flip | Surface | CSS | `references/surface-effects.md` |
| 10 | Bento Grid | Surface | CSS | `references/surface-effects.md` |
| 11 | Gradient CTAs | Surface | CSS | `references/surface-effects.md` |
| 12 | SVG Gradient Icons | Detail | SVG | `references/detail-effects.md` |
| 13 | Inset Border System | Detail | CSS | `references/detail-effects.md` |
| 14 | Grid Pattern Overlay | Detail | CSS | `references/detail-effects.md` |
| 15 | Custom Scrollbar | Detail | CSS | `references/detail-effects.md` |
| 16 | Responsive Clamp Typography | Detail | CSS | `references/detail-effects.md` |

## Modes

| Mode | Template | Effects Composed |
|------|----------|-----------------|
| `hero` | `assets/templates/hero-section.html` | Shader gradient + vignette + glassmorphism nav + clamp typography + springs |
| `bento` | `assets/templates/bento-showcase.html` | Bento grid + 9-layer shadows + hover zoom + glassmorphism + gradient CTAs |
| `ticker` | `assets/templates/ticker-landing.html` | Ticker marquee + smooth scroll + gradient CTAs + vignette + SVG icons |
| `page` | `assets/templates/dark-page.html` | All 16 effects in a full landing page |
| `catalog` | `assets/templates/effects-catalog.html` | Each effect demonstrated individually with controls |

## Color System

All effects read from `--grn-*` CSS custom properties. Override at `:root` to re-theme:

```css
:root {
  /* Background scale (dark-on-dark elevation) */
  --grn-bg: #000000;
  --grn-surface: #141414;
  --grn-elevated: #1A1A1A;
  --grn-card: #2B2B2B;

  /* Accent */
  --grn-accent: #C2F13C;
  --grn-accent-40: rgba(194, 241, 60, 0.4);
  --grn-accent-20: rgba(194, 241, 60, 0.2);

  /* Text */
  --grn-text: #FFFFFF;
  --grn-text-70: rgba(255, 255, 255, 0.7);
  --grn-text-40: rgba(255, 255, 255, 0.4);
  --grn-text-20: rgba(255, 255, 255, 0.2);
  --grn-text-10: rgba(255, 255, 255, 0.1);

  /* Borders */
  --grn-border: rgba(255, 255, 255, 0.2);
  --grn-border-subtle: rgba(255, 255, 255, 0.1);

  /* Motion */
  --grn-spring-snappy: cubic-bezier(0.34, 1.56, 0.64, 1);
  --grn-spring-smooth: cubic-bezier(0.25, 1, 0.5, 1);
  --grn-spring-subtle: cubic-bezier(0.22, 1, 0.36, 1);

  /* Blur tiers */
  --grn-blur-light: blur(5px);
  --grn-blur-medium: blur(10px);
  --grn-blur-heavy: blur(20px);

  /* Typography */
  --grn-font: 'Inter', system-ui, sans-serif;
  --grn-hero-size: clamp(32px, 4vw + 1rem, 6vw);
  --grn-body-size: clamp(16px, 1vw + 1rem, 1.1vw);
}
```

**Font:** Inter at weights 400, 500, 600. Always set `-webkit-font-smoothing: antialiased`.

## Layer Stack (Composability)

Every grainient page is a z-index stack of 6 layers:

```
Layer 0  z-index: 0    Body background (#000)
Layer 1  z-index: 1    Shader gradient canvas (position: fixed)
Layer 2  z-index: 2    Vignette overlay (position: fixed, pointer-events: none)
Layer 3  z-index: 3    Grid pattern overlay (position: fixed, pointer-events: none)
Layer 4  z-index: 10   Content sections (position: relative)
Layer 5  z-index: 100  Glassmorphism nav / floating UI (position: fixed)
```

Effects slot into layers. Content sections use surface colors (`--grn-surface`, `--grn-elevated`) for dark-on-dark elevation contrast.

See `references/composability.md` for composition recipes and performance budget.

## Implementation Rules

1. **Vanilla only.** No React, Vue, Svelte, Angular. Plain HTML + CSS + JS.
2. **Single-file output.** Everything in one HTML file. CDN imports for Inter font only.
3. **Dark-mode-first.** Body is `#000`. Surfaces elevate via `#141414` → `#1A1A1A` → `#2B2B2B`.
4. **`--grn-*` tokens everywhere.** Never hardcode colors — always reference custom properties.
5. **`prefers-reduced-motion` required.** Every animated effect needs a reduced-motion fallback.
6. **DPR clamp at 1.5** for WebGL canvas. Full DPR for CSS.
7. **`requestAnimationFrame` only.** Never `setInterval` for animation.
8. **`overflow: clip` over `overflow: hidden`** on individual containers, never on body.
9. **Inter font, antialiased.** No other fonts.

## Anti-Patterns

- Never use `ease` timing function — use `--grn-spring-*` cubic-bezier tokens
- Never use `box-shadow` with fewer than 4 layers — grainient shadows are deep stacks
- Never use `border` for the inset border system — use `box-shadow: inset 0 0 0 1px` or per-side gradients
- Never use `backdrop-filter` without a semi-transparent background — blur on opaque dark is invisible
- Never use `scroll-behavior: smooth` as a substitute for Lenis-style scroll — no inertia, no lerp control
- Never omit the vignette when using a shader background — content bleeds into shader without it
- Never hardcode pixel values for typography — always `clamp()` with viewport-relative middle
- Never use `opacity: 0` for hover-zoom initial state without `pointer-events: none`
- Never set all ticker columns to the same speed — vary by 10-30% per column
- Never use `perspective()` without `overflow: visible` on the container — clips 3D rotation
- Never use pure white (`#FFF`) as background anywhere — this is a dark-mode skill
- Never use Three.js for the fullscreen gradient — raw WebGL2 suffices; see rocaille-shader for Three.js needs

See `references/anti-patterns.md` for expanded explanations with code examples.

## Generator Script

```bash
python3 scripts/grainient_generator.py \
  --mode hero|bento|ticker|page|catalog \
  --accent "#C2F13C" \
  --bg "#000000" \
  --surface "#141414" \
  --output output.html
```

## Validation

```bash
python3 scripts/validate_grainient.py output.html
```

Checks: viewport meta, `--grn-*` properties, no framework imports, dark background, `requestAnimationFrame`, `prefers-reduced-motion`, Inter font, `overflow:clip`. Optional checks (pass if found): WebGL context, wheel listener, translateY, CSS grid, gradient CTA, box-shadow glow, backdrop-filter, vignette.

## References

Load on-demand when implementing specific effects:

| Reference | Covers |
|-----------|--------|
| `references/shader-gradient.md` | WebGL2 aurora shader: GLSL noise layers, setup, DPR, fallback |
| `references/vignette-system.md` | 4-directional CSS gradient overlays, z-index, opacity |
| `references/shadow-system.md` | 9-layer shadow recipe, lime/white glow variants |
| `references/smooth-scroll.md` | Lenis-style vanilla JS scroll, lerp math, rAF loop |
| `references/spring-animations.md` | 3 cubic-bezier presets, hover transitions |
| `references/hover-zoom.md` | overflow:clip + opacity+scale reveal pattern |
| `references/ticker-marquee.md` | Multi-column vertical ticker, speed variance |
| `references/surface-effects.md` | Glassmorphism, 3D card flip, bento grid, gradient CTAs |
| `references/detail-effects.md` | SVG gradient icons, inset borders, grid overlay, scrollbar, clamp typography |
| `references/color-system.md` | Full palette, CSS custom properties, dark-on-dark elevation |
| `references/composability.md` | Layer stack, composition recipes, performance budget |
| `references/anti-patterns.md` | 16+ anti-patterns with wrong/right code examples |

## Cross-Skill Relationships

- **rocaille-shader**: Cross-ref for Three.js shader path. Grainient owns CSS/surface effects, not shader pipelines.
- **minoan-frontend-design**: Broader creative direction. Grainient provides the dark-mode cinematic vocabulary.

## Attribution

Techniques derived from the Framer/WebGL dark-mode SaaS landing page pattern. Underlying technologies reimplemented from first principles: WebGL2 + GLSL simplex noise (Inigo Quilez), Lenis-style smooth scroll (vanilla JS), Framer Motion spring presets (CSS cubic-bezier approximations), glassmorphism (CSS backdrop-filter), multi-layer box shadow elevation (dark-on-dark depth).
