---
name: containerize-apps
description: Containerizes applications with impact-aware Dockerfiles and docker-compose configurations. This skill should be used when containerizing projects for Docker, creating Dockerfiles, docker-compose files, or preparing applications for Kubernetes deployment. It performs impact analysis first (env vars, network topology, auth/CORS), then generates properly configured container configs. Invokes the impact-analyzer subagent for comprehensive project scanning.
---

# Containerize Apps

## Overview

This skill containerizes applications with **impact analysis first**, ensuring Docker configs work correctly with authentication, networking, and environment configuration. It generates Dockerfiles, docker-compose files, and documents required changes.

## Workflow

```
1. Impact Analysis    → Scan project for containerization requirements
2. Blueprint Selection → Choose appropriate Dockerfile patterns
3. Configuration Gen   → Generate Dockerfiles + docker-compose
4. Impact Documentation → Document required code/config changes
5. Optional: Gordon    → Validate with Docker AI (if available)
```

---

## Step 1: Impact Analysis (REQUIRED)

Before generating ANY container configuration, invoke the impact-analyzer subagent:

```
Use Task tool with:
  subagent_type: "impact-analyzer"
  prompt: |
    Analyze this project for containerization requirements.

    Scan for:
    1. Environment variables (build-time vs runtime)
    2. Localhost/127.0.0.1 references that need Docker service names
    3. Auth/CORS configurations (Better Auth trustedOrigins, FastAPI CORS)
    4. Service dependencies and startup order
    5. Ports used by each service

    Return structured findings for containerization.
```

**Wait for the analysis report before proceeding.**

The report will identify:
- Environment variables needing configuration
- URLs that must change for container networking
- Auth configs requiring origin updates
- Service dependency graph

---

## Step 2: Blueprint Selection

Based on project analysis, select appropriate blueprints from `assets/`:

| Project Type | Blueprint | Key Considerations |
|--------------|-----------|-------------------|
| FastAPI/Python | `Dockerfile.fastapi` | uv, multi-stage, non-root |
| Next.js | `Dockerfile.nextjs` | standalone output, NEXT_PUBLIC_* |
| Python Service | `Dockerfile.python` | Generic Python app |
| MCP Server | `Dockerfile.mcp` | Based on Python service |

---

## Step 3: Generate Configurations

### 3.1 Dockerfiles

For each service, generate Dockerfile using blueprint + impact analysis:

**Customization points:**
```dockerfile
# From impact analysis - replace these:
CMD ["uvicorn", "{{MODULE_PATH}}:app", ...]  # Module path from project
EXPOSE {{PORT}}                               # Port from analysis
ENV {{ENV_VARS}}                              # Runtime env vars
ARG {{BUILD_ARGS}}                            # Build-time vars (NEXT_PUBLIC_*)
```

### 3.2 docker-compose.yml

Generate compose file with proper networking:

```yaml
# Network topology from impact analysis
services:
  web:
    build:
      context: ./web-dashboard
      args:
        # BROWSER: baked into JS bundle, runs on user's machine
        - NEXT_PUBLIC_API_URL=http://localhost:8000
        - NEXT_PUBLIC_SSO_URL=http://localhost:3001
    environment:
      - NODE_ENV=production
      # SERVER: read at runtime, runs inside container
      - SERVER_API_URL=http://api:8000
      - SERVER_SSO_URL=http://sso-platform:3001
    ports:
      - "3000:3000"
    depends_on:
      api:
        condition: service_healthy

  api:
    build:
      context: ./packages/api
    environment:
      - DATABASE_URL=${DATABASE_URL}              # From .env (external Neon)
      - FRONTEND_URL=http://web:3000              # Docker service name!
      - CORS_ORIGINS=http://localhost:3000,http://web:3000
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Add other services based on analysis...
```

### 3.3 .env.docker Template

Generate environment template for Docker:

```bash
# External services (keep actual values)
DATABASE_URL=postgresql://...@neon.tech/...

# Docker networking (use service names)
API_URL=http://api:8000
SSO_URL=http://sso:3001
FRONTEND_URL=http://web:3000

# Secrets (in production, use Docker secrets or K8s secrets)
BETTER_AUTH_SECRET=your-secret-here
```

