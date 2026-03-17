---
name: docker
description: |
  Docker containerization expert: Dockerfile optimization, multi-stage builds, security hardening,
  Docker Compose orchestration, and production deployment. Use for Dockerfile creation/review,
  image size issues, container security, networking, and orchestration.
metadata:
  tags: docker, dockerfile, docker-compose, containers, security, devops
---

# Docker Expert

## When to Use

- Creating or reviewing Dockerfiles
- Optimizing image size or build performance
- Hardening container security
- Setting up Docker Compose for multi-service apps
- Debugging container networking, volumes, or runtime issues
- Containerizing applications (Node.js, Python, Go, Java, Rust)

**Out of scope** (recommend dedicated skills):
- Kubernetes orchestration → kubernetes expert
- CI/CD pipelines → github-actions expert
- Cloud-specific container services (ECS, Cloud Run) → devops expert

## Core Principles

1. **Layer caching** — order layers from least to most frequently changing
2. **Security-first** — non-root users, minimal attack surface, no secrets in layers
3. **Minimal images** — only include what's needed at runtime
4. **Reproducibility** — pin versions, avoid `latest` tag, use lockfiles

## Base Image Selection

**Recommended hierarchy (most to least preferred):**

| Base Image | Size | Shell | Use Case |
|---|---|---|---|
| `cgr.dev/chainguard/*` (Wolfi) | ~10-30MB | Yes | Zero-CVE goal, SBOM included |
| `alpine:3.21` | ~7MB | Yes | General-purpose minimal |
| `gcr.io/distroless/*` | ~2-5MB | No | Hardened production, no debug |
| `*-slim` variants | ~70-100MB | Yes | When Alpine compatibility is an issue |
| `scratch` | 0MB | No | Static binaries (Go, Rust) |

**Rules:**
- Always pin exact versions: `node:22.14.0-alpine3.21` not `node:alpine`
- Never use `latest` — breaks reproducibility
- Match base to actual runtime needs

## Dockerfile Best Practices

### Layer Ordering

```dockerfile
# 1. Base image + system deps (rarely change)
FROM node:22-alpine
RUN apk add --no-cache dumb-init

# 2. Dependencies (change occasionally)
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

# 3. Application code (changes frequently)
COPY . .

# 4. Metadata + runtime config
USER node
EXPOSE 3000
CMD ["dumb-init", "node", "server.js"]
```

### .dockerignore

Always create one to reduce build context:

```
.git
node_modules
__pycache__
*.pyc
.vscode
.idea
.DS_Store
*.log
coverage/
.env
.env.local
dist/
build/
README.md
docs/
```

### BuildKit Cache Mounts

Speed up dependency installation:

```dockerfile
# Node.js
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Python
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Go
RUN --mount=type=cache,target=/go/pkg/mod \
    go build -o /app .
```

Enable with `DOCKER_BUILDKIT=1` or Docker Desktop (on by default).

## Multi-Stage Build Patterns

### Node.js

```dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:22-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:22-alpine AS runtime
RUN addgroup -g 1001 -S app && adduser -S app -u 1001
WORKDIR /app
COPY --from=build --chown=app:app /app/dist ./dist
COPY --from=deps --chown=app:app /app/node_modules ./node_modules
COPY --chown=app:app package.json ./
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

### Python

```dockerfile
FROM python:3.13-slim AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.13-slim AS runtime
RUN useradd -r -u 1001 app
WORKDIR /app
COPY --from=build /install /usr/local
COPY --chown=app:app . .
USER app
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Go

```dockerfile
FROM golang:1.24-alpine AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -ldflags="-s -w" -o /app .

FROM scratch
COPY --from=build /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=build /app /app
USER 65534:65534
EXPOSE 8080
ENTRYPOINT ["/app"]
```

### Java

