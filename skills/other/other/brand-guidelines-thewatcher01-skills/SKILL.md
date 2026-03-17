---
name: brand-guidelines
description: Applies consistent brand colors, typography, and visual identity to any output (documents, slides, web pages, components). Use when brand colors, style guidelines, visual formatting, or company design standards need to be applied.
---

# Brand Styling System

## Overview

This skill provides a framework for applying consistent brand identity across all outputs. Define your brand once, apply everywhere.

**Keywords**: branding, corporate identity, visual identity, styling, brand colors, typography, visual formatting, visual design, theming

## How to Use

### 1. Define Your Brand (or use the default)

If no brand is specified, ask the user for their brand guidelines. A complete brand definition includes:

```yaml
brand:
  name: "Your Brand"
  colors:
    primary:
      dark: "#141413"      # Primary text / dark backgrounds
      light: "#faf9f5"     # Light backgrounds / text on dark
    neutral:
      mid: "#b0aea5"       # Secondary elements
      light: "#e8e6dc"     # Subtle backgrounds
    accent:
      primary: "#d97757"   # Primary accent (CTAs, highlights)
      secondary: "#6a9bcc" # Secondary accent (links, info)
      tertiary: "#788c5d"  # Tertiary accent (success, nature)
  typography:
    headings:
      font: "Poppins"
      fallback: "Arial, sans-serif"
      min_size: "24pt"
    body:
      font: "Lora"
      fallback: "Georgia, serif"
```

### 2. Apply to Outputs

Once brand is defined, apply consistently to:
- **Slides/Presentations** (python-pptx): Use RGBColor for precise matching
- **Web pages/Components**: Use CSS custom properties
- **Documents**: Apply font and color hierarchy
- **Diagrams**: Use accent color cycling

## Application Rules

### Typography
- Headings (24pt+): Use heading font
- Body text: Use body font
- Auto-fallback if custom fonts unavailable
- Preserve text hierarchy and formatting

### Colors
- Dark backgrounds → light text, light backgrounds → dark text
- Accent colors cycle through primary → secondary → tertiary for variety
- Maintain contrast ratios (WCAG AA minimum)
- Non-text shapes use accent colors

### CSS Variables Template

```css
:root {
  --brand-dark: #141413;
  --brand-light: #faf9f5;
  --brand-neutral: #b0aea5;
  --brand-neutral-light: #e8e6dc;
  --brand-accent-1: #d97757;
  --brand-accent-2: #6a9bcc;
  --brand-accent-3: #788c5d;
  --font-heading: 'Poppins', Arial, sans-serif;
  --font-body: 'Lora', Georgia, serif;
}
```

## Technical Details

### Font Management
- Use system-installed fonts when available
- Provide automatic fallbacks for cross-platform compatibility
- No font installation required — works with existing system fonts

### Color Application
- Use RGB/hex values for precise brand matching
- For python-pptx: use `RGBColor` class
- For web: use CSS custom properties
- Maintain color fidelity across systems
