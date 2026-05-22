---
name: Color Palette Generator
slug: color-palette-generator
description: Create beautiful, accessible color schemes for any project
category: design
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create color palette"
  - "generate colors"
  - "color scheme"
  - "brand colors"
  - "design colors"
tags:
  - colors
  - design
  - branding
  - accessibility
---

# Color Palette Generator

An expert color theorist that creates harmonious, accessible color palettes for any project. This skill combines color theory principles, accessibility standards (WCAG), and modern design trends to generate cohesive color schemes that work across digital and print media.

Whether you need a vibrant brand identity, a calming UI palette, or a bold marketing scheme, this skill provides scientifically-backed color combinations with detailed usage guidelines, contrast ratios, and implementation code.

## Core Workflows

### Workflow 1: Brand Palette Creation
1. Gather requirements:
   - Brand personality (professional, playful, bold, minimal, etc.)
   - Industry context
   - Target audience
   - Desired emotional response
2. Generate primary color options (3-5 choices)
3. Build complementary palette:
   - Primary: Main brand color
   - Secondary: Supporting accent
   - Neutral: Grays/backgrounds
   - Semantic: Success, warning, error, info
4. Validate accessibility (WCAG AA/AAA compliance)
5. Provide usage guidelines and code

### Workflow 2: UI/UX Palette
1. Define interface requirements:
   - Light/dark mode support
   - Number of states needed
   - Content type (data-heavy, content-focused, etc.)
2. Create systematic color scale:
   - Base color with 9-11 tints/shades
   - Semantic colors with matching scales
   - Neutral scale for backgrounds/text
3. Map colors to UI elements:
   - Backgrounds, surfaces, overlays
   - Text hierarchy
   - Interactive states (hover, active, disabled)
   - Borders and dividers
4. Generate Tailwind/CSS variables
5. Create usage documentation

### Workflow 3: Palette from Inspiration
1. Accept input:
   - Image/photo reference
   - Brand logo
   - Competitor site
   - Color hex codes
2. Extract dominant colors using color theory
3. Refine and harmonize:
   - Apply color harmony rules (complementary, triadic, analogous)
   - Adjust saturation/lightness for consistency
   - Ensure sufficient contrast
4. Build complete palette with variations
5. Provide comparison with original

### Workflow 4: Accessibility Audit
1. Receive existing color palette
2. Test all color combinations:
   - Text on backgrounds
   - Button states
   - Interactive elements
3. Calculate contrast ratios (WCAG 2.1)
4. Identify failures and provide fixes:
   - Suggest darker/lighter alternatives
   - Show minimum adjustments needed
5. Generate accessibility report

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Create brand palette | "Generate a [mood] color palette for [industry]" |
| UI color system | "Create a UI palette for [project type]" |
| Extract from image | "Build palette from this [image/logo]" |
| Check accessibility | "Audit these colors for WCAG compliance" |
| Expand single color | "Create a full palette from #HEX" |
| Export formats | "Give me Tailwind/CSS/Figma variables" |

## Color Harmony Systems

**Monochromatic**: Single hue with varying lightness/saturation
- Use for: Minimal, sophisticated designs
- Best for: Photography sites, portfolios

**Analogous**: Adjacent colors on color wheel (30° apart)
- Use for: Harmonious, natural feel
- Best for: Wellness, nature, eco brands

**Complementary**: Opposite colors on wheel (180° apart)
- Use for: High contrast, energetic
- Best for: Sports, entertainment, retail

**Triadic**: Three colors equally spaced (120° apart)
- Use for: Balanced, vibrant
- Best for: Creative, playful brands

**Split-Complementary**: Base + two adjacent to complement
- Use for: Softer than complementary
- Best for: Professional services, SaaS

**Tetradic**: Four colors in two complementary pairs
- Use for: Rich, complex palettes
- Best for: Content-heavy, editorial

## Best Practices

- **Start with purpose**: Understand the emotional response and brand personality before choosing colors
- **Mind the ratios**: Use 60-30-10 rule (60% primary, 30% secondary, 10% accent)
- **Accessibility first**: Always check WCAG contrast ratios before finalizing
- **Test in context**: Colors look different on screens vs. print, light vs. dark backgrounds
- **Provide variations**: Include tints, shades, and tones for flexibility
- **Consider color blindness**: Test with simulators, ensure critical info isn't color-only
- **Document usage**: Specify which colors for what purpose (buttons, text, backgrounds)
- **Think systems**: Create scalable palettes that grow with the product
- **Cultural awareness**: Colors have different meanings in different cultures
- **Neutral foundation**: Every palette needs a solid gray scale
- **Semantic clarity**: Success, warning, error, info should be immediately recognizable
- **Dark mode ready**: Ensure colors work in both light and dark themes

## Deliverables Format

```
PALETTE NAME
Mood: [Adjectives describing the feel]

PRIMARY COLORS
Main Brand: #HEX - [Name] - RGB(r,g,b) - HSL(h,s,l)
  Usage: Primary buttons, headers, brand moments
  Accessible on: White, Light Gray

Secondary: #HEX - [Name]
  Usage: Accents, highlights, links
  Accessible on: White, Dark Gray

NEUTRAL SCALE
Gray-900: #HEX (Darkest - primary text)
Gray-800: #HEX (Secondary text)
...
Gray-100: #HEX (Lightest - subtle backgrounds)

SEMANTIC COLORS
Success: #HEX (Green family)
Warning: #HEX (Yellow/Orange family)
Error: #HEX (Red family)
Info: #HEX (Blue family)

CONTRAST RATIOS
✓ Primary on White: 4.8:1 (AA compliant)
✓ Secondary on Light Gray: 7.2:1 (AAA compliant)
✗ Warning on White: 2.1:1 (FAIL - suggest #HEX instead)

CODE EXPORT
[Tailwind config / CSS variables / Figma styles]

USAGE GUIDELINES
- When to use each color
- Do's and don'ts
- Common combinations
```

## Tools Integration

- Use **Midjourney** for generating color mood boards
- Use **WebSearch** to research industry color trends
- Use **Firecrawl** to analyze competitor color schemes
- Use **Playwright** to test colors in live browser context

## Common Requests

**Startup/Tech**: Blues, grays, vibrant accents
**Finance**: Navy, gold, conservative palette
**Healthcare**: Blues, greens, calming tones
**Food/Restaurant**: Reds, oranges, warm palette
**Eco/Sustainability**: Greens, earth tones, natural
**Luxury**: Black, gold, deep jewel tones
**Children/Education**: Primary colors, bright, playful
**Creative/Agency**: Bold, unconventional, statement colors
