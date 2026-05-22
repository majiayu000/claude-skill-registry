---
name: web-build-deploy
description: Building and deploying React web applications. Use when configuring builds, deploying to Vercel/Netlify, setting up CI/CD, Docker, or managing environments.
---

# Web Build & Deploy (React)

## Vercel Deployment

### Quick Deploy

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy to production
vercel --prod
```

### Configuration (vercel.json)

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ]
}
```

### Environment Variables

```bash
# Add via CLI
vercel env add NEXT_PUBLIC_API_URL

# Or in Vercel dashboard: Settings > Environment Variables

# Access in code
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

### Preview Deployments

Every push to a branch creates a preview URL automatically:
- `https://project-git-branch-username.vercel.app`

---

## Netlify Deployment

### Quick Deploy

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Login
netlify login

# Deploy preview
netlify deploy

# Deploy to production
netlify deploy --prod
```

### Configuration (netlify.toml)

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"

[build.environment]
  NODE_VERSION = "18"
```

### Environment Variables

```bash
# Add via CLI
netlify env:set API_URL https://api.example.com

# Or in Netlify dashboard: Site settings > Environment variables
```

---

## Docker Deployment

### Dockerfile (Multi-stage build)

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### nginx.conf (SPA routing)

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
}
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
    restart: unless-stopped

  # With backend
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=app

volumes:
  postgres_data:
```

### Build & Run

```bash
# Build image
docker build -t myapp:latest .

# Run container
docker run -p 80:80 myapp:latest

# With docker-compose
docker-compose up -d
docker-compose down
```

---

## GitHub Actions CI/CD

### Basic Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build
        env:
          VITE_API_URL: ${{ secrets.API_URL }}

      - name: Deploy to Vercel
        if: github.ref == 'refs/heads/main'
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### With Preview Deployments

```yaml
name: Preview

on: [pull_request]

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy Preview
        uses: amondnet/vercel-action@v25
        id: deploy
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}

      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '🚀 Preview deployed to: ${{ steps.deploy.outputs.preview-url }}'
            })
```

---

## Environment Configuration

### Vite

```typescript
// vite.config.ts
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');

  return {
    define: {
      'process.env.API_URL': JSON.stringify(env.VITE_API_URL),
    },
  };
});
```

```bash
# .env.development
VITE_API_URL=http://localhost:8000

# .env.production
VITE_API_URL=https://api.example.com
```

### Next.js

```bash
# .env.local (not committed)
DATABASE_URL=postgresql://localhost:5432/dev

# .env.production
NEXT_PUBLIC_API_URL=https://api.example.com
```

```typescript
// Access in code
// Client-side (must start with NEXT_PUBLIC_)
const apiUrl = process.env.NEXT_PUBLIC_API_URL;

// Server-side only
const dbUrl = process.env.DATABASE_URL;
```

---

## Build Optimization

### Vite Build Analysis

```bash
# Install analyzer
npm i -D rollup-plugin-visualizer

# Add to vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    visualizer({
      filename: 'stats.html',
      open: true,
    }),
  ],
});

# Build and analyze
npm run build
```

### Code Splitting

```typescript
// Route-based splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

// Component splitting
const HeavyChart = lazy(() => import('./components/HeavyChart'));
```

### Caching Strategy

```javascript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
        },
      },
    },
  },
});
```

---

## Health Checks & Monitoring

### Health Check Endpoint

```typescript
// For Docker/Kubernetes
// api/health.ts (Next.js)
export async function GET() {
  return Response.json({ status: 'healthy', timestamp: Date.now() });
}
```

### Error Tracking (Sentry)

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/react';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
});

// Wrap app
const SentryRoutes = Sentry.withSentryReactRouterV6Routing(Routes);
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| 404 on refresh (SPA) | Configure server for SPA fallback |
| Environment vars undefined | Check prefix (VITE_, NEXT_PUBLIC_) |
| Build fails on CI | Check Node version, clear cache |
| Docker image too large | Use multi-stage build, alpine base |
| Slow builds | Enable caching, parallelize |

---

## Deployment Checklist

Before deploying to production:

- [ ] Environment variables set
- [ ] Build succeeds locally
- [ ] Tests pass
- [ ] Security headers configured
- [ ] Error tracking enabled
- [ ] Performance optimized (bundle size, code splitting)
- [ ] SEO meta tags (if applicable)
- [ ] SSL/HTTPS enabled
- [ ] Custom domain configured
- [ ] Health check endpoint working