---

## Step 4: Document Required Changes

Generate a `CONTAINERIZATION.md` documenting what needs to change in the codebase:

```markdown
# Containerization Impact Report

## Required Code Changes

### 1. Auth Configuration (sso-platform/src/lib/auth.ts)
Add Docker service names to trustedOrigins:
```typescript
trustedOrigins: [
  "http://localhost:3000",
  "http://localhost:8000",
  "http://web:3000",      // ADD: Docker frontend
  "http://api:8000",      // ADD: Docker backend
]
```

### 2. Backend CORS (packages/api/src/main.py)
Update CORS origins:
```python
origins = [
    "http://localhost:3000",
    "http://web:3000",    # ADD: Docker frontend
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
]
```

### 3. Environment Variables
- `DATABASE_URL`: Keep as-is (external Neon)
- `NEXT_PUBLIC_API_URL`: Must be build ARG, set to http://api:8000
- `BETTER_AUTH_URL`: Runtime ENV, set to http://sso:3001
```

---

## Step 5: Optional Gordon Validation

If Docker Desktop with Gordon is available, suggest validation:

```bash
# Validate Dockerfile
cat packages/api/Dockerfile | docker ai "Rate this Dockerfile for production use"

# Or use Docker Desktop UI
# Click ✨ icon → "Review my Dockerfile"
```

**Note:** Gordon CLI can't read files directly. Use piping or Desktop UI.

---

## Blueprint Reference

### FastAPI Pattern

See `assets/Dockerfile.fastapi` for:
- Multi-stage build with uv
- Non-root user (uid 1000)
- Health check endpoint
- Python path configuration

**Customize:**
- `CMD` module path (e.g., `taskflow_api.main:app`)
- `EXPOSE` port
- Additional ENV vars

### Next.js Pattern

See `assets/Dockerfile.nextjs` for:
- Multi-stage build (deps → builder → runner)
- Standalone output mode
- Build-time ARGs for NEXT_PUBLIC_*
- Non-root user (uid 1001)

**Customize:**
- Build ARGs for environment
- Port if not 3000

### docker-compose Pattern

See `assets/docker-compose.template.yml` for:
- Service definitions with health checks
- Network topology comments
- depends_on with conditions
- Environment variable patterns

---

## Common Gotchas (Battle-Tested)

### 0. Missing Syntax Directive
**Problem:** Dockerfile may not use latest features or build checks
**Solution:** Always add `# syntax=docker/dockerfile:1` as the **first line**:
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.13-slim
...
```
This ensures:
- Latest stable Dockerfile features (build checks, heredocs, COPY --exclude)
- Auto-updates without upgrading Docker/BuildKit
- Can run `docker build --check` for linting

### 1. Browser vs Server URLs - Use Separate Variable Names
**Problem:** Browser runs on host (needs localhost), server runs in container (needs service names)
**Solution:** Use DIFFERENT variable names - no confusion:
```yaml
build:
  args:
    - NEXT_PUBLIC_API_URL=http://localhost:8000   # Browser only
environment:
  - SERVER_API_URL=http://api:8000                # Server only
```
**Code change:** Server-side routes use `process.env.SERVER_API_URL || process.env.NEXT_PUBLIC_API_URL`

This is cleaner than using same variable with different values.

### 2. localhost in Container
**Problem:** localhost refers to container, not host or other containers
**Solution:** Use Docker service names (api, web, sso) for server-side

### 3. Healthcheck IPv6 Issue
**Problem:** `wget http://localhost:3000` fails with IPv6 resolution
**Solution:** Always use `127.0.0.1` instead of `localhost` in healthchecks:
```yaml
healthcheck:
  test: ["CMD", "wget", "--spider", "http://127.0.0.1:3000/"]  # NOT localhost!
```

### 4. Database Driver Detection (Neon vs Local Postgres)
**Problem:** Code detects Neon vs local postgres incorrectly with Docker service names
**Solution:** Add `sslmode=disable` to local postgres URLs:
```yaml
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/db?sslmode=disable
```
Code can check: `url.includes("sslmode=disable")` → local postgres

### 5. Auth Origins
**Problem:** Better Auth rejects requests from unknown origins
**Solution:** Add Docker service names to trustedOrigins BEFORE building

