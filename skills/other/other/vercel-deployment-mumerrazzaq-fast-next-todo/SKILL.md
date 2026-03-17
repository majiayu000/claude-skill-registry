---
name: vercel-deployment
description: "Comprehensive skill for deploying applications to Vercel. Covers all deployment types: single projects, monorepos, static sites, Next.js, React, Python/FastAPI backends, serverless functions, and edge functions. Use when deploying to Vercel, configuring vercel.json, setting up environment variables, troubleshooting deployments, or understanding Vercel's architecture."
---

# Vercel Deployment Skill

## Overview

This skill provides complete guidance for deploying any type of application to Vercel. It covers single-project deployments, monorepo configurations, serverless functions, edge functions, and all supported frameworks.

## Quick Reference

| Deployment Type | Reference File |
|-----------------|----------------|
| Deployment strategies | `references/deployment-strategies.md` |
| Framework-specific guides | `references/framework-guides.md` |
| Python/FastAPI backends | `references/python-serverless.md` |
| Monorepo setup | `references/monorepo-configuration.md` |
| Environment variables | `references/environment-variables.md` |
| Edge cases & troubleshooting | `references/edge-cases-troubleshooting.md` |
| CLI commands | `references/cli-reference.md` |

## Workflow

### Step 1: Determine Deployment Strategy

First, identify the project structure:

```
Single Project?          → Standard deployment (auto-detected)
Monorepo?               → Multi-project or Turborepo setup
Static Site?            → Static hosting (no functions)
API Backend?            → Serverless functions
Full-Stack?             → Framework-specific (Next.js, Nuxt, etc.)
```

**Action**: Read `references/deployment-strategies.md` for detailed guidance.

### Step 2: Choose Framework Configuration

Vercel auto-detects most frameworks. For custom configurations:

| Framework | Auto-Detected | Custom Config Needed |
|-----------|---------------|---------------------|
| Next.js | Yes | Rarely |
| React (Vite/CRA) | Yes | Sometimes |
| Vue/Nuxt | Yes | Rarely |
| Python/FastAPI | Partial | Yes |
| Static HTML | Yes | No |

**Action**: Read `references/framework-guides.md` for framework-specific instructions.

### Step 3: Configure vercel.json (If Needed)

Use templates from `assets/templates/` based on your needs:

- `vercel.nextjs.json` — Next.js projects
- `vercel.static.json` — Static sites
- `vercel.python-api.json` — Python/FastAPI backends
- `vercel.monorepo-frontend.json` — Monorepo frontend
- `vercel.monorepo-backend.json` — Monorepo backend

### Step 4: Set Up Environment Variables

**Action**: Read `references/environment-variables.md` for:
- Production vs Preview vs Development environments
- Sensitive vs Public variables
- Shared variables across projects

### Step 5: Deploy

```bash
# Via CLI
vercel              # Preview deployment
vercel --prod       # Production deployment

# Via Git (automatic)
git push origin main  # Triggers production deploy
```

### Step 6: Verify & Troubleshoot

**Action**: If issues occur, read `references/edge-cases-troubleshooting.md`.

## Decision Tree

```
START
  │
  ├─► Is it a monorepo?
  │     ├─► YES → Read references/monorepo-configuration.md
  │     │         └─► Create separate Vercel projects per app
  │     │
  │     └─► NO → Continue
  │
  ├─► What's the backend?
  │     ├─► Node.js → Auto-detected, use API routes
  │     ├─► Python → Read references/python-serverless.md
  │     ├─► Go/Rust → Use serverless functions
  │     └─► None → Static deployment
  │
  ├─► What's the frontend?
  │     ├─► Next.js → Zero-config, auto-detected
  │     ├─► React (Vite) → Set outputDirectory
  │     ├─► Vue/Nuxt → Zero-config
  │     └─► Static HTML → Zero-config
  │
  └─► Deploy!
```

## Common Patterns

### Pattern 1: Next.js Full-Stack (Most Common)

```
project/
├── app/              # App Router
├── pages/api/        # API Routes (serverless)
├── public/
├── package.json
└── next.config.js
```

No `vercel.json` needed. Just push to Git.

### Pattern 2: React + Separate Backend

```
Frontend Project (Vercel Project #1):
└── frontend/
    ├── src/
    ├── package.json
    └── vercel.json (optional)

Backend Project (Vercel Project #2):
└── backend/
    ├── api/index.py
    ├── requirements.txt
    └── vercel.json
```

### Pattern 3: Static Site

```
project/
├── index.html
├── styles.css
└── script.js
```

Zero-config. Vercel serves static files automatically.

### Pattern 4: Python API Only

```
backend/
├── api/
│   └── index.py      # FastAPI app
├── requirements.txt
└── vercel.json
```

## Assets

### Templates (assets/templates/)

| Template | Use Case |
|----------|----------|
| `vercel.nextjs.json` | Next.js with custom config |
| `vercel.static.json` | Static sites |
| `vercel.python-api.json` | Python/FastAPI backend |
| `vercel.react-vite.json` | React with Vite |
| `vercel.monorepo-frontend.json` | Monorepo frontend project |
| `vercel.monorepo-backend.json` | Monorepo backend project |
| `vercel.edge-functions.json` | Edge function configuration |

### Examples (examples/)

| Example | Description |
|---------|-------------|
| `nextjs-fullstack/` | Complete Next.js deployment |
| `react-python-monorepo/` | Monorepo with React + FastAPI |
| `static-site/` | Simple static deployment |
| `python-api/` | Standalone Python API |

## Quick Commands

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy (preview)
vercel

# Deploy (production)
vercel --prod

# Link to existing project
vercel link

# Link all projects in monorepo
vercel link --repo

# Pull environment variables
vercel env pull

# Add environment variable
vercel env add SECRET_KEY production

# View logs
vercel logs https://your-project.vercel.app

# List deployments
vercel ls

# Rollback (promote old deployment)
vercel promote <deployment-url>
```

## When to Use This Skill

Use this skill when the user wants to:
- Deploy any application to Vercel
- Configure `vercel.json`
- Set up a monorepo on Vercel
- Deploy Python/FastAPI backends
- Troubleshoot Vercel deployment issues
- Understand Vercel's serverless architecture
- Configure environment variables
- Set up custom domains
- Implement CI/CD with Vercel
