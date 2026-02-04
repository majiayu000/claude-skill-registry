---
name: vercel-deployment
description: Deploy Next.js applications to Vercel with proper configuration. Use when setting up deployment, configuring environment variables, edge functions, or troubleshooting builds. Activates for deployment issues, environment setup, and Vercel configuration.
allowed-tools: Read,Write,Edit,Bash(npm:*,npx:*,vercel:*)
category: DevOps & Site Reliability
tags:
  - devops
  - automation
  - web
  - react
---

# Vercel Deployment

This skill helps you deploy and configure Next.js applications on Vercel following best practices.

## Quick Deploy Checklist

- [ ] Environment variables set in Vercel dashboard
- [ ] Build command configured (default: `next build`)
- [ ] Output directory correct (default: `.next`)
- [ ] Node.js version specified (20.x recommended)
- [ ] Database accessible from Vercel's network
- [ ] Secrets not committed to git

## Environment Variables

### Setting Variables

**Vercel Dashboard** (Recommended for secrets):
1. Project Settings → Environment Variables
2. Add variable with appropriate scope:
   - **Production**: Only production deployments
   - **Preview**: PR and branch previews
   - **Development**: Local `vercel dev`

**Via CLI**:
```bash
vercel env add VARIABLE_NAME production
vercel env pull .env.local  # Pull to local
```

### Variable Naming

```bash
# Server-only (never exposed to browser)
DATABASE_URL=
SESSION_SECRET=
ANTHROPIC_API_KEY=

# Client-exposed (prefixed with NEXT_PUBLIC_)
NEXT_PUBLIC_APP_URL=
NEXT_PUBLIC_ANALYTICS_ID=
```

### Size Limits

| Context | Limit |
|---------|-------|
| Total per deployment | 64 KB |
| Edge Functions | 5 KB per variable |
| Single variable | 64 KB max |

### Required Variables for This Project

```bash
# Authentication (required)
SESSION_SECRET=your-32-char-minimum-secret-here

# AI Integration (required for chat)
ANTHROPIC_API_KEY=sk-ant-api...

# Database (if using external)
DATABASE_URL=file:./data/app.db

# Push Notifications (optional)
VAPID_PUBLIC_KEY=
VAPID_PRIVATE_KEY=
VAPID_SUBJECT=mailto:admin@example.com

# OAuth (optional)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
APPLE_CLIENT_ID=
APPLE_CLIENT_SECRET=
```

## vercel.json Configuration

```json
{
  "buildCommand": "npm run build",
  "framework": "nextjs",
  "regions": ["iad1"],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store, must-revalidate" }
      ]
    },
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/old-path",
      "destination": "/new-path",
      "permanent": true
    }
  ],
  "rewrites": [
    {
      "source": "/api/v1/:path*",
      "destination": "/api/:path*"
    }
  ]
}
```

## TypeScript Configuration (New in 2025)

```typescript
// vercel.ts - Type-safe configuration
import { defineConfig } from '@vercel/config';

export default defineConfig({
  regions: ['iad1'],

  headers: async () => [
    {
      source: '/api/:path*',
      headers: [
        { key: 'Cache-Control', value: 'no-store' },
      ],
    },
  ],

  redirects: async () => [
    {
      source: '/old',
      destination: '/new',
      permanent: true,
    },
  ],
});
```

## Edge Functions

### When to Use Edge

Good for:
- Authentication/authorization
- A/B testing
- Geolocation-based content
- Request/response transforms
- Simple, fast operations

Not suitable for:
- Database connections (use serverless instead)
- Long-running operations
- Large dependencies

### Edge Function Example

```typescript
// src/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export const config = {
  matcher: ['/api/:path*', '/protected/:path*'],
};

export function middleware(request: NextRequest) {
  // Check auth token
  const token = request.cookies.get('session')?.value;

  if (!token && request.nextUrl.pathname.startsWith('/protected')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Add headers
  const response = NextResponse.next();
  response.headers.set('X-Request-Id', crypto.randomUUID());

  return response;
}
```

### Edge Runtime in API Routes

