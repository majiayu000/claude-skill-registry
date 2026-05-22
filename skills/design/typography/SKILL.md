---
name: typography
description: Apply professional typography principles to create readable, hierarchical, and aesthetically refined interfaces. Use when setting type scales, choosing fonts, adjusting spacing, designing text-heavy layouts, or when the user asks about readability, font pairing, line height, measure, or typographic hierarchy.
---

# Typography

Professional typography for user interfaces.

## Output Contract

For type system recommendations:

```markdown
## Type System

### Scale
- Base: [size, e.g., 16px]
- Ratio: [e.g., Minor Third 1.200]
- Rationale: [why this ratio]

### Hierarchy
| Level | Size | Weight | Line Height | Letter Spacing | Use |
|-------|------|--------|-------------|----------------|-----|
| Display | ... | ... | ... | ... | Hero, marketing |
| H1 | ... | ... | ... | ... | Page titles |
| H2 | ... | ... | ... | ... | Section heads |
| Body | ... | ... | ... | ... | Paragraphs |
| Small | ... | ... | ... | ... | Captions, labels |

### Fonts
- Primary: [font] - [rationale]
- Secondary: [font, if applicable]
- Mono: [font, if applicable]

### Implementation
```css
/* Ready-to-use CSS variables */
```
```

For typography audits:

```markdown
## Typography Audit

### Issues
| Element | Problem | Recommendation |
|---------|---------|----------------|
| ... | ... | ... |

### Quick Wins
- [Immediate improvement 1]
- [Immediate improvement 2]
```

## Core Principles

### Hierarchy & Structure
- Establish clear visual hierarchy through size, weight, and spacing
- Limit to 3-4 distinct heading levels in practice
- Use weight contrast (not just size) to differentiate levels
- Maintain consistent hierarchy patterns across the application

### Readability First
- Optimize for scanning: users read in F-patterns
- Left-align body text (centered only for short, formal text)
- Ensure sufficient contrast (4.5:1 minimum, 7:1 preferred)
- Test with real content, not lorem ipsum

### Restraint & Consistency
- Use 1-2 font families maximum (one serif, one sans-serif if pairing)
- Establish a type scale and stick to it
- Avoid decorative fonts for functional UI text
- Let whitespace do the work; resist the urge to fill

## Type Scales

### Modular Scales
Common ratios for harmonious sizing:
- **Minor Second** (1.067): Subtle, conservative
- **Major Second** (1.125): Gentle, professional
- **Minor Third** (1.200): Balanced, versatile
- **Major Third** (1.250): Bold, impactful
- **Perfect Fourth** (1.333): Strong hierarchy
- **Golden Ratio** (1.618): Dramatic, editorial

### Practical Scale (Minor Third, base 16px)
```
text-xs:   12px (0.75rem)
text-sm:   14px (0.875rem)
text-base: 16px (1rem)
text-lg:   18px (1.125rem)
text-xl:   20px (1.25rem)
text-2xl:  24px (1.5rem)
text-3xl:  30px (1.875rem)
text-4xl:  36px (2.25rem)
text-5xl:  48px (3rem)
```

### When to Deviate
- Marketing/hero sections can use larger jumps
- Dense data interfaces may need tighter scales
- Mobile often requires slightly larger base sizes

## Measure (Line Length)

### Optimal Ranges
- **Body text**: 45-75 characters (66 ideal)
- **Short-form**: 40-60 characters
- **Wide layouts**: Use columns or max-width constraints
- **Mobile**: Full width is acceptable due to narrow viewport

### Implementation
```css
/* Tailwind equivalents */
max-w-prose  /* ~65ch */
max-w-2xl    /* 672px, good for articles */
max-w-xl     /* 576px, compact content */
```

### Multi-Column Considerations
- Narrower columns = shorter measure acceptable
- Gutters should be at least 20px (1.25rem)
- Avoid orphaned words at column breaks

## Line Height (Leading)

### Guidelines by Context
- **Body text**: 1.5-1.7 (generous for readability)
- **Headings**: 1.1-1.3 (tighter, especially large sizes)
- **UI labels**: 1.2-1.4 (compact but legible)
- **Buttons**: 1.0-1.25 (single line, tight)

### Adjustments
- Increase line height for wider measure
- Decrease for larger type sizes
- Consider the x-height of the typeface
- Dark mode may benefit from slightly more leading

## Letter Spacing (Tracking)

