---
name: docker-devops
description: Docker orchestration and CI/CD for IntelliFill. Use when configuring containers, writing workflows, or setting up environments.
---

# Docker & DevOps Skill

This skill provides comprehensive guidance for Docker orchestration, CI/CD pipelines, and deployment strategies in IntelliFill.

## Table of Contents

1. [Docker Architecture](#docker-architecture)
2. [Dockerfile Patterns](#dockerfile-patterns)
3. [Docker Compose](#docker-compose)
4. [GitHub Actions](#github-actions)
5. [Environment Management](#environment-management)
6. [Health Checks](#health-checks)
7. [Deployment Strategies](#deployment-strategies)

## Docker Architecture

IntelliFill uses a multi-container architecture with Docker Compose.

### Container Structure

```
IntelliFill/
├── quikadmin/              # Backend API container
│   ├── Dockerfile.dev      # Development build
│   ├── Dockerfile.prod     # Production build
│   └── Dockerfile.test     # Testing build
├── quikadmin-web/          # Frontend UI container
│   ├── Dockerfile.dev
│   └── Dockerfile.prod
├── docker-compose.yml      # Development orchestration
└── docker-compose.e2e.yml  # E2E testing orchestration
```

### Service Overview

```yaml
# Services in docker-compose.yml
services:
  postgres:         # PostgreSQL database
  redis:            # Redis cache & queues
  backend:          # Express API
  frontend:         # React UI
  nginx:            # Reverse proxy (production)
```

## Dockerfile Patterns

IntelliFill uses multi-stage builds for optimization.

### Backend Dockerfile (Development)

```dockerfile
# quikadmin/Dockerfile.dev
FROM node:18-alpine AS base

# Install dependencies for native modules
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    cairo-dev \
    jpeg-dev \
    pango-dev \
    giflib-dev

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY prisma ./prisma/

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Generate Prisma Client
RUN npx prisma generate

# Expose port
EXPOSE 3002

# Development command with hot reload
CMD ["npm", "run", "dev"]
```

### Backend Dockerfile (Production)

```dockerfile
# quikadmin/Dockerfile.prod
FROM node:18-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    cairo-dev \
    jpeg-dev \
    pango-dev

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY prisma ./prisma/

# Install dependencies (production only)
RUN npm ci --only=production

# Copy source
COPY . .

# Generate Prisma Client
RUN npx prisma generate

# Build TypeScript
RUN npm run build

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

# Copy from builder
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/prisma ./prisma
COPY --from=builder /app/package*.json ./

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

USER nodejs

EXPOSE 3002

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3002/api/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1); });"

CMD ["node", "dist/index.js"]
```

### Frontend Dockerfile (Development)

```dockerfile
# quikadmin-web/Dockerfile.dev
FROM oven/bun:1 AS base

WORKDIR /app

# Copy package files
COPY package.json bun.lock ./

# Install dependencies
RUN bun install

# Copy source
COPY . .

EXPOSE 8080

# Development server with hot reload
CMD ["bun", "run", "dev", "--host", "0.0.0.0"]
```

### Frontend Dockerfile (Production)

```dockerfile
# quikadmin-web/Dockerfile.prod
FROM oven/bun:1 AS builder

WORKDIR /app

# Copy package files
COPY package.json bun.lock ./

# Install dependencies
RUN bun install

# Copy source
COPY . .

# Build production bundle
RUN bun run build

# Production stage with nginx
FROM nginx:alpine AS production

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

### Testing Dockerfile

```dockerfile
# quikadmin/Dockerfile.test
FROM node:18-alpine

WORKDIR /app

# Install dependencies
RUN apk add --no-cache \
    python3 \
    make \
    g++

# Copy package files
COPY package*.json ./
COPY prisma ./prisma/

# Install all dependencies (including devDependencies)
RUN npm ci

# Copy source
COPY . .

# Generate Prisma Client
RUN npx prisma generate

# Run tests
CMD ["npm", "run", "test:ci"]
```

## Docker Compose

IntelliFill uses Docker Compose for local development and E2E testing.

### Development Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: intellifill-postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: intellifill
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: intellifill-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./quikadmin
      dockerfile: Dockerfile.dev
    container_name: intellifill-backend
    environment:
      NODE_ENV: development
      PORT: 3002
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/intellifill
      REDIS_URL: redis://redis:6379
    ports:
      - "3002:3002"
    volumes:
      - ./quikadmin:/app
      - /app/node_modules
      - backend_uploads:/app/uploads
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    command: sh -c "npx prisma migrate deploy && npm run dev"

  frontend:
    build:
      context: ./quikadmin-web
      dockerfile: Dockerfile.dev
    container_name: intellifill-frontend
    environment:
      VITE_API_URL: http://localhost:3002/api
    ports:
      - "8080:8080"
    volumes:
      - ./quikadmin-web:/app
      - /app/node_modules
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
  backend_uploads:
```

### E2E Testing Compose

```yaml
# docker-compose.e2e.yml
version: '3.8'

services:
  postgres-test:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: intellifill_test
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis-test:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  backend-test:
    build:
      context: ./quikadmin
      dockerfile: Dockerfile.dev
    environment:
      NODE_ENV: test
      PORT: 3002
      DATABASE_URL: postgresql://postgres:postgres@postgres-test:5432/intellifill_test
      REDIS_URL: redis://redis-test:6379
    ports:
      - "3002:3002"
    depends_on:
      postgres-test:
        condition: service_healthy
      redis-test:
        condition: service_healthy
    command: sh -c "npx prisma migrate deploy && npm run dev"

  frontend-test:
    build:
      context: ./quikadmin-web
      dockerfile: Dockerfile.dev
    environment:
      VITE_API_URL: http://backend-test:3002/api
    ports:
      - "8080:8080"
    depends_on:
      - backend-test

  e2e-runner:
    build:
      context: ./e2e
      dockerfile: Dockerfile
    environment:
      BASE_URL: http://frontend-test:8080
      API_URL: http://backend-test:3002/api
    depends_on:
      - frontend-test
      - backend-test
    command: npm run test:e2e
```

### Production Compose (Example)

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  backend:
    build:
      context: ./quikadmin
      dockerfile: Dockerfile.prod
    environment:
      NODE_ENV: production
      PORT: 3002
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  frontend:
    build:
      context: ./quikadmin-web
      dockerfile: Dockerfile.prod
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

## GitHub Actions

IntelliFill uses GitHub Actions for CI/CD.

### Test Workflow

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend-tests:
    name: Backend Tests
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: intellifill_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: quikadmin/package-lock.json

      - name: Install dependencies
        working-directory: quikadmin
        run: npm ci

      - name: Generate Prisma Client
        working-directory: quikadmin
        run: npx prisma generate

      - name: Run migrations
        working-directory: quikadmin
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/intellifill_test
        run: npx prisma migrate deploy

      - name: Run tests
        working-directory: quikadmin
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/intellifill_test
          REDIS_URL: redis://localhost:6379
        run: npm run test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./quikadmin/coverage/lcov.info
          flags: backend

  frontend-tests:
    name: Frontend Tests
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1

      - name: Install dependencies
        working-directory: quikadmin-web
        run: bun install

      - name: Run tests
        working-directory: quikadmin-web
        run: bun run test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./quikadmin-web/coverage/lcov.info
          flags: frontend

  e2e-tests:
    name: E2E Tests
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build and run E2E tests
        run: |
          docker-compose -f docker-compose.e2e.yml up --abort-on-container-exit --exit-code-from e2e-runner

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: e2e-results
          path: e2e/test-results/
```

### Build and Deploy Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    name: Build and Push Docker Images
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push backend
        uses: docker/build-push-action@v5
        with:
          context: ./quikadmin
          file: ./quikadmin/Dockerfile.prod
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/intellifill-backend:latest
            ${{ secrets.DOCKER_USERNAME }}/intellifill-backend:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Build and push frontend
        uses: docker/build-push-action@v5
        with:
          context: ./quikadmin-web
          file: ./quikadmin-web/Dockerfile.prod
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/intellifill-frontend:latest
            ${{ secrets.DOCKER_USERNAME }}/intellifill-frontend:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /app/intellifill
            docker-compose pull
            docker-compose up -d
            docker system prune -f
```

## Environment Management

### Environment Files

```bash
# .env.example (template)
NODE_ENV=development
PORT=3002

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/intellifill
DIRECT_URL=postgresql://user:password@localhost:5432/intellifill

# Redis
REDIS_URL=redis://localhost:6379

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=xxx
SUPABASE_SERVICE_ROLE_KEY=xxx

# JWT
JWT_SECRET=your-secret-key
```

### Docker Environment Variables

```yaml
# docker-compose.yml
services:
  backend:
    env_file:
      - ./quikadmin/.env
    environment:
      # Override specific variables
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/intellifill
```

### Build Arguments

```dockerfile
# Dockerfile with build args
FROM node:18-alpine

ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV

ARG API_URL
ENV VITE_API_URL=$API_URL

WORKDIR /app
# ...
```

```yaml
# docker-compose.yml with build args
services:
  frontend:
    build:
      context: ./quikadmin-web
      args:
        NODE_ENV: development
        API_URL: http://localhost:3002/api
```

## Health Checks

### Application Health Endpoint

```typescript
// quikadmin/src/api/health.routes.ts
import { Router } from 'express';
import prisma from '../utils/prisma';
import redis from '../utils/redis';

const router = Router();

router.get('/health', async (req, res) => {
  try {
    // Check database
    await prisma.$queryRaw`SELECT 1`;

    // Check Redis
    await redis.ping();

    res.status(200).json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      services: {
        database: 'up',
        redis: 'up',
      },
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      error: error.message,
    });
  }
});

export default router;
```

### Docker Health Checks

```dockerfile
# Dockerfile with health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3002/api/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1); });"
```

```yaml
# docker-compose.yml with health checks
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3002/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Deployment Strategies

### Zero-Downtime Deployment

```bash
#!/bin/bash
# deploy.sh

# Pull latest images
docker-compose pull

# Start new containers
docker-compose up -d --no-deps --scale backend=2 backend

# Wait for health check
sleep 10

# Stop old containers
docker-compose up -d --no-deps --scale backend=1 backend

# Clean up
docker system prune -f
```

### Blue-Green Deployment

```yaml
# docker-compose.blue-green.yml
services:
  backend-blue:
    # Current production
  backend-green:
    # New version
  nginx:
    # Switch between blue/green
```

### Rolling Updates

```bash
# Update one container at a time
for service in backend-1 backend-2 backend-3; do
  docker-compose up -d $service
  sleep 30  # Wait for health check
done
```

## Best Practices

1. **Multi-stage builds** - Separate build and production stages
2. **Layer caching** - Order Dockerfile commands for optimal caching
3. **Non-root user** - Run containers as non-root
4. **Health checks** - Implement health checks for all services
5. **Resource limits** - Set memory and CPU limits
6. **Secrets management** - Use Docker secrets or external secret managers
7. **Volume mounts** - Use named volumes for persistence
8. **Network isolation** - Use custom networks
9. **Graceful shutdown** - Handle SIGTERM signals
10. **Logging** - Configure proper log drivers

## References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/)
