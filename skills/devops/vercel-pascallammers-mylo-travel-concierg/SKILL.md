---
name: vercel
description: Auto-activates when user mentions Vercel, deployment, edge functions, or Vercel hosting. Expert in Vercel platform including deployment, environment variables, Edge Functions, and performance optimization.
category: deployment
---

# Vercel Deployment Skill

**Version**: 1.0.0  
**Last Updated**: 2025-11-16  
**Scope**: Vercel platform deployment, Edge Functions, environment management, performance optimization

---

## Table of Contents

1. [Deployment Configuration](#1-deployment-configuration)
2. [Environment Variables](#2-environment-variables)
3. [Edge Functions & Middleware](#3-edge-functions--middleware)
4. [Domains & DNS](#4-domains--dns)
5. [Analytics & Monitoring](#5-analytics--monitoring)
6. [CI/CD Integration](#6-cicd-integration)
7. [Performance Optimization](#7-performance-optimization)
8. [Security](#8-security)

---

## 1. Deployment Configuration

### 1.1 vercel.json Structure

The `vercel.json` file is the primary configuration file for customizing Vercel deployments. It should be placed at the root of your project.

#### Schema Validation

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json"
}
```

Adding the schema enables autocomplete and validation in modern IDEs.

#### Basic Configuration

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "version": 2,
  "name": "my-awesome-project",
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/node"
    }
  ]
}
```

### 1.2 Build Settings

#### Build Command Override

```json
{
  "buildCommand": "npm run build:production",
  "devCommand": "npm run dev",
  "installCommand": "npm install"
}
```

✅ **Good**: Custom build pipeline
```json
{
  "buildCommand": "prisma generate && next build",
  "installCommand": "npm ci",
  "framework": "nextjs"
}
```

❌ **Bad**: Hardcoded paths or environment-specific commands
```json
{
  "buildCommand": "export NODE_ENV=production && /usr/local/bin/node build.js",
  "installCommand": "rm -rf node_modules && npm install"
}
```

#### Framework Presets

Vercel automatically detects frameworks, but you can override:

```json
{
  "framework": "nextjs",
  "buildCommand": null
}
```

**Supported Frameworks**:
- `nextjs` - Next.js
- `vite` - Vite
- `create-react-app` - Create React App
- `svelte` - Svelte/SvelteKit
- `nuxtjs` - Nuxt.js
- `remix` - Remix
- `astro` - Astro
- `gatsby` - Gatsby
- `hugo` - Hugo
- `jekyll` - Jekyll

### 1.3 Output Directory

```json
{
  "outputDirectory": "dist"
}
```

✅ **Good**: Match your framework's output
```json
{
  "framework": "vite",
  "outputDirectory": "dist"
}
```

❌ **Bad**: Wrong directory for framework
```json
{
  "framework": "nextjs",
  "outputDirectory": "build"
}
```

### 1.4 Monorepo Configuration

#### Turborepo Example

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "buildCommand": "cd ../.. && npx turbo run build --filter=web",
  "outputDirectory": ".next",
  "installCommand": "npm install --prefix=../.."
}
```

#### Nx Monorepo

```json
{
  "buildCommand": "npx nx build web --prod",
  "outputDirectory": "dist/apps/web",
  "installCommand": "npm install"
}
```

✅ **Good**: Proper monorepo setup
```json
{
  "buildCommand": "pnpm turbo build --filter=@myapp/web",
  "installCommand": "pnpm install --frozen-lockfile",
  "outputDirectory": "apps/web/.next",
  "framework": "nextjs"
}
```

❌ **Bad**: Building entire monorepo
```json
{
  "buildCommand": "npm run build",
  "installCommand": "npm install"
}
```

### 1.5 Redirects Configuration

```json
{
  "redirects": [
    {
      "source": "/old-blog/:slug",
      "destination": "/blog/:slug",
      "permanent": true
    },
    {
      "source": "/api/old",
      "destination": "/api/v2/old",
      "permanent": false
    }
  ]
}
```

✅ **Good**: SEO-friendly redirects
```json
{
  "redirects": [
    {
      "source": "/old-path/:path*",
      "destination": "/new-path/:path*",
      "permanent": true,
      "statusCode": 301
    },
    {
      "source": "/:path((?!new-path).*)",
      "has": [
        {
          "type": "host",
          "value": "old-domain.com"
        }
      ],
      "destination": "https://new-domain.com/:path*",
      "permanent": true
    }
  ]
}
```

❌ **Bad**: Redirect loops or wrong status codes
```json
{
  "redirects": [
    {
      "source": "/blog/:slug",
      "destination": "/old-blog/:slug",
      "permanent": true
    },
    {
      "source": "/old-blog/:slug",
      "destination": "/blog/:slug",
      "permanent": true
    }
  ]
}
```

### 1.6 Rewrites Configuration

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.example.com/:path*"
    },
    {
      "source": "/blog/:slug",
      "destination": "/blog/[slug]"
    }
  ]
}
```

✅ **Good**: API proxy pattern
```json
{
  "rewrites": [
    {
      "source": "/api/v1/:path*",
      "destination": "https://backend.example.com/v1/:path*"
    },
    {
      "source": "/sitemap.xml",
      "destination": "/api/sitemap"
    }
  ]
}
```

❌ **Bad**: Exposing internal services
```json
{
  "rewrites": [
    {
      "source": "/admin",
      "destination": "http://internal-admin.local:3000"
    }
  ]
}
```

### 1.7 Headers Configuration

```json
{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "s-maxage=86400, stale-while-revalidate"
        },
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        }
      ]
    }
  ]
}
```

✅ **Good**: Security and caching headers
```json
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
        }
      ]
    },
    {
      "source": "/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

❌ **Bad**: Overly permissive CORS
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        },
        {
          "key": "Access-Control-Allow-Credentials",
          "value": "true"
        }
      ]
    }
  ]
}
```

### 1.8 Functions Configuration

```json
{
  "functions": {
    "api/**/*.ts": {
      "memory": 1024,
      "maxDuration": 10
    },
    "api/heavy-task.ts": {
      "memory": 3008,
      "maxDuration": 60
    }
  }
}
```

✅ **Good**: Optimized per function
```json
{
  "functions": {
    "api/auth/**/*.ts": {
      "memory": 512,
      "maxDuration": 10,
      "regions": ["iad1"]
    },
    "api/image-processing.ts": {
      "memory": 3008,
      "maxDuration": 60,
      "regions": ["sfo1", "iad1"]
    },
    "api/quick/**/*.ts": {
      "memory": 256,
      "maxDuration": 5
    }
  }
}
```

❌ **Bad**: Over-provisioning all functions
```json
{
  "functions": {
    "api/**/*.ts": {
      "memory": 3008,
      "maxDuration": 60
    }
  }
}
```

### 1.9 Regions Configuration

```json
{
  "regions": ["iad1", "sfo1"]
}
```

Available regions:
- `iad1` - Washington, D.C., USA
- `sfo1` - San Francisco, CA, USA
- `pdx1` - Portland, OR, USA
- `gru1` - São Paulo, Brazil
- `lhr1` - London, UK
- `fra1` - Frankfurt, Germany
- `sin1` - Singapore
- `syd1` - Sydney, Australia
- `hnd1` - Tokyo, Japan
- `bom1` - Mumbai, India

✅ **Good**: Target specific user regions
```json
{
  "functions": {
    "api/eu/**/*.ts": {
      "regions": ["lhr1", "fra1"]
    },
    "api/us/**/*.ts": {
      "regions": ["iad1", "sfo1"]
    }
  }
}
```

❌ **Bad**: All regions everywhere (high cost)
```json
{
  "regions": ["iad1", "sfo1", "pdx1", "gru1", "lhr1", "fra1", "sin1", "syd1", "hnd1", "bom1"]
}
```

---

## 2. Environment Variables

### 2.1 Environment Variable Types

Vercel supports three environment scopes:

1. **Production** - Used for production deployments
2. **Preview** - Used for preview deployments (branches, PRs)
3. **Development** - Used locally with `vercel dev`

### 2.2 NEXT_PUBLIC_ Pattern

Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

✅ **Good**: Public API endpoints
```bash
# .env.production
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_ANALYTICS_ID=G-XXXXXXXXXX
NEXT_PUBLIC_APP_VERSION=1.0.0
```

❌ **Bad**: Secrets with NEXT_PUBLIC_
```bash
# .env.production - NEVER DO THIS
NEXT_PUBLIC_DATABASE_URL=postgres://user:password@host/db
NEXT_PUBLIC_API_SECRET=super-secret-key-123
NEXT_PUBLIC_STRIPE_SECRET_KEY=sk_live_xxxxx
```

### 2.3 Server-Only Variables

```bash
# .env
DATABASE_URL=postgres://user:password@host/db
API_SECRET_KEY=secret-key-for-server-only
STRIPE_SECRET_KEY=sk_live_xxxxx
JWT_SECRET=my-jwt-secret
```

### 2.4 Encrypted Variables

Vercel automatically encrypts all environment variables. For sensitive data:

✅ **Good**: Use Vercel environment variables UI
```bash
# Via Vercel Dashboard
# Settings > Environment Variables
# Name: DATABASE_PASSWORD
# Value: super-secret-password
# Scope: Production, Preview
```

❌ **Bad**: Committing secrets
```bash
# .env.local (committed to Git) - NEVER DO THIS
DATABASE_PASSWORD=super-secret-password
API_KEY=secret-key-123
```

### 2.5 System Environment Variables

Vercel provides automatic environment variables:

```typescript
// Available in all environments
process.env.VERCEL // "1"
process.env.VERCEL_ENV // "production" | "preview" | "development"
process.env.VERCEL_URL // "myapp-abc123.vercel.app"
process.env.VERCEL_REGION // "iad1"
process.env.VERCEL_GIT_PROVIDER // "github" | "gitlab" | "bitbucket"
process.env.VERCEL_GIT_REPO_SLUG // "my-repo"
process.env.VERCEL_GIT_REPO_OWNER // "my-org"
process.env.VERCEL_GIT_COMMIT_REF // "main"
process.env.VERCEL_GIT_COMMIT_SHA // "abc123def456"
process.env.VERCEL_GIT_COMMIT_MESSAGE // "feat: add feature"
process.env.VERCEL_GIT_COMMIT_AUTHOR_LOGIN // "username"
```

✅ **Good**: Use system variables for conditional logic
```typescript
export function getBaseUrl() {
  if (process.env.VERCEL_ENV === 'production') {
    return 'https://myapp.com';
  }
  if (process.env.VERCEL_URL) {
    return `https://${process.env.VERCEL_URL}`;
  }
  return 'http://localhost:3000';
}
```

❌ **Bad**: Hardcoding environment detection
```typescript
export function getBaseUrl() {
  if (process.env.NODE_ENV === 'production') {
    return 'https://myapp.com'; // Wrong for preview deployments
  }
  return 'http://localhost:3000';
}
```

### 2.6 Environment Variable Management

#### CLI Commands

```bash
# Pull environment variables to local
vercel env pull .env.local

# Add environment variable
vercel env add DATABASE_URL

# Remove environment variable
vercel env rm DATABASE_URL

# List all environment variables
vercel env ls
```

✅ **Good**: Environment-specific configuration
```bash
# Development
vercel env add NEXT_PUBLIC_API_URL development
# Enter value: http://localhost:8000

# Preview
vercel env add NEXT_PUBLIC_API_URL preview
# Enter value: https://api-staging.example.com

# Production
vercel env add NEXT_PUBLIC_API_URL production
# Enter value: https://api.example.com
```

❌ **Bad**: Same value for all environments
```bash
# All environments
vercel env add NEXT_PUBLIC_API_URL
# Enter value: https://api.example.com
# Scope: Production, Preview, Development
```

### 2.7 Local Development Setup

✅ **Good**: Proper .env file hierarchy
```
.env                # Shared defaults (committed)
.env.local          # Local overrides (NOT committed)
.env.development    # Development defaults (committed)
.env.production     # Production defaults (committed)
```

```bash
# .env (committed)
NEXT_PUBLIC_APP_NAME=MyApp

# .env.local (NOT committed, in .gitignore)
DATABASE_URL=postgres://localhost:5432/mydb
STRIPE_SECRET_KEY=sk_test_xxxxx

# .env.development (committed)
NEXT_PUBLIC_API_URL=http://localhost:8000
LOG_LEVEL=debug

# .env.production (committed)
NEXT_PUBLIC_API_URL=https://api.example.com
LOG_LEVEL=error
```

❌ **Bad**: Single .env file for everything
```bash
# .env (committed) - NEVER DO THIS
DATABASE_URL=postgres://prod-server:5432/mydb
STRIPE_SECRET_KEY=sk_live_xxxxx
NEXT_PUBLIC_API_URL=https://api.example.com
```

### 2.8 Accessing Variables in Code

#### Server-Side (Node.js Runtime)

```typescript
// app/api/users/route.ts
export async function GET() {
  const dbUrl = process.env.DATABASE_URL; // Available server-side only
  const apiKey = process.env.API_SECRET_KEY; // Available server-side only
  
  // ... use variables
  return Response.json({ success: true });
}
```

#### Client-Side (Browser)

```typescript
// app/components/Analytics.tsx
'use client';

export function Analytics() {
  const analyticsId = process.env.NEXT_PUBLIC_ANALYTICS_ID; // Available client-side
  
  // ... initialize analytics
  return null;
}
```

✅ **Good**: Environment-aware configuration
```typescript
// lib/config.ts
const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL,
  isDev: process.env.VERCEL_ENV === 'development',
  isPreview: process.env.VERCEL_ENV === 'preview',
  isProd: process.env.VERCEL_ENV === 'production',
  deploymentUrl: process.env.VERCEL_URL,
};

export default config;
```

❌ **Bad**: Accessing server variables client-side
```typescript
'use client';

export function ClientComponent() {
  // This will be undefined in the browser!
  const dbUrl = process.env.DATABASE_URL;
  
  return <div>{dbUrl}</div>; // undefined
}
```

### 2.9 Secret Management Best Practices

✅ **Good**: Rotate secrets regularly
```bash
# 1. Update in Vercel Dashboard
# 2. Trigger redeployment
vercel --prod

# 3. Verify new secret works
# 4. Invalidate old secret
```

❌ **Bad**: Never rotating secrets
```bash
# Same API key for 3 years - SECURITY RISK
```

✅ **Good**: Use different secrets per environment
```bash
# Production
STRIPE_SECRET_KEY=sk_live_xxxxx

# Preview
STRIPE_SECRET_KEY=sk_test_xxxxx

# Development
STRIPE_SECRET_KEY=sk_test_local_xxxxx
```

❌ **Bad**: Same production secrets in development
```bash
# All environments
STRIPE_SECRET_KEY=sk_live_xxxxx # DANGEROUS!
```

---

## 3. Edge Functions & Middleware

### 3.1 Edge Runtime vs Node.js Runtime

#### Edge Runtime

```typescript
// app/api/edge/route.ts
export const runtime = 'edge';

export async function GET(request: Request) {
  return Response.json({ 
    message: 'Running on Edge',
    region: process.env.VERCEL_REGION 
  });
}
```

**Characteristics**:
- Executes close to users globally
- Starts in <10ms
- Limited to Web APIs (no Node.js APIs)
- 25s execution timeout (streaming: 300s)
- 4MB code size limit

#### Node.js Runtime

```typescript
// app/api/node/route.ts
export const runtime = 'nodejs';

import { readFile } from 'fs/promises';

export async function GET() {
  // Full Node.js API access
  const data = await readFile('./data.json', 'utf-8');
  return Response.json({ data });
}
```

**Characteristics**:
- Full Node.js API access
- Regional execution
- 10s execution timeout (Pro: 60s, Enterprise: 900s)
- 50MB code size limit

### 3.2 Choosing the Right Runtime

✅ **Good**: Edge for low-latency global responses
```typescript
// middleware.ts - Perfect for Edge
export const config = { runtime: 'edge' };

export function middleware(request: Request) {
  const country = request.headers.get('x-vercel-ip-country');
  
  // Fast geo-routing
  if (country === 'US') {
    return NextResponse.rewrite('/us');
  }
  return NextResponse.rewrite('/intl');
}
```

❌ **Bad**: Edge with heavy computation
```typescript
// app/api/heavy/route.ts
export const runtime = 'edge'; // Wrong choice!

export async function POST(request: Request) {
  const data = await request.json();
  
  // Heavy CPU work - should use Node.js runtime
  const result = complexAlgorithm(data); // Might timeout on Edge
  
  return Response.json(result);
}
```

### 3.3 Edge Config

Edge Config is an ultra-low latency data store for the Edge.

```typescript
// lib/edge-config.ts
import { get } from '@vercel/edge-config';

export async function getFeatureFlags() {
  const flags = await get('featureFlags');
  return flags;
}
```

#### vercel.json Configuration

```json
{
  "edgeConfig": "ecfg_xxxxxxxxxxxxx"
}
```

✅ **Good**: Feature flags with Edge Config
```typescript
// middleware.ts
import { get } from '@vercel/edge-config';
import { NextResponse } from 'next/server';

export async function middleware(request: Request) {
  const flags = await get('features');
  const newUIEnabled = flags?.newUI === true;
  
  if (newUIEnabled) {
    return NextResponse.rewrite('/new-ui');
  }
  
  return NextResponse.next();
}
```

❌ **Bad**: Database queries in middleware
```typescript
// middleware.ts
import { sql } from '@vercel/postgres';

export async function middleware(request: Request) {
  // Too slow for middleware!
  const flags = await sql`SELECT * FROM feature_flags`;
  
  return NextResponse.next();
}
```

### 3.4 Next.js Middleware

#### Basic Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  
  // Add custom header
  response.headers.set('x-middleware-version', '1.0');
  
  return response;
}

export const config = {
  matcher: '/api/:path*',
};
```

#### Path Matching

✅ **Good**: Specific path matchers
```typescript
export const config = {
  matcher: [
    '/api/:path*',
    '/dashboard/:path*',
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
```

❌ **Bad**: Running on all paths unnecessarily
```typescript
export const config = {
  matcher: '/:path*', // Runs on EVERYTHING
};
```

### 3.5 Authentication Middleware

✅ **Good**: JWT verification on Edge
```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import { jwtVerify } from 'jose';

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value;
  
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  try {
    const secret = new TextEncoder().encode(process.env.JWT_SECRET);
    await jwtVerify(token, secret);
    
    return NextResponse.next();
  } catch (error) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
};
```

❌ **Bad**: Blocking database calls in middleware
```typescript
// middleware.ts
import { sql } from '@vercel/postgres';

export async function middleware(request: NextRequest) {
  const sessionId = request.cookies.get('session')?.value;
  
  // Too slow for Edge!
  const session = await sql`
    SELECT * FROM sessions WHERE id = ${sessionId}
  `;
  
  return NextResponse.next();
}
```

### 3.6 Geo-location & A/B Testing

✅ **Good**: Geo-based routing
```typescript
// middleware.ts
import { NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const country = request.geo?.country || 'US';
  const city = request.geo?.city;
  
  const response = NextResponse.next();
  
  // Set geo headers for personalization
  response.headers.set('x-user-country', country);
  response.headers.set('x-user-city', city || 'unknown');
  
  // Route EU users differently
  if (['DE', 'FR', 'IT', 'ES'].includes(country)) {
    return NextResponse.rewrite(new URL('/eu', request.url));
  }
  
  return response;
}
```

✅ **Good**: A/B testing with cookies
```typescript
// middleware.ts
import { NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const variant = request.cookies.get('ab-test-variant')?.value;
  
  if (!variant) {
    // Assign random variant
    const newVariant = Math.random() < 0.5 ? 'A' : 'B';
    const response = NextResponse.next();
    response.cookies.set('ab-test-variant', newVariant, {
      maxAge: 60 * 60 * 24 * 30, // 30 days
    });
    
    if (newVariant === 'B') {
      return NextResponse.rewrite(new URL('/variant-b', request.url));
    }
    
    return response;
  }
  
  if (variant === 'B') {
    return NextResponse.rewrite(new URL('/variant-b', request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: '/',
};
```

### 3.7 Request/Response Manipulation

✅ **Good**: Adding security headers
```typescript
// middleware.ts
import { NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  
  // Security headers
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set(
    'Permissions-Policy',
    'camera=(), microphone=(), geolocation=()'
  );
  
  return response;
}
```

✅ **Good**: Request rewriting
```typescript
// middleware.ts
import { NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const url = request.nextUrl;
  
  // Rewrite old URLs to new structure
  if (url.pathname.startsWith('/blog/')) {
    const slug = url.pathname.replace('/blog/', '');
    return NextResponse.rewrite(new URL(`/posts/${slug}`, request.url));
  }
  
  // Mobile subdomain handling
  if (request.headers.get('host')?.startsWith('m.')) {
    return NextResponse.rewrite(new URL(`/mobile${url.pathname}`, request.url));
  }
  
  return NextResponse.next();
}
```

### 3.8 Edge Function Performance

✅ **Good**: Optimized Edge function
```typescript
// app/api/fast/route.ts
export const runtime = 'edge';

export async function GET(request: Request) {
  const url = new URL(request.url);
  const id = url.searchParams.get('id');
  
  // Fast Edge Config lookup
  const data = await get(`item-${id}`);
  
  return Response.json(data, {
    headers: {
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=120',
    },
  });
}
```

❌ **Bad**: Slow database queries on Edge
```typescript
// app/api/slow/route.ts
export const runtime = 'edge';

export async function GET() {
  // Database in distant region = slow!
  const response = await fetch('https://db.us-west.example.com/api/data', {
    method: 'POST',
    body: JSON.stringify({ complex: 'query' }),
  });
  
  return Response.json(await response.json());
}
```

### 3.9 Edge Function Limits

**Size Limits**:
- 4MB total code size (Edge)
- 50MB total code size (Node.js)

**Execution Limits**:
- 25s timeout (Edge, without streaming)
- 300s timeout (Edge, with streaming)
- 10s timeout (Node.js, Hobby)
- 60s timeout (Node.js, Pro)
- 900s timeout (Node.js, Enterprise)

**Memory Limits**:
- 128MB (default)
- 1GB, 2GB, 3GB (configurable)

✅ **Good**: Streaming for long responses
```typescript
// app/api/stream/route.ts
export const runtime = 'edge';

export async function GET() {
  const encoder = new TextEncoder();
  
  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i < 100; i++) {
        controller.enqueue(encoder.encode(`data: ${i}\n\n`));
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      controller.close();
    },
  });
  
  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

---

## 4. Domains & DNS

### 4.1 Custom Domains

#### Adding a Domain

```bash
# Via CLI
vercel domains add example.com

# Via dashboard
# Settings > Domains > Add Domain
```

#### Domain Configuration

```json
{
  "alias": ["www.example.com", "example.com"]
}
```

### 4.2 DNS Configuration

#### A Records (Root Domain)

```
Type: A
Name: @
Value: 76.76.21.21
TTL: 3600
```

#### CNAME Records (Subdomain)

```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 3600
```

✅ **Good**: Proper DNS setup
```
# Root domain
Type: A
Name: @
Value: 76.76.21.21

# WWW subdomain
Type: CNAME
Name: www
Value: cname.vercel-dns.com

# Custom subdomain
Type: CNAME
Name: app
Value: cname.vercel-dns.com
```

❌ **Bad**: Mixed DNS providers
```
# Root at Cloudflare
Type: A (proxied)
Name: @
Value: 76.76.21.21

# WWW at Vercel
Type: CNAME
Name: www
Value: cname.vercel-dns.com
# This causes SSL issues!
```

### 4.3 WWW Redirects

✅ **Good**: Automatic www → non-www redirect
```json
{
  "redirects": [
    {
      "source": "/:path*",
      "has": [
        {
          "type": "host",
          "value": "www.example.com"
        }
      ],
      "destination": "https://example.com/:path*",
      "permanent": true
    }
  ]
}
```

✅ **Good**: Automatic non-www → www redirect
```json
{
  "redirects": [
    {
      "source": "/:path*",
      "has": [
        {
          "type": "host",
          "value": "example.com"
        }
      ],
      "destination": "https://www.example.com/:path*",
      "permanent": true
    }
  ]
}
```

❌ **Bad**: No redirect handling
```json
{
  "alias": ["www.example.com", "example.com"]
}
```

### 4.4 SSL/TLS Certificates

Vercel automatically provisions and renews SSL certificates.

**Features**:
- Automatic Let's Encrypt certificates
- Auto-renewal before expiration
- Wildcard certificates supported
- Custom certificates (Enterprise)

✅ **Good**: Let Vercel handle SSL
```bash
# Just add the domain
vercel domains add example.com

# SSL is automatic!
# Certificate issued within minutes
# Auto-renews every 90 days
```

❌ **Bad**: Managing SSL manually
```bash
# Don't do this - let Vercel handle it
certbot certonly --manual -d example.com
# Upload certificate manually
```

### 4.5 Wildcard Domains

```bash
# Add wildcard domain
vercel domains add *.example.com
```

#### DNS Configuration

```
Type: CNAME
Name: *
Value: cname.vercel-dns.com
TTL: 3600
```

✅ **Good**: Multi-tenant SaaS setup
```typescript
// middleware.ts
import { NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const hostname = request.headers.get('host') || '';
  const subdomain = hostname.split('.')[0];
  
  // Tenant-specific routing
  if (subdomain && subdomain !== 'www') {
    return NextResponse.rewrite(
      new URL(`/tenants/${subdomain}${request.nextUrl.pathname}`, request.url)
    );
  }
  
  return NextResponse.next();
}
```

### 4.6 Domain Verification

Vercel requires verification before using a domain:

1. **TXT Record Method**:
```
Type: TXT
Name: _vercel
Value: vc-domain-verify=xxxxx
TTL: 3600
```

2. **Automatic** (if using Vercel DNS)

### 4.7 Vercel DNS

Benefits of using Vercel as DNS provider:

- Instant propagation
- Automatic configuration
- No manual DNS setup
- Built-in DDoS protection

```bash
# Transfer DNS to Vercel
vercel dns import example.com
```

✅ **Good**: Full Vercel DNS setup
```bash
# 1. Add domain
vercel domains add example.com

# 2. Transfer DNS
vercel dns import example.com

# 3. Update nameservers at registrar
# ns1.vercel-dns.com
# ns2.vercel-dns.com
```

### 4.8 Preview Deployments Domain Pattern

Preview deployments get automatic URLs:

```
https://[project]-[hash]-[team].vercel.app
https://[project]-git-[branch]-[team].vercel.app
https://[project]-[team].vercel.app (production)
```

✅ **Good**: Custom preview domain per branch
```json
{
  "github": {
    "autoAlias": true,
    "silent": false
  }
}
```

This generates:
```
main → https://myapp.com
develop → https://myapp-git-develop-team.vercel.app
feature-x → https://myapp-git-feature-x-team.vercel.app
```

---

## 5. Analytics & Monitoring

### 5.1 Web Analytics

Enable privacy-friendly analytics without cookies.

```bash
# Install
npm install @vercel/analytics

# Add to app
```

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
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

✅ **Good**: Analytics with custom events
```typescript
'use client';

import { track } from '@vercel/analytics';

export function CheckoutButton() {
  const handleCheckout = () => {
    track('checkout_started', {
      value: 99.99,
      currency: 'USD',
    });
    
    // ... checkout logic
  };
  
  return <button onClick={handleCheckout}>Checkout</button>;
}
```

### 5.2 Speed Insights

Monitor Core Web Vitals in real-time.

```bash
npm install @vercel/speed-insights
```

```typescript
// app/layout.tsx
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  );
}
```

**Metrics Tracked**:
- **LCP** (Largest Contentful Paint)
- **FID** (First Input Delay)
- **CLS** (Cumulative Layout Shift)
- **FCP** (First Contentful Paint)
- **TTFB** (Time to First Byte)
- **INP** (Interaction to Next Paint)

✅ **Good**: Custom route monitoring
```typescript
// app/dashboard/page.tsx
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function Dashboard() {
  return (
    <>
      <h1>Dashboard</h1>
      <SpeedInsights route="/dashboard" />
    </>
  );
}
```

### 5.3 Runtime Logs

Access logs via Vercel CLI or Dashboard.

```bash
# Stream logs in real-time
vercel logs --follow

# Filter by function
vercel logs api/hello.ts

# Production logs only
vercel logs --prod

# Last 100 lines
vercel logs --limit 100
```

✅ **Good**: Structured logging
```typescript
// app/api/users/route.ts
export async function GET(request: Request) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    method: request.method,
    url: request.url,
    userAgent: request.headers.get('user-agent'),
  }));
  
  // ... handler logic
  
  console.log(JSON.stringify({
    status: 200,
    duration: 123,
  }));
  
  return Response.json({ success: true });
}
```

❌ **Bad**: Excessive logging
```typescript
export async function GET(request: Request) {
  console.log('Starting request');
  console.log('Got headers');
  console.log('Parsing body');
  console.log('Validating');
  console.log('Processing');
  console.log('Sending response');
  // Too noisy!
  
  return Response.json({ success: true });
}
```

### 5.4 Error Tracking

Integrate with error tracking services.

#### Sentry Integration

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.VERCEL_ENV,
  tracesSampleRate: 1.0,
  integrations: [
    new Sentry.BrowserTracing(),
  ],
});
```

