---
name: vercel-deployment
description: "Vercel deployment patterns and best practices. Use when deploying frontend applications, configuring edge functions, setting up preview deployments, or optimizing Next.js applications."
---

# Vercel Deployment

Comprehensive guide for deploying and optimizing applications on Vercel's edge platform.

## When to Use

- Deploying Next.js, React, Vue, or static sites
- Setting up preview deployments for PRs
- Configuring edge and serverless functions
- Optimizing performance with edge caching
- Managing environment variables and secrets
- Setting up custom domains and SSL

## Core Concepts

### Vercel Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Vercel Edge Network                      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Edge Middleware                       │   │
│  │              (Runs at edge, <1ms latency)                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│         ┌────────────────────┼────────────────────┐            │
│         │                    │                    │            │
│         ▼                    ▼                    ▼            │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐      │
│  │   Static    │     │  Serverless │     │    Edge     │      │
│  │   Assets    │     │  Functions  │     │  Functions  │      │
│  │   (CDN)     │     │  (Node.js)  │     │  (V8)       │      │
│  └─────────────┘     └─────────────┘     └─────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Function Types

| Type | Runtime | Cold Start | Use Case |
|------|---------|------------|----------|
| Serverless | Node.js | 250ms | API routes, SSR |
| Edge | V8 | <1ms | Auth, redirects, A/B |
| Static | N/A | 0 | HTML, CSS, JS, images |

## Project Configuration

### vercel.json

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm ci",
  "devCommand": "npm run dev",

  "regions": ["iad1", "sfo1", "cdg1"],

  "functions": {
    "api/**/*.ts": {
      "memory": 1024,
      "maxDuration": 30
    },
    "api/heavy-task.ts": {
      "memory": 3008,
      "maxDuration": 60
    }
  },

  "crons": [
    {
      "path": "/api/cron/daily-cleanup",
      "schedule": "0 0 * * *"
    },
    {
      "path": "/api/cron/hourly-sync",
      "schedule": "0 * * * *"
    }
  ],

  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "*" },
        { "key": "Access-Control-Allow-Methods", "value": "GET,POST,PUT,DELETE,OPTIONS" }
      ]
    },
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ],

  "redirects": [
    {
      "source": "/old-page",
      "destination": "/new-page",
      "permanent": true
    },
    {
      "source": "/blog/:slug",
      "destination": "/posts/:slug",
      "permanent": false
    }
  ],

  "rewrites": [
    {
      "source": "/api/v1/:path*",
      "destination": "https://api.example.com/:path*"
    }
  ]
}
```

### next.config.js (Next.js)

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Output configuration
  output: 'standalone',

  // Image optimization
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'images.example.com',
      },
    ],
    formats: ['image/avif', 'image/webp'],
  },

  // Headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on',
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=63072000; includeSubDomains; preload',
          },
        ],
      },
    ];
  },

  // Rewrites for API proxying
  async rewrites() {
    return [
      {
        source: '/api/external/:path*',
        destination: `${process.env.API_URL}/:path*`,
      },
    ];
  },

  // Experimental features
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
};

module.exports = nextConfig;
```

## Edge Functions

### Edge Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export const config = {
  matcher: [
    // Match all paths except static files
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};

export function middleware(request: NextRequest) {
  const { pathname, searchParams } = request.nextUrl;

  // Authentication check
  const token = request.cookies.get('token')?.value;
  if (pathname.startsWith('/dashboard') && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Geolocation-based routing
  const country = request.geo?.country || 'US';
  if (pathname === '/' && country === 'CN') {
    return NextResponse.redirect(new URL('/cn', request.url));
  }

  // A/B Testing
  const bucket = request.cookies.get('ab-bucket')?.value;
  if (!bucket) {
    const newBucket = Math.random() < 0.5 ? 'control' : 'experiment';
    const response = NextResponse.next();
    response.cookies.set('ab-bucket', newBucket, {
      maxAge: 60 * 60 * 24 * 30, // 30 days
    });
    return response;
  }

  // Rate limiting header
  const response = NextResponse.next();
  response.headers.set('X-Request-Country', country);

  return response;
}
```

### Edge API Route

```typescript
// app/api/edge-function/route.ts
import { NextRequest } from 'next/server';

export const runtime = 'edge';
export const preferredRegion = ['iad1', 'sfo1', 'cdg1'];

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const name = searchParams.get('name') || 'World';

  // Access edge-specific APIs
  const country = request.geo?.country;
  const city = request.geo?.city;

  return Response.json({
    message: `Hello, ${name}!`,
    location: { country, city },
    timestamp: Date.now(),
  });
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  // Process at the edge
  return Response.json({
    received: body,
    processedAt: new Date().toISOString(),
  });
}
```

## Serverless Functions

### API Route (App Router)

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { db } from '@/lib/db';

export const dynamic = 'force-dynamic';
export const maxDuration = 30;

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '10');

    const users = await db.user.findMany({
      skip: (page - 1) * limit,
      take: limit,
      orderBy: { createdAt: 'desc' },
    });

    return NextResponse.json({ users, page, limit });
  } catch (error) {
    console.error('Error fetching users:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const user = await db.user.create({
      data: {
        email: body.email,
        name: body.name,
      },
    });

    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    console.error('Error creating user:', error);
    return NextResponse.json(
      { error: 'Failed to create user' },
      { status: 500 }
    );
  }
}
```

### Dynamic Route Handler

```typescript
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await db.user.findUnique({
    where: { id: params.id },
  });

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(user);
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await request.json();

  const user = await db.user.update({
    where: { id: params.id },
    data: body,
  });

  return NextResponse.json(user);
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  await db.user.delete({
    where: { id: params.id },
  });

  return new NextResponse(null, { status: 204 });
}
```

