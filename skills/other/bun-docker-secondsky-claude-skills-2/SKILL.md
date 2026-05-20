---
name: Bun Docker
description: Use for Docker with Bun, Dockerfiles, oven/bun image, containerization, and deployments.
version: 1.0.0
---

# Bun Docker

Deploy Bun applications in Docker containers using official images.

## Official Images

```bash
# Latest stable
docker pull oven/bun

# Specific version
docker pull oven/bun:1.0.0

# Variants
oven/bun:latest       # Full image (~100MB)
oven/bun:slim         # Minimal image (~80MB)
oven/bun:alpine       # Alpine-based (~50MB)
oven/bun:distroless   # Distroless (~60MB)
oven/bun:debian       # Debian-based (~100MB)
```

## Basic Dockerfile

```dockerfile
FROM oven/bun:1 AS base

WORKDIR /app

# Install dependencies
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

# Copy source
COPY . .

# Run
EXPOSE 3000
CMD ["bun", "run", "src/index.ts"]
```

## Multi-Stage Build (Production)

```dockerfile
# Build stage
FROM oven/bun:1 AS builder

WORKDIR /app

COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun run build

# Production stage
FROM oven/bun:1-slim AS production

WORKDIR /app

# Copy only production dependencies
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile --production

# Copy built assets
COPY --from=builder /app/dist ./dist

# Run as non-root
USER bun

EXPOSE 3000
CMD ["bun", "run", "dist/index.js"]
```

## Alpine Image

```dockerfile
FROM oven/bun:1-alpine

WORKDIR /app

# Alpine uses apk for packages
RUN apk add --no-cache git

COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

COPY . .

CMD ["bun", "run", "src/index.ts"]
```

## Distroless Image

```dockerfile
# Build stage
FROM oven/bun:1 AS builder

WORKDIR /app
COPY . .
RUN bun install --frozen-lockfile
RUN bun build src/index.ts --compile --outfile=app

# Runtime stage
FROM gcr.io/distroless/base

COPY --from=builder /app/app /app

ENTRYPOINT ["/app"]
```

## Docker Compose

```yaml
# docker-compose.yml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://db:5432/app
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Hot Reload in Development

```yaml
# docker-compose.dev.yml
version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src
      - ./package.json:/app/package.json
    command: bun --hot run src/index.ts
```

```dockerfile
# Dockerfile.dev
FROM oven/bun:1

WORKDIR /app

COPY package.json bun.lockb ./
RUN bun install

# Source mounted as volume
CMD ["bun", "--hot", "run", "src/index.ts"]
```

## Compiled Binary

```dockerfile
FROM oven/bun:1 AS builder

WORKDIR /app
COPY . .
RUN bun install --frozen-lockfile
RUN bun build src/index.ts --compile --outfile=server

# Minimal runtime
FROM ubuntu:22.04

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/server /usr/local/bin/server

USER nobody
EXPOSE 3000
CMD ["server"]
```

## SQLite with Docker

```dockerfile
FROM oven/bun:1

WORKDIR /app

COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

COPY . .

# Create data directory
RUN mkdir -p /app/data

# Volume for SQLite database
VOLUME /app/data

ENV DATABASE_PATH=/app/data/app.sqlite

CMD ["bun", "run", "src/index.ts"]
```

## Health Checks

```dockerfile
FROM oven/bun:1

WORKDIR /app
COPY . .
RUN bun install --frozen-lockfile

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

CMD ["bun", "run", "src/index.ts"]
```

```typescript
// Health endpoint
app.get("/health", (c) => c.json({ status: "ok" }));
```

## Environment Variables

```dockerfile
FROM oven/bun:1

WORKDIR /app

# Build-time args
ARG NODE_ENV=production
ARG API_URL

# Runtime env
ENV NODE_ENV=${NODE_ENV}
ENV API_URL=${API_URL}

COPY . .
RUN bun install --frozen-lockfile

CMD ["bun", "run", "src/index.ts"]
```

```bash
# Build with args
docker build --build-arg API_URL=https://api.example.com -t myapp .

# Run with env
docker run -e DATABASE_URL=postgres://... myapp
```

## Caching Optimization

```dockerfile
FROM oven/bun:1 AS base

WORKDIR /app

# Cache dependencies separately
FROM base AS deps
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

# Build
FROM deps AS builder
COPY . .
RUN bun run build

# Production
FROM base AS runner
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY package.json ./

USER bun
CMD ["bun", "run", "dist/index.js"]
```

## Security Best Practices

```dockerfile
FROM oven/bun:1-slim

WORKDIR /app

# Don't run as root
USER bun

# Copy with correct ownership
COPY --chown=bun:bun package.json bun.lockb ./
RUN bun install --frozen-lockfile --production

COPY --chown=bun:bun . .

# Read-only filesystem
# (use with: docker run --read-only)

EXPOSE 3000
CMD ["bun", "run", "src/index.ts"]
```

## .dockerignore

```
node_modules
.git
.gitignore
*.md
Dockerfile*
docker-compose*
.env*
.DS_Store
coverage
dist
.bun
```

## Common Commands

```bash
# Build
docker build -t myapp .

# Run
docker run -p 3000:3000 myapp

# Run with env file
docker run --env-file .env -p 3000:3000 myapp

# Interactive shell
docker run -it oven/bun sh

# Check Bun version
docker run oven/bun bun --version
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `bun.lockb not found` | Missing lockfile | Run `bun install` locally |
| `EACCES permission` | File ownership | Use `--chown=bun:bun` |
| `OOM killed` | Memory limit | Increase container memory |
| `No space left` | Large layers | Use multi-stage builds |

## When to Load References

Load `references/optimization.md` when:
- Image size reduction
- Layer caching
- Build performance

Load `references/kubernetes.md` when:
- K8s deployment
- Horizontal scaling
- Service mesh
