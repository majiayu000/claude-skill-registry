---
name: ln-732-cicd-generator
description: Generates GitHub Actions CI workflow configuration
---

# ln-732-cicd-generator

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-730-devops-setup

Generates GitHub Actions CI pipeline for automated testing and validation.

---

## Purpose & Scope

Creates CI/CD workflow for GitHub:
- **Does**: Generate .github/workflows/ci.yml with lint, test, build, docker jobs
- **Does NOT**: Configure deployment, manage secrets, set up CD pipelines

---

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| **Stack Type** | ln-730 coordinator | backend-dotnet, backend-python |
| **Versions** | Auto-detected | Node.js, .NET or Python versions |
| **Frontend Path** | Auto-detected | Path to frontend directory |
| **Build Commands** | Auto-detected | npm scripts, dotnet/pytest commands |

---

## Outputs

| File | Purpose | Template |
|------|---------|----------|
| `.github/workflows/ci.yml` | Main CI pipeline | [github_ci_dotnet.template.yml](references/github_ci_dotnet.template.yml) or [github_ci_python.template.yml](references/github_ci_python.template.yml) |

---

## Workflow

### Phase 1: Stack Analysis

Determine which template to use:

| Detection | Backend Template |
|-----------|------------------|
| `.sln` or `.csproj` present | github_ci_dotnet.template.yml |
| `requirements.txt` or `pyproject.toml` present | github_ci_python.template.yml |

Detect commands:
- Frontend: Read scripts from package.json (lint, build, test)
- .NET: Standard dotnet restore/build/test
- Python: pip install, ruff lint, pytest

### Phase 2: Variable Substitution

Replace template variables:

| Variable | Source | Default |
|----------|--------|---------|
| `{{NODE_VERSION}}` | package.json engines | 22 |
| `{{DOTNET_VERSION}}` | *.csproj TargetFramework | 9.0.x |
| `{{PYTHON_VERSION}}` | pyproject.toml | 3.12 |
| `{{FRONTEND_PATH}}` | Directory detection | src/frontend |

### Phase 3: Directory Creation

Create `.github/workflows/` directory if not exists.

### Phase 4: File Generation

Generate ci.yml from selected template:
1. Check if workflow already exists (warn before overwrite)
2. Apply variable substitution
3. Write to `.github/workflows/ci.yml`
4. Validate YAML syntax

---

## Generated Pipeline Structure

### Jobs Overview

| Job | Purpose | Dependencies |
|-----|---------|--------------|
| **frontend** | Lint, build, test React/Vite | None |
| **backend** | Build, test .NET or Python | None |
| **docker** | Build images, health checks | frontend, backend |

### Frontend Job Steps

1. Checkout code
2. Setup Node.js with caching
3. Install dependencies (`npm ci`)
4. Run linter (`npm run lint`)
5. Build application (`npm run build`)
6. Run tests (`npm test`)

### Backend Job Steps (.NET)

1. Checkout code
2. Setup .NET SDK
3. Restore dependencies (`dotnet restore`)
4. Build (`dotnet build`)
5. Run tests (`dotnet test`)

### Backend Job Steps (Python)

1. Checkout code
2. Setup Python with pip caching
3. Install dependencies (`pip install -r requirements.txt`)
4. Run linter (`ruff check`)
5. Run tests (`pytest`)

### Docker Job Steps

1. Checkout code
2. Build images (`docker compose build`)
3. Start containers (`docker compose up -d`)
4. Wait for startup (30 seconds)
5. Health check frontend (port 3000)
6. Health check backend (port 5000/8000)
7. Show logs on failure
8. Stop containers (`docker compose down`)

---

## Triggers

| Event | Branches |
|-------|----------|
| **Push** | main, develop |
| **Pull Request** | main |

---

## Best Practices Applied

| Practice | Implementation |
|----------|----------------|
| **Dependency caching** | npm cache, pip cache |
| **Pinned versions** | actions/checkout@v4, setup-node@v4 |
| **Parallel jobs** | frontend and backend run in parallel |
| **Fail fast** | docker job waits for both to succeed |
| **Clean up** | docker compose down runs always |
| **Debug support** | logs shown on failure |

---

## Quality Criteria

Generated workflow must:
- [ ] Pass YAML syntax validation
- [ ] Use pinned action versions (not `@latest`)
- [ ] Include dependency caching
- [ ] Have health checks for docker job
- [ ] Clean up resources on completion

---

## Critical Notes

1. **GitHub Actions Only**: This skill generates only GitHub Actions workflows. No Azure/GitLab support.
2. **Template-based**: Use templates from references/. Do NOT hardcode workflow contents.
3. **Idempotent**: Check if .github/workflows/ exists. Warn before overwriting ci.yml.
4. **Version Detection**: Use detected versions, not hardcoded defaults.

---

## Reference Files

| File | Purpose |
|------|---------|
| [github_ci.template.yml](references/github_ci.template.yml) | Full template with comments |
| [github_ci_dotnet.template.yml](references/github_ci_dotnet.template.yml) | Compact .NET stack template |
| [github_ci_python.template.yml](references/github_ci_python.template.yml) | Compact Python stack template |

---

**Version:** 1.1.0
**Last Updated:** 2026-01-10
