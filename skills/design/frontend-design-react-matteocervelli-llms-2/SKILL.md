---
name: frontend-design-react
description: Create distinctive, production-grade React/TypeScript frontends with exceptional design quality
version: 1.0.0
framework: react-typescript
tools: [Read, Write, Edit, Grep, Glob, Bash]
dependencies: [react, react-dom, framer-motion, @types/react, @types/react-dom, typescript]
---

# Frontend Design React Skill

Create distinctive, production-grade React frontends with TypeScript and exceptional design quality. This skill integrates the 5-dimension design framework with React-specific patterns, Framer Motion animations, and accessibility best practices.

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

**Implementation**:
- **React**: Motion library (Framer Motion) for state-driven animation
- Page load: Stagger reveals with animation-delay (100ms, 200ms, 300ms)
- Scroll triggers: Elements animate in when viewport enters
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

**Display & Decorative**:
- **Playfair Display**: Elegant serif, high contrast, sophisticated
- **Bricolage Grotesque**: Modern sans with personality, handcrafted feel
- **Space Grotesk**: Geometric sans with character, works for display or body
- **Crimson Pro**: High-contrast serif, literary and elegant

**Body & Copy**:
- **IBM Plex Sans**: Humanist sans with warmth, works at all sizes
- **Space Grotesk**: Geometric sans that reads well in small sizes
- **Crimson Pro**: Serif for long-form content, distinctive personality

**Monospace (Technical, Quotes, Code)**:
- **JetBrains Mono**: Designed for code, readable and stylish
- **Fira Code**: Open source, ligatures for programming
- **IBM Plex Mono**: Humanist monospace, readable at any size

### Pairing Strategy

**High-Contrast Pairings (Recommended)**:

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

**Implementation Rules**:

1. Start with body size (16px or 18px is standard)
2. Create display size as 4-6x body (64px-96px)
3. Create headline as 2-3x body (32px-48px)
4. All other sizes fall between these extremes
5. Use odd numbers when possible (not round 10px increments)

**Example: 16px Base**:
- Display: 88px (5.5x)
- Headline: 48px (3x)
- Sub-headline: 28px (1.75x)
- Body: 16px (1x)
- Small: 13px (0.8x)

### Line Height & Letter Spacing

**Line Height Strategy**:
- **Display (90px+)**: 1.0-1.1 (tight, confident)
- **Headline (40px+)**: 1.1-1.2 (tight)
- **Sub-headline (24px+)**: 1.2-1.3 (moderate)
- **Body (14px-20px)**: 1.4-1.6 (loose for readability)
- **Small text (<14px)**: 1.5-1.7 (extra loose for clarity)

**Letter Spacing Strategy**:
- **Display (90px+)**: -0.5 to -1px (negative space tightens)
- **Headline (40px+)**: -0.25px (subtle tightening)
- **Body**: 0px (default)
- **Emphasis/Caps**: +0.5px to +1px (opens up all-caps)

### CSS-in-JS Implementation (Styled Components)

```typescript
import styled from 'styled-components';

export const TypographyTokens = {
  display: {
    fontSize: '88px',
    fontFamily: "'Playfair Display', serif",
    fontWeight: 700,
    lineHeight: 1.1,
    letterSpacing: '-0.5px',
  },
  h1: {
    fontSize: '48px',
    fontFamily: "'Playfair Display', serif",
    fontWeight: 700,
    lineHeight: 1.2,
    letterSpacing: '-0.25px',
  },
  body: {
    fontSize: '16px',
    fontFamily: "'IBM Plex Sans', sans-serif",
    fontWeight: 400,
    lineHeight: 1.6,
    letterSpacing: 0,
  },
  mono: {
    fontSize: '14px',
    fontFamily: "'JetBrains Mono', monospace",
    fontWeight: 400,
    lineHeight: 1.5,
    letterSpacing: '0.5px',
  },
  caption: {
    fontSize: '12px',
    fontFamily: "'IBM Plex Sans', sans-serif",
    fontWeight: 400,
    lineHeight: 1.7,
    letterSpacing: 0,
  },
};

export const Display = styled.h1`
  ${Object.entries(TypographyTokens.display)
    .map(([key, value]) => `${key}: ${value};`)
    .join('\n')}
`;

export const Heading = styled.h2`
  ${Object.entries(TypographyTokens.h1)
    .map(([key, value]) => `${key}: ${value};`)
    .join('\n')}
`;

export const Body = styled.p`
  ${Object.entries(TypographyTokens.body)
    .map(([key, value]) => `${key}: ${value};`)
    .join('\n')}
`;
```

### Font Loading (Google Fonts in React)

