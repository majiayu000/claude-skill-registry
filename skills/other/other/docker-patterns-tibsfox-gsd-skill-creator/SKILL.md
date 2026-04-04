---
name: docker-patterns
description: Provides Docker and containerization best practices including multi-stage builds, security hardening, and compose patterns. Use when writing Dockerfiles, optimizing images, setting up containers, or when user mentions 'Docker', 'container', 'Dockerfile', 'docker-compose', 'image'.
---

# Docker Patterns

Best practices for building secure, efficient, and production-ready Docker images and compositions.

## Multi-Stage Builds

Multi-stage builds separate build dependencies from runtime, producing smaller and more secure images.

### Node.js / TypeScript

```dockerfile
# Stage 1: Install dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts

# Stage 2: Build
FROM node:20-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build
RUN npm prune --production

# Stage 3: Production
FROM node:20-alpine AS production
WORKDIR /app

RUN addgroup -g 1001 appgroup && \
    adduser -u 1001 -G appgroup -s /bin/sh -D appuser

COPY --from=build --chown=appuser:appgroup /app/dist ./dist
COPY --from=build --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=build --chown=appuser:appgroup /app/package.json ./

USER appuser
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

### Python

```dockerfile
# Stage 1: Build
FROM python:3.12-slim AS build
WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: Production
FROM python:3.12-slim AS production
WORKDIR /app

RUN groupadd -r appgroup && useradd -r -g appgroup -s /sbin/nologin appuser

COPY --from=build /opt/venv /opt/venv
COPY --from=build --chown=appuser:appgroup /app .

ENV PATH="/opt/venv/bin:$PATH"
USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:create_app()"]
```

### Go

```dockerfile
# Stage 1: Build
FROM golang:1.22-alpine AS build
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /server ./cmd/server

# Stage 2: Production (scratch = no OS, minimal attack surface)
FROM scratch AS production

COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=build /server /server

USER 65534:65534
EXPOSE 8080

ENTRYPOINT ["/server"]
```

---

## Layer Caching Optimization

Docker caches each layer. Order instructions from least-frequently-changed to most-frequently-changed.

### Layer Order (Top = Changes Least)

```dockerfile
# 1. Base image              (changes: rarely)
FROM node:20-alpine

# 2. System dependencies     (changes: rarely)
RUN apk add --no-cache dumb-init

# 3. Create user             (changes: never)
RUN adduser -D appuser

# 4. Working directory        (changes: never)
WORKDIR /app

# 5. Package manifests       (changes: occasionally)
COPY package.json package-lock.json ./

# 6. Install dependencies    (changes: occasionally, cached if manifests unchanged)
RUN npm ci

# 7. Application code        (changes: frequently)
COPY . .

# 8. Build step              (changes: frequently)
RUN npm run build

# 9. Runtime config          (changes: rarely)
USER appuser
CMD ["node", "dist/index.js"]
```

### Caching Rules

| Rule | Why |
|------|-----|
| Copy lock files before source code | Dependency install is cached if lock file unchanged |
| Use `npm ci` not `npm install` | Deterministic installs, respects lock file exactly |
| Use `--no-cache-dir` for pip | Avoids storing pip cache in the layer |
| Combine RUN commands with `&&` | Fewer layers, smaller image |
| Use `.dockerignore` | Prevents cache busting from irrelevant file changes |

### What Busts the Cache

| Change | Layers Invalidated |
|--------|-------------------|
| Edit source code | Code COPY and everything after |
| Edit package.json | Dependency install and everything after |
| Change base image tag | Everything |
| Add a new RUN before existing ones | That RUN and everything after |

---

## Security Hardening

### Non-Root User (Required)

Never run containers as root. A compromised container running as root can escalate to host-level access.

```dockerfile
# Alpine
RUN addgroup -g 1001 appgroup && \
    adduser -u 1001 -G appgroup -s /bin/sh -D appuser
USER appuser

# Debian/Ubuntu
RUN groupadd -r appgroup && useradd -r -g appgroup -s /sbin/nologin appuser
USER appuser

# Scratch (numeric user, no user database)
USER 65534:65534
```

### Minimal Base Images

| Base Image | Size | Use Case |
|-----------|------|----------|
| `scratch` | 0 MB | Statically compiled Go binaries |
| `alpine` | ~5 MB | Most applications |
| `distroless` | ~20 MB | When you need glibc but not a shell |
| `slim` | ~80 MB | When alpine causes compatibility issues |
| `full` | ~900 MB | Never in production |

### Secrets Management

**NEVER put secrets in these locations:**

| Location | Why It Is Dangerous |
|----------|-------------------|
| `ENV` instruction | Visible in `docker inspect`, image history, and all child images |
| `ARG` instruction | Visible in build history (`docker history`) |
| `COPY`-ed files | Persists in image layer even if deleted in later layer |
| Build context | Accessible during build if not in `.dockerignore` |

**Safe alternatives:**

```dockerfile
# Runtime secrets via environment variables (set at run time, not build time)
# docker run -e DATABASE_URL=... myapp

# Docker secrets (Swarm/Compose)
# docker secret create db_password ./password.txt

