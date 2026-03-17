---
name: breakpoints
description: Use this skill when implementing responsive design, optimizing layouts for different screen sizes, or working on responsive components for the EVOLEA website. Provides the EVOLEA breakpoint system, fluid typography scales, and responsive CSS patterns following 2025 best practices with EVOLEA brand adherence.
---

# EVOLEA Responsive Breakpoint System

This skill provides the comprehensive breakpoint system and responsive design patterns for the EVOLEA website. Use it when creating new components, optimizing existing layouts, or ensuring consistent responsive behavior across all screen sizes while maintaining EVOLEA brand integrity.

## Core Principles (2025 Best Practices)

### 1. Mobile-First Approach
Always start with mobile styles as the base, then progressively enhance for larger screens using `min-width` media queries. EVOLEA serves families on-the-go, so mobile experience is critical.

### 2. Content-Driven Breakpoints
Choose breakpoints where the design naturally needs adjustment, not arbitrary device sizes. The content should guide the breakpoint selection.

### 3. Fluid over Fixed
Prefer `clamp()`, `min()`, and viewport units over fixed pixel values. This creates smoother scaling and reduces the number of breakpoints needed. Especially important for EVOLEA's vibrant gradient backgrounds.

### 4. Brand-First Design
Every breakpoint must maintain EVOLEA brand requirements:
- Prism gradient visibility
- Floating elements (orbs, butterflies) scale appropriately
- Text shadows on gradients remain visible
- Touch targets meet accessibility standards (44px minimum)

### 5. Test Real Devices
The breakpoints are guidelines. Always test on actual devices and adjust based on real-world behavior.

---

## Official Breakpoint Values

```css
:root {
  /* Standard Breakpoints (matches Tailwind defaults) */
  --bp-sm: 640px;    /* Mobile landscape / Small tablets */
  --bp-md: 768px;    /* Tablets portrait */
  --bp-lg: 1024px;   /* Tablets landscape / Small laptops */
  --bp-xl: 1280px;   /* Standard laptops */
  --bp-2xl: 1440px;  /* Large laptops / Standard desktops */

  /* Large Screen Breakpoints (EVOLEA-specific for gradient scaling) */
  --bp-3xl: 1920px;  /* Full HD / 27" displays */
  --bp-4xl: 2560px;  /* 2K / QHD displays */
  --bp-5xl: 3840px;  /* 4K UHD displays (future-proofing) */
}
```

### Media Query Usage

```css
/* Mobile first - base styles for smallest screens (375px+) */
.component { /* mobile styles */ }

/* Small devices (landscape phones, small tablets) */
@media (min-width: 640px) { }

/* Medium devices (tablets) */
@media (min-width: 768px) { }

/* Large devices (laptops, small desktops) */
@media (min-width: 1024px) { }

/* Extra large (standard desktops) */
@media (min-width: 1280px) { }

/* 2X large (large desktops) */
@media (min-width: 1440px) { }

/* 3X large (27" monitors, Full HD) - EVOLEA gradient optimization */
@media (min-width: 1920px) { }

/* 4X large (2K/QHD monitors) - EVOLEA premium experience */
@media (min-width: 2560px) { }
```

---

## Fluid Typography Scale (EVOLEA Brand)

Use `clamp()` for typography that scales smoothly between breakpoints. All values respect EVOLEA's Fredoka (headlines) and Poppins (body) fonts.

