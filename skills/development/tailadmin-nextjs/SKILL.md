---
name: tailadmin-nextjs
description: Next.js 16 admin dashboard with 30+ components, Tailwind CSS 4, ApexCharts, dark mode.
---

# TailAdmin Next.js

A free Next.js admin dashboard with 30+ components, dark mode, ApexCharts, calendar, forms, and tables.

## Tech Stack

- **Framework**: Next.js 16
- **React**: React 19
- **Styling**: Tailwind CSS 4
- **Charts**: ApexCharts
- **Package Manager**: pnpm
- **Dev Port**: 3000

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/tailadmin-nextjs-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/tailadmin-nextjs-template.git _temp_template
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
pnpm install
```

## Build

```bash
pnpm build
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
netlify deploy --prod
```

## Development

```bash
pnpm dev
```

Opens at http://localhost:3000
