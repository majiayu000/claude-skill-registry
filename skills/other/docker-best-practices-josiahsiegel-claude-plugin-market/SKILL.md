---
name: docker-best-practices
description: Comprehensive Docker best practices for images, containers, and production deployments
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# Docker Best Practices

This skill provides current Docker best practices across all aspects of container development, deployment, and operation.

## Image Best Practices

### Base Image Selection

**2025 Recommended Hierarchy:**
1. **Wolfi/Chainguard** (`cgr.dev/chainguard/*`) - Zero-CVE goal, SBOM included
2. **Alpine** (`alpine:3.19`) - ~7MB, minimal attack surface
3. **Distroless** (`gcr.io/distroless/*`) - ~2MB, no shell
4. **Slim variants** (`node:20-slim`) - ~70MB, balanced

**Key rules:**
- Always specify exact version tags: `node:20.11.0-alpine3.19`
- Never use `latest` (unpredictable, breaks reproducibility)
- Use official images from trusted registries
- Match base image to actual needs

### Dockerfile Structure

**Optimal layer ordering** (least to most frequently changing):
```dockerfile
1. Base image and system dependencies
2. Application dependencies (package.json, requirements.txt, etc.)
3. Application code
4. Configuration and metadata
```

**Rationale:** Docker caches layers. If code changes but dependencies don't, cached dependency layers are reused, speeding up builds.

**Example:**
```dockerfile
FROM python:3.12-slim

# 1. System packages (rarely change)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 2. Dependencies (change occasionally)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Application code (changes frequently)
COPY . /app
WORKDIR /app

CMD ["python", "app.py"]
```

### Multi-Stage Builds

Use multi-stage builds to separate build dependencies from runtime:

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS runtime
WORKDIR /app
# Only copy what's needed for runtime
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/server.js"]
```

**Benefits:**
- Smaller final images (no build tools)
- Better security (fewer attack vectors)
- Faster deployment (smaller upload/download)

### Layer Optimization

**Combine commands** to reduce layers and image size:

```dockerfile
# Bad - 3 layers, cleanup doesn't reduce size
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# Good - 1 layer, cleanup effective
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

### .dockerignore

Always create `.dockerignore` to exclude unnecessary files:

```
# Version control
.git
.gitignore

# Dependencies
node_modules
__pycache__
*.pyc

# IDE
.vscode
.idea

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Testing
coverage/
.nyc_output
*.test.js

# Documentation
README.md
docs/

# Environment
.env
.env.local
*.local
```

## Container Runtime Best Practices

### Security

```bash
docker run \
  # Run as non-root
  --user 1000:1000 \
  # Drop all capabilities, add only needed ones
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  # Read-only filesystem
  --read-only \
  # Temporary writable filesystems
  --tmpfs /tmp:noexec,nosuid \
  # No new privileges
  --security-opt="no-new-privileges:true" \
  # Resource limits
  --memory="512m" \
  --cpus="1.0" \
  my-image
```

### Resource Management

Always set resource limits in production:

```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '1.0'
          memory: 512M
```

### Health Checks

Implement health checks for all long-running containers:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 --start-period=40s \
  CMD curl -f http://localhost:3000/health || exit 1
```

Or in compose:
```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 40s
```

### Logging

Configure proper logging to prevent disk fill-up:

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

Or system-wide in `/etc/docker/daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### Restart Policies

```yaml
services:
  app:
    # For development
    restart: "no"

    # For production
    restart: unless-stopped

    # Or with fine-grained control (Swarm mode)
    deploy:
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
```

## Docker Compose Best Practices

### File Structure

```yaml
# No version field needed (Compose v2.40.3+)

services:
  # Service definitions
  web:
    # ...
  api:
    # ...
  database:
    # ...

networks:
  # Custom networks (preferred)
  frontend:
  backend:
    internal: true

volumes:
  # Named volumes (preferred for persistence)
  db-data:
  app-data:

configs:
  # Configuration files (Swarm mode)
  app-config:
    file: ./config/app.conf

secrets:
  # Secrets (Swarm mode)
  db-password:
    file: ./secrets/db_pass.txt
```

### Network Isolation

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access

services:
  web:
    networks:
      - frontend

  api:
    networks:
      - frontend
      - backend

  database:
    networks:
      - backend  # Not accessible from frontend
```

### Environment Variables

```yaml
services:
  app:
    # Load from file (preferred for non-secrets)
    env_file:
      - .env

    # Inline for service-specific vars
    environment:
      - NODE_ENV=production
      - LOG_LEVEL=info

    # For Swarm mode secrets
    secrets:
      - db_password
```

**Important:**
- Add `.env` to `.gitignore`
- Provide `.env.example` as template
- Never commit secrets to version control

### Dependency Management

```yaml
services:
  api:
    depends_on:
      database:
        condition: service_healthy  # Wait for health check
      redis:
        condition: service_started   # Just wait for start
```

## Production Best Practices

### Image Tagging Strategy

```bash
# Use semantic versioning
my-app:1.2.3
my-app:1.2
my-app:1
my-app:latest

# Include git commit for traceability
my-app:1.2.3-abc123f

