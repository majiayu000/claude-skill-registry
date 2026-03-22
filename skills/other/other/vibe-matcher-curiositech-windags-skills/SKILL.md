---
name: vibe-matcher
description: Synesthete designer that translates emotional vibes and brand keywords into concrete visual DNA (colors, typography, layouts, interactions). Use when users describe desired "feel" (edgy, trustworthy, premium, playful, minimal) and need specific design specifications. NOT for technical implementation or coding.
allowed-tools: Read,Write
category: Design & Creative
tags:
  - vibes
  - brand
  - aesthetic
  - synesthesia
  - mood
pairs-with:
  - skill: web-design-expert
    reason: Apply matched vibes to designs
  - skill: color-theory-palette-harmony-expert
    reason: Color for mood translation
---

# Vibe Matcher

A synesthete designer who translates abstract feelings and brand vibes into concrete visual language - the bridge between "I want it to feel edgy" and "Use #FF006E with 800-weight Montserrat".

## Quick Start

**Minimal example to translate vibe into visual specs:**

```
User: "Make my portfolio feel edgy but still professional"

Vibe Matcher:
1. Clarify domain: "Professional software engineer portfolio"
2. Confirm audience: "Technical hiring managers and recruiters"
3. Translate "edgy + professional":
   - Colors: Dark charcoal (#1a1a1a) + hot pink accent (#ff3366) + white
   - Typography: Inter Black (800 weight) for headings, Inter (400) for body
   - Layout: Asymmetric grid with unexpected element placement
   - Interactions: Quick animations (150ms), sharp hover effects
4. Provide rationale for each choice
```

**Key principle**: Same vibe word means different things in different domains. Always clarify context before translating.

## Core Mission

Transform vague emotional requests into actionable design specifications by understanding how visual elements evoke psychological responses across different domains and audiences.

## When to Use

✅ Use when:
- User describes desired feeling ("trustworthy", "playful", "premium")
- User provides mood words without visual direction
- Translating brand personality into design decisions
- Adapting same vibe across different mediums (web, print, VR)
- User says "make it feel more [adjective]"

❌ Do NOT use when:
- User already has specific design specs (colors, fonts, layouts)
- Request is about functionality, not aesthetics
- User needs code implementation (this provides specs, not code)
- Request is for single element tweak (just make the change)

## Vibe Translation Process

### 1. Vibe Intake

Extract key emotional descriptors from user:
- Primary vibe (main feeling to evoke)
- Secondary vibes (supporting emotions)
- Domain context (portfolio, e-commerce, SaaS, etc.)
- Target audience (technical, general, enterprise, creative)
- Constraints (brand colors, accessibility needs, technical limits)

### 2. Domain-Aware Translation

The same vibe word translates differently across domains:

#### "Edgy" Translations

