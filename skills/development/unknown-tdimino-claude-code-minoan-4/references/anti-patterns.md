# Anti-Patterns

## 1. Framework imports

**Wrong:** `import React from 'react'`
**Right:** Vanilla HTML + CSS + JS only.

## 2. `ease` timing function

**Wrong:** `transition: transform 0.3s ease`
**Right:** `transition: transform 0.6s var(--grn-spring-snappy)`

## 3. White background

**Wrong:** `background: #FFF`
**Right:** `background: var(--grn-bg)` (#000). This is a dark-mode skill.

## 4. Shallow box shadows

**Wrong:** `box-shadow: 0 2px 4px rgba(0,0,0,0.1)`
**Right:** Use the 9-layer recipe from `shadow-system.md`. Minimum 4 layers.

## 5. Standard `border`

**Wrong:** `border: 1px solid rgba(255,255,255,0.2)`
**Right:** `box-shadow: inset 0 0 0 1px var(--grn-border-subtle)` — no box model changes.

## 6. `backdrop-filter` without transparency

**Wrong:** `backdrop-filter: blur(20px); background: #141414`
**Right:** `backdrop-filter: blur(20px); background: rgba(0,0,0,0.7)` — blur on opaque is invisible.

## 7. `scroll-behavior: smooth`

**Wrong:** `html { scroll-behavior: smooth; }`
**Right:** Lenis-style JS scroll with lerp. No inertia or control with CSS.

## 8. Shader without vignette

**Wrong:** Shader canvas alone — content bleeds into shader.
**Right:** Always pair with 4-directional vignette overlays.

## 9. Hardcoded typography

**Wrong:** `font-size: 48px`
**Right:** `font-size: clamp(32px, 4vw + 1rem, 6vw)` — viewport-responsive.

## 10. Hover zoom without pointer-events

**Wrong:** `opacity: 0` overlay without `pointer-events: none` — captures clicks.
**Right:** Add `pointer-events: none` to initial state.

## 11. Uniform ticker speeds

**Wrong:** All columns at `speed: 0.5` — looks mechanical.
**Right:** Vary 10-30% per column (0.45, 0.50, 0.55, 0.60, 0.48).

## 12. `perspective` with `overflow: hidden`

**Wrong:** `perspective: 1200px; overflow: hidden` — clips 3D rotation.
**Right:** `perspective: 1200px; overflow: visible`.

## 13. `setInterval` for animation

**Wrong:** `setInterval(render, 16)`
**Right:** `requestAnimationFrame(render)` — syncs with display refresh.

## 14. Dark shadows on dark

**Wrong:** `box-shadow: 0 4px 12px rgba(0,0,0,0.3)` on #000 — invisible.
**Right:** Use colored glow (lime or white) for visible elevation.

## 15. Glassmorphism on opaque card

**Wrong:** `backdrop-filter: blur(10px)` on `background: #1A1A1A` — no visible effect.
**Right:** Card must have transparency for blur to show through.

## 16. Vignette color mismatch

**Wrong:** Vignette fades to `#000` when surface is `#141414` — visible seam.
**Right:** Vignette color must match `var(--grn-surface)` exactly.

## 17. Three.js for 2D gradient

**Wrong:** Import Three.js (600KB) for a fullscreen fragment shader.
**Right:** Raw WebGL2 — canvas + context + fullscreen quad + GLSL. See `rocaille-shader` for Three.js needs.