### 6. Service Startup Order
**Problem:** Frontend starts before API is ready
**Solution:** Use `depends_on` with `condition: service_healthy`

### 7. Health Check Timing
**Problem:** Container marked unhealthy before app starts
**Solution:** Use `start_period` in health check (e.g., 40s)

### 8. pgAdmin Email Validation
**Problem:** pgAdmin rejects `.local` domains
**Solution:** Use valid email like `admin@example.com`

### 9. Package Dependencies
**Problem:** playwright (300MB+) in dependencies bloats image
**Solution:** Keep test tools in devDependencies, ensure `postgres` driver is in dependencies

### 10. MCP Server Host Validation (421 Misdirected Request)
**Problem:** FastMCP's transport security rejects Docker service names
**Error:** `421 Misdirected Request - Invalid Host header`
**Cause:** MCP SDK defaults to `allowed_hosts=["127.0.0.1:*", "localhost:*", "[::1]:*"]`
**Solution:** Configure transport security to allow Docker container names:
```python
from mcp.server.transport_security import TransportSecuritySettings

transport_security = TransportSecuritySettings(
    allowed_hosts=[
        "127.0.0.1:*",
        "localhost:*",
        "[::1]:*",
        "mcp-server:*",  # Docker container name
        "0.0.0.0:*",
    ],
)
mcp = FastMCP(..., transport_security=transport_security)
```

### 11. MCP Server Health Check (406 Not Acceptable)
**Problem:** MCP `/mcp` endpoint returns 406 on GET requests
**Solution:** Add a separate `/health` endpoint via ASGI middleware:
```python
class HealthMiddleware:
    def __init__(self, app): self.app = app
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope["path"] == "/health":
            response = JSONResponse({"status": "healthy"})
            await response(scope, receive, send)
            return
        await self.app(scope, receive, send)
```

### 12. Database Migration Order (Drizzle vs SQLModel)
**Problem:** Drizzle `db:push` drops tables not in its schema (including API tables)
**Root Cause:** If API creates tables, then Drizzle runs, Drizzle drops them
**Solution:** Startup order must be:
1. Start postgres ONLY
2. Run Drizzle migrations (db:push)
3. THEN start API (creates its own tables)
See `references/startup-script-pattern.md`

### 13. SQLModel Table Creation
**Problem:** `SQLModel.metadata.create_all()` doesn't create tables
**Cause:** Models not imported before `create_all()` runs
**Solution:** Explicitly import all models in database.py:
```python
# MUST import before create_all()
from .models import User, Task, Project  # noqa: F401
```

### 14. JWKS Key Mismatch (401 Unauthorized)
**Problem:** JWT validated against wrong SSO instance's keys
**Error:** `Key not found - token kid: ABC, available kids: ['XYZ']`
**Cause:** Logged in via local SSO, but Docker API validates against Docker SSO
**Solution:** Clear browser cookies and login fresh through Docker stack

### 15. uv Network Timeout in Docker Build
**Problem:** `uv pip install` fails with network timeout
**Error:** `Failed to download distribution due to network timeout`
**Solution:** Increase timeout in Dockerfile:
```dockerfile
RUN UV_HTTP_TIMEOUT=120 uv pip install --system --no-cache -r pyproject.toml
```

---

## Output Checklist

After containerization, verify:

- [ ] Dockerfiles created for all services
- [ ] docker-compose.yml with proper networking
- [ ] .env.docker template with service names
- [ ] CONTAINERIZATION.md with required code changes
- [ ] Health checks configured
- [ ] Non-root users in all Dockerfiles
- [ ] Build ARGs for NEXT_PUBLIC_* variables
- [ ] Auth origins documented for update

---

## Resources

### references/
- `impact-analysis.md` - Detailed impact analysis guide
- `network-topology.md` - Docker/K8s networking patterns
- `auth-containerization.md` - Better Auth + Docker guide

### assets/
- `Dockerfile.fastapi` - FastAPI blueprint
- `Dockerfile.nextjs` - Next.js blueprint
- `Dockerfile.python` - Generic Python blueprint
- `docker-compose.template.yml` - Compose template
