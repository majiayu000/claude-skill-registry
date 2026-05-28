---
name: screwfast
description: Astro 5 landing page with Tailwind CSS 4, Preline UI, GSAP, and Starlight docs.
---

# ScrewFast Landing Page

A versatile landing page, blog, and docs template with Astro 5, Tailwind CSS 4, Preline UI, GSAP animations, and Starlight documentation.

## Tech Stack

- **Framework**: Astro 5 with Starlight docs
- **Styling**: Tailwind CSS 4, Preline UI
- **Animation**: GSAP, Lenis smooth scroll
- **Package Manager**: npm
- **Output**: `dist` directory
- **Dev Port**: 4321

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/screwfast-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/screwfast-template.git _temp_template
mv _temp_template/* _temp_template/.* . 2>/dev/null || true
rm -rf _temp_template
```

### 2. Remove Git History (Optional)

```bash
rm -rf .git
git init
```

### 3. Install Dependencies

```bash
npm install
```

## Build

```bash
npm run build
```

Runs `astro check && astro build && node process-html.mjs` which type checks, builds, and minifies HTML.

## Deploy

### Vercel (Recommended)

```bash
vercel pull --yes -t $VERCEL_TOKEN
vercel build --prod -t $VERCEL_TOKEN
vercel deploy --prebuilt --prod --yes -t $VERCEL_TOKEN
```

### Netlify

```bash
netlify deploy --prod --dir=dist
```

## Development

```bash
npm run dev
```

Opens at http://localhost:4321

Preview production build:
```bash
npm run preview
```
