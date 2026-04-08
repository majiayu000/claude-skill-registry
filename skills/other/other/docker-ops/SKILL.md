---
name: docker-ops
description: Dockerfile best practices, multi-stage builds, docker-compose, container networking, volume management, and image optimization.
---

# Docker Operations

Practical patterns for building, running, and maintaining containers in production.

## Multi-Stage Builds

Minimize final image size by separating build-time dependencies from runtime.

```dockerfile
# Stage 1: Builder
FROM node:20-alpine AS builder
WORKDIR /app

# Copy dependency manifests first (layer cache)
COPY package*.json ./
RUN npm ci --only=production

COPY tsconfig.json ./
COPY src/ ./src/
RUN npm run build

# Stage 2: Runtime (no devDependencies, no source files)
FROM node:20-alpine AS runtime
WORKDIR /app

# Security: run as non-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

USER appuser

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

```dockerfile
# Python multi-stage example
FROM python:3.12-slim AS builder
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.12-slim AS runtime
WORKDIR /app

COPY --from=builder /install /usr/local
COPY src/ ./src/

RUN useradd -r -s /bin/false appuser
USER appuser

CMD ["python", "-m", "src.main"]
```

## Docker Compose for Multi-Service Environments

```yaml
# docker-compose.yml
version: '3.9'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@postgres:5432/appdb
      - REDIS_URL=redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped
    networks:
      - internal
    deploy:
      resources:
        limits:
          memory: 512m
          cpus: '0.5'

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    networks:
      - internal

volumes:
  postgres_data:
  redis_data:

networks:
  internal:
    driver: bridge
```

## Container Networking

```bash
# Bridge network (default, same host)
docker network create --driver bridge my-network
docker run --network my-network --name service-a my-image

# Containers on same bridge network communicate by name
curl http://service-a:3000/health

# Host network (container shares host network stack, Linux only)
docker run --network host my-image

# Overlay network (multi-host, Docker Swarm or manual)
docker network create --driver overlay --attachable my-overlay
```

```yaml
# Compose network isolation example
services:
  frontend:
    networks:
      - public      # exposed to outside

  api:
    networks:
      - public      # receives traffic from frontend
      - internal    # talks to DB

  postgres:
    networks:
      - internal    # NOT reachable from frontend

networks:
  public:
  internal:
    internal: true  # blocks external traffic
```

## Volume Management

```yaml
# Named volumes (managed by Docker, persistent)
volumes:
  db_data:          # docker manages path
  uploads:
    driver: local

services:
  app:
    volumes:
      - uploads:/app/uploads         # named volume
      - ./config:/app/config:ro      # bind mount (read-only)
      - type: tmpfs                  # in-memory, discarded on stop
        target: /tmp
        tmpfs:
          size: 100m
```

```bash
# Volume lifecycle commands
docker volume ls
docker volume inspect my-volume
docker volume rm my-volume
docker volume prune           # remove all unused volumes (careful in prod)

# Backup a named volume
docker run --rm \
  -v my-volume:/source:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/volume-backup.tar.gz -C /source .

# Restore
docker run --rm \
  -v my-volume:/target \
  -v $(pwd):/backup \
  alpine tar xzf /backup/volume-backup.tar.gz -C /target
```

## Health Checks

```dockerfile
# HEALTHCHECK in Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

```yaml
# Override in docker-compose
services:
  api:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      start_period: 20s
      retries: 3
```

```typescript
// Express health endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  })
})
```

## .dockerignore Best Practices

```
# .dockerignore
node_modules
.git
.gitignore
*.log
*.md
.env
.env.*
coverage/
dist/
.next/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
Dockerfile*
docker-compose*.yml
.dockerignore
```

## Image Layer Caching Optimization

```dockerfile
# BAD: invalidates cache on any source change
COPY . .
RUN npm install

# GOOD: dependency layer cached unless package.json changes
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
```

```dockerfile
# Python: cache pip install separately
COPY requirements.txt .
RUN pip install -r requirements.txt   # cached until requirements.txt changes

COPY . .
```

## Environment Variable Management

```yaml
# docker-compose: prefer env_file over inline secrets
services:
  api:
    env_file:
      - .env.production         # loaded from file, not committed
    environment:
      - NODE_ENV=production     # override specific vars inline
```

```dockerfile
# ARG (build-time only, not in final image)
ARG BUILD_VERSION=unknown
LABEL version=$BUILD_VERSION

# ENV (runtime, visible in container)
ENV PORT=3000
ENV LOG_LEVEL=info
```

## Docker Secrets vs Env Vars

```yaml
# Docker Swarm secrets (production approach)
secrets:
  db_password:
    external: true

services:
  api:
    secrets:
      - db_password
    # Secret mounted at /run/secrets/db_password (file)
```

```typescript
// Read secret from file (not env var)
import { readFileSync } from 'fs'

function getSecret(name: string): string {
  const secretPath = `/run/secrets/${name}`
  try {
    return readFileSync(secretPath, 'utf-8').trim()
  } catch {
    return process.env[name.toUpperCase()] ?? ''
  }
}

const dbPassword = getSecret('db_password')
```

## Container Resource Limits

```yaml
# docker-compose deploy limits
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '0.5'          # max 50% of one CPU
          memory: 512m
        reservations:
          cpus: '0.25'
          memory: 256m
```

```bash
# docker run resource flags
docker run \
  --memory="512m" \
  --memory-swap="1g" \
  --cpus="0.5" \
  my-image
```

## Image Scanning for Vulnerabilities

```bash
# Trivy (recommended, free)
trivy image my-app:latest
trivy image --severity HIGH,CRITICAL my-app:latest
trivy image --exit-code 1 --severity CRITICAL my-app:latest  # fail on critical

# Snyk (SaaS, requires account)
snyk container test my-app:latest

# Docker Scout (built-in with Docker Desktop)
docker scout cves my-app:latest
docker scout recommendations my-app:latest
```

## Debugging Containers

```bash
# View logs
docker logs -f container-name
docker logs --tail 100 container-name
docker compose logs -f service-name

# Exec into running container
docker exec -it container-name sh
docker exec -it container-name bash

# Inspect container metadata
docker inspect container-name
docker inspect --format '{{.NetworkSettings.IPAddress}}' container-name

# Check resource usage
docker stats
docker stats --no-stream container-name

# Copy files to/from container
docker cp container-name:/app/logs/error.log ./error.log
docker cp ./config.json container-name:/app/config.json
```

## PID 1 Problem and Signal Handling (tini)

```dockerfile
# BAD: Node.js as PID 1 does not forward signals properly
CMD ["node", "dist/index.js"]

# GOOD: use tini as init process
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "dist/index.js"]
```

```yaml
# docker-compose init option (Docker 18.06+)
services:
  api:
    init: true      # uses tini automatically
```

```typescript
// Graceful shutdown in Node.js
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully')
  await server.close()
  await db.disconnect()
  process.exit(0)
})
```

## Common Pitfalls

```dockerfile
# AVOID: running as root
# USER root  ← dangerous

# AVOID: latest tag in production
# FROM node:latest  ← use specific version

# AVOID: installing dev tools in production image
# RUN apt-get install -y vim curl wget

# AVOID: secrets in build args (visible in image history)
# ARG SECRET_KEY=abc123

# PREFER: specific digest for reproducible builds
FROM node:20.11.0-alpine@sha256:abc123...
```

**Key principle**: Keep images small, run as non-root, pin versions, use multi-stage builds, always define health checks.