```typescript
// sentry.server.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.VERCEL_ENV,
  tracesSampleRate: 1.0,
});
```

✅ **Good**: Custom error context
```typescript
import * as Sentry from '@sentry/nextjs';

export async function GET(request: Request) {
  try {
    const data = await fetchData();
    return Response.json(data);
  } catch (error) {
    Sentry.captureException(error, {
      tags: {
        section: 'api',
        endpoint: '/api/data',
      },
      contexts: {
        request: {
          url: request.url,
          method: request.method,
        },
      },
    });
    
    return Response.json({ error: 'Internal error' }, { status: 500 });
  }
}
```

### 5.5 Monitoring Performance

#### Real User Monitoring (RUM)

```typescript
// lib/rum.ts
export function reportWebVitals(metric: any) {
  const body = JSON.stringify(metric);
  const url = '/api/analytics';

  if (navigator.sendBeacon) {
    navigator.sendBeacon(url, body);
  } else {
    fetch(url, { body, method: 'POST', keepalive: true });
  }
}
```

```typescript
// app/layout.tsx
import { reportWebVitals } from '@/lib/rum';

export { reportWebVitals };
```

#### Custom Metrics

✅ **Good**: API latency monitoring
```typescript
// app/api/users/route.ts
export async function GET() {
  const start = Date.now();
  
  const data = await db.query('SELECT * FROM users');
  
  const duration = Date.now() - start;
  
  console.log(JSON.stringify({
    metric: 'db_query_duration',
    value: duration,
    query: 'users',
  }));
  
  return Response.json(data);
}
```

