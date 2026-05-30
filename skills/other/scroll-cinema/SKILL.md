---
name: scroll-cinema
description: "Generate cinematic scrolltelling websites where scroll drives the narrative: Lenis smooth scroll, GSAP ScrollTrigger cinematic section reveals with fluid OKLCH color transitions, Three.js painted-texture shader backgrounds reactive to cursor, scroll, velocity, and chapter progress. Four modes — chapter-reveal (scroll-paced storytelling), painted-backdrop (reactive shader canvas), full-cinema (complete cinematic site), catalog (all shader presets side by side). This skill should be used when building storytelling websites, scroll-driven experiences, cinematic landing pages, or any page where sections reveal as chapters with color transitions and ambient 3D backgrounds. Triggers on scrollytelling, cinematic scroll, scroll-driven storytelling, Lenis smooth scroll, GSAP ScrollTrigger, scroll chapter reveal, scroll color transition, painted shader background, narrative scroll website, premium scroll experience, shader catalog."
argument-hint: "[--mode chapter-reveal|painted-backdrop|full-cinema|catalog] [--shader painted-dots|watercolor|domain-warp] [--entrance fade-up|split-text|scale-reveal|clip-path-wipe] [--chapters N] [story description]"
---

# Scroll Cinema

Generate premium scrollytelling websites where scroll is the narrative engine. Three libraries coordinate as a unified system: Lenis provides buttery smooth locomotion, GSAP ScrollTrigger orchestrates cinematic section reveals with fluid color transitions, and Three.js renders a living painted-texture background that reacts to cursor position and scroll progress.

This is NOT a general animation skill, a 3D product viewer, or a scroll-hijacking pattern. Scroll-cinema produces pages where the reader moves through chapters — each chapter entrance is choreographed, the color palette flows between sections, and an ambient shader canvas breathes behind the content.

## Quick Start

```bash
# Complete cinematic storytelling site
python3 ~/.claude/skills/scroll-cinema/scripts/scroll_cinema_generator.py \
  --mode full-cinema \
  --shader painted-dots \
  --chapters 5 \
  --pacing medium \
  --output story.html

# Chapter reveals with color transitions (no Three.js)
python3 ~/.claude/skills/scroll-cinema/scripts/scroll_cinema_generator.py \
  --mode chapter-reveal \
  --chapters 4 \
  --output chapters.html

# Standalone reactive shader background
python3 ~/.claude/skills/scroll-cinema/scripts/scroll_cinema_generator.py \
  --mode painted-backdrop \
  --shader watercolor \
  --output backdrop.html

# All three shader presets side by side
python3 ~/.claude/skills/scroll-cinema/scripts/scroll_cinema_generator.py \
  --mode catalog \
  --output catalog.html

```

Or describe a concept and let Claude generate directly from the templates and references.

Example: `/scroll-cinema a story about the Mediterranean told in five chapters — from dawn on the Aegean to dusk on the Strait of Sicily`

## Modes

| Mode | Output | Libraries |
|------|--------|-----------|
| `chapter-reveal` | Multi-section storytelling page with cinematic entrances and fluid color transitions | Lenis + GSAP ScrollTrigger + OKLCH color system |
| `painted-backdrop` | Three.js shader canvas reactive to cursor + scroll, standalone or embeddable | Three.js + GLSL + scroll-fed uniforms |
| `full-cinema` | Complete cinematic scrolltelling site — all systems integrated | Lenis + GSAP + Three.js + color system |
| `catalog` | All three shader presets rendered side by side with one WebGL context | Lenis + GSAP + Three.js (scissor test) |

## Core Architecture

```
┌──────────────┐     autoRaf: false      ┌─────────────────┐
│    Lenis     │ ──── lenis.raf(time) ──→ │   GSAP Ticker   │
│ (smooth DOM  │ ←── drives animation ─── │ (master clock)  │
│  scrolling)  │                          └────────┬────────┘
└──────┬───────┘                                   │
       │                                    ┌──────▼──────┐
       │ lenis.on('scroll')                 │ ScrollTrigger│
       │ → ScrollTrigger.update()           │ (orchestrate │
       │                                    │  sections)   │
       │                                    └──────┬───────┘
       │                                           │
       │  scroll progress                          │ drives
       │  + cursor position                        │
       ▼                                           ▼
┌──────────────┐                          ┌────────────────┐
│  Three.js    │                          │ Section Reveals │
│  Shader      │ ← uniforms: uScroll,    │ Color Interp.   │
│  Background  │   uMouse, uTime         │ Typography Anim │
└──────────────┘                          └────────────────┘
```

