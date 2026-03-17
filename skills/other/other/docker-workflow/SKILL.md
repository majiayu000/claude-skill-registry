---
name: docker-workflow
description: Comprehensive Docker containerization workflow covering multi-stage builds, docker-compose orchestration, image optimization, debugging, and production best practices. Use when containerizing applications, setting up development environments, or deploying with Docker.
---

# Docker Workflow

## Overview

Docker containerization streamlines development, testing, and deployment by packaging applications with their dependencies into portable, reproducible containers. This skill guides you through professional Docker workflows from development to production.

## Core Capabilities

- **Multi-stage builds**: Separate build and runtime dependencies for optimal image size
- **Docker Compose orchestration**: Manage multi-container applications with networking and dependencies
- **Image optimization**: Reduce image size by 50-90% through best practices
- **Development workflows**: Hot-reload, volume mounting, and environment-specific configs
- **Debugging tools**: Container inspection, health checks, and troubleshooting utilities
- **Production readiness**: Security hardening, health checks, and deployment strategies

## When to Use This Skill

Activate when:
- Containerizing a new application
- Setting up development environments with Docker
- Creating production-ready Docker images
- Orchestrating multi-container applications
- Debugging container issues
- Optimizing Docker builds and images

## Workflow Phases

### Phase 1: Initial Setup

#### Create .dockerignore

Exclude unnecessary files from build context:

```dockerignore
node_modules/
__pycache__/
*.pyc
.git/
.env
*.log
dist/
build/
coverage/
```

See `examples/.dockerignore` for comprehensive template.

**Key principles**:
- Exclude build artifacts and dependencies
- Exclude sensitive files (.env, credentials)
- Exclude version control (.git)
- Smaller context = faster builds

#### Analyze Application Requirements

Determine:
- Runtime (Node.js, Python, Go, Java)
- Dependencies and package managers
- Build vs. runtime requirements
- Port exposure and volume needs

### Phase 2: Multi-Stage Dockerfile

#### Choose Strategy

Multi-stage builds reduce final image size by 50-90%:

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

See `examples/Dockerfile.multi-stage` for templates for Node.js, Python, Go, Java, and Rust.

#### Optimize Layer Caching

Order matters - place changing content last:

```dockerfile
# ✅ GOOD: Dependencies cached separately
COPY package.json package-lock.json ./
RUN npm ci
COPY . .

# ❌ BAD: Any file change invalidates cache
COPY . .
RUN npm ci
```

#### Apply Security Best Practices

```dockerfile
# Use specific versions
FROM node:18.17.1-alpine

# Run as non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
USER nodejs

# Copy with ownership
COPY --chown=nodejs:nodejs . .
```

**Security checklist**:
- Pin base image versions
- Use minimal base images (alpine, slim)
- Run as non-root user
- Scan for vulnerabilities
- Minimize installed packages

### Phase 3: Docker Compose Setup

#### Define Services

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./src:/app/src  # Development hot-reload
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
    networks:
      - app-network

volumes:
  postgres-data:

networks:
  app-network:
```

See `examples/docker-compose.yml` for full-featured setup with monitoring, queues, and caching.

#### Environment Configuration

Use override files for different environments:

**Development (docker-compose.override.yml)**:
```yaml
services:
  app:
    build:
      target: development
    volumes:
      - ./src:/app/src
    environment:
      - NODE_ENV=development
    command: npm run dev
```

**Production (docker-compose.prod.yml)**:
```yaml
services:
  app:
    build:
      target: production
    restart: always
    environment:
      - NODE_ENV=production
```

**Usage**:
```bash
# Development (uses override automatically)
docker-compose up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Phase 4: Build and Run

#### Build Commands

```bash
# Basic build
docker build -t myapp:latest .

# Build specific stage
docker build --target production -t myapp:prod .

# Build with BuildKit (faster)
DOCKER_BUILDKIT=1 docker build -t myapp:latest .
```

#### Run Commands

