---
name: frontend-design-html
description: Create distinctive, production-grade HTML/CSS frontends with exceptional design quality
version: 1.0.0
framework: html-css-vanilla-js
tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Frontend Design HTML Skill

Create distinctive, production-grade HTML/CSS + vanilla JavaScript interfaces with high design quality. This skill combines the 5-dimension aesthetic framework with semantic HTML5, modern CSS, and CSS-only animations to build interfaces that are both beautiful and accessible.

---

## Base Aesthetics Framework

### Overview

This is the core 5-dimension framework for creating intentional, non-generic design that avoids the homogenized aesthetic of default AI outputs. Each dimension works together to create designs with personality and deliberation.

### The Five Dimensions

#### 1. Typography Dimension

**Purpose**: Typography is the primary carrier of voice and personality in digital design.

**Core Principles**:
- Typeface selection creates immediate emotional context
- Font pairings establish visual hierarchy and rhythm
- Weight and size extremes create contrast and emphasis
- Avoid: Inter, Roboto, Open Sans, Lato, system fonts (these are default AI outputs)
- Prefer: JetBrains Mono, Fira Code, Space Grotesk, Playfair Display, Crimson Pro, IBM Plex, Bricolage Grotesque

**Implementation**:
- Use high-contrast pairings: Display + Mono, Serif + Geometric Sans
- Employ weight extremes: 100/200 vs 800/900 (not mid-range weights)
- Apply size jumps of 3x or more, not incremental 1.5x steps
- Create visual hierarchy through deliberate typographic choices

**Example Pattern**:
- Display: Playfair Display (300, 400, 700)
- Body: IBM Plex Sans (400, 600)
- Mono: JetBrains Mono (400, 500)

#### 2. Color & Theme Dimension

**Purpose**: Color sets mood and creates visual coherence while avoiding cliché palettes.

**Core Principles**:
- Move beyond default color systems (Material Design, Tailwind defaults)
- Use unexpected but harmonious color relationships
- Consider context: what emotional response do you want?
- Saturation and tone matter as much as hue

