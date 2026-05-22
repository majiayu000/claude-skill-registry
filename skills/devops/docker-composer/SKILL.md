---
name: docker-composer
description: Expert guide for creating Docker Compose configurations, Dockerfiles, and container orchestration. Use when containerizing applications, setting up development environments, or configuring multi-container deployments.
---

# Docker Composer Skill

## Overview

This skill helps you create efficient Docker configurations for development and production. Covers Dockerfiles, Docker Compose, multi-stage builds, networking, volumes, and container orchestration best practices.

## Docker Philosophy

### Container Principles
1. **One process per container**: Keep containers focused
2. **Immutable infrastructure**: Don't modify running containers
3. **Stateless containers**: Store state in volumes or external services
4. **Minimal images**: Smaller = faster + more secure

### Best Practices
- **DO**: Use multi-stage builds for production
- **DO**: Pin specific versions for dependencies
- **DO**: Use `.dockerignore` to exclude unnecessary files
- **DO**: Run as non-root user
- **DON'T**: Store secrets in images or Dockerfiles
- **DON'T**: Use `latest` tag in production
- **DON'T**: Install unnecessary packages

## Dockerfile Patterns

### Node.js Production Dockerfile

```dockerfile
# Dockerfile
# ============================================
# Stage 1: Dependencies
# ============================================
FROM node:20-alpine AS deps
WORKDIR /app

# Install dependencies only when needed
COPY package.json package-lock.json ./
RUN npm ci --only=production

# ============================================
# Stage 2: Builder
# ============================================
FROM node:20-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Build application
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# ============================================
# Stage 3: Runner (Production)
# ============================================
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built assets
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### Python Production Dockerfile

```dockerfile
# Dockerfile
# ============================================
# Stage 1: Builder
# ============================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# Stage 2: Runner
# ============================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Create non-root user
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash appuser

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application
COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Development Dockerfile

```dockerfile
# Dockerfile.dev
FROM node:20-alpine

WORKDIR /app

# Install development dependencies
RUN apk add --no-cache git

# Copy package files first (for caching)
COPY package.json package-lock.json ./

# Install all dependencies (including devDependencies)
RUN npm install

# Don't copy files - mount as volume for hot reload
# COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

## Docker Compose Configurations

### Full-Stack Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  # ===================
  # Application
  # ===================
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules  # Exclude node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-network

  # ===================
  # Database
  # ===================
  db:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # ===================
  # Redis Cache
  # ===================
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    networks:
      - app-network

  # ===================
  # Admin Tools
  # ===================
  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

### Production Configuration

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    image: myapp:${VERSION:-latest}
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    env_file:
      - .env.production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - app-network
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: ${DB_NAME}
    secrets:
      - db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app
    networks:
      - app-network

secrets:
  db_password:
    file: ./secrets/db_password.txt

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: overlay
```

### Development Override Pattern

```yaml
# docker-compose.override.yml (auto-loaded with docker-compose.yml)
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug
    command: npm run dev

  db:
    ports:
      - "5432:5432"  # Expose for local tools

  redis:
    ports:
      - "6379:6379"  # Expose for local tools
```

## Advanced Patterns

### Multi-Service Monorepo

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Frontend
  web:
    build:
      context: .
      dockerfile: apps/web/Dockerfile
    ports:
      - "3000:3000"
    environment:
      - API_URL=http://api:4000
    depends_on:
      - api
    networks:
      - frontend
      - backend

  # Backend API
  api:
    build:
      context: .
      dockerfile: apps/api/Dockerfile
    ports:
      - "4000:4000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    networks:
      - backend

  # Background Workers
  worker:
    build:
      context: .
      dockerfile: apps/worker/Dockerfile
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    deploy:
      replicas: 2
    networks:
      - backend

  # Shared services
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - backend

networks:
  frontend:
  backend:

volumes:
  postgres_data:
  redis_data:
```

### Local Services Stack

```yaml
# docker-compose.services.yml
# Run local versions of external services for development
version: '3.8'

