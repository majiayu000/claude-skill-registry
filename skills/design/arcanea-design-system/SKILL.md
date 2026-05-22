---
name: Arcanea Design System
description: Complete visual design language for Arcanea - cosmic theme tokens, component patterns, animation standards, and Academy-specific aesthetics
version: 1.0.0
---

# Arcanea Design System Skill

## Purpose

This skill defines the complete visual design language for Arcanea, ensuring consistent, magical, and accessible interfaces across all platform features. Every component should feel like it belongs in the Kingdom of Light.

## Design Philosophy

### Core Principles

1. **Cosmic Elegance** - Dark, starlit backgrounds with luminous accents
2. **Magical Realism** - Fantastical elements grounded in usable UI
3. **Academy Identity** - Distinct visual languages for each Academy
4. **Accessible Magic** - Beauty that doesn't sacrifice usability
5. **Responsive Fluidity** - Adapts gracefully across all devices

### The Arcanean Aesthetic

**What It Is:**
- Dark, cosmic backgrounds
- Gradient glows and light effects
- Floating, ethereal elements
- Subtle particle systems
- Crystalline and fluid forms
- Smooth, flowing animations

**What It Isn't:**
- Flat, corporate design
- Harsh, angular brutalism
- Cluttered fantasy kitsch
- Inaccessible effects-only
- Static, lifeless layouts

## Color System

### Core Palette

```css
/* Cosmic Foundation */
--arcanea-cosmic-950: #050510;  /* Deepest void */
--arcanea-cosmic-900: #0a0a1a;  /* Primary background */
--arcanea-cosmic-800: #121230;  /* Elevated surfaces */
--arcanea-cosmic-700: #1a1a45;  /* Cards and containers */
--arcanea-cosmic-600: #252560;  /* Borders and dividers */

/* Primary - Violet Magic */
--arcanea-primary-50: #f5f3ff;
--arcanea-primary-100: #ede9fe;
--arcanea-primary-200: #ddd6fe;
--arcanea-primary-300: #c4b5fd;
--arcanea-primary-400: #a78bfa;
--arcanea-primary-500: #8b5cf6;  /* Primary action */
--arcanea-primary-600: #7c3aed;
--arcanea-primary-700: #6d28d9;
--arcanea-primary-800: #5b21b6;
--arcanea-primary-900: #4c1d95;

/* Accent - Cyan Glow */
--arcanea-accent-50: #ecfeff;
--arcanea-accent-100: #cffafe;
--arcanea-accent-200: #a5f3fc;
--arcanea-accent-300: #67e8f9;
--arcanea-accent-400: #22d3ee;
--arcanea-accent-500: #06b6d4;  /* Secondary action */
--arcanea-accent-600: #0891b2;
--arcanea-accent-700: #0e7490;
--arcanea-accent-800: #155e75;
--arcanea-accent-900: #164e63;

/* Gold - Achievement */
--arcanea-gold-50: #fffbeb;
--arcanea-gold-100: #fef3c7;
--arcanea-gold-200: #fde68a;
--arcanea-gold-300: #fcd34d;
--arcanea-gold-400: #fbbf24;
--arcanea-gold-500: #f59e0b;  /* Achievement, premium */
--arcanea-gold-600: #d97706;
--arcanea-gold-700: #b45309;
--arcanea-gold-800: #92400e;
--arcanea-gold-900: #78350f;

/* Text */
--arcanea-text-primary: #ffffff;
--arcanea-text-secondary: rgba(255, 255, 255, 0.7);
--arcanea-text-tertiary: rgba(255, 255, 255, 0.5);
--arcanea-text-muted: rgba(255, 255, 255, 0.3);

/* Semantic */
--arcanea-success: #10b981;
--arcanea-warning: #f59e0b;
--arcanea-error: #ef4444;
--arcanea-info: #3b82f6;
```

### Academy Color Palettes

