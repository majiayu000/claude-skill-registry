---
name: frontend-aesthetics
description: Guide frontend design decisions to create distinctive, creative UIs that avoid generic AI-generated aesthetics. Use when building UI components, designing layouts, selecting colors/fonts, or implementing animations.
---

# Frontend Aesthetics

Create distinctive, creative frontend designs that avoid generic AI-generated aesthetics and cookie-cutter patterns.

## When to Use

- Designing new UI components or layouts
- Selecting typography and font pairings
- Choosing color schemes and themes
- Implementing animations and micro-interactions
- Reviewing frontend designs for generic patterns
- Making design decisions for landing pages, dashboards, or web applications
- Providing design guidance to frontend-focused agents

## Instructions

### Step 1: Assess Design Context

Understand the project's brand identity, purpose, and target aesthetic before making design decisions.

**Key Questions**:

- What is the project's brand personality? (playful, professional, technical, editorial, etc.)
- Who is the target audience?
- What emotional response should the design evoke?
- What makes this project unique?

### Step 2: Typography Selection

Choose beautiful, unique, and interesting fonts that match the project's character.

**AVOID These Generic Fonts**:

- Inter (massively overused in AI-generated UIs)
- Roboto
- Arial
- System fonts (-apple-system, BlinkMacSystemFont)

**Recommended Font Categories**:

**Code/Technical Aesthetics**:

- JetBrains Mono
- Fira Code
- Cascadia Code
- Victor Mono

**Editorial/Sophisticated**:

- Playfair Display
- Crimson Pro
- Spectral
- Lora

**Modern/Clean**:

- Space Grotesk (use sparingly - increasingly common)
- DM Sans
- Outfit
- Plus Jakarta Sans

**Critical**: Vary font choices across different projects. Don't converge on the same selections (like Space Grotesk) across all generations.

### Step 3: Color & Theme Design

Create cohesive color systems using CSS variables with dominant colors and sharp accents.

**Principles**:

- Dominant colors with sharp accents > timid, evenly-distributed palettes
- Commit to a cohesive aesthetic using CSS variables
- Draw inspiration from IDE themes (Dracula, Nord, Tokyo Night, Monokai, etc.)
- Consider cultural aesthetics relevant to project context

**AVOID**:

- Purple gradients on white backgrounds (clichéd AI aesthetic)
- Generic blue/gray combinations
- Predictable rainbow palettes with equal weight
- Safe, corporate color schemes when inappropriate for context

**Approach**:

- Choose 1-2 dominant colors that define the brand
- Add 1-2 sharp accent colors for calls-to-action and highlights
- Use CSS custom properties for theming
- Consider both light and dark mode variations

### Step 4: Motion & Animation

Use animations strategically for high-impact moments and delightful micro-interactions.

**Animation Priorities**:

1. **High-impact moments**: Orchestrated page loads with staggered reveals
2. **Micro-interactions**: Button hovers, transitions, state changes
3. **Contextual effects**: Scroll-triggered animations, parallax

**Implementation Guidelines**:

- **For HTML/Vanilla JS**: Prioritize CSS-only solutions (transitions, animations, @keyframes)
- **For React**: Use Motion library (Framer Motion) when available
- **Focus on orchestration**: One well-orchestrated sequence > scattered micro-interactions
- **Use animation-delay**: Create staggered reveals for related elements

**Example Pattern**:

```css
.stagger-item {
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
}
.stagger-item:nth-child(1) {
  animation-delay: 0.1s;
}
.stagger-item:nth-child(2) {
  animation-delay: 0.2s;
}
.stagger-item:nth-child(3) {
  animation-delay: 0.3s;
}
```

### Step 5: Background & Atmosphere

Create depth and atmosphere through layered backgrounds and contextual effects.

**AVOID**:

- Defaulting to solid colors
- Plain white or gray backgrounds
- Flat, lifeless surfaces

**Recommended Approaches**:

- Layer CSS gradients for depth
- Use geometric patterns (stripes, grids, dots)
- Add subtle noise textures
- Implement contextual effects (glow, blur, shadows)
- Match background complexity to overall aesthetic

**Example Patterns**:

```css
/* Layered gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Geometric pattern */
background-image: repeating-linear-gradient(
  45deg,
  transparent,
  transparent 10px,
  rgba(0, 0, 0, 0.05) 10px,
  rgba(0, 0, 0, 0.05) 20px
);

/* Subtle noise texture */
background-image: url('data:image/svg+xml,...'), linear-gradient(...);
```

### Step 6: Validate Against Anti-Patterns

Review the design against common AI-generated UI pitfalls.

**Anti-Pattern Checklist**:

