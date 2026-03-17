---
name: graphic-design
description: Create professional graphic assets (banners, LinkedIn graphics, webinar promotions, social media visuals) with consistent NGM branding. Uses a hybrid approach combining AI-generated elements with template-based layouts.
allowed-tools: Read, Write, Edit, Glob, Grep, Browser
---

# NGM Graphic Design Studio

## Overview

Graphic Design Studio creates visual marketing assets for Next Generation Medicine that maintain brand consistency across all platforms. It uses a hybrid approach:

1. **AI-Generated Elements**: Backgrounds, abstract graphics, decorative elements
2. **Template-Based Composition**: Structured layouts with brand typography and colors
3. **Photo Integration**: Incorporating user-provided photos into designs

All graphics follow the NGM editorial design system—clean hierarchy, gold accents, Newsreader/Inter typography.

## Asset Types Supported

| Type | Dimensions | Use Case | Output Location |
|------|------------|----------|-----------------|
| **LinkedIn Banner** | 1584 × 396px | Personal/company profile headers | `content/graphics/linkedin-banner-[name].html` |
| **LinkedIn Post** | 1200 × 1200px | Feed posts, announcements | `content/graphics/linkedin-post-[topic].html` |
| **Webinar Promo** | 1920 × 1080px | Event promotion, presentation slides | `content/graphics/webinar-[event].html` |
| **Email Banner** | 600 × 200px | Newsletter headers, email campaigns | `content/graphics/email-banner-[topic].html` |
| **Social Story** | 1080 × 1920px | Instagram/LinkedIn stories | `content/graphics/story-[topic].html` |
| **Quote Card** | 1080 × 1080px | Quote graphics, testimonials | `content/graphics/quote-[topic].html` |

---

## Pre-Generation Steps (ALWAYS DO THIS)

Before creating ANY graphic:

### 1. Read the Design System
```
Read: .claude/skills/document-studio/design-system.md
```

### 2. Check Existing Graphics
```
Glob: content/graphics/*.html
```

### 3. Identify Required Assets
Clarify with user:
- Asset type and dimensions
- Primary text/headline
- Photos to include (if any)
- Call-to-action (if any)
- Target platform

### 4. For Updates, Read the Existing File
Read the full file to understand current structure before making changes.

---

## Design System Summary

### Color Palette
```css
--paper: #FFFFFF;        /* Main background */
--paper-alt: #FAFAF8;    /* Secondary background */
--ink-900: #0A0B0C;      /* Darkest text, headings */
--ink-700: #1F2124;      /* Body text */
--ink-500: #5C626B;      /* Secondary text */
--ink-400: #8B909A;      /* Muted text */
--line: #E5E3DE;         /* Borders, dividers */
--gold: #C5A572;         /* Accent color (use sparingly) */
--vermillion: #E03E2F;   /* Alert/CTA accent (rare) */
```

### Typography
```css
/* Headings - Editorial serif */
font-family: 'Newsreader', 'Noto Serif JP', Georgia, serif;

/* Body - Clean sans-serif */
font-family: 'Inter', system-ui, -apple-system, sans-serif;

/* Labels - Uppercase, tracked */
font-family: 'Inter', sans-serif;
font-size: 10px;
letter-spacing: 0.1em;
text-transform: uppercase;
color: var(--gold);
```

### Google Fonts Import
```html
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## Template Patterns

### Base HTML Structure

All graphics use this base structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Asset Name]</title>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --paper: #FFFFFF;
      --paper-alt: #FAFAF8;
      --ink-900: #0A0B0C;
      --ink-700: #1F2124;
      --ink-500: #5C626B;
      --ink-400: #8B909A;
      --line: #E5E3DE;
      --gold: #C5A572;
      --vermillion: #E03E2F;
    }
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      font-family: 'Inter', system-ui, sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    
    .canvas {
      width: [WIDTH]px;
      height: [HEIGHT]px;
      position: relative;
      overflow: hidden;
    }
    
    h1, h2, h3 {
      font-family: 'Newsreader', serif;
      font-weight: 500;
      color: var(--ink-900);
    }
    
    .label {
      font-family: 'Inter', sans-serif;
      font-size: 10px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--gold);
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="canvas">
    <!-- Content here -->
  </div>
</body>
</html>
```

### LinkedIn Banner (1584 × 396px)

Key elements:
- Left-aligned content with comfortable margins
- Headline in Newsreader, 36-48px
- Subtext in Inter, 16-20px
- Logo mark (N in black square) positioned appropriately
- Optional: Photo on right side, subtle background pattern

### LinkedIn Post (1200 × 1200px)

Key elements:
- Strong headline at top
- Visual hierarchy with clear sections
- Quote or statistic as focal point
- NGM branding at bottom
- Call-to-action if relevant

### Webinar Promo (1920 × 1080px)

Key elements:
- Event title prominently displayed
- Speaker photo and name
- Date, time, and platform info
- Registration CTA
- NGM branding

### Email Banner (600 × 200px)

Key elements:
- Single focused message
- Clean, scannable at small size
- Works in email clients (inline styles)

### Quote Card (1080 × 1080px)

Key elements:
- Quote as focal point
- Attribution with photo
- Minimal design, generous whitespace
- NGM logo mark

---

## Background Patterns

Use these background approaches:

### Solid
Clean paper or paper-alt background. Best for photo-heavy designs.

### Gradient
Subtle gradients from paper to paper-alt. Never jarring transitions.

