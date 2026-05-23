---
name: ia-presenter-themes
description: This skill should be used when creating, modifying, or troubleshooting custom themes for iA Presenter.
---

# iA Presenter Theme Creation

## Overview

Create or edit custom iA Presenter themes that control the visual appearance of presentations, including typography, colours, layouts, backgrounds, and responsive behaviour. Themes consist of CSS files, JSON configuration files, and optional custom fonts or images.

## Core Concepts

### Theme Structure

Every iA Presenter theme consists of:

1. **`template.json`** - Theme metadata (name, author, CSS filename, fonts)
2. **`presets.json`** - Colour presets for light/dark modes and gradients
3. **`theme.css`** - CSS rules for layouts, typography, and styling
4. **Custom fonts** (optional) - `.woff2` font files
5. **Images/assets** (optional) - Background images or other visual assets

### Theme Location

Themes are stored in:
```
~/Library/Containers/net.ia.presenter/Data/Library/Application Support/iA Presenter/Themes/
```

### Development Workflow

1. Create theme structure in ~/Library/Containers/net.ia.presenter/Data/Library/Application Support/iA Presenter/Themes/<YourTheme>
2. Created / edit CSS/JSON files
3. Ask the user to:
   1. Close and reopen iA Presenter to see changes
   2. Test in both light and dark modes
   3. Validate across different layouts

## Task Decision Tree

When the user requests theme work, determine the appropriate task:

### Creating a New Theme

**Trigger**: User wants to create a theme from scratch
**Steps**:
1. Clarify requirements (colour palette, fonts, layout preferences)
2. Choose approach: starter templates or custom build
3. Load `references/quick_reference.md` for CSS classes
4. Create `template.json`, `presets.json`, and CSS file
5. Write files to theme directory
6. Provide testing checklist

**Resources**: `assets/starter-theme/*`, `references/quick_reference.md`

### Modifying an Existing Theme

**Trigger**: User wants to customise an existing theme
**Steps**:
1. Read the existing theme files
2. Identify what needs modification
3. Load relevant references based on changes
4. Edit the appropriate files
5. Validate changes

**Resources**: `references/official_guide.md`, `references/quick_reference.md`

### Adding Custom Fonts

**Trigger**: User wants to add custom typography
**Steps**:
1. Verify font files (`.woff2` format) are available
2. Add `@font-face` declarations to CSS
3. Update `template.json` with display names
4. Update `presets.json` with CSS font family names
5. Confirm font files are in theme directory

**Resources**: `references/official_guide.md` (Custom Fonts section)

### Implementing Backgrounds

**Trigger**: User wants gradients, images, or SVG backgrounds
**Steps**:
1. Determine background type (image, SVG, gradient)
2. For gradients: Update `presets.json`
3. For images/SVG: Add to CSS with proper selectors
4. Test in both light and dark modes
5. Validate across layouts

**Resources**: `references/official_guide.md` (Backgrounds section), `references/advanced_techniques.md`

### Troubleshooting

**Trigger**: Theme not working as expected
**Steps**:
1. Identify the issue category
2. Load `references/advanced_techniques.md` for debugging tips
3. Apply debugging borders if needed
4. Validate JSON syntax
5. Check common issues (SVG colours, font paths, selectors)

**Resources**: `references/advanced_techniques.md`

## Common Customisations

### Typography

Modify heading sizes, line heights, and font weights. The starter CSS includes a typography section with heading sizes for both desktop and mobile. Target headings within layouts:

```css
section > :not([class*="layout-"]) h1,
[class*="layout-"] > div h1 {
  font-size: 2.986em;
  line-height: 1;
}
```

### Layout Alignment

Available layouts and their CSS classes:

| Layout      | Container Class          | Content Class         |
|-------------|--------------------------|-----------------------|
| Cover       | `.cover-container`       | `.layout-cover`       |
| Title       | `.title-container`       | `.layout-title`       |
| Section     | `.section-container`     | `.layout-section`     |
| Split       | `.v-split-container`     | `.layout-v-split`     |
| Grid        | `.grid-container`        | `.layout-grid`        |
| Caption     | `.caption-container`     | `.layout-caption`     |
| Image Title | `.title-image-container` | `.layout-title-image` |
| Default     | `.default-container`     | `.layout-default`     |