**Non-negotiable initialization sequence** — the single most important pattern in this skill:

```js
// 1. Register GSAP plugins FIRST
gsap.registerPlugin(ScrollTrigger);

// 2. Init Lenis with autoRaf OFF — GSAP drives the loop
const lenis = new Lenis({ autoRaf: false });

// 3. Connect Lenis to GSAP ticker (single animation frame)
gsap.ticker.add((time) => {
  lenis.raf(time * 1000); // GSAP=seconds, Lenis=ms
});
gsap.ticker.lagSmoothing(0);

// 4. Sync ScrollTrigger with Lenis scroll position
lenis.on('scroll', ScrollTrigger.update);
```

Full integration details, cleanup, and SPA lifecycle: `references/lenis-gsap-integration.md`

## Shader Presets

| Preset | Technique | Performance | Feel |
|--------|-----------|-------------|------|
| `painted-dots` | Dot-grid with mouse-reactive ripple, scroll-driven density | Lightest | Subtle, editorial, clean |
| `watercolor` | NPR Kuwahara-style edge-preserving filter + procedural noise | Medium | Organic, painterly, warm |
| `domain-warp` | Progressive sinusoidal domain warping | Lightest | Flowing, abstract, psychedelic at high iterations |

All shaders receive these uniforms from the orchestration layer:
- `uTime` — elapsed time from GSAP ticker
- `uMouse` — normalized cursor position, lerped at 0.08 for smoothness
- `uScroll` — Lenis smoothed scroll progress (0.0–1.0), lerped at 0.05
- `uVelocity` — scroll velocity magnitude (0.0–1.0), clamped ±3 then normalized, lerped at 0.10
- `uChapter` — smooth chapter index float, lerped at 0.03
- `uMobile` — 1.0 on viewports ≤768px, 0.0 otherwise (watercolor uses this to skip edge detection)
- `uResolution` — viewport dimensions for aspect correction
- `uChapterHue` / `uChapterLightness` — chapter color sync, lerped at 0.03

Full GLSL code, uniform pipeline, and lerp rates: `references/painted-shader-patterns.md`

## Color System

Scroll-driven color transitions between chapters using OKLCH interpolation. sRGB interpolation produces muddy brown midpoints when transitioning between hues — OKLCH maintains perceptual uniformity.

Each chapter defines a palette via data attributes:
```html
<section data-chapter="0" data-hue="250" data-chroma="0.15" data-lightness="0.25">
```

GSAP ScrollTrigger tweens CSS custom properties registered via `@property` for GPU-accelerated animation. Fallback to HSL interpolation where OKLCH is unsupported.

Full color system, @property registration, fallback strategy: `references/color-interpolation.md`

## Cinematic Easings

Four custom easing curves for scroll-driven cinematic animation:

| Curve | Cubic-Bezier | Feel | Best For |
|-------|-------------|------|----------|
| `cinematicSilk` | `0.45,0.05,0.55,0.95` | Luxurious slow in/out | Hero reveals, title entrances |
| `cinematicSmooth` | `0.25,0.1,0.25,1` | Natural deceleration | Section fade-ins, content blocks |
| `cinematicFlow` | `0.33,0,0.2,1` | Apple-like momentum | Parallax layers, camera moves |
| `cinematicLinear` | `0.4,0,0.6,1` | Subtle ease | Color shifts, background opacity |

Timing philosophy and ScrollTrigger scrub values: `references/cinematic-easings.md`

## Composition Parameters

