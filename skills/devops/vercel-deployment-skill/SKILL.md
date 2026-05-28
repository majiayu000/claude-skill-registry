---
name: "Vercel Deployment"
description: "Deploy Next.js to Vercel with zero-config, manage environment variables, set up CI/CD pipelines, and optimize production performance. Apply when deploying to Vercel, configuring environments, or setting up CI/CD workflows."
allowed-tools: Read, Write, Edit, Bash
version: 1.0.0
---

# Vercel Deployment

Systematic Vercel deployment ensuring fast, scalable, production-ready applications with CI/CD automation.

## Overview

This Skill enforces:
- Zero-config Next.js deployments
- Secure environment variable management
- Automated CI/CD pipelines (GitHub Actions)
- Preview deployments for every PR
- Production deployments on main branch merge
- Performance optimization

Apply when deploying to Vercel, configuring environments, or testing CI/CD workflows.

## Deployment Workflow

**Every deployment follows this process**:

```
Step 1: Connect GitHub repository
  ↓
Step 2: Configure environment variables
  ↓
Step 3: Set up CI/CD pipelines
  ↓
Step 4: Trigger preview deployment (on PR)
  ↓
Step 5: Merge and deploy production
  ↓
Step 6: Monitor performance
```

## Step 1: Initial Connection

### Connect GitHub Repository

```bash
# 1. Visit https://vercel.com and login
# 2. Click "New Project"
# 3. Select GitHub repository
# 4. Vercel auto-detects Next.js
# 5. Click "Deploy"
```

**Vercel automatically detects**:
- Framework: Next.js
- Build command: `next build`
- Output directory: `.next`
- Install command: `npm install`

No configuration needed for basic setup.

### Verify Deployment

After deploy:
- Live at: `yourproject.vercel.app`
- Production domain: `yourdomain.com` (if configured)
- Preview URL provided in PR comments

## Step 2: Environment Variables

### Setup Variables

**MUST NOT**: Hardcode secrets in code or commit `.env` files.

### Local Development

Pull dev environment variables:

```bash
vercel env pull
```

This creates `.env.local` with variables from Vercel Development environment.

Add to `.gitignore`:
```
.env.local
.env.*.local
```

### Vercel Dashboard Configuration

1. Go to Project Settings → Environment Variables
2. Add variable for each environment:
   - **Development**: Local development only
   - **Preview**: Pull requests and branches
   - **Production**: Main branch deployments

### Variable Types

```
Regular: Visible in logs and build output
Sensitive: Hidden, only for production/preview
System: Vercel-provided (__VERCEL_*)
```

### Example Configuration

```
DATABASE_URL=postgresql://...        # All environments
NEXT_PUBLIC_API_URL=https://api....  # Public (prefixed with NEXT_PUBLIC_)
STRIPE_SECRET_KEY=sk_live_...        # Sensitive production only
```

### Accessing Variables

**Public variables** (client-side, prefixed `NEXT_PUBLIC_`):

```ts
// Available in browser
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

**Secret variables** (server-side only):

```ts
// Only available on server
export async function getServerSideProps() {
  const dbUrl = process.env.DATABASE_URL;  // Server-side only
  return { props: {} };
}
```

**Anti-Pattern**:

```ts
// ❌ BAD: Hardcoded secrets
const apiKey = 'sk-1234567890';

// ❌ BAD: Committing .env
git add .env  // NEVER!

// ❌ BAD: Public secret key
const apiKey = process.env.STRIPE_SECRET_KEY;  // Exposed in browser!
```

## Step 3: CI/CD Pipeline Setup

### MUST NOT: Mention Claude/Anthropic

No automated footers, comments, or attributions to Claude or Anthropic in any generated code or documentation.

### GitHub Actions Workflow

Create `.github/workflows/production.yaml`:

```yaml
name: Vercel Production Deployment

env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

on:
  push:
    branches:
      - main

jobs:
  Deploy-Production:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: npm run lint

      - name: Run tests
        run: npm run test

      - name: Build
        run: npm run build

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Pull Vercel environment
        run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy to Production
        run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
```

### Preview Deployment

Create `.github/workflows/preview.yaml`:

```yaml
name: Vercel Preview Deployment

env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

on:
  pull_request:

jobs:
  Deploy-Preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: npm run lint

      - name: Run tests
        run: npm run test

      - name: Build
        run: npm run build

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Pull Vercel environment
        run: vercel pull --yes --environment=preview --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy to Preview
        run: vercel deploy --prebuilt --token=${{ secrets.VERCEL_TOKEN }}
```

### Configure GitHub Secrets

Add to GitHub repository → Settings → Secrets and variables → Actions:

```
VERCEL_ORG_ID     # From vercel link command
VERCEL_PROJECT_ID # From vercel link command
VERCEL_TOKEN      # From Vercel account settings
```

### Linking Project

```bash
# Link project to Vercel
vercel link