# Environment tags
my-app:1.2.3-production
my-app:1.2.3-staging
```

### Secrets Management

**Never do this:**
```dockerfile
# BAD - secret in layer history
ENV API_KEY=secret123
RUN echo "password" > /app/config
```

**Do this:**
```bash
# Use Docker secrets (Swarm) or external secret management
docker secret create db_password ./password.txt

# Or mount secrets at runtime
docker run -v /secure/secrets:/run/secrets:ro my-app

# Or use environment files (not in image)
docker run --env-file /secure/.env my-app
```

### Monitoring & Observability

```yaml
services:
  app:
    # Health checks
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s

    # Labels for monitoring tools
    labels:
      - "prometheus.io/scrape=true"
      - "prometheus.io/port=9090"
      - "com.company.team=backend"
      - "com.company.version=1.2.3"

    # Logging
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Backup Strategy

```bash
# Backup named volume
docker run --rm \
  -v VOLUME_NAME:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup-$(date +%Y%m%d).tar.gz -C /data .

# Restore volume
docker run --rm \
  -v VOLUME_NAME:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /data
```

### Update Strategy

```yaml
services:
  app:
    # For Swarm mode - rolling updates
    deploy:
      replicas: 3
      update_config:
        parallelism: 1        # Update 1 at a time
        delay: 10s            # Wait 10s between updates
        failure_action: rollback
        monitor: 60s
      rollback_config:
        parallelism: 1
        delay: 5s
```

## Platform-Specific Best Practices

### Linux

- Use user namespace remapping for added security
- Leverage native performance advantages
- Use Alpine for smallest images
- Configure SELinux/AppArmor profiles
- Use systemd for Docker daemon management

```json
// /etc/docker/daemon.json
{
  "userns-remap": "default",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "live-restore": true
}
```

### macOS

- Allocate sufficient resources in Docker Desktop
- Use `:delegated` or `:cached` for bind mounts
- Consider multi-platform builds for ARM (M1/M2)
- Limit file sharing to necessary directories

```yaml
# Better volume performance on macOS
volumes:
  - ./src:/app/src:delegated  # Host writes are delayed
  - ./build:/app/build:cached  # Container writes are cached
```

### Windows

- Choose container type: Windows or Linux
- Use forward slashes in paths
- Ensure drives are shared in Docker Desktop
- Be aware of line ending differences (CRLF vs LF)
- Consider WSL2 backend for better performance

```yaml
# Windows-compatible paths
volumes:
  - C:/Users/name/app:/app  # Forward slashes work
  # or
  - C:\Users\name\app:/app  # Backslashes need escaping in YAML
```

## Performance Best Practices

### Build Performance

```bash
# Use BuildKit (faster, better caching)
export DOCKER_BUILDKIT=1

# Use cache mounts
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Use bind mounts for dependencies
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci
```

### Image Size

- Use multi-stage builds
- Choose minimal base images
- Clean up in the same layer
- Use .dockerignore
- Remove build dependencies

```dockerfile
# Install and cleanup in one layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    package1 \
    package2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### Runtime Performance

```dockerfile
# Use exec form (no shell overhead)
CMD ["node", "server.js"]  # Good
# vs
CMD node server.js         # Bad - spawns shell

# Optimize signals
STOPSIGNAL SIGTERM

# Run as non-root (slightly faster, much more secure)
USER appuser
```

## Security Best Practices Summary

**Image Security:**
- Use official, minimal base images
- Scan for vulnerabilities (Docker Scout, Trivy)
- Don't include secrets in layers
- Run as non-root user
- Keep images updated

**Runtime Security:**
- Drop capabilities
- Use read-only filesystem
- Set resource limits
- Enable security options
- Isolate networks
- Use secrets management

**Compliance:**
- Follow CIS Docker Benchmark
- Implement container scanning in CI/CD
- Use signed images (Docker Content Trust)
- Maintain audit logs
- Regular security reviews

## Common Anti-Patterns to Avoid

❌ **Don't:**
- Run as root
- Use `--privileged`
- Mount Docker socket
- Use `latest` tag
- Hardcode secrets
- Skip health checks
- Ignore resource limits
- Use huge base images
- Skip vulnerability scanning
- Expose unnecessary ports
- Use inefficient layer caching
- Commit secrets to Git

✅ **Do:**
- Run as non-root
- Use minimal capabilities
- Isolate containers
- Tag with versions
- Use secrets management
- Implement health checks
- Set resource limits
- Use minimal images
- Scan regularly
- Apply least privilege
- Optimize build cache
- Use .env.example templates

## Checklist for Production-Ready Images

- [ ] Based on official, versioned, minimal image
- [ ] Multi-stage build (if applicable)
- [ ] Runs as non-root user
- [ ] No secrets in layers
- [ ] .dockerignore configured
- [ ] Vulnerability scan passed
- [ ] Health check implemented
- [ ] Proper labeling (version, description, etc.)
- [ ] Efficient layer caching
- [ ] Resource limits defined
- [ ] Logging configured
- [ ] Signals handled correctly
- [ ] Security options set
- [ ] Documentation complete
- [ ] Tested on target platform(s)

This skill represents current Docker best practices. Always verify against official documentation for the latest recommendations, as Docker evolves continuously.
