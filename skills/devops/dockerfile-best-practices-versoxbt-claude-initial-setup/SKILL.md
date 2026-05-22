---
name: dockerfile-best-practices
description: >
  Guide for writing production-ready Dockerfiles with multi-stage builds, layer caching,
  security hardening, and optimized image sizes. Use when the user creates a Dockerfile,
  asks about Docker image optimization, mentions container security, or needs help with
  build performance. Trigger whenever Docker or container packaging is discussed.
---

# Dockerfile Best Practices

Write secure, efficient, and maintainable Dockerfiles that produce minimal production images
with proper caching, non-root users, and health checks.

## When to Use
- User creates or modifies a Dockerfile
- User asks about reducing Docker image size
- User mentions container security or hardening
- User has slow Docker builds or cache invalidation issues
- User asks about COPY vs ADD or layer ordering

## Core Patterns

### Multi-Stage Builds

Separate build dependencies from runtime to minimize final image size.

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts
COPY src/ src/
COPY tsconfig.json ./
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS production
WORKDIR /app
RUN addgroup -g 1001 appgroup && \
    adduser -u 1001 -G appgroup -s /bin/sh -D appuser
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/package.json ./
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

### Layer Caching Optimization

Order instructions from least to most frequently changed. Copy dependency manifests
before source code so dependency installs are cached across builds.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# System deps change rarely -- cache this layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Dependencies change occasionally -- cache this layer
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Source code changes frequently -- last layer
COPY . .

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]
```

### Non-Root User

Never run containers as root in production. Create a dedicated user with minimal permissions.

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /server ./cmd/server

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /server /server
USER 65534:65534
ENTRYPOINT ["/server"]
```

### .dockerignore

Always include a .dockerignore to prevent sending unnecessary files to the build context.

```
.git
.github
node_modules
dist
*.md
.env*
.vscode
.idea
docker-compose*.yml
Dockerfile*
coverage
__pycache__
*.pyc
.pytest_cache
```

### Health Checks

Define health checks in the Dockerfile so orchestrators can monitor container health.

```dockerfile
# HTTP health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/healthz || exit 1

# TCP health check (when curl is unavailable)
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD nc -z localhost 8080 || exit 1
```

## Anti-Patterns

- **Using `latest` tag**: Always pin base image versions (`node:20.11-alpine`, not `node:latest`). Unpinned tags cause non-reproducible builds.
- **Running as root**: Never omit the `USER` instruction. Root in a container is root on the host if the container escapes.
- **Using ADD instead of COPY**: ADD auto-extracts archives and fetches URLs, which is unexpected. Use COPY for local files; use `curl` or `wget` explicitly for remote files.
- **Installing dev dependencies in production**: Use `npm ci --omit=dev` or `pip install --no-dev` in the final stage.
- **Single-stage builds**: Shipping compilers, build tools, and source code in production images wastes space and expands the attack surface.
- **Not cleaning up apt/apk cache**: Always add `rm -rf /var/lib/apt/lists/*` after `apt-get install` or use `--no-cache` with `apk add`.

## Quick Reference

| Practice | Do | Don't |
|---|---|---|
| Base image | `node:20-alpine` | `node:latest` |
| Copy files | `COPY . .` | `ADD . .` |
| User | `USER 1001` | (run as root) |
| Install deps | `RUN npm ci` | `RUN npm install` |
| Layer order | deps before source | source before deps |
| Secrets | `--mount=type=secret` | `COPY .env .` |
| Health | `HEALTHCHECK CMD ...` | (no health check) |
| Cache | `rm -rf /var/lib/apt/lists/*` | (leave cache) |
