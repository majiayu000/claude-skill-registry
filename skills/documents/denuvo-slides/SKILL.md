---
name: denuvo-slides
description: Slidev presentation about reverse engineering Denuvo in Hogwarts Legacy.
---

# Denuvo Slides

A Slidev presentation about reverse engineering Denuvo in Hogwarts Legacy.

## Tech Stack

- **Framework**: Slidev (Vue-based)
- **Package Manager**: pnpm
- **Output**: `dist` directory

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/denuvo-slides-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/denuvo-slides-template.git _temp_template
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

Note: The default build command may include a custom base path. Modify `package.json` build script if needed for your deployment target.

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
pnpm dev
```

Starts the Slidev server and opens the presentation in your browser. Edit slides in `slides.md`.
