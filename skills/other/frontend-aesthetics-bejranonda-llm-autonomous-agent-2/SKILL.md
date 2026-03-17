---
name: frontend-aesthetics
description: Distinctive frontend design principles for avoiding generic AI defaults, implementing thoughtful typography/color/animations, and creating polished user experiences based on Claude Code design research
version: 1.0.0
---

## Overview

This skill provides specific design principles and patterns for creating distinctive, polished frontend interfaces that avoid "AI slop" - the generic, obviously-generated aesthetic that results from default AI model choices. Based on official research from ["Improving frontend design through Skills"](https://claude.com/blog/improving-frontend-design-through-skills) by Anthropic.

**Skills Methodology**: This follows Anthropic's skills approach - reusable markdown documents that provide altitude-appropriate design guidance without permanent context overhead. Skills make effective design prompts contextual and reusable across projects.

**Core Problem: Distributional Convergence**: Language models naturally sample from the high-probability center of their training data distribution. This causes them to default to statistically common "safe choices" (Inter fonts, purple gradients, minimal animations, standard grid layouts) because these patterns dominate web design datasets. The result is bland, forgettable interfaces that lack intentional design decisions.

**Altitude-Appropriate Guidance**: This skill avoids both extremes:
- **Too Specific**: Prescribing exact hex codes or pixel values limits creativity
- **Too Vague**: Assuming models know design principles leads to generic defaults

Instead, it provides **contextual principles** with concrete examples that guide toward distinctive choices while preserving flexibility.

## The "AI Slop" Problem

### What Models Default To (Avoid These)

**Generic Fonts**:
- Inter, Roboto, Open Sans, Lato
- Default system fonts without customization
- Single font family for everything

**Generic Colors**:
- Purple-to-white gradients (#a855f7 → #ffffff)
- Plain white backgrounds
- Pastel color schemes without contrast
- Rainbow gradients

**Minimal Visual Interest**:
- No animations or micro-interactions
- Flat, single-layer backgrounds
- Standard grid layouts only
- No depth or texture

**Result**: Interface that looks "obviously AI-generated" - bland, safe, forgettable

### How to Recognize "AI Slop"

Calculate AI Slop Score (0-100, lower is better):
- +30 points: Using Inter/Roboto/Open Sans fonts
- +25 points: Purple gradient color scheme
- +20 points: Plain white background with no depth
- +15 points: No animations whatsoever
- +10 points: Standard grid layout only

**Score 60+**: High AI slop - needs significant design enhancement
**Score 30-59**: Moderate - some generic patterns present
**Score 0-29**: Distinctive - thoughtful design choices evident

## Typography Principles

### Avoid Generic Font Families

**Never Use (Without Strong Justification)**:
- Inter
- Roboto
- Open Sans
- Lato
- Helvetica Neue (as primary)
- Default system fonts

### Distinctive Font Recommendations

**Code/Technical Aesthetic**:
```
Primary: JetBrains Mono (headings, code blocks)
Secondary: Space Grotesk (body, UI)
Character: Modern, technical, developer-focused
```

**Editorial/Content**:
```
Primary: Playfair Display (headings, hero)
Secondary: Source Sans 3 (body)
Character: Classic, sophisticated, content-heavy
```

**Technical/Data**:
```
Primary: IBM Plex Sans (all text)
Secondary: IBM Plex Mono (code, data)
Character: Professional, systematic, dashboard-friendly
```

**Friendly/Playful**:
```
Primary: Fredoka (headings)
Secondary: Manrope (body)
Character: Approachable, consumer-facing, warm
```

**Elegant/Premium**:
```
Primary: Crimson Pro (headings)
Secondary: Karla (body)
Character: Sophisticated, refined, premium feel
```

### Font Pairing Principles

**High-Contrast Pairings** (Recommended):
Pair fonts from different categories for maximum distinctiveness:
- **Display + Monospace**: Playfair Display + JetBrains Mono
- **Serif + Geometric Sans**: Crimson Pro + Space Grotesk
- **Heavy Display + Light Sans**: Fredoka (700) + Manrope (300)

**Serif + Sans Pairing**:
- Use serif for headings (authority, elegance)
- Use sans-serif for body (readability)
- Ensure sufficient contrast in style (not both humanist)
- Example: Playfair Display + Source Sans 3

**Geometric + Humanist**:
- Geometric sans for headings (modern, structured)
- Humanist sans for body (friendly, readable)
- Example: Space Grotesk + Source Sans 3 (avoid Inter)

**Monospace + Sans**:
- Monospace for code, technical data, or distinctive headings
- Geometric/humanist sans for regular text
- Unified family approach when available (IBM Plex, JetBrains)
- Example: JetBrains Mono + Space Grotesk

**Extreme Weight Variations**:
Create hierarchy through dramatic weight differences:
- **Headings**: Use 100-200 (ultra-thin) OR 800-900 (extra-bold)
- **Body**: Use 300-400 (light to regular)
- **Avoid**: Medium weights (500-600) for headings - not distinctive enough
- **Example**: Manrope 200 for hero headings, Manrope 400 for body

**Size Jumps** (3x+ Ratio):
Create clear hierarchy with large size differences:
- **Hero**: 4rem (64px)
- **H1**: 2.5rem (40px) - not quite 3x but close
- **Body**: 1rem (16px) - 4x from hero
- **Avoid**: Incremental 1.5x jumps (too subtle)

**Variable Fonts** (Modern Approach):
- Single font file with multiple weights/styles
- Reduces HTTP requests
- Enables smooth weight transitions in animations
- Example: Manrope Variable, Inter Variable (if used thoughtfully)

### Typography Implementation

```css
/* Fluid Typography with clamp() */
:root {
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.825rem + 0.25vw, 1rem);
  --text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1.075rem + 0.25vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.35rem + 0.75vw, 2rem);
  --text-3xl: clamp(2rem, 1.75rem + 1.25vw, 3rem);
  --text-4xl: clamp(2.5rem, 2rem + 2.5vw, 4rem);
}

/* Type Scale with Clear Hierarchy */
.heading-1 {
  font-family: 'Playfair Display', serif;
  font-size: var(--text-4xl);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.heading-2 {
  font-family: 'Playfair Display', serif;
  font-size: var(--text-3xl);
  font-weight: 600;
  line-height: 1.2;
}

.body {
  font-family: 'Source Sans 3', sans-serif;
  font-size: var(--text-base);
  font-weight: 400;
  line-height: 1.6;
}
```

## Color Theory & Schemes

### Avoid Generic Color Schemes

**Never Use (Without Intentional Justification)**:
- Purple-on-white gradients (AI default)
- Plain #FFFFFF backgrounds
- Pastel rainbow without cohesion
- Generic Material Design colors verbatim

### Intentional Color Palette Design

**Principle**: Choose colors that create a **mood** and **brand identity**

**Ocean/Tech Professional**:
```
Primary: #0ea5e9 (sky blue)
Accent: #f59e0b (amber)
Background: #0f172a → #1e293b (dark slate gradient)
Text: #f8fafc / #cbd5e1 / #64748b
Mood: Professional, trustworthy, technical
```

**Sunset/Energetic**:
```
Primary: #f97316 (orange)
Accent: #ec4899 (pink)
Background: #fff7ed (light warm) with subtle gradients
Text: #1c1917 / #57534e / #78716c
Mood: Energetic, warm, inviting
```

**Forest/Calm**:
```
Primary: #059669 (emerald)
Accent: #facc15 (yellow)
Background: #f0fdf4 (light green) with layered depth
Text: #14532d / #166534 / #4ade80
Mood: Calm, natural, wellness
```

**Cyberpunk/Bold**:
```
Primary: #06b6d4 (cyan)
Accent: #f0abfc (fuchsia)
Background: #18181b (very dark) with neon glows
Text: #fafafa / #a1a1aa / #52525b
Mood: Modern, bold, tech-forward
```

### Color Application Principles

**Dominance Hierarchy**:
- Background: 60% of visual space
- Primary: 30% of elements
- Accent: 10% for highlights

**Contrast Requirements**:
- Text on background: Minimum 4.5:1 (WCAG AA)
- Large text: Minimum 3:1 (WCAG AA)
- Interactive elements: Clear hover/focus states
- Use tools: WebAIM Contrast Checker

**Semantic Color Usage**:
```
Success: Greens (#10b981, #22c55e)
Warning: Yellows/Oranges (#f59e0b, #eab308)
Error: Reds (#ef4444, #dc2626)
Info: Blues (#3b82f6, #0891b2)
```

**Implementation**:
```css
:root {
  --color-primary: 14 165 233;  /* RGB values for hsl() */
  --color-accent: 245 158 11;
  --color-bg-base: 15 23 42;
  --color-bg-surface: 30 41 59;
  --color-text-primary: 248 250 252;
}

/* Use with opacity */
.element {
  background-color: hsl(var(--color-primary) / 0.1);  /* 10% opacity */
  color: hsl(var(--color-text-primary));
}
```

## Background Depth & Texture

### Avoid Plain Backgrounds

**Never Use**:
- Solid white (#FFFFFF) with no variation
- Single-color backgrounds without depth
- Generic gradients alone

### Layered Background Techniques

**1. Subtle Noise Texture**:
```css
.background-noise {
  background-image:
    linear-gradient(135deg, hsl(var(--bg-base)) 0%, hsl(var(--bg-surface)) 100%),
    url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
}
```

**2. Geometric Grid Pattern**:
```css
.background-grid {
  background-image:
    linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px),
    linear-gradient(180deg, rgba(255,255,255,0.05) 1px, transparent 1px);
  background-size: 50px 50px;
}
```

**3. Radial Ambient Glow**:
```css
.background-glow {
  background:
    radial-gradient(circle at 20% 50%, rgba(14, 165, 233, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 50%, rgba(245, 158, 11, 0.1) 0%, transparent 50%),
    hsl(var(--bg-base));
}
```

**4. Layered SVG Waves**:
```css
.background-waves {
  background:
    linear-gradient(180deg, hsl(var(--primary) / 0.1) 0%, transparent 100%),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='rgba(255,255,255,0.05)' d='M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,144C960,149,1056,139,1152,128C1248,117,1344,107,1392,101.3L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z'%3E%3C/path%3E%3C/svg%3E") no-repeat bottom;
}
```

**5. Mesh Gradient (Modern)**:
```css
.background-mesh {
  background:
    radial-gradient(at 27% 37%, hsla(215, 98%, 61%, 0.3) 0px, transparent 50%),
    radial-gradient(at 97% 21%, hsla(125, 98%, 72%, 0.3) 0px, transparent 50%),
    radial-gradient(at 52% 99%, hsla(354, 98%, 61%, 0.3) 0px, transparent 50%),
    radial-gradient(at 10% 29%, hsla(256, 96%, 67%, 0.3) 0px, transparent 50%),
    radial-gradient(at 97% 96%, hsla(38, 60%, 74%, 0.3) 0px, transparent 50%),
    radial-gradient(at 33% 50%, hsla(222, 67%, 73%, 0.3) 0px, transparent 50%),
    radial-gradient(at 79% 53%, hsla(343, 68%, 79%, 0.3) 0px, transparent 50%);
}
```

## Animation & Motion Design

### Principle: High-Impact Moments Over Random Motion

**Core Insight**: One well-orchestrated page load with staggered reveals is worth more than a dozen random micro-animations scattered across the interface.

**Avoid**:
- Random animations everywhere without purpose
- Slow, drawn-out transitions that delay user interaction
- No animations at all (static interfaces feel lifeless)
- Animations that don't respect reduced-motion preferences

**Focus On High-Impact Moments**:
- **Page Load**: Create memorable first impression with orchestrated entrance
- **Major Transitions**: Route changes, modal appearances, significant state shifts
- **Content Reveal**: Progressive disclosure as user scrolls or interacts
- **Success Moments**: Celebrate user achievements with intentional motion
- **Purposeful Micro-Interactions**: Hover/click feedback that reinforces UI affordances

**Motion Priority**:
1. **Page Load Animation** (highest impact) - Users see this every time
2. **Major State Changes** (high impact) - Crucial for UX comprehension
3. **Micro-Interactions** (supporting) - Polish, not primary focus
4. **Decorative Motion** (lowest priority) - Use sparingly or omit

### Motion Library Selection

**Decision Framework**:
- **HTML-Only Projects**: Always use CSS animations (no dependencies, better performance)
- **React Projects**: Use [Framer Motion](https://www.framer.com/motion/) for complex choreography
- **Simple Transitions**: CSS is sufficient even in React
- **Complex Orchestration**: Motion library provides easier sequencing and stagger control

### Page Load Animation

**CSS-Only Approach** (HTML Projects, Simple React):
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.page-enter {
  animation: fadeInUp 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

/* Staggered children */
.stagger > :nth-child(1) { animation-delay: 0.1s; }
.stagger > :nth-child(2) { animation-delay: 0.2s; }
.stagger > :nth-child(3) { animation-delay: 0.3s; }
.stagger > :nth-child(4) { animation-delay: 0.4s; }
```

**React + Framer Motion** (For Complex Animations):
```typescript
import { motion } from 'framer-motion'

export default function Page({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.div>
  )
}

// Staggered list
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map((item) => (
    <motion.li key={item.id} variants={item}>
      {item.name}
    </motion.li>
  ))}
</motion.ul>
```

### Micro-Interactions

**Button Hover**:
```css
.button {
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
}

.button:active {
  transform: translateY(0);
  transition-duration: 0.1s;
}
```

**Card Hover**:
```css
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: scale(1.02);
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.15);
}
```

**Link Underline Animation**:
```css
.link {
  position: relative;
  text-decoration: none;
}

.link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.3s ease;
}

.link:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}
```

### Accessibility: Respect Reduced Motion

**Always Include**:
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
}
```