```typescript
// src/app/api/edge-example/route.ts
export const runtime = 'edge';

export async function GET(request: Request) {
  // Limited to edge-compatible APIs
  return Response.json({ timestamp: Date.now() });
}
```

## Build Configuration

### package.json Scripts

```json
{
  "scripts": {
    "build": "next build",
    "postbuild": "npm run db:generate"
  }
}
```

### Build Environment

```bash
# Set Node.js version
# In Vercel Dashboard → Settings → General → Node.js Version
# Or in package.json:
{
  "engines": {
    "node": "20.x"
  }
}
```

### Build Output

```bash
# Check build locally
npm run build

# Analyze bundle
ANALYZE=true npm run build
```

## Database Considerations

### SQLite on Vercel

SQLite with better-sqlite3 works in Vercel's serverless functions, but:
- Filesystem is **read-only** except `/tmp`
- Data doesn't persist between invocations
- Not suitable for production data storage

### Production Database Options

1. **Turso** (SQLite edge database)
   ```typescript
   import { createClient } from '@libsql/client';

   const db = createClient({
     url: process.env.TURSO_DATABASE_URL!,
     authToken: process.env.TURSO_AUTH_TOKEN,
   });
   ```

2. **Vercel Postgres**
   ```typescript
   import { sql } from '@vercel/postgres';

   const result = await sql`SELECT * FROM users`;
   ```

3. **PlanetScale** (MySQL)
4. **Neon** (Postgres)

## Preview Deployments

### Branch Previews

Every git push creates a preview deployment:
- `https://<project>-<branch>-<team>.vercel.app`
- Separate environment variables for preview

### Preview Environment Variables

```bash
# Different values for preview vs production
# In Vercel Dashboard, set both:

DATABASE_URL (Production): postgres://prod-db...
DATABASE_URL (Preview): postgres://staging-db...
```

### Commenting on PRs

Vercel automatically comments on PRs with:
- Preview URL
- Build status
- Performance metrics

## Troubleshooting

### Build Failures

```bash
# Check build locally first
npm run build

# Common issues:
# - Missing environment variables
# - TypeScript errors
# - ESLint errors (strict mode)
# - Missing dependencies
```

### Environment Variable Issues

```bash
# Verify variables are set
vercel env ls

# Pull to local for debugging
vercel env pull .env.local
```

### Function Timeout

```typescript
// Increase timeout (max 60s on Pro, 10s on Hobby)
// In vercel.json:
{
  "functions": {
    "api/long-running.ts": {
      "maxDuration": 60
    }
  }
}
```

### Memory Issues

```typescript
// Increase memory (affects cost)
{
  "functions": {
    "api/heavy-processing.ts": {
      "memory": 1024
    }
  }
}
```

## Monitoring

### Vercel Analytics

```typescript
// src/app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### Speed Insights

```typescript
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  );
}
```

### Function Logs

```bash
# View logs via CLI
vercel logs <deployment-url>

# Real-time logs
vercel logs <deployment-url> --follow
```

## Domains

### Custom Domain Setup

1. Vercel Dashboard → Domains
2. Add domain
3. Configure DNS:
   - A record: `76.76.21.21`
   - Or CNAME: `cname.vercel-dns.com`
4. SSL automatically provisioned

### Redirects

```json
// vercel.json
{
  "redirects": [
    {
      "source": "/:path((?!api/).*)",
      "has": [{ "type": "host", "value": "old-domain.com" }],
      "destination": "https://new-domain.com/:path",
      "permanent": true
    }
  ]
}
```

## Security

### Protected Routes

Use middleware for authentication checks (see Edge Functions above).

### Rate Limiting

Implement application-level rate limiting since Vercel doesn't provide built-in rate limiting for serverless functions.

### Secrets Management

- Never commit `.env` files
- Use Vercel's encrypted environment variables
- Rotate secrets regularly
- Different secrets for preview vs production

## References

- [Vercel Documentation](https://vercel.com/docs)
- [Environment Variables](https://vercel.com/docs/environment-variables)
- [Edge Functions](https://vercel.com/docs/functions/edge-functions)
- [Next.js on Vercel](https://vercel.com/docs/frameworks/nextjs)
