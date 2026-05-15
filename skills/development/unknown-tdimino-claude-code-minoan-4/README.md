# grainient

16 composable dark-mode visual effects as single-file HTML pages. WebGL2 shaders, CSS surface depth, JS-driven motion, and layout patterns — all via `--grn-*` CSS custom properties. No framework dependencies, no build step.

## Effects

| # | Effect | Tech | Tier |
|---|--------|------|------|
| 1 | WebGL Shader Gradient | WebGL2 + GLSL simplex noise FBM | Hero |
| 2 | Vignette Overlay | CSS linear-gradient (4-directional) | Hero |
| 3 | 9-Layer Box Shadows | CSS box-shadow (lime/white glow variants) | Hero |
| 4 | Smooth Scroll | Vanilla JS (Lenis-style lerp, rAF) | Motion |
| 5 | Spring Animations | CSS cubic-bezier (3 presets: snappy, smooth, subtle) | Motion |
| 6 | Hover Image Zoom | CSS overflow:clip + scale transition | Motion |
| 7 | Vertical Ticker Marquee | JS translateY + DOM reordering | Motion |
| 8 | Glassmorphism | CSS backdrop-filter (3 blur tiers) | Surface |
| 9 | 3D Perspective Card Flip | CSS perspective + rotateY + backface-visibility | Surface |
| 10 | Bento Grid | CSS Grid (mixed spans, dark-on-dark elevation) | Surface |
| 11 | Gradient CTAs | CSS linear-gradient + inset glow box-shadow | Surface |
| 12 | SVG Gradient Icons | SVG linearGradient (gold + lime palettes) | Detail |
| 13 | Inset Border System | CSS box-shadow: inset (not border) | Detail |
| 14 | Grid Pattern Overlay | CSS repeating-linear-gradient crosshatch | Detail |
| 15 | Custom Scrollbar | CSS ::-webkit-scrollbar + scrollbar-width | Detail |
| 16 | Responsive Clamp Typography | CSS clamp() with viewport-relative middle | Detail |

## Modes

| Mode | Template | Composition |
|------|----------|-------------|
| `hero` | `hero-section.html` | Shader + vignette + glassmorphism nav + clamp typography + springs |
| `bento` | `bento-showcase.html` | Bento grid + 9-layer shadows + hover zoom + glassmorphism + gradient CTAs |
| `ticker` | `ticker-landing.html` | Ticker marquee + smooth scroll + gradient CTAs + vignette + SVG icons |
| `page` | `dark-page.html` | All 16 effects composed into a full landing page |
| `catalog` | `effects-catalog.html` | Each effect demonstrated individually with interactive controls |

## Architecture

```
grainient/
├── SKILL.md                              Skill definition (triggers, rules, anti-patterns)
├── README.md                             This file
├── scripts/
│   ├── grainient_generator.py            Generator: --mode hero|bento|ticker|page|catalog
│   └── validate_grainient.py             Structural validator (22 checks)
├── assets/templates/
│   ├── hero-section.html                 WebGL2 aurora shader + glassmorphism nav (~530 lines)
│   ├── bento-showcase.html               Bento grid + 9-layer shadows + hover zoom (~480 lines)
│   ├── ticker-landing.html               Vertical ticker + smooth scroll + CTAs (~530 lines)
│   ├── dark-page.html                    Full composition of all 16 effects (~1,560 lines)
│   └── effects-catalog.html              Interactive catalog with per-effect controls (~2,460 lines)
└── references/
    ├── shader-gradient.md                WebGL2 setup, GLSL noise, 6-layer architecture, DPR
    ├── vignette-system.md                4-directional gradient overlays, z-index
    ├── shadow-system.md                  9-layer recipe, lime/white glow variants
    ├── smooth-scroll.md                  Lenis-style vanilla JS, lerp math, rAF
    ├── spring-animations.md              3 cubic-bezier presets, IntersectionObserver entry
    ├── hover-zoom.md                     overflow:clip + opacity+scale reveal
    ├── ticker-marquee.md                 Multi-column vertical ticker, speed variance
    ├── surface-effects.md                Glassmorphism, 3D card flip, bento, CTAs
    ├── detail-effects.md                 SVG icons, inset borders, grid overlay, scrollbar, typography
    ├── color-system.md                   Full palette, --grn-* tokens, elevation strategy
    ├── composability.md                  6-layer z-index stack, recipes, performance budget
    ├── anti-patterns.md                  17 anti-patterns with wrong/right code examples
    └── glass-hero-palette.md             Glass Hero palette preset: mint/violet tokens, Geist typography
```

## Usage

```bash
# Generate a hero section with WebGL aurora shader
python3 scripts/grainient_generator.py --mode hero --output hero.html

# Full landing page with all 16 effects
python3 scripts/grainient_generator.py --mode page --output landing.html

# Custom accent color (default: lime #C2F13C)
python3 scripts/grainient_generator.py --mode bento --accent "#FF6B35" --output showcase.html

# Interactive effects catalog
python3 scripts/grainient_generator.py --mode catalog --output catalog.html

# Validate output
python3 scripts/validate_grainient.py hero.html
```

### Generator Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--mode` | (required) | `hero`, `bento`, `ticker`, `page`, `catalog` |
| `--accent` | `#C2F13C` | Primary accent hex (use `#57FFA8` for glass-hero palette) |
| `--bg` | `#000000` | Body background hex |
| `--surface` | `#141414` | Surface elevation hex |
| `--font` | `Inter` | Body font family |
| `--output` | stdout | Output file path |