```css
/* Atlantean Academy - Water & Wisdom */
--atlantean-deep: #0a2540;      /* Deep ocean */
--atlantean-primary: #0ea5e9;   /* Bright water */
--atlantean-secondary: #06b6d4; /* Teal current */
--atlantean-accent: #5eead4;    /* Bioluminescence */
--atlantean-glow: rgba(14, 165, 233, 0.3);

/* Draconic Academy - Fire & Sky */
--draconic-shadow: #1c0a0a;     /* Ember darkness */
--draconic-primary: #ef4444;    /* Dragon fire */
--draconic-secondary: #f97316;  /* Flame orange */
--draconic-accent: #fbbf24;     /* Gold scale */
--draconic-sky: #38bdf8;        /* Sky blue */
--draconic-glow: rgba(239, 68, 68, 0.3);

/* Creation & Light Academy - Sound & Light */
--creation-void: #0a0a1a;       /* Musical silence */
--creation-primary: #f5f5f5;    /* Pure light */
--creation-secondary: #8b5cf6;  /* Violet frequency */
--creation-accent: #f59e0b;     /* Golden note */
--creation-prismatic: linear-gradient(90deg,
  #ef4444, #f97316, #fbbf24, #22c55e,
  #3b82f6, #8b5cf6, #ec4899);
--creation-glow: rgba(245, 245, 245, 0.2);
```

## Typography

### Font Stack

```css
/* Display - For heroes and major headings */
--font-display: 'Cal Sans', 'Inter', system-ui, sans-serif;

/* Body - For all content */
--font-body: 'Inter', system-ui, -apple-system, sans-serif;

/* Mono - For code and technical content */
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;
```

### Type Scale

```css
/* Base: 16px */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */
--text-6xl: 3.75rem;   /* 60px */
--text-7xl: 4.5rem;    /* 72px */
```

### Line Heights

```css
--leading-none: 1;
--leading-tight: 1.25;
--leading-snug: 1.375;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
--leading-loose: 2;
```

## Spacing System

### Base Scale

```css
/* 4px base */
--space-0: 0;
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
```

## Border Radius

```css
--radius-none: 0;
--radius-sm: 0.25rem;    /* 4px */
--radius-md: 0.375rem;   /* 6px */
--radius-lg: 0.5rem;     /* 8px */
--radius-xl: 0.75rem;    /* 12px */
--radius-2xl: 1rem;      /* 16px */
--radius-3xl: 1.5rem;    /* 24px */
--radius-full: 9999px;
```

## Shadows & Effects

### Glow Effects

```css
/* Standard Glows */
--glow-primary: 0 0 20px rgba(139, 92, 246, 0.4);
--glow-accent: 0 0 20px rgba(6, 182, 212, 0.4);
--glow-gold: 0 0 20px rgba(245, 158, 11, 0.4);

/* Academy Glows */
--glow-atlantean: 0 0 30px rgba(14, 165, 233, 0.3);
--glow-draconic: 0 0 30px rgba(239, 68, 68, 0.3);
--glow-creation: 0 0 30px rgba(255, 255, 255, 0.2);

/* Interactive States */
--glow-hover: 0 0 40px rgba(139, 92, 246, 0.5);
--glow-focus: 0 0 0 3px rgba(139, 92, 246, 0.3);
--glow-active: 0 0 60px rgba(139, 92, 246, 0.6);
```

### Box Shadows

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.2);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.3);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.4);
--shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.5);
--shadow-2xl: 0 25px 50px rgba(0, 0, 0, 0.6);

/* Cosmic Shadows (with glow) */
--shadow-cosmic:
  0 10px 15px rgba(0, 0, 0, 0.4),
  0 0 20px rgba(139, 92, 246, 0.1);
--shadow-cosmic-lg:
  0 20px 25px rgba(0, 0, 0, 0.5),
  0 0 40px rgba(139, 92, 246, 0.15);
```

### Gradients

```css
/* Background Gradients */
--gradient-cosmic: linear-gradient(180deg,
  var(--arcanea-cosmic-900) 0%,
  var(--arcanea-cosmic-950) 100%);