**Anti-Patterns to Avoid**:
- Primaries: Blue, Red, Green (default AI trinity)
- Neutrals: Pure grays (#999999, #CCCCCC) without personality
- Monochrome gradients that feel soulless
- Color palettes that match "flat design" clichés

**Implementation**:
- Define color intent: Is this a warm, cool, energetic, or calm system?
- Use color psychology intentionally
- Create contrast through saturation, not just hue
- Reserve one unexpected accent color for personality

**Example Approach**:
- Warm palette: Cognac browns, terracotta, warm neutrals with olive undertones
- Cool palette: Deep indigos, soft teals, cool grays with blue undertones
- Accent: Single unexpected color for UI elements (e.g., sulfur yellow, coral pink)

#### 3. Motion Dimension

**Purpose**: Motion reveals personality and guides user attention with intentionality.

**Core Principles**:
- Motion should feel deliberate, not random
- Orchestrate page loads with staggered timing
- Use scroll triggers for engaged scrolling experiences
- Hover states should surprise, not just respond

**Implementation for HTML/CSS**:
- CSS-only animations with easing functions (ease-in-out, cubic-bezier)
- Page load: Stagger reveals with animation-delay (100ms, 200ms, 300ms)
- Scroll triggers: Use Intersection Observer API for elements animating in when viewport enters
- Hover: Add transforms, color shifts, or subtle scale changes

**Anti-Patterns**:
- Linear timing on everything (feels robotic)
- Instantaneous interactions (feels cold)
- Animation-heavy design that distracts from content

#### 4. Spatial Composition Dimension

**Purpose**: Space and layout create rhythm and guide the eye through intentional composition.

**Core Principles**:
- Use asymmetrical layouts when possible (more interesting than grid-perfect)
- Create breathing room with generous whitespace
- Build visual rhythm through consistent spacing systems
- Avoid centered, symmetrical layouts unless purposeful

**Implementation**:
- Define a spacing scale: 8px, 12px, 16px, 24px, 32px, 48px, 64px
- Use odd-numbered layouts: 3-column, 5-item, 7-section
- Create focal points through compositional weight
- Consider micro-interactions within spatial relationships

**Anti-Patterns**:
- Everything centered (feels safe but predictable)
- Uniform padding everywhere
- Layouts that could describe "generic SaaS dashboard"

#### 5. Backgrounds & Visual Details Dimension

**Purpose**: The foundation layer that can transform a generic design into something memorable.

**Core Principles**:
- Background should support, not distract
- Add subtle details that reward close observation
- Use gradients intentionally, not as default effects
- Create texture through digital or illustrated means

**Implementation**:
- Subtle gradients: Use 2-3 colors with minimal contrast (40-60° angles)
- Illustrated patterns: Geometric, organic, or custom SVG elements
- Texture overlays: Subtle noise or grain (2-5% opacity)
- Micro-illustrations: Small graphics that reinforce brand voice

**Anti-Patterns**:
- Bland white backgrounds (consider soft colors instead)
- Obvious gradients (rainbow, neon contrasts)
- Busy patterns that compete with content
- Decorative elements that serve no purpose

### Anti-Generic-AI Guardrails

Use these checks to ensure your design doesn't default to generic AI output:

**Typography Check**:
- [ ] Does the typeface choice feel intentional or like a default?
- [ ] Are size jumps extreme (3x+) or incremental?
- [ ] Do font pairings create surprise and interest?

**Color Check**:
- [ ] Could this palette exist in a Material Design system?
- [ ] Do the colors feel chosen or randomly selected?
- [ ] Is there one unexpected accent color that creates personality?

**Motion Check**:
- [ ] Does animation feel orchestrated or reactive?
- [ ] Are timing curves deliberate or linear?
- [ ] Do hover states surprise or just respond?

**Spatial Check**:
- [ ] Is the layout asymmetrical or cookie-cutter centered?
- [ ] Does whitespace feel generous or cramped?
- [ ] Could the layout be described as "standard SaaS"?

**Background Check**:
- [ ] Is the background supporting or distracting?
- [ ] Are gradients subtle or obvious?
- [ ] Do visual details reward close observation?

---

## Typography Guidance

### Typefaces to Avoid

These fonts are ubiquitous in default AI outputs and should be rejected as your primary choice:

- **Inter**: Google's modern sans-serif, used everywhere in AI-generated design
- **Roboto**: Android's default, synonymous with generic design
- **Open Sans**: Neutral and safe, but overused
- **Lato**: Round and friendly, but lacks personality
- **System fonts**: Default OS fonts (SF Pro Display, Segoe UI) feel lazy

> If you use any of these, pair them with something unexpected and deliberately break the generic pattern.

### Typefaces to Prefer

These faces bring personality and intention to design:

#### Display & Decorative
- **Playfair Display**: Elegant serif, high contrast, sophisticated
- **Bricolage Grotesque**: Modern sans with personality, handcrafted feel
- **Space Grotesk**: Geometric sans with character, works for display or body
- **Crimson Pro**: High-contrast serif, literary and elegant

#### Body & Copy
- **IBM Plex Sans**: Humanist sans with warmth, works at all sizes
- **Space Grotesk**: Geometric sans that reads well in small sizes
- **Crimson Pro**: Serif for long-form content, distinctive personality

#### Monospace (Technical, Quotes, Code)
- **JetBrains Mono**: Designed for code, readable and stylish
- **Fira Code**: Open source, ligatures for programming
- **IBM Plex Mono**: Humanist monospace, readable at any size

### Pairing Strategy

#### High-Contrast Pairings (Recommended)

**Pattern 1: Display + Mono**
```
Headline: Playfair Display (elegant serif)
Body: JetBrains Mono (technical monospace)
Result: Sophisticated + Modern
```

**Pattern 2: Serif + Geometric Sans**
```
Headline: Crimson Pro (high-contrast serif)
Body: Space Grotesk (geometric sans)
Result: Elegant + Contemporary
```

**Pattern 3: Decorative + Humanist**
```
Headline: Bricolage Grotesque (handcrafted sans)
Body: IBM Plex Sans (warm humanist sans)
Result: Crafted + Approachable
```

### Avoid Sameness
Don't use two similar typefaces:
- ❌ Roboto Display + Roboto Body (feels flat)
- ❌ Inter + Open Sans (indistinguishable)
- ✅ Playfair Display + JetBrains Mono (creates contrast)

### Font Weights & Extremes

#### Weight Strategy

Use weight extremes to create contrast, not mid-range weights:

**Good**:
- Display: 300 (thin) or 700/800 (heavy)
- Body: 400 (regular) or 600 (semi-bold)
- Emphasis: 800/900 for strong hierarchy

**Avoid**:
- Middle weights everywhere (400, 500, 500) feels muddled
- Limited weight range (only 400, 500, 600) lacks contrast
- No visual distinction between hierarchy levels

### Size Jumps: Extreme Over Incremental

#### Size Scale Strategy

Use 3x+ jumps between hierarchy levels, not incremental 1.5x steps:

**Generic (Linear Scaling)**:
```
H1: 48px
H2: 36px (75% of H1)
H3: 28px (78% of H2)
Body: 16px
Small: 14px
```
Result: Feels predictable, every size feels similar distance apart.

**Intentional (3x+ Jumps)**:
```
Display: 96px (3x body)
Headline: 48px (3x body)
Sub-headline: 28px (1.75x body)
Body: 16px
Caption: 12px (0.75x body)
```
Result: Creates clear visual hierarchy, extreme sizes make smaller sizes feel intentional.

#### Implementation Rules

1. Start with body size (16px or 18px is standard)
2. Create display size as 4-6x body (64px-96px)
3. Create headline as 2-3x body (32px-48px)
4. All other sizes fall between these extremes
5. Use odd numbers when possible (not round 10px increments)

**Example: 16px Base**
- Display: 88px (5.5x)
- Headline: 48px (3x)
- Sub-headline: 28px (1.75x)
- Body: 16px (1x)
- Small: 13px (0.8x)

### Line Height & Letter Spacing

#### Line Height Strategy

- **Display (90px+)**: 1.0-1.1 (tight, confident)
- **Headline (40px+)**: 1.1-1.2 (tight)
- **Sub-headline (24px+)**: 1.2-1.3 (moderate)
- **Body (14px-20px)**: 1.4-1.6 (loose for readability)
- **Small text (<14px)**: 1.5-1.7 (extra loose for clarity)

#### Letter Spacing Strategy

- **Display (90px+)**: -0.5 to -1px (negative space tightens)
- **Headline (40px+)**: -0.25px (subtle tightening)
- **Body**: 0px (default)
- **Emphasis/Caps**: +0.5px to +1px (opens up all-caps)

### CSS Font Stack Example

```css
/* Display */
.display {
  font-family: 'Playfair Display', serif;
  font-size: 88px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.5px;
}

/* Headline */
.h1 {
  font-family: 'Playfair Display', serif;
  font-size: 48px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.25px;
}

/* Body */
.body {
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.6;
  letter-spacing: 0;
}

/* Monospace (Code/Quotes) */
.mono {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: 0.5px;
}

/* Small Text */
.caption {
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 12px;
  font-weight: 400;
  line-height: 1.7;
  letter-spacing: 0px;
}
```

### Font Loading (Google Fonts)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=IBM+Plex+Sans:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### Typography Checklist

- [ ] Have you rejected default fonts (Inter, Roboto, Open Sans, Lato)?
- [ ] Do your chosen typefaces create visual contrast?
- [ ] Are font sizes using 3x+ jumps or are they incremental?
- [ ] Do weights span the full range (300-900) or are they mid-range?
- [ ] Is there a clear hierarchy that's immediately visible?
- [ ] Does the pairing feel intentional, not accidental?
- [ ] Would you describe this typography as "generic" or "distinctive"?

---

## Motion & Animation Guidance

### Overview

Motion reveals personality and guides user attention with intentionality. Deliberate animation transforms passive interfaces into experiences that feel alive and considered.

### Core Principles

1. **Orchestration**: Animations should feel planned, not random
2. **Purpose**: Every animation should serve a functional or emotional purpose
3. **Timing**: Easing functions matter more than duration
4. **Context**: Page loads, scrolls, and hovers each have different animation strategies

### CSS Animations

Use CSS for simple, performant animations that run on page load or interaction:

#### Basic Fade-In
```css
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.element {
  animation: fadeIn 0.6s ease-out;
}
```

#### Slide + Fade In
```css
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.element {
  animation: slideInUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

#### Scale + Fade In
```css
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

.element {
  animation: scaleIn 0.5s ease-out;
}
```

### Page Load Animation Strategy

#### Orchestrated Reveal

Don't animate everything at once. Create a sequence that guides the user's eye:

**Timing Sequence**
```
0ms    - Background/Hero fades in
200ms  - Headline slides in from top
400ms  - Sub-headline fades in
600ms  - Primary CTA appears
800ms  - Supporting content staggered reveal
```

**CSS Implementation**
```css
.hero {
  animation: fadeIn 0.8s ease-out 0ms;
}

.headline {
  animation: slideInDown 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 200ms backwards;
}

.subheadline {
  animation: fadeIn 0.6s ease-out 400ms backwards;
}

.cta {
  animation: scaleIn 0.5s ease-out 600ms backwards;
}

.content-item {
  animation: slideInUp 0.8s ease-out backwards;
}

.content-item:nth-child(1) { animation-delay: 800ms; }
.content-item:nth-child(2) { animation-delay: 900ms; }
.content-item:nth-child(3) { animation-delay: 1000ms; }
```

### Staggered Reveals

#### Using animation-delay (CSS)

Stagger elements to create a cascade effect:

```css
.list-item {
  opacity: 0;
  animation: slideInUp 0.8s ease-out forwards;
}

.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 100ms; }
.list-item:nth-child(3) { animation-delay: 200ms; }
.list-item:nth-child(4) { animation-delay: 300ms; }
.list-item:nth-child(5) { animation-delay: 400ms; }
```

### Scroll Trigger Animations

#### Intersection Observer (Vanilla JS)

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in');
      observer.unobserve(entry.target);
    }
  });
});

document.querySelectorAll('[data-animate]').forEach((el) => {
  observer.observe(el);
});
```

