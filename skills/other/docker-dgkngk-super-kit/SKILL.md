---
name: docker
description: Container optimization, multi-stage builds, Docker Compose, and Docker best practices. Use when writing Dockerfiles, setting up containers, or optimizing image size.
---

# Docker Skill

## Overview
Container optimization, multi-stage builds, and Docker best practices.

## Multi-Stage Build

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app

# Install dependencies first (cache layer)
COPY package*.json ./
RUN npm ci

# Build application
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS production
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy only production dependencies
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Run as non-root
USER nextjs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

EXPOSE 3000
CMD ["node", "dist/server.js"]
```

## Docker Compose

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      target: production
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

volumes:
  postgres_data:
  redis_data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## Best Practices

### Image Size Optimization
```dockerfile
# Use alpine base
FROM node:20-alpine

# Install only production deps
RUN npm ci --only=production

# Remove unnecessary files
RUN rm -rf /var/cache/apk/*
```

### .dockerignore
```
node_modules
.git
.gitignore
*.md
.env*
coverage
.nyc_output
dist
```

### Security
- Run as non-root user
- Use secrets for sensitive data
- Scan images: `docker scout cves myimage`
- Keep base images updated