| Parameter | Range | Default | Effect |
|-----------|-------|---------|--------|
| `--mode` | `chapter-reveal\|painted-backdrop\|full-cinema\|catalog` | `full-cinema` | Output mode |
| `--shader` | `painted-dots\|watercolor\|domain-warp` | `painted-dots` | Shader preset (modes with Three.js) |
| `--chapters` | `2–8` | `5` | Number of story chapters |
| `--entrance` | `fade-up\|split-text\|scale-reveal\|clip-path-wipe` | `fade-up` | Section entrance animation (chapter modes) |
| `--pacing` | `slow\|medium\|fast` | `medium` | Scroll height multiplier: slow=1.5×, fast=0.6× |
| `--color-scheme` | `dark\|light` | `dark` | Background/foreground polarity |
| `--font` | font name | `Geist` | Primary display font (Google Fonts CDN) |
| `--accent` | hex color | — | Override accent color |
| `--output` | path | `output.html` | Output file path |

## Chapter Structure

Each chapter is a `<section>` element with sticky content. Minimum height scales with pacing. Entrance animations complete within the first 30% of the chapter's scroll distance — the reader never waits.

Section entrance patterns: fade-up (default), split-text, scale-reveal, clip-path-wipe.

Full chapter architecture, scroll pacing table, responsive layout: `references/chapter-structure.md`
Design tokens (colors, typography, spacing, animation): `references/design-tokens.md`

## Gotchas — What Claude Gets Wrong Without This Skill

1. **Initializes Lenis with `autoRaf: true` alongside GSAP.** Causes dual animation loops, stuttering, incorrect trigger firing. Must set `autoRaf: false` and let GSAP drive.
2. **Interpolates chapter colors in sRGB.** Produces muddy brown midpoints. Must use OKLCH or at minimum HSL.
3. **Feeds raw scroll position to Three.js shaders.** Produces jerky backgrounds. Must lerp the scroll value (rate 0.05).
4. **Creates separate `requestAnimationFrame` loops** for Three.js and GSAP. Must share a single tick via `gsap.ticker.add()`.
5. **Uses ScrollSmoother instead of Lenis.** ScrollSmoother requires GSAP Club (paid). Lenis is free and equivalent.
6. **Uses default GSAP easings.** They feel robotic for cinematic scroll. Must define cinematicSilk/Smooth/Flow/Linear custom curves.
7. **Animates CSS `background-color` per section.** Expensive repaint. Must use CSS custom properties with `@property` for GPU acceleration.
8. **Forgets cleanup in SPA contexts.** Lenis, ScrollTrigger, and Three.js all need explicit `.destroy()` on unmount.
9. **Uses `position: fixed` for the Three.js canvas inside the Lenis scroll wrapper.** Fixed-position children inside a transformed parent resolve relative to the parent. Canvas must be a sibling of (not child of) the scroll content wrapper.
10. **Puts text content inside the Three.js scene.** Text should be HTML overlay — Three.js is background only. Content must be accessible without WebGL.
11. **Omits `prefers-reduced-motion`.** Must disable all animation, show final states, revert Lenis to native scroll.
12. **Leaves `will-change` on permanently.** GPU memory leak. Add before animation, remove after completion.
13. **Missing `gsap.ticker.lagSmoothing(0)`.** Causes visible jumps in Lenis's smooth interpolation during lag frames.

Full anti-pattern catalog with wrong/right code examples: `references/anti-patterns.md`

## Implementation Rules

