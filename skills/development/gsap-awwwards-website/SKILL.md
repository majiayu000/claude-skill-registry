---
name: gsap-awwwards-website
description: SPYLT product landing with GSAP scroll animations, React 19, and Tailwind CSS 4.
---

# GSAP Awwwards Website

A stunning product landing page with GSAP scroll animations, modern React 19 architecture, and Tailwind CSS 4 styling.

## Tech Stack

- **Framework**: React 19
- **Build Tool**: Vite
- **Animation**: GSAP
- **Styling**: Tailwind CSS 4
- **Package Manager**: npm
- **Output**: `dist` directory
- **Dev Port**: 5173

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/gsap-awwwards-website-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/gsap-awwwards-website-template.git _temp_template
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

Creates a production build in the `dist/` directory.

## Deploy

> **CRITICAL**: For Vercel, you MUST use `vercel build --prod` then `vercel deploy --prebuilt --prod`. Never use `vercel --prod` directly.

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

Opens at http://localhost:5173

## Notes

- Static React site - no environment variables needed
- Never run `npm run dev` in VM environment
