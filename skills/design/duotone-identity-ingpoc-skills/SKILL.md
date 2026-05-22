---
name: duotone-identity
description: Use when designing app pages, typography, spacing, or any UI look and feel for the Identity Platform. Load for creating landing pages, chapter sections, SVG illustrations, or applying the duotone cream/charcoal design system. Keywords: design, ui, styling, theme, colors, layout
keywords: design, ui, theme, duotone, landing, svg, gsap, animation, styling
---

# Duotone Identity Design System

Anthropic-inspired duotone design language for Identity Platform. Strict cream/charcoal palette with intentional typography and animated SVG illustrations.

## Quick Reference

| Element | Value |
|---------|-------|
| **Primary Light** | `#FAF9F5` (cream) |
| **Primary Dark** | `#141413` (charcoal) |
| **Display Font** | Instrument Serif |
| **Body Font** | Inter |
| **SVG viewBox** | `500 x 500` |
| **Chapter Number** | `clamp(6rem, 15vw, 12rem)` italic |

---

## Color Palette

### Core Duotone Colors

```css
:root {
  --cream: #FAF9F5;    /* Light backgrounds, dark text */
  --charcoal: #141413; /* Dark backgrounds, light text */
}
```

### Usage Pattern

| Section | Background | Text |
|---------|------------|------|
| Light (Hero, Ch1, Ch3) | `var(--cream)` | `var(--charcoal)` |
| Dark (Ch2, Ch4, Finale) | `var(--charcoal)` | `var(--cream)` |

**Rule:** Never use other colors for primary UI. Accent colors only for interactive elements (wallet button, links).

### Section Alternating

```tsx
// Chapter 1, 3: Light
<section className="bg-[var(--cream)] text-[var(--charcoal)]">

// Chapter 2, 4: Dark
<section className="bg-[var(--charcoal)] text-[var(--cream)]">
```

---

## Typography

### Font Families

```css
/* Display / Headings */
font-family: 'Instrument Serif', Georgia, serif;

/* Body / UI */
font-family: 'Inter', -apple-system, sans-serif;
```

### Display Headings (H1, H2)

```css
.landing-h1 {
  font-size: clamp(3rem, 12vw, 8rem);
  line-height: 1;
  letter-spacing: -0.02em;
}

.landing-h2 {
  font-size: clamp(2rem, 6vw, 4.5rem);
  line-height: 1.15;
  letter-spacing: -0.02em;
}
```

### Chapter Labels

```tsx
<p className="text-xs md:text-sm font-semibold uppercase tracking-[0.2em] opacity-50 flex items-center gap-4">
  <span className="w-10 h-px bg-current opacity-50"></span>
  {label}
</p>
```

**Pattern:** 40px horizontal dash + uppercase text + 0.2em letter-spacing

### Chapter Numbers

```tsx
<span className="font-serif italic opacity-[0.08]"
      style={{ fontSize: 'clamp(6rem, 15vw, 12rem)', lineHeight: 1 }}>
  {String(number).padStart(2, '0')}
</span>
```

**Positioning:** `absolute top-4 left-4 md:top-8 md:left-8`

---

## Layout Patterns

### Chapter Section Structure

```tsx
<section className={`chapter ${isLight ? 'light' : 'dark'} min-h-screen flex items-center justify-center relative p-6 md:p-12 ${isLight ? 'bg-[var(--cream)] text-[var(--charcoal)]' : 'bg-[var(--charcoal)] text-[var(--cream)]'}`}>
  {/* Chapter Number - large, positioned */}
  <span className="chapter-number absolute top-4 left-4 md:top-8 md:left-8 font-serif italic opacity-[0.08]"
        style={{ fontSize: 'clamp(6rem, 15vw, 12rem)', lineHeight: 1 }}>
    {String(number).padStart(2, '0')}
  </span>

  <div className="chapter-inner grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12 max-w-6xl w-full relative z-10">
    {/* Content */}
    <div className="chapter-content">
      <p className="chapter-label text-xs md:text-sm font-semibold uppercase tracking-[0.2em] opacity-50 mb-4 flex items-center gap-4">
        <span className="w-10 h-px bg-current opacity-50"></span>
        {label}
      </p>
      <h2 className={`landing-h2 ${isLight ? 'text-[var(--charcoal)]' : 'text-[var(--cream)]'}`}>
        {title}
      </h2>
    </div>
    {/* Illustration */}
  </div>
</section>
```

**Key Rules:**

- Even chapters (2, 4): reverse layout (illustration left, content right)
- Odd chapters (1, 3): standard layout (content left, illustration right)
- Always explicitly set h2 color based on `isLight` (global CSS overrides)

---

## SVG Illustrations

### Standard viewBox

**Always use `viewBox="0 0 500 500"`** for consistency.

All coordinates must stay within 0-500 range to prevent clipping.

### Path Classes