### 5.6 Deployment Monitoring

Track deployment success/failure:

```bash
# Via webhook
curl -X POST https://your-monitoring.com/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "event": "deployment",
    "status": "success",
    "url": "https://myapp.com",
    "commit": "abc123"
  }'
```

#### vercel.json Deployment Hooks

```json
{
  "github": {
    "silent": false,
    "autoAlias": true,
    "autoJobCancelation": true
  }
}
```

✅ **Good**: Deployment notifications
```typescript
// app/api/deploy-hook/route.ts
export async function POST(request: Request) {
  const payload = await request.json();
  
  // Send to Slack
  await fetch(process.env.SLACK_WEBHOOK_URL!, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: `🚀 Deployment ${payload.deploymentStatus}`,
      blocks: [
        {
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `*${payload.name}* deployed to production\n<${payload.deploymentUrl}|View Deployment>`,
          },
        },
      ],
    }),
  });
  
  return Response.json({ success: true });
}
```

---

## 6. CI/CD Integration

### 6.1 GitHub Integration

Automatic deployments from GitHub:

1. **Connect Repository**
```bash
vercel link
# or via Dashboard: New Project → Import Git Repository
```

2. **Auto-Deploy Configuration**

```json
{
  "github": {
    "enabled": true,
    "autoAlias": true,
    "silent": false,
    "autoJobCancelation": true
  }
}
```

