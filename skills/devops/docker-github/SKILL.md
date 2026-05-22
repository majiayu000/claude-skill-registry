---
description: DevOps patterns for Docker and GitHub Actions for [PROJECT_NAME]
globs:
  - "Dockerfile"
  - "docker-compose*.yml"
  - ".github/workflows/**/*.yml"
  - ".github/actions/**/*"
alwaysApply: false
---

# DevOps Skill (Docker + GitHub Actions)

> Project: [PROJECT_NAME]
> Stack: Docker, GitHub Actions
> Generated: [DATE]

## Quick Reference

### Docker
- Multi-stage builds for smaller images
- Use .dockerignore
- Don't run as root
- Pin base image versions

### GitHub Actions
- Use reusable workflows
- Cache dependencies
- Use environment secrets
- Matrix builds for multiple versions

## Available Modules

| Module | File | Use When |
|--------|------|----------|
| Docker Patterns | docker.md | Containerization |
| CI/CD Pipelines | ci-cd.md | GitHub Actions |
| Dos and Don'ts | dos-and-donts.md | Project learnings |

## Project Context

### Tech Stack
<!-- Extracted from agent-os/product/tech-stack.md -->
- **Container Runtime:** [CONTAINER_RUNTIME]
- **CI/CD:** [CI_CD_PLATFORM]
- **Cloud Provider:** [CLOUD_PROVIDER]
- **Registry:** [CONTAINER_REGISTRY]

### Infrastructure Patterns
<!-- Extracted from agent-os/product/architecture-decision.md -->

**Deployment Strategy:**
[DEPLOYMENT_STRATEGY]

**Environment Management:**
[ENVIRONMENT_MANAGEMENT]

**Secrets Management:**
[SECRETS_MANAGEMENT]

### Project Structure
<!-- Extracted from agent-os/product/architecture-structure.md -->
```
[INFRA_STRUCTURE]
```

---

## Self-Learning

→ Füge Erkenntnisse zu `dos-and-donts.md` hinzu.
