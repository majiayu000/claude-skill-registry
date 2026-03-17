---
name: ln-730-devops-setup
description: Coordinates Docker, CI/CD, and environment configuration setup via auto-detection
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-730-devops-setup

**Type:** L2 Domain Coordinator
**Category:** 7XX Project Bootstrap
**Parent:** ln-700-project-bootstrap

Coordinates DevOps infrastructure setup by delegating to specialized workers.

---

## Purpose & Scope

Orchestrates the complete DevOps setup for a project:
- **Does**: Auto-detect stack, delegate to workers, verify configuration
- **Does NOT**: Generate files directly (delegates to ln-731, ln-732, ln-733)

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Project directory with source code |
| **Output** | Docker, CI/CD, environment configuration |
| **Workers** | ln-731 (Docker), ln-732 (CI/CD), ln-733 (Environment) |
| **Mode** | Auto-detect (no user prompts) |

---

## Supported Stacks

| Component | Option 1 | Option 2 |
|-----------|----------|----------|
| **Frontend** | React/Vite + Nginx | - |
| **Backend** | .NET 8/9 | Python (FastAPI/Django) |
| **Database** | PostgreSQL | - |
| **CI/CD** | GitHub Actions | - |

---

## Workflow

### Phase 1: Pre-flight Validation

Check required tools and project structure:
- Verify Docker is installed (`docker --version`)
- Verify docker-compose is available
- Check for existing DevOps files (warn if overwriting)

**Output**: Validation report or STOP with instructions

### Phase 2: Project Analysis (Auto-detect)

Detect project stack automatically:

| Detection | Method | Files to Check |
|-----------|--------|----------------|
| **Frontend** | Package.json presence | `src/frontend/package.json`, `package.json` |
| **Backend .NET** | .csproj/.sln presence | `*.sln`, `src/**/*.csproj` |
| **Backend Python** | requirements.txt/pyproject.toml | `requirements.txt`, `pyproject.toml` |
| **Database** | Connection strings in code | `appsettings.json`, `.env.example` |
| **Existing CI/CD** | Workflow files | `.github/workflows/`, `azure-pipelines.yml` |

**Version Detection**:
- Node.js: Read from `package.json` engines or use `node -v`
- .NET: Read from `*.csproj` TargetFramework
- Python: Read from `pyproject.toml` or `runtime.txt`
- PostgreSQL: Default to latest stable (17)

**Output**: Stack configuration object with detected versions

### Phase 3: Worker Delegation

Delegate to workers in parallel (independent tasks):

```
ln-730 (Coordinator)
    |
    +---> ln-731-docker-generator (via Task tool)
    |         Input: stack config, versions
    |         Output: Dockerfile.*, docker-compose.yml, .dockerignore
    |
    +---> ln-732-cicd-generator (via Task tool)
    |         Input: stack config, detected commands
    |         Output: .github/workflows/ci.yml
    |
    +---> ln-733-env-configurator (via Task tool)
              Input: detected environment variables
              Output: .env.example, .env.development, .gitignore updates
```

**Error Handling**:
- If worker fails, log error and continue with others
- Report all failures at the end
- Suggest manual fixes for failed components

### Phase 4: Configuration Verification

Verify generated configuration:
- Run `docker-compose config` to validate syntax
- Check all referenced files exist
- Verify no secrets in committed files

**Output**: Verification report

### Phase 5: Completion Report

Generate summary:
- List all created files
- Show detected stack configuration
- Provide next steps for user

---

## Generated Files

### Docker (ln-731)
- `Dockerfile.frontend` - Multi-stage build for frontend
- `Dockerfile.backend` - Multi-stage build for backend
- `docker-compose.yml` - Service orchestration
- `docker-compose.override.yml` - Development overrides (optional)
- `.dockerignore` - Build context exclusions

### CI/CD (ln-732)
- `.github/workflows/ci.yml` - Main CI pipeline

### Environment (ln-733)
- `.env.example` - Template with all variables
- `.env.development` - Development defaults
- `.env.production` - Production template (placeholders)
- `.gitignore` updates - Secrets protection

---

## Critical Notes

1. **Auto-detect Only**: No interactive prompts. Uses detected values or sensible defaults.
2. **Idempotent**: Check file existence before creation. Warn before overwriting.
3. **Parallel Execution**: Workers are independent, can run in parallel.
4. **Error Recovery**: Continue on partial failures, report all issues at end.
5. **Version Pinning**: Use detected versions, not hardcoded values.

---

## Definition of Done

- [ ] Pre-flight validation passed
- [ ] Stack auto-detected successfully
- [ ] All workers completed (or failures documented)
- [ ] `docker-compose config` validates successfully
- [ ] No secrets in generated files
- [ ] Completion report displayed

---

## Reference Files

- Worker: `../ln-731-docker-generator/SKILL.md`
- Worker: `../ln-732-cicd-generator/SKILL.md`
- Worker: `../ln-733-env-configurator/SKILL.md`

---

**Version:** 1.1.0
**Last Updated:** 2026-01-10
