---
name: docker-containerization
description: Auto-activates when user mentions Docker, containerize, Dockerfile, docker-compose, or container setup. Creates optimized Docker configurations for applications.
category: devops
---

# Docker Containerization

Creates production-ready Docker configurations with multi-stage builds and optimization.

## When This Activates

- User says: "containerize this", "Docker setup", "create Dockerfile"
- User mentions: "docker-compose", "container", "dockerize"
- Files: Dockerfile, docker-compose.yml being created/edited
- Deployment questions involving containers

## Docker Best Practices

### 1. Multi-Stage Builds

```dockerfile
# --- Build Stage ---
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY bun.lockb ./

# Install dependencies
RUN npm ci --only=production

# Copy source
COPY . .

# Build application
RUN npm run build

# --- Production Stage ---
FROM node:18-alpine AS runner

WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nodejs

# Copy built assets from builder
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./

# Switch to non-root user
USER nodejs

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "dist/index.js"]
```

### 2. Optimized Layering

```dockerfile
# Bad: Copies everything, cache invalidates on any file change
COPY . .
RUN npm install

# Good: Copy dependencies first (cached unless package.json changes)
COPY package*.json ./
RUN npm ci --only=production
COPY . .
```

### 3. .dockerignore

```
node_modules
npm-debug.log
.env
.env.local
.git
.gitignore
README.md
.DS_Store
*.md
.vscode
.idea
dist
build
coverage
```

## Docker Compose for Development

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules  # Prevent overwriting node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    command: npm run dev

  db:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Production Docker Compose

```yaml
version: '3.8'

services:
  app:
    image: myapp:latest
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - NODE_ENV=production
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
```

## Framework-Specific Dockerfiles

### Next.js Application

```dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package*.json ./
RUN npm ci

# Rebuild source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### Python FastAPI

```dockerfile
FROM python:3.11-slim AS base

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install dependencies
FROM base AS builder

COPY requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

# Production stage
FROM base AS runner

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .

RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Optimization Techniques

### 1. Layer Caching

```dockerfile
# ✅ Cache-friendly order (least → most frequently changing)
COPY package*.json ./
RUN npm ci
COPY tsconfig.json ./
COPY src ./src
RUN npm run build

# ❌ Cache-unfriendly (any change invalidates all)
COPY . .
RUN npm ci && npm run build
```

### 2. Reduce Image Size

```dockerfile
# Use alpine variants
FROM node:18-alpine  # ~170MB vs node:18 ~900MB

# Remove build dependencies
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && npm ci \
    && apk del .build-deps

# Clean up
RUN rm -rf /tmp/* /var/cache/apk/*
```

### 3. Security

```dockerfile
# Run as non-root
USER nodejs

# Scan for vulnerabilities
RUN npm audit --production

# Use specific versions (not 'latest')
FROM node:18.17.0-alpine
```

## Common Commands

```bash
# Build image
docker build -t myapp:latest .

# Build with build args
docker build --build-arg NODE_ENV=production -t myapp:prod .

# Run container
docker run -p 3000:3000 myapp:latest

# Run with environment variables
docker run -p 3000:3000 --env-file .env myapp:latest

# Docker Compose
docker-compose up -d          # Start in background
docker-compose down           # Stop and remove
docker-compose logs -f app    # Follow logs
docker-compose exec app sh    # Shell into container

# Clean up
docker system prune -a        # Remove unused images/containers
docker volume prune           # Remove unused volumes
```

## Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD node healthcheck.js || exit 1
```

```javascript
// healthcheck.js
const http = require('http');

const options = {
  host: 'localhost',
  port: 3000,
  path: '/health',
  timeout: 2000
};

const request = http.request(options, (res) => {
  if (res.statusCode === 200) {
    process.exit(0);
  } else {
    process.exit(1);
  }
});

request.on('error', () => process.exit(1));
request.end();
```

## Best Practices Checklist

- [ ] Multi-stage builds (separate build and runtime)
- [ ] Non-root user for security
- [ ] .dockerignore file to exclude unnecessary files
- [ ] Layer caching optimization (dependencies before source)
- [ ] Health checks defined
- [ ] Specific base image versions (no :latest)
- [ ] Environment variables for configuration
- [ ] Minimal image size (alpine variants)
- [ ] Production-only dependencies
- [ ] Proper signal handling (SIGTERM)

**Generate Dockerfiles, present to user, create files with approval.**