```css
:root {
  /* Display / Hero Typography (Fredoka Bold 700) */
  --font-hero: clamp(2.5rem, 4vw + 1rem, 6rem);
  /* Min: 40px mobile, Preferred: 4vw + 16px, Max: 96px desktop */

  /* Heading 1 (Fredoka Bold 700) */
  --font-h1: clamp(2rem, 3vw + 0.75rem, 4rem);
  /* Min: 32px, Preferred: 3vw + 12px, Max: 64px */

  /* Heading 2 (Fredoka SemiBold 600) */
  --font-h2: clamp(1.5rem, 2.5vw + 0.5rem, 3rem);
  /* Min: 24px, Preferred: 2.5vw + 8px, Max: 48px */

  /* Heading 3 (Fredoka SemiBold 600) */
  --font-h3: clamp(1.25rem, 2vw + 0.25rem, 2rem);
  /* Min: 20px, Preferred: 2vw + 4px, Max: 32px */

  /* Body Large (Poppins Regular 400) */
  --font-body-lg: clamp(1.125rem, 0.5vw + 1rem, 1.375rem);
  /* Min: 18px, Preferred: 0.5vw + 16px, Max: 22px */

  /* Body Text (Poppins Regular 400) */
  --font-body: clamp(1rem, 0.3vw + 0.9rem, 1.125rem);
  /* Min: 16px, Preferred: 0.3vw + 14px, Max: 18px */

  /* Small Text (Poppins Regular 400) */
  --font-small: clamp(0.875rem, 0.2vw + 0.8rem, 1rem);
  /* Min: 14px, Preferred: 0.2vw + 13px, Max: 16px */

  /* Micro Text - labels, badges (Poppins Medium 500) */
  --font-micro: clamp(0.75rem, 0.15vw + 0.7rem, 0.875rem);
  /* Min: 12px, Preferred: 0.15vw + 11px, Max: 14px */
}
```

### Usage Example

```astro
---
// In an Astro component
---
<style>
  .hero-headline {
    font-family: 'Fredoka', sans-serif;
    font-weight: 700;
    font-size: var(--font-hero);
    line-height: 1.1;
    /* EVOLEA Brand Requirement: Text shadow on gradients */
    text-shadow:
      0 2px 4px rgba(0, 0, 0, 0.1),
      0 4px 20px rgba(138, 61, 158, 0.3);
  }

  .section-title {
    font-family: 'Fredoka', sans-serif;
    font-weight: 600;
    font-size: var(--font-h2);
    color: var(--evolea-purple);
  }

  body {
    font-family: 'Poppins', sans-serif;
    font-size: var(--font-body);
    line-height: 1.7;
    color: var(--evolea-text);
  }
</style>
```

---

## Fluid Spacing Scale (EVOLEA Brand)

```css
:root {
  /* Section Spacing (between major page sections) */
  --space-section: clamp(4rem, 8vh, 8rem);
  /* Min: 64px, Preferred: 8vh, Max: 128px */

  /* Component Spacing (within sections) */
  --space-component: clamp(2rem, 4vh, 5rem);
  /* Min: 32px, Preferred: 4vh, Max: 80px */

  /* Card Gap (grid/flex gaps) */
  --space-card-gap: clamp(1rem, 2vw, 2.5rem);
  /* Min: 16px, Preferred: 2vw, Max: 40px */

  /* Content Padding (horizontal page padding) */
  --space-content-padding: clamp(1.5rem, 5vw, 4rem);
  /* Min: 24px, Preferred: 5vw, Max: 64px */

  /* Gradient Fade Height (for wave transitions) */
  --gradient-fade-height: clamp(80px, 10vh, 160px);
  /* For EVOLEA's signature wave fade effect */
}
```

---

## Container System (EVOLEA Brand)

```css
:root {
  /* Fixed Containers (for specific layouts) */
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
  --container-2xl: 1440px;
  --container-3xl: 1600px;  /* EVOLEA large screens */
  --container-4xl: 1800px;  /* EVOLEA ultra-wide */

  /* Fluid Container (recommended for most EVOLEA sections) */
  --container-fluid: min(92vw, 1800px);

  /* Hero Container (for prism gradient backgrounds) */
  --container-hero: min(90vw, 1600px);
}
```

### Container Usage Patterns

```css
/* Standard contained section (most EVOLEA pages) */
.section-content {
  max-width: var(--container-2xl);
  margin: 0 auto;
  padding: 0 var(--space-content-padding);
}

/* Large screen optimized container */
@media (min-width: 1920px) {
  .section-content {
    max-width: var(--container-3xl);
  }
}

/* Ultra-wide container (2K+) */
@media (min-width: 2560px) {
  .section-content {
    max-width: var(--container-4xl);
  }
}

/* Fluid container with constraints (hero sections) */
.hero-container {
  max-width: var(--container-hero);
  margin: 0 auto;
  padding: var(--space-section) var(--space-content-padding);
}
```

---

## EVOLEA Brand-Specific Patterns

### Prism Gradient Hero Section