```css
[data-animate] {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s ease-out;
}

[data-animate].animate-in {
  opacity: 1;
  transform: translateY(0);
}
```

### Hover State Surprises

Hover interactions should be delightful, not just functional:

#### CSS Hover Animations

```css
.card {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.2);
}

/* Icon rotation on hover */
.icon {
  transition: transform 0.3s ease-out;
}

.card:hover .icon {
  transform: rotate(45deg) scale(1.1);
}

/* Text color shift */
.link {
  color: #333;
  transition: color 0.3s ease-out;
  border-bottom: 2px solid transparent;
  transition: border-color 0.3s ease-out;
}

.link:hover {
  color: #0099ff;
  border-bottom-color: #0099ff;
}
```

### Easing Functions

#### Recommended Easing Values

- **ease-out**: 0.16, 0.04, 0.04, 1 (default snappy)
- **ease-in-out**: 0.42, 0, 0.58, 1 (smooth, balanced)
- **elastic**: cubic-bezier(0.34, 1.56, 0.64, 1) (playful overshoot)
- **sharp**: cubic-bezier(0.4, 0, 0.6, 1) (quick and direct)

### Anti-Patterns to Avoid

- **Linear timing**: Feels robotic, use easing instead
- **Instant interactions**: Feels cold, add 0.2-0.4s minimum transitions
- **Animation-heavy**: Don't animate everything; be selective
- **Slow animations**: >1s feels sluggish unless intentional
- **Predictable patterns**: Vary easing, duration, and delay