### Validator

Runs 22 checks (11 required, 11 optional):

**Required:** viewport meta, Inter font, `--grn-*` tokens, dark background, font smoothing, `prefers-reduced-motion`, spring cubic-bezier, responsive CSS, no framework imports, no `setInterval` animation, no `ease` timing.

**Optional (mode-specific):** WebGL context, `requestAnimationFrame`, wheel listener, `translateY`, CSS Grid, `overflow:clip`, gradient CTA, box-shadow glow, backdrop-filter, vignette divs, custom scrollbar.

## Color System

All effects read from `--grn-*` CSS custom properties. Override at `:root` to re-theme:

| Token | Default | Role |
|-------|---------|------|
| `--grn-bg` | `#000000` | Body background |
| `--grn-surface` | `#141414` | Card/section backgrounds |
| `--grn-elevated` | `#1A1A1A` | Elevated surfaces |
| `--grn-card` | `#2B2B2B` | Card backgrounds |
| `--grn-accent` | `#C2F13C` | Primary accent (lime) |
| `--grn-accent-40` | `rgba(194,241,60,0.4)` | Accent at 40% opacity |
| `--grn-accent-20` | `rgba(194,241,60,0.2)` | Accent at 20% opacity |
| `--grn-text` | `#FFFFFF` | Primary text |
| `--grn-text-70` | `rgba(255,255,255,0.7)` | Secondary text |
| `--grn-text-40` | `rgba(255,255,255,0.4)` | Muted text |
| `--grn-border` | `rgba(255,255,255,0.2)` | Standard border |
| `--grn-border-subtle` | `rgba(255,255,255,0.1)` | Subtle border |
| `--grn-spring-snappy` | `cubic-bezier(0.34,1.56,0.64,1)` | Buttons, toggles |
| `--grn-spring-smooth` | `cubic-bezier(0.25,1,0.5,1)` | Image zoom, galleries |
| `--grn-spring-subtle` | `cubic-bezier(0.22,1,0.36,1)` | Card reveals, hovers |
| `--grn-blur-light` | `blur(5px)` | Subtle overlays |
| `--grn-blur-medium` | `blur(10px)` | Panels |
| `--grn-blur-heavy` | `blur(20px)` | Navigation |

## Layer Stack

Every grainient page is a z-index stack of 6 layers:

```
Layer 0  z-index: 0    Body background (#000)
Layer 1  z-index: 1    WebGL shader canvas (position: fixed)
Layer 2  z-index: 2    Vignette overlay (position: fixed, pointer-events: none)
Layer 3  z-index: 3    Grid pattern overlay (position: fixed, pointer-events: none)
Layer 4  z-index: 10   Content sections (position: relative)
Layer 5  z-index: 100  Glassmorphism nav (position: fixed)
```

## Key Constraints

- **Vanilla only.** No React, Vue, Svelte, Angular. Plain HTML + CSS + JS.
- **Single-file output.** Everything in one `.html` file. CDN for Inter font only.
- **Dark-mode-first.** Body `#000`, surfaces elevate via `#141414` → `#1A1A1A` → `#2B2B2B`.
- **`requestAnimationFrame` only.** Never `setInterval` for animation.
- **`prefers-reduced-motion` required.** Every animated effect needs a fallback.
- **DPR clamp at 1.5** for WebGL canvas (full DPR for CSS).
- **Spring timing only.** Never use `ease` — always `--grn-spring-*` cubic-bezier tokens.
- **`overflow: clip` over `overflow: hidden`** on containers (never on body).

## Palette Presets

The default lime green (`#C2F13C`) can be swapped for alternative palettes:

**Glass Hero (Mint/Violet):** Mint green `#57FFA8` accent, violet `#A78BFA` secondary, blue-tinted near-black `#0a0a0c` base. See `references/glass-hero-palette.md` for the full token block, Geist typography, and glassmorphism recipes. For the full 3D glass experience, use threejs-particle-canvas Mode 6.

## Cross-Skill Relationships

- **rocaille-shader** — Three.js shader path. Grainient uses raw WebGL2 for the fullscreen gradient; rocaille-shader owns the Three.js pipeline.
- **minoan-frontend-design** — Broader creative direction. Grainient provides the dark-mode cinematic vocabulary.
- **threejs-particle-canvas Mode 6 (glass-hero)** — Full 3D glass with MeshPhysicalMaterial refraction, dispersion, iridescence. Grainient's glass-hero palette provides the flat CSS equivalent.

## Attribution

Techniques derived from the Framer/WebGL dark-mode SaaS landing page pattern. Underlying technologies reimplemented from first principles:

- **WebGL2 aurora shader** — GLSL simplex noise from [Inigo Quilez](https://iquilezles.org/articles/warp/) (iq / Shadertoy), FBM layering
- **Smooth scroll** — Lenis-style inertial scrolling (vanilla JS, lerp interpolation)
- **Spring animations** — Framer Motion spring presets approximated as CSS cubic-bezier curves
- **Glassmorphism** — CSS `backdrop-filter` with semi-transparent dark backgrounds
- **9-layer box shadows** — Multi-layer elevation system for dark-on-dark depth
- **Ticker marquee** — DOM-reordering infinite scroll pattern with speed variance
- **Glass Hero palette** — Color system and glassmorphism recipes deconstructed from [kaolti's glass-hero experiment](https://experiments.thisiswhitespace.com/glass-hero) (thisiswhitespace.com, May 2026)