### General Rules
- **Body text**: Default (0) or very slight increase
- **All caps**: Always add positive tracking (+0.05em to +0.1em)
- **Large headings**: Slight negative tracking (-0.01em to -0.02em)
- **Small text**: Slight positive tracking for legibility

### Tailwind Classes
```
tracking-tighter: -0.05em
tracking-tight:   -0.025em
tracking-normal:  0
tracking-wide:    0.025em
tracking-wider:   0.05em
tracking-widest:  0.1em
```

### All-Caps Text
- Always use `uppercase tracking-wide` or `tracking-wider`
- Keep short (1-3 words ideal)
- Common for labels, category tags, eyebrow text

## Font Selection

### System Font Stacks
Performant and native-feeling:
```css
/* Sans-serif (modern) */
font-family: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";

/* Serif */
font-family: ui-serif, Georgia, Cambria, "Times New Roman", serif;

/* Monospace */
font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
```

### Web Font Considerations
- Limit to 2-3 weights per family (400, 500/600, 700)
- Use `font-display: swap` for performance
- Variable fonts reduce file size for multiple weights
- Self-host for privacy and reliability

### Pairing Principles
- Pair by contrast (serif + sans-serif)
- Match x-height for visual harmony
- Use one font for headings, one for body
- Ensure both have needed weights/styles

### Safe Recommendations
- **Sans-serif**: Inter, Source Sans Pro, Open Sans, Work Sans
- **Serif**: Source Serif Pro, Lora, Merriweather, Literata
- **Monospace**: JetBrains Mono, Fira Code, Source Code Pro

## Paragraph Spacing

### Between Paragraphs
- Use margin-bottom equal to line-height or slightly more
- Typically 1em to 1.5em between paragraphs
- First paragraph after heading: reduced or no top margin

### Between Sections
- 2-3x paragraph spacing between major sections
- Use consistent spacing tokens from design system
- Consider visual grouping via proximity

## Typographic Details

### Quotation Marks
- Use curly quotes (" " ' ') not straight quotes (" ')
- Proper apostrophes: it's, don't, '90s
- Consider the locale (French guillemets, German quotes)

### Dashes
- **Hyphen** (-): Word breaks, compound words
- **En dash** (–): Ranges (2020–2024), relationships (New York–London)
- **Em dash** (—): Parenthetical statements, emphasis

### Numbers
- Use tabular (monospace) figures in tables for alignment
- Use proportional figures in body text
- Consider old-style figures for editorial content

### Ellipsis
- Use proper ellipsis character (…) not three periods
- Add thin space before/after in formal typography

## Responsive Typography

### Fluid Type
Scale font sizes smoothly between breakpoints:
```css
/* clamp(min, preferred, max) */
font-size: clamp(1rem, 0.5rem + 1.5vw, 1.5rem);
```

### Breakpoint Adjustments
- Increase base size slightly on mobile (17-18px)
- Reduce heading scale on mobile
- Increase line height for small screens
- Reduce measure on tablets (prose can feel too wide)

### Touch Targets
- Minimum 44x44px for tappable text elements
- Generous padding around links in body text
- Avoid text-only targets without visual indication

## Dark Mode Typography

### Adjustments
- Reduce font weight slightly (medium instead of semibold)
- Increase letter spacing marginally
- Consider warmer white (#f5f5f5) over pure white (#fff)
- Increase line height by ~0.1 for perceived lightness

### Contrast Considerations
- Pure white on pure black is harsh; soften both
- Aim for 10:1 to 15:1 contrast in dark mode
- Test with actual users; perceived contrast differs

## Accessibility

### Font Size Minimums
- Body text: 16px minimum (don't go below)
- Secondary text: 14px minimum, 12px absolute floor
- Legal/caption: 12px with increased tracking

### User Preferences
- Respect `font-size` from browser settings
- Use relative units (rem) not fixed (px) for text
- Provide text scaling options for dense UIs

### Dyslexia Considerations
- Avoid justified text
- Prefer sans-serif with distinct letterforms
- Generous line height and paragraph spacing
- OpenDyslexic as optional font choice

## Common Mistakes

### Avoid
- All-caps body text or long headings
- Centered body paragraphs
- Line length over 80 characters
- Insufficient contrast for "aesthetic" reasons
- Mixing too many font families
- Decorative fonts for UI text
- Justified text on the web (causes rivers)
- Tiny gray text on white backgrounds

### Watch For
- Orphans and widows in prominent text
- Inconsistent heading hierarchy
- Missing font fallbacks
- Layout shift from web font loading
- Underlined text that isn't a link
