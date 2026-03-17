---
name: vibe-designer
description: Create stunning, modern web designs with aurora effects, glassmorphism, neon glows, and sophisticated aesthetics. Perfect for developer tools, dashboards, and apps targeting vibe coders who appreciate refined, atmospheric UI.
license: MIT
---

This skill creates sophisticated, atmospheric web interfaces that resonate with modern developers and "vibe coders." Focus on creating memorable, polished designs with depth, glow effects, and intentional aesthetics.

The user provides design requirements: a component, page, dashboard, or full application. They may specify mood, colors, or technical constraints.

## Design Philosophy

Before coding, establish a clear **aesthetic direction**:

### Mood Selection
Choose a primary mood that drives all decisions:
- **Aurora/Cosmic**: Animated gradients, mesh backgrounds, space-inspired depth
- **Neon Cyber**: Electric glows, sharp contrasts, futuristic terminals
- **Glass Premium**: Refined glassmorphism, frosted layers, subtle luxury
- **Minimal Dark**: Deep blacks, precise typography, intentional whitespace
- **Warm Terminal**: Cozy developer vibes, amber/green accents, retro-modern
- **Vapor Wave**: Pink/cyan gradients, nostalgic 80s/90s aesthetic, dreamy

### Core Questions
- **Who is this for?** Developers, designers, power users, general audience?
- **What feeling should it evoke?** Professional, playful, mysterious, trustworthy, cutting-edge?
- **What's the one memorable element?** Every great design has a signature moment.

## Color System Architecture

### Dark Theme Foundations (Recommended for Vibe Coders)

Build depth with layered backgrounds:
```css
:root {
    /* Background layers - darkest to lightest */
    --bg-void: #05020a;      /* Deepest black with color tint */
    --bg-deep: #0a0812;      /* Base layer */
    --bg-primary: #0f0c18;   /* Main content background */
    --bg-secondary: #161224; /* Cards, elevated surfaces */
    --bg-tertiary: #1e1830;  /* Hover states, highlights */
    --bg-elevated: #261e40;  /* Highest elevation */
}
```

### Accent Color Palettes

**Purple/Violet (Linear, Raycast style)**
```css
--accent-primary: #a855f7;
--accent-secondary: #8b5cf6;
--accent-glow: rgba(168, 85, 247, 0.5);
```

**Cyan/Teal (Terminal, tech style)**
```css
--accent-primary: #06b6d4;
--accent-secondary: #22d3ee;
--accent-glow: rgba(6, 182, 212, 0.5);
```

**Emerald/Green (Nature, success style)**
```css
--accent-primary: #10b981;
--accent-secondary: #34d399;
--accent-glow: rgba(16, 185, 129, 0.5);
```

**Rose/Pink (Creative, playful style)**
```css
--accent-primary: #f43f5e;
--accent-secondary: #fb7185;
--accent-glow: rgba(244, 63, 94, 0.5);
```

**Amber/Gold (Warm, premium style)**
```css
--accent-primary: #f59e0b;
--accent-secondary: #fbbf24;
--accent-glow: rgba(245, 158, 11, 0.5);
```

### Text Hierarchy
Always tint text colors to match the accent:
```css
--text-primary: #f0eef5;    /* Main text - warm white */
--text-secondary: #a8a3b5;  /* Secondary - muted */
--text-tertiary: #6b6578;   /* Subtle labels */
--text-muted: #443d52;      /* Disabled, hints */
```

## Background Effects

### Aurora/Mesh Gradients
Create atmospheric depth with layered animated gradients:

```css
/* Multi-point mesh gradient */
--mesh-gradient:
    radial-gradient(at 40% 20%, rgba(168, 85, 247, 0.3) 0px, transparent 50%),
    radial-gradient(at 80% 0%, rgba(139, 92, 246, 0.2) 0px, transparent 50%),
    radial-gradient(at 0% 50%, rgba(217, 70, 239, 0.15) 0px, transparent 50%),
    radial-gradient(at 80% 50%, rgba(6, 182, 212, 0.08) 0px, transparent 50%),
    radial-gradient(at 0% 100%, rgba(168, 85, 247, 0.2) 0px, transparent 50%);

body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: var(--mesh-gradient);
    animation: aurora-drift 25s ease-in-out infinite;
    pointer-events: none;
}

@keyframes aurora-drift {
    0%, 100% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(-1%, 2%) scale(1.02); filter: hue-rotate(15deg); }
}
```

### Noise Texture Overlay
Add subtle grain for depth:
```css
.app::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    opacity: 0.025;
    pointer-events: none;
    mix-blend-mode: overlay;
}
```

## Glassmorphism Techniques

### Glass Panels
```css
.glass-panel {
    background: rgba(15, 12, 24, 0.85);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
}
```

