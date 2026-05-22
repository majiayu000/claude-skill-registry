---
name: Typography Advisor
slug: typography-advisor
description: Expert font pairing and typography system design
category: design
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "font pairing"
  - "typography"
  - "choose fonts"
  - "type system"
  - "readable fonts"
tags:
  - typography
  - fonts
  - design
  - readability
---

# Typography Advisor

A typography expert that creates beautiful, readable type systems for any medium. This skill combines typographic principles, font pairing expertise, and accessibility best practices to design cohesive typography that enhances content and brand identity.

From selecting the perfect font combination to building a complete type scale with hierarchies, this skill ensures your text is both aesthetically pleasing and functionally excellent across all devices and use cases.

## Core Workflows

### Workflow 1: Font Pairing Selection
1. Understand project context:
   - Medium (web, print, mobile, presentation)
   - Brand personality (modern, classic, playful, serious)
   - Content type (long-form, UI labels, marketing, technical)
   - Audience demographics
2. Recommend font pairs:
   - Heading font (display/serif/sans)
   - Body font (optimized for readability)
   - Optional: Accent/code font
3. Provide pairing rationale:
   - Why these fonts work together
   - Contrast principles applied
   - Mood and personality match
4. Show examples with actual content
5. Include fallback stacks and loading strategy

### Workflow 2: Type Scale Creation
1. Define base settings:
   - Base font size (typically 16px for web)
   - Scale ratio (1.125, 1.25, 1.333, 1.5, etc.)
   - Viewport ranges (mobile, tablet, desktop)
2. Generate type scale:
   - 6-8 hierarchical sizes
   - Calculate line heights
   - Set letter spacing
   - Define font weights
3. Map to semantic elements:
   - H1-H6 headings
   - Body, small, caption
   - Button, label, code
4. Create responsive variations
5. Export as CSS/Tailwind config

### Workflow 3: Typography System Audit
1. Analyze existing typography:
   - Inventory all font sizes, weights, families
   - Check consistency across pages
   - Measure readability metrics
2. Identify issues:
   - Too many sizes (inconsistency)
   - Poor contrast/readability
   - Weak hierarchy
   - Accessibility problems
3. Provide recommendations:
   - Consolidate to systematic scale
   - Improve legibility
   - Strengthen visual hierarchy
4. Create migration guide

### Workflow 4: Readability Optimization
1. Assess content requirements:
   - Reading context (skimming vs. deep reading)
   - Content length
   - User constraints (age, vision, mobile usage)
2. Optimize parameters:
   - Line length (45-75 characters ideal)
   - Line height (1.5-1.75 for body text)
   - Font size (minimum 16px for body)
   - Contrast (minimum 4.5:1 for normal text)
3. Test with real content
4. Provide device-specific adjustments

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Find font pairs | "Suggest fonts for [brand/project]" |
| Create type scale | "Build a typography system for [context]" |
| Audit existing | "Review my typography for issues" |
| Optimize readability | "Make this text more readable" |
| Get Google Fonts | "Recommend free fonts for [use case]" |
| Premium options | "Suggest premium fonts for [project]" |

## Font Pairing Principles

**Contrast is key**: Pair different styles (serif + sans, geometric + humanist)

**Limit to 2-3 fonts**: More creates chaos
- Heading font (personality)
- Body font (readability)
- Optional accent (code, callouts)

**Superfamilies work**: Fonts designed together (like IBM Plex, Work Sans, etc.)

**Consider x-height**: Fonts with similar x-heights pair better

**Match mood**: Both fonts should support the brand personality

**Test in context**: View fonts with actual content, not lorem ipsum

## Classic Pairings

**Modern & Clean**
- Heading: Inter / Body: Source Sans Pro
- Heading: Montserrat / Body: Open Sans
- Heading: Raleway / Body: Lato

**Editorial & Professional**
- Heading: Playfair Display / Body: Source Sans Pro
- Heading: Merriweather / Body: Open Sans
- Heading: Lora / Body: Lato

**Tech & Startup**
- Heading: Space Grotesk / Body: Inter
- Heading: Work Sans / Body: IBM Plex Sans
- Heading: DM Sans / Body: Inter

**Creative & Bold**
- Heading: Bebas Neue / Body: Roboto
- Heading: Oswald / Body: Open Sans
- Heading: Abril Fatface / Body: Lato

**Minimal & Sophisticated**
- Single font system: Inter (various weights)
- Single font system: IBM Plex Sans
- Heading: Helvetica Now / Body: Helvetica Now

## Type Scale Ratios

| Ratio | Name | Best For |
|-------|------|----------|
| 1.067 | Minor Second | Subtle, minimal contrast |
| 1.125 | Major Second | Conservative, professional |
| 1.200 | Minor Third | Balanced, versatile |
| 1.250 | Major Third | Clear hierarchy, most common |
| 1.333 | Perfect Fourth | Strong hierarchy |
| 1.414 | Augmented Fourth | Bold, editorial |
| 1.500 | Perfect Fifth | Dramatic, luxury |
| 1.618 | Golden Ratio | Harmonious, natural |