# Creates .vercel/project.json with project and org IDs
# Copy these to GitHub Secrets
```

## Step 4: Preview Deployments

### Automatic PR Previews

When PR opens:
1. GitHub Actions triggers preview workflow
2. Code is tested, built, deployed
3. Preview URL added to PR comments
4. Team reviews in production-like environment
5. Unique URL for each PR: `project-pr-123.vercel.app`

### Workflow

```
Push to feature branch → GitHub Actions runs tests & builds
  ↓
Deploy preview to Vercel
  ↓
PR gets preview URL comment
  ↓
Team reviews changes
  ↓
Merge to main triggers production
```

## Step 5: Production Deployment

### Merge to Main

```bash
# After PR approval
git checkout main
git pull origin main
git merge feature-branch
git push origin main

# GitHub Actions automatically:
# 1. Runs linting
# 2. Runs tests
# 3. Builds project
# 4. Deploys to production
```

### Deployment Checklist

Before merging to main:

- [ ] All tests pass locally
- [ ] Linting passes
- [ ] TypeScript compiles
- [ ] Preview deployment tested
- [ ] No sensitive data in code
- [ ] Environment variables configured
- [ ] Performance optimizations applied

## Step 6: Performance Optimization

### Image Optimization

```tsx
// ✅ GOOD: Use next/image
import Image from 'next/image';

export function ProfileImage({ src, alt }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={200}
      height={200}
      priority  // Load immediately
    />
  );
}

// ❌ BAD: Unoptimized HTML img
<img src={imageUrl} alt="profile" />
```

### Static Generation (ISR)

```ts
// ✅ GOOD: Incremental Static Regeneration
export const revalidate = 3600;  // Revalidate every 1 hour

export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 }
  });
  return <div>{data}</div>;
}
```

### Edge Functions

```ts
// ✅ GOOD: Run at edge (fastest response)
export const config = {
  runtime: 'edge'
};

export default async function middleware(request) {
  if (request.nextUrl.pathname === '/admin') {
    if (!request.headers.get('authorization')) {
      return new Response('Unauthorized', { status: 401 });
    }
  }
  return null;
}
```

### Bundle Analysis

```bash
# Analyze bundle size
npm run build

# Check what contributes to bundle
npm run analyze
```

## Anti-Patterns

```bash
# ❌ BAD: Push to main without tests
git push origin main

# ❌ BAD: Hardcoded API keys
const apiKey = 'sk-1234567890';

# ❌ BAD: No linting in pipeline
# Deploy without checking code quality

# ❌ BAD: Commit .env
git add .env

# ❌ BAD: No preview deployments
# Deploy to production without team review

# ❌ BAD: No environment variables separated
# Use same config for dev/preview/prod
```

## Verification Before Deployment

Before deploying to production:

- [ ] All GitHub Secrets configured (ORG_ID, PROJECT_ID, TOKEN)
- [ ] `.github/workflows/` files created (preview.yaml, production.yaml)
- [ ] Tests pass locally
- [ ] Linting passes
- [ ] Environment variables set in Vercel dashboard
- [ ] No hardcoded secrets in code
- [ ] `.env` files in `.gitignore`
- [ ] Preview deployment tested
- [ ] Performance optimized (images, bundle size)
- [ ] HTTPS enabled (automatic on Vercel)

## Common Commands

```bash
# Pull dev environment variables
vercel env pull

# Link project
vercel link

# Deploy preview
vercel deploy --prebuilt

# Deploy production
vercel deploy --prebuilt --prod

# View logs
vercel logs

# Run locally with production settings
vercel dev
```

## Troubleshooting

### Build Failures

```bash
# Check build logs in Vercel dashboard
# Verify environment variables set
# Run locally: npm run build
# Check for TypeScript errors: npx tsc --noEmit
```

### Environment Variable Not Found

```bash
# Verify variable exists in Vercel dashboard
# Check environment matches deployment (dev/preview/prod)
# For public variables, prefix with NEXT_PUBLIC_
# For server variables, only accessible in API routes or server functions
```

### Preview URL Not Working

```bash
# Verify GitHub Actions workflow passed
# Check workflow logs in GitHub Actions tab
# Confirm Vercel secrets set correctly
# Verify preview.yaml file exists
```

## Integration with Project Standards

Enforces deployment best practices:
- Zero-config Next.js deployment
- Secure secret management (S-5)
- Automated CI/CD pipeline
- Performance optimization
- Production-grade deployment workflow

## Resources

- Vercel Docs: https://vercel.com/docs
- Next.js Deployment: https://nextjs.org/learn/basics/deploying
- GitHub Actions: https://docs.github.com/en/actions
- Environment Variables: https://vercel.com/docs/projects/environment-variables
