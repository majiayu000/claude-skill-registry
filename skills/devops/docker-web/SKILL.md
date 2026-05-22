---
name: docker-web
description: Containerizes web applications with Docker for consistent deployments across environments. Use when creating Dockerfiles, building container images, or setting up Docker Compose for development.
---

# Docker for Web Applications

Containerize web applications for consistent development and deployment across environments.

## Quick Start

```bash
# Create Dockerfile
touch Dockerfile

# Build image
docker build -t my-app .

# Run container
docker run -p 3000:3000 my-app

# Docker Compose
docker compose up
```

## Node.js Dockerfile

### Basic

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

### Production Optimized

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Prune dev dependencies
RUN npm prune --production

# Production stage
FROM node:20-alpine AS production

WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nodeuser

# Copy built app
COPY --from=builder --chown=nodeuser:nodejs /app/dist ./dist
COPY --from=builder --chown=nodeuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodeuser:nodejs /app/package.json ./

USER nodeuser

ENV NODE_ENV=production
EXPOSE 3000

CMD ["node", "dist/index.js"]
```

## Next.js Dockerfile

### Standalone Output

```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

### next.config.js

```javascript
/** @type {import('next').NextConfig} */
module.exports = {
  output: 'standalone',
};
```

## React (Vite) Dockerfile

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage with nginx
FROM nginx:alpine AS production

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### nginx.conf

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## Docker Compose

### Development

```yaml
# docker-compose.yml
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
      - /app/node_modules
    environment:
      - NODE_ENV=development
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Production

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://user:password@db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  postgres_data:
```

## .dockerignore

```
# Dependencies
node_modules
npm-debug.log

# Build output
dist
build
.next

# Git
.git
.gitignore

# IDE
.idea
.vscode

# Environment
.env*
!.env.example

# Tests
coverage
*.test.js
*.test.ts
__tests__

# Docker
Dockerfile*
docker-compose*
.dockerignore

# Misc
README.md
*.md
```

## Multi-Stage Best Practices

### Separate Stages

```dockerfile
# Base - shared configuration
FROM node:20-alpine AS base
WORKDIR /app
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

# Dependencies
FROM base AS deps
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile

# Build
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm build

# Production deps only
FROM base AS prod-deps
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod --frozen-lockfile

# Runner
FROM base AS runner
ENV NODE_ENV=production
COPY --from=prod-deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

### Build Arguments

```dockerfile
ARG NODE_VERSION=20
FROM node:${NODE_VERSION}-alpine AS base

ARG API_URL
ENV NEXT_PUBLIC_API_URL=${API_URL}
```

```bash
docker build --build-arg NODE_VERSION=20 --build-arg API_URL=https://api.example.com .
```

## Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
```

```yaml
# docker-compose.yml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Security Best Practices

### Non-Root User

```dockerfile
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser

USER appuser
```

### Read-Only Filesystem

```yaml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp
    volumes:
      - app_data:/app/data
```

### Security Scanning

```bash
# Scan image for vulnerabilities
docker scout cves my-app

# Trivy
trivy image my-app
```

## Common Commands

```bash
# Build
docker build -t my-app .
docker build -t my-app:v1.0 --target production .

# Run
docker run -p 3000:3000 my-app
docker run -d --name my-app -p 3000:3000 my-app
docker run --env-file .env my-app

# Compose
docker compose up
docker compose up -d
docker compose up --build
docker compose down
docker compose logs -f

# Inspect
docker ps
docker logs my-app
docker exec -it my-app sh

# Clean up
docker system prune
docker image prune
docker volume prune
```

See [references/patterns.md](references/patterns.md) for framework-specific patterns.
