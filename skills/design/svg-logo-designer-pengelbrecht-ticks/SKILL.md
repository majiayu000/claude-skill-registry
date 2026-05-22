---
name: "SVG Logo Designer"
description: "Create professional SVG logos from descriptions and design specifications. Generates multiple logo variations with different layouts, styles, and concepts. Produces scalable vector graphics that can be used directly or exported to PNG. Use this skill when users ask to create logos, brand identities, icons, or visual marks for their designs."
---

# SVG Logo Designer

This skill creates professional, scalable vector graphic (SVG) logos from design specifications, offering multiple variations and layout options.

## When to Use This Skill

Activate this skill when the user requests:
- Create a logo from a description or specification
- Design a brand identity or visual mark
- Generate logo variations and concepts
- Create icons or symbols
- Design wordmarks or lettermarks
- Produce scalable graphics for branding
- Export logos in different layouts and styles

## Core Workflow

### Phase 1: Requirements Gathering

When a user requests a logo, gather comprehensive design requirements:

1. **Brand Information**
   - Company/product name
   - Industry and market
   - Target audience
   - Brand personality (modern, classic, playful, serious, etc.)
   - Brand values and messaging
   - Competitors (for differentiation)

2. **Design Preferences**
   - Logo type:
     - **Wordmark**: Text-based logo (Google, Coca-Cola style)
     - **Lettermark**: Initials/abbreviation (IBM, HBO style)
     - **Pictorial Mark**: Icon/symbol (Apple, Twitter style)
     - **Abstract Mark**: Abstract geometric form (Pepsi, Adidas style)
     - **Mascot**: Character-based (KFC Colonel, Michelin Man style)
     - **Combination Mark**: Icon + text (Burger King, Lacoste style)
     - **Emblem**: Text inside symbol (Starbucks, Harley-Davidson style)

3. **Style Guidelines**
   - Color palette (specific colors or let AI choose)
   - Color psychology considerations
   - Font preferences (if text-based)
   - Visual style:
     - Minimalist
     - Geometric
     - Organic/flowing
     - Bold/strong
     - Elegant/refined
     - Playful/friendly
     - Tech/modern
     - Vintage/retro

4. **Technical Requirements**
   - Size constraints (will it be used small? large?)
   - Application contexts (website, print, merchandise, etc.)
   - Color vs monochrome versions needed
   - Background usage (light, dark, transparent)
   - Scalability requirements

5. **Number of Variations**
   - How many different concepts? (Recommend 3-5)
   - How many layouts per concept? (Horizontal, vertical, square, circular)
   - Color variations needed?

### Phase 2: Design Concept Development

Create multiple logo concepts based on requirements:

#### Concept 1: Primary Direction

Develop the main design direction:

**Design Thinking:**
- Research visual metaphors related to brand
- Consider negative space opportunities
- Ensure memorability and uniqueness
- Balance simplicity with distinctiveness
- Consider cultural appropriateness

**SVG Structure:**
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <!-- Gradients, patterns, filters -->
    <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4F46E5;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#7C3AED;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- Logo elements -->
  <g id="logo-symbol">
    <!-- Symbol/icon elements -->
  </g>

  <g id="logo-text">
    <!-- Text elements (if applicable) -->
  </g>
</svg>
```

#### Concept 2-5: Alternative Directions

Create variations exploring different visual approaches:
- Different visual metaphors
- Different style treatments
- Different layouts and compositions
- Different color applications

### Phase 3: Layout Variations

For each concept, create multiple layout options:

#### Layout A: Horizontal Lockup
- Icon on left, text on right
- Best for website headers, business cards
- Wider aspect ratio

#### Layout B: Vertical Lockup
- Icon on top, text below
- Best for social media profiles, app icons
- Taller aspect ratio

#### Layout C: Square/Centered
- Icon and text centered
- Best for favicon, app icon, profile picture
- 1:1 aspect ratio

#### Layout D: Icon Only
- Symbol without text
- Best for small sizes, watermarks
- Compact, recognizable

#### Layout E: Text Only
- Wordmark without icon
- Best for minimal applications
- Typography-focused

### Phase 4: SVG Generation

Create professional, optimized SVG code:

**Best Practices:**

1. **Clean, Semantic Code**
```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60">
  <!-- Use groups for organization -->
  <g id="icon">
    <!-- Icon elements -->
  </g>
  <g id="wordmark">
    <!-- Text elements -->
  </g>
