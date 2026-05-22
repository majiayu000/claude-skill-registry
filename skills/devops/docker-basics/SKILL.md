---
name: docker-basics
description: Apply when containerizing applications: writing Dockerfiles, docker-compose configurations, and multi-stage builds.
version: 1.1.0
tokens: ~650
confidence: high
sources:
  - https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
  - https://docs.docker.com/compose/
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [docker, containers, devops, deployment]
---

## When to Use

Apply when containerizing applications: writing Dockerfiles, docker-compose configurations, and multi-stage builds.

## Patterns

### Pattern 1: Node.js Dockerfile (Multi-stage)
```dockerfile
# Source: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
# Build stage
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

USER nextjs
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Pattern 2: .dockerignore
```
# Source: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
node_modules
npm-debug.log
.git
.gitignore
.env
.env.*
Dockerfile*
docker-compose*
.dockerignore
README.md
.next
coverage
.nyc_output
```

### Pattern 3: Docker Compose for Development
```yaml
# Source: https://docs.docker.com/compose/
# docker-compose.yml
# Note: version field is deprecated in Compose Specification

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules  # Preserve container's node_modules
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/myapp
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
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

### Pattern 4: Health Checks
```dockerfile
# Source: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
```

```yaml
# In docker-compose
services:
  app:
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
```

### Pattern 5: Common Commands
```bash
# Build image
docker build -t myapp:latest .

# Run container
docker run -d -p 3000:3000 --name myapp myapp:latest

# View logs
docker logs -f myapp

# Execute command in container
docker exec -it myapp sh

# Docker Compose
docker compose up -d        # Start in background
docker compose down         # Stop and remove
docker compose logs -f app  # Follow logs
docker compose exec app sh  # Shell into service
```

### Pattern 6: Environment Variables
```yaml
# docker-compose.yml
services:
  app:
    env_file:
      - .env              # Load from file
    environment:
      - NODE_ENV=production
      - API_KEY=${API_KEY}  # From host environment
```

## Anti-Patterns

- **Running as root** - Always create non-root user
- **No .dockerignore** - Bloats image with unnecessary files
- **Single stage for production** - Use multi-stage builds
- **Hardcoded secrets** - Use env vars or secrets

## Verification Checklist

- [ ] Multi-stage build (separate build/runtime)
- [ ] Non-root user for runtime
- [ ] .dockerignore excludes dev files
- [ ] Health check configured
- [ ] Environment variables externalized
