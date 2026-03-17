---
name: compose-patterns-2025
description: Docker Compose production patterns 2025 including multi-environment strategies, health checks, and modern compose features
---

# Docker Compose Patterns for Production (2025)

## Overview

This skill documents production-ready Docker Compose patterns and best practices for 2025, based on official Docker documentation and industry standards.

## File Format Changes (2025)

**IMPORTANT:** The `version` field is now **obsolete** in Docker Compose v2.42+.

**Correct (2025):**
```yaml
services:
  app:
    image: myapp:latest
```

**Incorrect (deprecated):**
```yaml
version: '3.8'  # DO NOT USE
services:
  app:
    image: myapp:latest
```

## Multiple Environment Strategy

### Pattern: Base + Environment Overrides

**compose.yaml (base):**
```yaml
services:
  app:
    build:
      context: ./app
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=production
    restart: unless-stopped
```

**compose.override.yaml (development - auto-loaded):**
```yaml
services:
  app:
    build:
      target: development
    volumes:
      - ./app/src:/app/src:cached
    environment:
      - NODE_ENV=development
      - DEBUG=*
    ports:
      - "9229:9229"  # Debugger
```

**compose.prod.yaml (production - explicit):**
```yaml
services:
  app:
    build:
      target: production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 512M
      restart_policy:
        condition: on-failure
        max_attempts: 3
```

**Usage:**
```bash
# Development (auto-loads compose.override.yaml)
docker compose up

# Production
docker compose -f compose.yaml -f compose.prod.yaml up -d

# CI/CD
docker compose -f compose.yaml -f compose.ci.yaml up --abort-on-container-exit
```

## Environment Variable Management

### Pattern: .env Files per Environment

**.env.template (committed to git):**
```bash
# Database
DB_HOST=sqlserver
DB_PORT=1433
DB_NAME=myapp
DB_USER=sa
# DB_PASSWORD= (set in actual .env)

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
# REDIS_PASSWORD= (set in actual .env)

# Application
NODE_ENV=production
LOG_LEVEL=info
```

**.env.dev:**
```bash
DB_PASSWORD=Dev!Pass123
REDIS_PASSWORD=redis-dev-123
NODE_ENV=development
LOG_LEVEL=debug
```

**.env.prod:**
```bash
DB_PASSWORD=${PROD_DB_PASSWORD}  # From CI/CD
REDIS_PASSWORD=${PROD_REDIS_PASSWORD}
NODE_ENV=production
LOG_LEVEL=info
```

**Load specific environment:**
```bash
docker compose --env-file .env.dev up
```

## Security Patterns

### Pattern: Run as Non-Root User

```yaml
services:
  app:
    image: node:20-alpine
    user: "1000:1000"  # UID:GID
    read_only: true
    tmpfs:
      - /tmp
      - /app/.cache
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if binding to ports < 1024
    security_opt:
      - no-new-privileges:true
```

**Create user in Dockerfile:**
```dockerfile
FROM node:20-alpine

# Create app user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

# Set ownership
WORKDIR /app
COPY --chown=appuser:appuser . .

USER appuser
```

### Pattern: Secrets Management

**Docker Swarm secrets (production):**
```yaml
services:
  app:
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true  # Managed by Swarm
```

**Access secrets in application:**
```javascript
// Read from /run/secrets/
const fs = require('fs');
const dbPassword = fs.readFileSync('/run/secrets/db_password', 'utf8').trim();
```

**Development alternative (environment):**
```yaml
services:
  app:
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password
```

## Health Check Patterns

### Pattern: Comprehensive Health Checks

**HTTP endpoint:**
```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 40s
```

**Database ping:**
```yaml
services:
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER"]
      interval: 10s
      timeout: 3s
      retries: 3
```

**Custom script:**
```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "node", "/app/scripts/healthcheck.js"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 40s
```

**healthcheck.js:**
```javascript
const http = require('http');

const options = {
  hostname: 'localhost',
  port: 8080,
  path: '/health',
  timeout: 2000
};

const req = http.request(options, (res) => {
  process.exit(res.statusCode === 200 ? 0 : 1);
});

req.on('error', () => process.exit(1));
req.on('timeout', () => {
  req.destroy();
  process.exit(1);
});
req.end();
```

