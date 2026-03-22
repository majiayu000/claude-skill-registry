---
name: docker-compose-guide
description: >
  Guide for writing Docker Compose files with services, networks, volumes, health checks,
  and environment management. Use when the user creates or modifies docker-compose.yml,
  asks about multi-container setups, local development environments, or service orchestration.
  Trigger whenever Docker Compose, multi-container, or local dev environment is mentioned.
---

# Docker Compose Guide

Write well-structured Docker Compose configurations for local development, testing, and
production-like environments with proper networking, health checks, and dependency management.

## When to Use
- User creates or edits docker-compose.yml
- User sets up a local development environment with multiple services
- User asks about service dependencies, networking, or volumes
- User needs to coordinate database, cache, and app containers
- User asks about environment variable management in Docker

## Core Patterns

### Service Definition with Health Checks

Define services with explicit health checks so dependent services wait for readiness,
not just container start.

```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: myapp
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U myapp -d myapp"]
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 10s
    networks:
      - backend

  redis:
    image: redis:7-alpine
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - backend
```

### Application Service with Dependencies

Use `depends_on` with `condition: service_healthy` to ensure proper startup order.

```yaml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://myapp:secret@postgres:5432/myapp
      REDIS_URL: redis://redis:6379
      NODE_ENV: development
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - backend
      - frontend
    restart: unless-stopped
```

### Profiles for Optional Services

Use profiles to group services that are only needed in specific scenarios.

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"

  mailhog:
    image: mailhog/mailhog:latest
    ports:
      - "1025:1025"
      - "8025:8025"
    profiles:
      - debug

  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@local.dev
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    profiles:
      - debug

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    ports:
      - "9090:9090"
    profiles:
      - monitoring
```

Start with profiles: `docker compose --profile debug --profile monitoring up`

### Networks and Volumes

Explicitly define networks for service isolation and named volumes for data persistence.

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
```

### Environment Variable Management

Use `.env` files for defaults and `environment` for overrides. Never commit secrets.

```yaml
services:
  api:
    env_file:
      - .env
      - .env.local  # Overrides .env, not committed
    environment:
      LOG_LEVEL: ${LOG_LEVEL:-info}
      APP_VERSION: ${APP_VERSION:?APP_VERSION is required}
```

Example `.env` file:

```bash
# .env (committed, defaults only)
COMPOSE_PROJECT_NAME=myapp
LOG_LEVEL=info
NODE_ENV=development
```

## Anti-Patterns

- **Using `depends_on` without health checks**: `depends_on` only waits for container start, not service readiness. Always pair with `condition: service_healthy`.
- **Bind-mounting node_modules**: Overwriting container node_modules with host volume causes platform mismatches. Use anonymous volume exclusion: `/app/node_modules`.
- **Hardcoding passwords in compose file**: Use `env_file`, Docker secrets, or environment variables. Never commit credentials.
- **Using `links`**: Links are legacy. Use Docker networks instead -- services on the same network resolve each other by service name.
- **Not using named volumes**: Anonymous volumes are hard to manage and back up. Always use named volumes for persistent data.
- **Exposing database ports in production**: Only expose database ports for local development. In production, keep databases on internal networks.

## Quick Reference

```bash
# Start all services
docker compose up -d

# Start with specific profiles
docker compose --profile debug up -d

# Rebuild and start
docker compose up -d --build

# View logs
docker compose logs -f api

# Scale a service
docker compose up -d --scale worker=3

# Stop and remove volumes
docker compose down -v

# Execute command in running container
docker compose exec api sh

# Run one-off command
docker compose run --rm api npm test
```
