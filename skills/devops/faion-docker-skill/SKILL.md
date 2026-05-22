---
name: faion-docker-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(docker:*, docker-compose:*)
---

# Docker Operations Mastery

**Container Development and Deployment Best Practices (2025-2026)**

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Dockerfile** | FROM, RUN, COPY, WORKDIR, ENV, CMD, ENTRYPOINT |
| **Multi-stage** | Builder pattern, minimal runtime images |
| **Compose** | Services, networks, volumes, dependencies |
| **Optimization** | Layer caching, image size, build time |
| **Security** | Non-root users, secrets, scanning |
| **Networking** | Bridge, host, overlay, custom networks |
| **Volumes** | Named volumes, bind mounts, tmpfs |
| **Registry** | Push, pull, tagging, private registries |

---

## Core Principles

### 1. Build Once, Run Anywhere

```
Source Code
    |
    v
Dockerfile --> docker build --> Image --> docker run --> Container
                                   |
                                   v
                              Registry (push/pull)
```

### 2. Image Layering

Docker images are built in layers. Each instruction creates a new layer.

```
Layer 4: CMD ["python", "app.py"]     (0 MB)
Layer 3: COPY . /app                  (50 MB)
Layer 2: RUN pip install -r req.txt   (200 MB)
Layer 1: FROM python:3.12-slim        (150 MB)
```

**Rule:** Order instructions from least to most frequently changing for optimal caching.

---

## Dockerfile Patterns

### Base Image Selection

| Image Type | Example | Size | Use Case |
|------------|---------|------|----------|
| **Full** | `python:3.12` | ~900MB | Development, debugging |
| **Slim** | `python:3.12-slim` | ~150MB | Production balance |
| **Alpine** | `python:3.12-alpine` | ~50MB | Minimal size |
| **Distroless** | `gcr.io/distroless/python3` | ~30MB | Maximum security |

**Recommendation:** Start with `-slim`, move to Alpine/Distroless for production.

### Essential Instructions

```dockerfile
# Base image - always pin version
FROM python:3.12-slim

# Labels for metadata
LABEL maintainer="team@example.com"
LABEL version="1.0.0"
LABEL description="Production API service"

# Set working directory
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies (combine RUN commands)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (for layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Expose port (documentation only)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Entry point and command
ENTRYPOINT ["python"]
CMD ["app.py"]
```

### CMD vs ENTRYPOINT

| Instruction | Purpose | Override |
|-------------|---------|----------|
| **ENTRYPOINT** | Defines executable | `--entrypoint` flag |
| **CMD** | Default arguments | Command line args |

```dockerfile
# Pattern 1: ENTRYPOINT for fixed command
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8000"]  # docker run myapp --port 9000

# Pattern 2: CMD for flexible command
CMD ["python", "app.py"]  # docker run myapp sh (replaces entirely)

# Pattern 3: Combined (recommended)
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["gunicorn", "app:app"]
```

### Shell Form vs Exec Form

```dockerfile
# Exec form (recommended) - runs directly
CMD ["python", "app.py"]
ENTRYPOINT ["./entrypoint.sh"]

# Shell form - runs via /bin/sh -c
CMD python app.py
ENTRYPOINT ./entrypoint.sh  # Cannot receive signals properly
```

**Always use exec form** for proper signal handling.

---

## Multi-stage Builds

### Basic Pattern

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Runtime
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Result:** Build tools not in final image, reduced size by ~90%.

### Python Multi-stage

```dockerfile
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home appuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Go Multi-stage (CGO disabled)

```dockerfile
# Stage 1: Build
FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/server

# Stage 2: Runtime (scratch = empty image)
FROM scratch

COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

EXPOSE 8080

ENTRYPOINT ["/server"]
```

**Result:** Final image ~10-20MB.

### TypeScript Multi-stage

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Production dependencies
FROM node:20-alpine AS prod-deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev

# Stage 4: Runtime
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs

COPY --from=builder /app/dist ./dist
COPY --from=prod-deps /app/node_modules ./node_modules

USER nextjs

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

---

## Docker Compose

### Basic Configuration

```yaml
# docker-compose.yml
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - BUILD_ENV=production
    image: myapp:latest
    container_name: myapp
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./data:/app/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:15-alpine
    container_name: myapp-db
    restart: unless-stopped
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - db_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - app-network

