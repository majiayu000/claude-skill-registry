---
name: docker
description: Containerisation best practices, image optimisation, and multi-container orchestration
category: DevOps Operations
---

# Skill: docker

## What I do

I provide expertise in containerisation using Docker. I focus on creating reproducible development environments, building optimised production images, and orchestrating multi-service applications.

## When to use me

- Building production-ready container images
- Optimising build times and image sizes
- Defining multi-service stacks with Docker Compose
- Implementing multi-stage builds for compiled languages
- Ensuring consistent environments across dev, test, and prod

## Core principles

1. **Reproducibility** — Environments should be identical regardless of the host
2. **Immutability** — Images are never modified once built; they are replaced
3. **Layer Optimisation** — Order commands to maximise cache hits
4. **Security** — Use minimal base images and run as non-root users
5. **Isolation** — Each container should have a single responsibility

## Patterns & examples

**Optimised Multi-stage Build:**
```dockerfile
# Stage 1: Build
FROM golang:1.21-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o /app/bin/server

# Stage 2: Runtime (Minimal)
FROM alpine:3.18
RUN adduser -D -u 1000 appuser
USER appuser
COPY --from=builder /app/bin/server /server
ENTRYPOINT ["/server"]
```

**Layer Caching (Correct Order):**
```dockerfile
FROM node:20-slim
WORKDIR /app
# Install dependencies first (infrequent changes)
COPY package.json package-lock.json ./
RUN npm ci
# Copy source code last (frequent changes)
COPY . .
CMD ["npm", "start"]
```

## Anti-patterns to avoid

- ❌ **Running as root** — Increases attack surface; always use a non-privileged user
- ❌ **Bloated base images** — Avoid `ubuntu` or full `node` images; use `alpine` or `slim`
- ❌ **Secrets in Dockerfile** — Never use `ENV` or `ARG` for passwords or API keys
- ❌ **Hardcoded Config** — Use environment variables or volume mounts instead
- ❌ **Large Layers** — Don't combine unrelated files; keep `.dockerignore` updated


## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/DevOps-Operations/Docker.md`

## Related skills

- `devops` - Broader operational patterns
- `infrastructure-as-code` - Provisioning container hosts
- `automation` - CI/CD integration for container builds
- `security` - Scanning images for vulnerabilities
