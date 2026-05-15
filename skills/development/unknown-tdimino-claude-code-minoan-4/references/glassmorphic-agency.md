# Glassmorphic Agency

Dark-mode CSS patterns from jades.agency — scroll-driven blur
entrances, glassmorphic card layering, and group-hover compound
transitions. CSS-first with a single Three.js canvas as the only
GPU-heavy asset. Source: Next.js App Router + Tailwind v4 + Three.js r183.

## 1. Blur-Entrance System (Scroll-Driven)

```css
/* Initial state */
opacity: 0;
filter: blur(8-18px);
transform: translateY(10-42px);

/* Resolved state */
opacity: 1;
filter: blur(0);
transform: none;
```

- JS scroll-position interpolator drives inline styles
- Single easing: `cubic-bezier(0.22, 1, 0.36, 1)` (≈easeOutExpo)
- Blur range creates depth-of-field entrance effect

## 2. Glassmorphic Card Recipe

```css
backdrop-filter: blur(12px);         /* backdrop-blur-md */
background: rgba(255,255,255,0.05);  /* bg-foreground/5 */
border: 1px solid rgba(255,255,255,0.1); /* border-white/10 */
box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); /* shadow-2xl */
background-image: linear-gradient(to bottom right,
  rgba(255,255,255,0.05), rgba(255,255,255,0.1));
```

## 3. Group-Hover Card Compound

```html
<div class="group">
  <!-- Foreground: reveals on hover -->
  <div class="blur-sm opacity-0 scale-95
    group-hover:blur-0 group-hover:scale-100 group-hover:opacity-100
    transition-[opacity,transform,filter]"
    style="transition-timing-function: cubic-bezier(0.22, 1, 0.36, 1)">
  </div>
  <!-- Background: recedes on hover -->
  <div class="group-hover:scale-[0.92] group-hover:opacity-0
    transition-[opacity,transform]">
  </div>
</div>
```

## 4. Alpha Transparency Scale

`/5` → `/10` → `/18` → `/72` → `/85`

Depth via alpha multipliers, not z-index stacking.

For grainient's own 3-tier glassmorphism system with `--grn-*` tokens, see `surface-effects.md` #8.