## Dependency Management

### Pattern: Ordered Startup with Conditions

```yaml
services:
  web:
    depends_on:
      database:
        condition: service_healthy
      redis:
        condition: service_started
      migration:
        condition: service_completed_successfully

  database:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s

  redis:
    # No health check needed, just wait for start

  migration:
    image: myapp:latest
    command: npm run migrate
    restart: "no"  # Run once
    depends_on:
      database:
        condition: service_healthy
```

## Network Isolation Patterns

### Pattern: Three-Tier Network Architecture

```yaml
services:
  nginx:
    image: nginx:alpine
    networks:
      - frontend
    ports:
      - "80:80"

  api:
    build: ./api
    networks:
      - frontend
      - backend

  database:
    image: postgres:16-alpine
    networks:
      - backend  # No frontend access

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

### Pattern: Service-Specific Networks

```yaml
services:
  web-app:
    networks:
      - public
      - app-network

  api:
    networks:
      - app-network
      - data-network

  postgres:
    networks:
      - data-network

  redis:
    networks:
      - data-network

networks:
  public:
    driver: bridge
  app-network:
    driver: bridge
    internal: true
  data-network:
    driver: bridge
    internal: true
```

## Volume Patterns

### Pattern: Named Volumes for Persistence

```yaml
services:
  database:
    volumes:
      - db-data:/var/lib/postgresql/data  # Persistent data
      - ./init:/docker-entrypoint-initdb.d:ro  # Init scripts (read-only)
      - db-logs:/var/log/postgresql  # Logs

volumes:
  db-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /mnt/data/postgres  # Host path
  db-logs:
    driver: local
```

### Pattern: Development Bind Mounts

```yaml
services:
  app:
    volumes:
      - ./src:/app/src:cached  # macOS optimization
      - /app/node_modules  # Don't overwrite installed modules
      - app-cache:/app/.cache  # Named volume for cache
```

**Volume mount options:**
- `:ro` - Read-only
- `:rw` - Read-write (default)
- `:cached` - macOS performance optimization (host authoritative)
- `:delegated` - macOS performance optimization (container authoritative)
- `:z` - SELinux single container
- `:Z` - SELinux multi-container

## Resource Management Patterns

### Pattern: CPU and Memory Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

**Calculate total resources:**
```yaml
# 3 app replicas + database + redis
services:
  app:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'      # 3 x 0.5 = 1.5 CPUs
          memory: 512M     # 3 x 512M = 1.5GB

  database:
    deploy:
      resources:
        limits:
          cpus: '2'        # 2 CPUs
          memory: 4G       # 4GB

  redis:
    deploy:
      resources:
        limits:
          cpus: '0.5'      # 0.5 CPUs
          memory: 512M     # 512MB

# Total: 4 CPUs, 6GB RAM minimum
```

## Logging Patterns

### Pattern: Centralized Logging

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        compress: "true"
        labels: "app,environment"
```

**Alternative: Log to stdout/stderr (12-factor):**
```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

**View logs:**
```bash
docker compose logs -f app
docker compose logs --since 30m app
docker compose logs --tail 100 app
```

## Init Container Pattern

### Pattern: Database Migration

```yaml
services:
  migration:
    image: myapp:latest
    command: npm run migrate
    depends_on:
      database:
        condition: service_healthy
    restart: "no"  # Run once
    networks:
      - backend

  app:
    image: myapp:latest
    depends_on:
      migration:
        condition: service_completed_successfully
    networks:
      - backend
```

## YAML Anchors and Aliases

### Pattern: Reusable Configuration

```yaml
x-common-app-config: &common-app
  restart: unless-stopped
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "3"
  security_opt:
    - no-new-privileges:true
  cap_drop:
    - ALL
  cap_add:
    - NET_BIND_SERVICE

services:
  app1:
    <<: *common-app
    build: ./app1
    ports:
      - "8001:8080"

  app2:
    <<: *common-app
    build: ./app2
    ports:
      - "8002:8080"

  app3:
    <<: *common-app
    build: ./app3
    ports:
      - "8003:8080"
```

### Pattern: Environment-Specific Overrides

```yaml
x-logging: &default-logging
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

