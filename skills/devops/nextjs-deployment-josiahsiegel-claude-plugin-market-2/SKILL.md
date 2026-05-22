---
name: nextjs-deployment
description: Complete Next.js deployment system (Next.js 15.5/16). PROACTIVELY activate for: (1) Vercel deployment and configuration, (2) Self-hosted Node.js deployment, (3) Docker containerization, (4) Static export with output:'export', (5) Edge Runtime configuration, (6) Environment variables, (7) CI/CD with GitHub Actions, (8) Health checks and monitoring, (9) Production optimization, (10) Turbopack production builds (Next.js 16). Provides: Dockerfile, docker-compose, PM2 config, vercel.json, GitHub Actions workflows, Turbopack config. Ensures production-ready deployment with proper configuration.
---

## Quick Reference

| Output Mode | Config | Use Case |
|-------------|--------|----------|
| Default | - | Vercel/Node.js hosting |
| Standalone | `output: 'standalone'` | Docker containers |
| Static | `output: 'export'` | Static hosting (no SSR) |

| Platform | Command | Notes |
|----------|---------|-------|
| Vercel | `vercel --prod` | Automatic, recommended |
| Node.js | `npm run build && npm start` | Self-hosted |
| Docker | `docker build -t app .` | Container deployment |
| Static | `npm run build` → `out/` | CDN hosting |

| Runtime | Config | Features |
|---------|--------|----------|
| Node.js | Default | Full features |
| Edge | `export const runtime = 'edge'` | Fast, limited APIs |

| Environment | File | Usage |
|-------------|------|-------|
| Development | `.env.local` | Local dev |
| Production | `.env.production` | Build time |
| Runtime | Platform secrets | Server runtime |

## When to Use This Skill

Use for **deployment and production**:
- Deploying to Vercel (easiest path)
- Self-hosting with Docker or Node.js
- Static export for CDN hosting
- Setting up CI/CD pipelines
- Production configuration and monitoring

**Related skills:**
- For middleware: see `nextjs-middleware`
- For caching in production: see `nextjs-caching`
- For authentication: see `nextjs-authentication`

---

# Next.js Deployment

## Vercel Deployment

### Automatic Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Production deployment
vercel --prod
```

### Environment Variables

```bash
# Set environment variables
vercel env add DATABASE_URL production

# Pull env vars locally
vercel env pull .env.local
```

### vercel.json Configuration

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["iad1", "sfo1"],
  "functions": {
    "app/api/**/*.ts": {
      "memory": 1024,
      "maxDuration": 30
    }
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "*" }
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
      "source": "/api/proxy/:path*",
      "destination": "https://api.example.com/:path*"
    }
  ]
}
```

## Self-Hosted Deployment

### Node.js Server

```bash
# Build the application
npm run build

# Start production server
npm run start
```

### Custom Server

```tsx
// server.ts
import { createServer } from 'http';
import { parse } from 'url';
import next from 'next';

const dev = process.env.NODE_ENV !== 'production';
const hostname = process.env.HOSTNAME || 'localhost';
const port = parseInt(process.env.PORT || '3000', 10);

const app = next({ dev, hostname, port });
const handle = app.getRequestHandler();

app.prepare().then(() => {
  createServer(async (req, res) => {
    try {
      const parsedUrl = parse(req.url!, true);
      await handle(req, res, parsedUrl);
    } catch (err) {
      console.error('Error occurred handling', req.url, err);
      res.statusCode = 500;
      res.end('Internal Server Error');
    }
  })
    .once('error', (err) => {
      console.error(err);
      process.exit(1);
    })
    .listen(port, () => {
      console.log(`> Ready on http://${hostname}:${port}`);
    });
});
```

### PM2 Process Manager

```json
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: 'nextjs-app',
      script: 'npm',
      args: 'start',
      instances: 'max',
      exec_mode: 'cluster',
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 3000,
      },
    },
  ],
};
```

```bash
# Start with PM2
pm2 start ecosystem.config.js

# Monitor
pm2 monit

# Logs
pm2 logs
```

## Docker Deployment

### Dockerfile

```dockerfile
# Dockerfile
FROM node:20-alpine AS base

# Dependencies stage
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

# Builder stage
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

RUN npm run build

# Runner stage
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Automatically leverage output traces
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### next.config.js for Standalone

```tsx
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
};

module.exports = nextConfig;
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - '3000:3000'
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydb
      - NEXTAUTH_SECRET=your-secret
      - NEXTAUTH_URL=http://localhost:3000
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Static Export

### Configuration

```tsx
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  // Optional: Change the output directory
  distDir: 'dist',
  // Optional: Add trailing slashes
  trailingSlash: true,
  // Optional: Disable image optimization
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig;
```

### Build Static Export

```bash
npm run build
# Output in 'out' directory (or distDir if configured)
```

### Limitations

- No Server-Side Rendering
- No API Routes
- No Middleware
- No ISR
- Image Optimization requires external service

## Edge Runtime

### Edge Route Handler

```tsx
// app/api/edge/route.ts
export const runtime = 'edge';

export async function GET(request: Request) {
  return new Response(JSON.stringify({ message: 'Hello from Edge!' }), {
    headers: { 'content-type': 'application/json' },
  });
}
```

### Edge Middleware

```tsx
// middleware.ts
// Runs on Edge by default
import { NextResponse } from 'next/server';

export function middleware(request: Request) {
  return NextResponse.next();
}
```

### Edge Config (Vercel)

```tsx
import { get } from '@vercel/edge-config';

export const runtime = 'edge';

export async function GET() {
  const greeting = await get('greeting');
  return Response.json({ greeting });
}
```

## Production Checklist

### Environment Variables

```bash
# .env.production
DATABASE_URL=
NEXTAUTH_SECRET=
NEXTAUTH_URL=https://myapp.com
NEXT_PUBLIC_API_URL=https://api.myapp.com
```

### next.config.js Production

```tsx
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Strict mode for development
  reactStrictMode: true,

  // Optimize images
  images: {
    domains: ['images.example.com'],
    formats: ['image/avif', 'image/webp'],
  },

  // Security headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
        ],
      },
    ];
  },

  // Redirects
  async redirects() {
    return [
      {
        source: '/old-blog/:slug',
        destination: '/blog/:slug',
        permanent: true,
      },
    ];
  },

  // Experimental features
  experimental: {
    // Enable PPR
    ppr: true,
  },
};

module.exports = nextConfig;
```

### Health Check Endpoint

```tsx
// app/api/health/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Check database connection
    await db.$queryRaw`SELECT 1`;

    return NextResponse.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { status: 'unhealthy', error: 'Database connection failed' },
      { status: 503 }
    );
  }
}
```

## Monitoring

### Error Tracking (Sentry)

```tsx
// next.config.js
const { withSentryConfig } = require('@sentry/nextjs');

const nextConfig = {
  // Your config
};

module.exports = withSentryConfig(nextConfig, {
  silent: true,
  org: 'your-org',
  project: 'your-project',
});
```

```tsx
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
});
```

### Analytics

```tsx
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

## CI/CD

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
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

      - name: Run tests
        run: npm test

      - name: Build
        run: npm run build

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Use output: 'standalone' | Smaller Docker images |
| Set proper env vars | Use Vercel/platform secrets |
| Enable caching | Use CDN, browser caching |
| Monitor performance | Vercel Analytics, Sentry |
| Use health checks | Load balancer integration |
| Enable compression | Gzip/Brotli in reverse proxy |
