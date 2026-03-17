---
name: nextjs-deployment
description: Provides comprehensive patterns for deploying Next.js applications to production. Use when configuring Docker containers, setting up GitHub Actions CI/CD pipelines, managing environment variables, implementing preview deployments, or setting up monitoring and logging for Next.js applications. Covers standalone output, multi-stage Docker builds, health checks, OpenTelemetry instrumentation, and production best practices.
allowed-tools: Read, Write, Edit, Bash
---

# Next.js Deployment

Deploy Next.js applications to production with Docker, CI/CD pipelines, and comprehensive monitoring.

## Overview

This skill provides patterns for:
- Docker configuration with multi-stage builds
- GitHub Actions CI/CD pipelines
- Environment variables management (build-time and runtime)
- Preview deployments
- Monitoring with OpenTelemetry
- Logging and health checks
- Production optimization

## When to Use

Activate when user requests involve:
- "Deploy Next.js", "Dockerize Next.js", "containerize"
- "GitHub Actions", "CI/CD pipeline", "automated deployment"
- "Environment variables", "runtime config", "NEXT_PUBLIC"
- "Preview deployment", "staging environment"
- "Monitoring", "OpenTelemetry", "tracing", "logging"
- "Health checks", "readiness", "liveness"
- "Production build", "standalone output"
- "Server Actions encryption key", "NEXT_SERVER_ACTIONS_ENCRYPTION_KEY"

## Quick Reference

### Output Modes

| Mode | Use Case | Command |
|------|----------|---------|
| `standalone` | Docker/container deployment | `output: 'standalone'` |
| `export` | Static site (no server) | `output: 'export'` |
| (default) | Node.js server deployment | `next start` |

### Environment Variable Types

| Prefix | Availability | Use Case |
|--------|--------------|----------|
| `NEXT_PUBLIC_` | Build-time + Browser | Public API keys, feature flags |
| (no prefix) | Server-only | Database URLs, secrets |
| Runtime | Server-only | Different values per environment |

### Key Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Multi-stage container build |
| `.github/workflows/deploy.yml` | CI/CD pipeline |
| `next.config.ts` | Build configuration |
| `instrumentation.ts` | OpenTelemetry setup |
| `src/app/api/health/route.ts` | Health check endpoint |

## Instructions

### Configure Standalone Output

Enable standalone output for optimized Docker deployments:

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'standalone',
  poweredByHeader: false,
  generateBuildId: async () => {
    // Use git hash for consistent builds across servers
    return process.env.GIT_HASH || process.env.GITHUB_SHA || 'build'
  },
}

export default nextConfig
```

### Create Multi-Stage Dockerfile

Build optimized Docker image with minimal footprint:

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN \
  if [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
  elif [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  else echo "Lockfile not found." && exit 1; \
  fi

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Set build-time environment variables
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Generate build ID from git (set during build)
ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH}

# Server Actions encryption key (CRITICAL for multi-server deployments)
ARG NEXT_SERVER_ACTIONS_ENCRYPTION_KEY
ENV NEXT_SERVER_ACTIONS_ENCRYPTION_KEY=${NEXT_SERVER_ACTIONS_ENCRYPTION_KEY}

RUN \
  if [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm run build; \
  elif [ -f yarn.lock ]; then yarn build; \
  elif [ -f package-lock.json ]; then npm run build; \
  else npm run build; \
  fi

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy standalone output
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Copy public files if they exist
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

USER nextjs

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => r.statusCode === 200 ? process.exit(0) : process.exit(1))"

CMD ["node", "server.js"]
```

### Set Up GitHub Actions CI/CD

Create automated build and deployment pipeline:

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      id-token: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Generate Server Actions Key
        id: generate-key
        run: |
          KEY=$(openssl rand -base64 32)
          echo "key=$KEY" >> $GITHUB_OUTPUT

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            GIT_HASH=${{ github.sha }}
            NEXT_SERVER_ACTIONS_ENCRYPTION_KEY=${{ steps.generate-key.outputs.key }}

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      - name: Deploy to staging
        run: |
          echo "Deploying to staging..."
          # Add your deployment commands here
          # e.g., kubectl, helm, or platform-specific CLI

  deploy-production:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com

    steps:
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # Add your deployment commands here
```

### Manage Environment Variables

#### Build-Time Variables (next.config.ts)

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  env: {
    // These are inlined at build time
    APP_VERSION: process.env.npm_package_version || '1.0.0',
    BUILD_DATE: new Date().toISOString(),
  },
  // Public runtime config (available on server and client)
  publicRuntimeConfig: {
    apiUrl: process.env.NEXT_PUBLIC_API_URL,
    featureFlags: {
      newDashboard: process.env.NEXT_PUBLIC_FF_NEW_DASHBOARD === 'true',
    },
  },
}

export default nextConfig
```