✅ **Good**: Branch-based deployments
```yaml
# .github/vercel.json
{
  "github": {
    "enabled": true,
    "autoAlias": true,
    "autoJobCancelation": true
  }
}
```

**Behavior**:
- `main` branch → Production deployment
- Other branches → Preview deployments
- Pull requests → Preview deployments with comments

### 6.2 Automatic Deployments

**Triggers**:
- Push to any branch
- Pull request opened/updated
- Manual trigger via `vercel --prod`

✅ **Good**: Controlled production deployments
```json
{
  "github": {
    "enabled": true,
    "autoAlias": true,
    "deploymentEnabled": {
      "main": true,
      "staging": true
    },
    "autoJobCancelation": true
  }
}
```

❌ **Bad**: Every branch to production
```json
{
  "github": {
    "enabled": true,
    "autoAlias": false
  }
}
```

### 6.3 Preview Deployments

Preview deployments are created for:
- Every push to non-production branch
- Every pull request

✅ **Good**: PR preview comments enabled
```
Project Settings → Git → Pull Request Comments: ON
```

This adds comments to PRs:
```
✅ Preview deployment ready!

Built with commit abc123

https://myapp-git-feature-team.vercel.app

Inspect: https://vercel.com/team/myapp/deployments/abc123
```

### 6.4 Production Deployments

