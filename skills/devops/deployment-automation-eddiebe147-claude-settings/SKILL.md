---
name: deployment-automation
description: Expert guide for deploying Next.js apps to Vercel, managing environments, CI/CD pipelines, and production best practices. Use when deploying, setting up automation, or managing production.
---

# Deployment Automation Skill

## Overview

This skill helps you deploy and manage your Next.js application in production. From Vercel deployments to CI/CD pipelines, this covers everything you need for smooth, automated deployments.

## Vercel Deployment

### Install Vercel CLI
```bash
npm i -g vercel
vercel login
```

### Deploy to Production
```bash
# Deploy to production
vercel --prod

# Deploy with specific environment
vercel --prod --env production
```

### Deploy from Git
```bash
# Link project
vercel link

# Auto-deploy on git push (configured in Vercel dashboard)
git push origin main  # Auto-deploys to production
git push origin develop  # Auto-deploys to preview
```

### Project Configuration
```json
// vercel.json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["iad1"],  // AWS us-east-1
  "env": {
    "NEXT_PUBLIC_APP_URL": "https://myapp.com"
  },
  "build": {
    "env": {
      "NEXT_PUBLIC_VERCEL_ENV": "@vercel-env"
    }
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/old-page",
      "destination": "/new-page",
      "permanent": true
    }
  ],
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.backend.com/:path*"
    }
  ]
}
```

### Environment Variables

**Using Vercel CLI:**
```bash
# Add production env var
vercel env add SUPABASE_URL production

# Add to all environments
vercel env add DATABASE_URL

# Pull env vars locally
vercel env pull .env.local
```

**Using Vercel Dashboard:**
1. Go to Project Settings → Environment Variables
2. Add variables for each environment:
   - Production
   - Preview
   - Development

**Encrypted Secrets:**
```bash
# Add sensitive data
vercel secrets add database-url "postgresql://..."

# Reference in vercel.json
{
  "env": {
    "DATABASE_URL": "@database-url"
  }
}
```

### Environment-Specific Config
```typescript
// lib/config.ts
const config = {
  development: {
    apiUrl: 'http://localhost:3000/api',
    supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
  },
  preview: {
    apiUrl: process.env.NEXT_PUBLIC_API_URL!,
    supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
  },
  production: {
    apiUrl: 'https://api.myapp.com',
    supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
  },
}

const env = (process.env.NEXT_PUBLIC_VERCEL_ENV || 'development') as keyof typeof config

export const appConfig = config[env]
```

## GitHub Actions CI/CD

### Basic Workflow
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run type check
        run: npm run type-check

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build
        env:
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.NEXT_PUBLIC_SUPABASE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.NEXT_PUBLIC_SUPABASE_ANON_KEY }}
```

### Deploy to Vercel from GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### Run Tests on PR
```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Unit tests
        run: npm test

      - name: E2E tests
        run: npx playwright test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

## Pre-deployment Checks

### Custom Pre-deploy Script
```json
// package.json
{
  "scripts": {
    "predeploy": "npm run check:all",
    "check:all": "npm run lint && npm run type-check && npm test",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "test": "jest"
  }
}
```

### Health Check Endpoint
```typescript
// app/api/health/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  try {
    // Check database connection
    await db.$queryRaw`SELECT 1`

    // Check external services
    const services = await Promise.allSettled([
      fetch(process.env.API_URL!),
      fetch(process.env.SUPABASE_URL!),
    ])

    const allHealthy = services.every(s => s.status === 'fulfilled')

    return NextResponse.json({
      status: allHealthy ? 'healthy' : 'degraded',
      timestamp: new Date().toISOString(),
      version: process.env.NEXT_PUBLIC_APP_VERSION,
      services: {
        database: 'healthy',
        api: services[0].status === 'fulfilled' ? 'healthy' : 'unhealthy',
        supabase: services[1].status === 'fulfilled' ? 'healthy' : 'unhealthy',
      }
    })
  } catch (error) {
    return NextResponse.json(
      { status: 'unhealthy', error: error.message },
      { status: 503 }
    )
  }
}
```

## Database Migrations

### Run Migrations on Deploy
```json
// package.json
{
  "scripts": {
    "build": "npm run db:migrate && next build",
    "db:migrate": "npx supabase db push"
  }
}
```

### Safe Migration Strategy
```bash
# 1. Test migration locally
npx supabase db reset
npx supabase db push

# 2. Create backup
npx supabase db dump > backup.sql

# 3. Apply to production
npx supabase db push --linked

# 4. Verify
curl https://myapp.com/api/health
```

## Monitoring & Alerts

### Vercel Speed Insights
```typescript
// app/layout.tsx
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  )
}
```

