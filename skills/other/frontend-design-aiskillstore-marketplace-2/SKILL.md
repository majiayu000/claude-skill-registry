---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with exceptional design quality. Use when building web components, pages, or applications that need creative, polished aesthetics.
version: 1.0.0
author: AI-Vibe-Prompts
tags: [design, frontend, ui, aesthetics, creative]
auto_invoke: false
---

# Frontend Design Skill

## Objective

Guide creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices that create memorable user experiences.

## When to Use This Skill

Invoke when:
- Building new web components, pages, or applications
- User requests distinctive or creative design
- Creating landing pages or marketing sites
- Developing design-forward applications
- Need to avoid generic/template aesthetics
- Building portfolio or showcase projects

## Design Philosophy

### Core Principle: Bold Intentionality

Create interfaces that are **unforgettable** through intentional design choices. Both bold maximalism and refined minimalism work - the key is having a clear aesthetic direction and executing it with precision.

**Anti-patterns to avoid**:
- Generic AI aesthetics (overused fonts like Inter, Roboto, Arial)
- Cliched color schemes (especially purple gradients on white)
- Predictable layouts and cookie-cutter component patterns
- Design that lacks context-specific character
- Converging on common design choices (e.g., Space Grotesk repeatedly)

## Design Thinking Process

Before writing any code, establish:

### 1. Context Understanding
- **Purpose**: What problem does this interface solve?
- **Audience**: Who uses it? What are their expectations?
- **Constraints**: Technical requirements (framework, performance, accessibility)

### 2. Aesthetic Direction Selection

Pick a BOLD direction and commit to it:

**Aesthetic Options** (use for inspiration, create unique variations):
- **Brutally Minimal**: Extreme whitespace, monochrome, typography-focused
- **Maximalist Chaos**: Dense information, vibrant colors, layered complexity
- **Retro-Futuristic**: Y2K aesthetics, chrome effects, bold gradients
- **Organic/Natural**: Earthy tones, fluid shapes, soft shadows
- **Luxury/Refined**: Premium materials, subtle elegance, restrained palette
- **Playful/Toy-like**: Rounded shapes, bright colors, whimsical interactions
- **Editorial/Magazine**: Bold typography, grid layouts, dynamic composition
- **Brutalist/Raw**: Concrete textures, exposed structure, functional clarity
- **Art Deco/Geometric**: Sharp angles, symmetry, metallic accents
- **Soft/Pastel**: Gentle colors, smooth gradients, dreamy atmosphere
- **Industrial/Utilitarian**: Mechanical, functional, no-nonsense
- **Glassmorphism**: Frosted glass, transparency, layered depth
- **Neomorphism**: Soft shadows, embossed elements, tactile feel

### 3. Differentiation Focus

Ask: **What makes this UNFORGETTABLE?**
- What's the one thing someone will remember?
- What unexpected choice creates delight?
- How does this stand apart from competitors?

## Frontend Aesthetics Guidelines

### Typography: The Foundation

**Critical**: Choose fonts that are beautiful, unique, and interesting.

**Avoid**: Generic fonts (Arial, Inter, Roboto, system fonts)

**Seek**: Distinctive choices that elevate aesthetics
- Display fonts: Unique, characterful, attention-grabbing
- Body fonts: Refined, readable, complementary

**Strategy**:
- Pair a distinctive display font with a refined body font
- Use font weight and size variation for hierarchy
- Consider variable fonts for fluid scaling
- Add font features (ligatures, stylistic alternates)

**Examples**:
```css
/* Bold Display + Refined Body */
font-family: 'Syne', sans-serif; /* Display */
font-family: 'IBM Plex Sans', sans-serif; /* Body */

/* Editorial Style */
font-family: 'Playfair Display', serif; /* Display */
font-family: 'Work Sans', sans-serif; /* Body */

/* Modern Geometric */
font-family: 'Clash Display', sans-serif; /* Display */
font-family: 'Satoshi', sans-serif; /* Body */
```

### Color & Theme: Cohesive Aesthetics

**Strategy**: Commit to a cohesive aesthetic direction

**Best practices**:
- Use CSS variables for consistency
- Dominant colors with sharp accents outperform evenly-distributed palettes
- Create atmospheric backgrounds instead of solid colors
- Consider dark mode as primary design, not afterthought

**Implementation**:
```css
:root {
  /* Primary palette - be bold */
  --color-primary: #FF6B35;
  --color-accent: #004E89;
  --color-neutral: #F7F7F2;

  /* Atmospheric background */
  --bg-gradient: linear-gradient(135deg,
    var(--color-primary) 0%,
    var(--color-accent) 100%);

  /* Depth and layering */
  --surface-glass: rgba(255, 255, 255, 0.1);
  --surface-overlay: rgba(0, 0, 0, 0.05);
}
```

### Motion: Choreographed Delight

**Philosophy**: Prioritize high-impact moments over scattered micro-interactions

**Strategies**:
- One well-orchestrated page load with staggered reveals
- Use `animation-delay` for choreography
- Scroll-triggered animations that surprise
- Hover states that delight

**CSS-first approach** (for HTML):
```css
/* Staggered page load */
.hero-title {
  animation: slideUp 0.6s ease-out;
}

.hero-subtitle {
  animation: slideUp 0.6s ease-out 0.1s backwards;
}

.hero-cta {
  animation: slideUp 0.6s ease-out 0.2s backwards;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**React with Motion library**:
```jsx
import { motion } from 'framer-motion';

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

