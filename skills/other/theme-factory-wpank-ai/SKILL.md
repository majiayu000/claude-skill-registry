---
name: theme-factory
model: fast
description: Curated collection of professional color and typography themes for styling artifacts — slides, docs, reports, landing pages. Use when applying visual themes to presentations, generating themed content, or creating custom brand palettes. Triggers on theme, color palette, font pairing, slide styling, presentation theme, brand colors.
---

# Theme Factory

Apply consistent, professional styling to any artifact using curated themes with color palettes and font pairings.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install theme-factory
```


---

## When to Use

- Styling slide decks, reports, or documents with a cohesive visual identity
- Applying color palettes and font pairings to HTML pages or landing pages
- Choosing a pre-built theme for quick professional styling
- Creating a custom theme when none of the presets fit

---

## How to Use

### Step 1: Present Available Themes

Show the user the 10 available themes with their descriptions:

| # | Theme | Vibe | Best For |
|---|-------|------|----------|
| 1 | Ocean Depths | Professional, calming maritime | Corporate, financial, consulting |
| 2 | Sunset Boulevard | Warm, vibrant energy | Creative pitches, marketing, events |
| 3 | Forest Canopy | Natural, grounded earth tones | Environmental, sustainability, wellness |
| 4 | Modern Minimalist | Clean, contemporary grayscale | Tech, architecture, design showcases |
| 5 | Golden Hour | Rich, warm autumnal | Hospitality, lifestyle, artisan brands |
| 6 | Arctic Frost | Cool, crisp precision | Healthcare, technology, clean tech |
| 7 | Desert Rose | Soft, sophisticated dusty tones | Fashion, beauty, interior design |
| 8 | Tech Innovation | Bold, high-contrast modern | Startups, software launches, AI/ML |
| 9 | Botanical Garden | Fresh, organic vibrancy | Food, garden, natural products |
| 10 | Midnight Galaxy | Dramatic, cosmic depth | Entertainment, gaming, luxury brands |

### Step 2: Get User Selection

Ask which theme to apply. Wait for explicit confirmation before proceeding.

### Step 3: Apply the Theme

1. Read the selected theme file from `themes/` directory
2. Apply colors and fonts consistently throughout the artifact
3. Ensure proper contrast and readability
4. Maintain the theme's visual identity across all pages/slides

---

## Theme File Structure

Each theme in `themes/` follows this format:

```markdown
# Theme Name

Description of the visual mood and inspiration.

## Color Palette
- **Primary Dark**: `#hex` — Usage description
- **Accent**: `#hex` — Usage description
- **Secondary**: `#hex` — Usage description
- **Light/Background**: `#hex` — Usage description

## Typography
- **Headers**: Font family
- **Body Text**: Font family

## Best Used For
Context and audience descriptions.
```

---

## Applying Themes to Different Artifacts

### Slide Decks

- **Background**: Use the primary dark color for title slides, light color for content slides
- **Headers**: Apply the header font in the accent color
- **Body text**: Use the body font in the primary dark color on light backgrounds
- **Accents**: Use accent/secondary colors for charts, highlights, dividers

### HTML / Landing Pages

```css
:root {
  --theme-primary: #hex;     /* From theme's primary dark */
  --theme-accent: #hex;      /* From theme's accent color */
  --theme-secondary: #hex;   /* From theme's secondary */
  --theme-bg: #hex;          /* From theme's light/background */
  --theme-font-heading: "Theme Header Font", sans-serif;
  --theme-font-body: "Theme Body Font", sans-serif;
}
```

### Documents / Reports

- **Cover page**: Primary dark background with light text
- **Section headers**: Accent color with header font
- **Body**: Body font on light background
- **Charts/tables**: Use accent and secondary for data series
- **Callout boxes**: Secondary color as background with primary text

---

## Creating a Custom Theme

When no preset fits, generate a custom theme:

1. **Gather input** — Ask about the brand, audience, mood, and context
2. **Select palette** — Choose 4 colors that form a cohesive palette:
   - One dark anchor color (backgrounds, text)
   - One primary accent (emphasis, CTAs)
   - One secondary accent (supporting elements)
   - One light/neutral (backgrounds, whitespace)
3. **Pair fonts** — Choose complementary heading and body fonts:
   - Heading: distinctive, personality-driven
   - Body: readable, clean
4. **Validate contrast** — Ensure WCAG AA compliance for text on backgrounds
5. **Name the theme** — Give it an evocative name describing the visual feeling
6. **Document** — Write a theme file matching the standard format
7. **Review** — Show the theme for approval before applying

### Palette Harmony Rules

- **Complementary**: Colors opposite on the wheel (high contrast)
- **Analogous**: Colors adjacent on the wheel (harmonious)
- **Triadic**: Three evenly spaced colors (vibrant but balanced)
- **Split-complementary**: Base + two colors adjacent to its complement (versatile)

---

## Contrast Guidelines

Ensure readability when applying any theme:

| Combination | Minimum Ratio | WCAG Level |
|-------------|--------------|------------|
| Body text on background | 4.5:1 | AA |
| Large text (18px+) on background | 3:1 | AA |
| UI components / borders | 3:1 | AA |
| Enhanced readability | 7:1 | AAA |

Test accent colors against both light and dark backgrounds before finalizing.

---

## Available Themes

All theme definitions are in the `themes/` directory:

- [themes/ocean-depths.md](themes/ocean-depths.md)
- [themes/sunset-boulevard.md](themes/sunset-boulevard.md)
- [themes/forest-canopy.md](themes/forest-canopy.md)
- [themes/modern-minimalist.md](themes/modern-minimalist.md)
- [themes/golden-hour.md](themes/golden-hour.md)
- [themes/arctic-frost.md](themes/arctic-frost.md)
- [themes/desert-rose.md](themes/desert-rose.md)
- [themes/tech-innovation.md](themes/tech-innovation.md)
- [themes/botanical-garden.md](themes/botanical-garden.md)
- [themes/midnight-galaxy.md](themes/midnight-galaxy.md)

---

## NEVER Do

- **Apply a theme without confirmation** — always get explicit user selection
- **Mix colors from different themes** — each theme is a cohesive unit
- **Ignore contrast ratios** — readability trumps aesthetics
- **Use accent colors for large text blocks** — accents are for emphasis only
- **Skip font pairing** — headers and body fonts must complement each other
- **Hardcode theme values** — use CSS variables for easy theme switching

---

## Related Skills

- [design-system-patterns](../design-system-patterns/) — Token architecture and theming infrastructure
- [distinctive-design-systems](../distinctive-design-systems/) — Aesthetic documentation and unique visual identity
