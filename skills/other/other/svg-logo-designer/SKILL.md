---
name: svg-logo-designer
description: Create professional SVG logos from descriptions and design specifications. Use when the user asks to create a logo, icon, brand mark, or scalable vector graphic. Generates multiple logo variations with different layouts, styles, and concepts.
---

# SVG Logo Designer

## Overview

This skill creates professional, scalable vector graphics (SVG) logos and icons. SVG format ensures logos remain crisp at any size and can be easily modified, exported to PNG, or used directly in web applications.

## Logo Design Process

### 1. Understand the Brief

Gather key information:
- **Company/Product Name**: What text should appear?
- **Industry/Domain**: What sector (tech, trades, healthcare, etc.)?
- **Brand Values**: Professional, playful, modern, traditional, bold, minimal?
- **Target Audience**: Who is this for?
- **Style Preferences**: Abstract, literal, typography-based, geometric, organic?
- **Color Preferences**: Specific colors or open to suggestions?

### 2. Generate Concept Variations

Create 2-3 distinct logo concepts with different approaches:

**Variation A: Wordmark**
- Typography-focused design
- Custom lettering or refined font treatment
- Minimal or no iconography

**Variation B: Icon + Text**
- Balanced combination of symbol and text
- Icon represents brand values or industry
- Can work with or without text

**Variation C: Abstract Mark**
- Geometric or organic abstract symbol
- Memorable and unique shape
- Modern and scalable

### 3. SVG Best Practices

Follow these technical standards:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <!-- Use viewBox for scalability -->
  <!-- Keep artwork centered in viewBox -->
  <!-- Use clean, simple paths -->
  <!-- Avoid unnecessary complexity -->
</svg>
```

**Technical Guidelines:**
- Use `viewBox` instead of fixed width/height for scalability
- Keep paths clean and optimized
- Use meaningful group IDs and classes
- Limit colors to 1-3 for versatility
- Ensure logo works in monochrome
- Test at multiple sizes (favicon to billboard)

### 4. Color Strategies

**Primary Logo**: Full color version
**Secondary Logo**: Single color (usually black)
**Reversed Logo**: White on dark backgrounds
**Monochrome**: Grayscale version

Use CSS variables or separate SVG versions for color variations.

### 5. Layout Variations

Provide horizontal and vertical/stacked versions:
- **Horizontal**: Icon + text side-by-side
- **Vertical**: Icon above text (stacked)
- **Icon-only**: For favicons, app icons, social media

## Output Format

For each logo variation, provide:

1. **SVG Code**: Complete, valid SVG markup
2. **Preview Description**: How it looks and feels
3. **Use Cases**: Where this version works best
4. **Color Codes**: Hex values for all colors used
5. **Export Instructions**: How to save as PNG if needed

## Logo Design Principles

### Simplicity
- Less is more - remove unnecessary details
- Should be recognizable at small sizes
- Avoid trends that quickly date

### Memorability
- Distinctive and unique
- One clear focal point
- Conceptually relevant to brand

### Timelessness
- Avoid overly trendy styles
- Classic approaches with modern execution
- Should age well over years

### Versatility
- Works in color and black & white
- Scales from favicon to billboard
- Readable on any background color

### Appropriateness
- Fits the industry and brand personality
- Appeals to target audience
- Conveys the right tone and values

## Example Workflow

1. **User**: "Create a logo for 'Blue Collar Bot', a SaaS platform for trade businesses"

2. **Designer** (you):
   - Analyze: Trade industry, tech platform, needs professional yet accessible feel
   - Concepts:
     - A: Geometric robot icon with wrench/tool integration
     - B: Bold typography with subtle gear/bot element
     - C: Abstract mark suggesting both automation and hands-on work
   - Create 3 SVG variations
   - Provide color and monochrome versions
   - Include horizontal and icon-only layouts

3. **Deliverables**:
   - 3 concept variations × 2-3 layouts each
   - Color codes and export instructions
   - Recommendations for primary logo

## Common Logo Types

- **Wordmark**: Text-only (Google, Coca-Cola)
- **Lettermark**: Initials (IBM, HP, CNN)
- **Brand Mark**: Icon-only (Apple, Twitter bird)
- **Combination Mark**: Icon + text (Adidas, Burger King)
- **Emblem**: Text inside icon (Starbucks, Harley-Davidson)

Choose type based on brand name length, industry, and recognition goals.

## When to Use This Skill

- Creating a new logo for a company or product
- Redesigning an existing logo
- Generating logo variations for different contexts
- Creating icons for apps or websites
- Designing brand marks or emblems
- Need scalable vector graphics

## File Export Tips

To convert SVG to PNG:
1. Save SVG code to a .svg file
2. Open in design tool (Figma, Illustrator, Inkscape)
3. Export as PNG at desired resolution (typically 1024×1024 for general use)

Or use online tools:
- CloudConvert.com
- SVG2PNG.com
- Inkscape (free desktop app)