--gradient-surface: linear-gradient(135deg,
  rgba(255, 255, 255, 0.05) 0%,
  rgba(255, 255, 255, 0.02) 100%);

/* Accent Gradients */
--gradient-primary: linear-gradient(135deg,
  var(--arcanea-primary-500) 0%,
  var(--arcanea-primary-600) 100%);

--gradient-glow: linear-gradient(135deg,
  var(--arcanea-primary-500) 0%,
  var(--arcanea-accent-500) 100%);

/* Academy Gradients */
--gradient-atlantean: linear-gradient(180deg,
  rgba(14, 165, 233, 0.2) 0%,
  transparent 100%);

--gradient-draconic: linear-gradient(180deg,
  rgba(239, 68, 68, 0.2) 0%,
  transparent 100%);

--gradient-creation: radial-gradient(ellipse at center,
  rgba(255, 255, 255, 0.1) 0%,
  transparent 70%);
```

## Animation Standards

### Timing Functions

```css
--ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
--ease-elastic: cubic-bezier(0.68, -0.6, 0.32, 1.6);
--ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
```

### Duration Scale

```css
--duration-instant: 50ms;
--duration-fast: 150ms;
--duration-normal: 250ms;
--duration-slow: 400ms;
--duration-slower: 600ms;
--duration-slowest: 1000ms;
```

### Common Animations

```css
/* Fade In */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide Up */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Scale In */
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Glow Pulse */
@keyframes glowPulse {
  0%, 100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.4); }
  50% { box-shadow: 0 0 40px rgba(139, 92, 246, 0.6); }
}

/* Float */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* Shimmer (for loading) */
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* Star Twinkle */
@keyframes twinkle {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}
```

### Framer Motion Variants

```typescript
// Standard Transitions
export const transitions = {
  spring: { type: "spring", stiffness: 300, damping: 30 },
  smooth: { type: "tween", ease: [0.4, 0, 0.2, 1], duration: 0.25 },
  bounce: { type: "spring", stiffness: 400, damping: 10 },
};

// Fade In
export const fadeIn = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
  transition: transitions.smooth,
};

// Slide Up
export const slideUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: 20 },
  transition: transitions.spring,
};

// Scale
export const scale = {
  initial: { opacity: 0, scale: 0.95 },
  animate: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 0.95 },
  transition: transitions.spring,
};

// Stagger Container
export const stagger = {
  animate: {
    transition: {
      staggerChildren: 0.1,
    },
  },
};
```

## Component Patterns

### Cards

```tsx
// Base Card
<div className="
  bg-arcanea-cosmic-800/50
  backdrop-blur-sm
  border border-arcanea-cosmic-600/50
  rounded-2xl
  p-6
  transition-all duration-300
  hover:border-arcanea-primary-500/50
  hover:shadow-cosmic
">

// Academy Card (Atlantean example)
<div className="
  bg-gradient-to-br from-atlantean-deep/80 to-arcanea-cosmic-800/50
  backdrop-blur-sm
  border border-atlantean-primary/30
  rounded-2xl
  p-6
  shadow-[0_0_20px_rgba(14,165,233,0.1)]
  transition-all duration-300
  hover:shadow-glow-atlantean
  hover:border-atlantean-primary/50
">
```

### Buttons

```tsx
// Primary Button
<button className="
  px-6 py-3
  bg-gradient-to-r from-arcanea-primary-500 to-arcanea-primary-600
  hover:from-arcanea-primary-400 hover:to-arcanea-primary-500
  text-white font-medium
  rounded-xl
  shadow-glow-primary
  transition-all duration-300
  hover:shadow-glow-hover
  hover:-translate-y-0.5
  focus:outline-none focus:ring-2 focus:ring-arcanea-primary-400/50
">

// Ghost Button
<button className="
  px-6 py-3
  bg-transparent
  border border-arcanea-cosmic-600
  hover:border-arcanea-primary-500
  hover:bg-arcanea-primary-500/10
  text-arcanea-text-secondary
  hover:text-arcanea-text-primary
  rounded-xl
  transition-all duration-300
