---
name: astro-supabase-netlify
description: Astro with Supabase integration for Netlify.
---

# Astro + Supabase (Netlify)

Astro with Supabase integration.

## Tech Stack

- **Framework**: Astro
- **Database**: Supabase
- **Package Manager**: npm

## Prerequisites

- Supabase project

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/netlify-templates/astro-supabase-starter.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/netlify-templates/astro-supabase-starter.git _temp_template
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

### 4. Setup Environment

Configure Supabase credentials in `.env`

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