```css
.hero-section {
  position: relative;
  min-height: 60vh;
  min-height: 60dvh;
  display: flex;
  align-items: center;
  overflow: hidden;
  padding: var(--space-section) var(--space-content-padding);
}

/* Prism gradient background */
.hero-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    #7BEDD5 0%,      /* Mint */
    #FFE066 20%,     /* Sunshine */
    #FF9ECC 40%,     /* Blush */
    #E97BF1 60%,     /* Magenta */
    #CD87F8 80%,     /* Lavender */
    #BA53AD 100%     /* Deep Purple */
  );
  z-index: -1;
}

@media (min-width: 768px) {
  .hero-section {
    min-height: 70vh;
    min-height: 70dvh;
  }
}

@media (min-width: 1024px) {
  .hero-section {
    min-height: 80vh;
    min-height: 80dvh;
  }
}

@media (min-width: 1920px) {
  .hero-section {
    min-height: 85vh;
    min-height: 85dvh;
  }
}
```

### Floating Orbs (EVOLEA Signature)

```css
.floating-orbs {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
  z-index: 1;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.4;
  animation: float 20s ease-in-out infinite;
}

.orb-mint {
  width: clamp(150px, 20vw, 300px);
  height: clamp(150px, 20vw, 300px);
  background: radial-gradient(circle, #7BEDD5, #5DD5C0);
  top: 10%;
  left: 5%;
}

.orb-gold {
  width: clamp(120px, 15vw, 250px);
  height: clamp(120px, 15vw, 250px);
  background: radial-gradient(circle, #FFE066, #FFC83D);
  top: 60%;
  right: 10%;
  animation-delay: -7s;
}

.orb-magenta {
  width: clamp(180px, 22vw, 350px);
  height: clamp(180px, 22vw, 350px);
  background: radial-gradient(circle, #E97BF1, #DD48E0);
  bottom: 15%;
  left: 20%;
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(15px, -20px) scale(1.05);
  }
  50% {
    transform: translate(-10px, 15px) scale(0.95);
  }
  75% {
    transform: translate(20px, -10px) scale(1.02);
  }
}

@media (min-width: 1920px) {
  .orb {
    filter: blur(80px);
  }

  .orb-mint {
    width: clamp(200px, 18vw, 400px);
    height: clamp(200px, 18vw, 400px);
  }
}
```

### Wave Fade Transition (EVOLEA Signature)

```css
.wave-fade {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: var(--gradient-fade-height);
  pointer-events: none;
  overflow: visible;
}

.wave-layer {
  position: absolute;
  width: 200%;
  height: 100%;
  background: linear-gradient(
    180deg,
    rgba(186, 83, 173, 0.8) 0%,
    rgba(205, 135, 248, 0.4) 50%,
    transparent 100%
  );
  clip-path: polygon(
    0% 0%,
    0% 30%,
    5% 40%,
    10% 35%,
    15% 45%,
    20% 50%,
    25% 43%,
    30% 55%,
    35% 60%,
    40% 53%,
    45% 65%,
    50% 57%,
    55% 50%,
    60% 60%,
    65% 67%,
    70% 55%,
    75% 63%,
    80% 50%,
    85% 60%,
    90% 53%,
    95% 45%,
    100% 40%,
    100% 0%
  );
  animation: waveDrift 25s ease-in-out infinite;
}

@keyframes waveDrift {
  0%, 100% { transform: translateX(0) scaleY(1); }
  25% { transform: translateX(-12%) scaleY(1.05); }
  50% { transform: translateX(-25%) scaleY(0.95); }
  75% { transform: translateX(-12%) scaleY(1.02); }
}

@media (min-width: 1920px) {
  .wave-fade {
    height: clamp(120px, 12vh, 200px);
  }
}
```

### Floating Butterflies (EVOLEA Brand Element)