```typescript
// In your main App.tsx or _document.tsx
import { useEffect } from 'react';

export function FontLoader() {
  useEffect(() => {
    const link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@300;400;700&family=IBM+Plex+Sans:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap';
    link.rel = 'stylesheet';
    document.head.appendChild(link);
  }, []);

  return null;
}
```

### Typography Checklist

- [ ] Have you rejected default fonts (Inter, Roboto, Open Sans, Lato)?
- [ ] Do your chosen typefaces create visual contrast?
- [ ] Are font sizes using 3x+ jumps or are they incremental?
- [ ] Do weights span the full range (300-900) or are they mid-range?
- [ ] Is there a clear hierarchy that's immediately visible?
- [ ] Does the pairing feel intentional, not accidental?
- [ ] Would you describe this typography as "generic" or "distinctive"?

## Motion & Animation Guidance (React/Framer Motion)

### Overview

Motion reveals personality and guides user attention with intentionality. Deliberate animation transforms passive interfaces into experiences that feel alive and considered.

### Core Principles

1. **Orchestration**: Animations should feel planned, not random
2. **Purpose**: Every animation should serve a functional or emotional purpose
3. **Timing**: Easing functions matter more than duration
4. **Context**: Page loads, scrolls, and hovers each have different animation strategies

### React/Framer Motion Animations

Use Framer Motion for state-driven animations and complex sequences:

**Basic Animation**:
```tsx
import { motion } from 'framer-motion';

export function AnimatedCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.6,
        ease: "easeOut"
      }}
    >
      Card content
    </motion.div>
  );
}
```

**Staggered Children Animation**:
```tsx
import { motion } from 'framer-motion';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const childVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: "easeOut" },
  },
};

export function AnimatedList({ items }: { items: Array<any> }) {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map((item) => (
        <motion.div key={item.id} variants={childVariants}>
          {item.content}
        </motion.div>
      ))}
    </motion.div>
  );
}
```

### Page Load Animation Strategy

**Orchestrated Reveal**:

Don't animate everything at once. Create a sequence that guides the user's eye:

```tsx
import { motion } from 'framer-motion';

export function PageLoad() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.2 },
    },
  };

  return (
    <>
      <motion.div
        className="hero"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      />
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
      >
        Headline
      </motion.h1>
      <motion.div
        className="content"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Content items */}
      </motion.div>
    </>
  );
}
```

**Timing Sequence**:
```
0ms    - Background/Hero fades in
200ms  - Headline slides in from top
400ms  - Sub-headline fades in
600ms  - Primary CTA appears
800ms  - Supporting content staggered reveal
```

### Scroll Trigger Animations

Using Framer Motion with scroll events:

```tsx
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

export function ScrollReveal({ children }: { children: React.ReactNode }) {
  const { ref, inView } = useInView({ threshold: 0.1 });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 40 }}
      animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 40 }}
      transition={{ duration: 0.8, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
```

### Hover State Surprises

Hover interactions should be delightful, not just functional:

```tsx
export function HoverCard() {
  return (
    <motion.div
      whileHover={{
        y: -8,
        boxShadow: '0 24px 48px rgba(0,0,0,0.2)',
      }}
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      <motion.span
        whileHover={{ rotate: 45, scale: 1.1 }}
        transition={{ duration: 0.2 }}
      >
        🎯
      </motion.span>
    </motion.div>
  );
}
```

### Easing Functions

**Recommended Easing Values**:
- **ease-out**: 0.16, 0.04, 0.04, 1 (default snappy)
- **ease-in-out**: 0.42, 0, 0.58, 1 (smooth, balanced)
- **elastic**: cubic-bezier(0.34, 1.56, 0.64, 1) (playful overshoot)
- **sharp**: cubic-bezier(0.4, 0, 0.6, 1) (quick and direct)

### Motion Checklist

- [ ] Are animations orchestrated (staggered) or simultaneous?
- [ ] Do animations have easing functions or are they linear?
- [ ] Is there at least one delightful hover surprise?
- [ ] Do scroll triggers reveal content naturally?
- [ ] Are animation durations 0.4-0.8s (snappy) not 1.5s+ (sluggish)?
- [ ] Is animation supporting the design or competing with it?

## Anti-Patterns: What to Avoid

### Typography Anti-Patterns

**Generic Font Choices** - Avoid Inter, Roboto, Open Sans, Lato, system fonts. Result: Immediately reads as "default AI design," no personality.

**Incremental Size Jumps** - Avoid H1: 48px, H2: 40px, H3: 32px. Better: Display: 88px, Headline: 48px, Sub: 28px, Body: 16px.

**Mid-Range Font Weights Only** - Avoid using only weights 400, 500, 600. Better: Display: 300 or 700, Body: 400, Emphasis: 800/900.

### Color & Theme Anti-Patterns