1. **Vanilla only.** No React, Vue, Svelte. Plain HTML + CSS + JS. CDN imports for Three.js, GSAP, Lenis.
2. **Single-file output.** Everything in one HTML file. CDN imports only.
3. **Single animation loop.** GSAP ticker drives everything — Lenis, ScrollTrigger, Three.js render. No separate rAF.
4. **`performance.now()` for timing.** Never `Date.now()` in animation loops.
5. **`prefers-reduced-motion` required.** Every animated effect shows final state immediately. Shader animation freezes. Lenis reverts to native scroll.
6. **Semantic HTML chapters.** `<section>` with headings, readable without JS. Three.js canvas is `aria-hidden="true"`.
7. **OKLCH color interpolation** with sRGB/HSL fallback. Never animate `background-color` directly — use `@property`-registered custom properties.
8. **`--sc-*` token prefix** for all CSS custom properties. Never hardcode colors or timing.
9. **Lerped shader uniforms.** Never feed raw values — smooth with lerp at rates defined in design tokens.
10. **Device pixel ratio capped at 2.0** on desktop, 1.5 on mobile. `Math.min(window.devicePixelRatio, isMobile ? 1.5 : 2.0)`.
11. **Viewport meta required.** `<meta name="viewport" content="width=device-width, initial-scale=1">`.
12. **Resize handler.** Update renderer size, resolution uniform, camera aspect. Debounced 80ms. Call `setPixelRatio()` before `setSize()` to avoid double framebuffer allocation.
13. **Single global export.** `window.__scCleanup` is the sole intentional global — a cleanup function for SPA integration. All other state lives in module scope.

## Cross-Skill Relationships

- **`threejs-particle-canvas`**: scroll-cinema's painted backdrop produces the *background canvas*. threejs-particle-canvas produces *ambient contemplative experiences*. If scroll drives the narrative → scroll-cinema. If the canvas IS the experience → threejs-particle-canvas.
- **`conductor-motion`**: conductor-motion owns behavioral simulations (typewriter, progress bars). Scroll-cinema owns cinematic section choreography. A scroll-cinema page may embed conductor-motion patterns within individual sections.
- **`rocaille-shader`**: rocaille-shader's domain warping GLSL serves as the `domain-warp` preset upstream. Scroll-cinema orchestrates it with scroll. If standalone shader art → rocaille-shader. If scroll-driven background → scroll-cinema.
- **`grainient`**: grainient owns CSS surface effects (shadows, glass, aurora). Scroll-cinema owns scroll-driven orchestration. A scroll-cinema page may use grainient palettes. No overlap — grainient is 2D CSS, scroll-cinema is the 3D+scroll orchestration layer.
- **`shape` / `design-md`**: Upstream. `.design-context.md` and `DESIGN.md` feed color palette and typography into scroll-cinema. If `.design-context.md` exists with MOTION_INTENSITY dial, derive pacing from it (1-3 → slow, 4-6 → medium, 7-10 → fast).

## CDN Versions

Pin these versions for stability:
```html
<!-- Lenis 1.2.3 -->
<script src="https://unpkg.com/lenis@1.2.3/dist/lenis.min.js"></script>
<link rel="stylesheet" href="https://unpkg.com/lenis@1.2.3/dist/lenis.css">

<!-- GSAP 3.12 + ScrollTrigger + CustomEase -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12/dist/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12/dist/CustomEase.min.js"></script>

<!-- Three.js r170 -->
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js"
  }
}
</script>
```

## References

Load on-demand when implementing specific aspects:

| Working on... | Load |
|---|---|
| Lenis + GSAP init, cleanup, SPA lifecycle | `references/lenis-gsap-integration.md` |
| Custom easing curves, scroll timing | `references/cinematic-easings.md` |
| Three.js shader presets, GLSL code, uniform pipeline | `references/painted-shader-patterns.md` |
| OKLCH color system, @property, fallbacks | `references/color-interpolation.md` |
| Chapter HTML structure, sticky sections, pacing | `references/chapter-structure.md` |
| Wrong/right code examples | `references/anti-patterns.md` |
| CSS custom properties, typography, responsive | `references/design-tokens.md` |

## Validation

```bash
python3 ~/.claude/skills/scroll-cinema/scripts/validate_scroll_cinema.py output.html
```

Checks: Lenis CDN, GSAP CDN, Three.js CDN (if applicable), `autoRaf: false`, `gsap.ticker.add` with `lenis.raf`, `ScrollTrigger.update` in scroll callback, `prefers-reduced-motion` media query, `aria-hidden` on canvas, no `setInterval` for animation, viewport meta, no `transition: all`, semantic section elements, `--sc-*` custom properties, no standalone `requestAnimationFrame`, no raw scroll in uniforms, no direct `backgroundColor` animation, SRI integrity hashes, cleanup function, scroll-driven entrance animations with `toggleActions`, entrance reduced-motion gating.