```css
.floating-butterflies {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 2;
}

.butterfly {
  position: absolute;
  width: clamp(40px, 5vw, 80px);
  height: auto;
  opacity: 0.6;
  animation: butterflyFloat 30s ease-in-out infinite;
}

.butterfly-1 {
  top: 20%;
  left: 10%;
}

.butterfly-2 {
  top: 60%;
  right: 15%;
  animation-delay: -10s;
}

.butterfly-3 {
  top: 40%;
  right: 40%;
  animation-delay: -20s;
}

@keyframes butterflyFloat {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  25% {
    transform: translate(30px, -20px) rotate(8deg);
  }
  50% {
    transform: translate(15px, 25px) rotate(-5deg);
  }
  75% {
    transform: translate(-20px, -15px) rotate(6deg);
  }
}

@media (min-width: 1920px) {
  .butterfly {
    width: clamp(60px, 4vw, 100px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .butterfly {
    animation: none;
  }
}
```

---

## Component Patterns

### Responsive Card Grid (Program Cards, Blog Cards)

```css
.card-grid {
  display: grid;
  gap: var(--space-card-gap);
  grid-template-columns: 1fr;
}

@media (min-width: 640px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 1440px) {
  .card-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 1920px) {
  .card-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: clamp(1.5rem, 2vw, 3rem);
  }
}
```

### EVOLEA Card Component

```css
.evolea-card {
  background: white;
  border-radius: 24px;
  padding: clamp(1.5rem, 3vw, 2.5rem);
  box-shadow: 0 4px 20px rgba(186, 83, 173, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.evolea-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(186, 83, 173, 0.15);
}

/* Spectrum accent bar */
.evolea-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(
    90deg,
    #7BEDD5,
    #FFE066,
    #FF7E5D,
    #EF8EAE,
    #E97BF1,
    #CD87F8
  );
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.evolea-card:hover::before {
  transform: scaleX(1);
}

@media (min-width: 1920px) {
  .evolea-card {
    padding: clamp(2rem, 3vw, 3rem);
  }
}
```

### Two-Column Content Layout

```css
.two-col-layout {
  display: grid;
  gap: var(--space-component);
  grid-template-columns: 1fr;
  align-items: center;
}

@media (min-width: 1024px) {
  .two-col-layout {
    grid-template-columns: 1fr 1.2fr;
  }

  .two-col-layout.reverse {
    grid-template-columns: 1.2fr 1fr;
  }
}

@media (min-width: 1920px) {
  .two-col-layout {
    gap: clamp(3rem, 6vw, 8rem);
  }
}
```

---

## Large Screen Optimizations

### 27" Display (1920px+)

```css
@media (min-width: 1920px) {
  /* Expand containers */
  .main-container {
    max-width: var(--container-3xl);
  }

  /* Scale hero typography */
  .hero-headline {
    font-size: clamp(3.5rem, 5vw, 7rem);
  }

  /* Increase whitespace */
  section {
    padding: clamp(5rem, 10vh, 10rem) var(--space-content-padding);
  }

  /* Scale buttons and interactive elements */
  .btn {
    padding: clamp(1rem, 1.2vw, 1.5rem) clamp(2rem, 2.5vw, 3rem);
    font-size: clamp(1rem, 0.9vw, 1.25rem);
  }

  /* Floating orbs scale up */
  .orb {
    filter: blur(80px);
  }

  /* Prism gradient becomes more dramatic */
  .hero-section::before {
    background-size: 150% 150%;
  }
}
```

### 4K Display (2560px+)

```css
@media (min-width: 2560px) {
  /* Further container expansion */
  .main-container {
    max-width: var(--container-4xl);
  }

  /* Hero scaling */
  .hero-headline {
    font-size: clamp(4rem, 4.5vw, 8rem);
  }

  /* Card grid can show 5 columns */
  .card-grid {
    grid-template-columns: repeat(5, 1fr);
  }

  /* Floating elements scale dramatically */
  .orb-mint {
    width: clamp(250px, 16vw, 450px);
    height: clamp(250px, 16vw, 450px);
  }

  /* Wave fade becomes taller */
  .wave-fade {
    height: clamp(150px, 15vh, 250px);
  }
}
```

---

## Accessibility Requirements

### Touch Targets (EVOLEA Brand Requirement #10)

```css
/* Minimum touch target: 44px (WCAG 2.1 Level AAA) */
.btn,
.link,
.interactive,
.nav-link,
.card {
  min-height: 44px;
  min-width: 44px;
}

/* Scale for precision pointer devices on large screens */
@media (min-width: 1920px) and (pointer: fine) {
  .btn {
    padding: clamp(1rem, 1.2vw, 1.5rem) clamp(2rem, 2.5vw, 3rem);
  }
}
```

