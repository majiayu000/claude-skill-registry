---
name: docker
description: Docker container building, management, and optimization. Activate for dockerfile, docker-compose, images, containers, multi-stage builds, and container debugging.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Docker Skill

Provides comprehensive Docker container building and management capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Building Docker images
- Writing Dockerfiles
- Container management
- Docker Compose configurations
- Multi-platform builds
- Container optimization

## Quick Reference

### Build Commands
\`\`\`bash
# Build image
docker build -t <name>:<tag> -f <Dockerfile> <context>
docker build -t golden-armada/claude-agent:latest -f deployment/docker/claude/Dockerfile .

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t <name>:<tag> .

# Build with args
docker build --build-arg VERSION=1.0.0 -t <name>:<tag> .
\`\`\`

### Run Commands
\`\`\`bash
# Run container
docker run -d -p 8080:8080 --name agent golden-armada/claude-agent:latest

# Run with environment
docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY golden-armada/claude-agent:latest

# Run interactively
docker run -it --rm golden-armada/claude-agent:latest /bin/sh

# Run with volume
docker run -v $(pwd):/app golden-armada/claude-agent:latest
\`\`\`

### Management
\`\`\`bash
# List
docker ps -a
docker images

# Cleanup
docker system prune -f
docker image prune -a -f
docker container prune -f

# Logs
docker logs <container> --tail=100 -f

# Exec
docker exec -it <container> /bin/sh
\`\`\`

## Dockerfile Best Practices

\`\`\`dockerfile
# 1. Use specific base image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy application
COPY . .

# 5. Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 6. Expose port
EXPOSE 8080

# 7. Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8080/health || exit 1

# 8. Define entrypoint
CMD ["gunicorn", "-b", "0.0.0.0:8080", "agent:app"]
\`\`\`

## Multi-Stage Build Example

\`\`\`dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
\`\`\`

## Golden Armada Docker Commands

\`\`\`bash
# Build Claude agent
docker build -f deployment/docker/claude/Dockerfile \
  -t golden-armada/claude-agent:latest \
  deployment/docker/claude/

# Build orchestrator
docker build -f deployment/docker/orchestrator/Dockerfile \
  -t golden-armada/orchestrator:latest \
  deployment/docker/orchestrator/

# Run locally
docker run -p 8080:8080 \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  golden-armada/claude-agent:latest
\`\`\`