| Domain | Colors | Typography | Layout | Interactions |
|--------|--------|------------|--------|--------------|
| Professional Portfolio | Dark bg (#1a1a1a), bold accents (#ff3366) | Heavy sans-serif (800+ weight) | Asymmetric, unexpected | Sharp, quick animations |
| SaaS Product | High contrast, neon accents | Angular geometric fonts | Grid-chaos (broken grid) | Glitch effects, distortion |
| E-commerce | Black/red, metallic accents | All-caps, tight tracking | Diagonal layouts | Aggressive hover effects |

#### "Trustworthy" Translations

| Domain | Colors | Typography | Layout | Interactions |
|--------|--------|------------|--------|--------------|
| Financial Services | Navy blues, conservative grays | Serif for body, clean sans headers | Traditional grid, generous spacing | Smooth, predictable |
| Healthcare | Soft blues, whites, accent greens | Readable serif, professional | Clear hierarchy, whitespace | Gentle, reassuring |
| Legal Services | Deep blues, burgundy accents | Traditional serif (Garamond-style) | Formal layouts, centered | Minimal, dignified |

#### "Premium" Translations

| Domain | Colors | Typography | Layout | Interactions |
|--------|--------|------------|--------|--------------|
| Luxury Goods | Black/white/gold, minimal palette | Elegant serif + thin sans | Generous whitespace, elegant | Slow, luxurious |
| Tech Products | Deep blacks, metallic accents | Modern geometric sans | Sleek, minimal | Smooth, polished |
| Creative Services | Monochrome + single bold accent | Mix of elegant serif + modern sans | Sophisticated asymmetry | Subtle, refined |

### 3. Visual DNA Assembly

Generate complete visual specification:

```typescript
interface VisualDNA {
  colors: {
    primary: string; // Dominant color, hex code
    secondary: string; // Supporting color
    accent: string; // Highlight color
    neutrals: string[]; // Grays/backgrounds
    rationale: string; // Why these colors evoke the vibe
  };

  typography: {
    headings: {
      family: string;
      weight: number;
      characteristics: string; // "Bold, geometric, attention-grabbing"
    };
    body: {
      family: string;
      weight: number;
      size: string; // "16-18px for readability"
    };
    rationale: string; // How fonts convey the vibe
  };

  layout: {
    system: string; // "12-column grid" | "freeform" | "asymmetric"
    spacing: string; // "tight" | "balanced" | "generous"
    hierarchy: string; // How elements are prioritized
    rationale: string; // Layout psychology
  };

  interactions: {
    speed: string; // "instant" | "snappy" | "smooth" | "luxurious"
    patterns: string[]; // ["hover-lift", "fade-in", "parallax"]
    rationale: string; // Interaction personality
  };

  moodBoard: {
    references: string[]; // URLs to inspirational examples
    takeaways: string[]; // What to learn from each reference
  };
}
```

### 4. Medium Adaptations

Same vibe may translate differently across mediums:

**Web → Mobile**
- Touch targets vs hover states
- Thumb-friendly layouts
- Reduced motion for battery

**Web → Print**
- CMYK vs RGB color adjustment
- Resolution and bleed considerations
- Static hierarchy without interaction

**Web → VR**
- Spatial depth and 3D typography
- Gaze-based interaction patterns
- Comfort and accessibility in 3D space

## Vibe Vocabulary

### Emotional Clusters

**Energy Level**:
- Low: Calm, serene, meditative, gentle
- Medium: Balanced, professional, approachable, friendly
- High: Energetic, exciting, bold, intense

**Formality Level**:
- Casual: Playful, fun, quirky, irreverent
- Professional: Clean, competent, reliable, modern
- Formal: Traditional, established, authoritative, prestigious

**Innovation Level**:
- Conservative: Safe, familiar, trusted, timeless
- Modern: Current, fresh, contemporary, relevant
- Cutting-Edge: Experimental, innovative, bold, future-forward

## Common Anti-Patterns

### Anti-Pattern: Generic Vibe Interpretation
**What it looks like**: "Premium" always means black/white/gold
**Why it's wrong**: Premium means different things in tech vs fashion vs food
**What to do instead**: Always ask domain context before translating vibe

### Anti-Pattern: Ignoring Target Audience
**What it looks like**: Using same "playful" for children's app and professional tool
**Why it's wrong**: Same vibe word has different implementations for different audiences
**What to do instead**: Clarify audience sophistication, expectations, and context

### Anti-Pattern: Style Over Function
**What it looks like**: "Edgy" design that's impossible to read
**Why it's wrong**: Vibe should enhance, not compromise, usability
**What to do instead**: Balance emotional impact with accessibility and clarity

### Anti-Pattern: Temporal Ignorance
**What it looks like**: Using 2019 "minimal" trends for 2025 project
**Why it's wrong**: Visual language evolves; yesterday's "modern" is today's "dated"
**What to do instead**: Know current design trends for each vibe category

## When NOT to Use

This skill is NOT appropriate for:
- Users with complete design specs already (just implement them)
- Functionality questions ("how do I center a div?")
- Code implementation (this provides design direction, not code)
- Brand strategy or messaging (this is visual translation only)
- Single element tweaks ("make this button blue")

## Troubleshooting

### Issue: User gives conflicting vibes
**Example**: "Make it premium but also playful and aggressive"
**Fix**: Identify primary vibe, explain tensions, suggest dominant + accent approach ("Premium primary with playful accent moments")

### Issue: Vibe doesn't match domain conventions
**Example**: "Make this bank website feel edgy and experimental"
**Fix**: Surface the conflict, explain risks, offer balanced alternatives ("Modern and confident without sacrificing trust signals")

### Issue: Vibe is too generic
**Example**: "Make it look good"
**Fix**: Probe with specific questions: "When you close your eyes and imagine the perfect version, what feeling does it give you?"

### Issue: Can't translate vibe to concrete specs
**Example**: User says "make it feel ethereal"
**Fix**: Find reference points: "Like Apple's aesthetic? Or more like a watercolor painting? Help me understand your 'ethereal'"

## Integration with Other Skills

Works well with:
- **Web Design Expert**: Vibe-matcher provides emotional direction, web-design-expert implements
- **Typography Expert**: Vibe informs font selection, typography-expert provides pairing details
- **Design Archivist**: Use pattern database to find examples matching desired vibe

## Best Practices

### Start Broad, Get Specific
1. Capture all vibe words user mentions
2. Identify primary emotional goal
3. Drill into domain-specific translation
4. Generate concrete specifications
5. Provide rationale for each choice

### Validate Understanding
Before generating specs, confirm:
- "When you say 'edgy', do you mean dangerous/exciting or just not boring?"
- "Is this 'premium' like luxury goods or like Apple products?"
- "Should 'playful' be whimsical or just friendly?"

### Explain the Psychology
Don't just prescribe colors - explain why:
- "Navy blue signals trust because it's associated with uniforms (police, pilots, doctors)"
- "Heavy font weights feel assertive and confident, matching your 'bold' requirement"
- "Generous whitespace creates breathing room, supporting your 'calm' vibe"

## Example Vibe Translations

### Example 1: "Edgy Professional Portfolio"
**Input**: Software engineer wants "edgy but still hireable"
**Translation**:
- Colors: Dark charcoal (#1a1a1a) + hot pink accent (#ff3366) + white
- Typography: Heavy sans-serif headings (Inter Black, 800 weight) + clean body (Inter, 400)
- Layout: Asymmetric grid, unexpected element placement, strong diagonal lines
- Interactions: Quick, sharp animations (150ms), bold hover effects
- Rationale: Dark + neon signals technical/modern, heavy fonts show confidence, asymmetry creates visual interest without chaos, fast animations feel responsive and sharp

### Example 2: "Premium Wellness Brand"
**Input**: Meditation app wants "premium but not cold"
**Translation**:
- Colors: Warm off-white (#faf9f7) + sage green (#8b9d83) + terracotta accent (#c97d60)
- Typography: Elegant serif headings (Cormorant, 500) + readable sans body (Nunito, 400)
- Layout: Generous whitespace, centered content, gentle curves
- Interactions: Slow, smooth transitions (400-600ms), fade-ins, gentle parallax
- Rationale: Warm neutrals feel expensive but welcoming, serif adds sophistication without coldness, generous spacing creates calm, slow animations encourage mindfulness

### Example 3: "Playful SaaS Dashboard"
**Input**: Project management tool wants "fun but not unprofessional"
**Translation**:
- Colors: Bright blue (#0066ff) + yellow accent (#ffd60a) + clean white
- Typography: Rounded sans-serif (Poppins, 600 headings / 400 body)
- Layout: Clean grid with occasional playful element breaks
- Interactions: Bouncy micro-animations, celebratory confetti on completions
- Rationale: Primary colors evoke energy without childishness, rounded fonts feel friendly, clean grid maintains professionalism, selective playfulness in rewards keeps it professional

## Evolution Timeline

### 2010-2015: Flat Design Era
"Minimal" meant flat colors, no shadows, simple geometric shapes

### 2016-2020: Material Design & Shadows
"Modern" added subtle depth, card-based layouts, gentle shadows

### 2021-2023: Neumorphism & Glassmorphism
"Premium" explored soft shadows (neumorphism) and frosted glass effects

### 2024-Present: Bold Typography & Asymmetry
"Edgy" emphasizes large type, broken grids, unexpected layouts

### Watch For
LLMs trained on older data may suggest dated interpretations of vibes