volumes:
  db_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

### Development vs Production

```yaml
# docker-compose.yml (base)
version: "3.9"

services:
  app:
    build: .
    networks:
      - app-network

networks:
  app-network:
```

```yaml
# docker-compose.override.yml (development, auto-loaded)
version: "3.9"

services:
  app:
    build:
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - DEBUG=true
    command: npm run dev
```

```yaml
# docker-compose.prod.yml (production)
version: "3.9"

services:
  app:
    build:
      target: production
    restart: unless-stopped
    ports:
      - "80:3000"
    environment:
      - NODE_ENV=production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
```

**Usage:**
```bash
# Development (uses override automatically)
docker compose up

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Service Dependencies

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
      migrations:
        condition: service_completed_successfully

  migrations:
    build: .
    command: python manage.py migrate
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 5s
      timeout: 5s
      retries: 5
```

---

## Image Optimization

### Layer Caching Strategy

```dockerfile
# BAD: Invalidates cache on any code change
COPY . .
RUN pip install -r requirements.txt

# GOOD: Dependencies cached separately
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### Reducing Image Size

| Technique | Example | Impact |
|-----------|---------|--------|
| **Use slim/alpine** | `python:3.12-slim` vs `python:3.12` | -80% |
| **Multi-stage builds** | Separate build/runtime | -50-90% |
| **Remove cache** | `rm -rf /var/lib/apt/lists/*` | -50MB |
| **Combine RUN** | Multiple commands in one RUN | -5-10% |
| **Use .dockerignore** | Exclude unnecessary files | Variable |
| **No dev dependencies** | `npm ci --omit=dev` | -30-50% |

### .dockerignore

```dockerignore
# Git
.git
.gitignore

# Dependencies
node_modules
venv
__pycache__
*.pyc

# Build artifacts
dist
build
*.egg-info

# IDE
.vscode
.idea
*.swp

# Docker
Dockerfile*
docker-compose*
.docker

# Environment
.env
.env.*
*.local

# Tests
tests
test
coverage
.pytest_cache
.coverage

# Documentation
docs
*.md
!README.md

# Misc
*.log
tmp
temp
```

### Analyzing Image Size

```bash
# View image layers
docker history myapp:latest

# Detailed size analysis
docker image inspect myapp:latest --format='{{.Size}}'

# Use dive for deep analysis
dive myapp:latest

# Compare images
docker images --filter "reference=myapp" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

---

## Container Networking

### Network Types

| Type | Use Case | Command |
|------|----------|---------|
| **bridge** (default) | Container-to-container on same host | `docker network create mynet` |
| **host** | Container uses host network | `--network host` |
| **none** | No networking | `--network none` |
| **overlay** | Multi-host communication (Swarm) | `docker network create -d overlay mynet` |
| **macvlan** | Container with MAC address | `docker network create -d macvlan ...` |

### Custom Bridge Network

```bash
# Create network
docker network create --driver bridge \
    --subnet=172.20.0.0/16 \
    --gateway=172.20.0.1 \
    app-network

# Run container on network
docker run -d --name app --network app-network myapp

# Connect running container
docker network connect app-network existing-container

# Inspect network
docker network inspect app-network
```

### DNS and Service Discovery

```yaml
# docker-compose.yml
services:
  app:
    networks:
      app-network:
        aliases:
          - api
          - backend

  db:
    networks:
      app-network:

networks:
  app-network:
```

Containers can reach each other by service name: `postgres://db:5432/mydb`

### Port Mapping

```bash
# Map container port to host
docker run -p 8080:80 nginx          # host:container
docker run -p 127.0.0.1:8080:80 nginx  # bind to localhost only
docker run -p 8080-8090:80-90 nginx    # port range
docker run -P nginx                    # auto-map EXPOSE ports
```

---

## Volume Management

### Volume Types

| Type | Syntax | Use Case |
|------|--------|----------|
| **Named volume** | `mydata:/app/data` | Persistent data |
| **Bind mount** | `./src:/app/src` | Development, configs |
| **tmpfs** | `--tmpfs /tmp` | Temporary, sensitive data |

### Named Volumes

```bash
# Create volume
docker volume create app-data

# Use in container
docker run -v app-data:/app/data myapp

# Inspect volume
docker volume inspect app-data

# Backup volume
docker run --rm -v app-data:/data -v $(pwd):/backup alpine \
    tar czf /backup/backup.tar.gz -C /data .

# Restore volume
docker run --rm -v app-data:/data -v $(pwd):/backup alpine \
    tar xzf /backup/backup.tar.gz -C /data
```

### Compose Volumes

```yaml
services:
  app:
    volumes:
      # Named volume
      - app-data:/app/data
      # Bind mount
      - ./config:/app/config:ro
      # Anonymous volume (preserved on rebuild)
      - /app/node_modules
      # tmpfs (in-memory)
      - type: tmpfs
        target: /tmp
        tmpfs:
          size: 100m

volumes:
  app-data:
    driver: local
    driver_opts:
      type: none
      device: /path/on/host
      o: bind
```

### Volume Best Practices

1. **Use named volumes for persistent data** (databases, uploads)
2. **Use bind mounts for development** (source code, configs)
3. **Use read-only where possible** (`:ro` flag)
4. **Backup volumes regularly**
5. **Clean unused volumes:** `docker volume prune`

---

## Registry Operations

### Docker Hub

```bash
# Login
docker login

# Tag image
docker tag myapp:latest username/myapp:v1.0.0

# Push to registry
docker push username/myapp:v1.0.0

# Pull from registry
docker pull username/myapp:v1.0.0
```

### Private Registry

```bash
# Run local registry
docker run -d -p 5000:5000 --name registry registry:2

# Tag for private registry
docker tag myapp:latest localhost:5000/myapp:v1.0.0

# Push to private registry
docker push localhost:5000/myapp:v1.0.0

# Pull from private registry
docker pull localhost:5000/myapp:v1.0.0
```

### AWS ECR

```bash
# Get login token
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Tag for ECR
docker tag myapp:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:v1.0.0

# Push to ECR
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:v1.0.0
```

### Image Tagging Strategy

| Tag | Purpose | Example |
|-----|---------|---------|
| `latest` | Most recent build | `myapp:latest` |
| Semantic version | Release version | `myapp:1.2.3` |
| Git SHA | Specific commit | `myapp:abc1234` |
| Branch | Feature branches | `myapp:feature-login` |
| Date | Build timestamp | `myapp:2026-01-18` |

**Recommended:** Use semantic versioning + git SHA for production.

```bash
# Tag with multiple tags
docker build -t myapp:latest \
             -t myapp:v1.2.3 \
             -t myapp:$(git rev-parse --short HEAD) \
             .
```

---

## Security Best Practices

### Run as Non-root User

```dockerfile
# Create user
RUN useradd --create-home --shell /bin/bash --uid 1000 appuser

# Copy files with correct ownership
COPY --chown=appuser:appuser . .

# Switch to user
USER appuser
```

### Secrets Management

```yaml
# docker-compose.yml
services:
  app:
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true  # Created via: docker secret create api_key key.txt
```

**Access in container:** `/run/secrets/db_password`

### Security Scanning

```bash
# Scan with Docker Scout
docker scout cves myapp:latest

# Scan with Trivy
trivy image myapp:latest

# Scan with Snyk
snyk container test myapp:latest
```

### Security Checklist

- [ ] Use specific image tags (not `latest` in production)
- [ ] Run as non-root user
- [ ] Use read-only filesystem where possible
- [ ] Drop all capabilities: `--cap-drop ALL`
- [ ] Add only needed capabilities: `--cap-add NET_BIND_SERVICE`
- [ ] Scan images for vulnerabilities
- [ ] Use secrets for sensitive data (not ENV)
- [ ] Set resource limits
- [ ] Use distroless/minimal base images
- [ ] Keep images updated

### Secure Compose Example

```yaml
services:
  app:
    image: myapp:v1.0.0
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
        reservations:
          cpus: "0.25"
          memory: 128M
```

---

## Health Checks

### Dockerfile HEALTHCHECK

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```

### Compose Healthcheck

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### Health Check Options

| Option | Description |
|--------|-------------|
| `--interval` | Time between checks (default: 30s) |
| `--timeout` | Maximum time to wait for check (default: 30s) |
| `--start-period` | Grace period for container startup |
| `--retries` | Consecutive failures before unhealthy |

---

## Common Commands

### Build

```bash
# Build image
docker build -t myapp:latest .

# Build with different Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# Build with build args
docker build --build-arg VERSION=1.0.0 -t myapp:1.0.0 .

# Build without cache
docker build --no-cache -t myapp:latest .

# Build with target stage
docker build --target builder -t myapp:builder .
```

### Run

```bash
# Run interactive
docker run -it --rm myapp:latest bash

# Run detached
docker run -d --name myapp myapp:latest

# Run with environment
docker run -e DATABASE_URL=postgres://... myapp

# Run with port mapping
docker run -p 8080:80 myapp

# Run with volume
docker run -v $(pwd)/data:/app/data myapp

# Run with resource limits
docker run --memory=512m --cpus=0.5 myapp
```

### Compose

```bash
# Start services
docker compose up -d

# Build and start
docker compose up -d --build

# View logs
docker compose logs -f app

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# Execute command in running service
docker compose exec app bash

# Scale service
docker compose up -d --scale app=3
```

### Maintenance

```bash
# View running containers
docker ps

# View all containers
docker ps -a

# View logs
docker logs -f container_name

# Execute in container
docker exec -it container_name bash

# Copy files
docker cp container_name:/app/file.txt ./file.txt

# Prune unused resources
docker system prune -a --volumes
```

---

## Debugging

### Container Inspection

```bash
# Inspect container
docker inspect container_name

# View processes
docker top container_name

# Resource usage
docker stats container_name

# View logs with timestamps
docker logs --timestamps container_name

# Follow logs
docker logs -f --tail 100 container_name
```

### Network Debugging

```bash
# List networks
docker network ls

# Inspect network
docker network inspect bridge

# Test connectivity from container
docker exec -it app ping db
docker exec -it app nslookup db
```

### Build Debugging

```bash
# Build with verbose output
docker build --progress=plain -t myapp .

# Build specific stage
docker build --target builder -t myapp:debug .

# Run shell in build stage
docker run -it --rm myapp:debug sh
```

---

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Using `latest` tag | Unpredictable deployments | Pin specific versions |
| Root user | Security vulnerability | Create non-root user |
| Secrets in ENV | Visible in inspect/logs | Use Docker secrets |
| Large images | Slow deploys, more vulnerabilities | Multi-stage builds |
| Ignoring .dockerignore | Large context, slow builds | Proper exclusions |
| Not using health checks | Silent failures | Add HEALTHCHECK |
| Hardcoding config | Inflexible containers | Use ENV/secrets |
| Single RUN per line | Many layers, large image | Combine RUN commands |

---

## Quick Audits

### Dockerfile Checklist

- [ ] Base image version pinned
- [ ] Non-root user configured
- [ ] .dockerignore present
- [ ] Multi-stage build (if applicable)
- [ ] Layer caching optimized
- [ ] HEALTHCHECK defined
- [ ] Labels for metadata
- [ ] Exec form for CMD/ENTRYPOINT

### Security Checklist

- [ ] No secrets in image
- [ ] Running as non-root
- [ ] Read-only filesystem (if possible)
- [ ] Resource limits set
- [ ] Image scanned for vulnerabilities
- [ ] Base image updated recently

### Production Checklist

- [ ] Image tagged with version
- [ ] Health checks configured
- [ ] Logging to stdout/stderr
- [ ] Graceful shutdown handled
- [ ] Environment variables documented
- [ ] Resource limits defined
- [ ] Restart policy set

---

## Tools

| Tool | Purpose |
|------|---------|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | GUI for Docker management |
| [Docker Scout](https://docs.docker.com/scout/) | Vulnerability scanning |
| [Dive](https://github.com/wagoodman/dive) | Image layer analysis |
| [Hadolint](https://github.com/hadolint/hadolint) | Dockerfile linting |
| [Trivy](https://github.com/aquasecurity/trivy) | Security scanning |
| [Buildx](https://github.com/docker/buildx) | Multi-platform builds |
| [Docker Compose](https://docs.docker.com/compose/) | Multi-container orchestration |
| [Lazydocker](https://github.com/jesseduffield/lazydocker) | Terminal UI for Docker |

---

## Sources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Compose Specification](https://docs.docker.com/compose/compose-file/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [Hadolint Rules](https://github.com/hadolint/hadolint#rules)


---

## Methodologies

| ID | Name | File |
|----|------|------|
| M-DO-001 | Cicd Github Actions | [methodologies/M-DO-001_cicd_github_actions.md](methodologies/M-DO-001_cicd_github_actions.md) |
| M-DO-002 | Cicd Gitlab Ci | [methodologies/M-DO-002_cicd_gitlab_ci.md](methodologies/M-DO-002_cicd_gitlab_ci.md) |
| M-DO-003 | Docker Basics | [methodologies/M-DO-003_docker_basics.md](methodologies/M-DO-003_docker_basics.md) |
| M-DO-004 | Docker Compose | [methodologies/M-DO-004_docker_compose.md](methodologies/M-DO-004_docker_compose.md) |
| M-DO-005 | Kubernetes Basics | [methodologies/M-DO-005_kubernetes_basics.md](methodologies/M-DO-005_kubernetes_basics.md) |
| M-DO-006 | Helm Charts | [methodologies/M-DO-006_helm_charts.md](methodologies/M-DO-006_helm_charts.md) |
| M-DO-007 | Aws Ec2 | [methodologies/M-DO-007_aws_ec2.md](methodologies/M-DO-007_aws_ec2.md) |
| M-DO-008 | Aws Lambda | [methodologies/M-DO-008_aws_lambda.md](methodologies/M-DO-008_aws_lambda.md) |
| M-DO-009 | Terraform Basics | [methodologies/M-DO-009_terraform_basics.md](methodologies/M-DO-009_terraform_basics.md) |
| M-DO-010 | Infrastructure Patterns | [methodologies/M-DO-010_infrastructure_patterns.md](methodologies/M-DO-010_infrastructure_patterns.md) |
| M-DO-011 | Monitoring Prometheus | [methodologies/M-DO-011_monitoring_prometheus.md](methodologies/M-DO-011_monitoring_prometheus.md) |
| M-DO-012 | Logging Elk | [methodologies/M-DO-012_logging_elk.md](methodologies/M-DO-012_logging_elk.md) |
| M-DO-013 | Tracing Jaeger | [methodologies/M-DO-013_tracing_jaeger.md](methodologies/M-DO-013_tracing_jaeger.md) |
| M-DO-014 | Secrets Management | [methodologies/M-DO-014_secrets_management.md](methodologies/M-DO-014_secrets_management.md) |
| M-DO-015 | Ssl Certificates | [methodologies/M-DO-015_ssl_certificates.md](methodologies/M-DO-015_ssl_certificates.md) |
| M-DO-016 | Backup Recovery | [methodologies/M-DO-016_backup_recovery.md](methodologies/M-DO-016_backup_recovery.md) |
| M-DO-017 | Networking Basics | [methodologies/M-DO-017_networking_basics.md](methodologies/M-DO-017_networking_basics.md) |
| M-DO-018 | Dns Route53 | [methodologies/M-DO-018_dns_route53.md](methodologies/M-DO-018_dns_route53.md) |
| M-DO-019 | Cdn Cloudfront | [methodologies/M-DO-019_cdn_cloudfront.md](methodologies/M-DO-019_cdn_cloudfront.md) |
| M-DO-020 | Container Registry | [methodologies/M-DO-020_container_registry.md](methodologies/M-DO-020_container_registry.md) |
| M-DO-021 | Security Scanning | [methodologies/M-DO-021_security_scanning.md](methodologies/M-DO-021_security_scanning.md) |
| M-DO-022 | Cost Optimization | [methodologies/M-DO-022_cost_optimization.md](methodologies/M-DO-022_cost_optimization.md) |
| M-DO-023 | Database Operations | [methodologies/M-DO-023_database_operations.md](methodologies/M-DO-023_database_operations.md) |
| M-DO-024 | Feature Flags | [methodologies/M-DO-024_feature_flags.md](methodologies/M-DO-024_feature_flags.md) |
| M-DO-025 | Incident Management | [methodologies/M-DO-025_incident_management.md](methodologies/M-DO-025_incident_management.md) |
| M-DO-026 | Gitops | [methodologies/M-DO-026_gitops.md](methodologies/M-DO-026_gitops.md) |
| M-DO-027 | Service Mesh | [methodologies/M-DO-027_service_mesh.md](methodologies/M-DO-027_service_mesh.md) |
| M-DO-028 | Slo Sli | [methodologies/M-DO-028_slo_sli.md](methodologies/M-DO-028_slo_sli.md) |
