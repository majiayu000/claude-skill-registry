---
name: docker-compose
description: Define and run multi-container Docker applications with Compose. Covers service orchestration, networking, volumes, development environments, and production configurations. Use when setting up local development, multi-service apps, or containerized workflows.
---

# Docker Compose Skill

## Overview

Docker Compose enables defining and running multi-container applications using declarative YAML configuration. This skill covers Compose v2 with file format 3.8+.

## Compose File Structure

### Basic Template

```yaml
# compose.yaml (preferred) or docker-compose.yml
services:
  app:
    image: node:20-alpine
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src
    environment:
      - NODE_ENV=development

networks:
  default:
    driver: bridge

volumes:
  app-data:
```

### Full Structure Reference

```yaml

services: # Container definitions
networks: # Network configurations
volumes: # Named volume definitions
configs: # Configuration objects
secrets: # Sensitive data
```

## Services Configuration

### Image-Based Service

```yaml
services:
  api:
    image: nginx:alpine
    container_name: my-api
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    labels:
      - "traefik.enable=true"
```

### Build-Based Service

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        NODE_      target: development
      cache_from:
        - myapp:cache
    image: myapp:latest
```

### Advanced Build Options

```yaml
services:
  app:
    build:
      context: ./app
      dockerfile: Dockerfile.dev
      args:
        - BUILD_ENV=development
      labels:
        - "com.example.version=1.0"
      platforms:
        - linux/amd64
        - linux/arm64
      secrets:
        - npm_token
      ssh:
        - default
```

## Networks

### Custom Network Configuration

```yaml
services:
  frontend:
    networks:
      - frontend-net

  backend:
    networks:
      - frontend-net
      - backend-net

  database:
    networks:
      - backend-net

networks:
  frontend-net:
    driver: bridge
  backend-net:
    driver: bridge
    internal: true # No external access
```

### Network with Custom IPAM

```yaml
networks:
  app-network:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.28.0.0/16
          gateway: 172.28.0.1
```

### External Networks

```yaml
networks:
  proxy-network:
    external: true
    name: nginx-proxy_default
```

## Volumes

### Named Volumes

```yaml
services:
  db:
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro

volumes:
  postgres-data:
    driver: local
```

### Bind Mounts with Options

```yaml
services:
  app:
    volumes:
      # Read-write bind mount
      - ./src:/app/src:rw
      # Read-only bind mount
      - ./config:/app/config:ro
      # Delegated consistency (macOS performance)
      - ./node_modules:/app/node_modules:delegated
      # Anonymous volume
      - /app/temp
```

### Volume with Driver Options

```yaml
volumes:
  nfs-data:
    driver: local
    driver_opts:
      type: nfs
      o: addr=192.168.1.100,rw
      device: ":/path/to/dir"
```

## Environment Variables

### Inline Environment

```yaml
services:
  app:
    environment:
      - NODE_ENV=production
      - API_URL=https://api.example.com
      - DEBUG=false
```

### Environment from File

```yaml
services:
  app:
    env_file:
      - .env
      - .env.local
    environment:
      # Override specific vars
      - LOG_LEVEL=debug
```

### .env File Best Practices

```bash
# .env file (DO NOT commit to version control)
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret123
POSTGRES_DB=myapp

# .env.example (commit this)
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
```

### Variable Substitution

```yaml
services:
  app:
    image: myapp:${TAG:-latest}
    environment:
      - DATABASE_URL=postgres://${DB_USER}:${DB_PASS}@db:5432/${DB_NAME}
```

## Health Checks

### Basic Health Check

```yaml
services:
  api:
    image: myapp:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Health Check Variants

```yaml
services:
  # HTTP health check
  web:
    healthcheck:
      test: ["CMD-SHELL", "wget -q --spider http://localhost:80 || exit 1"]

  # TCP health check
  redis:
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s

  # Database health check
  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Disable health check
  worker:
    healthcheck:
      disable: true
```

## Dependencies

### Basic Dependencies

```yaml
services:
  app:
    depends_on:
      - db
      - redis

  db:
    image: postgres:15

  redis:
    image: redis:alpine
```

### Conditional Dependencies (Recommended)

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
      migrations:
        condition: service_completed_successfully

  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 10

  migrations:
    build: ./migrations
    depends_on:
      db:
        condition: service_healthy
```

## Profiles

### Define Profiles

```yaml
services:
  app:
    image: myapp:latest
    # Always runs (no profile)

  debug:
    image: myapp:debug
    profiles:
      - debug

  test:
    image: myapp:test
    profiles:
      - test
      - ci

  monitoring:
    image: prometheus:latest
    profiles:
      - monitoring
      - production
```

### Using Profiles

```bash
# Run default services only
docker compose up

# Run with specific profile
docker compose --profile debug up

# Run multiple profiles
docker compose --profile debug --profile monitoring up

# Set via environment
COMPOSE_PROFILES=debug,monitoring docker compose up
```

## Development vs Production Configs

### Base Configuration (compose.yaml)

```yaml
services:
  app:
    image: myapp:${TAG:-latest}
    environment:
      - NODE_ENV=${NODE_ENV:-production}
    restart: unless-stopped

  db:
    image: postgres:15
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

### Development Override (compose.override.yaml)

```yaml
# Automatically loaded with compose.yaml
services:
  app:
    build:
      context: .
      target: development
    volumes:
      - ./src:/app/src
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=*
    ports:
      - "3000:3000"
      - "9229:9229" # Debug port
    command: npm run dev

  db:
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=devpassword
```

