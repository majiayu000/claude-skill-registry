---
name: content-ops-netlify
description: Next.js content model with visual editing for Netlify.
---

# Content Ops Starter (Netlify)

A flexible content model with visual editing.

## Tech Stack

- **Framework**: Next.js
- **Package Manager**: npm

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/netlify-templates/content-ops-starter.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/netlify-templates/content-ops-starter.git _temp_template
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
