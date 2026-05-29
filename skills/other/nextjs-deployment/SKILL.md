---
name: nextjs-deployment
description: Provides comprehensive patterns for deploying Next.js applications to production. Use when configuring Docker containers, setting up GitHub Actions CI/CD pipelines, managing environment variables, implementing preview deployments, or setting up monitoring and logging for Next.js applications. Covers standalone output, multi-stage Docker builds, health checks, OpenTelemetry instrumentation, and production best practices.
allowed-tools: Read, Write, Edit, Bash
---

# Next.js Deployment

Deploy Next.js applications to production with Docker, CI/CD pipelines, and comprehensive monitoring.

## Overview

This skill provides patterns and code examples for deploying Next.js applications to production environments. It covers containerization with Docker, CI/CD automation with GitHub Actions, environment configuration, health checks, and production monitoring. Use standalone output mode for container deployments, multi-stage Docker builds for optimized images, and OpenTelemetry for observability.

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

### 1. Configure Standalone Output

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'standalone',
  poweredByHeader: false,
  generateBuildId: async () => process.env.GIT_HASH || 'build',
}

export default nextConfig
```

### 2. Create Dockerfile

See [references/docker-patterns.md](references/docker-patterns.md) for complete multi-stage builds, multi-arch support, and optimization.

```dockerfile
# syntax=docker/dockerfile:1
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
ENV NEXT_TELEMETRY_DISABLED=1 NODE_ENV=production
ARG GIT_HASH NEXT_SERVER_ACTIONS_ENCRYPTION_KEY
ENV GIT_HASH=${GIT_HASH} NEXT_SERVER_ACTIONS_ENCRYPTION_KEY=${NEXT_SERVER_ACTIONS_ENCRYPTION_KEY}
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1 PORT=3000 HOSTNAME="0.0.0.0"
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
USER nextjs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => r.statusCode === 200 ? process.exit(0) : process.exit(1))"
CMD ["node", "server.js"]
```

### 3. Set Up GitHub Actions

See [references/github-actions.md](references/github-actions.md) for complete workflows with testing, security scanning, and deployment strategies.

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy
on:
  push:
    branches: [main, develop]

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
      - id: generate-key
        run: echo "key=$(openssl rand -base64 32)" >> $GITHUB_OUTPUT
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            GIT_HASH=${{ github.sha }}
            NEXT_SERVER_ACTIONS_ENCRYPTION_KEY=${{ steps.generate-key.outputs.key }}
```

### 4. Configure Environment Variables

```typescript
// src/lib/env.ts
export function getEnv() {
  return {
    databaseUrl: process.env.DATABASE_URL!,
    apiKey: process.env.API_KEY!,
    publicApiUrl: process.env.NEXT_PUBLIC_API_URL!,
  }
}

export function validateEnv() {
  const required = ['DATABASE_URL', 'API_KEY', 'NEXT_PUBLIC_API_URL']
  const missing = required.filter((key) => !process.env[key])
  if (missing.length > 0) {
    throw new Error(`Missing required environment variables: ${missing.join(', ')}`)
  }
}
```

### 5. Implement Health Checks

```typescript
// src/app/api/health/route.ts
import { NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

export async function GET() {
  const checks = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version || 'unknown',
    uptime: process.uptime(),
  }
  return NextResponse.json(checks)
}
```

### 6. Set Up Monitoring

See [references/monitoring.md](references/monitoring.md) for OpenTelemetry configuration, logging, alerting, and dashboards.

```typescript
// instrumentation.ts
import { registerOTel } from '@vercel/otel'

export function register() {
  registerOTel({
    serviceName: process.env.OTEL_SERVICE_NAME || 'next-app',
  })
}
```

### 7. Handle Server Actions Encryption

**CRITICAL**: Generate and set consistent encryption key for multi-server deployments:

```bash
# Generate key
openssl rand -base64 32

# Set in GitHub Actions Secrets as NEXT_SERVER_ACTIONS_ENCRYPTION_KEY
```

Without this key, Server Actions fail with "Failed to find Server Action" errors in multi-server deployments.

## Best Practices

- **Docker**: Use multi-stage builds, enable standalone output, set non-root user, include health checks
- **Security**: Never commit `.env.local`, use `NEXT_PUBLIC_` only for public values, set `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY`
- **Performance**: Use `output: 'standalone'`, enable CDN for static assets, use `next/image`
- **Environment**: Use same Docker image across environments, inject runtime config via env vars

## Examples

```typescript
// next.config.ts
const nextConfig = {
  output: 'standalone',
  poweredByHeader: false,
  compress: true,
  generateBuildId: async () => process.env.GIT_HASH || 'build',
}
export default nextConfig
```

```yaml
# docker-compose.yml
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

## Constraints and Warnings

### Constraints

- Standalone output requires Node.js 18+
- Server Actions encryption key must be consistent across all instances
- Runtime environment variables only work with `output: 'standalone'`
- OpenTelemetry requires instrumentation.ts at project root

### Warnings

- **Never** use `NEXT_PUBLIC_` prefix for sensitive values
- Always set `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` for multi-server deployments
- Without health checks, orchestrators may send traffic to unhealthy instances
- Runtime env vars don't work with static export (`output: 'export'`)

## References

- **[references/docker-patterns.md](references/docker-patterns.md)** - Advanced Docker configurations, multi-arch builds, optimization
- **[references/github-actions.md](references/github-actions.md)** - Complete CI/CD workflows, testing, security scanning
- **[references/monitoring.md](references/monitoring.md)** - OpenTelemetry, logging, alerting, dashboards
- **[references/deployment-platforms.md](references/deployment-platforms.md)** - Platform-specific guides (Vercel, AWS, GCP, Azure)
