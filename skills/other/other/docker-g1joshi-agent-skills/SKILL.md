---
name: docker
description: Docker containerization with Dockerfile, Compose, and multi-stage builds. Use for containers.
---

# Docker

Docker standardizes software delivery by packaging apps into containers. In 2025, Docker emphasizes **BuildKit** for high-performance builds and **Docker Scout** for supply chain security.

## When to Use

- **Local Development**: Replicate production environments locally (`docker compose`).
- **CI/CD**: Standard unit of deployment for 99% of modern pipelines.
- **Legacy Migration**: Wrap old apps in containers to extend their life.

## Quick Start (BuildKit)

```dockerfile
# syntax=docker/dockerfile:1
FROM node:22-alpine AS base
WORKDIR /app
COPY package*.json ./

FROM base AS deps
RUN npm ci

FROM base AS release
COPY --from=deps /app/node_modules ./node_modules
COPY . .
CMD ["node", "index.js"]
```

## Core Concepts

### BuildKit

The modern build engine (default in 2025). Features concurrent build steps, secret mounting, and cache exports.
`DOCKER_BUILDKIT=1 docker build .`

### Multi-stage Builds

Keep images tiny by separating "build" environment (compilers, SDKs) from "runtime" environment (minimal OS).

### Docker Compose

Define multi-container apps.
`docker compose up -d --watch` (New `watch` mode syncs files continuously).

## Best Practices (2025)

**Do**:

- **Use `docker init`**: Generates best-practice Dockerfiles and .dockerignore for your language.
- **Use Distroless / Alpine**: Minimize attack surface.
- **Scan with Docker Scout**: Check for CVEs early in the pipeline.

**Don't**:

- **Don't run as Root**: Use `USER node` or create a specific user in the Dockerfile.
- **Don't leak secrets**: Use `--mount=type=secret` during build, never `COPY .env`.

## References

- [Docker Documentation](https://docs.docker.com/)
