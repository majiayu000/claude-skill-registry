---
name: slides-as-code
description: |
  Create presentation slides as standalone HTML files with automated PNG export. Use when users ask to: create slides, build a deck, make a presentation, design slides, export slides to images, or work with HTML-based presentations. Triggers: "create slides", "make a presentation", "build a deck", "slide deck", "export slides", "slides as code".
---

# Slides as Code

Create presentation decks as standalone HTML files (1920x1080). Each slide is self-contained with embedded CSS. Preview in browser, export to PNG/PPTX.

## Workflow

**Always follow this sequence when creating a deck:**

1. Initialize project in user's working directory (NOT inside the skill folder)
2. Create all slide HTML files in `<project>/html/`
3. Update `<project>/html/viewer.html` slides array
4. **Run export**: `cd <project> && npm run build`

**IMPORTANT:** After creating slides, always run `npm run build` to generate PNG and PPTX exports. Do not skip this step.

## Quick Start

Initialize a new deck **in the user's current working directory**:

```bash
# CORRECT: Run from user's cwd, use absolute path to script
bash ~/.claude/skills/slides-as-code/scripts/init-slideshow.sh my-deck

# WRONG: Don't cd into skill folder first
# cd ~/.claude/skills/slides-as-code && bash scripts/init-slideshow.sh my-deck
```

This creates `my-deck/` in the current directory with all files ready.

Auto-installs dependencies. Takes ~30 seconds.

## Design Philosophy

**Don't look AI-generated.** Think Apple iOS, Linear, Vercel - professionally designed by outlier designers.

### NEVER use:
- Emoji icons (🚀 ✨ 💡 🎯) - instant AI-generated signal
- Clip art or stock icons
- Colored background boxes for every section
- Generic headers ("Our Solution", "Key Benefits")
- Placeholder text or fake code

### ALWAYS use:
- **Typography as design** - Let fonts do the work, not decorations
- **Whitespace** - Generous spacing is sophistication
- **Restrained color** - Gradient on 1-2 key words only
- **Real content** - Actual code, specific numbers, concrete claims
- **Symbols over icons** - Use → ✓ ✕ + = as visual elements

### Quality bar:
If a slide looks like it could be from a free template or AI generator, redesign it. Aim for the aesthetic of Linear's changelog, Vercel's marketing, or Apple keynotes.

For detailed styling: See [references/design-guide.md](references/design-guide.md)
For layout patterns: See [references/slide-patterns.md](references/slide-patterns.md)

## Typography

```css
/* Three fonts, each with a purpose */
font-family: 'Space Grotesk', sans-serif;  /* Titles, UI */
font-family: 'Lora', serif;                 /* Body text */
font-family: 'JetBrains Mono', monospace;   /* Code */
```

Title: 52-72px, weight 300 (light = sophisticated), letter-spacing -0.02em

## Colors

```css
/* Gradient - use sparingly */
background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%);

/* Text hierarchy */
#1a1a1a  /* Headings */
#333333  /* Body */
#555555  /* Subtle */
#888888  /* Muted */

/* Surfaces */
#ffffff  /* Background */
#fafafa  /* Light cards */
#1a1a1a  /* Dark cards/code */
```

## Slide Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Slide N - Specific Title</title>
    <link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;600&family=Space+Grotesk:wght@300;400;500;600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { margin: 0; padding: 0; overflow: hidden; }
        body {
            font-family: 'Space Grotesk', sans-serif;
            background: #ffffff;
            width: 1920px;
            height: 1080px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
</head>
<body>
    <!-- Content -->
</body>
</html>
```

## Common Elements

**Gradient text:**
```css
.gradient {
    background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 500;
}
```

**Arrow bullets:**
```css
.bullets li::before { content: "→"; color: #8B5CF6; }
```

**Check/X bullets:**
```css
.gained li::before { content: "✓"; color: #8B5CF6; }
.eliminated li::before { content: "✕"; color: #EC4899; }
```

**Code box:**
```css
.code-box {
    background: #1a1a1a;
    border-radius: 10px;
    padding: 32px 40px;
}
```

## Viewer

Update slides array in `html/viewer.html`:
```javascript
const slides = ['slide1.html', 'slide2.html', 'slide3.html'];
```

Open in browser, use arrow keys to navigate.

## Export

```bash
npm run export    # HTML → PNG (2x resolution)
npm run pptx      # PNG → PPTX
npm run build     # Full pipeline
```
