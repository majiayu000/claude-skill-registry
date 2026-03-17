---
name: docker-dev
description: Assistance with Local Development using Docker (Compose, DevContainers).
context_cost: medium
---
# Docker Dev Skill

## Triggers
- docker
- compose
- local dev
- devcontainer
- dev environment
- containerize
- dockerization

## Purpose
To set up robust, reproducible local development environments using Docker technologies.

## Capabilities

### 1. Docker Compose (Local Dev)
-   **Generate `compose.yaml`**: Define services (App + DB + Redis).
-   **Watch Mode**: Configure `develop.watch` for hot-reloading (sync + rebuild).
-   **Networking**: Ensure services can talk to each other (and to host if needed).

### 2. DevContainers (VS Code)
-   **Configuration**: Generate `.devcontainer/devcontainer.json`.
-   **Features**: Add standard features (git, node, python, docker-in-docker).
-   **Extensions**: Pre-install VS Code extensions for the team.

### 3. Optimization
-   **Multi-stage Builds**: Separate build-deps from runtime-deps.
-   **Caching**: Optimize layer ordering for faster builds.
-   **Distroless**: Use distroless images for production (keep shells in dev).

## Instructions
1.  **Prefer Compose Watch**: Always recommend `docker compose watch` over legacy volume mounts for code sync.
2.  **User Mapping**: Ensure file permissions work by mapping non-root user (UID/GID) inside container.
3.  **Persistence**: Use Docker Volumes for DB data so it survives restarts.

## Deliverables
-   `compose.yaml` with watch config.
-   `.devcontainer/` folder.
-   `Dockerfile` (Target: dev & prod).