---

## Design Thinking: Pre-Coding Workflow

### Overview

Before writing code or generating design, establish the intentional foundation. This workflow prevents default thinking and ensures your design serves a purpose beyond aesthetic choice.

### The Pre-Design Checklist

Don't design until you answer these four questions:

1. **Purpose**: What problem are we solving? Who are we solving it for?
2. **Tone**: What emotional response do we want? What aesthetic direction reflects this?
3. **Constraints**: What are the real technical, temporal, or business limits?
4. **Differentiation**: What one unforgettable element makes this distinctly ours?

### 1. Purpose: Problem & Users

#### Understand the Problem

Before choosing any visual element, define what you're solving:

**Questions to Answer**:
- What specific problem does this design solve?
- Who are the primary users? (age, technical skill, context)
- What emotions are they bringing to this interface? (frustrated, excited, skeptical)
- What's the desired outcome after interaction?
- What makes this problem unique vs. competitors?

#### User Context Worksheet

```
Primary User:
- Age & background: ___________
- Technical skill level: ___________
- Primary use context: (work, leisure, research, etc.)
- How much time will they spend here? ___________
- What's their emotional state on arrival? ___________

Problem They're Solving:
- Specific challenge: ___________
- Current workaround (how do they solve it now?): ___________
- Desired outcome: ___________
- What's the cost of not solving it? ___________

Success Metrics:
- How will we know if this design works? ___________
- What behavior change indicates success? ___________
```

