---
name: docker-expert
description: Expert-level Docker containerization, image optimization, and container orchestration. Use this skill for building efficient Docker images, managing containers, and implementing Docker best practices.
tags: ['devops', 'containers', 'docker', 'infrastructure']
version: 1.0.0
category: devops
allowed-tools:
  - Read
  - Write
  - Bash(docker:*, docker-compose:*)
license: Apache-2.0
compatibility:
  - agentskills
  - claude-code
metadata:
  version: 1.0.0
  author: PCL Team
  category: devops
  tags:
    - docker
    - containers
    - devops
    - orchestration
---

# Docker Expert

You are an expert in Docker containerization with deep knowledge of Dockerfile optimization, multi-stage builds, container security, networking, and Docker Compose orchestration.

## Core Expertise

### Docker Fundamentals

- **Images**: Building, layering, caching strategies, image optimization
- **Containers**: Lifecycle management, resource limits, health checks
- **Registries**: Docker Hub, private registries, image tagging strategies
- **Storage**: Volumes, bind mounts, tmpfs mounts
- **Networking**: Bridge, host, overlay, custom networks
- **Security**: User namespaces, capabilities, secrets management

### Dockerfile Best Practices

- **Multi-stage builds**: Reducing image size and build time
- **Layer optimization**: Minimizing layers and cache invalidation
- **Base images**: Choosing appropriate base images (Alpine, Distroless, scratch)
- **Build arguments**: Parameterized builds
- **Health checks**: Container health monitoring
- **Signals**: Proper signal handling and graceful shutdown

### Docker Compose

- **Service definition**: Multi-container applications
- **Dependencies**: Service dependencies and startup order
- **Networking**: Service discovery and communication
- **Volumes**: Persistent data management
- **Environment variables**: Configuration management
- **Profiles**: Environment-specific configurations

## Best Practices

### 1. Dockerfile Optimization

**Multi-stage build for minimal size:**

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app

# Copy only production dependencies and built files
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY package.json ./

# Run as non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Layer caching optimization:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (changes less frequently)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (changes more frequently)
COPY . .

CMD ["python", "app.py"]
```

**Use .dockerignore:**

```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.DS_Store
*.md
dist
coverage
.pytest_cache
__pycache__
```

### 2. Security Best Practices

**Run as non-root user:**

```dockerfile
FROM node:20-alpine

# Create app user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Copy and install as root
COPY package*.json ./
RUN npm ci --only=production

# Copy app files
COPY --chown=nodejs:nodejs . .

# Switch to non-root user
USER nodejs

EXPOSE 3000
CMD ["node", "server.js"]
```

**Use distroless images:**

```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o app

# Production stage with distroless
FROM gcr.io/distroless/static-debian11
COPY --from=builder /app/app /app
ENTRYPOINT ["/app"]
```

**Scan images for vulnerabilities:**

```bash
# Using Docker Scout
docker scout cves my-image:latest

# Using Trivy
trivy image my-image:latest
```

### 3. Resource Management

**Set resource limits:**

```yaml
# docker-compose.yml
services:
  app:
    image: my-app:latest
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

**Health checks:**

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1
```

### 4. Networking

**Custom network for service isolation:**

```yaml
services:
  frontend:
    networks:
      - frontend-network

  backend:
    networks:
      - frontend-network
      - backend-network

  database:
    networks:
      - backend-network

networks:
  frontend-network:
  backend-network:
```

## Common Tasks

### Task 1: Create Optimized Node.js Image

```dockerfile
# Multi-stage build for Node.js application
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including dev)
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Prune dev dependencies
RUN npm prune --production

# Production image
FROM node:20-alpine

# Add security updates
RUN apk add --no-cache dumb-init

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy built application and dependencies
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs package.json ./

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD node healthcheck.js || exit 1

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/index.js"]
```

### Task 2: Python Application with Dependencies

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1001 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Task 3: Multi-Service Application with Docker Compose

```yaml
version: '3.9'

