---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use when building web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Adapted from Anthropic Skills (https://github.com/anthropics/skills/tree/main/frontend-design)
---

# Frontend Design

## Core Principle

When building frontend interfaces, create distinctive, production-grade designs with intentional aesthetic direction. Avoid generic "AI slop" aesthetics that lack character and context-specific design.

## When to Use This Skill

- Building web components
- Creating web pages
- Developing web applications
- Implementing UI/UX designs
- When user requests frontend development
- When aesthetic quality matters

## The Iron Laws

### 1. UNDERSTAND CONTEXT BEFORE CODING

**NEVER start coding without understanding:**
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: What aesthetic direction fits? (minimal, maximalist, retro, organic, luxury, playful, editorial, brutalist, art deco, industrial, etc.)
- **Constraints**: Technical requirements (framework, performance, accessibility)
- **Differentiation**: What makes this memorable and unique?

### 2. COMMIT TO A BOLD AESTHETIC DIRECTION

**Choose ONE clear conceptual direction and execute with precision:**

✅ **Valid approaches:**
- Brutally minimal with perfect spacing
- Maximalist chaos with controlled density
- Retro-futuristic with nostalgic elements
- Organic/natural with flowing forms
- Luxury/refined with elegant restraint
- Editorial/magazine with strong typography

❌ **Avoid:**
- Generic, context-free design
- Default choices without intention
- "Safe" but forgettable aesthetics
- Timid, half-committed execution

**Authority**: Bold maximalism AND refined minimalism both work - the key is intentionality, not intensity.

### 3. IMPLEMENT PRODUCTION-GRADE CODE

**Code must be:**
- Production-ready and functional
- Visually striking and memorable
- Cohesive with clear aesthetic point-of-view
- Meticulously refined in every detail

## Design Implementation Protocol

### Step 1: Check Brand Guidelines

**ALWAYS check first:**
```
I'm using the frontend-design skill to build [component/page/app].

Brand Guidelines Check:
- Location: .claude/BRAND-GUIDELINES.md
- Status: [EXISTS / NOT FOUND]
```

**If guidelines exist:**
```
Brand Guidelines Applied:
- Colors: [Primary: #XXX, Secondary: #XXX, Accent: #XXX]
- Typography: [Heading: Font A, Body: Font B]
- Visual Style: [Minimal/Maximal, Rounded/Angular, etc.]
- Personality: [Adjectives from brand guidelines]

I will design within these brand parameters.
```

**If no guidelines:**
```
No brand guidelines found. Proceeding with context-based design decisions.
```

### Step 2: Context Analysis

**Template:**
```
Context Analysis:
- Purpose: [What problem does it solve? Who uses it?]
- Tone: [Chosen aesthetic direction OR brand personality]
- Constraints: [Technical requirements]
- Differentiation: [What makes it memorable?]

Aesthetic Direction: [Describe the bold direction chosen]
```

### Step 2: Typography Excellence

**Choose fonts that are beautiful, unique, and interesting:**

✅ **DO:**
- Distinctive display fonts paired with refined body fonts
- Unexpected, characterful font choices
- Fonts that elevate the aesthetic
- Consider: Google Fonts with character, premium font services

❌ **NEVER:**
- Generic fonts: Arial, Inter, Roboto
- System fonts without intention
- Overused AI-generation fonts: Space Grotesk
- Default font stacks

**Example Combinations:**
- Display: Playfair Display / Body: Source Sans Pro
- Display: Abril Fatface / Body: Lato
- Display: Righteous / Body: Inter (when Inter fits aesthetic)
- Display: Bebas Neue / Body: Open Sans
- All: IBM Plex Mono (for code/technical aesthetic)

### Step 3: Color & Theme Strategy

**If brand guidelines exist: USE BRAND COLORS**

```css
/* Copy directly from .claude/BRAND-GUIDELINES.md */
:root {
  /* Brand colors from guidelines */
  --color-brand-primary: #[from guidelines];
  --color-brand-secondary: #[from guidelines];
  --color-accent-1: #[from guidelines];
  /* ... complete palette from guidelines */
}
```

**If NO brand guidelines: Create cohesive aesthetic**

✅ **DO:**
- Use CSS variables for consistency
- Dominant colors with sharp accents
- Context-specific color stories
- Unexpected but harmonious palettes

❌ **NEVER:**
- Purple gradients on white (cliched)
- Timid, evenly-distributed palettes
- Generic corporate blue/gray
- Color choices without conceptual backing

**Implementation:**
```css
:root {
  /* Primary palette */
  --color-primary: #...;
  --color-secondary: #...;
  --color-accent: #...;

  /* Semantic colors */
  --color-background: #...;
  --color-surface: #...;
  --color-text: #...;
  --color-text-secondary: #...;

  /* State colors */
  --color-success: #...;
  --color-warning: #...;
  --color-error: #...;
}
```

### Step 4: Motion & Animation

**Use animations for high-impact moments:**

✅ **DO:**
- CSS-only solutions for HTML when possible
- Motion library for React (framer-motion, react-spring)
- Page load reveals with staggered timing
- Scroll-triggered animations
- Hover states that surprise and delight
- One well-orchestrated sequence > scattered micro-interactions

❌ **AVOID:**
- Excessive animations everywhere
- Animations without purpose
- Janky, poorly-timed transitions

**Example: Staggered Page Load**
```css
.element {
  opacity: 0;
  animation: fadeInUp 0.6s ease-out forwards;
}

.element:nth-child(1) { animation-delay: 0.1s; }
.element:nth-child(2) { animation-delay: 0.2s; }
.element:nth-child(3) { animation-delay: 0.3s; }

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
```

### Step 5: Spatial Composition

**Create unexpected, memorable layouts:**

✅ **DO:**
- Asymmetry with intention
- Overlap and layering
- Diagonal flow
- Grid-breaking elements
- Generous negative space OR controlled density
- Unexpected proportions

❌ **AVOID:**
- Predictable centered layouts
- Generic card grids
- Cookie-cutter patterns
- Timid spacing

### Step 6: Backgrounds & Visual Details

**Create atmosphere and depth:**

✅ **DO:**
- Gradient meshes
- Noise textures
- Geometric patterns
- Layered transparencies
- Dramatic shadows
- Decorative borders
- Custom cursors
- Grain overlays
- Context-appropriate effects

❌ **AVOID:**
- Flat solid colors without intention
- Generic white/gray backgrounds
- No visual interest or texture

**Example: Textured Background**
```css
.background {
  background:
    linear-gradient(135deg, #667eea 0%, #764ba2 100%),
    url('data:image/svg+xml;base64,...') /* noise texture */;
  background-blend-mode: multiply;
}
```

## Complexity Matching

**Match implementation complexity to aesthetic vision:**

### Maximalist Design → Elaborate Code
- Extensive animations and effects
- Complex layering and compositing
- Rich interactions and micro-animations
- Detailed textures and patterns
- Dynamic, responsive elements

### Minimalist Design → Restraint & Precision
- Perfect spacing and alignment
- Careful typography choices
- Subtle, purposeful animations
- Precise color usage
- Attention to micro-details

**Authority**: Elegance comes from executing the vision well, not from choosing "simple" or "complex."

## Anti-Patterns to Avoid

### Generic AI Aesthetics

❌ **NEVER use:**
- Overused fonts: Inter, Roboto, Arial, system fonts
- Cliched colors: purple gradients on white
- Predictable layouts: centered hero with card grid
- Cookie-cutter patterns that lack character
- Generic component libraries without customization

### Common Mistakes

❌ **Mistakes:**
- Starting to code without context understanding
- Choosing "safe" over distinctive
- Using the same fonts/colors across different projects
- Forgetting accessibility
- Implementing without testing responsiveness
- No consideration for performance

✅ **Solutions:**
- Complete context analysis first
- Commit boldly to aesthetic direction
- Vary designs based on context
- Include ARIA labels and semantic HTML
- Test on multiple screen sizes
- Optimize images and animations

## Framework-Specific Guidelines

### React
```jsx
// Use framer-motion for animations
import { motion } from 'framer-motion';

const Component = () => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6 }}
  >
    Content
  </motion.div>
);
```

### Vue
```vue
<template>
  <transition name="fade">
    <div class="component">Content</div>
  </transition>
</template>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.6s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
```

### HTML/CSS/JS
```html
<!-- Use semantic HTML -->
<article class="card" role="article">
  <header class="card__header">
    <h2 class="card__title">Title</h2>
  </header>
  <div class="card__content">
    <p class="card__description">Description</p>
  </div>
</article>
```

## Production Checklist

Before declaring frontend work complete:

- [ ] **Brand guidelines checked** (.claude/BRAND-GUIDELINES.md)
- [ ] **Brand colors applied** (if guidelines exist)
- [ ] **Brand typography applied** (if guidelines exist)
- [ ] **Brand visual style followed** (if guidelines exist)
- [ ] Context analysis completed and documented
- [ ] Bold aesthetic direction chosen and executed
- [ ] Typography is distinctive and appropriate
- [ ] Color system uses CSS variables
- [ ] Animations are purposeful and performant
- [ ] Layout is unexpected and memorable
- [ ] Visual details add atmosphere
- [ ] Responsive across all screen sizes
- [ ] Accessibility: ARIA labels, semantic HTML, keyboard navigation
- [ ] Performance: optimized images, efficient CSS/JS
- [ ] Cross-browser testing completed
- [ ] Code is clean and maintainable

## Remember

**Claude is capable of extraordinary creative work.**

Don't hold back. Show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

**Vary your designs**: No two interfaces should look the same. Each should be uniquely designed for its specific context, purpose, and audience.

**Quality over speed**: Production-grade design takes time. Don't rush the aesthetic decisions.

**Intentionality is everything**: Whether minimal or maximal, the key is executing with clear purpose and precision.

---

## Integration with Brand Guidelines

**This skill automatically integrates with the brand-guidelines skill:**

1. Checks for `.claude/BRAND-GUIDELINES.md` at start
2. If found: Applies brand colors, typography, and visual style
3. If not found: Suggests creating brand guidelines first
4. Creative interpretation allowed within brand parameters
5. Never override brand without explicit user request

**Recommended workflow:**
```
1. Use brand-guidelines skill first (establish/document brand)
2. Then use frontend-design skill (applies brand automatically)
3. Result: Consistent, on-brand, distinctive designs
```

---

**Attribution**: This skill is adapted from [Anthropic Skills](https://github.com/anthropics/skills/tree/main/frontend-design)

**Integrates with**: brand-guidelines skill for automatic brand application
