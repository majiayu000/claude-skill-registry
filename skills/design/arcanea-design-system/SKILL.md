---
name: arcanea-design-system
description: The complete Arcanean Design System - cosmic visual language, academy themes, component patterns, and design tokens for magical interfaces
version: 2.0.0
author: Arcanea
tags: [design, ui, ux, visual, theming, css]
triggers:
  - design
  - UI
  - theme
  - colors
  - visual
  - interface
  - cosmic
  - academy theme
---

# The Arcanean Design System

> *"In Arcanea, every pixel carries meaning. The visual language is not decoration - it is communication."*

---

## Design Philosophy

### The Three Principles

1. **Magic Over Mundane**: Every element should feel slightly extraordinary
2. **Depth Creates Drama**: Layers, glows, and dimension suggest hidden power
3. **Restraint Amplifies Impact**: Cosmic effects work because they're used sparingly

### The Visual Metaphor
The Arcanean UI represents **a portal into creative consciousness**:
- Dark backgrounds = the cosmic void of infinite possibility
- Glowing elements = activated creative energy
- Glass surfaces = the veil between worlds
- Gold accents = distilled wisdom and achievement

---

## Color Architecture

### The Cosmic Foundation

```css
/* === COSMIC DEPTHS === */
--cosmic-void: #0b0e14;      /* Deepest background - infinite space */
--cosmic-deep: #121826;      /* Primary background - creative space */
--cosmic-surface: #1a2332;   /* Elevated surfaces - active zones */
--cosmic-raised: #242f42;    /* Highest surfaces - focus areas */
```

### The Arcanean Gold
```css
/* === UNIVERSAL ACCENT === */
--gold-light: #fff4d6;       /* Whisper of light */
--gold-medium: #ffd966;      /* Warm glow */
--gold-bright: #ffcc33;      /* Active energy */
--gold-deep: #e6b800;        /* Deep wisdom */
--gold-dark: #b38600;        /* Ancient knowledge */
```

### Academy Color Palettes

#### Atlantean Academy (Story/Water)
```css
/* Deep ocean blues with bioluminescent teal */
--atlantean-primary: #1e5a99;    /* Deep ocean */
--atlantean-teal: #26cccc;       /* Bioluminescent glow */
--atlantean-glow: #00e6e6;       /* Maximum luminescence */

/* Use for: Story creation, narrative tools, text-heavy interfaces */
```

#### Draconic Academy (Visual/Sky)
```css
/* Crimson fire with golden scales */
--draconic-crimson: #d92952;     /* Dragon fire */
--draconic-gold: #ffc61a;        /* Scale gold */
--draconic-sky: #2d8fe6;         /* Soaring heights */

/* Use for: Visual creation, image tools, canvas interfaces */
```

#### Creation & Light Academy (Music/Audio)
```css
/* Pure light with prismatic refractions */
--creation-gold: #ffcc33;        /* Pure light */
--creation-prism-blue: #2d85f5;  /* Refracted blue */
--creation-wave: #3dc4e6;        /* Sound frequency */

/* Use for: Audio creation, music tools, frequency interfaces */
```

---

## Typography System

### Font Stack
```css
/* Display (Headings, Titles) */
font-family: 'Cinzel', 'Cormorant Garamond', serif;

/* Body (Content, UI) */
font-family: 'Crimson Pro', 'Source Serif Pro', Georgia, serif;

/* Code (Monospace) */
font-family: 'JetBrains Mono', 'Fira Code', monospace;
```

### Type Scale
```css
--text-xs: 0.75rem;    /* 12px - Captions, labels */
--text-sm: 0.875rem;   /* 14px - Secondary content */
--text-base: 1rem;     /* 16px - Body text */
--text-lg: 1.125rem;   /* 18px - Emphasis */
--text-xl: 1.25rem;    /* 20px - Subheadings */
--text-2xl: 1.5rem;    /* 24px - Section headers */
--text-3xl: 1.875rem;  /* 30px - Page titles */
--text-4xl: 2.25rem;   /* 36px - Hero text */
--text-5xl: 3rem;      /* 48px - Display */
```

### Text Colors
```css
--text-primary: #e6eefc;    /* Main content */
--text-secondary: #9bb1d0;  /* Supporting text */
--text-muted: #708094;      /* Tertiary content */
--text-disabled: #515b6b;   /* Inactive elements */
```

