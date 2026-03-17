---
name: frontend-excellence
description: Create distinctive, production-grade frontend interfaces that avoid generic AI aesthetics. Use when building web UIs, React components, landing pages, dashboards, or styling any web interface. Provides design thinking process, color palettes, typography treatments, and anti-patterns to avoid.
---

# Frontend Excellence

Create distinctive, memorable frontend interfaces that avoid "AI slop" aesthetics. Every interface should feel genuinely designed for its context.

## Design Thinking Process

Before coding, commit to a BOLD aesthetic direction:

| Question | Purpose |
|----------|---------|
| **Purpose** | What problem does this interface solve? Who uses it? |
| **Tone** | Pick an extreme: brutalist, maximalist, retro-futuristic, organic, luxury, playful, editorial, art deco, soft pastel, industrial |
| **Constraints** | Framework requirements, performance, accessibility |
| **Differentiation** | What's the ONE thing someone will remember? |

**Key insight:** Bold maximalism and refined minimalism both work. The key is intentionality, not intensity.

## Anti-Patterns (AI Slop)

### ❌ Never Use

**Typography:**
- Inter, Roboto, Arial, system fonts
- Space Grotesk (overused "good" choice)
- Default font stacks without character

**Color:**
- Purple gradients on white backgrounds
- Evenly-distributed, timid palettes
- Default framework colors

**Layout:**
- Excessive centered elements
- Predictable symmetric layouts
- Cookie-cutter component patterns
- Uniform rounded corners everywhere

## What to Do Instead

### Typography

| Technique | Description |
|-----------|-------------|
| **Extreme contrast** | 72pt headlines vs 11pt body |
| **All-caps headers** | With wide letter spacing |
| **Monospace for data** | Technical content, stats, code |
| **Display + body pairing** | Distinctive display font with refined body font |
| **Outlined text** | For emphasis on bold backgrounds |

### Color & Theme

Choose from or adapt these palettes:

**Professional:**
```
Classic Blue:      #1C2833 #2E4053 #AAB7B8 #F4F6F6
Black & Gold:      #BF9A4A #000000 #F4F6F6
Charcoal & Red:    #292929 #E33737 #CCCBCB
```

**Warm:**
```
Teal & Coral:      #5EA8A7 #277884 #FE4447 #FFFFFF
Warm Blush:        #A49393 #EED6D3 #E8B4B8 #FAF7F2
Sage & Terracotta: #87A96B #E07A5F #F4F1DE #2C2C2C
```

**Bold:**
```
Bold Red:          #C0392B #E74C3C #F39C12 #2ECC71
Vibrant Orange:    #F96D00 #F2F2F2 #222831
Pink & Purple:     #F8275B #FF574A #FF737D #3D2F68
```

**Cool:**
```
Deep Purple:       #B165FB #181B24 #40695B #FFFFFF
Forest Green:      #191A19 #4E9F3D #1E5128 #FFFFFF
Cream & Forest:    #FFE1C7 #40695B #FCFCFC
```

**Use dominant colors with sharp accents** - this outperforms timid, evenly-distributed palettes.

### Spatial Composition

| Pattern | Description |
|---------|-------------|
| **Asymmetry** | Unequal column widths (30/70, 40/60, 25/75) |
| **Overlap** | Elements breaking boundaries, layered depth |
| **Diagonal flow** | Angled section dividers, rotated elements |
| **Grid-breaking** | Strategic elements that escape the grid |
| **Negative space** | Generous breathing room OR controlled density |

### Visual Details

**Geometric:**
- Diagonal section dividers instead of horizontal
- Rotated text headers at 90° or 270°
- Circular/hexagonal frames for images
- Triangular accent shapes in corners

**Borders & Frames:**
- Thick single-color borders (10-20pt) on one side only
- Double-line borders with contrasting colors
- Corner brackets instead of full frames
- L-shaped borders (top+left or bottom+right)
- Underline accents beneath headers (3-5pt thick)

**Backgrounds:**
- Solid color blocks occupying 40-60% of slide/page
- Gradient fills (vertical or diagonal only)
- Split backgrounds (two colors, diagonal or vertical)
- Edge-to-edge color bands
- Noise textures, grain overlays

### Motion & Animation

**Prioritize high-impact moments:**

1. **Page load** - Staggered reveals using `animation-delay`
2. **Scroll triggers** - Elements entering viewport
3. **Hover states** - Surprising transformations

One well-orchestrated page load creates more delight than scattered micro-interactions.

**CSS-first for HTML, Motion library for React.**

## Implementation Rules

### Match Complexity to Vision

- **Maximalist designs** → Elaborate code with extensive animations and effects
- **Minimalist designs** → Restraint, precision, careful spacing and typography

Elegance comes from executing the vision well.

### Consistency

- Use CSS variables for colors: `--color-primary`, `--color-accent`
- Establish spacing scale: 4px, 8px, 16px, 24px, 32px, 48px, 64px
- Repeat visual patterns across components

### Accessibility

- Ensure sufficient contrast (WCAG AA minimum)
- Don't rely on color alone for meaning
- Maintain readable font sizes (16px body minimum)
- Test with keyboard navigation

## Craftsmanship Standard

Create work that appears:
- **Meticulously crafted** - Every detail intentional
- **Product of deep expertise** - Professional-level execution
- **Painstakingly refined** - No rough edges
- **Master-level implementation** - Could be shown as portfolio work

The final result should look like it took countless hours by someone at the absolute top of their field.