services:
  # Frontend service
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - '3000:3000'
    environment:
      - API_URL=http://backend:4000
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - app-network
    restart: unless-stopped

  # Backend service
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - '4000:4000'
    environment:
      - DATABASE_URL=postgresql://user:password@database:5432/mydb
      - REDIS_URL=redis://cache:6379
    depends_on:
      database:
        condition: service_healthy
      cache:
        condition: service_started
    networks:
      - app-network
      - db-network
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:4000/health']
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped

  # PostgreSQL database
  database:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - db-network
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U user']
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis cache
  cache:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge
  db-network:
    driver: bridge

volumes:
  postgres-data:
  redis-data:
```

### Task 4: Development Environment with Hot Reload

```yaml
version: '3.9'

services:
  app:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - '3000:3000'
      - '9229:9229' # Node.js debugger
    environment:
      - NODE_ENV=development
    command: npm run dev
```

**Dockerfile with development target:**

```dockerfile
FROM node:20-alpine AS base
WORKDIR /app
COPY package*.json ./

FROM base AS development
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]

FROM base AS production
RUN npm ci --only=production
COPY . .
CMD ["node", "dist/index.js"]
```

### Task 5: Build and Deploy

```bash
# Build image
docker build -t my-app:latest .

# Build with specific target
docker build --target production -t my-app:prod .

# Build with build args
docker build --build-arg NODE_ENV=production -t my-app:latest .

# Tag for registry
docker tag my-app:latest registry.example.com/my-app:1.0.0

# Push to registry
docker push registry.example.com/my-app:1.0.0

# Run container
docker run -d \
  --name my-app \
  --restart unless-stopped \
  -p 3000:3000 \
  -e NODE_ENV=production \
  my-app:latest

# Using Docker Compose
docker-compose up -d
docker-compose ps
docker-compose logs -f
docker-compose down
```

## Anti-Patterns to Avoid

### ❌ Don't Run as Root

```dockerfile
# Bad
FROM node:20
WORKDIR /app
COPY . .
CMD ["node", "server.js"]  # Runs as root

# Good
FROM node:20
WORKDIR /app
COPY . .
RUN useradd -m appuser
USER appuser
CMD ["node", "server.js"]
```

### ❌ Don't Install Unnecessary Packages

```dockerfile
# Bad
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    curl wget vim emacs nano  # Unnecessary in production

# Good
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
```

### ❌ Don't Use Latest Tag in Production

```dockerfile
# Bad
FROM node:latest  # Unpredictable

# Good
FROM node:20.10.0-alpine3.18  # Specific version
```

### ❌ Don't Embed Secrets in Images

```dockerfile
# Bad
COPY .env .
ENV API_KEY=secret123  # Hard-coded secret

# Good
# Use secrets or environment variables at runtime
docker run -e API_KEY=$API_KEY my-app
# Or use Docker secrets (Swarm/Kubernetes)
```

## Advanced Patterns

### BuildKit Cache Mounts

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.21-alpine

WORKDIR /app

# Cache go modules
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=bind,source=go.sum,target=go.sum \
    --mount=type=bind,source=go.mod,target=go.mod \
    go mod download

COPY . .

# Cache build artifacts
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app/server .

CMD ["/app/server"]
```

### Docker Compose with Profiles

```yaml
services:
  app:
    profiles: ['production', 'development']
    # ...

  test-db:
    profiles: ['development']
    # Only runs in development
    image: postgres:16-alpine

  monitoring:
    profiles: ['production']
    # Only runs in production
    image: prometheus
```

```bash
# Run with specific profile
docker-compose --profile development up
docker-compose --profile production up
```

## Checklist

When creating Docker images:

- [ ] Use multi-stage builds to reduce image size
- [ ] Run containers as non-root user
- [ ] Use specific image tags, not `latest`
- [ ] Add `.dockerignore` file
- [ ] Optimize layer caching
- [ ] Set health checks
- [ ] Define resource limits
- [ ] Use distroless or minimal base images
- [ ] Scan images for vulnerabilities
- [ ] Handle signals properly (SIGTERM)
- [ ] Set proper restart policies
- [ ] Use secrets management (not environment variables)
- [ ] Document exposed ports and volumes
- [ ] Test images before deploying

## Resources

- **Official Documentation**: [Docker Docs](https://docs.docker.com/)
- **Best Practices**: [Docker Build Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- **Security**: [Docker Security](https://docs.docker.com/engine/security/)
- **Compose Spec**: [Compose Specification](https://compose-spec.io/)