## Layout Innovation

### Break from Standard Grids

**Asymmetric Grid**:
```css
.hero-grid {
  display: grid;
  grid-template-columns: 1fr 1.5fr 1fr;
  grid-template-rows: auto auto;
  gap: 2rem;
}

.hero-text {
  grid-column: 1 / 3;
  grid-row: 1;
}

.hero-image {
  grid-column: 2 / 4;
  grid-row: 1 / 3;
  transform: translateY(-2rem);  /* Break alignment */
}
```

**Broken Grid Layout**:
```css
.content-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1.5rem;
}

.card-1 {
  grid-column: 1 / 6;
  grid-row: 1 / 3;
}

.card-2 {
  grid-column: 6 / 10;
  grid-row: 1 / 2;
  transform: translateY(2rem);  /* Offset for visual interest */
}

.card-3 {
  grid-column: 10 / 13;
  grid-row: 1 / 3;
}
```

**Overlapping Elements**:
```css
.overlap-container {
  position: relative;
}

.background-card {
  position: relative;
  z-index: 1;
}

.foreground-element {
  position: absolute;
  top: -2rem;
  left: -2rem;
  z-index: 2;
}
```

## Design Enhancement Checklist

Before considering design complete:

**Typography**:
- [ ] No generic fonts (Inter, Roboto, Open Sans, Lato)
- [ ] Clear font pairing strategy (serif + sans, mono + sans, etc.)
- [ ] Fluid typography with clamp() or responsive scale
- [ ] Clear hierarchy with size, weight, and spacing

