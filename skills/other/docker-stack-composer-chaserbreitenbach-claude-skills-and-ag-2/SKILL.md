---
name: docker-stack-composer
version: 1.0.0
description: |
  Multi-service Docker deployment configuration generator with support for
  development, staging, and production environments.
author: QuantQuiver AI R&D
license: MIT

category: tooling
tags:
  - docker
  - docker-compose
  - containers
  - deployment
  - devops
  - microservices
  - infrastructure

dependencies:
  skills: []
  python: ">=3.9"
  packages:
    - pyyaml
  tools:
    - bash
    - code_execution

triggers:
  - "docker compose"
  - "container setup"
  - "multi-service deployment"
  - "Docker configuration"
  - "containerize application"
  - "microservices stack"
  - "Docker stack"
---

# Docker Stack Composer

## Purpose

A multi-service Docker deployment configuration generator that produces complete docker-compose configurations with support for development, staging, and production environments, including networking, volumes, health checks, and security best practices.

**Problem Space:**
- Manual Docker configuration is repetitive and error-prone
- Environment-specific configurations often diverge
- Security best practices frequently overlooked
- Service dependencies complex to manage

**Solution Approach:**
- Template-based generation with environment overrides
- Built-in security configurations (non-root users, read-only filesystems)
- Service dependency management with health checks
- Development/production configuration separation

## When to Use

- New microservices architecture setup
- Containerizing existing applications
- Setting up development environments
- Production deployment configurations
- Multi-service local development
- Database + cache + app stack setup

## When NOT to Use

- Kubernetes deployments (use Helm charts)
- Single-container applications without dependencies
- Serverless deployments
- When using managed container services (ECS task definitions)

---

## Core Instructions

### Stack Architecture Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMMON STACK PATTERNS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Pattern 1: Web Application Stack                               │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐        │
│  │  Nginx  │──▶│   App   │──▶│  Redis  │   │ Postgres│        │
│  │ (proxy) │   │ (Flask) │   │ (cache) │   │  (db)   │        │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘        │
│                                                                 │
│  Pattern 2: Microservices                                       │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                      │
│  │ Gateway │──▶│Service A│──▶│Service B│                      │
│  └─────────┘   └─────────┘   └─────────┘                      │
│       │             │             │                            │
│       └─────────────┴─────────────┘                            │
│                     │                                          │
│              ┌─────────────┐                                   │
│              │  Message    │                                   │
│              │   Queue     │                                   │
│              └─────────────┘                                   │
│                                                                 │
│  Pattern 3: Data Pipeline                                       │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐        │
│  │ Ingress │──▶│  Kafka  │──▶│ Worker  │──▶│TimescaleDB│       │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Service Configuration Schema

```yaml
services:
  service_name:
    # Image configuration
    image: "image:tag"           # Or build context
    build:
      context: ./path
      dockerfile: Dockerfile
      args:
        - ARG=value

    # Runtime configuration
    container_name: service_name
    restart: unless-stopped      # always | on-failure | no
    user: "1000:1000"           # Non-root user

    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          memory: 256M

    # Networking
    ports:
      - "8080:80"               # host:container
    networks:
      - frontend
      - backend
    expose:
      - "80"                    # Internal only

    # Environment
    environment:
      - KEY=value
    env_file:
      - .env

    # Storage
    volumes:
      - ./data:/app/data:ro     # Read-only mount
      - cache:/app/cache        # Named volume

    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

    # Dependencies
    depends_on:
      db:
        condition: service_healthy
```

### Standard Procedures

#### 1. Identify Services

Map application components to container services:
- Web servers (nginx, traefik)
- Application servers (python, node, go)
- Databases (postgres, mysql, mongo)
- Caches (redis, memcached)
- Message queues (rabbitmq, kafka)
- Monitoring (prometheus, grafana)

#### 2. Configure Networks

