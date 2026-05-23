---
name: dillion-portfolio
description: Minimalist developer portfolio with blog, work timeline, and project showcase using Next.js 14.
---

# Dillion Portfolio

A minimalist developer portfolio with blog, work experience timeline, and project showcase.

## Tech Stack

- **Framework**: Next.js 14
- **React**: React 18
- **Animation**: Framer Motion
- **Styling**: Tailwind CSS, shadcn/ui
- **Content**: MDX for blog
- **Package Manager**: pnpm
- **Dev Port**: 3000

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/portfolio-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/portfolio-template.git _temp_template
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
netlify deploy --prod --dir=.next
```

## Customization

Edit content in the `src/data/` directory:
- `resume.tsx` - Personal info, work experience, education, projects

Portfolio content is stored in `content/` directory as MDX files.

## Development

```bash
pnpm dev
```

Opens at http://localhost:3000
