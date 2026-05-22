---
name: tanstack-chat-netlify
description: Modern chat app with TanStack Router and Claude AI for Netlify.
---

# TanStack Chat (Netlify)

A modern chat application with TanStack Router and Claude AI.

## Tech Stack

- **Framework**: React
- **Router**: TanStack Router
- **AI**: Claude AI integration
- **Package Manager**: npm

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/netlify-templates/tanstack-template.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/netlify-templates/tanstack-template.git _temp_template
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