services:
  # Local S3-compatible storage
  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"  # Console
    volumes:
      - minio_data:/data
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"

  # Local email testing
  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI

  # Local Stripe webhooks
  stripe-cli:
    image: stripe/stripe-cli
    command: listen --api-key ${STRIPE_SECRET_KEY} --forward-to http://app:3000/api/webhooks/stripe
    depends_on:
      - app

  # Elasticsearch
  elasticsearch:
    image: elasticsearch:8.11.0
    ports:
      - "9200:9200"
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  # Kibana (Elasticsearch UI)
  kibana:
    image: kibana:8.11.0
    ports:
      - "5601:5601"
    environment:
      ELASTICSEARCH_HOSTS: http://elasticsearch:9200
    depends_on:
      - elasticsearch

volumes:
  minio_data:
  elasticsearch_data:
```

### Testing Configuration

```yaml
# docker-compose.test.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.test
    environment:
      - NODE_ENV=test
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/myapp_test
    depends_on:
      db:
        condition: service_healthy
    command: npm run test:ci

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: myapp_test
    tmpfs:
      - /var/lib/postgresql/data  # Use tmpfs for speed
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 2s
      timeout: 5s
      retries: 5

  # E2E testing
  playwright:
    image: mcr.microsoft.com/playwright:v1.40.0-focal
    volumes:
      - .:/app
      - /app/node_modules
    working_dir: /app
    environment:
      - CI=true
      - BASE_URL=http://app:3000
    depends_on:
      - app
    command: npx playwright test
```

## .dockerignore

```dockerignore
# .dockerignore

# Dependencies
node_modules
npm-debug.log
yarn-error.log

# Build output
.next
dist
build
out

# Development
.git
.gitignore
*.md
!README.md

# IDE
.vscode
.idea
*.swp
*.swo

# Environment
.env
.env.*
!.env.example

# Tests
coverage
*.test.js
*.spec.js
__tests__
e2e
playwright-report

# Docker
Dockerfile*
docker-compose*
.docker

# Misc
.DS_Store
*.log
tmp
```

## Docker Commands Reference

### Development Workflow

```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f app

# Rebuild after package changes
docker-compose up -d --build

# Run one-off commands
docker-compose exec app npm run migrate
docker-compose exec app npm run seed

# Stop everything
docker-compose down

# Stop and remove volumes (reset database)
docker-compose down -v
```

### Production Workflow

```bash
# Build production image
docker build -t myapp:1.0.0 .

# Run with production config
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale app=3

# Rolling update
docker-compose pull app
docker-compose up -d --no-deps app
```

### Debugging

```bash
# Shell into running container
docker-compose exec app sh

# Inspect container
docker inspect <container_id>

# View resource usage
docker stats

# Clean up unused resources
docker system prune -a

# View networks
docker network ls
docker network inspect app-network
```

## Health Checks

### Application Health Check

```typescript
// src/app/api/health/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  const checks = {
    uptime: process.uptime(),
    timestamp: new Date().toISOString(),
    database: false,
    redis: false,
  };

  try {
    // Check database
    await db.execute('SELECT 1');
    checks.database = true;
  } catch (e) {
    console.error('Database health check failed:', e);
  }

  try {
    // Check Redis
    await redis.ping();
    checks.redis = true;
  } catch (e) {
    console.error('Redis health check failed:', e);
  }

  const isHealthy = checks.database && checks.redis;

  return NextResponse.json(checks, {
    status: isHealthy ? 200 : 503
  });
}
```

### Docker Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1
```

## Checklist

### Dockerfile
- [ ] Multi-stage build for production
- [ ] Non-root user
- [ ] Minimal base image (alpine when possible)
- [ ] Layer caching optimized (dependencies before code)
- [ ] Health check defined
- [ ] `.dockerignore` configured

### Docker Compose
- [ ] Services have health checks
- [ ] Volumes for persistent data
- [ ] Networks for service isolation
- [ ] Resource limits defined
- [ ] Restart policies configured
- [ ] Environment variables externalized

### Security
- [ ] No secrets in Dockerfile or docker-compose
- [ ] Images scanned for vulnerabilities
- [ ] Minimal privileges (no root)
- [ ] Network isolation between services

## When to Use This Skill

Invoke this skill when:
- Containerizing a new application
- Setting up development environments with Docker
- Creating multi-service architectures
- Optimizing Docker builds
- Debugging container issues
- Setting up CI/CD pipelines with Docker
- Migrating from docker-compose to Kubernetes
