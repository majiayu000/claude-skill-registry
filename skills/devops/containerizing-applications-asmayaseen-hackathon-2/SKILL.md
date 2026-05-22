---
name: containerizing-applications
description: |
  Containerizes applications with Docker, docker-compose, and Helm charts.
  Use when creating Dockerfiles, docker-compose configurations, or Helm charts for Kubernetes.
  Includes Docker Hardened Images (95% fewer CVEs), multi-stage builds, and 15+ battle-tested gotchas.
---

# Containerizing Applications

## Quick Start

1. Run impact analysis first (env vars, network topology, auth/CORS)
2. Generate Dockerfiles using patterns below
3. Create docker-compose.yml with proper networking
4. Package as Helm chart for Kubernetes

## Dockerfile Patterns

### FastAPI/Python (Multi-stage with uv)

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.13-slim AS builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml .
RUN uv pip install --system --no-cache -r pyproject.toml

FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY . .
RUN useradd -u 1000 appuser && chown -R appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Next.js (Standalone)

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_SSO_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_SSO_URL=$NEXT_PUBLIC_SSO_URL
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

## docker-compose Pattern

```yaml
services:
  web:
    build:
      context: ./web
      args:
        # BROWSER: baked into JS bundle
        - NEXT_PUBLIC_API_URL=http://localhost:8000
    environment:
      # SERVER: read at runtime inside container
      - SERVER_API_URL=http://api:8000
    ports:
      - "3000:3000"
    depends_on:
      api:
        condition: service_healthy

  api:
    build: ./api
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - CORS_ORIGINS=http://localhost:3000,http://web:3000
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://127.0.0.1:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Helm Chart Structure

```
helm/myapp/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── ingress.yaml
```

### Chart.yaml

```yaml
apiVersion: v2
name: myapp
version: 1.0.0
appVersion: "1.0.0"
```

### values.yaml Pattern

```yaml
api:
  replicaCount: 1
  image:
    repository: myapp/api
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 8000
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
```

### Helm Commands

```bash
helm create mychart              # Create new chart
helm template . --debug          # Render templates
helm install myapp ./chart       # Install
helm upgrade myapp ./chart       # Upgrade
helm install myapp ./chart \
  --set api.image.tag=v2.0.0     # Override values
```

## Battle-Tested Gotchas (15+)

### 1. Browser vs Server URLs
**Problem:** Browser runs on host, server runs in container
```yaml
build:
  args:
    - NEXT_PUBLIC_API_URL=http://localhost:8000   # Browser
environment:
  - SERVER_API_URL=http://api:8000                # Server
```

### 2. Healthcheck IPv6 Issue
**Problem:** `wget http://localhost:3000` fails with IPv6
```yaml
healthcheck:
  test: ["CMD", "wget", "--spider", "http://127.0.0.1:3000/"]  # NOT localhost!
```

### 3. MCP Server 421 Misdirected Request
**Problem:** FastMCP rejects Docker service names
```python
transport_security = TransportSecuritySettings(
    allowed_hosts=["127.0.0.1:*", "localhost:*", "mcp-server:*", "0.0.0.0:*"]
)
```

### 4. SQLModel Tables Not Created
**Problem:** Models not imported before `create_all()`
```python
# MUST import before create_all()
from .models import User, Task, Project  # noqa: F401
SQLModel.metadata.create_all(engine)
```

### 5. Database Migration Order
**Problem:** Drizzle `db:push` drops tables not in schema
**Solution:** Start postgres → Run Drizzle → Then start API

### 6. uv Network Timeout
```dockerfile
RUN UV_HTTP_TIMEOUT=120 uv pip install --system --no-cache -r pyproject.toml
```

### 7. Missing Syntax Directive
```dockerfile
# syntax=docker/dockerfile:1    # ALWAYS first line
FROM python:3.13-slim
```

### 8. localhost in Container
Use Docker service names (api, web, sso) for server-side, NOT localhost

### 9. Auth Origins
Add Docker service names to trustedOrigins BEFORE building

### 10. Service Startup Order
Use `depends_on` with `condition: service_healthy`

### 11. Health Check Timing
Use `start_period` (e.g., 40s) for apps that take time to start

### 12. pgAdmin Email Validation
Use valid email like `admin@example.com`, not `.local` domains

### 13. Playwright in Dependencies
Keep test tools in devDependencies (300MB+ bloat)

### 14. MCP Health Check 406
Add separate `/health` endpoint via ASGI middleware

### 15. Helm Comma Parsing
Use values file instead of `--set` for comma-containing values

## Production Security

### Docker Hardened Images (Recommended)

**95% fewer CVEs** than community images. Free under Apache 2.0.

```dockerfile
# BEFORE: Community image with unknown CVEs
FROM python:3.12-slim

# AFTER: Docker Hardened Image
FROM docker.io/docker/python:3.12-dhi
```

**Five Pillars of DHI:**
| Pillar | What You Get |
|--------|--------------|
| Minimal Attack Surface | 98% CVE reduction |
| 100% Complete SBOM | SPDX/CycloneDX format |
| SLSA Build Level 3 | Verified provenance |
| OpenVEX | Machine-readable vuln status |
| Cosign Signatures | Cryptographic verification |

**Verify signatures:**
```bash
cosign verify docker.io/docker/python:3.12-dhi
```

**Read SBOM:**
```bash
docker sbom docker.io/docker/python:3.12-dhi
```

### Trivy Scanning (CI/CD)

```yaml
- name: Scan for vulnerabilities
  run: trivy image --severity HIGH,CRITICAL --exit-code 1 ${{ env.IMAGE }}
```

### Distroless Images (Alternative)

```dockerfile
# Python - use gcr.io/distroless/python3-debian12
FROM gcr.io/distroless/python3-debian12
# No shell, no package manager, runs as nonroot by default
```

### Multi-Arch Builds

```yaml
- uses: docker/build-push-action@v5
  with:
    platforms: linux/amd64,linux/arm64  # Build for both
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### BuildKit Secrets

```dockerfile
# Mount secrets during build (never stored in layers)
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) npm install
```

See [references/production-security.md](references/production-security.md) for full patterns.

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `operating-k8s-local` - Local Kubernetes with Minikube
- `deploying-cloud-k8s` - Cloud Kubernetes deployment
- `scaffolding-fastapi-dapr` - FastAPI patterns

## References

- [references/production-security.md](references/production-security.md) - Trivy, distroless, multi-arch, BuildKit secrets