#### Runtime Environment Variables

For runtime variables with Docker, use a single image across environments:

```typescript
// src/lib/env.ts
export function getEnv() {
  return {
    // Server-only (read at request time)
    databaseUrl: process.env.DATABASE_URL!,
    apiKey: process.env.API_KEY!,

    // Public (must be prefixed with NEXT_PUBLIC_ at build time)
    publicApiUrl: process.env.NEXT_PUBLIC_API_URL!,
  }
}

// Validate required environment variables
export function validateEnv() {
  const required = ['DATABASE_URL', 'API_KEY', 'NEXT_PUBLIC_API_URL']
  const missing = required.filter((key) => !process.env[key])

  if (missing.length > 0) {
    throw new Error(`Missing required environment variables: ${missing.join(', ')}`)
  }
}
```

#### Environment Variable Files

```bash
# .env.local (development - never commit)
DATABASE_URL=postgresql://localhost:5432/mydb
API_KEY=dev-key
NEXT_PUBLIC_API_URL=http://localhost:3000/api

# .env.production (production defaults)
NEXT_PUBLIC_API_URL=https://api.example.com

# .env.example (template for developers)
DATABASE_URL=
API_KEY=
NEXT_PUBLIC_API_URL=
```

### Implement Health Checks

Create a health check endpoint for load balancers and orchestrators:

```typescript
// src/app/api/health/route.ts
import { NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

export async function GET() {
  const checks = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version || 'unknown',
    buildId: process.env.GIT_HASH || 'unknown',
    uptime: process.uptime(),
    checks: {
      memory: checkMemory(),
      // Add database, cache, etc. checks here
    },
  }

  const isHealthy = Object.values(checks.checks).every((check) => check.status === 'ok')

  return NextResponse.json(checks, {
    status: isHealthy ? 200 : 503
  })
}

function checkMemory() {
  const used = process.memoryUsage()
  const threshold = 1024 * 1024 * 1024 // 1GB

  return {
    status: used.heapUsed < threshold ? 'ok' : 'warning',
    heapUsed: `${Math.round(used.heapUsed / 1024 / 1024)}MB`,
    heapTotal: `${Math.round(used.heapTotal / 1024 / 1024)}MB`,
  }
}
```

### Set Up OpenTelemetry Monitoring

Add observability with OpenTelemetry:

```typescript
// instrumentation.ts
import { registerOTel } from '@vercel/otel'

export function register() {
  registerOTel({
    serviceName: process.env.OTEL_SERVICE_NAME || 'next-app',
    serviceVersion: process.env.npm_package_version,
  })
}
```

```typescript
// instrumentation.node.ts
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http'
import { NodeSDK } from '@opentelemetry/sdk-node'
import { SimpleSpanProcessor } from '@opentelemetry/sdk-trace-node'
import { PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics'
import { resourceFromAttributes } from '@opentelemetry/resources'
import { ATTR_SERVICE_NAME, ATTR_SERVICE_VERSION } from '@opentelemetry/semantic-conventions'

const sdk = new NodeSDK({
  resource: resourceFromAttributes({
    [ATTR_SERVICE_NAME]: process.env.OTEL_SERVICE_NAME || 'next-app',
    [ATTR_SERVICE_VERSION]: process.env.npm_package_version || '1.0.0',
  }),
  spanProcessor: new SimpleSpanProcessor(
    new OTLPTraceExporter({
      url: process.env.OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
    })
  ),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({
      url: process.env.OTEL_EXPORTER_OTLP_METRICS_ENDPOINT,
    }),
  }),
})

sdk.start()

// Graceful shutdown
process.on('SIGTERM', () => {
  sdk.shutdown()
    .then(() => console.log('OpenTelemetry terminated'))
    .catch((err) => console.error('OpenTelemetry termination error', err))
    .finally(() => process.exit(0))
})
```

