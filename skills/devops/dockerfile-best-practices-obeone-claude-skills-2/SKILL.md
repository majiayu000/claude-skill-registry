---
name: dockerfile-best-practices
description: "Create and optimize Dockerfiles with BuildKit, multi-stage builds, advanced caching, and security. Use when: (1) Creating new Dockerfile, (2) Optimizing existing Dockerfile, (3) Reducing image size, (4) Improving security, (5) Using Python with uv, (6) Resolving cache or slow build issues, (7) Setting up CI/CD builds"
metadata:
  version: "1.0.1"
---

# Dockerfile Best Practices

Comprehensive guide for creating optimized, secure, and fast Docker images using modern BuildKit features.

## Quick Start Workflow

When working with Dockerfiles, follow this decision tree:

1. **Choose your language/framework** → Use appropriate template below
2. **Apply security hardening** → Non-root user, pin versions, secrets management
3. **Optimize for cache** → Separate deps from code, use cache mounts
4. **Multi-stage if needed** → Separate build from runtime for compiled languages
5. **Review with analyzer** → Run `scripts/analyze_dockerfile.py`

## Essential Rules (Always Apply)

1. **Start with BuildKit syntax:**
   ```dockerfile
   # syntax=docker/dockerfile:1
   ```

2. **Pin runtime versions, not OS versions:**
   ```dockerfile
   # ✅ GOOD - Pin runtime, let OS update
   FROM python:3.12-slim

   # ❌ BAD - Pins OS version (bookworm), prevents security updates
   FROM python:3.12-slim-bookworm
   ```
   **Why?** OS versions update with security patches. Pin runtime (python:3.12) for reproducible behavior.

3. **Create `.dockerignore`:**
   Use template from `assets/dockerignore-template`

4. **Use cache mounts for package managers:**
   ```dockerfile
   RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
   ```

5. **APT cache setup (before any apt operations):**
   ```dockerfile
   RUN rm -f /etc/apt/apt.conf.d/docker-clean; \
       echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
   ```

6. **Never use ARG/ENV for secrets:**
   ```dockerfile
   RUN --mount=type=secret,id=api_key curl -H "Authorization: $(cat /run/secrets/api_key)" https://api.example.com
   ```

7. **Use non-root user with safe UID/GID:**
   ```dockerfile
   # Let system auto-assign (simple)
   RUN groupadd -r app && useradd -r -g app app

   # Or use UID/GID >10000 for consistency across environments
   RUN groupadd -r -g 10001 app && useradd -r -u 10001 -g app app
   ```

## Language-Specific Templates

### Python (with uv - Recommended)

For detailed Python/uv integration, see `references/uv_integration.md`.

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies (separate layer for caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy and install project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Security: non-root user with UID/GID >10000
RUN groupadd -r -g 10001 app && \
    useradd -r -u 10001 -g app app && \
    chown -R app:app /app
USER app

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "myapp"]
```

### Node.js

```dockerfile
# syntax=docker/dockerfile:1

FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json yarn.lock ./
RUN --mount=type=cache,target=/root/.yarn \
    yarn install --frozen-lockfile --production

# Copy source
COPY . .

# Security: non-root user with UID/GID >10000
RUN addgroup -g 10001 app && \
    adduser -u 10001 -G app -S app && \
    chown -R app:app /app
USER app

EXPOSE 3000
CMD ["node", "index.js"]
```

### Go (Multi-stage)

```dockerfile
# syntax=docker/dockerfile:1

# Build stage
FROM golang:1-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o main

# Runtime stage
FROM alpine:3
RUN addgroup -g 10001 app && adduser -u 10001 -G app -S app
USER app
COPY --from=builder /app/main /main
ENTRYPOINT ["/main"]
```

### Debian-based (with APT cache)

```dockerfile
# syntax=docker/dockerfile:1

FROM debian:stable-slim

# Configure APT for cache reuse
RUN rm -f /etc/apt/apt.conf.d/docker-clean; \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

WORKDIR /app

# Install dependencies with cache mount
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates

# Copy application
COPY . .

# Security: non-root user with UID/GID >10000
RUN groupadd -r -g 10001 app && \
    useradd -r -u 10001 -g app app && \
    chown -R app:app /app
USER app

CMD ["./app"]
```

### PHP (with Composer)

```dockerfile
# syntax=docker/dockerfile:1

FROM php:8-fpm-alpine

WORKDIR /app

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Install dependencies
COPY composer.json composer.lock ./
RUN --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --optimize-autoloader --no-scripts

# Copy source
COPY . .
RUN composer dump-autoload --optimize

# Security: non-root user with UID/GID >10000
RUN addgroup -g 10001 app && \
    adduser -u 10001 -G app -S app && \
    chown -R app:app /app
USER app