### Vercel Analytics
```typescript
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

### Custom Monitoring
```typescript
// lib/monitoring.ts
export async function reportDeployment() {
  if (process.env.NODE_ENV === 'production') {
    await fetch('https://monitoring.example.com/deployments', {
      method: 'POST',
      body: JSON.stringify({
        version: process.env.NEXT_PUBLIC_APP_VERSION,
        timestamp: new Date().toISOString(),
        environment: process.env.NEXT_PUBLIC_VERCEL_ENV,
      }),
    })
  }
}

// Call in app initialization
reportDeployment()
```

## Feature Flags

### Environment-Based Flags
```typescript
// lib/features.ts
export const features = {
  newDesign: process.env.NEXT_PUBLIC_FEATURE_NEW_DESIGN === 'true',
  betaFeatures: process.env.NEXT_PUBLIC_FEATURE_BETA === 'true',
  analytics: process.env.NEXT_PUBLIC_FEATURE_ANALYTICS === 'true',
}

// Usage
import { features } from '@/lib/features'

export function Component() {
  if (!features.newDesign) {
    return <OldDesign />
  }
  return <NewDesign />
}
```

### Advanced Feature Flags (Vercel Edge Config)
```typescript
import { get } from '@vercel/edge-config'

export async function getFeatureFlag(key: string): Promise<boolean> {
  try {
    return await get<boolean>(key) ?? false
  } catch {
    return false
  }
}

// Usage in Server Component
export default async function Page() {
  const showNewFeature = await getFeatureFlag('new-feature')

  if (showNewFeature) {
    return <NewFeature />
  }
  return <OldFeature />
}
```

## Rollback Strategy

### Instant Rollback
```bash
# List deployments
vercel ls

# Promote previous deployment to production
vercel promote <deployment-url>
```

### Automated Rollback on Error
```yaml
# .github/workflows/deploy-with-rollback.yml
name: Deploy with Rollback

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Get previous deployment
        id: prev-deploy
        run: |
          PREV_URL=$(vercel ls --token=${{ secrets.VERCEL_TOKEN }} | grep production | head -n 2 | tail -n 1 | awk '{print $2}')
          echo "prev_url=$PREV_URL" >> $GITHUB_OUTPUT

      - name: Deploy to Vercel
        id: deploy
        run: |
          URL=$(vercel --prod --token=${{ secrets.VERCEL_TOKEN }})
          echo "deploy_url=$URL" >> $GITHUB_OUTPUT

      - name: Health check
        id: health
        run: |
          sleep 10
          STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${{ steps.deploy.outputs.deploy_url }}/api/health)
          if [ $STATUS -ne 200 ]; then
            echo "Health check failed"
            exit 1
          fi

      - name: Rollback on failure
        if: failure()
        run: |
          vercel promote ${{ steps.prev-deploy.outputs.prev_url }} --token=${{ secrets.VERCEL_TOKEN }}
```

## Preview Deployments

### Automatic Preview URLs
Every branch push gets a unique URL:
```
https://myapp-git-feature-branch-username.vercel.app
```

### Preview Comments on PR
```yaml
# .github/workflows/preview-comment.yml
name: Preview Deployment Comment

on:
  deployment_status:

jobs:
  comment:
    if: github.event.deployment_status.state == 'success'
    runs-on: ubuntu-latest

    steps:
      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `✅ Preview deployed to ${process.env.DEPLOYMENT_URL}`
            })
```

## Performance Budgets

### Lighthouse CI
```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI

on:
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: |
            https://preview-url.vercel.app
            https://preview-url.vercel.app/dashboard
          uploadArtifacts: true
          temporaryPublicStorage: true
```

### Bundle Size Check
```yaml
# .github/workflows/bundle-size.yml
name: Bundle Size Check

on: [pull_request]

jobs:
  size:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Check bundle size
        uses: andresz1/size-limit-action@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Best Practices Checklist

- [ ] Use environment variables for secrets
- [ ] Set up automatic deployments from Git
- [ ] Configure preview deployments for PRs
- [ ] Implement health check endpoint
- [ ] Set up monitoring and alerts
- [ ] Run tests before deploying
- [ ] Use feature flags for gradual rollouts
- [ ] Have a rollback strategy
- [ ] Monitor Core Web Vitals
- [ ] Set performance budgets
- [ ] Run database migrations safely
- [ ] Use separate environments (dev/staging/prod)
- [ ] Implement proper error tracking
- [ ] Document deployment process

## When to Use This Skill

Invoke this skill when:
- Deploying to Vercel for the first time
- Setting up CI/CD pipelines
- Configuring environment variables
- Implementing feature flags
- Setting up monitoring
- Creating rollback strategies
- Optimizing deployment speed
- Debugging production issues
- Managing preview deployments
- Setting up automated tests