## Best Practices

- **Mobile first**: Ensure fonts are readable at small sizes
- **Performance matters**: Limit font weights and styles loaded (2-4 max)
- **Use variable fonts**: One file, infinite weights (modern browsers)
- **System fonts as fallbacks**: Always provide -apple-system, BlinkMacSystemFont, etc.
- **FOIT/FOUT strategy**: Use font-display: swap for better UX
- **Subset fonts**: Only load characters you need (Latin, numerals, etc.)
- **Line length matters**: 45-75 characters per line for readability
- **Hierarchy first**: Size differences should be obvious at a glance
- **Consistent spacing**: Use the type scale for margins and padding too
- **Test with real content**: Lorem ipsum hides readability issues
- **Accessibility**: Minimum 16px body, 4.5:1 contrast, avoid light weights for small text
- **Respect user settings**: Don't break zoom, respect reduced motion
- **Version control**: Document font versions when using commercial fonts

## Typography Checklist

**Legibility**
- [ ] Minimum 16px for body text
- [ ] Adequate contrast (4.5:1 minimum)
- [ ] Line height 1.5+ for paragraphs
- [ ] Line length 45-75 characters
- [ ] Sufficient letter spacing for small text
- [ ] No light weights below 16px

**Hierarchy**
- [ ] Clear visual distinction between levels
- [ ] Consistent use of font sizes
- [ ] Logical heading structure (H1 > H2 > H3)
- [ ] Distinct styling for links, buttons, labels

**System**
- [ ] All sizes follow the type scale
- [ ] Limited to 2-3 font families
- [ ] Documented usage guidelines
- [ ] Responsive adjustments for mobile
- [ ] Proper fallback fonts

**Performance**
- [ ] Fonts properly subset
- [ ] Maximum 4-5 font files loaded
- [ ] font-display strategy set
- [ ] Preload critical fonts
- [ ] Consider variable fonts

## Deliverables Format

```
TYPOGRAPHY SYSTEM
Project: [Name]
Context: [Web/Print/Mobile]

FONTS
Heading: [Font Name] - [Weights used]
  Source: Google Fonts / Adobe Fonts / Commercial
  Fallback: [Stack]
  Usage: H1-H3, Display text, Hero headings

Body: [Font Name] - [Weights used]
  Source: Google Fonts / Adobe Fonts / Commercial
  Fallback: [Stack]
  Usage: Paragraphs, UI labels, captions

CODE (optional)
Mono: [Font Name]
  Source: Google Fonts
  Usage: Code blocks, technical content

TYPE SCALE (1.25 ratio, 16px base)
Display: 49px / 3.052rem (H1 on desktop)
H1: 39px / 2.441rem
H2: 31px / 1.953rem
H3: 25px / 1.563rem
H4: 20px / 1.25rem
Body: 16px / 1rem
Small: 13px / 0.8rem
Caption: 10px / 0.64rem

SPECIFICATIONS
H1: [Font] 39px/1.2 tracking -0.02em weight 700
H2: [Font] 31px/1.3 tracking -0.01em weight 600
Body: [Font] 16px/1.6 tracking 0 weight 400
...

RESPONSIVE ADJUSTMENTS
Mobile (<768px): Reduce scale ratio to 1.2
Tablet (768-1024px): Use base scale
Desktop (>1024px): Increase display sizes 10%

CSS/TAILWIND EXPORT
[Code with variables, classes, utilities]

USAGE GUIDELINES
- Use H1 only once per page
- Maximum 3 font weights per family
- Never go below 14px for body text
- Increase line-height for longer paragraphs
```

## Font Resources

**Free & High Quality**
- Google Fonts: Inter, Roboto, Open Sans, Playfair Display
- Adobe Fonts: (with Creative Cloud)
- Font Squirrel: Verified free fonts

**Premium**
- Fontshare: Free high-quality fonts
- Fontesk: Curated free fonts
- Commercial: Hoefler&Co, Klim Type Foundry, Grilli Type

**Tools**
- Google Fonts
- FontPair.co (pairing inspiration)
- Type Scale Calculator
- Modular Scale
- Archetype (font testing)

## Common Requests

**Landing page**: Bold heading + clean body (e.g., Montserrat + Inter)
**Blog/Editorial**: Serif heading + sans body (e.g., Merriweather + Open Sans)
**SaaS Product**: Modern sans system (e.g., Inter family)
**E-commerce**: Friendly sans (e.g., DM Sans + Work Sans)
**Portfolio**: Distinctive display + neutral body (e.g., Space Grotesk + IBM Plex)
**Documentation**: Readable system font (e.g., -apple-system stack)