```bash
# Deploy to production
vercel --prod

# Deploy specific branch
git checkout main
vercel --prod

# Promote preview to production
vercel promote https://myapp-git-feature-team.vercel.app
```

✅ **Good**: Protected production deployments
```
GitHub Settings → Branch Protection Rules:
- Require pull request reviews
- Require status checks
- Require branches to be up to date
```

### 6.5 Deploy Hooks

Create webhooks to trigger deployments:

```bash
# Create deploy hook
curl -X POST https://api.vercel.com/v1/integrations/deploy/HOOK_ID
```

✅ **Good**: CMS webhook integration
```typescript
// Contentful webhook
POST https://api.vercel.com/v1/integrations/deploy/HOOK_ID

// Triggers deployment on content publish
```

#### vercel.json Deploy Hook Configuration

```json
{
  "github": {
    "enabled": true
  },
  "crons": [
    {
      "path": "/api/rebuild",
      "schedule": "0 0 * * *"
    }
  ]
}
```

### 6.6 Environment-Specific Builds

✅ **Good**: Build commands per environment
```json
{
  "build": {
    "env": {
      "NEXT_PUBLIC_BUILD_ENV": "@environment"
    }
  }
}
```

```typescript
// next.config.js
const buildEnv = process.env.NEXT_PUBLIC_BUILD_ENV;

module.exports = {
  generateBuildId: async () => {
    return `${buildEnv}-${Date.now()}`;
  },
  env: {
    BUILD_ENV: buildEnv,
  },
};
```

