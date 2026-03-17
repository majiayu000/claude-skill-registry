---
name: Vercel Deploy
description: This skill should be used when the user asks to "deploy to Vercel", "deploy frontend", "push to production", "deploy my app", "go live on Vercel", or mentions Vercel deployment workflows.
version: 1.0.0
---

# Deploy to Vercel

## Overview

Vercel deployment automates frontend application deployment with zero-configuration builds, automatic SSL, and global CDN. This skill guides through production-ready Vercel deployments for modern web applications.

## Prerequisites Check

### Install Vercel CLI
```bash
npm install -g vercel
```

### Authentication
```bash
vercel login
```

### Verify Setup
```bash
vercel --version
vercel whoami
```

## Project Configuration

### Vercel Configuration File
Create `vercel.json` in project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "NODE_ENV": "production"
  },
  "build": {
    "env": {
      "VITE_API_URL": "@api_url"
    }
  }
}
```

### Build Configuration
Ensure `package.json` has proper build scripts:

```json
{
  "scripts": {
    "build": "vite build",
    "preview": "vite preview",
    "type-check": "tsc --noEmit"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

## Deployment Workflows

### Production Deployment
```bash
# Deploy to production
vercel --prod

# Deploy with custom domain
vercel --prod --domain your-app.com
```

### Preview Deployment
```bash
# Deploy preview (staging)
vercel

# Deploy specific branch preview
vercel --target preview --git-branch staging
```

### Environment-Specific Deployment
```bash
# Deploy with environment
vercel --prod --env NODE_ENV=production --env API_URL=https://api.production.com
```

## Environment Configuration

### Environment Variables Setup
```bash
# Add production environment variables
vercel env add VITE_API_URL production
vercel env add VITE_APP_NAME production
vercel env add DATABASE_URL production

# Add preview environment variables
vercel env add VITE_API_URL preview
vercel env add DATABASE_URL preview

# List all environment variables
vercel env ls
```

### Local Environment Sync
```bash
# Pull environment variables to local
vercel env pull .env.local

# Link project to Vercel
vercel link
```

## Framework-Specific Configurations

### React/Vite Applications
```json
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@mui/material', '@emotion/react']
        }
      }
    }
  },
  optimizeDeps: {
    exclude: ['lucide-react']
  }
});
```

### Next.js Applications
```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true
  },
  images: {
    domains: ['your-image-domain.com']
  },
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY
  }
};

module.exports = nextConfig;
```

### SvelteKit Applications
```javascript
// svelte.config.js
import adapter from '@sveltejs/adapter-vercel';

export default {
  kit: {
    adapter: adapter({
      runtime: 'nodejs18.x'
    })
  }
};
```

## Custom Domain Setup

### Add Custom Domain
```bash
# Add domain to Vercel project
vercel domains add your-domain.com

# Set domain as alias
vercel alias set your-deployment-url.vercel.app your-domain.com
```

### DNS Configuration
Update DNS records with your domain provider:

```
Type: CNAME
Name: www
Value: cname.vercel-dns.com

Type: A
Name: @
Value: 76.76.19.61
```

## Advanced Deployment Features

### Edge Functions
```typescript
// api/edge-function.ts
import { NextRequest } from 'next/server';

export const config = {
  runtime: 'edge'
};

export default function handler(req: NextRequest) {
  return new Response(
    JSON.stringify({
      message: 'Hello from Edge Function',
      timestamp: new Date().toISOString(),
      location: req.geo?.city || 'Unknown'
    }),
    {
      status: 200,
      headers: {
        'content-type': 'application/json',
        'cache-control': 'max-age=60'
      }
    }
  );
}
```

### Serverless Functions
```javascript
// api/serverless.js
export default function handler(req, res) {
  if (req.method === 'POST') {
    // Handle POST request
    const { data } = req.body;

    res.status(200).json({
      success: true,
      message: 'Data processed',
      data: data
    });
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
```

### ISR (Incremental Static Regeneration)
```typescript
// pages/products/[id].tsx
export async function getStaticProps({ params }) {
  const product = await fetchProduct(params.id);

  return {
    props: { product },
    revalidate: 60 // Regenerate page every 60 seconds
  };
}

export async function getStaticPaths() {
  const products = await fetchProducts();

  return {
    paths: products.map(p => ({ params: { id: p.id } })),
    fallback: 'blocking'
  };
}
```

## CI/CD Integration

### GitHub Actions Deployment
```yaml
# .github/workflows/vercel-deployment.yml
name: Deploy to Vercel

on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run tests
      run: npm test

    - name: Build application
      run: npm run build

    - name: Deploy to Vercel
      uses: amondnet/vercel-action@v25
      with:
        vercel-token: ${{ secrets.VERCEL_TOKEN }}
        vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
        vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
        vercel-args: '--prod'
      if: github.ref == 'refs/heads/main'
```

### GitLab CI/CD
```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "18"

test:
  stage: test
  image: node:$NODE_VERSION
  script:
    - npm ci
    - npm run test
    - npm run type-check

build:
  stage: build
  image: node:$NODE_VERSION
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/

deploy_production:
  stage: deploy
  image: node:$NODE_VERSION
  script:
    - npm install -g vercel
    - vercel --token $VERCEL_TOKEN --prod --yes
  only:
    - main
  environment:
    name: production
    url: https://your-app.vercel.app
```

## Monitoring and Analytics

### Vercel Analytics Integration
```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### Performance Monitoring
```javascript
// lib/analytics.js
export function trackPageView(url) {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('config', 'GA_MEASUREMENT_ID', {
      page_location: url
    });
  }
}

export function trackEvent(action, category, label, value) {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', action, {
      event_category: category,
      event_label: label,
      value: value
    });
  }
}
```

## Security Configuration

### Security Headers
```json
// vercel.json
{
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
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        },
        {
          "key": "Content-Security-Policy",
          "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
        }
      ]
    }
  ]
}
```

### Environment Security
```bash
# Secure environment variable management
vercel env add SECRET_KEY production --sensitive
vercel env add API_KEY production --sensitive

