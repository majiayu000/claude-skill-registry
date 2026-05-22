---
name: docker-hub-toolkit
description: |
  Automate Python project Docker Hub deployments with optimized multi-stage builds, CI/CD pipelines, and security best practices.
  This skill should be used when users ask to containerize Python apps, build Docker images, push to Docker Hub, set up CI/CD for Docker, optimize Dockerfiles, debug Docker build failures, or deploy Python projects as containers.
---

# Docker Hub Toolkit

End-to-end automation for deploying Python project images to Docker Hub with maximum performance and efficiency.

## What This Skill Does

- Generates optimized multi-stage Dockerfiles (base → builder → dev → production)
- Builds, tags, and pushes images to Docker Hub
- Creates CI/CD pipelines (GitHub Actions) for automated deployment
- Optimizes image size and build speed with BuildKit caching
- Sets up multi-platform builds (amd64/arm64)
- Generates `.dockerignore` and `docker-compose.yml`
- Scans images for security vulnerabilities
- Debugs failed Docker builds

## What This Skill Does NOT Do

- Deploy to Kubernetes/ECS/cloud orchestrators (container runtime only)
- Manage Docker Hub billing or account settings
- Handle non-Python project images
- Create Docker Swarm or cluster configurations
- Manage Docker Hub webhooks or automated test integrations

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Python framework (FastAPI/Flask/Django), entry point, dependencies file |
| **Conversation** | Docker Hub username, image name, target platforms, version tag |
| **Skill References** | Multi-stage patterns, CI/CD templates, security practices from `references/` |
| **User Guidelines** | Team Docker standards, naming conventions, security requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Required Clarifications

Ask about USER'S context:

1. **Docker Hub credentials**: "What is your Docker Hub username/namespace?"
2. **Project type**: "What Python framework? (FastAPI, Flask, Django, script)"
3. **Entry point**: "What command starts your app? (e.g., `uvicorn app.main:app`)"
4. **Deployment target**: "Local push, or automated CI/CD via GitHub Actions?"

---

## Workflow

### Full Deployment Pipeline

```
1. Generate Dockerfile    → Multi-stage optimized build
2. Create .dockerignore   → Exclude unnecessary files
3. Build image            → With BuildKit caching
4. Tag image              → Semantic version + git SHA
5. Security scan          → Check for vulnerabilities
6. Push to Docker Hub     → Authenticated push
7. Set up CI/CD           → GitHub Actions automation (optional)
```

### Stage-by-Stage Execution

#### Stage 1: Generate Base Configuration

1. Detect Python version from `pyproject.toml`, `setup.py`, or `.python-version`
2. Identify dependency file (`requirements.txt`, `pyproject.toml`, `Pipfile`)
3. Generate `.dockerignore` from `assets/templates/dockerignore.template`
4. Create multi-stage Dockerfile using patterns from `references/multi-stage-builds.md`

#### Stage 2: Build Dependencies Stage

1. Use `--mount=type=cache,target=/root/.cache/pip` for pip caching
2. Use `--mount=type=bind` for dependency files
3. Install to `--user` for clean multi-stage copy
4. Verify dependency resolution succeeds

#### Stage 3: Development/Test Stage (Optional)

1. Copy dependencies from builder
2. Copy source code
3. Run tests (`pytest`) and linting
4. Target with `docker build --target dev`

#### Stage 4: Production Build & Push

1. Fresh slim base image
2. Create non-root user
3. Copy only runtime dependencies from builder
4. Set proper `CMD`/`ENTRYPOINT`
5. Tag with version strategy
6. Push to Docker Hub

---

## Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/build-and-push.sh` | Build, tag, and push image | `bash scripts/build-and-push.sh USERNAME APP_NAME VERSION` |
| `scripts/validate-dockerfile.sh` | Lint and validate Dockerfile | `bash scripts/validate-dockerfile.sh [path/to/Dockerfile]` |
| `scripts/setup-multiplatform.sh` | Configure buildx for multi-arch | `bash scripts/setup-multiplatform.sh` |

---

## Dependencies

- Docker Engine 20.10+ (BuildKit support)
- Docker CLI with buildx plugin
- Docker Hub account with access token
- Git (for SHA-based tagging)
- Python 3.10+ (for the project being containerized)

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Build fails on pip install | Check requirements.txt syntax, verify package availability |
| Push denied/unauthorized | Run `docker login`, verify access token |
| Image too large (>500MB) | Switch to slim base, verify multi-stage COPY |
| BuildKit not available | Set `DOCKER_BUILDKIT=1` or use `docker buildx build` |
| Multi-platform fails | Run `scripts/setup-multiplatform.sh` |
| Rate limit exceeded | Wait or use authenticated pulls |

See `references/troubleshooting.md` for comprehensive error resolution.

---

## Input/Output

- **Input**: Python project with dependency file (requirements.txt/pyproject.toml)
- **Output**: Optimized Docker image pushed to Docker Hub at `username/app:tag`

---

## Output Checklist

Before delivering, verify:

- [ ] Multi-stage Dockerfile with base → builder → production stages
- [ ] `.dockerignore` excludes `.git`, `__pycache__`, `.venv`, `.env`, `node_modules`
- [ ] BuildKit cache mounts used for pip installs
- [ ] Non-root user in production stage
- [ ] `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1` set
- [ ] Image tagged with semantic version
- [ ] Image pushed successfully to Docker Hub
- [ ] Image size < 200MB (for typical Python apps)
- [ ] No secrets or credentials in image layers
- [ ] CI/CD pipeline configured (if requested)

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/multi-stage-builds.md` | Dockerfile patterns, stage architecture, anti-patterns |
| `references/docker-hub-deployment.md` | Push workflow, tagging strategy, Hub settings |
| `references/ci-cd-github-actions.md` | GitHub Actions pipeline, caching, automation |
| `references/claude-integration.md` | Claude Code commands, hooks, CLAUDE.md standards |
| `references/troubleshooting.md` | Build/push errors, size issues, security fixes |
| `documentation/docker_hub_stages.md` | Original multi-stage build stages reference |
| `documentation/docker_hub_python_project_partner.md` | Claude capabilities for Docker Hub |
