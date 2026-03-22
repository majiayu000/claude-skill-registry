---
name: rebrand
description: Applies brand customization across the entire site — colors, fonts, logos, metadata, and social images. Use when rebranding, changing the site identity, or applying a new theme.
disable-model-invocation: true
---

Walk the user through a complete rebranding of the Website Foundation template.

## Steps

### 1. Gather Brand Information

Ask the user for:
- **Brand name** (e.g., "Acme Corp")
- **Tagline** (one-line description)
- **Contact email** (e.g., "hello@acme.com")
- **Site URL** (e.g., "https://acme.com")
- **Accent color** (optional — e.g., "ocean blue", "#3b82f6", or an OKLCH value)

### 2. Update Configuration Files

- **`astro.config.mjs`** — Change `site` to the new URL
- **`wrangler.jsonc`** — Change `name` to the new project name (kebab-case), update `destination_address` to the new contact email
- **`package.json`** — Change `name` field to match

### 3. Update Text Content

- **`src/layouts/Base.astro`** — Update the default `description` prop (line 15)
- **`src/components/Header.astro`** — Update the logo `alt` text (line 20)
- **`src/components/Footer.astro`** — Update copyright text (line 10) and contact email (line 13)
- **`src/pages/index.astro`** — Update the hero `<h1>` heading (line 27) and description paragraph (line 29-31)
- **`src/pages/blog/index.astro`** — Update the page title in `<Base>` (line 15)

### 4. Update Visual Identity (if accent color provided)

- **`src/styles/global.css`** — Add accent color tokens in the `@theme` block:
  ```css
  --color-accent-600: oklch(50% 0.18 <hue>);
  --color-accent-500: oklch(60% 0.18 <hue>);
  --color-accent-400: oklch(70% 0.15 <hue>);
  ```

### 5. Note Asset Replacements

Tell the user they should replace these files with their own assets:
- `public/favicon.svg` — Browser tab icon (SVG)
- `public/favicon.ico` — Fallback favicon
- `public/apple-icon.png` — Apple touch icon (180x180)
- `public/wave-artisan-logo.svg` — Header logo (update `src` in Header.astro if filename changes)
- `public/opengraph.png` — Social media preview image (1200x630)
- `public/fonts/` — Font files (if changing fonts, update `global.css` and `Base.astro` preload tags)

### 6. Verify

Run all checks to confirm nothing broke:

```bash
bun run check && bun run test && bun run build
```

Report the results to the user.