```bash
# Single container
docker run -d -p 3000:3000 -e NODE_ENV=production myapp:latest

# Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f app

# Execute in container
docker-compose exec app sh

# Stop and remove
docker-compose down -v
```

### Phase 5: Debugging and Troubleshooting

#### Use Helper Script

The `scripts/docker_helper.sh` utility provides common debugging operations:

```bash
# Check container health
./scripts/docker_helper.sh health myapp

# Inspect details
./scripts/docker_helper.sh inspect myapp

# View logs
./scripts/docker_helper.sh logs myapp 200

# Open shell
./scripts/docker_helper.sh shell myapp

# Analyze image size
./scripts/docker_helper.sh size myapp:latest

# Cleanup resources
./scripts/docker_helper.sh cleanup
```

#### Common Issues

**Container exits immediately**:
```bash
docker logs myapp
docker run -it --entrypoint sh myapp:latest
```

**Network connectivity**:
```bash
docker network inspect myapp_default
docker exec myapp ping db
```

**Volume permissions**:
```bash
# Fix in Dockerfile
RUN chown -R nodejs:nodejs /app/data
```

### Phase 6: Optimization

#### Reduce Image Size

**Strategies**:
1. Use smaller base images (alpine > slim > debian)
2. Multi-stage builds to exclude build tools
3. Combine RUN commands for fewer layers
4. Clean up in same layer
5. Use .dockerignore

**Example**:
```dockerfile
# ✅ GOOD: Combined, cleaned up
RUN apt-get update && \
    apt-get install -y --no-install-recommends package1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

#### Build Performance

```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Use cache mounts
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Parallel builds
docker-compose build --parallel
```

### Phase 7: Production Deployment

#### Production Dockerfile

```dockerfile
FROM node:18-alpine AS production

# Security: non-root user
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001

WORKDIR /app
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD node healthcheck.js

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

#### Deployment Commands

```bash
# Tag for registry
docker tag myapp:latest registry.example.com/myapp:v1.0.0

# Push to registry
docker push registry.example.com/myapp:v1.0.0

# Deploy
docker-compose pull && docker-compose up -d

# Rolling update
docker-compose up -d --no-deps --build app
```

## Common Patterns

### Full-Stack Application
- Frontend + Backend + Database + Redis
- See `examples/docker-compose.yml`

### Microservices
- API Gateway + Multiple Services + Message Queue
- Network isolation and service discovery

### Development with Hot Reload
- Volume mounting for source code
- Override files for dev configuration

## Best Practices Summary

### Security
✅ Use specific image versions, not `latest`
✅ Run as non-root user
✅ Use secrets management for sensitive data
✅ Scan images for vulnerabilities
✅ Use minimal base images

### Performance
✅ Use multi-stage builds
✅ Optimize layer caching
✅ Use .dockerignore
✅ Combine RUN commands
✅ Use BuildKit

### Development
✅ Use docker-compose for multi-container apps
✅ Use volumes for hot-reload
✅ Implement health checks
✅ Use proper dependency ordering

### Production
✅ Set restart policies
✅ Use orchestration (Swarm, Kubernetes)
✅ Monitor with health checks
✅ Use reverse proxy
✅ Implement rolling updates

## Helper Resources

- **scripts/docker_helper.sh**: Container inspection, health checks, automation
- **examples/Dockerfile.multi-stage**: Templates for Node.js, Python, Go, Java, Rust
- **examples/docker-compose.yml**: Full-featured multi-service setup
- **examples/.dockerignore**: Comprehensive ignore patterns

## Quick Reference

### Essential Commands

```bash
# Build
docker build -t myapp .
docker-compose build

# Run
docker run -d -p 3000:3000 myapp
docker-compose up -d

# Logs
docker logs -f myapp
docker-compose logs -f

# Execute
docker exec -it myapp sh
docker-compose exec app sh

# Stop
docker-compose down

# Clean
docker system prune -a
```

### Debugging

```bash
# Inspect
docker inspect myapp

# Stats
docker stats myapp

# Networks
docker network inspect bridge

# Volumes
docker volume ls
```
