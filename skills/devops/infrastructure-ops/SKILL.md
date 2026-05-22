---
name: infrastructure-ops
description: Use when the DevOp is working with Docker, containers, cloud services, networking, server configuration, storage, compute scaling, or any infrastructure setup. Activates for Dockerfile creation, docker-compose configuration, cloud resource management, or server administration.
version: 1.0.0
---

# Infrastructure Operations Expertise

## When This Applies

Apply this guidance when:
- Writing or modifying Dockerfiles and docker-compose configs
- Setting up cloud services or infrastructure
- Configuring networking, storage, or compute resources
- Managing server environments

## Docker Best Practices

### Dockerfile Patterns

```dockerfile
# Use specific version tags, never 'latest'
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependency files first (layer caching)
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Copy source code last (changes most frequently)
COPY . .

# Run as non-root user
RUN addgroup -g 1001 appgroup && adduser -u 1001 -G appgroup -D appuser
USER appuser

# Use exec form for CMD
CMD ["node", "server.js"]
```

### Key Docker Rules

1. **Pin versions** — Base images, package managers, and dependencies
2. **Minimize layers** — Combine related RUN commands with `&&`
3. **Use .dockerignore** — Exclude node_modules, .git, tests, docs
4. **Non-root user** — Never run containers as root
5. **Health checks** — Add HEALTHCHECK instruction
6. **Multi-stage builds** — Separate build and runtime stages for smaller images

### Docker Compose

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

## Environment Configuration

### Principles

- **Environment variables** for runtime configuration
- **Never hardcode** secrets, URLs, or environment-specific values
- **Use .env files** for local development (never commit them)
- **Document all variables** in a `.env.example` file
- **Validate on startup** — Fail fast if required config is missing

### Configuration Hierarchy

```
Defaults → .env file → Environment variables → CLI arguments
(lowest priority)                       (highest priority)
```

## Networking

- Use internal Docker networks for service-to-service communication
- Expose only necessary ports
- Use reverse proxies (nginx, traefik) for external traffic
- Configure proper DNS resolution between services
- Set up health checks for load-balanced services

## Security Checklist

- [ ] No secrets in Dockerfiles or docker-compose files
- [ ] Containers run as non-root users
- [ ] Base images are from trusted sources
- [ ] Network access is restricted to what's needed
- [ ] Volumes have appropriate permissions
- [ ] Images are scanned for vulnerabilities