x-resources: &default-resources
  limits:
    cpus: '1'
    memory: 512M
  reservations:
    cpus: '0.5'
    memory: 256M

services:
  app:
    logging: *default-logging
    deploy:
      resources: *default-resources
```

## Port Binding Patterns

### Pattern: Security-First Port Binding

```yaml
services:
  # Public services
  web:
    ports:
      - "80:8080"
      - "443:8443"

  # Development only (localhost binding)
  debug:
    ports:
      - "127.0.0.1:9229:9229"  # Debugger only accessible from host

  # Environment-based binding
  app:
    ports:
      - "${DOCKER_WEB_PORT_FORWARD:-127.0.0.1:8000}:8000"
```

**Environment control:**
```bash
# Development (.env.dev)
DOCKER_WEB_PORT_FORWARD=127.0.0.1:8000  # Localhost only

# Production (.env.prod)
DOCKER_WEB_PORT_FORWARD=8000  # All interfaces
```

## Restart Policy Patterns

```yaml
services:
  # Always restart (production services)
  app:
    restart: always

  # Restart unless manually stopped (most common)
  database:
    restart: unless-stopped

  # Never restart (one-time tasks)
  migration:
    restart: "no"

  # Restart on failure only (with Swarm)
  worker:
    deploy:
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
```

## Validation and Testing

### Pattern: Pre-Deployment Validation

```bash
#!/bin/bash
set -euo pipefail

echo "Validating Compose syntax..."
docker compose config > /dev/null

echo "Building images..."
docker compose build

echo "Running security scan..."
for service in $(docker compose config --services); do
  image=$(docker compose config | yq ".services.$service.image")
  if [ -n "$image" ]; then
    docker scout cves "$image" || true
  fi
done

echo "Starting services..."
docker compose up -d

echo "Checking health..."
sleep 10
docker compose ps

echo "Running smoke tests..."
curl -f http://localhost:8080/health || exit 1

echo "✓ All checks passed"
```

## Complete Production Example

```yaml
# Modern Compose format (no version field for v2.40+)

x-common-service: &common-service
  restart: unless-stopped
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "3"
  security_opt:
    - no-new-privileges:true

services:
  nginx:
    <<: *common-service
    image: nginxinc/nginx-unprivileged:alpine
    ports:
      - "80:8080"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
    networks:
      - frontend
    depends_on:
      api:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:8080/health"]
      interval: 30s

  api:
    <<: *common-service
    build:
      context: ./api
      dockerfile: Dockerfile
      target: production
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    networks:
      - frontend
      - backend
    depends_on:
      migration:
        condition: service_completed_successfully
      redis:
        condition: service_started
    env_file:
      - .env
    healthcheck:
      test: ["CMD", "node", "healthcheck.js"]
      interval: 30s
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M

  migration:
    image: myapp:latest
    command: npm run migrate
    restart: "no"
    networks:
      - backend
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    <<: *common-service
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password
    secrets:
      - postgres_password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 2G

  redis:
    <<: *common-service
    image: redis:7.4-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local

secrets:
  postgres_password:
    file: ./secrets/postgres_password.txt
```

## Common Mistakes to Avoid

1. **Using `version` field** - Obsolete in 2025
2. **No health checks** - Leads to race conditions
3. **Running as root** - Security risk
4. **No resource limits** - Can exhaust host resources
5. **Hardcoded secrets** - Use secrets or environment variables
6. **No logging limits** - Disk space issues
7. **Bind mounts in production** - Use named volumes
8. **Missing restart policies** - Services don't recover
9. **No network isolation** - All services can talk to each other
10. **Not using .dockerignore** - Larger build contexts

## Troubleshooting Commands

```bash
# Validate syntax
docker compose config

# View merged configuration
docker compose config --services

# Check which file is being used
docker compose config --files

# View environment interpolation
docker compose config --no-interpolate

# Check service dependencies
docker compose config | yq '.services.*.depends_on'

# View resource usage
docker stats $(docker compose ps -q)

# Debug startup issues
docker compose up --no-deps service-name

# Force recreate
docker compose up --force-recreate service-name
```

## References

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose v2.42+ Release Notes](https://github.com/docker/compose/releases)
- [Best Practices](https://docs.docker.com/compose/how-tos/production/)
