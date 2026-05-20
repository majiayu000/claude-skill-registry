---
name: multi-stage-builds
description: >
  Guide for Docker multi-stage builds with builder patterns, distroless and alpine base images,
  cache mounts, and build args. Use when the user needs to optimize Docker image size, separate
  build from runtime dependencies, or improve build performance. Trigger when the user mentions
  multi-stage, distroless, slim images, or Docker build optimization.
---

# Multi-Stage Builds

Use multi-stage Docker builds to produce minimal, secure production images by separating
build-time tooling from runtime dependencies.

## When to Use
- User needs to reduce Docker image size
- User ships compilers or build tools in production images
- User asks about distroless or alpine base images
- User wants faster Docker builds with cache mounts
- User needs different images for dev, test, and production

## Core Patterns

### Node.js Builder Pattern

Separate TypeScript compilation and dependency installation from the runtime image.

```dockerfile
# ---------- Stage 1: Install dependencies ----------
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# ---------- Stage 2: Build ----------
FROM deps AS builder
COPY tsconfig.json ./
COPY src/ src/
RUN npm run build && npm prune --omit=dev

# ---------- Stage 3: Production ----------
FROM gcr.io/distroless/nodejs20-debian12
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
EXPOSE 3000
CMD ["dist/index.js"]
```

Result: ~150MB image instead of ~1GB with full Node.js + dev dependencies.

### Go Static Binary

Go compiles to a single static binary, making `scratch` or distroless ideal.

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-s -w" -o /server ./cmd/server

FROM gcr.io/distroless/static-debian12
COPY --from=builder /server /server
USER nonroot:nonroot
ENTRYPOINT ["/server"]
```

Result: ~10-20MB image with zero OS packages and no shell for attackers to exploit.

### Python with Virtual Environment

Isolate Python dependencies in a virtualenv, then copy only the venv to the runtime image.

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM python:3.12-slim
WORKDIR /app
RUN groupadd -r app && useradd -r -g app app
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app
ENV PATH="/opt/venv/bin:$PATH"
USER app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cache Mounts for Faster Builds

Use BuildKit cache mounts to persist package manager caches across builds, avoiding
repeated downloads.

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .
RUN npm run build

FROM rust:1.77-alpine AS rust-builder
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
COPY src/ src/
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release && \
    cp target/release/myapp /usr/local/bin/myapp
```

### Build Args for Conditional Stages

Use build args to customize builds without separate Dockerfiles.

```dockerfile
ARG BUILD_ENV=production

FROM node:20-alpine AS base
WORKDIR /app
COPY package.json package-lock.json ./

FROM base AS deps-production
RUN npm ci --omit=dev

FROM base AS deps-development
RUN npm ci

FROM deps-${BUILD_ENV} AS deps

FROM node:20-alpine AS final
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
```

Build with: `docker build --build-arg BUILD_ENV=development -t myapp:dev .`

### Target-Based Development Workflow

Use named stages with `--target` for different environments from a single Dockerfile.

```dockerfile
FROM node:20-alpine AS base
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM base AS development
COPY . .
CMD ["npm", "run", "dev"]

FROM base AS test
COPY . .
RUN npm run lint && npm test

FROM base AS builder
COPY . .
RUN npm run build && npm prune --omit=dev

FROM gcr.io/distroless/nodejs20-debian12 AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["dist/index.js"]
```

```bash
docker build --target development -t myapp:dev .
docker build --target test -t myapp:test .
docker build --target production -t myapp:prod .
```

## Anti-Patterns

- **Copying build tools into production**: Never include compilers, package managers, or dev headers in the final stage. They waste space and increase attack surface.
- **Using `ubuntu` or `debian` for runtime**: Prefer `alpine`, `slim`, `distroless`, or `scratch`. A full Debian base adds 100-200MB of unnecessary packages.
- **Not separating dependency install from code copy**: If you COPY everything before `npm ci`, every source code change invalidates the dependency cache.
- **Ignoring `--mount=type=cache`**: Without cache mounts, every build re-downloads all dependencies from scratch. Enable BuildKit and use cache mounts.
- **Single Dockerfile per environment**: Use `--target` and build args instead of maintaining separate Dockerfiles for dev, test, and prod.

## Quick Reference

| Base Image | Size | Shell | Use Case |
|---|---|---|---|
| `scratch` | 0 MB | No | Go static binaries |
| `distroless/static` | ~2 MB | No | Static binaries, max security |
| `distroless/cc` | ~20 MB | No | C/C++ apps needing libc |
| `distroless/nodejs20` | ~130 MB | No | Node.js production |
| `alpine` | ~7 MB | Yes | When you need a shell |
| `debian-slim` | ~80 MB | Yes | When you need apt packages |

```bash
# Enable BuildKit (required for cache mounts)
export DOCKER_BUILDKIT=1

# Build specific target
docker build --target production -t myapp:prod .

# Check final image size
docker images myapp:prod
```
