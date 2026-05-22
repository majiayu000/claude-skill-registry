---
name: vite-react
description: Vite + React template with TypeScript. Clone, setup, build, and deploy to Vercel or Netlify.
---

# Vite React Template

A complete Vite + React project with TypeScript, ESLint, and hot module replacement.

## Tech Stack

- **Framework**: React 19
- **Build Tool**: Vite 7
- **Language**: TypeScript
- **Package Manager**: npm
- **Output**: `dist` directory
- **Dev Port**: 5173

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/vite-react-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/vite-react-template.git _temp_template
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

TypeScript compilation runs before build (`tsc -b && vite build`).

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

Opens at http://localhost:5173 with HMR enabled.
