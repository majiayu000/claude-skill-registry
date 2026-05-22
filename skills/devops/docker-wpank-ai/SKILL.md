---
model: fast
description: |
  WHAT: Docker containerization expertise - multi-stage builds, image optimization, security hardening, 
  Docker Compose orchestration, and production deployment patterns.
  
  WHEN: User needs Dockerfile optimization, container issues, image size problems, security hardening, 
  networking configuration, Docker Compose setup, or production container deployment.
  
  KEYWORDS: docker, dockerfile, container, image, multi-stage build, docker-compose, 
  image optimization, container security, non-root, health check, volume, network
---

# Docker

Container optimization, security hardening, multi-stage builds, and production deployment patterns.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install docker
```


## NEVER

- **NEVER use `:latest` tag** - Always use specific version tags for reproducibility
- **NEVER run as root** - Create and use non-root users with specific UID/GID
- **NEVER store secrets in images** - Use Docker secrets, env vars at runtime, or secret managers
- **NEVER skip .dockerignore** - Always create comprehensive .dockerignore to reduce build context
- **NEVER install dev dependencies in production** - Use multi-stage builds to separate concerns
- **NEVER leave package manager caches** - Clean in the same RUN layer (`npm ci && npm cache clean --force`)
- **NEVER use `docker-compose` (v1)** - Use `docker compose` (v2) with plugin syntax

## Quick Reference

### Multi-Stage Build Pattern

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Stage 2: Build
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

# Stage 3: Production
FROM node:20-alpine AS runtime
RUN addgroup -g 1001 -S nodejs && adduser -S app -u 1001
WORKDIR /app
COPY --from=deps --chown=app:nodejs /app/node_modules ./node_modules
COPY --from=build --chown=app:nodejs /app/dist ./dist
COPY --from=build --chown=app:nodejs /app/package*.json ./

USER app
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

### Security-Hardened Container

```dockerfile
FROM node:20-alpine

# Create non-root user with specific UID/GID
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

WORKDIR /app

# Copy with ownership
COPY --chown=appuser:appgroup package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER 1001

# At runtime: --cap-drop=ALL --read-only --security-opt=no-new-privileges
```

### Production Docker Compose

```yaml
services:
  app:
    build:
      context: .
      target: production
    depends_on:
      db:
        condition: service_healthy
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB_FILE: /run/secrets/db_name
      POSTGRES_USER_FILE: /run/secrets/db_user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_name
      - db_user
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access

volumes:
  postgres_data:

secrets:
  db_name:
    file: ./secrets/db_name.txt
  db_user:
    file: ./secrets/db_user.txt
  db_password:
    file: ./secrets/db_password.txt
```

### .dockerignore Template

```
# Dependencies
node_modules
.pnpm-store

# Build outputs
dist
build
.next
out

# Development
.git
.gitignore
*.md
LICENSE
docs/

# IDE
.vscode
.idea
*.swp
*.swo

# Testing
coverage
.nyc_output
*.test.js
*.spec.js
__tests__

# Environment
.env*
!.env.example

# Docker
Dockerfile*
docker-compose*
.docker

# Misc
.DS_Store
*.log
tmp
```

## Common Patterns

### Build Cache Optimization

```dockerfile
# Mount build cache for faster rebuilds
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production
```

### Build-Time Secrets

```dockerfile
# BuildKit secrets (never stored in image layers)
FROM alpine
RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) && \
    # Use API_KEY for build process
    echo "Key loaded"
```

```bash
# Build with secret
docker build --secret id=api_key,src=./api_key.txt .
```

### Multi-Architecture Builds

```bash
# Create builder for multi-arch
docker buildx create --name multiarch --use

# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 \
  -t myapp:latest --push .
```

### Development Override

```yaml
# docker-compose.override.yml (auto-loaded in dev)
services:
  app:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules  # Anonymous volume for node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=app:*
    ports:
      - "9229:9229"  # Debug port
    command: npm run dev
```

## Framework-Specific Patterns

### Next.js Production

```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000
CMD ["node", "server.js"]
```

### Python FastAPI

```dockerfile
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

FROM base AS deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runtime
WORKDIR /app
RUN useradd -m -u 1001 appuser
COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --chown=appuser:appuser . .

USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Go Distroless

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server

FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/server /server
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/server"]
```

## Troubleshooting

### Image Size Issues

```bash
# Analyze layers
docker history myapp:latest --no-trunc

# Use dive for detailed analysis
dive myapp:latest

# Check actual size
docker images myapp --format "{{.Size}}"
```

**Common causes:**
- Dev dependencies in production → Use `npm ci --only=production`
- Large base images → Use Alpine or distroless
- Uncleaned caches → Clean in same RUN layer
- Unnecessary files → Improve .dockerignore

### Build Performance

```bash
# Enable BuildKit (faster, better caching)
export DOCKER_BUILDKIT=1

# Build with cache export
docker build --cache-from myapp:latest -t myapp:new .

# Check build cache
docker buildx du
```

### Debugging Containers

```bash
# Shell into running container
docker exec -it <container> sh

# Shell into failed container
docker run -it --entrypoint sh myapp:latest

# Check container logs
docker logs -f <container>

# Inspect container details
docker inspect <container>
```

## Review Checklist

### Dockerfile
- [ ] Multi-stage build separates build/runtime
- [ ] Dependencies copied before source (layer caching)
- [ ] Specific base image tags (no `:latest`)
- [ ] Non-root user with specific UID/GID
- [ ] Package cache cleaned in same RUN layer
- [ ] Health check configured
- [ ] .dockerignore is comprehensive

### Security
- [ ] Runs as non-root user
- [ ] No secrets in image layers
- [ ] Minimal base image (Alpine/distroless)
- [ ] Read-only filesystem where possible
- [ ] Capabilities dropped at runtime

### Docker Compose
- [ ] Health checks with `condition: service_healthy`
- [ ] Resource limits defined
- [ ] Internal networks for backend services
- [ ] Secrets via files, not environment
- [ ] Restart policy configured