# Use Vercel's built-in secrets
vercel secrets add my-secret-name "secret-value"
```

## Troubleshooting Common Issues

### Build Failures
```bash
# Check build logs
vercel logs

# Local build debugging
vercel dev --debug

# Clear build cache
vercel --force
```

### Domain Issues
```bash
# Verify domain configuration
vercel domains inspect your-domain.com

# Check DNS propagation
nslookup your-domain.com

# Force SSL certificate renewal
vercel certs issue your-domain.com
```

### Performance Issues
```bash
# Analyze bundle size
npm install -g @vercel/ncc
ncc analyze dist/

# Check Core Web Vitals
vercel inspect https://your-app.vercel.app
```

## Best Practices

### Optimization Strategies

**Code Splitting:**
```javascript
// Lazy load components
const LazyComponent = React.lazy(() => import('./LazyComponent'));

// Dynamic imports for large dependencies
const loadChartLibrary = () => import('chart.js');
```

**Image Optimization:**
```typescript
// Next.js Image component
import Image from 'next/image';

<Image
  src="/hero-image.jpg"
  alt="Hero"
  width={800}
  height={600}
  priority
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>
```

**Caching Strategy:**
```json
{
  "headers": [
    {
      "source": "/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    },
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "s-maxage=60, stale-while-revalidate"
        }
      ]
    }
  ]
}
```

### Deployment Checklist

**Pre-Deployment:**
- [ ] All tests pass locally
- [ ] Build completes without errors
- [ ] Environment variables configured
- [ ] Dependencies up to date
- [ ] Security headers configured
- [ ] Performance optimizations applied

**Post-Deployment:**
- [ ] Deployment URL accessible
- [ ] Custom domain working
- [ ] SSL certificate valid
- [ ] Analytics tracking functional
- [ ] Error monitoring active
- [ ] Performance metrics baseline established

## Additional Resources

### Reference Files
For detailed deployment configurations, consult:
- **`references/framework-configs.md`** - Framework-specific Vercel configurations
- **`references/performance-optimization.md`** - Performance optimization strategies
- **`references/security-best-practices.md`** - Security configuration guidelines

### Example Files
Working deployment examples in `examples/`:
- **`examples/react-vite-config.js`** - Complete React+Vite Vercel setup
- **`examples/nextjs-deployment.js`** - Next.js deployment configuration
- **`examples/ci-cd-pipeline.yml`** - Complete CI/CD pipeline

### Scripts
Deployment utility scripts in `scripts/`:
- **`scripts/deploy-production.sh`** - Automated production deployment
- **`scripts/setup-vercel-project.sh`** - Initial Vercel project setup
- **`scripts/performance-check.sh`** - Post-deployment performance validation

Deploy modern web applications with confidence using Vercel's powerful platform and these production-ready configurations.