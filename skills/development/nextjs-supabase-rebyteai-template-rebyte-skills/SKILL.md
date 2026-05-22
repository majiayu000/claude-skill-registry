---
name: nextjs-supabase
description: Next.js full-stack application with Supabase backend.
---

# Next.js + Supabase

A full-stack application with Supabase backend.

## Tech Stack

- **Framework**: Next.js
- **Database**: Supabase
- **Package Manager**: npm

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/nextjs-supabase-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/nextjs-supabase-template.git _temp_template
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

Configure Supabase credentials in `.env.local`

## Build

```bash
npm run build
```

## Development

```bash
npm run dev
```