### 6.7 Vercel CLI in CI/CD

#### GitHub Actions

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
      - uses: actions/checkout@v3
      
      - name: Install Vercel CLI
        run: npm install -g vercel
      
      - name: Deploy to Vercel
        run: vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
        env:
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
```

✅ **Good**: Full CI pipeline
```yaml
name: CI/CD

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 20
      - run: npm ci
      - run: npm test
      - run: npm run lint
      
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        run: npx vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
        env:
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
```

### 6.8 Deployment Protection

Enable protection for production deployments:

```
Project Settings → Deployment Protection
- Enable Vercel Authentication
- Enable Password Protection
- Enable Trusted IPs
```

✅ **Good**: Staging environment protection
```bash
# Password protect staging deployments
vercel env add PASSWORD_PROTECT staging
# Enter value: secretpassword123
```

---

## 7. Performance Optimization

### 7.1 Edge Caching

Vercel's Edge Network automatically caches responses.

#### Cache-Control Headers

✅ **Good**: Aggressive caching for static assets
```typescript
// app/api/static/route.ts
export async function GET() {
  const data = { version: '1.0.0' };
  
  return Response.json(data, {
    headers: {
      'Cache-Control': 'public, max-age=31536000, immutable',
    },
  });
}
```

✅ **Good**: Stale-while-revalidate for dynamic content
```typescript
// app/api/posts/route.ts
export async function GET() {
  const posts = await db.posts.findMany();
  
  return Response.json(posts, {
    headers: {
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=120',
    },
  });
}
```

❌ **Bad**: No caching headers
```typescript
export async function GET() {
  const data = await fetchExpensiveData();
  return Response.json(data); // No cache!
}
```

### 7.2 ISR (Incremental Static Regeneration)

```typescript
// app/blog/[slug]/page.tsx
export const revalidate = 60; // Revalidate every 60 seconds

