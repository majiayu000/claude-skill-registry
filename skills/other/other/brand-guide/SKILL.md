---
name: brand-guide
description: Generate and maintain brand style guides - colors, fonts, imagery, voice/tone, responsive specs. Use when documenting brand identity or creating style guide pages.
allowed-tools: Read, Write, Edit, Bash(python3 *), Grep, Glob
---

# Brand Guide Skill

Generate comprehensive brand style guides documenting colors, typography, imagery, voice/tone, and responsive design specifications.

## When to Use This Skill

Invoke this skill when you need to:
- Create a brand style guide page
- Document color palettes with hex/rgb values
- Specify typography guidelines
- Define imagery and photography style
- Establish voice and tone guidelines
- Document responsive design breakpoints
- Extract brand info from existing themes

## What This Skill Does

1. **Extracts brand data** from existing theme files (CSS, PHP)
2. **Generates HTML/Markdown** brand guide content
3. **Creates WordPress pages** with brand documentation
4. **Documents responsive behavior** at all breakpoints

## Brand Data Structure

```yaml
brand:
  name: "Brand Name"
  tagline: "Brand Tagline"
  established: 2025
  location: "City, State"

colors:
  primary:
    name: "Color Name"
    hex: "#HEXCODE"
    rgb: "rgb(r, g, b)"
    usage: "When to use this color"
  secondary:
    name: "Color Name"
    hex: "#HEXCODE"
    usage: "When to use this color"
  accent:
    name: "Color Name"
    hex: "#HEXCODE"
    usage: "When to use this color"

typography:
  primary_font: "Font Family"
  weights: [300, 400, 700]
  headings:
    style: "font-light tracking-tighter"
    sizes:
      h1: "text-5xl md:text-9xl"
      h2: "text-4xl md:text-5xl"
      h3: "text-xl"
  body:
    style: "font-light leading-relaxed"
    size: "text-lg"

imagery:
  style: "Professional/Candid/etc"
  treatment: "Filters, overlays"
  subjects: ["Subject 1", "Subject 2"]
  aspect_ratios:
    hero: "16:9"
    card: "4:5"
    square: "1:1"

voice:
  personality: ["Adjective 1", "Adjective 2", "Adjective 3"]
  tone: "Description of tone"
  examples:
    do: ["Example of correct copy"]
    dont: ["Example of incorrect copy"]

responsive:
  breakpoints:
    mobile: "< 768px"
    tablet: "768px - 1024px"
    desktop: "> 1024px"
  behaviors:
    navigation: "Hamburger on mobile, full on desktop"
    hero: "Stacked on mobile, side-by-side on desktop"
```

## CSR Development Brand

### Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| CSR Cream | #EDEAE3 | rgb(237, 234, 227) | Backgrounds, cards, header |
| CSR Dark Blue | #07254B | rgb(7, 37, 75) | Text, headings, footer, CTAs |
| CSR Light Blue | #B4C1D1 | rgb(180, 193, 209) | Hover states, labels, accents |

### Typography

**Primary Font:** Manrope (Google Fonts)

| Element | Style | Size (Mobile) | Size (Desktop) |
|---------|-------|---------------|----------------|
| H1 | font-light tracking-tighter | text-5xl | text-9xl |
| H2 | font-light | text-4xl | text-5xl |
| H3 | font-light | text-xl | text-xl |
| Body | font-light leading-relaxed | text-lg | text-lg |
| Label | font-bold uppercase tracking-widest | text-xs | text-xs |

### Imagery

- **Style:** Professional architectural photography
- **Treatment:** Subtle grayscale (20%), dark blue overlay (10% opacity)
- **Subjects:** Modern buildings, Miami skyline, luxury interiors, construction
- **Aspect Ratios:**
  - Hero: 16:9 (video) or full height
  - Portfolio cards: 4:5
  - Team photos: 1:1

### Voice & Tone

**Personality:** Professional, Sophisticated, Trustworthy, Visionary

**Tone:** Confident but not arrogant, elegant but accessible

**Do:**
- "CSR acquires and develops real estate assets that create long-term value"
- "Built on Legacy"
- "Elevating the standard of living through thoughtful design"

**Don't:**
- Overly casual language
- Excessive exclamation points
- Industry jargon without explanation

### Responsive Breakpoints

| Breakpoint | Width | Tailwind Class |
|------------|-------|----------------|
| Mobile | < 768px | Default (no prefix) |
| Tablet | 768px - 1024px | md: |
| Desktop | > 1024px | lg: |

## Scripts

### extract-brand.py
Extracts brand data from theme CSS/PHP files.

**Usage:**
```bash
python3 /root/.claude/skills/brand-guide/scripts/extract-brand.py \
  --theme-path /path/to/theme \
  --output /path/to/brand-data.yaml
```

### generate-guide.py
Generates brand guide HTML from brand data.

**Usage:**
```bash
python3 /root/.claude/skills/brand-guide/scripts/generate-guide.py \
  --brand-data /path/to/brand-data.yaml \
  --output /path/to/brand-guide.html
```

### color-utils.py
Utilities for color manipulation and contrast checking.

**Usage:**
```bash
python3 /root/.claude/skills/brand-guide/scripts/color-utils.py \
  --hex "#07254B" \
  --check-contrast "#EDEAE3"
```

## Templates

### brand-guide-page.html
Full brand guide page template with all sections.

### color-palette.html
Color palette section showing swatches with codes.

### typography.html
Typography section with font samples at all sizes.

### imagery.html
Imagery guidelines with example treatments.

### voice-tone.html
Voice and tone section with do's and don'ts.

### responsive.html
Responsive design specs with breakpoint documentation.

## Workflow

### Create Brand Guide for Existing Site

1. **Extract brand data:**
   ```bash
   python3 scripts/extract-brand.py --theme-path /path/to/theme
   ```

2. **Review and enhance** the extracted data (add voice/tone, etc.)

3. **Generate guide:**
   ```bash
   python3 scripts/generate-guide.py --brand-data brand.yaml
   ```

4. **Create WordPress page** using wordpress-admin skill

### Create Brand Guide from Scratch

1. Fill out brand data template (see structure above)
2. Generate guide HTML
3. Create WordPress page
4. Add screenshots at each breakpoint

## Integration with wordpress-admin

After generating a brand guide, create it as a WordPress page:

```bash
# Create the page
docker exec wordpress-local-wordpress-1 wp post create \
  --post_type=page \
  --post_title="Brand Style Guide" \
  --post_name="brand-guide" \
  --post_status="publish" \
  --post_content="$(cat brand-guide.html)" \
  --allow-root

# Set SEO
docker exec wordpress-local-wordpress-1 wp post meta update <ID> _yoast_wpseo_focuskw "CSR brand style guide" --allow-root
docker exec wordpress-local-wordpress-1 wp post meta update <ID> _yoast_wpseo_metadesc "Complete brand style guide for CSR Real Estate including colors, typography, imagery guidelines, and voice specifications." --allow-root
```

## Reference Files

- **CSR Theme:** /root/csrdevelopment.com/csrdevelopment.com/public_html/wp-content/themes/csr-theme/
- **CSR Style CSS:** /root/csrdevelopment.com/csrdevelopment.com/public_html/wp-content/themes/csr-theme/style.css
- **CSR Logo:** /root/csrdevelopment.com/csrdevelopment.com/public_html/wp-content/themes/csr-theme/assets/images/csr-logo.svg

## Examples

See `/root/.claude/skills/brand-guide/examples/csr-brand-guide.md` for a complete CSR Development brand guide example.
