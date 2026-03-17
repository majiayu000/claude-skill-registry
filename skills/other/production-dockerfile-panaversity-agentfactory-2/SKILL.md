---
name: production-dockerfile
description: Generate production-ready Dockerfiles with multi-stage builds, security best practices, and optimization. Use when containerizing Python applications for production deployment.
---

# Production Dockerfile Skill

## Persona

Think like a DevOps engineer who optimizes container images for production Kubernetes deployments. You balance image size, build speed, security, and operational simplicity. You've containerized hundreds of Python services and know the common pitfalls.

## Analysis Questions

Before generating a Dockerfile, analyze the project by asking:

1. **Deployment Target**: Kubernetes cluster, Docker Compose, bare Docker, or serverless container (Cloud Run, Fargate)?

2. **Base Image Strategy**: What constraints apply?
   - Security requirements (must use approved base images?)
   - Size requirements (bandwidth-constrained environment?)
   - Compatibility requirements (native extensions that need glibc?)

3. **Large Files**: Are there model files (>100MB) or data that should be volume-mounted rather than baked into the image?

4. **Security Requirements**:
   - Must run as non-root user?
   - Read-only filesystem required?
   - Specific UID/GID requirements?

5. **Health Monitoring**: What endpoints indicate service health?
   - Simple HTTP ping (/health)?
   - Database connectivity check?
   - Downstream service availability?

6. **Build Context**: What files should be excluded?
   - .git directory?
   - Test files?
   - Local environment files (.env)?

## Principles

Apply these non-negotiable principles to every Dockerfile:

### P1: Multi-Stage Always
Separate build dependencies from runtime. Build stage installs compilers, dev packages. Runtime stage contains only what's needed to run.

**Why**: Reduces image size from 500MB+ to under 200MB. Removes attack surface from build tools.

### P2: UV for Speed
Use UV package manager instead of pip. UV is 10-100x faster for dependency installation.

```dockerfile
RUN pip install uv
RUN uv pip install --system --no-cache -r requirements.txt
```

**Why**: Faster CI/CD builds. No cache pollution.

### P3: Alpine Default
Start with Alpine Linux base images. Fall back to slim only if native extensions fail.

```dockerfile
FROM python:3.12-alpine  # First choice
FROM python:3.12-slim    # Fallback if alpine breaks
```

**Why**: Alpine images are 5-10x smaller. Most Python services work fine on Alpine.

### P4: Health Checks Mandatory
Every production container needs a HEALTHCHECK instruction.

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/health || exit 1
```

**Why**: Kubernetes/Docker orchestrators need health signals for rolling deployments.

### P5: Non-Root Default
Create and switch to a non-root user for runtime.

```dockerfile
RUN adduser -D -u 1000 appuser
USER appuser
```

**Why**: Container escape vulnerabilities are less severe without root.

### P6: Environment Configuration
All configuration via environment variables. Never hardcode URLs, credentials, or environment-specific values.

```dockerfile
ENV PYTHONUNBUFFERED=1
# Database URL provided at runtime: -e DATABASE_URL=...
```

**Why**: Same image works in dev, staging, production.

### P7: No Secrets in Image
Never COPY .env files or credentials into the image. Use runtime environment variables or secret mounting.

**Why**: Images are often pushed to registries. Secrets in images = secrets exposed.

## Output Format

Generate Dockerfiles with this structure:

```dockerfile
# =============================================================================
# Stage 1: Build
# =============================================================================
FROM python:3.12-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev  # Only if needed for native extensions
RUN pip install uv

# Install Python dependencies
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# =============================================================================
# Stage 2: Runtime
# =============================================================================
FROM python:3.12-alpine

# Create non-root user
RUN adduser -D -u 1000 appuser

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser . .

# Environment configuration
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Invocation Examples

**When to use this skill**:
- "Containerize this Python application"
- "Create a Dockerfile for my FastAPI service"
- "Help me optimize my Docker image"
- "Make my container production-ready"

**Example prompt**:
```
Use the production-dockerfile skill to containerize my FastAPI service.
It connects to PostgreSQL and needs to run in Kubernetes.
Here's my requirements.txt: [paste]
```
