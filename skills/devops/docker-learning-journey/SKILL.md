---
name: docker-learning-journey
description: |
  Interactive Docker learning guide from basics to production, tailored for Python/FastAPI developers.
  This skill should be used when users want to learn Docker concepts, understand container fundamentals,
  practice Docker commands, or progress from beginner to production-ready Docker knowledge.
---

# Docker Learning Journey

An interactive, progressive Docker learning guide designed for Python and FastAPI developers. Learn by doing with practical exercises and real-world examples.

## What This Skill Does

- Teaches Docker concepts progressively (basics → intermediate → production)
- Connects Docker concepts to Python/FastAPI knowledge you already have
- Provides hands-on exercises at each level
- Offers quick command references with explanations
- Guides containerization of FastAPI applications

## What This Skill Does NOT Do

- Cover Kubernetes (that's a separate journey)
- Handle cloud-specific deployments (AWS ECS, GCP Cloud Run)
- Replace official Docker documentation for edge cases

---

## Before Starting

Assess where you are:

| Level | You Can... | Start At |
|-------|------------|----------|
| **Beginner** | Haven't used Docker | Module 1 |
| **Basic** | Run containers, pull images | Module 2 |
| **Intermediate** | Write Dockerfiles, use compose | Module 3 |
| **Advanced** | Multi-stage builds, optimization | Module 4 |

---

## Learning Modules

### Module 1: Docker Fundamentals

**Goal**: Understand what Docker is and run your first container

**Key Concepts**:
```
Image      = Blueprint/Recipe (like a Python class)
Container  = Running instance (like a Python object)
Registry   = Image storage (like PyPI for packages)
```

**Your First Commands**:
```bash
# 1. Check Docker is installed
docker --version

# 2. Pull an image (download the blueprint)
docker pull python:3.12-slim

# 3. Run a container (create an instance)
docker run -it python:3.12-slim python
# You're now inside a Python container! Type exit() to leave

# 4. See what's running
docker ps        # Running containers
docker ps -a     # All containers (including stopped)

# 5. See downloaded images
docker images
```

**Python Analogy**:
```python
# This is like Docker:
class PythonEnvironment:        # Image
    def __init__(self):
        self.python = "3.12"
        self.packages = []

env1 = PythonEnvironment()      # Container 1
env2 = PythonEnvironment()      # Container 2 (isolated!)
```

**Exercise**: See `assets/exercises/01-first-container.md`

---

### Module 2: Building Images with Dockerfile

**Goal**: Create your own images with Dockerfile

**Key Concept**: Dockerfile = Recipe with steps

```dockerfile
# Every Dockerfile starts with a base image
FROM python:3.12-slim

# Set working directory (like cd)
WORKDIR /app

# Copy files from your computer into the image
COPY requirements.txt .

# Run commands (install dependencies)
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Default command when container starts
CMD ["python", "main.py"]
```

**Layer Concept** (Important!):
```
┌─────────────────────────┐
│ CMD ["python", "main.py"] │  ← Layer 5 (your command)
├─────────────────────────┤
│ COPY . .                  │  ← Layer 4 (your code)
├─────────────────────────┤
│ RUN pip install...        │  ← Layer 3 (dependencies)
├─────────────────────────┤
│ COPY requirements.txt     │  ← Layer 2 (requirements file)
├─────────────────────────┤
│ FROM python:3.12-slim     │  ← Layer 1 (base image)
└─────────────────────────┘

Each layer is CACHED! Change order matters for speed.
```

**Build Commands**:
```bash
# Build an image from Dockerfile
docker build -t myapp:v1 .

# -t = tag (name:version)
# .  = build context (current directory)

# Run your new image
docker run myapp:v1
```

**Exercise**: See `assets/exercises/02-first-dockerfile.md`

---

### Module 3: Docker Compose (Multi-Container Apps)

**Goal**: Run multiple containers together (FastAPI + Database)

**Key Concept**: Compose = Orchestra conductor for containers

```yaml
# docker-compose.yml
services:
  api:                          # Your FastAPI app
    build: .
    ports:
      - "8000:8000"             # host:container
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db

  db:                           # PostgreSQL database
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:                # Persist data between restarts
```

**Compose Commands**:
```bash
# Start all services
docker compose up

# Start in background (detached)
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f api

# Rebuild after code changes
docker compose up --build
```

**Exercise**: See `assets/exercises/03-compose-fastapi.md`

---

### Module 4: Production Patterns

**Goal**: Build optimized, secure, production-ready images

**Multi-Stage Builds** (The Key Technique):
```dockerfile
# Stage 1: Builder (temporary, has build tools)
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

# Stage 2: Runtime (final, minimal)
FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY ./app ./app
ENV PATH="/app/.venv/bin:$PATH"
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

**Why Multi-Stage?**
```
Builder Stage: 400MB (has uv, build tools)
         ↓
    Copies only .venv
         ↓
Runtime Stage: 150MB (minimal, secure)
```

**Production Checklist**:
- [ ] Multi-stage build (small image)
- [ ] Non-root user (security)
- [ ] Health check (monitoring)
- [ ] .dockerignore (exclude unnecessary files)
- [ ] No secrets in image (use env vars)

**Exercise**: See `assets/exercises/04-production-build.md`

---

## Quick Reference

### Essential Commands

| Task | Command |
|------|---------|
| Pull image | `docker pull image:tag` |
| Run container | `docker run -d -p 8000:80 image` |
| List running | `docker ps` |
| List all | `docker ps -a` |
| Stop container | `docker stop <id>` |
| Remove container | `docker rm <id>` |
| List images | `docker images` |
| Build image | `docker build -t name:tag .` |
| Remove image | `docker rmi image:tag` |
| View logs | `docker logs <id>` |
| Shell into | `docker exec -it <id> /bin/bash` |

### Compose Commands

| Task | Command |
|------|---------|
| Start services | `docker compose up` |
| Start detached | `docker compose up -d` |
| Stop services | `docker compose down` |
| Rebuild | `docker compose up --build` |
| View logs | `docker compose logs -f` |
| Run command | `docker compose exec api bash` |

### Port Mapping Explained

```
-p 8000:80
   │    │
   │    └── Container port (inside)
   └─────── Host port (your computer)

Access at: http://localhost:8000
```

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "port already in use" | Another process on that port | Change host port or stop other process |
| "image not found" | Typo or not pulled | `docker pull image:tag` |
| "permission denied" | Docker daemon not running | Start Docker Desktop |
| "no space left" | Docker cache full | `docker system prune` |
| "connection refused" | Container not ready | Add health check, use `depends_on` |

---

## Python Developer's Mental Model

| Python | Docker |
|--------|--------|
| `pip install` | `docker pull` |
| `requirements.txt` | Dockerfile's `RUN pip install` |
| `venv` | Container isolation |
| `python main.py` | `docker run` |
| `pip freeze` | `docker images` |
| Multiple projects | Multiple containers |
| `.gitignore` | `.dockerignore` |

---

## Learning Path Checklist

### Week 1: Foundations
- [ ] Install Docker Desktop
- [ ] Run `hello-world` container
- [ ] Pull and run Python image
- [ ] Understand images vs containers
- [ ] Complete Exercise 01

### Week 2: Building
- [ ] Write first Dockerfile
- [ ] Build custom image
- [ ] Understand layers and caching
- [ ] Complete Exercise 02

### Week 3: Composing
- [ ] Write docker-compose.yml
- [ ] Run FastAPI + PostgreSQL
- [ ] Understand volumes and networks
- [ ] Complete Exercise 03

### Week 4: Production
- [ ] Multi-stage Dockerfile
- [ ] Optimize image size
- [ ] Add security practices
- [ ] Complete Exercise 04

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/01-core-concepts.md` | Deep dive into Docker architecture |
| `references/02-dockerfile-reference.md` | All Dockerfile instructions |
| `references/03-compose-reference.md` | Docker Compose file format |
| `references/04-fastapi-docker.md` | FastAPI-specific patterns |
| `references/05-troubleshooting.md` | Common issues and fixes |

## Exercises

| Exercise | Level | Goal |
|----------|-------|------|
| `assets/exercises/01-first-container.md` | Beginner | Run Python in container |
| `assets/exercises/02-first-dockerfile.md` | Beginner | Build custom image |
| `assets/exercises/03-compose-fastapi.md` | Intermediate | Full stack app |
| `assets/exercises/04-production-build.md` | Advanced | Optimized deployment |

## Cheatsheets

| File | Contents |
|------|----------|
| `assets/cheatsheets/commands.md` | All Docker commands |
| `assets/cheatsheets/dockerfile.md` | Dockerfile syntax |
| `assets/cheatsheets/compose.md` | Compose file syntax |