export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map((post) => ({ slug: post.slug }));
}

export default async function Post({ params }) {
  const post = await getPost(params.slug);
  return <article>{post.content}</article>;
}
```

✅ **Good**: On-demand revalidation
```typescript
// app/api/revalidate/route.ts
import { revalidatePath } from 'next/cache';

export async function POST(request: Request) {
  const { path, secret } = await request.json();
  
  if (secret !== process.env.REVALIDATE_SECRET) {
    return Response.json({ error: 'Invalid secret' }, { status: 401 });
  }
  
  revalidatePath(path);
  
  return Response.json({ revalidated: true });
}
```

### 7.3 CDN Configuration

Vercel automatically serves all content through its global CDN.

**CDN Regions**: 16+ global edge regions

✅ **Good**: Regional optimization
```json
{
  "regions": ["iad1", "sfo1"],
  "functions": {
    "api/us/**/*.ts": {
      "regions": ["iad1", "sfo1"]
    },
    "api/eu/**/*.ts": {
      "regions": ["lhr1", "fra1"]
    }
  }
}
```

### 7.4 Image Optimization

Next.js Image component automatically optimizes images on Vercel.

```typescript
// app/components/ProductImage.tsx
import Image from 'next/image';

export function ProductImage({ src, alt }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={800}
      height={600}
      quality={85}
      priority={false}
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
    />
  );
}
```

✅ **Good**: Responsive images
```typescript
<Image
  src="/hero.jpg"
  alt="Hero"
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  fill
  style={{ objectFit: 'cover' }}
