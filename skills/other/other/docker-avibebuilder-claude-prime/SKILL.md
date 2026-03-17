---
name: docker
description: "Docker containerization best practices and patterns. Use this skill when creating Dockerfiles, configuring Docker Compose, optimizing images, implementing container security, or deploying to production. Covers multi-stage builds, healthchecks, and resource limits."
---

# Docker

Containerization best practices for Dockerfile and Docker Compose.

## Core Principles (Must Remember)

### Image Building

1. **Minimal base images** - Use slim/alpine variants; pin to digest for reproducibility
2. **Multi-stage builds** - Separate build dependencies from runtime
3. **Layer optimization** - Combine RUN commands; place frequently changed files last
4. **COPY over ADD** - ADD only for tar extraction or remote URLs

### Security

5. **Non-root users** - Always use UID >10000; never run as root in production
6. **No secrets in images** - Use Docker secrets or runtime env injection
7. **.dockerignore required** - Exclude .git, .env, node_modules, build artifacts
8. **Scan images** - Use Trivy, Docker Scout, or Snyk before deployment

### Runtime

9. **One process per container** - Single responsibility principle
10. **Healthchecks required** - Define HEALTHCHECK in Dockerfile or Compose
11. **Resource limits** - Always set mem_limit and cpus in production
12. **Read-only filesystems** - Use --read-only where possible

### Compose

13. **Network segmentation** - Dedicated networks per service group
14. **Named volumes** - Never use anonymous volumes in production
15. **depends_on with healthchecks** - Use condition: service_healthy
16. **Environment separation** - Use override files for dev/staging/prod

## Anti-Patterns (Avoid)

- Running as root (58% of production containers still do this)
- Hardcoded secrets in Dockerfile or compose.yaml
- Using `latest` tag in production
- Single Dockerfile for all environments
- Exposing database ports to host network
- Missing healthchecks (Docker can't detect service failures)

## References

| Reference | Content |
|-----------|---------|
| [dockerfile.md](./references/dockerfile.md) | Multi-stage patterns, CMD vs ENTRYPOINT, ARG/ENV |
| [compose.md](./references/compose.md) | Services, networks, volumes, profiles, depends_on |
| [security.md](./references/security.md) | .dockerignore, secrets, scanning, network isolation |
| [production.md](./references/production.md) | Healthchecks, restart policies, logging, dev workflow |
