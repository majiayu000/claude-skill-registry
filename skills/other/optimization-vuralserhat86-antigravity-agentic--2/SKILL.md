---
name: docker_optimization
router_kit: ManagementKit
description: Docker image optimization patterns including multi-stage builds, layer caching, security hardening, and size reduction techniques. Use when building Docker images, optimizing container size, improving build performance, or implementing Docker security best practices. Reduces image sizes by 70-90% and build times by 50-80%.
metadata:
  skillport:
    category: auto-healed
    tags: [automation, aws, bash scripting, ci/cd, cloud computing, containerization, deployment strategies, devops, docker, docker optimization, gitops, infrastructure, infrastructure as code, kubernetes, linux, logging, microservices, monitoring, orchestration, pipelines, reliability, scalability, security, server management, terraform]      - docker_optimization
---

# Docker Optimization Patterns

Comprehensive guide to optimizing Docker images for size, build speed, and security. Covers multi-stage builds, layer caching strategies, security hardening, and production deployment patterns.

---

## Quick Reference

**When to use this skill:**
- Building production Docker images
- Optimizing image size (reducing from 500MB+ to <100MB)
- Improving Docker build times
- Implementing Docker security best practices
- Debugging slow builds or large images
- Setting up Docker for microservices

**Common triggers:**
- "My Docker image is too large"
- "Docker builds take forever"
- "How do I optimize this Dockerfile"
- "Docker security best practices"
- "Multi-stage build pattern"

---

## Part 1: Multi-Stage Builds

### The Problem: Bloated Images

**Typical single-stage Dockerfile** (800MB+ image):
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

**Problems:**
- Includes build tools (gcc, make, etc.) - 300MB+
- Includes pip cache - 100MB+
- Includes source .git directory - 50MB+
- Includes test files and dev dependencies - 50MB+
- **Total: 800MB+ for simple Python app**

### The Solution: Multi-Stage Pattern

**Optimized multi-stage Dockerfile** (120MB image):
```dockerfile
# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app

# Install build dependencies in separate layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (cache optimization)
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Copy only Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy only application code
COPY app.py .
COPY src/ ./src/

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Run as non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "app.py"]
```

**Result: 800MB → 120MB (85% reduction)**

### Multi-Stage Pattern Breakdown

**Stage 1: Builder** (Throw away after build)
- Install build tools
- Compile dependencies
- Run tests (optional)
- Generate artifacts

**Stage 2: Runtime** (Final image)
- Minimal base image
- Copy only artifacts from builder
- No build tools
- No source files (only compiled/necessary files)

---

## Part 2: Layer Caching Optimization

### Understanding Docker Layer Caching

Each instruction creates a layer. Docker caches unchanged layers.

**Bad Order** (cache invalidated on every code change):
```dockerfile
FROM python:3.11-slim
COPY . .                        # ❌ Copies everything
RUN pip install -r requirements.txt  # ❌ Runs on every code change
```

**Good Order** (cache preserved):
```dockerfile
FROM python:3.11-slim
COPY requirements.txt .         # ✅ Only requirements
RUN pip install -r requirements.txt  # ✅ Cached if requirements unchanged
COPY . .                        # ✅ Code changes don't invalidate pip cache
```

### Layer Caching Best Practices

**1. Order by change frequency** (least to most):
```dockerfile
# 1. System dependencies (rarely change)
RUN apt-get update && apt-get install -y curl

# 2. Language runtime (rarely changes)
FROM python:3.11-slim

# 3. Dependencies (change occasionally)
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4. Application code (changes frequently)
COPY . .
```

**2. Separate COPY operations**:
```dockerfile
# ❌ Bad: Invalidates cache on any file change
COPY . .

# ✅ Good: Cache preserved unless specific files change
COPY package.json package-lock.json ./
RUN npm ci
COPY src/ ./src/
COPY public/ ./public/
```

**3. Use .dockerignore**:
```
# .dockerignore
.git
.gitignore
node_modules
npm-debug.log
Dockerfile
.dockerignore
.env
.venv
__pycache__
*.pyc
tests/
docs/
```

---

## Part 3: Image Size Optimization

### Choose Minimal Base Images

**Image Size Comparison**:
```
python:3.11          → 1.01GB
python:3.11-slim     → 130MB   (87% smaller)
python:3.11-alpine   → 50MB    (95% smaller)
```

**When to use each**:
- **Full image** (`python:3.11`): Never for production
- **Slim** (`python:3.11-slim`): Default choice, good compatibility
- **Alpine** (`python:3.11-alpine`): Smallest, but can have glibc issues

### Multi-Stage Size Optimization

