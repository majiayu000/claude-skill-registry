---
name: astrowind
description: Astro 5.0 + Tailwind CSS landing page with blog, dark mode, and perfect PageSpeed scores.
---

# AstroWind Template

A production-ready Astro 5.0 + Tailwind CSS template with perfect PageSpeed scores, dark mode, blog with RSS, and SEO optimization.

## Tech Stack

- **Framework**: Astro 5.0 with MDX support
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **Features**: Dark mode, RSS, SEO, Blog
- **Package Manager**: npm
- **Output**: `dist` directory
- **Dev Port**: 4321

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/astrowind-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/astrowind-template.git _temp_template
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

## Configuration

Edit `src/config.yaml` to customize:
- Site name, description, and metadata
- Navigation links
- Social media links
- Analytics settings
