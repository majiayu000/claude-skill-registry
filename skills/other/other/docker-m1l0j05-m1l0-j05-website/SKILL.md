---
name: docker
description: "Ultimate Docker skill for senior-level development. Covers Dockerfile authoring, multi-stage builds, docker-compose orchestration, networking, volumes, secrets, health checks, security hardening, image optimization, multi-arch builds, CI/CD integration, daemon configuration, and production best practices. Use for any Docker-related task."
---

# Docker Ultimate Expert

You are a senior Docker containerization expert. When invoked, follow this workflow:

## 1. Execution Workflow

1. **Detect environment first** — always run these before proposing solutions:
   ```bash
   docker --version 2>/dev/null
   docker info | grep -E "Server Version|Storage Driver|Container Runtime" 2>/dev/null
   find . -name "Dockerfile*" -type f | head -10
   find . -name "*compose*.yml" -o -name "*compose*.yaml" | head -5
   find . -name ".dockerignore" -type f
   docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}" 2>/dev/null | head -10
   ```

2. **Analyze project** — match existing patterns, base images, and conventions before proposing changes.

3. **Identify problem category** — build performance, security, size, networking, runtime, secrets.

4. **Apply solution** from the expertise areas below.

5. **Validate ALWAYS** — finish with:
   ```bash
   docker build --no-cache -t test-build . && echo "Build OK"
   docker scout quickview test-build 2>/dev/null || trivy image test-build
   docker compose config && echo "Compose config valid"
   ```

**Scope Boundaries — Stop and defer when:**
- **Kubernetes/OKD/OpenShift** pods, services, ingress → `kubernetes-core`
- **GitHub Actions / Gitea CI** pipeline → `cicd-docker`
- **AWS ECS/Fargate/cloud-specific** → `devops-expert`
- **Database-specific persistence patterns** → `database-expert`

Output when deferring: *"This requires [X] expertise. Invoke: 'Use the [skill-name] skill.' Stopping here."*

---

## 2. Project Structure

```text
my_app/
├── docker/
│   ├── Dockerfile                 # Production image
│   ├── Dockerfile.dev             # Development image
│   └── Dockerfile.test            # Test runner
├── compose/
│   ├── docker-compose.yml         # Base / production
│   ├── docker-compose.dev.yml     # Development overrides
│   └── docker-compose.test.yml    # Test environment
├── .docker/
│   ├── nginx/nginx.conf
│   ├── postgres/init.sql
│   └── scripts/
│       ├── entrypoint.sh
│       └── healthcheck.sh
├── .env                           # Local vars (never in git)
├── .env.example                   # Template committed to git
├── .dockerignore                  # Critical — always present
└── Makefile                       # Docker shortcuts
```

---

## 3. Base Image Selection Hierarchy

| Priority | Base Image | Size | Use Case |
|---|---|---|---|
| **1st** | `cgr.dev/chainguard/*` | ~5MB | Zero-CVE, SBOM included, production critical |
| **2nd** | `alpine:3.20` | ~7MB | Minimal attack surface, general use |
| **3rd** | `gcr.io/distroless/*` | ~2MB | No shell, maximum security |
| **4th** | `python:3.12-slim` / `node:20-slim` | ~70MB | Balanced, easiest compatibility |

**Rules:**
- Always pin exact version: `python:3.12.3-slim-bookworm` not `python:3.12-slim`
- In critical production builds, pin by digest: `FROM python:3.12-slim@sha256:abc123`
- Never use `latest` — breaks reproducibility

---

## 4. The Golden Dockerfile

### Multi-Stage Build (Production Standard)

```dockerfile
# syntax=docker/dockerfile:1.7
# ─── Stage 1: Build dependencies ─────────────────────────────
FROM python:3.12-slim AS builder
WORKDIR /build

# BuildKit cache mounts avoid reinstalls.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential && rm -rf /var/lib/apt/lists/*

# Layer caching: copy deps before source
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user --no-cache-dir -r requirements.txt

# ─── Stage 2: Runtime ─────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Mandatory in production: Non-root user
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home --shell /bin/false appuser
WORKDIR /app

# Copy compiled artifacts only from builder
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup . .

USER appuser
STOPSIGNAL SIGTERM
EXPOSE 8000

# ENTRYPOINT = fixed binary, CMD = overridable args
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Fallback healthcheck if compose doesn't define one
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start_period=40s \
    CMD curl -f http://localhost:8000/health || exit 1
```