### Reduced Motion (EVOLEA Brand Requirement)

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  /* Disable EVOLEA-specific animations */
  .orb,
  .butterfly,
  .wave-layer {
    animation: none !important;
  }
}
```

### High Contrast Mode

```css
@media (prefers-contrast: high) {
  .evolea-card {
    border: 2px solid currentColor;
  }

  .btn {
    border: 2px solid currentColor;
  }

  /* Ensure text remains visible on gradients */
  .hero-headline {
    text-shadow:
      0 0 10px rgba(0, 0, 0, 0.9),
      0 2px 4px rgba(0, 0, 0, 0.8);
  }
}
```

### Text Contrast (EVOLEA Brand Requirement #3)

```css
/* NEVER use text without shadows on gradients */
.text-on-gradient {
  color: #FFFFFF;
  text-shadow:
    0 2px 4px rgba(0, 0, 0, 0.1),
    0 4px 20px rgba(138, 61, 158, 0.3),
    0 0 60px rgba(186, 83, 173, 0.2);
}

/* Ensure minimum contrast ratio of 4.5:1 (WCAG AA) */
.body-text {
  color: var(--evolea-text); /* #2D2A32 */
}

.secondary-text {
  color: var(--evolea-text-light); /* #5C5762 */
}
```

---

## Testing Checklist

When implementing responsive designs, test at these key EVOLEA viewports:

| Size | Width | Use Case | EVOLEA Priority |
|------|-------|----------|-----------------|
| Mobile | 375px | iPhone SE/13 Mini | **Critical** |
| Mobile L | 428px | iPhone 14 Pro Max | High |
| Tablet | 768px | iPad Mini | **Critical** |
| Tablet L | 1024px | iPad Pro 11" | High |
| Laptop | 1440px | MacBook Pro 14" | **Critical** |
| Desktop | 1920px | Full HD Monitor | High |
| 2K | 2560px | QHD / 27" Retina | Medium |
| 4K | 3840px | 4K UHD Monitor | Low |

### EVOLEA-Specific Testing Points

- [ ] Prism gradient visible and not washed out
- [ ] Floating orbs visible but not overwhelming
- [ ] Butterflies animate smoothly (or disabled with reduced-motion)
- [ ] Wave fade transitions seamlessly
- [ ] Text shadows visible on all gradient backgrounds
- [ ] Mobile menu has **solid background** (Brand Requirement #2)
- [ ] All images use SVG icons, **never emojis** (Brand Requirement #1)
- [ ] Touch targets minimum 44px
- [ ] Logo butterfly never covers the "A"
- [ ] Donate button (gold) visible in navigation

### Testing Commands

```bash
# Start local dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Chrome DevTools responsive mode shortcuts:
# Ctrl+Shift+M (Windows) / Cmd+Shift+M (Mac)

# Specific viewport sizes to test:
# 375 x 812 (Mobile)
# 768 x 1024 (Tablet)
# 1440 x 900 (Laptop)
# 1920 x 1080 (Desktop)
# 2560 x 1440 (2K)
```

---

## Common EVOLEA Responsive Patterns

### Hero Section

```astro
---
// src/components/HeroSection.astro
interface Props {
  title: string;
  subtitle?: string;
  variant?: 'prism' | 'dark';
}
const { title, subtitle, variant = 'prism' } = Astro.props;
---

<section class:list={['hero-section', `hero-${variant}`]}>
  <div class="floating-orbs">
    <div class="orb orb-mint"></div>
    <div class="orb orb-gold"></div>
    <div class="orb orb-magenta"></div>
  </div>

  <div class="floating-butterflies">
    <div class="butterfly butterfly-1">
      <svg><!-- Butterfly SVG --></svg>
    </div>
    <div class="butterfly butterfly-2">
      <svg><!-- Butterfly SVG --></svg>
    </div>
  </div>

  <div class="hero-container">
    <h1 class="hero-headline text-on-gradient">{title}</h1>
    {subtitle && <p class="hero-subtitle text-on-gradient">{subtitle}</p>}
    <slot />
  </div>

  <div class="wave-fade">
    <div class="wave-layer"></div>
  </div>
</section>