```dockerfile
FROM eclipse-temurin:21-jdk-alpine AS build
WORKDIR /app
COPY . .
RUN ./gradlew build --no-daemon

FROM eclipse-temurin:21-jre-alpine AS runtime
RUN addgroup -g 1001 -S app && adduser -S app -u 1001
WORKDIR /app
COPY --from=build --chown=app:app /app/build/libs/*.jar app.jar
USER app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD wget -qO- http://localhost:8080/actuator/health || exit 1
CMD ["java", "-jar", "app.jar"]
```

### Rust

```dockerfile
FROM rust:1.84-alpine AS build
RUN apk add --no-cache musl-dev
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs && cargo build --release && rm -rf src
COPY src ./src
RUN cargo build --release

FROM scratch
COPY --from=build /app/target/release/app /app
USER 65534:65534
EXPOSE 8080
ENTRYPOINT ["/app"]
```

## Security Hardening

### Non-Root Users

```dockerfile
# Alpine
RUN addgroup -g 1001 -S app && adduser -S app -u 1001 -G app
USER app

# Debian/Ubuntu
RUN groupadd -g 1001 app && useradd -r -u 1001 -g app app
USER app

# Distroless/scratch (numeric only)
USER 65534:65534
```

### Secrets Management

```dockerfile
# BuildKit secrets (never stored in layers)
RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) && \
    ./configure --api-key="$API_KEY"
```

```bash
# Build with secret
docker build --secret id=api_key,src=./api_key.txt .
```

**Never do:**
```dockerfile
ENV API_KEY=secret123          # Visible in image history
COPY .env /app/.env            # Baked into layer
ARG PASSWORD=hunter2           # Visible in build history
```

### Runtime Hardening

```bash
docker run \
  --user 1001:1001 \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --read-only \
  --tmpfs /tmp:noexec,nosuid \
  --security-opt="no-new-privileges:true" \
  --memory="512m" \
  --cpus="1.0" \
  my-image
```

### Vulnerability Scanning

```bash
# Docker Scout
docker scout quickview my-image
docker scout cves my-image

# Trivy
trivy image my-image

# Grype
grype my-image
```

## Docker Compose

### Production-Ready Pattern

```yaml
services:
  app:
    build:
      context: .
      target: runtime
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.5"
          memory: 256M
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:17-alpine
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

  redis:
    image: redis:7-alpine
    command: redis-server --maxmemory 128mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access

volumes:
  postgres_data:
  redis_data:

secrets:
  db_name:
    file: ./secrets/db_name.txt
  db_user:
    file: ./secrets/db_user.txt
  db_password:
    file: ./secrets/db_password.txt
```

### Network Isolation

```yaml
networks:
  frontend:        # Web-facing services
  backend:
    internal: true # Database, cache — no external access

services:
  proxy:
    networks: [frontend]
  api:
    networks: [frontend, backend]
  db:
    networks: [backend]  # Only reachable from api
```

### Dev vs Prod Overrides

```yaml
# compose.yml (base)
services:
  app:
    build: .

# compose.override.yml (dev, loaded automatically)
services:
  app:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "9229:9229"  # Debug
    environment:
      - NODE_ENV=development
    command: npm run dev

# compose.prod.yml
services:
  app:
    build:
      target: runtime
    environment:
      - NODE_ENV=production
    restart: unless-stopped
```

```bash
# Dev (auto-loads compose.override.yml)
docker compose up

# Prod
docker compose -f compose.yml -f compose.prod.yml up -d
```

## Image Optimization

### Size Reduction Techniques

1. **Multi-stage builds** — don't ship build tools
2. **Minimal base images** — Alpine or distroless
3. **Combine RUN commands** — cleanup in same layer
4. **Copy selectively** — only needed artifacts

