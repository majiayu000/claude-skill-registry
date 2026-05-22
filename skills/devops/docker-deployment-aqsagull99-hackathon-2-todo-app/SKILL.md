---
name: docker-deployment
description: Comprehensive Docker containerization for Python/FastAPI applications, from simple hello-world apps to production-ready deployments with security best practices, multi-stage builds, and optimized configurations. Use when containerizing Python/FastAPI applications for development, testing, or production environments, including Dockerfile creation, Docker Compose setup, security hardening, and production optimization.
---

# Docker Deployment for Python/FastAPI Applications

This skill provides comprehensive support for containerizing Python/FastAPI applications, from simple hello-world apps to production-ready deployments with security best practices, including prerequisite verification and resource configuration for AI services.

## Prerequisites Validation

Before using this skill, verify your Docker installation and system resources:

### Docker Installation Verification
```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Test Docker functionality
docker run hello-world

# Check Docker system info
docker info
```

### System Resource Requirements
For AI services and production deployments:
- Minimum 4GB RAM allocated to Docker
- Recommended 8GB+ RAM for AI workloads
- At least 2 CPU cores allocated
- Sufficient disk space for container images

### Docker Desktop Setup (Recommended)
```bash
# For Linux
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# For AI services with GPU support (Linux)
sudo apt install nvidia-container-toolkit
sudo systemctl restart docker
```

## When to Use This Skill

Use this skill when you need to:
1. Containerize Python/FastAPI applications with optimized Dockerfiles
2. Create multi-stage builds for security and efficiency
3. Generate Docker Compose files for multi-service applications
4. Apply security best practices to Docker configurations
5. Optimize applications for production deployment
6. Set up proper environment variables and secrets management
7. Configure resource allocation for AI services and heavy workloads
8. Validate Docker installation and system prerequisites

## Resource Configuration for AI Services

When deploying AI services or resource-intensive applications, configure Docker resources appropriately:

### Docker Run Resource Constraints
```bash
# Memory and CPU limits
docker run -m 4g --cpus=2.0 my-ai-service

# With GPU support (NVIDIA)
docker run --gpus all -m 8g --cpus=4.0 my-ai-service

# PID limits for container isolation
docker run --pids-limit 100 my-ai-service
```

### Docker Compose Resource Configuration
```yaml
version: "3.8"

services:
  ai-service:
    image: my-ai-service:latest
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 8G
          pids: 200
        reservations:
          cpus: '2.0'
          memory: 4G
    # For GPU support
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

### Docker Desktop Resource Allocation
For Docker Desktop:
1. Go to Settings > Resources
2. Allocate sufficient memory (recommended 8GB+ for AI workloads)
3. Set CPU cores (at least 4 for AI services)
4. Configure Swap space if needed

## Quick Start

### Basic Dockerfile Generation
For a simple Python/FastAPI application:

```dockerfile
# syntax=docker/dockerfile:1

# === Build stage: Install dependencies and create virtual environment ===
FROM python:3.11-slim AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# === Final stage: Create minimal runtime image ===
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Copy Python dependencies from builder stage
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Make sure scripts in .local are usable
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Dockerfile with Security Hardened Images (DHI)
For enhanced security in production:

```dockerfile
# syntax=docker/dockerfile:1

# === Build stage: Install dependencies and create virtual environment ===
FROM dhi.io/python:3.11-alpine3.18-dev AS builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN python -m venv /app/venv
COPY requirements.txt .

# Install any additional packages if needed using apk
RUN apk add --no-cache gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt

# === Final stage: Create minimal runtime image ===
FROM dhi.io/python:3.11-alpine3.18

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

# Create non-root user for security
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

COPY app.py ./
COPY --from=builder /app/venv /app/venv

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Multi-Service Docker Compose Setup

For applications requiring databases and other services:

```yaml
version: "3.8"

services:
  web:
    build:
      context: .
      target: final
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:15
    restart: unless-stopped
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

## Advanced Security Configuration

For production environments with secrets management:

```yaml
version: "3.8"

services:
  web:
    build:
      context: .
      target: final
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
    env_file:
      - .env
    secrets:
      - db_password
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    # Additional security settings
    read_only: true
    tmpfs:
      - /tmp
      - /run
    cap_drop:
      - ALL

  db:
    image: postgres:15
    restart: unless-stopped
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5
    cap_drop:
      - ALL

secrets:
  db_password:
    file: ./secrets/db_password.txt

volumes:
  postgres_data:
```

## Key Docker Best Practices Applied

1. **Multi-stage builds**: Separate build and runtime environments to reduce attack surface
2. **Non-root users**: Run containers as non-root users for security
3. **Minimal base images**: Use slim/alpine images to reduce vulnerabilities
4. **Health checks**: Built-in application health monitoring
5. **Environment variables**: Proper configuration management
6. **Secrets management**: Secure handling of sensitive data
7. **Resource limits**: Optional CPU and memory constraints for stability
8. **Production optimizations**: Optimized pip installs, bytecode caching disabled

## Scripts Available

See [DOCKER-SCRIPTS.md](references/DOCKER-SCRIPTS.md) for automated Dockerfile generation scripts.

## Security Considerations

See [SECURITY.md](references/SECURITY.md) for detailed security best practices and production hardening techniques.

## Optimization Techniques

See [OPTIMIZATION.md](references/OPTIMIZATION.md) for performance tuning and optimization strategies.

## Prerequisites and Validation

See [PREREQUISITES.md](references/PREREQUISITES.md) for system requirements, Docker installation validation, and resource allocation guidelines for AI services.