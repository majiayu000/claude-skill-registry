---
name: shared-ci-cd-docker
description: Docker containerization patterns for Node.js/TypeScript development and production
---

# Docker Containerization Patterns

> **Quick Guide:** Docker Engine 29 with BuildKit for containerizing Node.js/TypeScript applications. Multi-stage builds for minimal production images (1GB to under 100MB). Docker Compose v2 for development environments. BuildKit cache mounts for 10x faster dependency installs. Non-root users, health checks, and secret mounts for production security. Alpine for size, Debian slim for compatibility.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use multi-stage builds for production images - NEVER ship dev dependencies, TypeScript compiler, or source files in production)**

**(You MUST run containers as non-root user - NEVER run production containers as root (default))**

**(You MUST use `CMD ["node", "server.js"]` (exec form) - NEVER use `npm start` or shell form as CMD)**

**(You MUST use BuildKit secret mounts for sensitive data at build time - NEVER use ARG or ENV for secrets)**

**(You MUST copy package.json/lockfile BEFORE source code - NEVER `COPY . .` before `npm ci` (breaks layer cache))**

</critical_requirements>

---

## Examples

- [Dockerfile Patterns](examples/core.md) - Multi-stage builds, Bun, monorepo, layer caching, .dockerignore, signal handling
- [Docker Compose](examples/compose.md) - Development environments, networking, volumes, healthchecks
- [Production & CI/CD](examples/production.md) - Security hardening, secrets, CI/CD pipelines, vulnerability scanning
- [Quick Reference](reference.md) - Dockerfile instructions, CLI commands, base image comparison

---

**Auto-detection:** Dockerfile, docker-compose, compose.yaml, Docker, container, multi-stage build, BuildKit, .dockerignore, Docker Compose, docker build, docker run, HEALTHCHECK, Docker Scout, docker init, containerize, container image, Docker network, Docker volume

**When to use:**

- Creating Dockerfiles for Node.js/TypeScript applications
- Setting up multi-stage builds to minimize production image size
- Configuring Docker Compose for local development environments
- Optimizing Docker layer caching and BuildKit cache mounts
- Implementing container security (non-root, secrets, read-only filesystem)
- Setting up health checks for container orchestration
- Building CI/CD pipelines that build and push Docker images

**When NOT to use:**

- Serverless deployments (AWS Lambda, Vercel Functions) that don't use containers
- Static site hosting (Netlify, Vercel, Cloudflare Pages) with no server runtime
- Local development without containerization requirements
- Kubernetes-specific orchestration patterns (use a Kubernetes skill)

**Key patterns covered:**

- Multi-stage Dockerfile for Node.js/TypeScript (builder pattern)
- Docker Compose v2 development environments
- BuildKit cache mounts and layer optimization
- Container security (non-root, secrets, capabilities, read-only)
- Health checks for production containers
- `.dockerignore` for build context optimization
- Volume mounts (named volumes, bind mounts, tmpfs)
- Docker networking (bridge, host, overlay)
- CI/CD integration (GitHub Actions build-push)
- Signal handling (tini for graceful shutdown)

---

<philosophy>

## Philosophy

Containers provide reproducible, isolated environments that eliminate "works on my machine" problems. Docker is the standard for packaging Node.js/TypeScript applications into portable, lightweight images.

**Core principles:**

1. **Minimal production images** - Ship only what the app needs to run (compiled JS, production deps, runtime)
2. **Layer cache optimization** - Structure Dockerfiles so unchanged layers are reused, making rebuilds fast
3. **Security by default** - Non-root users, no secrets in images, minimal attack surface
4. **Development parity** - Docker Compose mirrors production topology locally

**When to use Docker:**

- Applications deploying to container orchestrators (Kubernetes, ECS, Cloud Run)
- Teams needing consistent development environments across OS platforms
- Microservice architectures requiring isolated services with dependencies
- CI/CD pipelines building reproducible artifacts

**When NOT to use Docker:**

- Pure serverless (Lambda/Vercel Functions) where the platform manages containers
- Static sites deployed to CDNs
- Simple scripts or CLI tools distributed via npm
- When added complexity outweighs the isolation benefit

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Multi-Stage Dockerfile for Node.js/TypeScript

Multi-stage builds compile TypeScript in a builder stage, then copy only compiled JS and production dependencies into a minimal runtime image. This reduces images from 1GB+ to under 100MB.

A production Dockerfile uses three stages:

1. **deps** - Install production dependencies only
2. **builder** - Install all dependencies, compile TypeScript
3. **runner** - Copy compiled output and production deps into minimal image

```dockerfile
# Stage 1: Production dependencies
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev --no-audit --no-fund

# Stage 2: Build TypeScript
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --no-audit --no-fund
COPY tsconfig.json ./
COPY src/ ./src/
RUN npm run build

# Stage 3: Production runtime
FROM node:22-alpine AS runner
WORKDIR /app
RUN apk add --no-cache tini
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser
COPY --from=deps --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist
COPY --chown=appuser:appgroup package.json ./
USER appuser
EXPOSE 3000
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "dist/server.js"]
```