```dockerfile
# Bad — 3 layers, cleanup doesn't reduce size
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# Good — 1 layer, cleanup is effective
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

### CMD: Exec Form vs Shell Form

```dockerfile
CMD ["node", "server.js"]   # Exec form — PID 1, receives signals directly
CMD node server.js           # Shell form — spawns /bin/sh, signal issues
```

Always prefer exec form.

## Development Workflow

### Hot Reload Setup

```yaml
services:
  app:
    build:
      target: development
    volumes:
      - .:/app              # Source code
      - /app/node_modules   # Prevent overwrite
    ports:
      - "3000:3000"
      - "9229:9229"         # Debug port
    environment:
      - NODE_ENV=development
      - DEBUG=app:*
    command: npm run dev
```

### Debugging

```yaml
services:
  app:
    # Node.js inspect
    command: node --inspect=0.0.0.0:9229 server.js
    ports:
      - "9229:9229"

    # Python debugpy
    # command: python -m debugpy --listen 0.0.0.0:5678 main.py
    # ports:
    #   - "5678:5678"
```

## Platform-Specific

### Linux

```json
// /etc/docker/daemon.json
{
  "userns-remap": "default",
  "storage-driver": "overlay2",
  "live-restore": true,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

- Use user namespace remapping for added security
- Configure SELinux/AppArmor profiles for production
- Use `overlay2` storage driver

### macOS

```yaml
volumes:
  - ./src:/app/src:delegated  # Better write performance
  - ./build:/app/build:cached  # Container writes cached
```

- Allocate sufficient resources in Docker Desktop
- Use `:delegated`/`:cached` for bind mount performance
- Consider `mutagen` or `docker compose watch` for file sync
- Multi-platform builds for ARM (Apple Silicon)

### Windows

- Prefer **WSL2 backend** for best performance
- Handle line endings: add `.gitattributes` with `* text=auto eol=lf`
- Use forward slashes in Dockerfiles and compose files
- Ensure drives are shared in Docker Desktop settings
- Be aware of file permission differences

```gitattributes
# .gitattributes — prevent CRLF issues in containers
* text=auto eol=lf
*.sh text eol=lf
Dockerfile text eol=lf
```

## Production Checklist

- [ ] Pinned base image version (no `latest`)
- [ ] Multi-stage build separates build and runtime
- [ ] Runs as non-root user
- [ ] No secrets in layers or ENV
- [ ] `.dockerignore` configured
- [ ] Health check implemented
- [ ] Resource limits set (CPU, memory)
- [ ] Logging configured with rotation
- [ ] Vulnerability scan passed
- [ ] Signals handled correctly (exec form CMD, or `dumb-init`/`tini`)
- [ ] Read-only filesystem where possible
- [ ] Capabilities dropped (`--cap-drop=ALL`)

## Anti-Patterns

| Don't | Do Instead |
|---|---|
| Run as root | `USER 1001` or named user |
| Use `latest` tag | Pin exact versions |
| `--privileged` flag | `--cap-add` only what's needed |
| Mount Docker socket | Use Docker-in-Docker or alternatives |
| Hardcode secrets in ENV/ARG | BuildKit secrets or runtime mounts |
| Skip health checks | `HEALTHCHECK` in Dockerfile or Compose |
| Ignore resource limits | Set `memory` and `cpus` limits |
| Copy entire context | Use `.dockerignore` |
| Install unnecessary packages | `--no-install-recommends` |
| Use shell form CMD | Use exec form `["cmd", "arg"]` |

## Diagnostics

### Slow Builds
- Check layer ordering (deps before source)
- Enable BuildKit (`DOCKER_BUILDKIT=1`)
- Use cache mounts for package managers
- Review `.dockerignore` (large build context?)

### Large Images
- Use multi-stage builds
- Switch to Alpine or distroless
- Combine RUN commands with cleanup
- Check `docker history <image>` to find large layers

### Networking Issues
- Verify service names for DNS resolution
- Check network assignments in Compose
- Use `docker network inspect` to debug
- Ensure health checks pass before dependent services start

### Container Crashes
- Check logs: `docker logs <container>`
- Verify signal handling (PID 1 must handle SIGTERM)
- Check resource limits (OOM kills)
- Validate health check endpoints exist
