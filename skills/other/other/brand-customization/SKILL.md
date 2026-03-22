---
name: brand-customization
description: Rebrand the site with custom name, colors, fonts, logo, and identity. Modify all touchpoints from site metadata to visual styling. Use when the user mentions "rebrand", "customize", "change colors", "change font", "change logo", "change name", "accent color", "theme", or "dark mode".
---

# Brand Customization

Rebrand Website Foundation by modifying these touchpoints:

## Site Metadata

- **`astro.config.mjs`** — Change `site` to your production URL
- **`wrangler.jsonc`** — Change `name` to your project name, update `destination_address`
- **`package.json`** — Change `name` field
- **`Base.astro`** — Update default `description` prop

## Visual Identity

- **Favicon** — Replace `public/favicon.svg`, `public/favicon.ico`, `public/apple-icon.png`
- **Logo** — Replace `public/wave-artisan-logo.svg`, update `Header.astro` `alt` text and `src`
- **OpenGraph image** — Replace `public/opengraph.png` (1200x630 recommended)

## Text Content

- **`Header.astro`** — Logo `alt` text (line 20)
- **`Footer.astro`** — Copyright text and contact email (lines 10, 13)
- **`index.astro`** — Hero heading and description (lines 27-31)
- **`Base.astro`** — Default description in Props (line 15)

## Colors

Edit `src/styles/global.css` to customize the OKLCH gray palette or add accent colors. See [color system reference](references/color-system.md).

## Fonts

Replace the variable font files in `public/fonts/` and update the `@font-face` declarations in `global.css`. See [typography reference](references/typography.md).

## After Rebranding

Run verification to ensure nothing broke:

```bash
bun run check && bun run test && bun run build
```