### Glass with Glow Border
```css
.glass-glow {
    position: relative;
}

.glass-glow::after {
    content: '';
    position: absolute;
    top: 0;
    left: 15%;
    right: 15%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.5), transparent);
    box-shadow: 0 0 15px rgba(168, 85, 247, 0.4);
}
```

## Glow & Neon Effects

### Glow Shadows
```css
--glow-sm: 0 0 10px rgba(168, 85, 247, 0.3);
--glow-md: 0 0 20px rgba(168, 85, 247, 0.4);
--glow-lg: 0 0 40px rgba(168, 85, 247, 0.5);

/* Combined shadow + glow */
--shadow-glow: 0 4px 16px rgba(0, 0, 0, 0.5), 0 0 30px rgba(168, 85, 247, 0.2);
```

### Gradient Borders on Hover
```css
.card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
    padding: 1px;
    background: linear-gradient(135deg, transparent, transparent);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask-composite: exclude;
    transition: background 0.3s;
}

.card:hover::before {
    background: linear-gradient(135deg, #a855f7, #8b5cf6, #d946ef);
}
```

### Pulsing Glow Indicators
```css
.status-indicator {
    width: 8px;
    height: 8px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981, 0 0 16px #10b981;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 8px currentColor, 0 0 16px currentColor; }
    50% { opacity: 0.6; box-shadow: 0 0 4px currentColor; }
}
```

## Typography

### Font Pairing Recommendations

**Modern Tech (Linear style)**
- Display: `'Space Grotesk'`, `'Outfit'`, `'Sora'`
- Body: `'Inter'` (sparingly), `'DM Sans'`
- Mono: `'JetBrains Mono'`, `'Fira Code'`

**Premium/Luxury**
- Display: `'Playfair Display'`, `'Cormorant'`
- Body: `'Source Sans Pro'`, `'Lato'`

**Playful/Creative**
- Display: `'Archivo Black'`, `'Bebas Neue'`
- Body: `'Nunito'`, `'Quicksand'`

### Gradient Text
```css
.gradient-text {
    background: linear-gradient(135deg, #a855f7, #8b5cf6, #d946ef);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-shift 8s linear infinite;
}

@keyframes gradient-shift {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}
```

## Micro-interactions

### Lift on Hover
```css
.interactive {
    transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1),
                box-shadow 300ms ease-out;
}

.interactive:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-glow);
}
```

### Focus Ring Animation
```css
*:focus-visible {
    outline: none;
    box-shadow: 0 0 0 2px var(--bg-primary), 0 0 0 4px rgba(168, 85, 247, 0.5);
    animation: focus-pulse 1.5s ease-in-out infinite;
}

@keyframes focus-pulse {
    0%, 100% { box-shadow: 0 0 0 2px var(--bg-primary), 0 0 0 4px rgba(168, 85, 247, 0.5); }
    50% { box-shadow: 0 0 0 2px var(--bg-primary), 0 0 0 4px rgba(168, 85, 247, 0.8); }
}
```

### Staggered Entrance
```css
.item { animation: fade-up 300ms ease-out backwards; }
.item:nth-child(1) { animation-delay: 50ms; }
.item:nth-child(2) { animation-delay: 100ms; }
.item:nth-child(3) { animation-delay: 150ms; }

@keyframes fade-up {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
```

## Buttons

### Primary Gradient Button
```css
.btn-primary {
    background: linear-gradient(135deg, #a855f7, #8b5cf6, #d946ef);
    border: none;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-weight: 500;
    box-shadow: 0 2px 12px rgba(168, 85, 247, 0.4);
    transition: all 150ms ease;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 24px rgba(168, 85, 247, 0.5), 0 0 40px rgba(168, 85, 247, 0.3);
    filter: brightness(1.1);
}
```

## Accessibility

ALWAYS include reduced motion support:
```css
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

## Anti-Patterns to AVOID

- Generic white backgrounds with purple accents (overused AI aesthetic)
- Flat, lifeless designs without depth or atmosphere
- Inconsistent glow intensities (too bright or too subtle)
- Over-animating everything (choose 2-3 key moments)
- Using blur without purpose (blur should create hierarchy)
- Ignoring dark mode (vibe coders prefer dark themes)
- Cookie-cutter card layouts without visual interest

## Implementation Checklist

When building:
1. [ ] Establish color system with CSS variables
2. [ ] Add atmospheric background (gradient or texture)
3. [ ] Implement glass/elevated surfaces with blur
4. [ ] Add glow effects to interactive elements
5. [ ] Create smooth hover/focus transitions
6. [ ] Include entrance animations for key elements
7. [ ] Test with prefers-reduced-motion
8. [ ] Ensure text contrast meets WCAG standards

Remember: The goal is to create interfaces that developers WANT to use and look at. Every design choice should contribute to an atmosphere that feels intentional, refined, and memorable.
