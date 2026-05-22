---
name: nextjs-blog-netlify
description: Next.js blog with visual editing and Tailwind CSS for Netlify.
---

# Next.js Blog (Netlify)

A customizable blog with visual editing and Tailwind CSS.

## Tech Stack

- **Framework**: Next.js
- **Styling**: Tailwind CSS
- **Package Manager**: npm

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/netlify-templates/nextjs-blog-theme.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/netlify-templates/nextjs-blog-theme.git _temp_template
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

## Deploy to Netlify

```bash
netlify deploy --prod
```

## Development

```bash
npm run dev
```