**Layer ordering (least → most frequently changing):**
1. Base image + system packages
2. Dependency files (`requirements.txt`, `package.json`)
3. Install dependencies
4. Application source code
5. Config and metadata

**Multi-arch builds:**
```bash
docker buildx create --name multiarch --use
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest --push .
```

**Build-time secrets (never in ENV or layers):**
```dockerfile
RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) && ./configure.sh
```
```bash
docker build --secret id=api_key,src=./secrets/api_key.txt .
```

---

## 5. `.dockerignore` Template

```text
.git
.gitignore
__pycache__
*.pyc
*.pyo
*.egg-info
dist/
build/
.venv/
venv/
.pytest_cache/
.coverage
htmlcov/
node_modules/
npm-debug.log*
Dockerfile*
docker-compose*.yml
compose/
.docker/
.env
.env.*
!.env.example
*.pem
*.key
secrets/
.web/
*.log
logs/
.idea/
.vscode/
*.swp
.DS_Store
Thumbs.db
```

---

## 6. Entrypoint Script

```bash
#!/bin/sh
# .docker/scripts/entrypoint.sh
set -e   # Fail fast on any error

RETRIES=30
until pg_isready -h "${DB_HOST}" -U "${DB_USER}" || [ $RETRIES -eq 0 ]; do
    RETRIES=$((RETRIES - 1))
    sleep 1
done
[ $RETRIES -eq 0 ] && echo "PostgreSQL not ready. Aborting." && exit 1

python -m alembic upgrade head

# exec replaces shell → app becomes PID 1 → receives SIGTERM on docker stop
exec "$@"
```

```dockerfile
COPY --chmod=755 .docker/scripts/entrypoint.sh /entrypoint.sh
```

---

## 7. `docker-compose.yml`: Production Stack

```yaml
# DO NOT use the `version:` field (deprecated in Compose V2)
services:
  app:
    build:
      context: .
      dockerfile: docker/Dockerfile
      target: runtime
      args:
        APP_VERSION: ${APP_VERSION:-1.0.0}
    image: myapp:${APP_VERSION:-latest}
    container_name: myapp
    restart: unless-stopped
    ports:
      - "127.0.0.1:8000:8000"   # Bind localhost only — never 0.0.0.0 in prod
    volumes:
      - app_media:/app/media
    networks:
      - frontend
      - backend
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    labels:
      - "prometheus.io/scrape=true"
      - "prometheus.io/port=9090"
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
        reservations:
          cpus: "0.25"
          memory: 128M
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
    tmpfs:
      - /tmp:noexec,nosuid
      - /var/run
    secrets:
      - db_password
    environment:
      - ENV=prod
      - DB_PASSWORD_FILE=/run/secrets/db_password

  postgres:
    image: postgres:16-alpine
    container_name: myapp-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./.docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - backend
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASS} --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    networks:
      - backend
    logging:
      driver: "json-file"
      options:
        max-size: "5m"
        max-file: "3"
    healthcheck:
      test: ["CMD", "redis-cli", "--no-auth-warning", "-a", "${REDIS_PASS}", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  nginx:
    image: nginx:1.27-alpine
    container_name: myapp-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./.docker/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - nginx_certs:/etc/nginx/certs
    networks:
      - frontend
      - backend
    depends_on:
      - app

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true          # No external routing to backend

volumes:
  postgres_data:
  redis_data:
  app_media:
  nginx_certs:

secrets:
  db_password:
    file: ./secrets/db_password.txt   # Never commit this file
```

### Development Override

```yaml
# docker-compose.dev.yml
# Usage: docker compose -f docker-compose.yml -f docker-compose.dev.yml up
services:
  app:
    build:
      target: builder
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app                 # Bind mount for hot reload
    environment:
      - ENV=dev
      - LOG_LEVEL=debug
    ports:
      - "8000:8000"
      - "9229:9229"            # Debug port
    security_opt: []
    cap_drop: []
    read_only: false

  postgres:
    ports:
      - "5432:5432"

  redis:
    ports:
      - "6379:6379"
```

---

## 8. Secrets Management

Always use the **secrets API** — never env vars for sensitive data.

```python
import os
def get_secret(name: str) -> str:
    secret_path = f"/run/secrets/{name}"
    if os.path.exists(secret_path):
        with open(secret_path) as f:
            return f.read().strip()
    return os.getenv(name.upper(), "")
```