## Environment Variables

### Variable Types

| Type | Prefix | Accessible |
|------|--------|------------|
| Server | None | Server only |
| Public | `NEXT_PUBLIC_` | Client & Server |
| System | `VERCEL_` | Auto-provided |

### Configuration

```bash
# .env.local (local development)
DATABASE_URL="postgresql://..."
API_SECRET="secret-key"
NEXT_PUBLIC_APP_URL="http://localhost:3000"

# Production (set in Vercel dashboard)
DATABASE_URL="postgresql://prod..."
API_SECRET="prod-secret"
NEXT_PUBLIC_APP_URL="https://myapp.com"
```

### Environment-Specific Variables

```javascript
// Access in code
const dbUrl = process.env.DATABASE_URL;
const appUrl = process.env.NEXT_PUBLIC_APP_URL;

// Vercel system variables
const deploymentUrl = process.env.VERCEL_URL;
const environment = process.env.VERCEL_ENV; // production, preview, development
const gitCommit = process.env.VERCEL_GIT_COMMIT_SHA;
const gitBranch = process.env.VERCEL_GIT_COMMIT_REF;
```

## Preview Deployments

### Branch Configuration

```json
// vercel.json
{
  "git": {
    "deploymentEnabled": {
      "main": true,
      "staging": true,
      "feature/*": true
    }
  }
}
```

### Preview Environment Variables

```bash
# Set different values for preview deployments
# In Vercel Dashboard: Settings > Environment Variables

# Production
DATABASE_URL=postgresql://prod-db/app

# Preview (automatically used for PR deployments)
DATABASE_URL=postgresql://staging-db/app

# Development
DATABASE_URL=postgresql://dev-db/app
```

### Comment on PR

```yaml
# .github/workflows/vercel-preview.yml
name: Vercel Preview
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        id: deploy
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}

      - name: Comment Preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `Preview deployed to: ${{ steps.deploy.outputs.preview-url }}`
            })
```

## Caching & Performance

### Cache Headers

```typescript
// app/api/data/route.ts
export async function GET() {
  const data = await fetchData();

  return Response.json(data, {
    headers: {
      // Cache for 1 hour, revalidate in background
      'Cache-Control': 's-maxage=3600, stale-while-revalidate=86400',
    },
  });
}
```

### ISR (Incremental Static Regeneration)

```typescript
// app/posts/[slug]/page.tsx
export const revalidate = 3600; // Revalidate every hour

export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map((post) => ({ slug: post.slug }));
}

export default async function PostPage({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);
  return <Post post={post} />;
}
```

### On-Demand Revalidation

```typescript
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const { secret, path, tag } = await request.json();

  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ error: 'Invalid secret' }, { status: 401 });
  }

  if (path) {
    revalidatePath(path);
  }

  if (tag) {
    revalidateTag(tag);
  }

  return NextResponse.json({ revalidated: true });
}
```

## Database Connections

### Connection Pooling with Prisma

```typescript
// lib/db.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const db = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query'] : [],
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = db;
}
```

### Vercel Postgres

```typescript
// lib/db.ts
import { sql } from '@vercel/postgres';

export async function getUsers() {
  const { rows } = await sql`SELECT * FROM users`;
  return rows;
}

export async function createUser(email: string, name: string) {
  const { rows } = await sql`
    INSERT INTO users (email, name)
    VALUES (${email}, ${name})
    RETURNING *
  `;
  return rows[0];
}
```

### Vercel KV (Redis)

```typescript
// lib/cache.ts
import { kv } from '@vercel/kv';

export async function cacheGet<T>(key: string): Promise<T | null> {
  return kv.get(key);
}

export async function cacheSet<T>(key: string, value: T, ttl?: number): Promise<void> {
  if (ttl) {
    await kv.set(key, value, { ex: ttl });
  } else {
    await kv.set(key, value);
  }
}

// Rate limiting example
export async function rateLimit(ip: string, limit: number, window: number): Promise<boolean> {
  const key = `rate-limit:${ip}`;
  const current = await kv.incr(key);

  if (current === 1) {
    await kv.expire(key, window);
  }

  return current <= limit;
}
```

## CLI Commands

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Link project
vercel link

# Deploy
vercel                    # Preview deployment
vercel --prod             # Production deployment

# Environment variables
vercel env ls
vercel env add DATABASE_URL production
vercel env pull .env.local

# Domains
vercel domains ls
vercel domains add example.com
vercel domains verify example.com

# Logs
vercel logs
vercel logs --follow

# Secrets (deprecated, use env)
vercel secrets ls

# Project settings
vercel project ls
vercel inspect [deployment-url]

# Rollback
vercel rollback [deployment-url]
```

## Performance Checklist

- [ ] Use Edge Functions for auth/redirects
- [ ] Enable ISR for dynamic content
- [ ] Configure proper cache headers
- [ ] Use `next/image` for images
- [ ] Minimize client-side JavaScript
- [ ] Use streaming where applicable
- [ ] Configure proper regions
- [ ] Set up monitoring (Vercel Analytics)

## Security Checklist

- [ ] Environment variables for secrets
- [ ] CORS headers configured
- [ ] Rate limiting on APIs
- [ ] Input validation
- [ ] CSP headers set
- [ ] No secrets in client code

## Integration

Works with:
- `/react` - Next.js development
- `/devops` - CI/CD pipelines
- `/security` - Security headers
- `/benchmark` - Performance testing