**Cliché Color Schemes** - Avoid Material Design Trinity (Blue, Red, Green), default SaaS blues, rainbow palettes, pure grays.

**Monochrome Everything** - Avoid: Background: #f5f5f5, Text: #333333, Accent: #0099ff. Result: Feels corporate and soulless.

**Oversaturated Accent Colors** - Avoid neon colors at 100% saturation that don't exist in real life.

### Layout & Spatial Anti-Patterns

**Cookie-Cutter Centered Layout** - Avoid: Everything centered, symmetrical, predictable grid alignment. Reads as: "Default SaaS dashboard"

**Uniform Padding Everywhere** - Avoid: Same padding on all elements, no variation in spacing, everything feels equally distant.

### Motion & Animation Anti-Patterns

**Linear Timing on Everything** - Avoid: `transition: all 0.3s linear;` - Feels robotic.

**No Animation at All** - Avoid: Instant page loads, no hover feedback, transitions that snap instantly.

**Animation-Heavy Design** - Avoid: Animating every element, multiple simultaneous animations, animation that distracts from content.

**Slow, Sluggish Motion** - Avoid: `transition: all 2s linear;` - Feels like the app is struggling to load.

## Design Thinking: Pre-Coding Workflow

### The Pre-Design Checklist

Don't design until you answer these four questions:

1. **Purpose**: What problem are we solving? Who are we solving it for?
2. **Tone**: What emotional response do we want? What aesthetic direction reflects this?
3. **Constraints**: What are the real technical, temporal, or business limits?
4. **Differentiation**: What one unforgettable element makes this distinctly ours?

### 1. Purpose: Problem & Users

**Questions to Answer**:
- What specific problem does this design solve?
- Who are the primary users? (age, technical skill, context)
- What emotions are they bringing to this interface? (frustrated, excited, skeptical)
- What's the desired outcome after interaction?
- What makes this problem unique vs. competitors?

### 2. Tone: Aesthetic Direction

Based on your purpose, what emotional response should the design evoke?

**Emotional Directions**:
- **Trustworthy**: Professional, calm, reliable (finance, healthcare)
- **Energetic**: Playful, bold, surprising (creator tools, social)
- **Sophisticated**: Elegant, refined, literary (luxury, editorial)
- **Direct**: Minimal, fast, no-nonsense (productivity tools)
- **Warm**: Inviting, personable, human (community, education)
- **Bold**: Confident, unconventional, statement-making (startups, innovation)

### 3. Constraints: Reality Check

Before designing, know your boundaries:

**Categories**:
- **Technical**: Browser support, performance budget, framework limitations
- **Temporal**: How long do you have to build?
- **Business**: Brand guidelines, compliance requirements, market positioning
- **Creative**: Audience expectations, competitive landscape

### 4. Differentiation: The Unforgettable Element

Every intentional design has one element that makes it memorable and distinctly yours.

**Types of Differentiation**:

1. **Typography Signature** - A distinctive typeface pairing, unusual size/weight hierarchy
2. **Color Signature** - An unexpected color choice in an expected place
3. **Motion Signature** - A particular animation pattern no one else uses
4. **Layout/Composition Signature** - An unusual spatial arrangement
5. **Micro-interaction Signature** - A delight that appears on interaction
6. **Visual Detail Signature** - Illustration style, pattern, or specific visual treatment

### Anti-Pattern: Designing Without Foundation

**What NOT to do**:
```
"Let's make an app. Use modern design. Blue accent color.
Put a card here, buttons there. Done."
```

**What TO do instead**:
```
"This app is for busy professionals who are skeptical of new tools.
We want them to feel calm confidence. We'll differentiate with
warm serif typography and burnt orange accents. Motion will be
snappy and encouraging. The unforgettable element is the delight
of task completion with orchestrated motion."
```

### Checklist: Are You Ready to Design?

- [ ] Can you articulate the specific problem you're solving in one sentence?
- [ ] Can you describe the primary user in detail?
- [ ] Have you defined the emotional intent (not just "modern")?
- [ ] Can you name the tone adjectives that describe your design?
- [ ] Do you know your technical constraints?
- [ ] Do you know your timeline?
- [ ] Can you describe one unforgettable element that's distinctly yours?
- [ ] Would you describe your design direction as "intentional" or "defaulted"?

## Workflow Steps: 8-Phase Design Process for React

### Phase 1: Design Thinking
Complete the pre-design checklist. Answer: Purpose, Tone, Constraints, Differentiation. No code yet.

### Phase 2: Typography Dimension
- Select 2-3 typefaces using high-contrast pairing principles
- Define font weights (use extremes: 300/700/900, not 400/500/600)
- Create size scale with 3x+ jumps (not incremental scaling)
- Set up CSS-in-JS typography tokens with line heights and letter spacing

