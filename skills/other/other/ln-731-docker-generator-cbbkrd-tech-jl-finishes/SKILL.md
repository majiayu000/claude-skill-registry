---
name: ln-731-docker-generator
description: Generates Docker and docker-compose configuration for multi-container development
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-731-docker-generator

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-730-devops-setup

Generates production-ready Docker configuration for containerized development.

---

## Purpose & Scope

Creates Docker infrastructure for local development and production:
- **Does**: Generate Dockerfiles, docker-compose, .dockerignore, nginx config
- **Does NOT**: Build images, start containers, manage deployments

---

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| **Stack Type** | ln-730 coordinator | frontend, backend-dotnet, backend-python |
| **Versions** | Auto-detected | Node.js, .NET, Python versions |
| **Project Name** | Directory name | Used for container naming |
| **Ports** | Defaults or detected | Frontend: 3000, Backend: 5000/8000, DB: 5432 |

---

## Outputs

| File | Purpose | Template |
|------|---------|----------|
| `Dockerfile.frontend` | Frontend build & serve | [dockerfile_frontend.template](references/dockerfile_frontend.template) |
| `Dockerfile.backend` | Backend build & run | [dockerfile_backend_dotnet.template](references/dockerfile_backend_dotnet.template) or [dockerfile_backend_python.template](references/dockerfile_backend_python.template) |
| `docker-compose.yml` | Service orchestration | [docker_compose.template](references/docker_compose.template) |
| `.dockerignore` | Build context exclusions | [dockerignore.template](references/dockerignore.template) |
| `nginx.conf` | Frontend proxy config | [nginx.template](references/nginx.template) |

---

## Workflow

### Phase 1: Input Validation

Validate received configuration from coordinator:
- Check stack type is supported (frontend, backend-dotnet, backend-python)
- Verify versions are valid (Node 18+, .NET 8+, Python 3.10+)
- Confirm project directory exists

**Output**: Validated configuration or error

### Phase 2: Template Selection

Select appropriate templates based on stack:

| Stack | Templates Used |
|-------|----------------|
| **Frontend only** | dockerfile_frontend, nginx, dockerignore |
| **Backend .NET** | dockerfile_backend_dotnet, docker_compose, dockerignore |
| **Backend Python** | dockerfile_backend_python, docker_compose, dockerignore |
| **Full stack .NET** | All of the above (dotnet variant) |
| **Full stack Python** | All of the above (python variant) |

### Phase 3: Variable Substitution

Replace template variables with detected values:

| Variable | Source | Example |
|----------|--------|---------|
| `{{NODE_VERSION}}` | package.json engines or default | 22 |
| `{{DOTNET_VERSION}}` | *.csproj TargetFramework | 9.0 |
| `{{PYTHON_VERSION}}` | pyproject.toml or default | 3.12 |
| `{{PROJECT_NAME}}` | Directory name | my-app |
| `{{DLL_NAME}}` | *.csproj AssemblyName | MyApp.Api.dll |
| `{{FRONTEND_PORT}}` | Default or detected | 3000 |
| `{{BACKEND_PORT}}` | Stack-dependent | 5000 (.NET), 8000 (Python) |
| `{{BACKEND_HOST}}` | Service name | backend |
| `{{CMD}}` | Framework-dependent | `["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]` (FastAPI) or `["gunicorn", "--bind", "0.0.0.0:8000", "{{PROJECT_NAME}}.wsgi:application"]` (Django) |

### Phase 4: File Generation

Generate files from templates:
1. Check if file already exists (warn before overwrite)
2. Apply variable substitution
3. Write file to appropriate location
4. Validate syntax where possible

**File Locations**:
- `Dockerfile.frontend` -> `src/frontend/Dockerfile`
- `Dockerfile.backend` -> project root
- `docker-compose.yml` -> project root
- `.dockerignore` -> project root
- `nginx.conf` -> `src/frontend/nginx.conf`

---

## Supported Stacks

### Frontend: React/Vite + Nginx

**Requirements**:
- package.json with build script
- Vite or CRA configuration

**Generated**:
- Multi-stage Dockerfile (builder + nginx)
- Nginx config with SPA routing and API proxy

### Backend: .NET 8/9

**Requirements**:
- *.sln file in root
- *.csproj with TargetFramework

**Generated**:
- Multi-stage Dockerfile (SDK build + ASP.NET runtime)
- Health check endpoint configuration

### Backend: Python (FastAPI/Django)

**Requirements**:
- requirements.txt or pyproject.toml

**Generated**:
- Multi-stage Dockerfile (builder + slim runtime)
- uvicorn (FastAPI) or gunicorn (Django) entrypoint

---

## Security & Performance Best Practices

All generated files follow these guidelines:

| Practice | Implementation |
|----------|----------------|
| **Non-root user** | Create and use appuser (UID 1001) |
| **Minimal images** | Alpine/slim variants |
| **Multi-stage builds** | Exclude build tools from runtime |
| **No secrets** | Use environment variables, not hardcoded |
| **Health checks** | Built-in HEALTHCHECK instructions (wget/curl) |
| **Specific versions** | Pin base image versions (e.g., nginx:1.27-alpine) |
| **Non-interactive mode** | ARG DEBIAN_FRONTEND=noninteractive |
| **Layer caching** | Copy dependency files first, source code last |
| **BuildKit cache** | Use `--mount=type=cache` for pip |
| **Python optimization** | PYTHONDONTWRITEBYTECODE=1, PYTHONUNBUFFERED=1 |

---

## Quality Criteria

Generated files must meet:
- [ ] `docker-compose config` validates without errors
- [ ] All base images use specific versions (not `latest`)
- [ ] Non-root user configured in all Dockerfiles
- [ ] Health checks present for all services
- [ ] .dockerignore excludes all sensitive files
- [ ] No hardcoded secrets or passwords

---

## Critical Notes

1. **Version Detection**: Use detected versions from coordinator, not hardcoded defaults.
2. **Idempotent**: Check file existence before writing. Warn if overwriting.
3. **Template-based**: All generation uses templates from references/. Do NOT hardcode file contents.
4. **Security First**: Every generated file must follow security best practices.

---

## Reference Files

| File | Purpose |
|------|---------|
| [dockerfile_frontend.template](references/dockerfile_frontend.template) | React/Vite multi-stage Dockerfile |
| [dockerfile_backend_dotnet.template](references/dockerfile_backend_dotnet.template) | .NET multi-stage Dockerfile |
| [dockerfile_backend_python.template](references/dockerfile_backend_python.template) | Python multi-stage Dockerfile |
| [docker_compose.template](references/docker_compose.template) | docker-compose.yml template |
| [dockerignore.template](references/dockerignore.template) | .dockerignore template |
| [nginx.template](references/nginx.template) | Nginx configuration |

---

**Version:** 1.2.0
**Last Updated:** 2026-01-21