<style>
  /* Mobile-first styles */
  .hero-section {
    position: relative;
    min-height: 60vh;
    min-height: 60dvh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: var(--space-section) var(--space-content-padding);
  }

  .hero-prism::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(
      135deg,
      #7BEDD5 0%,
      #FFE066 20%,
      #FF9ECC 40%,
      #E97BF1 60%,
      #CD87F8 80%,
      #BA53AD 100%
    );
    z-index: -1;
  }

  .hero-container {
    max-width: var(--container-hero);
    margin: 0 auto;
    text-align: center;
    z-index: 10;
  }

  .hero-headline {
    font-family: 'Fredoka', sans-serif;
    font-weight: 700;
    font-size: var(--font-hero);
    line-height: 1.1;
    margin-bottom: clamp(1rem, 3vw, 2rem);
  }

  .hero-subtitle {
    font-family: 'Poppins', sans-serif;
    font-size: var(--font-body-lg);
    line-height: 1.6;
    max-width: 600px;
    margin: 0 auto;
  }

  @media (min-width: 768px) {
    .hero-section {
      min-height: 70vh;
      min-height: 70dvh;
    }
  }

  @media (min-width: 1024px) {
    .hero-section {
      min-height: 80vh;
      min-height: 80dvh;
    }
  }

  @media (min-width: 1920px) {
    .hero-section {
      min-height: 85vh;
      min-height: 85dvh;
    }

    .hero-container {
      max-width: var(--container-3xl);
    }
  }
</style>
```

### Section Padding

```css
.section {
  padding: var(--space-section) var(--space-content-padding);
}

/* Alternate: specific vertical/horizontal control */
.section-alt {
  padding-top: var(--space-section);
  padding-bottom: var(--space-section);
  padding-left: var(--space-content-padding);
  padding-right: var(--space-content-padding);
}
```

### Image Scaling

```css
.responsive-image {
  width: 100%;
  height: auto;
  max-width: 100%;
  border-radius: 24px; /* EVOLEA brand style */
}

.hero-image {
  max-width: clamp(300px, 50vw, 800px);
}

@media (min-width: 1920px) {
  .hero-image {
    max-width: clamp(400px, 45vw, 1000px);
  }
}
```

---

## Reference Files

- **EVOLEA Brand Guide:** `.claude/todo/EVOLEA-BRAND-GUIDE-V3.md`
- **Project Instructions:** `CLAUDE.md`
- **CSS Specifications:** `breakpoints/CSS-SPECIFICATIONS.md`
- **Testing Manual:** `breakpoints/TESTING-MANUAL.md`
- **Tailwind Config:** `tailwind.config.mjs`
- **Global Styles:** `src/styles/global.css`

---

## Quick Reference Card

```
EVOLEA BREAKPOINTS:
sm   640px   Tablets
md   768px   Tablets landscape
lg   1024px  Small laptops
xl   1280px  Laptops
2xl  1440px  Desktops
3xl  1920px  27" monitors (gradient optimization)
4xl  2560px  2K/QHD (premium experience)

CONTAINERS:
Standard: 1440px
Large:    1600px
Ultra:    1800px
Fluid:    min(92vw, 1800px)
Hero:     min(90vw, 1600px)

TYPOGRAPHY (clamp - Fredoka/Poppins):
Hero:     2.5rem → 4vw+1rem → 6rem
H1:       2rem → 3vw+0.75rem → 4rem
H2:       1.5rem → 2.5vw+0.5rem → 3rem
Body:     1rem → 0.3vw+0.9rem → 1.125rem

SPACING (clamp):
Section:   4rem → 8vh → 8rem
Component: 2rem → 4vh → 5rem
Card Gap:  1rem → 2vw → 2.5rem

EVOLEA BRAND REQUIREMENTS:
1. NO emojis (SVG icons only)
2. Solid mobile menu backgrounds
3. Text shadows on all gradients
4. Real photos only (no AI for real content)
5. Butterfly never covers "A"
6. Bold, vibrant colors only
7. Every page has prism hero
8. Every page has page closer
9. Fredoka for headlines always
10. Test on mobile always
```

---

**Last Updated:** December 2024
**Version:** 1.0
**Maintainer:** EVOLEA Development Team
