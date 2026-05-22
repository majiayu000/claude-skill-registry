---
name: arcanea-design-system
description: Generate UI code that strictly adheres to the Arcanea Brand Guidelines (Cosmic, Glassmorphism, Crystal Accents)
---

# Arcanea Design System

Use this system for ALL UI generation.

## 1. Core Colors (Tailwind)

| Token | Hex | Usage |
|-------|-----|-------|
| `bg-cosmic-void` | `#0b0e14` | Page backgrounds |
| `bg-cosmic-deep` | `#121826` | Card backgrounds |
| `text-primary` | `#e6eefc` | Headings |
| `text-secondary` | `#9bb1d0` | Body text |
| `text-crystal` | `#7fffd4` | Primary brand accent |
| `border-crystal/20` | `rgba(127, 255, 212, 0.2)` | Glass borders |

## 2. Typography

- **Headings:** `font-cinzel` (Serif Display). Uppercase for H1/H2.
- **Body:** `font-inter` (Sans). Clean, readable.
- **Narrative:** `font-crimson-pro` (Serif). For lore text.
- **Code:** `font-jetbrains` (Mono).

## 3. The "Glass" Effect (Critical)

Never use flat backgrounds for cards. Use this stack:

```css
.glass {
  background: rgba(18, 24, 38, 0.7);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(127, 255, 212, 0.15);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}
```

## 4. Component Patterns

### Buttons
- **Primary:** `bg-gradient-to-r from-teal-400 to-blue-500 text-cosmic-void font-bold uppercase tracking-widest hover:shadow-[0_0_20px_rgba(127,255,212,0.4)]`
- **Secondary:** `border border-crystal/30 text-crystal hover:bg-crystal/10`

### Gradients
- **Text:** `bg-clip-text text-transparent bg-gradient-to-r from-teal-300 via-blue-400 to-purple-500`
- **Borders:** Use a pseudo-element or container to create gradient borders.

## 5. Motion (Framer Motion)

- **Hover:** `whileHover={{ scale: 1.02, y: -2 }}`
- **Entrance:** `initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, ease: "easeOut" }}`

## Example Component

```tsx
<div className="relative p-8 rounded-3xl overflow-hidden glass group">
  <div className="absolute inset-0 bg-gradient-to-br from-teal-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
  <h3 className="font-cinzel text-2xl text-transparent bg-clip-text bg-gradient-to-r from-tea-200 to-teal-400 mb-4">
    The First Gate
  </h3>
  <p className="font-crimson-pro text-lg text-secondary leading-relaxed">
    Begin your journey where the roots meet the stone.
  </p>
</div>
```