---

## Spacing System

### Base Unit: 4px
```css
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

### Container Widths
```css
--container-xs: 320px;
--container-sm: 640px;
--container-md: 768px;
--container-lg: 1024px;
--container-xl: 1280px;
--container-2xl: 1536px;
```

---

## Effect System

### Glass Morphism
```css
/* Light glass - subtle depth */
.glass-light {
  background: rgba(18, 24, 38, 0.4);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

/* Standard glass - primary surfaces */
.glass {
  background: rgba(18, 24, 38, 0.6);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Heavy glass - important elements */
.glass-heavy {
  background: rgba(18, 24, 38, 0.8);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.15);
}
```

### Glow Effects
```css
/* Soft glow - ambient */
.glow-soft {
  box-shadow: 0 0 20px rgba(155, 177, 208, 0.3);
}

/* Academy glows */
.glow-atlantean {
  box-shadow: 0 0 30px rgba(0, 230, 230, 0.5);
}

.glow-draconic {
  box-shadow: 0 0 30px rgba(255, 219, 77, 0.5);
}

.glow-creation {
  box-shadow: 0 0 30px rgba(255, 230, 128, 0.5);
}
```

### Text Glow
```css
.text-glow-soft {
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}

.text-glow-atlantean {
  text-shadow: 0 0 15px rgba(0, 230, 230, 0.6);
}
```

### Shimmer Animation
```css
.shimmer {
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.1) 25%,
    rgba(255, 204, 51, 0.1) 50%,
    rgba(38, 204, 204, 0.1) 75%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

## Component Patterns

### Cards
```jsx
// Standard Arcanean Card
<div className="
  bg-cosmic-surface/60
  backdrop-blur-md
  border border-white/10
  rounded-lg
  p-6
  hover:border-gold-medium/30
  transition-all duration-300
">
  {children}
</div>

// Academy-Themed Card
<div className={cn(
  "glass rounded-lg p-6 transition-all duration-300",
  academy === 'atlantean' && "hover:glow-atlantean",
  academy === 'draconic' && "hover:glow-draconic",
  academy === 'creation' && "hover:glow-creation"
)}>
  {children}
</div>
```

### Buttons
```jsx
// Primary Button
<button className="
  bg-gold-bright
  text-cosmic-void
  font-display font-semibold
  px-6 py-3
  rounded-md
  hover:bg-gold-medium
  active:bg-gold-deep
  transition-colors duration-200
">
  {label}
</button>

// Ghost Button
<button className="
  bg-transparent
  text-text-primary
  border border-cosmic-border-bright
  px-6 py-3
  rounded-md
  hover:bg-cosmic-surface
  hover:border-gold-medium/50
  transition-all duration-200
">
  {label}
</button>

// Academy Button
<button className={cn(
  "px-6 py-3 rounded-md font-display transition-all duration-200",
  academy === 'atlantean' && "bg-atlantean-teal text-cosmic-void hover:glow-atlantean",
  academy === 'draconic' && "bg-draconic-gold text-cosmic-void hover:glow-draconic",
  academy === 'creation' && "bg-creation-gold text-cosmic-void hover:glow-creation"
)}>
  {label}
</button>
```

### Inputs
```jsx
// Standard Input
<input className="
  w-full
  bg-cosmic-surface
  border border-cosmic-border-bright
  text-text-primary
  placeholder:text-text-muted
  rounded-md
  px-4 py-3
  focus:outline-none
  focus:ring-2 focus:ring-gold-medium/50
  focus:border-gold-medium
  transition-all duration-200
"/>

// Magical Input (with glow on focus)
<input className="
  w-full
  glass-light
  border border-white/10
  text-text-primary
  placeholder:text-text-muted
  rounded-md
  px-4 py-3
  focus:outline-none
  focus:glow-soft
  focus:border-gold-bright/50
  transition-all duration-300
"/>
```

---

## Layout Patterns

### The Cosmic Canvas
```jsx
// Full-page cosmic background
<div className="
  min-h-screen
  bg-cosmic-deep
  bg-gradient-to-b from-cosmic-void via-cosmic-deep to-cosmic-surface
">
  {children}
</div>
```

### The Portal Frame
```jsx
// Centered content with mystical framing
<div className="
  min-h-screen
  flex items-center justify-center
  p-4
">
  <div className="
    w-full max-w-lg
    glass-heavy
    rounded-2xl
    p-8
    border border-gold-medium/20
  ">
    {children}
  </div>
</div>
```

### The Library Layout
```jsx
// Sidebar + content for exploration
<div className="flex min-h-screen">
  <aside className="
    w-64
    bg-cosmic-surface
    border-r border-cosmic-border
    p-6
  ">
    {navigation}
  </aside>
  <main className="flex-1 p-8">
    {content}
  </main>
</div>
```

---

## Animation Principles

### The Arcanean Motion Language

1. **Emergence**: Elements fade in from transparency
2. **Ascension**: Elements rise slightly as they appear
3. **Luminescence**: Glows pulse subtly
4. **Flow**: Transitions are smooth, never jarring

### Standard Durations
```css
--duration-instant: 100ms;   /* Micro-interactions */
--duration-fast: 200ms;      /* Hover states */
--duration-normal: 300ms;    /* Standard transitions */
--duration-slow: 500ms;      /* Page transitions */
--duration-glacial: 1000ms;  /* Ambient animations */
```

### Easing Functions
```css
--ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
--ease-dramatic: cubic-bezier(0.7, 0, 0.3, 1);
```

### Entrance Animations
```css
/* Fade + Rise */
@keyframes emerge {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Scale + Fade */
@keyframes manifest {
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
@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(255, 204, 51, 0.3);
  }
  50% {
    box-shadow: 0 0 40px rgba(255, 204, 51, 0.6);
  }
}
```

---

## Responsive Design

### Breakpoint System
```css
/* Mobile First */
sm: 640px   /* Small tablets, large phones */
md: 768px   /* Tablets */
lg: 1024px  /* Small laptops */
xl: 1280px  /* Desktops */
2xl: 1536px /* Large screens */
```

### Responsive Patterns
```jsx
// Typography scaling
<h1 className="text-2xl md:text-3xl lg:text-4xl xl:text-5xl">
  {title}
</h1>

// Layout switching
<div className="
  flex flex-col md:flex-row
  gap-4 md:gap-8
">
  {children}
</div>

// Visibility control
<div className="hidden lg:block">Desktop only</div>
<div className="lg:hidden">Mobile/Tablet only</div>
```

---

## Accessibility

### Focus States
```css
/* Always visible, beautiful focus */
:focus-visible {
  outline: 2px solid var(--gold-bright);
  outline-offset: 2px;
  border-radius: 4px;
}
```

### Color Contrast
- All text meets WCAG AA standards (4.5:1 minimum)
- Interactive elements meet enhanced contrast (7:1)
- Focus indicators are always visible

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Design Tokens Reference

### Quick Copy
```javascript
const ARCANEA_TOKENS = {
  colors: {
    cosmic: {
      void: '#0b0e14',
      deep: '#121826',
      surface: '#1a2332',
      raised: '#242f42',
    },
    gold: {
      light: '#fff4d6',
      medium: '#ffd966',
      bright: '#ffcc33',
      deep: '#e6b800',
    },
    atlantean: {
      primary: '#1e5a99',
      teal: '#26cccc',
      glow: '#00e6e6',
    },
    draconic: {
      crimson: '#d92952',
      gold: '#ffc61a',
      sky: '#2d8fe6',
    },
    creation: {
      gold: '#ffcc33',
      prism: '#2d85f5',
      wave: '#3dc4e6',
    },
  },
  fonts: {
    display: 'Cinzel, serif',
    body: 'Crimson Pro, serif',
    mono: 'JetBrains Mono, monospace',
  },
  radii: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    full: '9999px',
  },
};
```

---

## Usage Guidelines

### Do
- Use cosmic backgrounds as the foundation
- Apply glows sparingly for emphasis
- Let glass effects create depth
- Use academy colors for domain context
- Animate with purpose, not decoration

### Don't
- Make everything glow (dilutes impact)
- Use light backgrounds (breaks the metaphor)
- Mix academy themes haphazardly
- Over-animate (magic becomes noise)
- Forget accessibility

---

*"The interface is a portal. Design it as such."*