**Color**:
- [ ] Intentional color palette (not purple-on-white default)
- [ ] Mood/brand identity expressed through colors
- [ ] WCAG AA contrast compliance (4.5:1 minimum)
- [ ] Semantic colors for success/warning/error/info

**Background**:
- [ ] Layered depth (not plain solid color)
- [ ] Subtle texture or pattern
- [ ] Visual interest without overwhelming content

**Animation**:
- [ ] Page load/transition animations present
- [ ] Micro-interactions on hover/click
- [ ] Purposeful animations (not random)
- [ ] `prefers-reduced-motion` respected

**Layout**:
- [ ] Not just standard grid (visual interest added)
- [ ] Clear visual rhythm and spacing
- [ ] Asymmetry or broken-grid elements where appropriate
- [ ] Responsive across all breakpoints

**Overall**:
- [ ] AI Slop Score < 30 (distinctive, intentional design)
- [ ] Design feels crafted, not generated
- [ ] Accessibility standards met
- [ ] Performance optimized (animations use transform/opacity)

## When to Apply

Use this skill when:
- Creating new frontend interfaces
- Enhancing existing designs that look generic
- Avoiding "AI-generated" aesthetic
- Implementing distinctive brand identity
- Designing landing pages, dashboards, or web applications
- Reviewing designs for visual appeal and distinction
- Training models to generate better design outputs

This approach ensures frontend designs are distinctive, polished, and intentional - not generic AI defaults.
