---
name: typography-designer
description: Designs typography systems including font choices, font sizes, font weights, line heights, and text styles. Creates type scale and defines usage guidelines. Ensures readability and accessibility.
---

# Typography Designer Skill

## Instructions

1. Analyze typography requirements from task
2. Select appropriate font families (or use existing)
3. Create type scale (heading sizes, body text, etc.)
4. Define font weights and line heights
5. Specify text styles and variations
6. Ensure readability and accessibility
7. Return structured typography specifications with:
   - Font families
   - Type scale
   - Font weights
   - Line heights
   - Text styles
   - Usage guidelines

## Examples

**Input:** "Design typography system"
**Output:**
```markdown
### Typography System

**Font Families:**
- Primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
- Monospace: 'Fira Code', 'Courier New', monospace

**Type Scale:**
- H1: 32px (2rem), weight 700, line-height 1.2
- H2: 24px (1.5rem), weight 700, line-height 1.3
- H3: 20px (1.25rem), weight 600, line-height 1.4
- H4: 18px (1.125rem), weight 600, line-height 1.4
- H5: 16px (1rem), weight 600, line-height 1.5
- H6: 14px (0.875rem), weight 600, line-height 1.5
- Body: 16px (1rem), weight 400, line-height 1.6
- Small: 14px (0.875rem), weight 400, line-height 1.5
- Caption: 12px (0.75rem), weight 400, line-height 1.4

**Font Weights:**
- Light: 300
- Regular: 400
- Medium: 500
- Semi-bold: 600
- Bold: 700

**Text Styles:**
- Heading: Bold, larger size, tighter line-height
- Body: Regular weight, comfortable line-height
- Link: Same as body, with underline and color
- Code: Monospace font, smaller size
- Caption: Smaller size, lighter weight

**Responsive Typography:**
- Mobile: Base 14px, scale down headings
- Tablet: Base 16px, standard scale
- Desktop: Base 16px, standard scale
```

## Typography Elements

- **Font Families**: Primary, secondary, monospace fonts
- **Type Scale**: Heading hierarchy (H1-H6), body, small, caption
- **Font Weights**: Light, regular, medium, semi-bold, bold
- **Line Heights**: Line spacing for readability
- **Letter Spacing**: Character spacing adjustments
- **Text Styles**: Paragraph, heading, link, code, caption
- **Text Colors**: Primary and secondary text colors
- **Text Alignment**: Left, center, right, justify

## Accessibility Requirements

- **Readable Sizes**: Minimum 14px for body text (16px preferred)
- **Line Height**: Minimum 1.5 for body text
- **Line Length**: Maximum 75-80 characters per line
- **Color Contrast**: Text meets WCAG AA (4.5:1)
- **Font Loading**: Consider font loading and fallbacks

## Responsive Typography

- **Mobile**: Smaller base size, adjusted scale
- **Tablet**: Standard base size
- **Desktop**: Standard or slightly larger base size
- **Fluid Typography**: Consider using rem/em for scalability