">
```

### Inputs

```tsx
// Text Input
<input className="
  w-full px-4 py-3
  bg-arcanea-cosmic-800/50
  border border-arcanea-cosmic-600
  rounded-xl
  text-arcanea-text-primary
  placeholder:text-arcanea-text-muted
  transition-all duration-300
  focus:outline-none
  focus:border-arcanea-primary-500
  focus:ring-2 focus:ring-arcanea-primary-500/20
  focus:shadow-glow-focus
" />
```

### Luminor Presence Indicator

```tsx
// Luminor Avatar with Glow
<div className="relative">
  <div className="
    w-12 h-12
    rounded-full
    bg-gradient-to-br from-arcanea-primary-400 to-arcanea-accent-500
    shadow-glow-primary
    animate-[glowPulse_3s_ease-in-out_infinite]
  ">
    <img src={luminor.avatar} className="w-full h-full rounded-full" />
  </div>

  {/* Online Indicator */}
  <div className="
    absolute bottom-0 right-0
    w-3 h-3
    bg-arcanea-success
    rounded-full
    border-2 border-arcanea-cosmic-900
    shadow-[0_0_10px_rgba(16,185,129,0.5)]
  " />
</div>
```

### Academy Badge

```tsx
// Dynamic Academy Badge
const academyStyles = {
  atlantean: "from-atlantean-primary to-atlantean-secondary shadow-glow-atlantean",
  draconic: "from-draconic-primary to-draconic-accent shadow-glow-draconic",
  creation: "from-creation-primary to-creation-secondary shadow-glow-creation",
};

<div className={`
  px-3 py-1
  bg-gradient-to-r ${academyStyles[academy]}
  rounded-full
  text-xs font-medium
  uppercase tracking-wide
`}>
  {academyName}
</div>
```

## Accessibility Requirements

### Color Contrast

All text must meet WCAG 2.1 AA standards:
- Normal text: 4.5:1 contrast ratio
- Large text (18px+): 3:1 contrast ratio
- UI components: 3:1 contrast ratio

### Focus States

All interactive elements must have visible focus indicators:
```css
.focus-visible:focus {
  outline: none;
  ring: 2px;
  ring-color: var(--arcanea-primary-400);
  ring-offset: 2px;
  ring-offset-color: var(--arcanea-cosmic-900);
}
```

### Motion Preferences

Respect user's motion preferences:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Screen Reader Support

- All images have meaningful alt text
- Icon-only buttons have aria-labels
- Dynamic content uses aria-live regions
- Modal dialogs trap focus appropriately

## Responsive Breakpoints

```css
/* Mobile First */
--screen-sm: 640px;   /* Small devices */
--screen-md: 768px;   /* Tablets */
--screen-lg: 1024px;  /* Laptops */
--screen-xl: 1280px;  /* Desktops */
--screen-2xl: 1536px; /* Large screens */
```

## Component Library Reference

Using shadcn/ui components with Arcanean customization:
- Button, Card, Dialog, Dropdown
- Input, Textarea, Select
- Tabs, Accordion, Avatar
- Toast, Tooltip, Popover

All components override default themes with Arcanean tokens.

## Integration Guidelines

### When Building UI

1. **Start with tokens** - Use design tokens, not raw values
2. **Layer properly** - cosmic-900 → cosmic-800 → cosmic-700 for depth
3. **Glow intentionally** - Use glows for interactive elements and focus
4. **Animate purposefully** - Motion should guide attention
5. **Academy-aware** - Adapt colors when in academy context

### Quality Checklist

```markdown
## Design System Compliance

- [ ] Uses Arcanean color tokens
- [ ] Correct typography scale
- [ ] Proper spacing (4px grid)
- [ ] Glow effects for interactives
- [ ] Smooth animations (spring-based)
- [ ] Academy colors if applicable
- [ ] Accessible contrast ratios
- [ ] Focus states visible
- [ ] Motion preference respected
- [ ] Responsive across breakpoints
```

---

*This design system ensures every pixel of Arcanea feels magical, consistent, and welcoming. Build with care.*