```typescript
// src/lib/logger.ts
interface LogEntry {
  level: string
  message: string
  timestamp: string
  requestId?: string
  [key: string]: unknown
}

export function createLogger(requestId?: string) {
  const base = {
    timestamp: new Date().toISOString(),
    ...(requestId && { requestId }),
  }

  return {
    info: (message: string, meta?: Record<string, unknown>) => {
      log({ level: 'info', message, ...base, ...meta })
    },
    warn: (message: string, meta?: Record<string, unknown>) => {
      log({ level: 'warn', message, ...base, ...meta })
    },
    error: (message: string, error?: Error, meta?: Record<string, unknown>) => {
      log({
        level: 'error',
        message,
        error: error?.message,
        stack: error?.stack,
        ...base,
        ...meta
      })
    },
  }
}

function log(entry: LogEntry) {
  // In production, send to structured logging service
  // In development, pretty print
  if (process.env.NODE_ENV === 'production') {
    console.log(JSON.stringify(entry))
  } else {
    console.log(`[${entry.level.toUpperCase()}] ${entry.message}`, entry)
  }
}
```

### Configure Preview Deployments

Set up preview environments for pull requests:

```yaml
# .github/workflows/preview.yml
name: Preview Deployment

on:
  pull_request:
    types: [opened, synchronize, closed]

jobs:
  deploy-preview:
    if: github.event.action != 'closed'
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build
        env:
          NEXT_PUBLIC_API_URL: https://staging-api.example.com
          NEXT_PUBLIC_PREVIEW: 'true'

      - name: Deploy to Preview
        run: |
          # Example: Deploy to Vercel, Netlify, or your platform
          # npx vercel --token=${{ secrets.VERCEL_TOKEN }} --prebuilt
          echo "Deploying preview for PR #${{ github.event.number }}"

  cleanup-preview:
    if: github.event.action == 'closed'
    runs-on: ubuntu-latest

    steps:
      - name: Cleanup Preview
        run: |
          echo "Cleaning up preview for PR #${{ github.event.number }}"
```

### Handle Server Actions Encryption

**CRITICAL**: For multi-server deployments, set a consistent encryption key:

```bash
# Generate a key locally
openssl rand -base64 32

# Set in GitHub Actions (Secret)
# NEXT_SERVER_ACTIONS_ENCRYPTION_KEY

# Or generate in workflow (see GitHub Actions example above)
```

```dockerfile
# In Dockerfile - pass as build arg
ARG NEXT_SERVER_ACTIONS_ENCRYPTION_KEY
ENV NEXT_SERVER_ACTIONS_ENCRYPTION_KEY=${NEXT_SERVER_ACTIONS_ENCRYPTION_KEY}
```

Without this key, Server Actions will fail with "Failed to find Server Action" errors in multi-server deployments.

## Best Practices

### Docker Best Practices

1. **Use multi-stage builds** to minimize final image size
2. **Enable standalone output** for production deployments
3. **Set proper permissions** with non-root user
4. **Include health checks** for orchestration platforms
5. **Cache dependencies** in CI/CD for faster builds

### Security Checklist

- Never commit `.env.local` or secrets
- Use `NEXT_PUBLIC_` prefix only for truly public values
- Set `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` for multi-server deployments
- Disable telemetry in production with `NEXT_TELEMETRY_DISABLED=1`
- Remove `poweredByHeader` in production

### Performance Optimization

- Use `output: 'standalone'` for minimal Docker images
- Enable compression at the reverse proxy level
- Configure CDN for static assets
- Use `next/image` for optimized images

### Environment Management

- Use same Docker image across all environments
- Inject runtime configuration via environment variables
- Use different tags for different environments (`latest`, `staging`)
- Implement feature flags for gradual rollouts

## Examples

### Example 1: Complete Production Setup

**Input:** Set up production deployment with Docker and GitHub Actions

**Output:**

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'standalone',
  poweredByHeader: false,
  compress: true,
  generateBuildId: async () => process.env.GIT_HASH || 'build',
  env: {
    APP_VERSION: process.env.npm_package_version,
  },
}

