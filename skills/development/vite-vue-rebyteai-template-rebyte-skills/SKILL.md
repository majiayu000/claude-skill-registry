---
name: vite-vue
description: Vite + Vue 3.5 template with TypeScript. Clone, setup, build, and deploy to Vercel or Netlify.
---

# Vite Vue Template

A lightning-fast Vue 3.5 development environment with Vite 7 and TypeScript.

## Tech Stack

- **Framework**: Vue 3.5
- **Build Tool**: Vite 7
- **Language**: TypeScript
- **Package Manager**: npm
- **Output**: `dist` directory
- **Dev Port**: 5173

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/vite-vue-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/vite-vue-template.git _temp_template
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

Vue TypeScript compilation runs before build (`vue-tsc -b && vite build`).

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

Opens at http://localhost:5173 with HMR enabled. Uses Single File Components (SFC) with `<script setup>` syntax.