To align content, target the inner `div` of each layout:

```css
.layout-cover > div {
  justify-content: center;  /* vertical: flex-start, center, flex-end */
  align-items: center;      /* horizontal: flex-start, center, flex-end */
}
```

### Backgrounds

**Image backgrounds**:
```css
.backgrounds .cover-container {
  background-image: url("cover-bg.jpg");
  background-size: cover;
  background-position: center;
}
```

**Inline SVG** (use `rgb()` colours, not hex):
```css
.backgrounds .v-split-container {
  background-image: url('data:image/svg+xml;utf8,<svg>...</svg>');
}
```

**Gradients** (defined in `presets.json`, not CSS):
```json
{
  "LightBgGradient": ["#c7e7ff", "#f0c8ff", "#ffdada", "#ffebb2"],
  "DarkBgGradient": ["#15354c", "#3e154c", "#4c2828", "#4c3900"]
}
```

### Light and Dark Modes

Configure colours for both modes in `presets.json`:
```json
{
  "Appearance": "light",
  "DarkBodyTextColor": "#000000",
  "LightBodyTextColor": "#ffffff",
  "DarkTitleTextColor": "#000000",
  "LightTitleTextColor": "#ffffff",
  "DarkBackgroundColor": "#1a1a1a",
  "LightBackgroundColor": "#ffffff"
}
```

**CRITICAL: Understanding iA Presenter Colour Naming**

The colour field names in `presets.json` can be counter-intuitive. They refer to the COLOUR OF THE ELEMENT, not the mode:

- **`DarkBodyTextColor`** = Dark-coloured text (e.g. #000000 black)
  - Used for text ON light backgrounds in light mode

- **`LightBodyTextColor`** = Light-coloured text (e.g. #ffffff white)
  - Used for text ON dark backgrounds in dark mode

- **`DarkBackgroundColor`** = Dark background colour (e.g. #1a1a1a)
  - Used as background in dark mode

- **`LightBackgroundColor`** = Light background colour (e.g. #ffffff)
  - Used as background in light mode

**Example - For good contrast:**
```json
{
  "DarkBodyTextColor": "#000000",      // Black text for light backgrounds
  "LightBodyTextColor": "#ffffff",     // White text for dark backgrounds
  "DarkBackgroundColor": "#1a1a1a",    // Dark grey background
  "LightBackgroundColor": "#ffffff"    // White background
}
```

In light mode: Uses LightBackgroundColor (#ffffff) with DarkBodyTextColor (#000000)
In dark mode: Uses DarkBackgroundColor (#1a1a1a) with LightBodyTextColor (#ffffff)

**Common Mistake:** Swapping DarkBodyTextColor and LightBodyTextColor, which results in invisible text.

Force appearance for specific layouts in `template.json`:
```json
"Layouts": [
  {
    "Name": "Cover",
    "Classes": "dark"
  }
]
```

### Responsive Design

Default CSS applies to mobile. Use media queries for larger screens:

```css
/* Mobile (default) */
@media (max-width: 639px) {
  [class*="layout-"] > div h1 {
    font-size: 2.074em;
  }
}

/* Desktop/Tablet */
@media (min-width: 768px) {
  /* Desktop-specific styles */
}
```

## Troubleshooting Guide

### Text Not Visible (Invisible Text Issue)

**Symptom**: Text appears invisible in both light and dark modes

**Cause**: Incorrect colour assignments in `presets.json`. The colour naming refers to the colour of the element, not the mode.

**Solution**: Ensure colours are assigned correctly:
```json
{
  "DarkBodyTextColor": "#000000",      // Dark text (for light backgrounds)
  "LightBodyTextColor": "#ffffff",     // Light text (for dark backgrounds)
  "DarkBackgroundColor": "#1a1a1a",    // Dark background
  "LightBackgroundColor": "#ffffff"    // Light background
}
```

**Common Mistake**: Setting `DarkBodyTextColor` to a light colour like "#ffffff" - this puts white text on a white background in light mode.

### Inline SVG Broken

Use `rgb(255,0,0)` instead of `#FF0000` in inline SVG. Hex colours break inline SVG in CSS.

### Fonts Not Loading

Verify:
1. Font files (`.woff2`) are in the theme directory
2. `@font-face` declarations use correct file paths
3. `template.json` has display font names
4. `presets.json` has CSS font family names

### Layout Alignment Issues

Target the inner `div` of layouts:
```css
.layout-cover > div { /* alignment properties */ }
```

Not the container:
```css
.cover-container { /* this won't align content */ }
```

### Debugging Technique

Use coloured borders during development:

```css
.cover-container { border: 5px solid red; }
.layout-cover > div { border: 5px dashed red; }
.title-container { border: 5px solid blue; }
.layout-title > div { border: 5px dotted blue; }
```

Remove these before final distribution.

## Validation Checklist

When creating or modifying themes:

- [ ] All required files exist (`template.json`, `presets.json`, CSS file)
- [ ] JSON files have valid syntax
- [ ] Tested in both light and dark modes
- [ ] Responsive behaviour verified at different viewport sizes
- [ ] Custom fonts load correctly (if applicable)
- [ ] All layouts tested (cover, title, section, split, grid, caption, image title, default)
- [ ] Gradients render smoothly (if applicable)
- [ ] Backgrounds display correctly (if applicable)
- [ ] Debugging borders and comments removed

## Best Practices

1. **Start with templates** - Use `assets/starter-theme/*` for consistency
2. **Reference documentation** - Load `references/quick_reference.md` for CSS classes
3. **Test thoroughly** - Verify in light/dark modes and all layouts
4. **Use semantic names** - Name colours and presets descriptively
5. **Comment CSS** - Add comments for complex or non-obvious rules
6. **Mobile-first** - Default styles for mobile, enhance for desktop
7. **Consistent spacing** - Use consistent units (em, rem) for scalability
8. **Minimal overrides** - Only override what's necessary
9. **British English** - Use British spelling in all comments and documentation

## Key Reminders

- **CRITICAL: Colour naming** - DarkBodyTextColor = dark-coloured text (for light backgrounds), LightBodyTextColor = light-coloured text (for dark backgrounds). DO NOT swap these!
- **No hot reload on theme creation** - The user must close and reopen iA Presenter when you first create a theme, but subsequent updates will apply on the fly.
- **Inner div targeting** - Alignment rules target `.layout-* > div`, not the container
- **Inline SVG colours** - Use `rgb()` format, not hexadecimal
- **Mobile-first** - Default CSS applies to mobile, add `@media (min-width: 768px)` for desktop
- **Both modes** - Always configure and test light and dark appearances
- **Grid modifiers** - Grid layouts have `.grid-items-2`, `.grid-items-3`, etc. classes
- **British spelling** - Use "colour", "centre", "customise" in all content
- **Minimal CSS overrides** - Avoid setting explicit colours in CSS for text/backgrounds - let presets.json handle them
- **Update placeholders** - Update any placeholder content in the template.json, theme.css, presets.json files
- If you need clarification on the theme you may ask the user for more details about their preferences and requirements.

## Resources

### references/

Reference documentation to load into context as needed:

- **`official_guide.md`** - Complete official iA Presenter theme documentation covering all layouts, CSS classes, font configuration, backgrounds, gradients, and appearances
- **`quick_reference.md`** - Condensed reference with CSS classes, selectors, file structure, and common patterns for quick lookup
- **`advanced_techniques.md`** - Advanced techniques including centring content, debugging borders, inline SVG backgrounds, and workflow tips

Load progressively:
- **Always useful**: `quick_reference.md` (CSS classes, structure)
- **For new themes**: `assets/starter-theme/*` files
- **For complex customisation**: `official_guide.md`
- **For debugging**: `advanced_techniques.md`

### assets/

Starter theme templates in `assets/starter-theme/`:

- **`template.json`** - Minimal theme metadata template
- **`presets.json`** - Colour preset template with sensible defaults
- **`theme.css`** - Comprehensive CSS starter with commented sections for typography, layouts, backgrounds, headers/footers, responsive design
- **`README.md`** - Guide for using the starter templates

Use these templates as a starting point for new themes. Copy and customise based on user requirements.