```css
background: linear-gradient(135deg, var(--paper) 0%, var(--paper-alt) 100%);
```

### Dark Mode
For emphasis or variety. Use ink-900 background with white text.

```css
background: var(--ink-900);
color: white;
```

```css
h1, h2 { color: white; }
.label { color: var(--gold); }
```

### Geometric
Subtle geometric patterns using lines. Never busy or distracting.

```css
background: 
  linear-gradient(135deg, transparent 25%, var(--line) 25%, var(--line) 26%, transparent 26%),
  var(--paper);
background-size: 40px 40px;
```

---

## Photo Integration

When incorporating user photos:

### Profile Photos
- Circular crop for speaker/author photos
- 200-400px diameter depending on asset
- Subtle shadow: `box-shadow: 0 4px 20px rgba(0,0,0,0.1);`

```css
.photo-circle {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
```

### Background Photos
- Overlay with semi-transparent layer for text readability
- Position with object-fit: cover

```css
.photo-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(10,11,12,0.85) 0%, rgba(10,11,12,0.7) 100%);
}
```

### Side Photos
- Clean edges, generous spacing from text
- Consider partial overlay for depth

---

## AI-Generated Element Guidelines

When using AI image generation (via Replicate, DALL-E, etc.):

### Suitable For:
- Abstract backgrounds (gradients, textures, patterns)
- Decorative elements (shapes, lines, accents)
- Conceptual imagery (longevity, health, science themes)
- Icon-style illustrations

### Not Suitable For:
- Realistic photos of Dr. Vinjamoori (use real photos)
- Text in images (render text as HTML)
- Logos or branded elements

### Prompt Patterns:

**Abstract Background:**
> "Minimal abstract background, soft gradient from cream to warm white, subtle geometric lines, editorial design aesthetic, clean professional, 4k"

**Medical/Science Theme:**
> "Abstract representation of cellular health and longevity, minimal line art style, gold and charcoal color palette on cream background, editorial illustration"

**Decorative Element:**
> "Elegant gold decorative line pattern, minimal editorial style, isolated on transparent background"

---

## Creating Graphics

### 1. LinkedIn Banner

**Required inputs:**
- Headline text
- Subtext (optional)
- Photo (optional)

**Process:**
1. Read design system
2. Determine content layout (text-only or with photo)
3. Create HTML using LinkedIn banner template
4. Save to `content/graphics/linkedin-banner-[name].html`

**Template Reference:** `.claude/skills/graphic-design/templates/linkedin-banner.html`

### 2. LinkedIn Post

**Required inputs:**
- Main message/headline
- Supporting text
- Topic/theme

**Process:**
1. Read design system
2. Identify visual focus (quote, stat, announcement)
3. Create HTML using post template
4. Save to `content/graphics/linkedin-post-[topic].html`

**Template Reference:** `.claude/skills/graphic-design/templates/linkedin-post.html`

### 3. Webinar Promo

**Required inputs:**
- Event title
- Date and time
- Speaker name and photo
- Registration link

**Process:**
1. Read design system
2. Create HTML with event details
3. Include speaker photo with proper attribution
4. Save to `content/graphics/webinar-[event-slug].html`

**Template Reference:** `.claude/skills/graphic-design/templates/webinar-promo.html`

---

## Exporting to Images

The HTML files can be converted to PNG/JPG using:

1. **Browser Screenshot**: Open HTML in browser, take screenshot at exact dimensions
2. **Puppeteer Script**: Automated conversion using headless browser
3. **Online Tools**: Use html2canvas or similar services

To ensure correct dimensions, the `.canvas` element should have:
```css
width: [exact width]px;
height: [exact height]px;
```

---

## Quality Checklist

Before finalizing any graphic:

- [ ] Dimensions match target platform requirements
- [ ] Typography follows NGM system (Newsreader/Inter)
- [ ] Colors use NGM palette (gold sparingly)
- [ ] Text is readable at target size
- [ ] Photos have appropriate treatment (crop, shadow)
- [ ] NGM branding is present but not overwhelming
- [ ] Visual hierarchy is clear
- [ ] No placeholder text remains
- [ ] Renders correctly in browser
- [ ] Responsive considerations (if applicable)

---

## Anti-Patterns to Avoid

1. **Overusing gold** — Accent only, never large areas
2. **Busy backgrounds** — Keep patterns subtle
3. **Poor contrast** — Ensure text readability
4. **Cluttered layouts** — Embrace whitespace
5. **Generic stock imagery** — Use real photos or custom AI elements
6. **Tiny text** — Design for platform viewing size
7. **Missing branding** — Include NGM mark appropriately
8. **Inconsistent styling** — Match existing NGM materials

---

## Usage Examples

### Create a LinkedIn banner
```
Create a LinkedIn banner for Dr. Vinjamoori's profile with the headline "Turning Science Into Strategy" and subtext "Founder, Next Generation Medicine"
```

### Create a webinar promo
```
Create a webinar promo for "The Future of GLP-1s in Longevity Medicine" scheduled for January 15, 2026 at 12pm EST. Include Dr. Vinjamoori's photo.
```

### Create a quote card
```
Create a quote card with: "The future of medicine isn't just about living longer—it's about living better, longer." - Dr. Anant Vinjamoori
```

### Update existing graphic
```
Update the LinkedIn banner to change the headline to "Building the Future of Longevity Medicine"
```