```yaml
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

#### 3. Define Volumes

```yaml
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
```

#### 4. Environment Separation

Create override files:
- `docker-compose.yml` - Base configuration
- `docker-compose.override.yml` - Development defaults
- `docker-compose.prod.yml` - Production overrides

### Security Best Practices

```yaml
# Security-hardened service template
services:
  app:
    image: app:latest
    user: "1000:1000"              # Non-root user
    read_only: true                # Read-only root filesystem
    tmpfs:
      - /tmp                       # Writable tmp
      - /var/run                   # Writable runtime
    security_opt:
      - no-new-privileges:true     # Prevent privilege escalation
    cap_drop:
      - ALL                        # Drop all capabilities
    cap_add:
      - NET_BIND_SERVICE           # Only add what's needed
```

### Decision Framework

**Database Selection:**
| Use Case | Database | Why |
|----------|----------|-----|
| General CRUD | PostgreSQL | Full-featured, reliable |
| Document store | MongoDB | Flexible schema |
| Time-series | TimescaleDB | Optimized for time data |
| Key-value | Redis | Speed, caching |
| Graph data | Neo4j | Relationship queries |

**Cache Selection:**
| Use Case | Cache | Why |
|----------|-------|-----|
| Simple caching | Redis | Feature-rich, persistent |
| Session store | Redis | Built-in TTL |
| Distributed cache | Redis Cluster | Scalability |

---

## Templates

### Web Application Stack

```yaml
# docker-compose.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      app:
        condition: service_healthy
    networks:
      - frontend
    restart: unless-stopped

  app:
    build:
      context: .
      dockerfile: Dockerfile
    expose:
      - "8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - frontend
      - backend
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    networks:
      - backend
    restart: unless-stopped

networks:
  frontend:
  backend:
    internal: true

volumes:
  postgres_data:
  redis_data:
```

### Development Override

```yaml
# docker-compose.override.yml (auto-loaded in dev)
version: '3.8'

services:
  app:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/__pycache__
    environment:
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    command: ["python", "-m", "flask", "run", "--reload", "--host=0.0.0.0"]

  db:
    ports:
      - "5432:5432"  # Expose for local tools

  redis:
    ports:
      - "6379:6379"
```

### Production Override

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  nginx:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M

  app:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          memory: 512M
    environment:
      - DEBUG=false
      - LOG_LEVEL=INFO
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp

  db:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

### Multi-Stage Dockerfile

```dockerfile
# Dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Development stage
FROM python:3.11-slim as development

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY . .

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

# Production stage
FROM python:3.11-slim as production

RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/* && rm -rf /wheels

COPY --chown=app:app . .

USER app

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app()"]
```

---

## Examples

### Example 1: Flask + PostgreSQL + Redis

**Input**: "Create Docker setup for my Flask API with PostgreSQL and Redis"

**Output**: Complete docker-compose.yml with:
- Flask app service with health checks
- PostgreSQL with persistent volume
- Redis for caching
- Proper networking (backend isolated)
- Development override with hot reload

### Example 2: Microservices Setup

**Input**: "Set up Docker for 3 microservices communicating via RabbitMQ"

**Output**: docker-compose.yml with:
- 3 service definitions
- RabbitMQ with management UI
- Service discovery via Docker DNS
- Health checks for all services
- Shared network configuration

---

## Validation Checklist

Before finalizing Docker configuration:

- [ ] All services have health checks
- [ ] Volumes defined for persistent data
- [ ] Networks properly segmented
- [ ] Environment variables not hardcoded
- [ ] Resource limits set for production
- [ ] Non-root users where possible
- [ ] Dependencies use service_healthy condition
- [ ] Restart policies appropriate
- [ ] Secrets not in image or compose file

---

## Related Resources

- Skill: `cicd-pipeline-generator` - Add Docker build to CI/CD
- Skill: `system-hardening-toolkit` - Host security
- Docker Compose Documentation: https://docs.docker.com/compose/
- Docker Security Best Practices: https://docs.docker.com/develop/security-best-practices/

---

## Changelog

### 1.0.0 (January 2026)
- Initial release
- Web application stack templates
- Microservices patterns
- Development/production separation
- Security hardening templates
