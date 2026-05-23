---
name: awwwards-landing-page
description: Designer portfolio with Locomotive Scroll, GSAP, and Framer Motion animations.
---

# Awwwards Landing Page

A stunning portfolio landing page with smooth scroll animations using Locomotive Scroll, GSAP, and Framer Motion.

## Tech Stack

- **Framework**: Next.js
- **Animation**: Locomotive Scroll, GSAP, Framer Motion
- **Package Manager**: pnpm or npm
- **Dev Port**: 3000

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/awwwards-landing-page-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/awwwards-landing-page-template.git _temp_template
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

> **CRITICAL**: For Vercel, you MUST use `vercel build --prod` then `vercel deploy --prebuilt --prod`. Never use `vercel --prod` directly.

### Vercel (Recommended)

```bash
vercel pull --yes -t $VERCEL_TOKEN
vercel build --prod -t $VERCEL_TOKEN
vercel deploy --prebuilt --prod --yes -t $VERCEL_TOKEN
```

### Netlify

```bash
netlify deploy --prod
```

## Development

```bash
npm run dev
```

Opens at http://localhost:3000

## Notes

- Static Next.js site - no environment variables needed
- Never run `npm run dev` in VM environment