**Why good:** Three-stage build separates concerns, BuildKit cache mount speeds up npm ci, non-root user, tini for signal handling, only production artifacts in final image

See [examples/core.md](examples/core.md) for complete Dockerfiles including Bun and monorepo variants.

---

### Pattern 2: Docker Compose for Development

Docker Compose v2 defines multi-container development environments. Use `compose.yaml` (not `docker-compose.yml`) with the `docker compose` command (no hyphen).

```yaml
# compose.yaml
services:
  app:
    build:
      context: .
      target: builder
    volumes:
      - .:/app:cached
      - /app/node_modules
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:17-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dev"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

**Why good:** Health checks on dependencies with `condition: service_healthy`, bind mount with `:cached` for macOS perf, anonymous volume protects node_modules, named volume for database persistence

See [examples/compose.md](examples/compose.md) for full development environments with Redis, networking, and volume patterns.

---

### Pattern 3: BuildKit Cache Mounts

BuildKit (default since Docker Engine 23+) provides cache mounts that persist package manager caches across builds, reducing install times by 10x or more.

```dockerfile
# npm
RUN --mount=type=cache,target=/root/.npm \
    npm ci --no-audit --no-fund

# pnpm
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile
```

**Layer ordering rules:** Pin base image versions > Copy dependency manifests > Install dependencies > Copy source code > Build/compile. This maximizes cache hits.

See [examples/core.md](examples/core.md) for cache mount patterns for npm, Bun, pnpm, and apt.

---

### Pattern 4: Container Security

#### Non-Root User

```dockerfile
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser
COPY --chown=appuser:appgroup --from=builder /app/dist ./dist
USER appuser
```

#### Secret Mounts (Build Time)

```dockerfile
# Secret is ephemeral - never persisted in image layers
RUN --mount=type=secret,id=npm_token,env=NPM_TOKEN \
    npm ci --no-audit --no-fund
# Build: docker build --secret id=npm_token,env=NPM_TOKEN .
```

#### Runtime Hardening

```yaml
services:
  app:
    read_only: true
    tmpfs: [/tmp]
    security_opt: [no-new-privileges:true]
    cap_drop: [ALL]
```

See [examples/production.md](examples/production.md) for complete production compose, secrets management, and CI/CD pipelines.

---

### Pattern 5: Health Checks

Health checks enable orchestrators to detect unresponsive containers and restart them automatically.

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=30s \
    CMD ["node", "-e", "fetch('http://localhost:3000/health').then(r => { if (!r.ok) process.exit(1) }).catch(() => process.exit(1))"]
```

**Why good:** Uses Node.js built-in fetch (no curl needed in Alpine), start-period allows app startup, checks dedicated health endpoint not just root path

See [examples/production.md](examples/production.md) for health check endpoint implementation and Compose healthcheck patterns.

---

### Pattern 6: .dockerignore

```text
node_modules
dist
.git
.env
.env.*
!.env.example
Dockerfile*
compose.yaml
__tests__
*.test.ts
coverage
.github
```

**Why good:** Excludes node_modules (reinstalled deterministically), .env files (prevents secret leaks), .git (invalidates cache), keeps build context small

See [examples/core.md](examples/core.md) for a comprehensive .dockerignore file.

---

### Pattern 7: Signal Handling and Graceful Shutdown

Node.js as PID 1 does not handle SIGTERM/SIGINT correctly. Use tini as init system.

```dockerfile
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "dist/server.js"]
```

**Why good:** Tini forwards signals to node process, handles zombie process reaping, ensures graceful shutdown on `docker stop`

See [examples/core.md](examples/core.md) for complete TypeScript graceful shutdown implementation.

</patterns>

---

<performance>

## Performance Optimization

### Image Size Reduction

| Technique           | Impact                                   |
| ------------------- | ---------------------------------------- |
| Multi-stage builds  | 1GB to under 100MB (90%+ reduction)      |
| Alpine base image   | 135MB vs 1GB (full) vs 200MB (slim)      |
| `npm ci --omit=dev` | Removes dev dependencies from production |
| `.dockerignore`     | Smaller build context, faster sends      |

### Build Speed Optimization

| Technique                              | Impact                                          |
| -------------------------------------- | ----------------------------------------------- |
| BuildKit cache mounts                  | 10x faster dependency installs                  |
| Layer ordering (deps before source)    | Cache hit on source-only changes                |
| `.dockerignore` excluding node_modules | Prevents sending GBs to daemon                  |
| `--no-audit --no-fund` flags           | Skip unnecessary npm checks                     |
| Parallel multi-stage builds            | BuildKit builds independent stages concurrently |

### CI/CD Build Cache