- [ ] Not using Inter, Roboto, Arial, or system fonts
- [ ] No purple gradients on white backgrounds
- [ ] Color palette has clear hierarchy (dominant + accent, not even distribution)
- [ ] Animations are orchestrated and purposeful (not scattered)
- [ ] Backgrounds have depth and atmosphere (not solid colors)
- [ ] Layout is creative and context-appropriate (not cookie-cutter)
- [ ] Typography is distinctive and matches brand personality
- [ ] Design choices vary from previous projects (not repetitive)

### Step 7: Return Design Guidance

Provide specific, actionable design recommendations.

**Expected Output**:

```json
{
  "typography": {
    "primary": "Font name and reasoning",
    "secondary": "Font name and reasoning",
    "code": "Monospace font (if applicable)"
  },
  "colors": {
    "dominant": ["#hex1", "#hex2"],
    "accent": ["#hex3"],
    "theme_inspiration": "IDE theme or cultural aesthetic reference"
  },
  "animations": {
    "approach": "CSS-only or Framer Motion",
    "focus": "Page load orchestration or micro-interactions",
    "key_moments": ["List of high-impact animation opportunities"]
  },
  "backgrounds": {
    "technique": "Layered gradients, geometric patterns, etc.",
    "atmosphere": "Description of desired depth/mood"
  },
  "anti_pattern_validation": {
    "passed": true,
    "warnings": []
  }
}
```

## Error Handling

- **Missing Context**: Ask clarifying questions about brand identity and project purpose
- **Generic Choices Detected**: Explicitly warn and suggest distinctive alternatives
- **Repetitive Patterns**: Flag convergence on previously used aesthetics
- **Unclear Requirements**: Request specific design goals or constraints

## Examples

### Example 1: Technical Documentation Site

**Input**:

```json
{
  "project": "Developer documentation platform",
  "brand": "Technical, clean, code-focused",
  "audience": "Software engineers"
}
```

**Output**:

```json
{
  "typography": {
    "primary": "DM Sans - modern, readable, technical feel without being generic",
    "secondary": "Crimson Pro - for editorial content and longer reads",
    "code": "JetBrains Mono - excellent code aesthetics with ligatures"
  },
  "colors": {
    "dominant": ["#0f172a", "#1e293b"],
    "accent": ["#38bdf8", "#f97316"],
    "theme_inspiration": "Tokyo Night - dark blues with bright cyan and orange accents"
  },
  "animations": {
    "approach": "CSS-only for performance",
    "focus": "Staggered page load for documentation sections",
    "key_moments": ["Code block reveal", "Navigation transitions", "Search result appearance"]
  },
  "backgrounds": {
    "technique": "Dark gradient with subtle grid pattern overlay",
    "atmosphere": "Technical depth with code editor vibe"
  },
  "anti_pattern_validation": {
    "passed": true,
    "warnings": []
  }
}
```

### Example 2: Creative Agency Landing Page

**Input**:

```json
{
  "project": "Design agency portfolio",
  "brand": "Bold, creative, experimental",
  "audience": "Potential clients seeking innovative design"
}
```

**Output**:

```json
{
  "typography": {
    "primary": "Playfair Display - elegant, sophisticated, makes a statement",
    "secondary": "Outfit - modern contrast for body text",
    "code": "Not applicable"
  },
  "colors": {
    "dominant": ["#000000", "#fffef7"],
    "accent": ["#ff6b35", "#00d9ff"],
    "theme_inspiration": "High-contrast editorial with vibrant accent pops"
  },
  "animations": {
    "approach": "Framer Motion for complex orchestration",
    "focus": "Full-page orchestrated entry sequence",
    "key_moments": [
      "Hero text reveal with stagger",
      "Project thumbnails parallax",
      "Section transitions"
    ]
  },
  "backgrounds": {
    "technique": "Animated gradient mesh with organic shapes",
    "atmosphere": "Dynamic, bold, artistic depth"
  },
  "anti_pattern_validation": {
    "passed": true,
    "warnings": []
  }
}
```

### Example 3: Anti-Pattern Detection

**Input**:

```json
{
  "project": "SaaS dashboard",
  "proposed_design": {
    "font": "Inter",
    "colors": ["#6366f1", "#8b5cf6", "#ffffff"],
    "background": "solid white",
    "animations": "minimal button hovers"
  }
}
```

**Output**:

```json
{
  "typography": {
    "primary": "REJECTED: Inter is overused. Recommend: Plus Jakarta Sans - similar readability, more distinctive",
    "secondary": "Consider Spectral for data-heavy sections to add visual interest"
  },
  "colors": {
    "dominant": ["#0c4a6e", "#082f49"],
    "accent": ["#06b6d4", "#fbbf24"],
    "theme_inspiration": "REJECTED: Purple gradient is clichéd. Recommend: Deep ocean blues with cyan/amber accents (Dracula-inspired)"
  },
  "animations": {
    "approach": "Framer Motion",
    "focus": "UPGRADE: Add orchestrated dashboard load sequence",
    "key_moments": ["Staggered card reveals", "Chart animations", "Data transitions"]
  },
  "backgrounds": {
    "technique": "REJECTED: Solid white is flat. Recommend: Subtle gradient with noise texture",
    "atmosphere": "Add depth with layered backgrounds and geometric patterns"
  },
  "anti_pattern_validation": {
    "passed": false,
    "warnings": [
      "Using Inter font (generic AI aesthetic)",
      "Purple gradient color scheme (overused)",
      "Solid white background (no atmosphere)",
      "Minimal animations (missed opportunities for delight)"
    ]
  }
}
```

### Example 4: E-commerce Product Page

**Input**:

```json
{
  "project": "Premium fashion e-commerce",
  "brand": "Luxury, minimalist, editorial",
  "audience": "High-end fashion consumers"
}
```

**Output**:

```json
{
  "typography": {
    "primary": "Lora - sophisticated serif for luxury feel",
    "secondary": "DM Sans - clean sans-serif for product details and UI",
    "code": "Not applicable"
  },
  "colors": {
    "dominant": ["#1a1a1a", "#f5f5f0"],
    "accent": ["#c4a57b"],
    "theme_inspiration": "Luxury editorial - black, cream, gold accent"
  },
  "animations": {
    "approach": "CSS-only for lightweight performance",
    "focus": "Smooth product image transitions and subtle reveals",
    "key_moments": [
      "Product image crossfade",
      "Size selector micro-interaction",
      "Add to cart confirmation"
    ]
  },
  "backgrounds": {
    "technique": "Soft gradient from cream to off-white with subtle texture",
    "atmosphere": "Luxurious, tactile, premium feel"
  },
  "anti_pattern_validation": {
    "passed": true,
    "warnings": []
  }
}
```

## Validation

- [ ] Recommends distinctive fonts that match project character
- [ ] Explicitly warns against generic fonts (Inter, Roboto, Arial, system)
- [ ] Creates color palettes with clear hierarchy (dominant + accent)
- [ ] Avoids clichéd color schemes (purple gradients)
- [ ] Suggests orchestrated animations for high-impact moments
- [ ] Recommends backgrounds with depth and atmosphere
- [ ] Validates against anti-patterns
- [ ] Varies aesthetic recommendations across different contexts
- [ ] Provides context-specific reasoning for each choice

## Integration with Agents

### Frontend-Focused Agents

Before implementing UI components, invoke frontend-aesthetics Skill to receive design guidance:

```markdown
## Step 1: Design Guidance

Use frontend-aesthetics Skill to get typography, color, animation, and background recommendations.

Input: Project context, brand identity, target aesthetic
Output: Comprehensive design guidance with specific recommendations

Validate output against anti-patterns before proceeding.
```

### Code Review Agents

Use frontend-aesthetics Skill to evaluate existing frontend code for generic patterns:

```markdown
## Step 3: Frontend Aesthetics Review

Use frontend-aesthetics Skill in validation mode:

- Extract current font choices from CSS
- Identify color palette from CSS variables
- Review animation implementation
- Check background complexity

Flag any anti-patterns detected.
```

### Orchestrator Integration

Include frontend-aesthetics validation in quality gates:

```markdown
## Phase 2: Design Review

Use frontend-aesthetics Skill to validate design choices:

1. Check typography selection
2. Validate color scheme
3. Review animation approach
4. Assess background depth

If anti_pattern_validation.passed == false:
Delegate design improvements to frontend worker
```

## Notes

- **Token Budget**: This skill is intentionally focused (~500 tokens) for use as a design reference without overwhelming agent context
- **Variation is Critical**: Agents should avoid converging on the same design choices (like Space Grotesk) across all projects
- **Context Matters**: Design recommendations should always match the project's brand identity and purpose
- **Creativity Over Templates**: Encourage unexpected, distinctive choices rather than safe, predictable patterns
- **Performance Considerations**: CSS-only animations are preferred for HTML; Framer Motion is appropriate for React when available
- **Font Licensing**: Ensure recommended fonts are available via Google Fonts or other accessible sources
- **Accessibility**: Distinctive aesthetics should not compromise readability or WCAG compliance
- **Iteration**: Design choices can be refined based on user feedback and testing

## References

Based on official Anthropic guidance: "Improving Claude's front-end aesthetic sense" (2025-01-15)