/>
```

❌ **Bad**: Unoptimized images
```typescript
<img src="/large-image.jpg" alt="Unoptimized" />
```

### 7.5 Font Optimization

```typescript
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-roboto-mono',
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
```

✅ **Good**: Self-hosted fonts
```typescript
import localFont from 'next/font/local';

const myFont = localFont({
  src: './my-font.woff2',
  display: 'swap',
  variable: '--font-custom',
});
```

### 7.6 Code Splitting

Next.js automatically code-splits. Optimize further:

✅ **Good**: Dynamic imports
```typescript
// app/components/HeavyChart.tsx
import dynamic from 'next/dynamic';

const Chart = dynamic(() => import('./Chart'), {
  loading: () => <p>Loading chart...</p>,
  ssr: false,
});

export function HeavyChart() {
  return <Chart data={data} />;
}
```

### 7.7 Bundle Analysis

```bash
# Install
npm install @next/bundle-analyzer

# Configure
```

```javascript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // Next.js config
});
```

```bash
# Run analysis
ANALYZE=true npm run build
```

✅ **Good**: Tree shaking
```typescript
// Import only what you need
import { debounce } from 'lodash-es';

// NOT
import _ from 'lodash';
```

### 7.8 Preloading & Prefetching

```typescript
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <link rel="preconnect" href="https://api.example.com" />
        <link rel="dns-prefetch" href="https://analytics.example.com" />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

✅ **Good**: Route prefetching
```typescript
import Link from 'next/link';

<Link href="/dashboard" prefetch={true}>
  Dashboard
</Link>
```

---

## 8. Security

### 8.1 DDoS Protection

Vercel provides automatic DDoS protection:

- Rate limiting
- Traffic filtering
- Automatic mitigation

### 8.2 Firewall Rules

Configure IP allowlisting/blocklisting:

```
Project Settings → Firewall
- Add IP allowlist
- Add IP blocklist
- Configure rate limits
```

✅ **Good**: Geo-blocking
```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const country = request.geo?.country;
  
  const blockedCountries = ['XX', 'YY'];
  
  if (blockedCountries.includes(country || '')) {
    return new Response('Access denied', { status: 403 });
  }
  
  return NextResponse.next();
}
```

### 8.3 Attack Challenge Mode

Enable challenge for suspicious requests:

```
Project Settings → Security → Attack Challenge Mode: ON
```

### 8.4 Security Headers

✅ **Good**: Complete security headers
```typescript
// next.config.js
module.exports = {
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
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          },
        ],
      },
    ];
  },
};
```

✅ **Good**: Content Security Policy
```typescript
// middleware.ts
const CSP = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self';
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
`;

export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  
  response.headers.set(
    'Content-Security-Policy',
    CSP.replace(/\s{2,}/g, ' ').trim()
  );
  
  return response;
}
```

❌ **Bad**: Unsafe CSP
```typescript
const CSP = `default-src *; script-src * 'unsafe-inline' 'unsafe-eval';`;
```

### 8.5 Authentication & Authorization

✅ **Good**: Middleware-based auth
```typescript
// middleware.ts
import { verifyAuth } from '@/lib/auth';

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token')?.value;
  
  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  const isValid = await verifyAuth(token);
  
  if (!isValid) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
};
```

✅ **Good**: Rate limiting
```typescript
// lib/rate-limit.ts
import { LRUCache } from 'lru-cache';

const rateLimitCache = new LRUCache({
  max: 500,
  ttl: 60000, // 60 seconds
});

export function rateLimit(ip: string, limit: number = 10): boolean {
  const tokenCount = (rateLimitCache.get(ip) as number) || 0;
  
  if (tokenCount >= limit) {
    return false;
  }
  
  rateLimitCache.set(ip, tokenCount + 1);
  return true;
}
```

```typescript
// app/api/protected/route.ts
import { rateLimit } from '@/lib/rate-limit';

export async function POST(request: Request) {
  const ip = request.headers.get('x-forwarded-for') || 'unknown';
  
  if (!rateLimit(ip, 10)) {
    return Response.json({ error: 'Too many requests' }, { status: 429 });
  }
  
  // Process request
  return Response.json({ success: true });
}
```

---

## Conclusion

This Vercel deployment skill covers:

✅ **Deployment Configuration** - vercel.json, builds, monorepos, redirects, headers  
✅ **Environment Variables** - Types, NEXT_PUBLIC_, secrets, system vars  
✅ **Edge Functions & Middleware** - Edge vs Node.js, middleware patterns, geo-routing  
✅ **Domains & DNS** - Custom domains, SSL, wildcards, DNS configuration  
✅ **Analytics & Monitoring** - Web Analytics, Speed Insights, error tracking, logs  
✅ **CI/CD Integration** - GitHub integration, preview deployments, deploy hooks  
✅ **Performance Optimization** - Caching, ISR, CDN, image/font optimization  
✅ **Security** - DDoS protection, firewalls, security headers, CSP  

**Best Practices**:
- Use Edge Functions for global low-latency responses
- Implement proper caching strategies
- Secure environment variables properly
- Monitor performance with Speed Insights
- Enable security headers and CSP
- Optimize images and fonts
- Use ISR for dynamic static content

**Resources**:
- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Edge Functions](https://vercel.com/docs/functions/runtimes/edge)
- [Environment Variables](https://vercel.com/docs/environment-variables)

---

**End of Vercel Deployment Skill** (900+ lines)
