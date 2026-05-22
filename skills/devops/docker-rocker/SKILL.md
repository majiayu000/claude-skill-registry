---
name: docker-rocker
description: |
  Production-grade Docker containerization for FastAPI, Pytest, SQLModel, and Pydantic projects.
  This skill should be used when users ask to dockerize FastAPI applications, create multi-stage
  Docker builds, optimize Docker images for Python APIs, set up CI/CD Docker pipelines, or
  deploy containerized Python web APIs with maximum performance and minimal image size.
---

# Docker Rocker

Production-grade Docker automation for Python FastAPI web API projects using multi-stage builds, UV package manager, and performance optimization strategies.

## What This Skill Does

- Creates optimized multi-stage Dockerfiles (Builder → Runtime → Testing stages)
- Configures UV package manager for 50-70% faster dependency installation
- Implements layer caching strategies for rapid rebuilds
- Sets up non-root user security configurations
- Generates docker-compose files for development and production
- Optimizes for SQLModel/Neon database connections in containers
- Configures Pydantic settings for container environments

## What This Skill Does NOT Do

- Manage Kubernetes deployments (use dedicated k8s skills)
- Handle cloud-specific container registries (AWS ECR, GCR, ACR)
- Configure reverse proxies (Nginx, Traefik)
- Manage container orchestration at scale
- Handle secrets management beyond environment variables

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Project structure, existing Dockerfile, pyproject.toml/requirements.txt, app entry point |
| **Conversation** | Target deployment (dev/staging/prod), database connection requirements, special dependencies |
| **Skill References** | Multi-stage patterns from `references/`, optimization strategies, security practices |
| **User Guidelines** | Team Docker conventions, registry requirements, CI/CD integration needs |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Required Clarifications

Ask about USER's context before generating Dockerfiles:

| Question | Purpose |
|----------|---------|
| **Deployment target?** | Dev (hot-reload) vs Production (optimized) vs CI/CD (testing) |
| **Package manager?** | UV (recommended) vs pip vs Poetry |
| **Database type?** | Neon PostgreSQL, local PostgreSQL, SQLite, other |
| **Special system deps?** | Libraries requiring apt packages (Pillow, psycopg2, etc.) |
| **Port configuration?** | Default 80 or custom port |

---

## Docker Deployment Stages

### Stage Overview

| Stage | Purpose | Base Image | Final Size |
|-------|---------|------------|------------|
| **Builder** | Install dependencies, compile packages | python:3.12-slim | ~400MB (discarded) |
| **Runtime** | Production application | python:3.12-slim | ~150MB |
| **Testing** | CI/CD test execution | extends Builder | ~450MB |
| **Development** | Hot-reload for local dev | python:3.12-slim | ~300MB |

### Stage Selection Logic

```
What is the deployment target?

Production deployment?
  → Use Builder + Runtime stages
  → Minimal image, no dev dependencies

CI/CD pipeline?
  → Use Builder + Testing stage
  → Include pytest, dev dependencies

Local development?
  → Use Development stage
  → Volume mounts, hot-reload enabled

All of the above?
  → Generate complete multi-stage Dockerfile with all targets
```

---

## Workflow

### 1. Analyze Project Structure

```bash
# Check for existing configurations
ls -la pyproject.toml uv.lock requirements*.txt Dockerfile docker-compose.yml
```

Identify:
- Package manager (UV if uv.lock exists, Poetry if poetry.lock, pip otherwise)
- Entry point (app/main.py, src/main.py, main.py)
- Dependencies requiring system packages

### 2. Select Dockerfile Template

Based on user's deployment target, use appropriate template from `assets/templates/`:

| Target | Template |
|--------|----------|
| Production only | `Dockerfile.production` |
| With testing | `Dockerfile.complete` |
| Development | `Dockerfile.dev` |
| Full multi-stage | `Dockerfile.multistage` |

### 3. Configure Environment Variables

```dockerfile
# Performance optimizations
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Application settings
ENV APP_MODULE=app.main:app \
    PORT=80
```

### 4. Optimize Layer Caching

Order Dockerfile instructions by change frequency:
1. Base image (rarely changes)
2. System dependencies (rarely changes)
3. Python dependencies (changes occasionally)
4. Application code (changes frequently)

### 5. Configure Database Connections

For Neon/PostgreSQL in containers:

```python
# Use NullPool - let external pooler handle connections
from sqlalchemy.pool import NullPool

engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
    pool_pre_ping=True,
)
```

### 6. Generate docker-compose

Create appropriate compose file for target environment.

### 7. Validate Build

```bash
# Build and verify
docker build --target runtime -t app:latest .
docker run --rm app:latest python -c "import app; print('OK')"
```

---

## Quick Commands

| Task | Command |
|------|---------|
| Build production image | `docker build --target runtime -t app:prod .` |
| Build test image | `docker build --target testing -t app:test .` |
| Run tests in container | `docker run --rm app:test pytest -v` |
| Build with no cache | `docker build --no-cache -t app:latest .` |
| Check image size | `docker images app:latest` |
| Scan for vulnerabilities | `docker scout cves app:latest` |

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `uv: command not found` | UV not installed in image | Add `COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv` |
| `ModuleNotFoundError` | Dependencies not in runtime | Verify COPY of .venv from builder |
| `Permission denied` | Non-root user can't write | Use `--chown=app:app` on COPY |
| `Connection refused` to DB | Network isolation | Use docker-compose networks or host.docker.internal |
| `OOM killed` | Container memory limit | Increase memory limit or optimize workers |
| Build cache not working | Layer order wrong | Reorder: deps before code |

---

## Output Checklist

Before delivering Dockerfile, verify:

- [ ] Multi-stage build separates builder and runtime
- [ ] UV cache mounts configured for fast rebuilds
- [ ] `UV_COMPILE_BYTECODE=1` set for startup speed
- [ ] Non-root user created and used
- [ ] `.dockerignore` includes .venv, __pycache__, .git
- [ ] Layer order optimized (deps before code)
- [ ] Health check configured
- [ ] `--proxy-headers` flag for FastAPI behind load balancer
- [ ] Database connection uses NullPool for external pooling
- [ ] Secrets not hardcoded (use environment variables)

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/multi-stage-builds.md` | Understanding stage architecture and patterns |
| `references/optimization-strategies.md` | Reducing image size and build time |
| `references/fastapi-patterns.md` | FastAPI-specific Docker configurations |
| `references/security-best-practices.md` | Container security hardening |
| `references/database-connections.md` | SQLModel/Neon connection patterns in containers |

## Asset Templates

| Template | Use Case |
|----------|----------|
| `assets/templates/Dockerfile.multistage` | Complete multi-stage (Builder + Runtime + Testing) |
| `assets/templates/Dockerfile.production` | Production-only optimized build |
| `assets/templates/Dockerfile.dev` | Development with hot-reload |
| `assets/templates/docker-compose.yml` | Full development stack |
| `assets/templates/docker-compose.prod.yml` | Production compose |
| `assets/templates/.dockerignore` | Standard ignore patterns |
