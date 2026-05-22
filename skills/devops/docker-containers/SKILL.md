---
name: docker-containers
description: "Docker containerization patterns for development and production. Covers Dockerfile best practices, multi-stage builds, docker-compose, and container orchestration."
version: 1.0.0
triggers:
  - docker
  - container
  - dockerfile
  - docker-compose
  - containerize
---

# Docker Containers Skill

Build efficient, secure Docker containers for development and production environments.

## Dockerfile Best Practices

### Node.js Multi-Stage Build

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Security: Run as non-root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built assets
COPY --from=builder /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

USER nextjs
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Next.js Standalone Build

```dockerfile
FROM node:20-alpine AS base

# Dependencies
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Build
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production
FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000
CMD ["node", "server.js"]
```

## Docker Compose Patterns

### Development Environment

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Production with Traefik

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    image: ghcr.io/frankxai/app:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`frankx.ai`)"
      - "traefik.http.routers.app.tls.certresolver=letsencrypt"

  traefik:
    image: traefik:v3.0
    command:
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.email=frank@frankx.ai"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

## .dockerignore

```
# .dockerignore
node_modules
npm-debug.log
.git
.gitignore
.env*
.next
dist
coverage
*.md
!README.md
Dockerfile*
docker-compose*
.dockerignore
```

## Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1
```

```typescript
// app/api/health/route.ts
export async function GET() {
  return Response.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
  });
}
```

## Security Best Practices

```dockerfile
# 1. Use specific versions (not :latest)
FROM node:20.11.0-alpine3.19

# 2. Run as non-root
USER node

# 3. Don't include secrets in image
# Use runtime environment variables or secrets management

# 4. Minimize layers
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*

# 5. Scan for vulnerabilities
# docker scout cves image:tag
```

## Build Commands

```bash
# Build image
docker build -t myapp:latest .

# Build with target stage
docker build --target builder -t myapp:dev .

# Build with cache
docker build --cache-from myapp:latest -t myapp:new .

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest --push .
```

## Docker Compose Commands

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f app

# Execute command in container
docker compose exec app sh

# Stop and remove
docker compose down

# Rebuild and restart
docker compose up -d --build
```

## Anti-Patterns

❌ Using `:latest` tag in production
❌ Running as root
❌ Including dev dependencies in production
❌ Large images (use alpine/slim)
❌ Secrets in Dockerfile or image
❌ Not using .dockerignore

✅ Pin exact versions
✅ Run as non-root user
✅ Multi-stage builds
✅ Minimal base images
✅ Runtime secrets only
✅ Comprehensive .dockerignore
