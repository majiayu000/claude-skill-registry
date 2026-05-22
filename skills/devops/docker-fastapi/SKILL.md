---
name: docker-fastapi
description: Comprehensive Docker containerization for Python/FastAPI applications from development to production deployments. Use when Claude needs to containerize Python/FastAPI applications with proper multi-stage builds, production-ready configurations, security best practices, and optimized Docker images for deployment to cloud platforms or container orchestration systems.
---

# Docker FastAPI

## Overview

This skill provides comprehensive guidance for containerizing Python/FastAPI applications using Docker. It includes best practices for Dockerfile creation, multi-stage builds, production configurations, security hardening, and deployment strategies from development to production environments.

## Decision Hierarchy

When optimizing containers, resolve conflicts in this order:

1. **Security** (non-negotiable): Non-root user (UID 10001+), no secrets in image, health checks
2. **Runtime Size** (beats build speed): Multi-stage builds even if slower to build
3. **Operational Clarity** (beats cleverness): Explicit over implicit, predictable behavior
4. **Build Speed** (when above are satisfied): UV package manager, layer caching

## Core Capabilities

### 1. Dockerfile Generation
- **Development Dockerfiles**: Fast feedback loops with hot-reloading
- **Production Dockerfiles**: Optimized, secure, minimal images using multi-stage builds
- **Security-focused**: Non-root users (UID 10001+), minimal base images, no shell access
- **Performance-optimized**: Layer caching, UV official images, dependency optimization
- **Best Practice Compliant**: Proper instruction ordering, comprehensive comments, .dockerignore generation

### 2. Multi-stage Build Patterns (P1: Always Use Multi-Stage)
- **Builder Stage**: Has compilers, dev tools, UV package manager
- **Runtime Stage**: Minimal production image, no build tools, no UV
- **Layer Optimization**: Efficient caching and reduced image sizes

### 3. Production Deployment Patterns
- **Process Management**: Proper process managers (gunicorn, uvicorn) for FastAPI
- **Resource Management**: Memory and CPU constraints
- **Health Checks**: Native Python health checks (no curl dependency)
- **Environment Configuration**: Proper environment variable handling

### 4. Build Principles

**P1: Multi-Stage Always** - Even if current deps don't require compilation, future deps might.

**P2: Layer Order Matters** - Copy dependency files first, install, then copy source:
```dockerfile
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache
COPY src/ ./src/
```

**P3: Single RUN for Related Operations** - Combine related commands to reduce layers:
```dockerfile
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /sbin/nologin appuser && \
    chown -R appuser:appgroup /app
```

## Quick Start Guide

### Production Multi-stage Build (Recommended)

For production deployments with optimized security and size:

```dockerfile
# syntax=docker/dockerfile:1

# ============================================
# BUILD STAGE - Has UV, compilers, dev tools
# ============================================
FROM ghcr.io/astral-sh/uv:python3.12-slim AS builder

WORKDIR /app

# P2: Dependency files first (changes less frequently)
COPY pyproject.toml uv.lock ./

# P3: Install deps into virtual env, not system Python
RUN uv sync --frozen --no-cache --no-dev

# P2: Source code last (changes most frequently)
COPY src/ ./src/
COPY main.py ./

# ============================================
# RUNTIME STAGE - Minimal, no build tools
# ============================================
FROM python:3.12-slim AS runtime

WORKDIR /app

# Runtime environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# P3: User setup in single layer with secure defaults
# UID 10001+ for Kubernetes pod security compliance
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /sbin/nologin appuser && \
    mkdir -p /app && \
    chown -R appuser:appgroup /app

# P1: Copy only runtime artifacts from builder (no UV, no build tools)
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/src /app/src
COPY --from=builder --chown=appuser:appgroup /app/main.py /app/

# Switch to non-root user (use numeric UID for portability)
USER 10001

EXPOSE 8000

# Health check using Python (no curl needed - smaller attack surface)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Production command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### With Gunicorn Workers (High Traffic)

```dockerfile
# syntax=docker/dockerfile:1

# ============================================
# BUILD STAGE
# ============================================
FROM ghcr.io/astral-sh/uv:python3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --no-dev

COPY src/ ./src/
COPY main.py ./

# ============================================
# RUNTIME STAGE
# ============================================
FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    WORKERS=4 \
    TIMEOUT=120 \
    KEEP_ALIVE=5 \
    MAX_REQUESTS=1000 \
    MAX_REQUESTS_JITTER=100

RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /sbin/nologin appuser && \
    mkdir -p /app && \
    chown -R appuser:appgroup /app

COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/src /app/src
COPY --from=builder --chown=appuser:appgroup /app/main.py /app/

USER 10001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["sh", "-c", "gunicorn main:app --workers ${WORKERS} --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout ${TIMEOUT} --keep-alive ${KEEP_ALIVE} --max-requests ${MAX_REQUESTS} --max-requests-jitter ${MAX_REQUESTS_JITTER}"]
```

### Alpine Variant (Smallest Size)

```dockerfile
# syntax=docker/dockerfile:1

# ============================================
# BUILD STAGE
# ============================================
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --no-dev

COPY src/ ./src/
COPY main.py ./

# ============================================
# RUNTIME STAGE
# ============================================
FROM python:3.12-alpine AS runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Alpine uses addgroup/adduser with different flags
RUN addgroup -g 10001 appgroup && \
    adduser -D -u 10001 -G appgroup -s /sbin/nologin appuser && \
    mkdir -p /app && \
    chown -R appuser:appgroup /app

COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/src /app/src
COPY --from=builder --chown=appuser:appgroup /app/main.py /app/

USER 10001

EXPOSE 8000