<motion.div variants={container} initial="hidden" animate="show">
  <motion.h1 variants={item}>Title</motion.h1>
  <motion.p variants={item}>Subtitle</motion.p>
  <motion.button variants={item}>CTA</motion.button>
</motion.div>
```

### Spatial Composition: Break the Grid

**Principles**:
- Embrace asymmetry and unexpected layouts
- Use overlap and layering for depth
- Diagonal flow creates energy
- Balance generous negative space OR controlled density

**Techniques**:
- Grid-breaking elements (overlap grid boundaries)
- Diagonal sections and angled divisions
- Floating elements with custom positioning
- Z-index layering for depth

### Backgrounds & Visual Details: Atmosphere

**Goal**: Create atmosphere and depth, not just solid colors

**Creative approaches**:
- **Gradient Meshes**: Complex, multi-point gradients
- **Noise Textures**: Subtle grain for tactility
- **Geometric Patterns**: SVG patterns, subtle or bold
- **Layered Transparencies**: Glassmorphic effects
- **Dramatic Shadows**: Elevation and depth
- **Decorative Borders**: Custom shapes and styles
- **Custom Cursors**: Interactive feedback
- **Grain Overlays**: Film-like texture

**Example - Atmospheric background**:
```css
.hero {
  position: relative;
  background:
    radial-gradient(circle at 20% 50%, rgba(255, 107, 53, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 50%, rgba(0, 78, 137, 0.3) 0%, transparent 50%),
    linear-gradient(135deg, #1a1a2e 0%, #0f0f1e 100%);
}

/* Noise overlay */
.hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
  pointer-events: none;
}
```

## Implementation Complexity Matching

**IMPORTANT**: Match code complexity to aesthetic vision

### Maximalist Designs
Need elaborate code with:
- Extensive animations and effects
- Complex layering and composition
- Rich interactive elements
- Multiple visual details and textures

### Minimalist/Refined Designs
Need restraint with:
- Careful attention to spacing
- Precise typography
- Subtle details (shadows, borders, transitions)
- Clean, purposeful code

**Remember**: Elegance comes from executing the vision well, not from complexity level.

## Production-Grade Requirements

All implementations must be:
- **Functional**: Working code, not mockups
- **Accessible**: WCAG AA compliant (minimum)
- **Performant**: Optimized assets, lazy loading
- **Responsive**: Mobile-first approach
- **Cohesive**: Clear aesthetic point-of-view
- **Polished**: Meticulously refined in every detail

## Variation Strategy

**CRITICAL**: No two designs should be the same

For each project, vary:
- Light vs dark theme
- Font choices (never repeat common choices)
- Aesthetic direction
- Color schemes
- Layout approaches
- Animation styles

**Remember**: Claude is capable of extraordinary creative work. Don't hold back - show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

## Example Frameworks & Tools

### React Component Example
```jsx
import { motion } from 'framer-motion';

export function DistinctiveHero() {
  return (
    <section className="relative min-h-screen overflow-hidden bg-gradient-to-br from-amber-50 via-rose-50 to-violet-50">
      {/* Atmospheric background effect */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-amber-400 rounded-full mix-blend-multiply filter blur-3xl animate-blob" />
        <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-rose-400 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-2000" />
        <div className="absolute bottom-1/4 left-1/2 w-96 h-96 bg-violet-400 rounded-full mix-blend-multiply filter blur-3xl animate-blob animation-delay-4000" />
      </div>

      {/* Content with staggered animation */}
      <motion.div
        className="relative z-10 container mx-auto px-6 py-24"
        initial="hidden"
        animate="visible"
        variants={{
          hidden: { opacity: 0 },
          visible: {
            opacity: 1,
            transition: { staggerChildren: 0.15 }
          }
        }}
      >
        <motion.h1
          className="font-display text-7xl md:text-9xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 via-rose-600 to-violet-600"
          variants={{
            hidden: { opacity: 0, y: 50 },
            visible: { opacity: 1, y: 0 }
          }}
        >
          Distinctive
        </motion.h1>

        <motion.p
          className="font-body text-xl md:text-2xl text-gray-700 max-w-2xl mt-6"
          variants={{
            hidden: { opacity: 0, y: 50 },
            visible: { opacity: 1, y: 0 }
          }}
        >
          Breaking free from generic design patterns
        </motion.p>

        <motion.button
          className="mt-12 px-8 py-4 bg-gradient-to-r from-amber-600 to-rose-600 text-white font-semibold rounded-full shadow-2xl hover:shadow-amber-500/50 transition-all duration-300 hover:scale-105"
          variants={{
            hidden: { opacity: 0, y: 50 },
            visible: { opacity: 1, y: 0 }
          }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Explore Further
        </motion.button>
      </motion.div>
    </section>
  );
}
```

## Quality Checklist

Before delivering:
- [ ] Aesthetic direction is clear and intentional
- [ ] Typography choices are distinctive and purposeful
- [ ] Colors create atmosphere, not just fill space
- [ ] Animations enhance experience meaningfully
- [ ] Layout breaks expected patterns creatively
- [ ] Visual details add depth and interest
- [ ] Code is production-ready and functional
- [ ] Accessibility standards are met
- [ ] Performance is optimized
- [ ] Design would be memorable to users

## Integration with Other Skills

Works well with:
- `quality-gates` - Validate accessibility and performance
- `react-optimizer` - Optimize React component performance
- `nextjs-optimization` - Build performant Next.js applications
- `designer` agent - Comprehensive design system work

## Version History

- **1.0.0** (2025-01-25): Initial skill creation for distinctive frontend design