### 2. Tone: Aesthetic Direction

#### Define Emotional Intent

Based on your purpose, what emotional response should the design evoke?

**Emotional Directions**:
- **Trustworthy**: Professional, calm, reliable (finance, healthcare)
- **Energetic**: Playful, bold, surprising (creator tools, social)
- **Sophisticated**: Elegant, refined, literary (luxury, editorial)
- **Direct**: Minimal, fast, no-nonsense (productivity tools)
- **Warm**: Inviting, personable, human (community, education)
- **Bold**: Confident, unconventional, statement-making (startups, innovation)

#### Tone Definition Worksheet

```
Emotional Intent:
- Primary emotion we want users to feel: ___________
- Tone adjectives (3-5): ___________
- What should users think when they see this? ___________
- What should they feel when they interact? ___________

Design Personality:
- Is this design "serious" or "playful"?
- Is it "minimal" or "expressive"?
- Is it "traditional" or "unconventional"?
- Is it "warm" or "cool"?

Visual Direction:
- Color personality: (warm, cool, saturated, muted)
- Typography style: (traditional, modern, handcrafted, geometric)
- Motion style: (snappy, smooth, playful, none)
- Overall style: (minimalist, maximalist, balanced)
```

### 3. Constraints: Reality Check

#### Define Technical, Business, and Creative Limits

Before designing, know your boundaries:

**Categories**:
- **Technical**: Browser support, performance budget, framework limitations
- **Temporal**: How long do you have to build?
- **Business**: Brand guidelines, compliance requirements, market positioning
- **Creative**: Audience expectations, competitive landscape

#### Constraints Worksheet

```
Technical Constraints:
- Required browser support: ___________
- Performance budget: (load time, interaction delay)
- Required frameworks/libraries: ___________
- API availability/limitations: ___________
- Device support (mobile first?): ___________

Temporal Constraints:
- Design timeline: ___________
- Development timeline: ___________
- Launch date: ___________
- Available resources: ___________

Business Constraints:
- Brand guidelines to follow: (yes/no, which parts?)
- Compliance requirements: (WCAG, GDPR, etc.)
- Target market expectations: ___________
- Pricing/positioning tier: (premium, budget, etc.)

Creative Freedom:
- How much can we deviate from industry norms?
- Are we required to use specific design patterns?
- Any visual or interaction taboos?
```

### 4. Differentiation: The Unforgettable Element

#### Identify One Distinctive Feature

Every intentional design has one element that makes it memorable and distinctly yours. This isn't about complexity—it's about one deliberate choice that stands out.

#### Differentiation Framework

**Types of Differentiation**:

1. **Typography Signature**
   - A distinctive typeface pairing
   - Unusual size or weight hierarchy
   - Custom font treatment
   - Example: "We pair serif headlines with monospace body text"

2. **Color Signature**
   - An unexpected color choice in an expected place
   - A color that exists nowhere else in the category
   - Color that tells a story
   - Example: "Burnt orange accent in a tool that's usually all blue"

3. **Motion Signature**
   - A particular animation pattern no one else uses
   - Orchestration that guides the eye
   - A interaction that feels unique
   - Example: "Staggered reveals that feel orchestrated, not random"

4. **Layout/Composition Signature**
   - An unusual spatial arrangement
   - Asymmetrical composition
   - Unexpected visual rhythm
   - Example: "Sidebar on the right instead of left"

5. **Micro-interaction Signature**
   - A delight that appears on interaction
   - Easter egg or surprise element
   - Unique feedback pattern
   - Example: "Icons that animate in unexpected ways on hover"

6. **Visual Detail Signature**
   - Illustration style
   - Pattern or texture
   - Specific visual treatment
   - Example: "Custom illustrations that appear throughout"

#### Differentiation Worksheet

```
Current State (What do competitors do?):
- Typography: ___________
- Color: ___________
- Motion: ___________
- Layout: ___________
- Interactions: ___________

Our Differentiation (What will we do differently?):
- Chosen category: (Typography, Color, Motion, etc.)
- The specific distinctive choice: ___________
- Why this choice? (How does it serve the purpose & tone?)
- Where will it appear? (Headline, accent, hover state, etc.)
- Is it instantly recognizable as "ours"? (Yes/No)

The Unforgettable Element:
- In one sentence, describe what makes this design distinctly ours:
  ___________
```