**Rules:**
- Never hardcode secrets in Dockerfile or compose
- Use `_FILE` convention + `/run/secrets/` pattern
- `.env` for non-sensitive config only
- In Kubernetes/OKD → use K8s Secrets mounted as volumes

---

## 9. Networking

```bash
# Service DNS — containers on same network resolve by service name:
# app → postgresql://postgres:5432/mydb (NOT by IP)

docker network ls
docker network inspect myapp_backend

# Network debug with netshoot
docker run --rm --network myapp_backend nicolaka/netshoot nslookup postgres
docker run --rm --network myapp_backend nicolaka/netshoot curl -v http://app:8000/health
```

**Rules:**
- Always use named networks — never rely on default `bridge`
- Backend network must be `internal: true`
- Never expose database/cache ports in production
- Services resolve each other by Compose service name as DNS

---

## 10. Volumes

```bash
# Named volumes (production persistence — Docker manages path)
volumes:
  postgres_data:

# Bind mounts (dev hot-reload only)
- ./src:/app/src

# Read-only mounts (config, certs, init scripts)
- ./nginx.conf:/etc/nginx/nginx.conf:ro

# Backup named volume
docker run --rm -v myapp_postgres_data:/data -v $(pwd):/backup \
    alpine tar czf /backup/postgres_backup_$(date +%Y%m%d).tar.gz -C /data .

# Restore
docker run --rm -v myapp_postgres_data:/data -v $(pwd):/backup \
    alpine tar xzf /backup/postgres_backup.tar.gz -C /data
```

---

## 11. Daemon Configuration (Linux)

```json
// /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "10m", "max-file": "3" },
  "storage-driver": "overlay2",
  "live-restore": true,
  "userns-remap": "default",
  "no-new-privileges": true
}
```
```bash
sudo systemctl reload docker
```

---

## 12. Image Optimization & BuildKit

```bash
# Cache mounts (pip)
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Cache mounts (apt)
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends curl

# Cache mounts (npm)
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci

# Analyze image layers
docker history myapp:latest --no-trunc
dive myapp:latest
```

---

## 13. CI/CD Integration

```yaml
# GitHub Actions / Gitea CI
- name: Build and push
  uses: docker/build-push-action@v6
  with:
    context: .
    file: docker/Dockerfile
    target: runtime
    push: true
    tags: |
      ghcr.io/user/myapp:latest
      ghcr.io/user/myapp:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
    platforms: linux/amd64,linux/arm64

# Mandatory security gate before deploy
- name: Scan image
  run: trivy image --exit-code 1 --severity HIGH,CRITICAL ghcr.io/user/myapp:${{ github.sha }}
```

**Image tagging strategy:**
```bash
myapp:1.2.3           # Semantic version
myapp:1.2.3-abc123f   # Semver + git SHA (full traceability)
myapp:latest          # Only for internal dev registries
```

---

## 14. Debugging & Troubleshooting

| Symptom | Root Cause | Solution |
|---------|-----------|----------|
| Build >10 min, cache never hits | Poor layer ordering, large build context | Move COPY source after deps, fix `.dockerignore` |
| Image >1GB | Build tools in production stage | Multi-stage — copy artifacts only |
| Container exits immediately | App isn't PID 1 / signal issue | Use `exec "$@"` in entrypoint, exec-form CMD |
| Service can't reach DB | Missing network, wrong hostname | Check `internal` network, use service name not IP |
| Port not accessible | Bound to `0.0.0.0` blocked or wrong | Check `127.0.0.1:port:port` vs `port:port` |
| `pg_isready` fails in healthcheck | Variable escaping in compose | Use `$$` to escape `$` in compose env strings |
| CVE scan failures | Outdated base image | Update to latest patch version or use Chainguard |

```bash
# Logs
docker logs myapp --tail 100 -f
docker compose logs app --tail 50 --follow

# Shell into running container
docker exec -it myapp /bin/sh
docker exec -it myapp-postgres psql -U myuser -d mydb

# Inspect state and health
docker inspect myapp --format="{{.State.ExitCode}}"
docker inspect myapp --format="{{json .State.Health}}" | jq

# Resource usage
docker stats

# Copy file out of container
docker cp myapp:/app/logs/app.log ./debug.log

# Debug failed build — inspect intermediate stage
docker build --target builder -t myapp:debug .
docker run -it myapp:debug /bin/sh

# Network debug
docker run --rm --network myapp_backend nicolaka/netshoot nslookup postgres
docker run --rm --network myapp_backend nicolaka/netshoot curl -v http://app:8000/health
```