EXPOSE 9000
CMD ["php-fpm"]
```

## Security Checklist

- [ ] Use specific version tags for base images
- [ ] Use minimal base image (alpine, slim, distroless)
- [ ] Create and use non-root user
- [ ] Never expose secrets via ARG/ENV
- [ ] Use `RUN --mount=type=secret` for sensitive data
- [ ] Add HEALTHCHECK instruction
- [ ] Scan image for vulnerabilities (`docker scan`)

## Performance Checklist

- [ ] Add BuildKit syntax directive
- [ ] Create comprehensive `.dockerignore`
- [ ] Order instructions: manifests → deps → code
- [ ] Use `--mount=type=cache` for all package managers
- [ ] Implement multi-stage builds for compiled languages
- [ ] Chain RUN commands with `&&`
- [ ] Clean up in same RUN instruction

## Size Optimization

**Quick wins:**
1. Use alpine or slim variants
2. Multi-stage builds
3. Remove unnecessary files in same layer
4. Use `--no-install-recommends` with apt
5. Consider distroless for runtime

## Common Patterns

### Intermediate Layers (Faster Rebuilds)

Separate dependency installation from code copy:

```dockerfile
# Install deps first (rarely changes)
COPY package.json package-lock.json ./
RUN npm ci --production

# Copy code (changes frequently)
COPY . .
```

### Remote Cache (CI/CD)

```bash
docker buildx build \
  --cache-from=type=registry,ref=myregistry.com/app:cache \
  --cache-to=type=registry,ref=myregistry.com/app:cache,mode=max \
  --push \
  -t myregistry.com/app:latest .
```

### Secret Management

```bash
# Build with secret
docker buildx build --secret id=api_key,src=./key.txt .

# Or from environment
docker buildx build --secret id=api_key,env=API_KEY .
```

## Tools and Scripts

### Analyze Dockerfile

```bash
python scripts/analyze_dockerfile.py ./Dockerfile
```

Detects common anti-patterns:
- Missing BuildKit syntax
- Using :latest tags
- ADD instead of COPY
- Missing cache mounts
- Secrets in ARG/ENV
- Missing non-root USER
- apt-get without cleanup

### Generate .dockerignore

```bash
cp assets/dockerignore-template .dockerignore
```

## Docker Compose Best Practices

For multi-container applications, follow modern Compose practices:

### Key Rules

1. **Don't use `version:` field** - Deprecated since Compose V2
   ```yaml
   # ✅ GOOD - No version field
   services:
     app:
       image: myapp:1.0.0
   ```

2. **Never use `container_name:`** - Prevents scaling and parallel environments
   ```yaml
   # ✅ GOOD - Let Compose generate names
   services:
     app:
       image: myapp:1.0.0
       # No container_name - allows scaling with --scale

   # Use project names for environment isolation:
   # docker compose -p myapp-dev up
   # docker compose -p myapp-test up
   ```

3. **Use specific image tags** - Not `:latest`
4. **Define health checks** - For service dependencies
5. **Set resource limits** - Prevent resource exhaustion

For complete Compose guide, see `references/compose_best_practices.md`.

## Reference Documentation

For detailed information, consult these references:

1. **`references/optimization_guide.md`** - Complete optimization guide with BuildKit, caching, multi-stage builds
2. **`references/best_practices.md`** - Checklist of all best practices with impact levels
3. **`references/examples.md`** - Real-world before/after optimization examples
4. **`references/uv_integration.md`** - Python with uv package manager (recommended for Python)
5. **`references/compose_best_practices.md`** - Docker Compose modern practices (no version:, no container_name:)

## Common Issues and Solutions

### Slow builds

- Add cache mounts: `RUN --mount=type=cache,target=...`
- Optimize layer ordering: deps before code
- Use remote cache in CI/CD

### Large images

- Use multi-stage builds
- Switch to alpine/slim base images
- Clean up in same RUN instruction
- Remove dev dependencies

### Security concerns

- Pin versions with SHA256
- Use non-root USER
- Never use ARG/ENV for secrets
- Use BuildKit secret mounts
- Scan with `docker scan`

### Cache invalidation

- Separate dependency installation from code
- Use `--mount=type=bind` for manifests
- Order instructions correctly

## Examples by Use Case

### CLI Tool

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["mytool"]
```

### Web API

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine
WORKDIR /app
COPY package.json yarn.lock ./
RUN --mount=type=cache,target=/root/.yarn yarn install --frozen-lockfile --production
COPY . .
RUN addgroup -g 10001 app && \
    adduser -u 10001 -G app -S app && \
    chown -R app:app /app
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "server.js"]
```

### Static Site

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json yarn.lock ./
RUN --mount=type=cache,target=/root/.yarn yarn install --frozen-lockfile
COPY . .
RUN yarn build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

## Build Commands Reference

```bash
# Basic build
docker buildx build -t myapp:latest .

# With cache from registry
docker buildx build \
  --cache-from=type=registry,ref=registry.com/myapp:cache \
  --cache-to=type=registry,ref=registry.com/myapp:cache,mode=max \
  -t myapp:latest .

# With secrets
docker buildx build \
  --secret id=api_key,src=./key.txt \
  -t myapp:latest .

# Multi-platform
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myapp:latest --push .

# Target specific stage
docker buildx build --target builder -t myapp:builder .
```

## Next Steps

After creating your Dockerfile:

1. Run analyzer: `python scripts/analyze_dockerfile.py Dockerfile`
2. Test locally: `docker buildx build -t test .`
3. Check size: `docker images test`
4. Scan for vulnerabilities: `docker scout cves test`
5. Profile build: `docker buildx build --progress=plain . 2>&1 | less`
