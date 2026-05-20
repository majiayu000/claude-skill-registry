---
name: docker-essentials
description: Docker and Docker Compose patterns - Dockerfile best practices, multi-stage builds, compose networking, and container debugging. Auto-triggers when working with containers.
---

# Docker Essentials Skill

## Dockerfile Best Practices

### Multi-Stage Build (Python)

```dockerfile
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN pip install uv && \
    uv sync --frozen --no-dev --no-editable

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src/ ./src/

ENV PATH="/app/.venv/bin:$PATH"

# Non-root user
RUN useradd -r -s /bin/false appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Multi-Stage Build (Node.js)

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./

USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Layer Caching Rules

| Order | What to COPY                                        | Why                       |
| ----- | --------------------------------------------------- | ------------------------- |
| 1     | Dependency files (`pyproject.toml`, `package.json`) | Changes least often       |
| 2     | Install dependencies                                | Cached unless deps change |
| 3     | Application code                                    | Changes most often        |

```dockerfile
# GOOD: Dependencies cached separately
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY src/ ./src/

# BAD: Busts cache on every code change
COPY . .
RUN uv sync --frozen
```

### Security Hardening

```dockerfile
# Use specific version tags (never :latest in production)
FROM python:3.12.8-slim

# Don't run as root
RUN useradd -r -s /bin/false appuser
USER appuser

# Read-only filesystem where possible
# (set at runtime: docker run --read-only)

# No unnecessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Scan for vulnerabilities
# docker scout cves my-image
```

## Docker Compose

### Development Setup

```yaml
# compose.yaml (preferred over docker-compose.yml)
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: builder # Use build stage for dev
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src # Hot reload
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD:?required}@db:5432/${POSTGRES_DB:-app}
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-app}
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD in .env}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

### Networking

```yaml
services:
  frontend:
    networks:
      - frontend-net

  api:
    networks:
      - frontend-net
      - backend-net

  db:
    networks:
      - backend-net # Not accessible from frontend

networks:
  frontend-net:
  backend-net:
```

### Production Overrides

```yaml
# compose.prod.yaml
services:
  app:
    build:
      target: runtime # Use production stage
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 1G
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

```bash
# Run with production overrides
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

## Container Debugging

### Common Commands

```bash
# View logs (follow mode)
docker compose logs -f app

# Execute shell in running container
docker compose exec app bash

# View resource usage
docker stats

# Inspect container details
docker inspect <container>

# View container processes
docker top <container>

# Copy files from container
docker cp <container>:/app/debug.log ./debug.log
```

### Debugging a Crashed Container

```bash
# Check why it exited
docker compose logs app --tail 50

# Start with shell instead of CMD
docker compose run --entrypoint /bin/sh app

# Inspect the last state
docker inspect --format='{{.State.ExitCode}}' <container>
docker inspect --format='{{.State.Error}}' <container>
```

### Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

## .dockerignore

```
.git
.github
.venv
__pycache__
*.pyc
node_modules
.env
*.md
tests/
docs/
.claude/
```

## Image Size Optimization

| Technique                            | Savings |
| ------------------------------------ | ------- |
| Use `-slim` or `-alpine` base images | 50-90%  |
| Multi-stage builds                   | 30-70%  |
| Combine RUN commands                 | 5-15%   |
| Remove package manager caches        | 5-10%   |
| Use `.dockerignore`                  | Varies  |

```bash
# Check image size
docker images my-app

# Analyze layers
docker history my-app

# Deep dive into layers
docker scout cves my-app
```

## Activation Triggers

This skill auto-activates when prompts contain:

- "docker", "dockerfile", "container"
- "compose", "docker-compose", "docker compose"
- "image", "build image", "multi-stage"
- "container debug", "docker logs"

## Integration

- **k8s-operations** skill: Deploying containers to Kubernetes
- **@infrastructure-engineer** agent: Docker and infra management
- **cicd-automation** skill: Docker in CI/CD pipelines
