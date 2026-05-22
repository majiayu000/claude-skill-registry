---
name: devcontainer
description: "Diagnose devcontainer configuration problems and guide development environment setup. This skill should be used when the user asks to 'set up devcontainer', 'fix container startup', 'configure VS Code dev container', 'Codespaces setup', or has Docker development environment issues. Keywords: devcontainer, docker, VS Code, Codespaces, container, development environment, Dockerfile."
license: MIT
compatibility: Requires Docker Desktop or compatible container runtime. Works with VS Code and GitHub Codespaces.
metadata:
  author: jwynia
  version: "1.0"
---

# Devcontainer Diagnostic

Diagnose devcontainer and Docker development environment problems. Help create reproducible, fast-starting development environments that work consistently across VS Code, GitHub Codespaces, and team members.

## When to Use This Skill

Use this skill when:
- Setting up a new devcontainer
- Container startup is too slow
- Configuration errors or conflicts
- Different behavior in VS Code vs Codespaces
- Multi-service development environment needed

Do NOT use this skill when:
- Writing application code
- Deploying to production
- Configuring CI/CD pipelines

## Core Principle

**Development containers should provide instant productivity. Every configuration choice affects startup time, reproducibility, and team onboarding. Make these trade-offs explicit.**

## Diagnostic States

### DV0: No Devcontainer Strategy

**Symptoms:** Manual setup, "check the README", works on one machine fails on others

**Interventions:**
- Start with pre-built devcontainer base image
- Use `assets/devcontainer-simple.md` template

### DV1: Slow Container Startup

**Symptoms:** 5+ minute startup, heavy postCreateCommand, avoiding rebuilds

**Key Questions:**
- How long does startup actually take?
- What's in postCreateCommand?
- Are you using prebuilds?

**Interventions:**
- Move npm install/pip install to Dockerfile (cached)
- Use mcr.microsoft.com/devcontainers/* base images
- Configure prebuilds for team repos
- Run `scripts/analyze-devcontainer.ts`

### DV2: Configuration Problems

**Symptoms:** JSON errors, VS Code won't connect, features conflicting

**Checklist:**
- [ ] devcontainer.json passes JSON validation
- [ ] Using only ONE of: image, build.dockerfile, dockerComposeFile
- [ ] Features are compatible and ordered correctly
- [ ] Extensions use correct publisher.extension-name format

### DV3: Environment Parity Issues

**Symptoms:** Works in VS Code, fails in Codespaces (or vice versa)

**Common Issues:**
| Issue | Local VS Code | Codespaces |
|-------|---------------|------------|
| Docker socket | Usually available | Docker-in-Docker needed |
| Secrets | .env files work | Use Codespaces secrets |
| File watching | Native | May need polling |

### DV4: Multi-Service Complexity

**Symptoms:** Need database/cache/queue, services can't communicate

**Interventions:**
- Use Docker Compose integration
- Named volumes for persistence
- Health checks for service readiness
- Use `assets/devcontainer-compose.md` template

### DV5: Dockerfile Issues

**Symptoms:** Build failures, huge images, no caching

**Best Practices:**
```dockerfile
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Dependencies first (cached)
RUN apt-get update && apt-get install -y \
    build-essential && rm -rf /var/lib/apt/lists/*

# Copy deps then install (cached if deps unchanged)
COPY package*.json ./
RUN npm install

# Code last (changes frequently)
COPY . .
```

### DV6: Devcontainer Validated

**Indicators:**
- Startup under 2 minutes
- Works in VS Code and Codespaces
- New developers productive in 30 minutes

## Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `analyze-devcontainer.ts` | Find issues and optimizations | `deno run --allow-read scripts/analyze-devcontainer.ts` |
| `validate-dockerfile.ts` | Check Dockerfile best practices | `deno run --allow-read scripts/validate-dockerfile.ts` |
| `scan-image.ts` | Vulnerability scanning (wraps Trivy) | `deno run --allow-run scripts/scan-image.ts [image]` |

## Anti-Patterns

### The Kitchen Sink
Installing every tool "just in case" - 10+ minute startups.
**Fix:** Start minimal. Add only when needed.

### The postCreateCommand Overload
Everything in postCreateCommand - runs every time.
**Fix:** Move stable operations to Dockerfile.

### The Snowflake Container
Manual changes inside running containers.
**Fix:** ALL changes go in config files.

## Templates

- `assets/devcontainer-simple.md` - Basic single-container setup
- `assets/devcontainer-dockerfile.md` - Custom Dockerfile approach
- `assets/devcontainer-compose.md` - Multi-service setup

## Related Skills

- **system-design** - Multi-service architecture informs Compose config
- **pwa-development** - Consistent environment for PWA toolchain