### Production Configuration (compose.prod.yaml)

```yaml
services:
  app:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 256M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  db:
    volumes:
      - type: volume
        source: postgres-data
        target: /var/lib/postgresql/data
        volume:
          nocopy: true
```

### Using Multiple Compose Files

```bash
# Development (uses compose.yaml + compose.override.yaml)
docker compose up

# Production
docker compose -f compose.yaml -f compose.prod.yaml up -d

# CI/Testing
docker compose -f compose.yaml -f compose.test.yaml up --abort-on-container-exit
```

## Common Application Stacks

### Node.js + PostgreSQL + Redis

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://postgres:password@db:5432/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./src:/app/src

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=app
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:alpine
    volumes:
      - redis-data:/data

volumes:
  postgres-data:
  redis-data:
```

### Python + FastAPI + MongoDB

```yaml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongo:27017/app
    volumes:
      - ./app:/code/app
    command: uvicorn app.main:app --host 0.0.0.0 --reload
    depends_on:
      mongo:
        condition: service_healthy

  mongo:
    image: mongo:7
    volumes:
      - mongo-data:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5

  mongo-express:
    image: mongo-express
    ports:
      - "8081:8081"
    environment:
      - ME_CONFIG_MONGODB_URL=mongodb://mongo:27017/
    profiles:
      - debug

volumes:
  mongo-data:
```

### Full Stack with Nginx Reverse Proxy

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro
    depends_on:
      - frontend
      - api

  frontend:
    build:
      context: ./frontend
      target: production
    expose:
      - "3000"

  api:
    build:
      context: ./backend
    expose:
      - "8000"
    environment:
      - DATABASE_URL=postgres://postgres:${DB_PASSWORD}@db:5432/app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:
```

## Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G
        reservations:
          cpus: "0.5"
          memory: 512M
    # For Compose standalone (non-Swarm)
    mem_limit: 1g
    memswap_limit: 2g
    cpus: 1.0
```

## Logging Configuration

```yaml
services:
  app:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "5"
        compress: "true"

  # Alternative: syslog
  api:
    logging:
      driver: syslog
      options:
        syslog-address: "tcp://192.168.1.100:514"
        tag: "myapp-api"

  # Disable logging
  noisy-service:
    logging:
      driver: none
```

## Secrets Management

```yaml
services:
  app:
    secrets:
      - db_password
      - api_key
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    environment: API_KEY
```

## Troubleshooting Commands

### Essential Commands

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f [service]

# View running services
docker compose ps

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# Rebuild services
docker compose build --no-cache

# Restart specific service
docker compose restart api

# Execute command in running container
docker compose exec app sh

# Run one-off command
docker compose run --rm app npm test
```

### Debugging Commands

```bash
# Validate compose file
docker compose config

# View parsed compose file
docker compose config --format json

# View service dependencies
docker compose config --services

# Check container resource usage
docker compose top

# View container stats
docker stats $(docker compose ps -q)

# Inspect network
docker network inspect $(docker compose ps -q --format "{{.Networks}}" | head -1)

# View container logs with timestamps
docker compose logs -f -t --tail=100

# Follow logs for specific service
docker compose logs -f api db
```

### Common Issues

```bash
# Port already in use
docker compose down
lsof -i :3000  # Find process using port

# Volume permission issues
docker compose down -v
docker volume prune

# Stale containers
docker compose down --remove-orphans

# Network conflicts
docker network prune

# Rebuild after Dockerfile changes
docker compose up -d --build

# Force recreate containers
docker compose up -d --force-recreate

# Pull latest images
docker compose pull
docker compose up -d
```

### Health Check Debugging

```bash
# Check health status
docker compose ps

# View health check logs
docker inspect --format='{{json .State.Health}}' <container_id> | jq

# Test health check command manually
docker compose exec api curl -f http://localhost:3000/health
```

## Best Practices

### File Organization

```
project/
├── compose.yaml              # Base configuration
├── compose.override.yaml     # Development overrides (git-ignored)
├── compose.prod.yaml         # Production configuration
├── compose.test.yaml         # Test configuration
├── .env.example              # Environment template
├── .env                      # Local environment (git-ignored)
├── docker/
│   ├── app/
│   │   └── Dockerfile
│   └── nginx/
│       └── Dockerfile
└── scripts/
    ├── start-dev.sh
    └── start-prod.sh
```

### Security Checklist

- [ ] Never commit `.env` files with secrets
- [ ] Use secrets for sensitive data in production
- [ ] Set `read_only: true` where possible
- [ ] Use specific image tags, not `latest`
- [ ] Limit container capabilities
- [ ] Use non-root users in containers
- [ ] Enable health checks for all services
- [ ] Use internal networks for backend services

### Performance Tips

```yaml
services:
  app:
    # Use tmpfs for temporary data
    tmpfs:
      - /tmp
      - /app/cache

    # Optimize for macOS/Windows
    volumes:
      - ./src:/app/src:cached

    # Limit logging
    logging:
      driver: json-file
      options:
        max-size: "10m"
```

## Quick Reference

| Command                           | Description             |
| --------------------------------- | ----------------------- |
| `docker compose up -d`            | Start in detached mode  |
| `docker compose down -v`          | Stop and remove volumes |
| `docker compose logs -f`          | Follow all logs         |
| `docker compose exec <svc> sh`    | Shell into container    |
| `docker compose build --no-cache` | Rebuild without cache   |
| `docker compose pull`             | Pull latest images      |
| `docker compose config`           | Validate configuration  |
| `docker compose --profile <p> up` | Start with profile      |