| Class | Purpose | Animation |
|-------|---------|-----------|
| `.fill-path` | Shapes, filled elements | Opacity 0→0.9, scale 0.8→1 |
| `.draw-path` | Lines, strokes | strokeDashoffset animation |
| `.label-path` | Text labels | Opacity 0→0.7 |

### CSS Initial States

```css
.fill-path {
  opacity: 0;
  transform-origin: center;
  vector-effect: non-scaling-stroke;
}

.draw-path {
  opacity: 0;
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.label-path {
  opacity: 0;
  font-size: 14px;
  font-weight: 500;
  text-anchor: middle;
  pointer-events: none;
}
```

### Common SVG Patterns

**Person/Figure (Chapter 1):**

```tsx
<circle className="fill-path" cx="250" cy="140" r="35" fill="#141413" opacity="0"/>
<path className="fill-path" d="M 215 180 Q 200 220 210 280..." fill="#141413" opacity="0"/>
```

**Process Flow (Chapter 2):**

```tsx
{/* Horizontal left-to-right flow */}
<rect className="fill-path" x="60" y="200" width="80" height="60" fill="#FAF9F5" opacity="0"/>
<path className="draw-path" d="M 140 230 L 180 230" stroke="#FAF9F5" strokeWidth="2" opacity="0"/>
```

**Growth Trajectory (Chapter 3):**

```tsx
<path className="draw-path" d="M 50 420 Q 120 400 160 350..." stroke="#141413" strokeWidth="3" opacity="0"/>
<circle className="fill-path" cx="160" cy="350" r="10" fill="#141413" opacity="0"/>
```

**Central Hub (Chapter 4):**

```tsx
<circle className="fill-path" cx="250" cy="250" r="45" fill="#FAF9F5" opacity="0"/>
<circle className="draw-path" cx="250" cy="250" r="65" fill="none" stroke="#FAF9F5" strokeWidth="2" opacity="0"/>
```

---

## GSAP Animations

### Animation Pattern for Chapters

```typescript
import { gsap } from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export const useChapterAnimations = () => {
  useEffect(() => {
    const chapters = document.querySelectorAll('.chapter');
    if (chapters.length === 0) return;

    const ctx = gsap.context(() => {
      chapters.forEach((chapter) => {
        const fillPaths = chapter.querySelectorAll('.fill-path');
        const drawPaths = chapter.querySelectorAll('.draw-path');

        // Fill paths: opacity + scale
        if (fillPaths.length > 0) {
          gsap.to(fillPaths, {
            opacity: 0.9,
            scale: 1,
            duration: 0.8,
            stagger: 0.1,
            ease: 'back.out(1.5)',
            scrollTrigger: {
              trigger: chapter,
              start: 'top 80%',
              toggleActions: 'play none none reverse',
            },
          });
        }

        // Draw paths: stroke animation
        if (drawPaths.length > 0) {
          drawPaths.forEach(path => {
            const length = (path as SVGPathElement).getTotalLength() || 1000;
            (path as SVGPathElement).style.strokeDasharray = String(length);
            (path as SVGPathElement).style.strokeDashoffset = String(length);
          });

          gsap.to(drawPaths, {
            strokeDashoffset: 0,
            opacity: 0.6,
            duration: 1.5,
            stagger: 0.1,
            ease: 'power2.inOut',
            scrollTrigger: {
              trigger: chapter,
              start: 'top 75%',
              toggleActions: 'play none none reverse',
            },
          });
        }
      });
    });

    return () => ctx.revert();
  }, []);
};
```

### Key GSAP Rules

1. **Always use `gsap.context()`** for cleanup
2. **`toggleActions: 'play none none reverse'`** for reversible scroll animations
3. **Never use inline `style={{ transform: 'scale' }}`** - let GSAP handle all transforms
4. **Initialize strokeDasharray in the effect**, not inline styles
5. **stagger: 0.1** for sequential element animations

---

## Resources

### references/

- `palette.md` - Full color definitions with usage examples
- `typography.md` - Font loading, sizing, and heading styles
- `svg-patterns.md` - Common SVG illustration templates
- `gsap-recipes.md` - Copy-paste animation patterns

### scripts/

- `validate_colors.sh` - Check if colors match duotone palette
- `generate_chapter.sh` - Scaffold new chapter section

---

## Usage Examples

**Creating a new chapter:**

```
1. Use scripts/generate_chapter.sh 5
2. Add SVG to illustration container (500x500 viewBox)
3. Use fill-path/draw-path/label-path classes
4. Set isLight based on position (odd=light, even=dark)
```

**Validating colors:**

```
Use scripts/validate_colors.sh before committing to ensure only cream/charcoal are used
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|---------|--------|
| Use other colors for UI | Only cream/charcoal |
| Inline `style={{ scale }}` | Let GSAP animate |
| Different viewBox sizes | Always 500x500 |
| Coordinates outside 0-500 | Keep within bounds |
| Generic class names | Use fill-path/draw-path/label-path |