### Pre-Design Workflow: The Complete Picture

Before you design, complete this:

```
1. PROBLEM & USERS ✓
   Problem: ___________
   Primary user: ___________
   Their emotion on arrival: ___________
   Success metric: ___________

2. TONE & AESTHETICS ✓
   Emotional intent: ___________
   Tone adjectives: ___________
   Personality: (Serious/Playful, Minimal/Expressive, etc.)
   Visual direction: ___________

3. CONSTRAINTS ✓
   Technical: ___________
   Temporal: ___________
   Business: ___________
   Creative freedom level: ___________

4. DIFFERENTIATION ✓
   Unforgettable element: ___________
   Why this specific choice: ___________
   Where it appears: ___________

5. READY TO DESIGN ✓
   All four questions answered: (Yes/No)
   Team alignment on direction: (Yes/No)
   Prepared to brief designer/engineer: (Yes/No)
```

---

## Anti-Patterns: What to Avoid

### Typography Anti-Patterns

**Avoid**:
- Inter for everything (default AI choice)
- Roboto for everything (default Android)
- Open Sans for everything (neutral = forgettable)
- Lato for everything (too friendly, lacks edge)
- System fonts (-apple-system, system-ui)

Result: Immediately reads as "default AI design," no personality.

### Color & Theme Anti-Patterns

**Avoid**:
- **Material Design Trinity**: Blue, Red, Green as primary, secondary, accent
- **Default SaaS Colors**: Cool blues (#0099ff, #0066cc) everywhere
- **Rainbow Palette**: Every color at full saturation
- **Pure Grays**: #999999, #CCCCCC without personality
- **Inverted Black/White**: No mid-tones or color

Identifies as: "I used the default design system"

### Layout & Spatial Anti-Patterns

**Avoid**:
- Everything centered (feels safe but predictable)
- Symmetrical on both sides
- Predictable grid alignment
- "Stacked boxes" arrangement
- Uniform padding everywhere
- Same padding on all elements

Reads as: "Default SaaS dashboard"

### Motion & Animation Anti-Patterns

**Avoid**:
- Linear timing on everything (feels robotic)
- No animation at all (instant page loads feel cold)
- Animation-heavy design that distracts from content
- Slow, sluggish motion (>1s feels sluggish unless intentional)

### Background & Visual Details Anti-Patterns

**Avoid**:
- Pure white (#ffffff) with no texture
- Rainbow gradients (kitsch)
- High-contrast gradients (0% to 100%)
- Busy, distracting patterns
- Patterns that compete with content
- Generic illustration styles

---

## HTML/CSS-Specific Guidance

### Semantic HTML5 Elements

Always use semantic elements for structure and accessibility:

```html
<header>
  <!-- Site header, logo, primary navigation -->
</header>

<nav>
  <!-- Navigation links -->
</nav>

<main>
  <!-- Primary page content -->
  <article>
    <!-- Self-contained content -->
    <section>
      <!-- Thematic grouping -->
    </section>
  </article>

  <aside>
    <!-- Tangential content, sidebars -->
  </aside>
</main>

<footer>
  <!-- Site footer, secondary links, metadata -->
</footer>
```

### CSS Grid and Flexbox

Use CSS Grid for complex layouts and Flexbox for component-level organization:

```css
/* Grid for page layout */
body {
  display: grid;
  grid-template-columns: 1fr minmax(0, 64rem) 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

header {
  grid-column: 1 / -1;
}

main {
  grid-column: 2;
}

/* Flexbox for component alignment */
.card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

### CSS Custom Properties (Variables)

Define color, spacing, and typography in custom properties for easy theming:

```css
:root {
  /* Colors */
  --color-primary: #2d3748;
  --color-accent: #d4a574; /* Warm brown accent */
  --color-background: #f7f5f2; /* Warm cream */
  --color-text: #3d3d3d;

  /* Typography */
  --font-display: 'Playfair Display', serif;
  --font-body: 'IBM Plex Sans', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Spacing */
  --space-xs: 0.5rem;
  --space-sm: 0.75rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
  --space-3xl: 4rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);

  /* Transitions */
  --transition-fast: 0.2s ease-out;
  --transition-base: 0.3s ease-out;
  --transition-slow: 0.6s ease-out;
}
```

### Mobile-First Responsive Design

Start with mobile layout, then enhance for larger screens:

```css
/* Mobile-first (default) */
.container {
  width: 100%;
  padding: var(--space-md);
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    max-width: 768px;
    margin: 0 auto;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }
}
```

### WCAG 2.1 Level AA Compliance

Build accessibility into your design:

```html
<!-- Use proper heading hierarchy -->
<h1>Page Title</h1>
<h2>Section Heading</h2>
<h3>Subsection</h3>