**Node.js Example** (900MB → 150MB):
```dockerfile
# Builder stage
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

**Result**: 900MB → 150MB (83% reduction)

### Clean Up in Same Layer

**❌ Bad** (creates large intermediate layers):
```dockerfile
RUN apt-get update
RUN apt-get install -y build-essential
RUN rm -rf /var/lib/apt/lists/*
```

**✅ Good** (single layer, no intermediate garbage):
```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*
```

### Remove Build Dependencies After Use

```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        make \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove \
        gcc \
        g++ \
        make \
    && rm -rf /var/lib/apt/lists/*
```

---

## Part 4: Security Best Practices

### Don't Run as Root

**❌ Bad** (runs as root):
```dockerfile
FROM python:3.11-slim
COPY app.py .
CMD ["python", "app.py"]
```

**✅ Good** (runs as non-root user):
```dockerfile
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

WORKDIR /app
USER appuser

COPY --chown=appuser:appuser app.py .
CMD ["python", "app.py"]
```

### Never Include Secrets in Image

**❌ Bad** (secrets baked into image):
```dockerfile
ENV DATABASE_PASSWORD=secret123
COPY .env .
```

**✅ Good** (secrets provided at runtime):
```dockerfile
# Pass secrets via environment variables at runtime
# docker run -e DATABASE_PASSWORD=$DB_PASS myapp
```

**✅ Also Good** (Docker secrets):
```dockerfile
# Use Docker secrets (Swarm/Kubernetes)
CMD ["sh", "-c", "python app.py"]
# Secrets mounted at /run/secrets/
```

### Scan Images for Vulnerabilities

```bash
# Using Docker Scout
docker scout cves myapp:latest

# Using Trivy
trivy image myapp:latest

# Using Snyk
snyk container test myapp:latest
```

### Use Specific Image Tags

**❌ Bad** (unpredictable):
```dockerfile
FROM python:latest
```

**✅ Good** (reproducible):
```dockerfile
FROM python:3.11.9-slim-bookworm
```

---

## Part 5: Build Performance Optimization

### BuildKit (Modern Docker Builder)

Enable BuildKit for faster builds:
```bash
export DOCKER_BUILDKIT=1
docker build -t myapp .
```

**Benefits**:
- Parallel layer building
- Skip unused stages
- Better caching
- 30-50% faster builds

### Build Cache Mounts

**With BuildKit** (cache pip downloads):
```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

**Benefits**:
- Pip packages cached between builds
- No need to clear cache (doesn't bloat image)
- Significantly faster rebuilds

### Parallel Multi-Stage Builds

BuildKit automatically parallelizes independent stages:
```dockerfile
# Stage 1: Frontend build (runs in parallel)
FROM node:20 AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Backend build (runs in parallel)
FROM python:3.11-slim AS backend
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Stage 3: Final image (waits for both stages)
FROM python:3.11-slim
COPY --from=frontend /app/frontend/dist /app/static
COPY --from=backend /app/backend /app
```

---

## Part 6: Production Patterns

### Health Checks

```dockerfile
FROM python:3.11-slim
COPY app.py .

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "app.py"]
```

### Proper Signal Handling

```dockerfile
# Use exec form to ensure proper signal handling
CMD ["python", "app.py"]  # ✅ Receives SIGTERM

# Not shell form
CMD python app.py  # ❌ Shell doesn't forward signals
```

### Labels for Metadata

```dockerfile
LABEL org.opencontainers.image.title="MyApp"
LABEL org.opencontainers.image.version="1.2.3"
LABEL org.opencontainers.image.authors="team@example.com"
LABEL org.opencontainers.image.source="https://github.com/org/repo"
```

---

## Part 7: Language-Specific Patterns

### Python Optimization

```dockerfile
FROM python:3.11-slim AS builder

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Install to user site-packages
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0"]
```

### Node.js Optimization

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./

# Install production dependencies only
RUN npm ci --only=production && \
    # Remove npm cache
    npm cache clean --force

# Runtime stage
FROM node:20-alpine

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeuser -u 1001

WORKDIR /app
COPY --from=builder --chown=nodeuser:nodejs /app/node_modules ./node_modules
COPY --chown=nodeuser:nodejs . .

USER nodeuser
EXPOSE 3000

CMD ["node", "server.js"]
```

### Go Optimization

```dockerfile
# Builder stage
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Runtime stage - minimal scratch image
FROM scratch

# Copy CA certificates for HTTPS
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy binary
COPY --from=builder /app/main /main

EXPOSE 8080
ENTRYPOINT ["/main"]
```

**Result**: 1GB → 15MB (98.5% reduction!)

---

## Part 8: Common Mistakes to Avoid

### Mistake 1: Installing Recommended Packages

**❌ Bad** (installs hundreds of unnecessary packages):
```dockerfile
RUN apt-get install curl
```

**✅ Good** (minimal installation):
```dockerfile
RUN apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

### Mistake 2: Using ADD Instead of COPY

**❌ Bad** (ADD has implicit behavior):
```dockerfile
ADD requirements.txt .  # Can extract tarballs, fetch URLs
```

**✅ Good** (COPY is explicit):
```dockerfile
COPY requirements.txt .  # Only copies files
```

### Mistake 3: Multiple FROM Without AS

**❌ Bad** (can't reference previous stages):
```dockerfile
FROM python:3.11
RUN pip install -r requirements.txt
FROM python:3.11-slim
# Can't copy from previous stage!
```

**✅ Good** (named stages):
```dockerfile
FROM python:3.11 AS builder
RUN pip install -r requirements.txt
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
```

### Mistake 4: Not Using .dockerignore

Without .dockerignore:
- Copies .git directory (50MB+)
- Copies node_modules (100MB+)
- Copies test files
- Invalidates cache on any file change

### Mistake 5: Hardcoding Versions Incorrectly

**❌ Bad** (no control over patch versions):
```dockerfile
FROM python:3.11
```

**✅ Good** (pin exact version):
```dockerfile
FROM python:3.11.9-slim-bookworm
```

---

## Part 9: Before/After Examples

### Example 1: Python FastAPI App

**Before** (1.2GB image, 5min build):
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app:app"]
```

**After** (140MB image, 2min build):
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
ENV PATH=/root/.local/bin:$PATH
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
COPY src/ ./src/

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

**Results**:
- Size: 1.2GB → 140MB (88% reduction)
- Build time: 5min → 2min (60% faster)
- Security: Now runs as non-root
- Cache: Code changes don't rebuild dependencies

---

## Part 10: Quick Optimization Checklist

**Image Size**:
- [ ] Use slim or alpine base images
- [ ] Multi-stage build (build tools in first stage only)
- [ ] Clean up in same layer (`apt-get install && rm -rf`)
- [ ] Use `--no-install-recommends` with apt-get
- [ ] Remove package manager cache (`pip --no-cache-dir`, `npm cache clean`)
- [ ] Use .dockerignore

**Build Speed**:
- [ ] Order COPY by change frequency
- [ ] Copy dependency files before code
- [ ] Enable BuildKit
- [ ] Use build cache mounts

**Security**:
- [ ] Run as non-root user
- [ ] Pin specific image versions
- [ ] Scan for vulnerabilities
- [ ] Never include secrets in image
- [ ] Use minimal base images

**Production**:
- [ ] Add HEALTHCHECK
- [ ] Use exec form for CMD
- [ ] Add metadata labels
- [ ] Proper signal handling
- [ ] Set up proper logging

---

## Resources

**Official Docker Documentation**:
- Multi-stage builds: https://docs.docker.com/build/building/multi-stage/
- Best practices: https://docs.docker.com/develop/dev-best-practices/
- BuildKit: https://docs.docker.com/build/buildkit/

**Security Scanning**:
- Docker Scout: https://docs.docker.com/scout/
- Trivy: https://github.com/aquasecurity/trivy
- Snyk: https://snyk.io/product/container-vulnerability-management/

**Base Images**:
- Docker Hub: https://hub.docker.com/
- Google Distroless: https://github.com/GoogleContainerTools/distroless
*Docker Optimization v1.2 - Verified*

## 🔄 Workflow

> **Kaynak:** [Docker Build Best Practices](https://docs.docker.com/build/building/best-practices/) & [Trivy Docs](https://aquasecurity.github.io/trivy/)

### Aşama 1: Base & Structure
- [ ] **Base Image**: Üretim için `-alpine` veya `-slim` imajını seç (Pin version: `python:3.11.9-slim`).
- [ ] **Layers**: Değişmeyen katmanları (Dependency Install) yukarı taşı, kod kopyalamayı (`COPY . .`) en alta al.
- [ ] **Multi-Stage**: Build araçlarını (`gcc`, `npm`) builder stage'de bırak, runtime stage'e taşıma.

### Aşama 2: Security & Linting
- [ ] **Linter**: Dockerfile'ı `hadolint` ile tara (`hadolint Dockerfile`).
- [ ] **User**: `USER appuser` ile root olmayan kullanıcıya geç.
- [ ] **Secrets**: `ENV` ile secret geçme, secret mount kullan.

### Aşama 3: Performance Check
- [ ] **Context**: `.dockerignore` dosyası `.git`, `node_modules` ve testleri hariç tutuyor mu?
- [ ] **Cache**: `RUN --mount=type=cache` kullanarak paket yöneticisi önbelleğini hızlandır.
- [ ] **Scan**: İmajı `trivy image <name>` ile tarat ve kritik açıkları gider.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | İmaj boyutu builder stage'den %50+ daha küçük mü? |
| 2 | `dive <image>` ile bakıldığında gizli dosya/key kalmış mı? |
| 3 | Container root olmadan çalışabiliyor mu? |