```yaml
# GitHub Actions - Cache Docker layers
- uses: docker/setup-buildx-action@v3
- uses: docker/build-push-action@v7
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**Why good:** GitHub Actions cache (`type=gha`) persists layers across CI runs, `mode=max` caches all layers (not just final)

</performance>

---

<decision_framework>

## Decision Framework

### Base Image Selection

```
Which base image?
  |
  +-- Need smallest image? --> Alpine (node:22-alpine, ~135MB)
  |     +-- musl libc compatibility issues? --> Use Debian slim instead
  |
  +-- Need maximum compatibility? --> Debian slim (node:22-slim, ~200MB)
  |     +-- Native extensions work out of the box
  |
  +-- Need debugging tools? --> Full image (node:22, ~1GB)
  |     +-- Development only, never for production
  |
  +-- Maximum security? --> Distroless (gcr.io/distroless/nodejs22-debian12)
        +-- No shell, no package manager, smallest attack surface
```

### Compose vs Dockerfile Targets

```
How to manage dev vs prod?
  |
  +-- Multi-stage Dockerfile with targets
  |     +-- `docker compose build --target builder` for dev
  |     +-- Final stage for production
  |
  +-- Separate compose files
        +-- compose.yaml (base)
        +-- compose.override.yaml (dev - auto-loaded)
        +-- compose.prod.yaml (production)
```

### Volume Strategy

```
What data needs to persist?
  |
  +-- Source code (dev hot reload) --> Bind mount with :cached
  +-- Database files --> Named volume
  +-- Temporary/cache data --> tmpfs
  +-- Secrets at runtime --> Docker secrets or tmpfs
  +-- node_modules in dev --> Anonymous volume (protect from host)
```

</decision_framework>

---

<integration>

## Integration Guide

**Works with:**

- **GitHub Actions**: `docker/build-push-action@v7` for CI/CD builds, `docker/setup-buildx-action@v3` for BuildKit
- **GitHub Container Registry (ghcr.io)**: Free private image hosting for GitHub repos
- **Kubernetes**: Production orchestration, pod security contexts, liveness/readiness probes
- **Docker Scout**: `docker scout cves` for vulnerability scanning in CLI and CI
- **Node.js**: Official `node:22-alpine` images, signal handling with tini
- **PostgreSQL/Redis**: Official Alpine images with health checks in Compose

**Replaces / Conflicts with:**

- **Vagrant**: Docker Compose replaces VM-based development environments
- **Manual server provisioning**: Dockerfiles codify environment setup
- **nvm/fnm for Node versions**: Dockerfile pins exact Node version

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Running production containers as root (default behavior - always add USER directive)
- Secrets in ARG/ENV/COPY (persist in image layers - use `--mount=type=secret`)
- Single-stage builds shipping dev dependencies and source code to production
- Using `npm start` as CMD (npm swallows SIGTERM - use `CMD ["node", "dist/server.js"]`)
- No `.dockerignore` file (node_modules sent to daemon, secrets leaked into image)
- Using `:latest` tag for base images (non-deterministic builds)

**Medium Priority Issues:**

- `COPY . .` before `npm ci` (any file change invalidates dependency cache)
- No health check defined (orchestrator cannot detect unresponsive containers)
- `docker-compose.yml` with `version:` key (deprecated - use `compose.yaml` without version)
- `depends_on` without `condition: service_healthy` (container starts before dependency is ready)
- Using `npm install` instead of `npm ci` in Dockerfile (non-deterministic, slower)

**Common Mistakes:**

- Forgetting anonymous volume for node_modules in dev (`/app/node_modules`) causing host to overwrite container's modules
- Not using `:cached` on bind mounts on macOS (significant performance impact)
- Installing build tools (gcc, make, python) in the final stage instead of the builder stage
- Exposing database ports to host in production Compose (only needed for dev)

**Gotchas & Edge Cases:**

- Alpine uses musl libc - some npm packages with native C bindings (bcrypt, sharp, canvas) may fail; use `npm rebuild` or switch to Debian slim
- Node.js `fetch()` is available since Node 18+ (no need for curl in health checks on Alpine)
- BuildKit cache mounts require `# syntax=docker/dockerfile:1` or Docker Engine 23+ with BuildKit enabled by default
- `docker compose down -v` removes named volumes (data loss) - use `docker compose down` without `-v` to preserve data
- Docker Desktop on macOS/Windows has different file system performance than Linux - bind mounts are slower
- `COPY --chown` is more efficient than `COPY` + `RUN chown` (one layer vs two)
- `tini` must be installed explicitly on Alpine (`apk add --no-cache tini`) - it is NOT included by default in `node:alpine` images
- The `node_modules/.cache` directory can grow large in development - add it to `.dockerignore`

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use multi-stage builds for production images - NEVER ship dev dependencies, TypeScript compiler, or source files in production)**

**(You MUST run containers as non-root user - NEVER run production containers as root (default))**

**(You MUST use `CMD ["node", "server.js"]` (exec form) - NEVER use `npm start` or shell form as CMD)**

**(You MUST use BuildKit secret mounts for sensitive data at build time - NEVER use ARG or ENV for secrets)**

**(You MUST copy package.json/lockfile BEFORE source code - NEVER `COPY . .` before `npm ci` (breaks layer cache))**

**Failure to follow these rules will result in bloated images (1GB+), security vulnerabilities (root access, leaked secrets), broken graceful shutdown (lost requests on deploy), and slow CI builds (no layer caching).**

</critical_reminders>