# Alpine has wget built-in (no curl needed)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --spider -q http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Development Dockerfile (Hot-reloading)

For development with automatic reloading (security relaxed for convenience):

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install UV for fast dependency installation
RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# Development command with auto-reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Legacy: requirements.txt Support

If not using pyproject.toml/uv.lock:

```dockerfile
# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:python3.12-slim AS builder

WORKDIR /app

COPY requirements.txt ./
RUN uv venv && uv pip install --no-cache -r requirements.txt

COPY src/ ./src/
COPY main.py ./

FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /sbin/nologin appuser && \
    mkdir -p /app && \
    chown -R appuser:appgroup /app

COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appgroup /app/src /app/src
COPY --from=builder --chown=appuser:appgroup /app/main.py /app/

USER 10001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Production Deployment Patterns

### Docker Compose for Development

For local development with database and other services:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - /app/.venv  # Don't mount venv from host
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Docker Compose for Production

```yaml
version: '3.8'

services:
  app:
    image: myapp:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_KEY=${API_KEY}
      - WORKERS=4
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
```

## Security Best Practices

### 1. Non-root User Execution (UID 10001+)

Always run containers as a non-root user with high UID for K8s compliance:

```dockerfile
# Debian/Ubuntu
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /sbin/nologin appuser && \
    chown -R appuser:appgroup /app
USER 10001

# Alpine
RUN addgroup -g 10001 appgroup && \
    adduser -D -u 10001 -G appgroup -s /sbin/nologin appuser && \
    chown -R appuser:appgroup /app
USER 10001
```

**Why UID 10001+?**
- Kubernetes `runAsNonRoot` and `MustRunAsNonRoot` policies
- Avoids collision with host system users
- Better security audit compliance

### 2. Health Checks Without Curl

Don't install curl just for health checks - use native tools:

```dockerfile
# Python (recommended - no extra dependencies)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Alpine (wget is built-in)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --spider -q http://localhost:8000/health || exit 1
```

### 3. Secret Management

Never hardcode secrets - pass them at runtime:

```dockerfile
# ❌ NEVER do this
ENV DATABASE_URL=postgresql://user:password@host/db
ENV API_KEY=sk_live_abc123

# ✅ Do this - empty defaults, inject at runtime
ENV DATABASE_URL="" \
    API_KEY=""
```

```bash
# Pass secrets at runtime
docker run -e DATABASE_URL=$DATABASE_URL -e API_KEY=$API_KEY myapp:latest

# Or use Docker secrets (Swarm) / Kubernetes secrets
```

### 4. Minimal Attack Surface

- Use multi-stage builds (no build tools in production)
- Don't install curl, wget, or other tools unless necessary
- Use `/sbin/nologin` as shell to prevent interactive access
- Use distroless or Alpine for smallest possible image

## Build Optimization

### Layer Caching Strategy

Order matters for cache efficiency:

```dockerfile
# 1. Base image (rarely changes)
FROM python:3.12-slim

# 2. System deps (changes occasionally)
RUN apt-get update && apt-get install -y ...

# 3. Python deps (changes when pyproject.toml changes)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# 4. Application code (changes frequently)
COPY src/ ./src/
```

### Image Size Comparison

| Approach | Typical Size |
|----------|-------------|
| `python:3.12` (full) | ~900MB |
| `python:3.12-slim` | ~150MB |
| `python:3.12-alpine` | ~50MB |
| Multi-stage slim | ~100-200MB |
| Multi-stage alpine | ~50-100MB |

## Common Commands

### Build and Run
```bash
# Build with BuildKit (recommended)
DOCKER_BUILDKIT=1 docker build -t my-fastapi-app .

# Build with metadata
docker build \
    --build-arg BUILD_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ) \
    --build-arg VERSION=1.0.0 \
    -t my-fastapi-app:1.0.0 .

# Run the container
docker run -p 8000:8000 my-fastapi-app

# Run with environment variables
docker run -p 8000:8000 -e WORKERS=8 my-fastapi-app
```

### Validation Tests
```bash
# Test 1: Verify non-root user
docker run --rm my-fastapi-app whoami
# Expected: appuser (not root)

# Test 2: Verify UID
docker run --rm my-fastapi-app id
# Expected: uid=10001(appuser) gid=10001(appgroup)

# Test 3: Verify health check works
docker run -d --name test my-fastapi-app
sleep 10
docker inspect test | jq '.[0].State.Health.Status'
# Expected: "healthy"
docker rm -f test

# Test 4: Check image size
docker images my-fastapi-app
```

## Kubernetes Deployment

For K8s, `HEALTHCHECK` is ignored - use pod probes:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 10001
      containers:
      - name: app
        image: my-fastapi-app:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
          requests:
            memory: "256Mi"
            cpu: "250m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 2
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
              - ALL
```

## Troubleshooting

### 1. Application Not Starting
- Check logs: `docker logs <container>`
- Verify correct module path in CMD
- Ensure all dependencies installed in venv

### 2. Permission Issues
- Check file ownership: `docker run --rm myapp ls -la /app`
- Ensure directories created before USER directive
- Use `--chown` with COPY commands

### 3. Health Check Failing
- Test endpoint manually: `docker exec <container> python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"`
- Increase `--start-period` for slow-starting apps
- Check application logs for errors

### 4. Large Image Size
- Use multi-stage builds
- Use Alpine base images
- Remove `__pycache__` and `.pyc` files
- Check for unnecessary dependencies

## References

This skill includes the following resources:
- **scripts/**: Docker build and deployment helper scripts
- **references/**: Detailed Docker and FastAPI deployment guides
- **assets/**: Dockerfile templates for different scenarios