export default nextConfig
```

```dockerfile
# Dockerfile
FROM node:20-alpine AS base

FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production
ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH}
ARG NEXT_SERVER_ACTIONS_ENCRYPTION_KEY
ENV NEXT_SERVER_ACTIONS_ENCRYPTION_KEY=${NEXT_SERVER_ACTIONS_ENCRYPTION_KEY}
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
USER nextjs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => r.statusCode === 200 ? process.exit(0) : process.exit(1))"
CMD ["node", "server.js"]
```

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
      - id: key
        run: echo "key=$(openssl rand -base64 32)" >> $GITHUB_OUTPUT
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          build-args: |
            GIT_HASH=${{ github.sha }}
            NEXT_SERVER_ACTIONS_ENCRYPTION_KEY=${{ steps.key.outputs.key }}
```

### Example 2: Runtime Environment Variables

**Input:** Configure different API URLs for staging and production

**Output:**

```typescript
// src/lib/env.ts
const envSchema = {
  server: {
    DATABASE_URL: process.env.DATABASE_URL!,
    API_SECRET: process.env.API_SECRET!,
  },
  public: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL!,
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME || 'MyApp',
  },
}

export function getServerEnv() {
  return envSchema.server
}

export function getPublicEnv() {
  return envSchema.public
}

// Use in Server Components
import { getServerEnv } from '@/lib/env'

async function fetchData() {
  const env = getServerEnv()
  // Use env.DATABASE_URL
}

// Use in Client Components
import { getPublicEnv } from '@/lib/env'

function ApiClient() {
  const env = getPublicEnv()
  // Use env.NEXT_PUBLIC_API_URL
}
```

```yaml
# docker-compose.yml for local development
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://db:5432/myapp
      - NEXT_PUBLIC_API_URL=http://localhost:3000/api
```

### Example 3: OpenTelemetry Integration

**Input:** Add distributed tracing to Next.js application

**Output:**

```typescript
// instrumentation.ts
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    await import('./instrumentation.node')
  }
}
```

```typescript
// instrumentation.node.ts
import { NodeSDK } from '@opentelemetry/sdk-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { resourceFromAttributes } from '@opentelemetry/resources'
import { ATTR_SERVICE_NAME } from '@opentelemetry/semantic-conventions'

const sdk = new NodeSDK({
  resource: resourceFromAttributes({
    [ATTR_SERVICE_NAME]: process.env.OTEL_SERVICE_NAME || 'next-app',
  }),
  spanProcessor: new SimpleSpanProcessor(
    new OTLPTraceExporter({
      url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
    })
  ),
})

sdk.start()
```

```typescript
// src/app/api/users/route.ts
import { trace } from '@opentelemetry/api'

export async function GET() {
  const tracer = trace.getTracer('next-app')

  return tracer.startActiveSpan('fetch-users', async (span) => {
    try {
      const users = await db.user.findMany()
      span.setAttribute('user.count', users.length)
      return NextResponse.json(users)
    } catch (error) {
      span.recordException(error as Error)
      throw error
    } finally {
      span.end()
    }
  })
}
```

## Constraints and Warnings

### Constraints

- Standalone output requires Node.js 18+
- Server Actions encryption key must be consistent across all instances
- Runtime environment variables only work with `output: 'standalone'`
- Health checks need explicit route handler
- OpenTelemetry requires instrumentation.ts at project root

### Warnings

- **Never** use `NEXT_PUBLIC_` prefix for sensitive values
- Always set `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` for multi-server deployments
- Without health checks, orchestrators may send traffic to unhealthy instances
- Runtime env vars don't work with static export (`output: 'export'`)
- Cache build artifacts in CI/CD to speed up builds

## References

Consult these files for detailed patterns:

- **[references/docker-patterns.md](references/docker-patterns.md)** - Advanced Docker configurations, multi-arch builds, optimization
- **[references/github-actions.md](references/github-actions.md)** - Complete CI/CD workflows, testing, security scanning
- **[references/monitoring.md](references/monitoring.md)** - OpenTelemetry, logging, alerting, dashboards
- **[references/deployment-platforms.md](references/deployment-platforms.md)** - Platform-specific guides (Vercel, AWS, GCP, Azure)