### Phase 3: Color & Theme Dimension
- Define emotional intent (warm, cool, energetic, calm)
- Create color system with CSS variables or styled-components
- Establish primary color, secondaries, and one unexpected accent
- Plan dark mode if needed (not just inverted)

### Phase 4: Motion Dimension
- Identify animation opportunities (page load, scroll, hover, transitions)
- Plan Framer Motion sequences with staggered timing
- Define easing curves for different interaction types
- Create reusable animation variants

### Phase 5: Spatial Composition Dimension
- Design layout with asymmetrical composition (avoid centered grids)
- Define spacing scale (8px, 12px, 16px, 24px, 32px, 48px, 64px)
- Create component structure that respects spacing
- Use Flexbox/Grid intentionally for layout hierarchy

### Phase 6: Backgrounds & Visual Details Dimension
- Design subtle backgrounds (soft colors, minimal gradients)
- Add texture or pattern (2-5% opacity, not busy)
- Create micro-details that reward observation
- Implement via CSS or SVG patterns

### Phase 7: Implementation (React Components)
- Create TypeScript interfaces for props
- Use functional components with hooks
- Implement Framer Motion animations
- Apply CSS-in-JS styling with tokens
- Add React.memo for performance optimization
- Ensure accessibility (ARIA, semantic HTML)

### Phase 8: Validation
- **Design Review**: Does it match the intentional direction?
- **Accessibility Review**: WCAG 2.1 AA compliance, semantic markup
- **Performance Review**: Component render performance, animation smoothness
- **Mobile Review**: Responsive design, touch interactions

## React-Specific Best Practices

### TypeScript Component Structure

```typescript
interface CardProps {
  title: string;
  description: string;
  onInteract?: () => void;
  variant?: 'primary' | 'secondary';
}

export const Card: React.FC<CardProps> = React.memo(({
  title,
  description,
  onInteract,
  variant = 'primary'
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -4 }}
      className={`card card--${variant}`}
    >
      <h3>{title}</h3>
      <p>{description}</p>
    </motion.div>
  );
});

Card.displayName = 'Card';
```

### Accessibility in React

```typescript
export const InteractiveButton: React.FC<{
  label: string;
  onClick: () => void;
  disabled?: boolean;
  ariaLabel?: string;
}> = ({ label, onClick, disabled, ariaLabel }) => {
  return (
    <motion.button
      onClick={onClick}
      disabled={disabled}
      aria-label={ariaLabel || label}
      role="button"
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      {label}
    </motion.button>
  );
};
```

### Performance Optimization

```typescript
// Use React.memo to prevent unnecessary re-renders
export const OptimizedComponent = React.memo(({ data }: Props) => {
  return <div>{data}</div>;
});

// Use useCallback for stable function references
const handleClick = useCallback(() => {
  // Handle click
}, []);

// Use useMemo for expensive computations
const processedData = useMemo(() => {
  return expensiveOperation(data);
}, [data]);
```

### Mobile-First Responsive Design

```typescript
import styled from 'styled-components';

export const ResponsiveContainer = styled.div`
  /* Mobile-first */
  padding: 16px;
  font-size: 14px;

  /* Tablet */
  @media (min-width: 768px) {
    padding: 24px;
    font-size: 16px;
  }

  /* Desktop */
  @media (min-width: 1024px) {
    padding: 32px;
    font-size: 18px;
  }
`;
```

## Anti-Generic-AI Checklist (React Edition)

- [ ] YES to TypeScript for type safety and documentation
- [ ] YES to Framer Motion for orchestrated, non-linear animations
- [ ] YES to proper React patterns (hooks, composition, memo)
- [ ] YES to distinctive typography (rejected defaults, intentional pairing)
- [ ] YES to custom color system (not Material Design or Tailwind defaults)
- [ ] YES to asymmetrical layouts (not centered, grid-perfect boring)
- [ ] YES to accessibility (semantic HTML, ARIA, keyboard support)
- [ ] YES to motion that serves purpose (not animation for animation's sake)
- [ ] NO to Inter, Roboto, Open Sans as primary fonts
- [ ] NO to Material Design colors (blue/red/green trinity)
- [ ] NO to linear timing functions
- [ ] NO to centered, symmetrical, "default SaaS" layouts
- [ ] NO to instant interactions (add easing and duration)

## References

- **Anthropic research** on non-generic AI design
- **Typography theory**: "Thinking with Type" by Ellen Lupton
- **Color theory**: Emotional context and psychological associations
- **Motion design**: Orchestration and choreography principles
- **React patterns**: "Advanced React" and hooks documentation
- **Framer Motion**: https://www.framer.com/motion/
- **Easing functions**: https://easings.net/
- **Google Fonts**: https://fonts.google.com