</svg>
```

2. **Scalable Design**
   - Use viewBox for scalability
   - Avoid pixel-specific sizes
   - Use relative units
   - Design at multiple sizes to test

3. **Color Management**
```xml
<!-- Define colors once, reuse throughout -->
<defs>
  <style>
    .primary { fill: #4F46E5; }
    .secondary { fill: #10B981; }
    .text { fill: #1F2937; }
  </style>
</defs>

<rect class="primary" x="0" y="0" width="100" height="100" />
```

4. **Optimization**
   - Remove unnecessary attributes
   - Combine paths where possible
   - Use symbols for repeated elements
   - Minimize decimal precision
   - Remove invisible elements

5. **Accessibility**
```xml
<svg role="img" aria-labelledby="logo-title logo-desc">
  <title id="logo-title">Company Name Logo</title>
  <desc id="logo-desc">A blue circular icon with the company name</desc>
  <!-- Logo content -->
</svg>
```

### Phase 5: Presentation

Present logos in an organized, professional manner:

```markdown
# Logo Design Concepts

## Concept 1: [Concept Name/Theme]

### Design Rationale
[Explain the thinking behind this design, visual metaphors used, and how it represents the brand]

### Primary Logo (Horizontal)
```xml
<svg><!-- SVG code here --></svg>
```

**Usage:** Headers, website navigation, business cards
**Dimensions:** 200×60px (scalable)

### Vertical Layout
```xml
<svg><!-- SVG code here --></svg>
```

**Usage:** Social media profiles, mobile apps
**Dimensions:** 100×120px (scalable)

### Icon Only
```xml
<svg><!-- SVG code here --></svg>
```

**Usage:** Favicon, app icon, small spaces
**Dimensions:** 64×64px (scalable)

### Color Variations

**Full Color:**
- Primary: #4F46E5 (Indigo)
- Secondary: #10B981 (Emerald)

**Monochrome (Dark):**
- Single color: #1F2937 (Gray-900)

**Monochrome (Light):**
- Single color: #FFFFFF (White)

**Reversed:**
- For dark backgrounds

---

## Concept 2: [Concept Name/Theme]

[Repeat structure for additional concepts]
```

### Phase 6: File Generation

Save SVG files with proper naming:

```javascript
// File naming convention
company-name-logo-concept1-horizontal.svg
company-name-logo-concept1-vertical.svg
company-name-logo-concept1-icon.svg
company-name-logo-concept2-horizontal.svg
// etc.
```

Use the Write tool to save each variation:
```javascript
// Example
Write({
  file_path: "./logos/acme-logo-concept1-horizontal.svg",
  content: svgCode
});
```

### Phase 7: Usage Guidelines

Provide comprehensive usage documentation:

```markdown
# Logo Usage Guidelines

## File Formats Provided

### SVG (Scalable Vector Graphics)
- **Use for:** Websites, digital applications, large prints
- **Benefits:** Infinitely scalable, small file size, editable
- **How to use:** Embed directly in HTML or open in design tools

### Exporting to PNG
If you need PNG format:

**Option 1: Using Inkscape (Free)**
```bash
inkscape logo.svg --export-png=logo.png --export-width=1000
```

**Option 2: Using ImageMagick**
```bash
convert -background none logo.svg logo.png
```

**Option 3: Online Converter**
- Visit: https://cloudconvert.com/svg-to-png
- Upload SVG, download PNG

## Clear Space

Maintain minimum clear space around logo:
- Distance = Height of logo symbol
- No text or graphics in clear space

## Minimum Sizes

- **Digital:** 100px width minimum
- **Print:** 1 inch width minimum

## Color Usage

### Primary Color Palette
- Use full color on white/light backgrounds
- Use monochrome white on dark backgrounds
- Use monochrome dark on light backgrounds

### Color Variations by Context

**Website Headers:**
- Full color version preferred
- Ensure 4.5:1 contrast with background

**Social Media:**
- Use square/circular crops
- Provide background color if needed

**Print Materials:**
- Full color for color printing
- Monochrome black for B&W printing
- Consider spot color for cost-effective printing

## Incorrect Usage

❌ Do Not:
- Stretch or distort the logo
- Change colors outside approved palette
- Add effects (shadows, glows, etc.)
- Rotate or skew the logo
- Place on busy backgrounds without clear space
- Recreate or modify logo elements

## File Organization

```
logos/
  concept-1/
    horizontal/
      full-color.svg
      monochrome-dark.svg
      monochrome-light.svg
    vertical/
      [same variations]
    icon/
      [same variations]
  concept-2/
    [same structure]
```

## Technical Specifications

### Web Usage
```html
<!-- Inline SVG (Recommended for control) -->
<svg><!-- SVG code --></svg>

<!-- Image tag (Simpler) -->
<img src="logo.svg" alt="Company Name Logo" />

<!-- CSS Background -->
.logo {
  background-image: url('logo.svg');
  background-size: contain;
}
```

### Responsive Implementation
```css
.logo {
  width: 100%;
  max-width: 200px;
  height: auto;
}

/* Mobile */
@media (max-width: 768px) {
  .logo {
    max-width: 150px;
  }
}
```
```

## Design Patterns & Examples

### Wordmark Logo

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 80">
  <defs>
    <style>
      .wordmark {
        font-family: 'Helvetica', sans-serif;
        font-size: 48px;
        font-weight: 700;
        fill: #1F2937;
      }
    </style>
  </defs>
  <text x="10" y="60" class="wordmark">COMPANY</text>
</svg>
```

### Geometric Icon

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4F46E5" />
      <stop offset="100%" style="stop-color:#7C3AED" />
    </linearGradient>
  </defs>

  <!-- Hexagon shape -->
  <polygon
    points="50,5 95,27.5 95,72.5 50,95 5,72.5 5,27.5"
    fill="url(#grad)"
    stroke="#312E81"
    stroke-width="2"
  />

  <!-- Inner element -->
  <circle cx="50" cy="50" r="20" fill="#FFFFFF" />
</svg>
```

### Abstract Mark

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <!-- Flowing abstract shape -->
  <path
    d="M10,50 Q30,20 50,50 T90,50 Q70,80 50,50 T10,50 Z"
    fill="#10B981"
    opacity="0.8"
  />
  <path
    d="M15,55 Q35,25 55,55 T95,55"
    fill="none"
    stroke="#059669"
    stroke-width="3"
    stroke-linecap="round"
  />
</svg>
```

### Combination Mark

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 80">
  <!-- Icon -->
  <g id="icon">
    <circle cx="40" cy="40" r="30" fill="#4F46E5" />
    <path d="M30,35 L35,45 L50,25" stroke="#FFFFFF" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round" />
  </g>

  <!-- Text -->
  <g id="text">
    <text x="85" y="45" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="#1F2937">
      COMPANY
    </text>
  </g>
</svg>
```

## Color Psychology Guide

Help users choose appropriate colors:

**Blue** (#0066CC, #4F46E5)
- Trust, professionalism, stability
- Industries: Finance, technology, healthcare

**Green** (#10B981, #059669)
- Growth, health, eco-friendly
- Industries: Environment, wellness, finance

**Red** (#DC2626, #EF4444)
- Energy, passion, urgency
- Industries: Food, entertainment, retail

**Purple** (#7C3AED, #8B5CF6)
- Creativity, luxury, spirituality
- Industries: Beauty, tech, creative

**Orange** (#F97316, #FB923C)
- Friendly, energetic, affordable
- Industries: Retail, food, entertainment

**Yellow** (#FBBF24, #FCD34D)
- Optimism, clarity, warmth
- Industries: Food, children, energy

**Black/Gray** (#1F2937, #6B7280)
- Sophisticated, modern, classic
- Industries: Luxury, fashion, technology

## Iteration Process

After presenting initial concepts:

1. **Gather Feedback**
   - Which concept resonates most?
   - What elements to keep/change?
   - Any concerns or issues?

2. **Refine Selected Concept**
   - Adjust colors if needed
   - Tweak proportions
   - Refine details
   - Test at different sizes

3. **Create Final Variations**
   - All layout options
   - All color variations
   - Special use cases

4. **Deliver Final Package**
   - All SVG files
   - Usage guidelines
   - Technical specs
   - Export instructions

## Communication Style

When working with users:

1. **Understand the Brand**
   - Ask about brand personality
   - Understand target audience
   - Research industry context

2. **Explain Design Choices**
   - Share rationale for visual metaphors
   - Explain color psychology
   - Justify composition decisions

3. **Provide Options**
   - Offer multiple concepts
   - Show layout variations
   - Demonstrate color options

4. **Be Flexible**
   - Accept feedback gracefully
   - Iterate based on input
   - Explain limitations when necessary

5. **Educate**
   - Explain SVG benefits
   - Guide on proper usage
   - Share best practices

## Deliverables

Provide complete logo package:

1. **SVG Files**
   - All concepts (3-5)
   - All layouts per concept (3-5)
   - All color variations (3-4)
   - Total: 30-75 files typically

2. **Documentation**
   - Usage guidelines
   - Color specifications
   - Size recommendations
   - Do's and don'ts

3. **Technical Info**
   - File organization structure
   - Export instructions (SVG to PNG)
   - Web implementation examples
   - Print specifications

4. **Optional: Mockups**
   - Logo on business card
   - Logo on website header
   - Logo on product
   - Logo on signage

## Example Workflow

**User Request:**
> "Create a logo for my tech startup called 'CloudSync'. We provide cloud storage solutions. Looking for something modern and trustworthy."

**Your Response:**

1. **Clarify:**
   - "I'll create a modern, tech-focused logo for CloudSync. A few questions:
     - Preferred colors? (Suggesting blue for trust, or let me propose a palette)
     - Logo type preference? (I'm thinking combination mark - icon + text)
     - Any visual elements to avoid or include? (clouds, sync symbols, etc.)
     - How many concepts would you like to see? (I recommend 3-4)"

2. **Develop Concepts:**
   - **Concept 1**: Abstract cloud with sync arrows, modern geometric style
   - **Concept 2**: Minimalist wordmark with stylized 'C' incorporating cloud
   - **Concept 3**: Circular badge with cloud and connection nodes
   - **Concept 4**: Bold lettermark 'CS' with cloud integration

3. **Create Variations:**
   - For each concept: horizontal, vertical, icon-only layouts
   - Color variations: full color, monochrome, reversed

4. **Present:**
   - Show all concepts with rationale
   - Provide SVG code for each
   - Include usage guidelines
   - Offer iteration based on feedback

5. **Refine:**
   - User selects favorite concept
   - Make requested adjustments
   - Finalize all variations
   - Deliver complete package

Remember: Great logos are simple, memorable, timeless, versatile, and appropriate. Focus on creating designs that will work across all applications and stand the test of time!