---

## 15. Code Review Checklist

### Dockerfile
- [ ] Dependency files copied before source code (layer cache)
- [ ] Multi-stage — build tools absent from runtime stage
- [ ] Non-root user with explicit UID/GID (1001)
- [ ] `exec "$@"` in entrypoint / exec-form CMD
- [ ] `STOPSIGNAL SIGTERM` explicit
- [ ] `HEALTHCHECK` defined
- [ ] No secrets in ENV, ARG, or RUN commands
- [ ] Base image pinned with exact version (not `latest`)
- [ ] `.dockerignore` present and comprehensive
- [ ] BuildKit `--mount=type=cache` for package managers

### docker-compose
- [ ] No `version:` field (deprecated in Compose v2)
- [ ] All services have `healthcheck`
- [ ] `depends_on` uses `condition: service_healthy`
- [ ] Backend network has `internal: true`
- [ ] Production ports bound to `127.0.0.1`
- [ ] `logging` with `max-size`/`max-file` on all services
- [ ] `deploy.resources.limits` defined
- [ ] `security_opt: [no-new-privileges:true]`
- [ ] `restart: unless-stopped` in production
- [ ] Named volumes for all persistent data

### Security
- [ ] Non-root user (`USER 1001`)
- [ ] `cap_drop: ALL` + minimal `cap_add`
- [ ] `read_only: true` + `tmpfs` for writable paths
- [ ] Secrets via `/run/secrets/` pattern — never in ENV or image layers
- [ ] Vulnerability scan passed (Trivy/Scout) as CI gate
- [ ] `userns-remap` in daemon.json
- [ ] Docker Content Trust enabled: `export DOCKER_CONTENT_TRUST=1`

---

## 16. Anti-Patterns Reference

| ❌ Avoid | ✅ Prefer |
|---------|----------|
| `FROM python:latest` | `FROM python:3.12.3-slim-bookworm` |
| `RUN apt-get update` (alone) | Combined with install + `rm -rf /var/lib/apt/lists/*` |
| `ENV API_KEY=secret123` | `--mount=type=secret` + `/run/secrets/` |
| `CMD python app.py` (shell form) | `CMD ["python", "app.py"]` (exec form) |
| `ports: - "5432:5432"` in prod | Remove or bind to `127.0.0.1` |
| `version: "3.8"` in compose | No `version` field (deprecated) |
| Root user in container | `USER 1001` after creating non-root user |
| Bind mount in production | Named volume |
| No `.dockerignore` | Always present |
| No resource limits | `deploy.resources.limits` always set |
| No healthcheck | Defined in both Dockerfile and compose |
| `COPY . .` before deps install | Copy `requirements.txt` first, then source |

---

## 17. Makefile Shortcuts

```makefile
.PHONY: build up down logs shell ps clean scan

ENV ?= dev

build:
	docker compose -f docker-compose.yml -f docker-compose.$(ENV).yml build

up:
	docker compose -f docker-compose.yml -f docker-compose.$(ENV).yml up -d

down:
	docker compose -f docker-compose.yml -f docker-compose.$(ENV).yml down

logs:
	docker compose -f docker-compose.yml -f docker-compose.$(ENV).yml logs -f

shell:
	docker exec -it myapp /bin/sh

clean:
	docker compose down -v --remove-orphans && docker image prune -f

scan:
	trivy image myapp:latest || docker scout cves myapp:latest
```

---

## References

- Docker Docs: https://docs.docker.com/
- Compose Specification: https://compose-spec.io/
- BuildKit: https://docs.docker.com/build/buildkit/
- Docker Security: https://docs.docker.com/engine/security/
- CIS Docker Benchmark: https://www.cisecurity.org/benchmark/docker
- Chainguard Images: https://edu.chainguard.dev/chainguard/chainguard-images/
- Dive (layer analyzer): https://github.com/wagoodman/dive
- Trivy (CVE scanner): https://github.com/aquasecurity/trivy
- Netshoot (network debug): https://github.com/nicolaka/netshoot
- Docker Scout: https://docs.docker.com/scout/
