---
name: docker-helper
description: >-
  Build, debug, and optimize Docker configurations. Use when a user asks to
  create a Dockerfile, fix Docker build errors, optimize image size, write
  docker-compose files, debug container issues, set up multi-stage builds,
  or troubleshoot networking between containers. Covers Dockerfile best
  practices and compose orchestration.
license: Apache-2.0
compatibility: "Requires Docker 20+ installed"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: devops
  tags: ["docker", "containers", "dockerfile", "compose", "devops"]
---

# Docker Helper

## Overview

Create, debug, and optimize Docker configurations including Dockerfiles, docker-compose setups, and container troubleshooting. Follows Docker best practices for security, image size, and build speed.

## Instructions

When a user asks for help with Docker, determine which task they need:

### Task A: Create a Dockerfile

1. Identify the application language and framework
2. Choose the right base image (prefer `-slim` or `-alpine` variants)
3. Use multi-stage builds for compiled languages
4. Follow this ordering for optimal layer caching:

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Runtime
FROM node:20-alpine
WORKDIR /app
RUN addgroup -g 1001 appgroup && adduser -u 1001 -G appgroup -D appuser
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
USER appuser
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Key rules:**
- Copy dependency files first, then source (caching)
- Run as non-root user
- Use `.dockerignore` to exclude `node_modules`, `.git`, `.env`
- Pin base image versions (e.g., `node:20.11-alpine`, not `node:latest`)
- Combine RUN commands to reduce layers

### Task B: Write docker-compose.yml

```yaml
version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

**Key rules:**
- Use `depends_on` with health checks, not just service names
- Use named volumes for persistent data
- Never hardcode secrets in compose files for production (use env files or secrets)
- Set restart policies

### Task C: Debug container issues

Follow this diagnostic sequence:

```bash
# 1. Check container status
docker ps -a

# 2. Read container logs
docker logs <container> --tail 50

# 3. Inspect container details
docker inspect <container> | jq '.[0].State'

# 4. Check resource usage
docker stats --no-stream

# 5. Get a shell inside the container
docker exec -it <container> /bin/sh

# 6. Check networking
docker network ls
docker network inspect <network>
```

Common issues and fixes:
- **Container exits immediately**: Check logs; usually a missing env var or config file
- **Port already in use**: `lsof -i :PORT` to find the conflict
- **Cannot connect between containers**: Ensure they are on the same Docker network and use service names as hostnames
- **Out of disk space**: `docker system prune -a` to clean up unused images and containers
- **Build fails at COPY**: Check `.dockerignore` and verify paths are relative to build context

### Task D: Optimize image size

```bash
# Check current image size
docker images | grep myapp

# Analyze layers
docker history myapp:latest
```

Optimization checklist:
1. Switch to alpine base images
2. Use multi-stage builds (build deps stay in builder stage)
3. Combine RUN commands with `&&`
4. Remove package manager caches: `rm -rf /var/cache/apk/*`
5. Use `.dockerignore` to exclude test files, docs, .git
6. Do not install dev dependencies in the final image

## Examples

### Example 1: Create a Dockerfile for a Python FastAPI app

**User request:** "Create a Dockerfile for my FastAPI project"

**Output Dockerfile:**
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN useradd -r -s /bin/false appuser
COPY --from=builder /install /usr/local
COPY . .
USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Output .dockerignore:**
```
__pycache__
*.pyc
.git
.env
.venv
tests/
*.md
```

**Result:** Image size ~180MB instead of ~1.2GB with the full Python image.

### Example 2: Debug a container that keeps restarting

**User request:** "My web container keeps restarting, can you help?"

**Diagnostic steps:**
```
$ docker ps -a
CONTAINER ID  IMAGE    STATUS                     NAMES
a1b2c3d4e5f6  web:1.0  Restarting (1) 5 sec ago   web

$ docker logs web --tail 20
Error: ECONNREFUSED 127.0.0.1:5432
    at TCPConnectWrap.afterConnect

Root cause: The app is trying to connect to PostgreSQL at 127.0.0.1,
but in Docker the database is a separate container.

Fix: Change DATABASE_URL from localhost to the service name:
  DATABASE_URL=postgres://user:pass@db:5432/myapp
                                     ^^ service name, not localhost
```

## Guidelines

- Always create a `.dockerignore` alongside any Dockerfile.
- Pin base image versions to specific tags, not `latest`.
- Never store secrets in Docker images or Dockerfiles. Use environment variables or Docker secrets.
- For production, always run as a non-root user.
- When optimizing, measure before and after with `docker images`.
- If a build is slow, check layer ordering. Dependencies (package.json, requirements.txt) should be copied and installed before source code.
- For local development, use bind mounts for live reloading. For production, use COPY.
- Health checks should test actual application readiness, not just process existence.