# Mount secrets at build time (BuildKit, not persisted in layers)
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
```

### Security Checklist

- [ ] Running as non-root user
- [ ] Using minimal base image (alpine/distroless/scratch)
- [ ] No secrets in ENV, ARG, or COPY instructions
- [ ] No secrets in build context (check `.dockerignore`)
- [ ] Pinned base image versions (not `latest`)
- [ ] `--no-cache-dir` on package installs
- [ ] Read-only filesystem where possible (`--read-only` flag)
- [ ] No unnecessary packages installed
- [ ] Health check configured
- [ ] Dropped all Linux capabilities not needed (`--cap-drop=ALL`)

### Image Scanning

Scan images for known vulnerabilities before deploying.

```bash
# Docker Scout (built into Docker Desktop)
docker scout cves myimage:latest

# Trivy (open source)
trivy image myimage:latest

# Snyk
snyk container test myimage:latest
```

---

## Health Checks

### Dockerfile HEALTHCHECK

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--interval` | 30s | Time between checks |
| `--timeout` | 30s | Max time for a check to complete |
| `--start-period` | 0s | Grace period for container startup |
| `--retries` | 3 | Consecutive failures before unhealthy |

### Health Check Commands by Stack

| Stack | Command |
|-------|---------|
| Node.js | `wget --spider http://localhost:3000/health` |
| Python | `python -c "import urllib.request; urllib.request.urlopen('http://...')"` |
| Go | Binary built with health endpoint |
| Nginx | `curl -f http://localhost/ \|\| exit 1` |
| PostgreSQL | `pg_isready -U postgres` |
| Redis | `redis-cli ping` |

### Health Endpoint Best Practices

- Return 200 for healthy, 503 for unhealthy
- Check downstream dependencies (database, cache) in the health endpoint
- Keep checks fast (< 1 second)
- Separate liveness (is the process alive?) from readiness (can it serve traffic?)

---

## Docker Compose Patterns

### Development Compose

```yaml
# compose.yaml (development)
services:
  app:
    build:
      context: .
      target: deps  # Stop at dependency stage for dev
    volumes:
      - .:/app
      - /app/node_modules  # Prevent host node_modules from overriding
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    depends_on:
      db:
        condition: service_healthy
    command: npm run dev

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: myapp_dev
      POSTGRES_USER: devuser
      POSTGRES_PASSWORD: devpassword  # Dev only; never use simple passwords in production
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U devuser -d myapp_dev"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  pgdata:
```

### Production Compose

```yaml
# compose.prod.yaml
services:
  app:
    build:
      context: .
      target: production
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    env_file:
      - .env.production  # Secrets loaded from file, not hardcoded
    depends_on:
      db:
        condition: service_healthy
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.5"
    read_only: true
    tmpfs:
      - /tmp
    security_opt:
      - no-new-privileges:true
```

### Compose Best Practices

| Practice | Why |
|----------|-----|
| Use `depends_on` with `condition: service_healthy` | Prevents app starting before dependencies are ready |
| Set resource limits | Prevents one container from consuming all resources |
| Use named volumes for data | Anonymous volumes are hard to manage |
| Use `restart: unless-stopped` in production | Auto-restart on failure, but not after manual stop |
| Separate dev and prod compose files | Different targets, volumes, and security settings |
| Use `read_only: true` where possible | Prevents runtime filesystem modifications |

---

## .dockerignore

Always include a `.dockerignore` to keep the build context small and prevent leaking sensitive files.

```
# Version control
.git
.gitignore

# Dependencies (installed in container)
node_modules
__pycache__
*.pyc
venv/

# Environment and secrets
.env
.env.*
*.pem
*.key
credentials.json

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo

# Build output
dist/
build/
coverage/
*.log

# Docker files (no need to copy into context)
Dockerfile
docker-compose*.yml
compose*.yaml
.dockerignore

# Documentation
*.md
LICENSE
docs/

# Tests (unless needed for build)
tests/
test/
__tests__/
*.test.*
*.spec.*
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Running as root | Container compromise = host compromise | Add non-root user, `USER appuser` |
| Using `latest` tag | Non-reproducible builds | Pin versions: `node:20.11-alpine` |
| Secrets in ENV/ARG | Visible in image metadata and history | Use runtime env vars or Docker secrets |
| Single-stage builds | Large images with build tools in production | Use multi-stage builds |
| No `.dockerignore` | Large context, potential secret leaks | Always include `.dockerignore` |
| `COPY . .` before `npm install` | Cache busted on every code change | Copy package files first, install, then copy code |
| Installing dev dependencies in production | Larger image, larger attack surface | Use `npm ci --omit=dev` or `npm prune --production` |
| No health check | Orchestrator cannot detect unhealthy containers | Add `HEALTHCHECK` instruction |
| Storing data in containers | Data lost when container is removed | Use volumes for persistent data |
| Ignoring image size | Slow pulls, more storage, larger attack surface | Use alpine/distroless, multi-stage, `.dockerignore` |
| `apt-get install` without cleanup | Cached package lists bloat the layer | `apt-get update && apt-get install -y ... && rm -rf /var/lib/apt/lists/*` |
| Using `ADD` instead of `COPY` | `ADD` has magic behavior (auto-extract, URL fetch) | Use `COPY` unless you specifically need `ADD` features |

## Production Readiness Checklist

Before deploying a containerized application:

- [ ] Multi-stage build separates build and runtime
- [ ] Running as non-root user
- [ ] Base image pinned to specific version
- [ ] No secrets baked into the image
- [ ] `.dockerignore` prevents context leaks
- [ ] Health check configured
- [ ] Resource limits set (memory, CPU)
- [ ] Graceful shutdown handled (SIGTERM)
- [ ] Logs written to stdout/stderr (not files)
- [ ] Image scanned for vulnerabilities
- [ ] Read-only filesystem where possible
- [ ] No unnecessary packages or tools installed