<!-- Always include alt text -->
<img src="hero.jpg" alt="Descriptive text about the image">

<!-- Use ARIA attributes when needed -->
<button aria-label="Close dialog" aria-pressed="false">
  ✕
</button>

<!-- Ensure color contrast ratios are sufficient -->
<!-- Aim for 4.5:1 for normal text, 3:1 for large text -->
```

```css
/* Ensure focus indicators are visible */
:focus {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* Use sufficient line height for readability -->
body {
  line-height: 1.6;
}

/* Ensure touch targets are at least 44x44px -->
button {
  min-height: 44px;
  min-width: 44px;
}
```

---

## Implementation Workflow

Before coding, complete the design thinking worksheet:

### 1. Design Thinking Phase
- **Purpose**: [Define problem and users]
- **Tone**: [Choose extreme aesthetic direction]
- **Constraints**: [Technical requirements]
- **Differentiation**: [Unforgettable element]

### 2. Typography Dimension
- [Select distinctive fonts from approved list]
- [Define weight extremes and size jumps]
- [Create high-contrast pairings]

### 3. Color & Theme Dimension
- [Choose cohesive color palette with CSS variables]
- [Dominant colors with sharp accents]
- [Avoid generic schemes]

### 4. Motion Dimension
- [Design orchestrated page load]
- [Staggered reveals with animation-delay]
- [Hover states and scroll triggers]
- [CSS-only, no JavaScript animation libraries]

### 5. Spatial Composition Dimension
- [Plan unexpected layouts]
- [Asymmetry, overlap, diagonal flow]
- [Grid-breaking elements]

### 6. Backgrounds & Visual Details Dimension
- [Create atmospheric depth]
- [Layer gradients, patterns, effects]
- [Avoid solid colors]

### 7. Implementation
- Write semantic HTML5
- Implement CSS with custom properties
- Add CSS animations and transitions
- Use Intersection Observer for scroll triggers
- Ensure accessibility (ARIA, keyboard navigation, focus indicators)
- Test responsiveness (mobile, tablet, desktop)

### 8. Validation
- **Design Quality**: Check against anti-patterns list
- **Accessibility**: WCAG 2.1 Level AA compliance
- **Performance**: Optimize CSS, minimize reflows, use hardware acceleration
- **Cross-browser**: Test in modern browsers (Chrome, Firefox, Safari, Edge)

---

## Pre-Submit Checklist

Before delivering, verify:

- [ ] NO generic fonts (Inter, Roboto, Arial, system fonts)
- [ ] NO purple gradients on white backgrounds
- [ ] NO centered, predictable layouts
- [ ] YES to distinctive font choices with extreme weights
- [ ] YES to cohesive color palette with CSS variables
- [ ] YES to orchestrated animations (staggered page load)
- [ ] YES to unexpected spatial composition
- [ ] YES to atmospheric backgrounds (not solid colors)
- [ ] YES to WCAG 2.1 Level AA compliance
- [ ] YES to semantic HTML5 elements
- [ ] YES to CSS-only animations (no JS animation libraries)
- [ ] YES to mobile-first responsive design
- [ ] YES to accessible focus states and keyboard navigation
- [ ] YES to performance optimization

---

## Resources

- **Google Fonts**: https://fonts.google.com
- **Color Theory**: Emotional context and psychological associations
- **Motion Design**: "The Illusion of Life" by Disney animators
- **Accessibility**: WCAG 2.1 Guidelines (https://www.w3.org/WAI/WCAG21/quickref/)
- **CSS Reference**: MDN Web Docs (https://developer.mozilla.org/en-US/docs/Web/CSS/)
