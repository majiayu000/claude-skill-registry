---
name: docker-composer
description: "Create and manage Docker and Docker Compose configurations. Builds optimized Dockerfiles and multi-service compose setups. Use when user says 'docker', 'dockerize', 'container', 'compose', or 'containerize'."
allowed-tools: Bash, Read, Write, Edit
---

# Docker Composer

You are an expert at containerizing applications with Docker.

## When To Use

- User says "Dockerize this", "Add to compose"
- User mentions "Container setup"
- New service needs containerization
- Development environment setup

## Inputs

- Application type and runtime
- Dependencies (databases, caches, etc.)
- Environment requirements

## Outputs

- Dockerfile
- docker-compose.yml
- .dockerignore
- Documentation

## Dockerfile Best Practices

```dockerfile
# Use specific version tags
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency files first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Use non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Docker Compose Template

```yaml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/dbname
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=dbname
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d dbname"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

## .dockerignore Template

```
.git
.gitignore
.env
.venv
venv
__pycache__
*.pyc
*.pyo
.pytest_cache
.coverage
htmlcov
node_modules
*.log
.DS_Store
README.md
docker-compose*.yml
Dockerfile*
```

## Language-Specific Dockerfiles

### Python (FastAPI)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Node.js

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
USER node
EXPOSE 3000
CMD ["node", "server.js"]
```

### Go

```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o main .

FROM alpine:3.19
WORKDIR /app
COPY --from=builder /app/main .
USER nobody
EXPOSE 8080
CMD ["./main"]
```

## Multi-Stage Builds

For smaller images:

```dockerfile
# Build stage
FROM python:3.12 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "main.py"]
```

## Development vs Production

```yaml
# docker-compose.yml (production)
services:
  app:
    image: myapp:latest
    restart: always

# docker-compose.override.yml (development - auto-loaded)
services:
  app:
    build: .
    volumes:
      - .:/app
    environment:
      - DEBUG=true
```

## Common Services

### Redis

```yaml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
  volumes:
    - redis_data:/data
```

### PostgreSQL

```yaml
postgres:
  image: postgres:16-alpine
  environment:
    POSTGRES_PASSWORD: secret
  volumes:
    - postgres_data:/var/lib/postgresql/data
```

## Anti-Patterns

- Using `latest` tag in production
- Running as root
- Storing secrets in Dockerfile
- No health checks
- Massive image sizes (use slim/alpine)
- Not using .dockerignore
- Installing dev dependencies in production

## Keywords

docker, dockerize, container, compose, containerize, Dockerfile
