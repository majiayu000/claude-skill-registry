---
name: docker-deployment
description: Docker, docker-compose, and deployment configuration best practices. Use when writing Dockerfiles, docker-compose.yml, CI/CD configs, or setting up any containerized deployment.
---

# Docker Deployment Patterns

## Production Dockerfile (Python)
```dockerfile
FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

FROM base AS builder
RUN pip install --no-cache-dir uv
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

FROM base AS runtime
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
RUN useradd -m appuser && chown -R appuser /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

## docker-compose.yml (Development)
```yaml
services:
  app:
    build: .
    ports: ["8000:8000"]
    volumes: ["./:/app"]  # hot reload in dev
    env_file: [.env]
    depends_on:
      db: { condition: service_healthy }
      redis: { condition: service_healthy }
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes: [postgres_data:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s

volumes:
  postgres_data:
```

## .env.example (Always provide this)
```bash
# Database
DB_HOST=db
DB_PORT=5432
DB_NAME=myapp
DB_USER=myapp
DB_PASSWORD=changeme_in_production

# Redis
REDIS_URL=redis://redis:6379/0

# App
SECRET_KEY=changeme_in_production
DEBUG=false
ALLOWED_ORIGINS=http://localhost:3000
```

## Makefile
```makefile
.PHONY: dev build test migrate

dev:
	docker-compose up --build

build:
	docker-compose build

test:
	docker-compose run --rm app pytest

migrate:
	docker-compose run --rm app alembic upgrade head

shell:
	docker-compose exec app bash
```

## Rules
- Multi-stage builds: keep final image small (no build tools)
- Never run as root — create appuser
- Health checks on ALL services
- Never hardcode secrets — always env vars
- .env.example with ALL required vars (no values)
- Volumes for persistent data (DB, uploads)
- Separate docker-compose.override.yml for dev overrides
- Pin image versions (postgres:16, not postgres:latest)
