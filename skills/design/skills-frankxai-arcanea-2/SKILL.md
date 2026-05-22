---
name: arcanea-design-system
description: >
  Arcanea Cosmic Glass Design System v2.0.
  Generate UI code that strictly adheres to the Design Bible.
  Source of truth: .arcanea/design/DESIGN_BIBLE.md
version: 2.0.0
---

# Arcanea Design System v2.0 — Cosmic Glass

Use this system for ALL UI generation. Apple Liquid Glass + Cosmic Mythology + Premium SaaS.

## 1. Color Tokens (Tailwind)

### Backgrounds
| Token | Hex | Usage |
|-------|-----|-------|
| `bg-cosmic-void` | `#0b0e14` | Page backgrounds |
| `bg-cosmic-deep` | `#121826` | Card backgrounds |
| `bg-cosmic-surface` | `#1a2332` | Modals, popovers |
| `bg-cosmic-raised` | `#242f42` | Hover states |

### Brand
| Token | Hex | Usage |
|-------|-----|-------|
| `brand-primary` | `#8b5cf6` | Primary actions (Violet) |
| `brand-accent` / `crystal` | `#7fffd4` | Crystal highlights |
| `brand-gold` / `gold` | `#ffd700` | Achievement, premium |
| `brand-secondary` / `water` | `#78a6ff` | Secondary actions |

### Text
| Token | Hex | Contrast on void |
|-------|-----|------------------|
| `text-primary` | `#e6eefc` | 14.2:1 (AAA) |
| `text-secondary` | `#9bb1d0` | 7.5:1 (AAA) |
| `text-muted` | `#708094` | 4.8:1 (AA) |

## 2. Typography

| Font | Tailwind | Usage |
|------|----------|-------|
| **Cinzel** | `font-display` | h1, h2, hero headings |
| **Crimson Pro** | `font-body` | Narrative text (> 50 words) |
| **Inter** | `font-sans` | UI: buttons, labels, nav, forms |
| **JetBrains Mono** | `font-mono` | Code blocks, data |

Fluid scale: `text-fluid-xs` through `text-fluid-hero`

## 3. Glass Effects

### Standard Glass
```html
<div class="glass rounded-2xl p-6">Standard card</div>
<div class="glass-strong rounded-2xl p-6">Nav/modal</div>
<div class="glass-subtle rounded-xl p-4">Hover overlay</div>
```

### Liquid Glass (Apple 2026)
```html
<div class="liquid-glass rounded-3xl p-8">Premium surface</div>
<div class="liquid-glass-elevated rounded-3xl p-8">Hero card</div>
```

### Special Effects
```html
<div class="iridescent-glass rounded-3xl p-8">Rainbow-shift featured</div>
<div class="bubble-shine rounded-full w-24 h-24">Badge/orb</div>
```

## 4. Component Patterns

### Buttons
```tsx
// Primary
<button className="bg-brand-primary text-white rounded-lg px-4 py-2 font-medium shadow-glow-brand hover:scale-[1.02] transition-all duration-fast">
  Primary Action
</button>

// Crystal
<button className="bg-gradient-crystal text-cosmic-void rounded-lg px-4 py-2 font-medium shadow-glow-sm">
  Crystal Action
</button>

// Ghost
<button className="text-text-secondary hover:text-text-primary rounded-lg px-4 py-2 font-medium transition-colors">
  Ghost Action
</button>
```

### Cards
```tsx
// Standard
<div className="glass rounded-2xl p-6 hover-lift glow-card">
  <h3 className="font-display text-fluid-2xl text-gradient-crystal mb-4">Title</h3>
  <p className="font-sans text-fluid-base text-text-secondary">Description</p>
</div>

// Featured
<div className="liquid-glass rounded-3xl p-8 border-gradient">
  <h3 className="font-display text-fluid-3xl text-gradient-brand mb-4">Featured</h3>
</div>
```

### Gradient Text
```tsx
<h1 className="text-gradient-crystal">Crystal</h1>
<h1 className="text-gradient-brand">Violet → Crystal</h1>
<h1 className="text-gradient-fire">Fire → Gold</h1>
<h1 className="text-gradient-gold">Gold</h1>
```

## 5. Backgrounds
```tsx
// Page background
<div className="bg-cosmic-void bg-cosmic-mesh min-h-screen">

// Hero with mesh gradient
<section className="bg-mesh-gradient py-24 lg:py-32">

// Aurora atmospheric
<section className="bg-aurora py-24">
```

## 6. Motion (Framer Motion)

```tsx
// Cosmic fade in
const cosmicFadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6, ease: [0.22, 1, 0.36, 1] }
};

// Stagger container
const staggerContainer = {
  animate: { transition: { staggerChildren: 0.08 } }
};

// Hover
whileHover={{ scale: 1.02, y: -4 }}
transition={{ type: "spring", stiffness: 300, damping: 20 }}
```

## 7. Anti-Patterns

- Raw `#ffffff` text → use `text-primary` (#e6eefc)
- Emoji as icons → use Lucide React
- Space Grotesk → not in our type system
- Crystal as large bg fill → accent only
- Flat box-shadows → use elevation scale
- Hardcoded hex → use CSS variables or Tailwind tokens
- Skip cosmic depth ladder → void → deep → surface → raised

## Source of Truth

`.arcanea/design/DESIGN_BIBLE.md` — if anything conflicts, the Bible wins.
