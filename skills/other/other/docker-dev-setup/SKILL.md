---
name: docker-dev-setup
description: "Containerize an application with a production-grade Dockerfile, Docker Compose for local development, and optional Dev Container configuration. Use for: Dockerizing apps, multi-stage builds, Compose local dev stacks, .dockerignore, image size optimization, dev containers. Triggers: docker, dockerfile, compose, container, containerize, dockerize, docker-compose, devcontainer, dev container, docker setup, docker image, docker build."
---

# Docker Dev Setup

Create a production-grade Docker setup for any application: multi-stage Dockerfile, Compose for local development services, .dockerignore, and optional VS Code Dev Container.

## When to Use

- Dockerizing an application for the first time
- Creating a multi-stage Dockerfile for smaller, secure images
- Setting up Docker Compose for local development (app + database + cache)
- Adding a `.dockerignore` to speed up builds and prevent secret leaks
- Optimizing an existing Docker image (size, build speed, security)
- Creating a Dev Container for VS Code / GitHub Codespaces
- Debugging Docker build failures or runtime issues

## Tools Used

- **Read** — inspect existing project files (package.json, requirements.txt, go.mod, existing Dockerfiles)
- **Write** — create Dockerfile, compose.yaml, .dockerignore, devcontainer.json
- **Edit** — modify existing Docker configuration
- **Bash** — run docker build, docker compose, check image size
- **Glob** — find project entry points, existing Docker files
- **Grep** — detect frameworks, dependencies, existing Docker usage

## Bundled Files

```
docker-dev-setup/
├── references/
│   ├── dockerfile-patterns.md    # Multi-stage builds, caching, security
│   ├── compose-patterns.md       # Services, health checks, volumes, networking
│   └── troubleshooting.md        # Common errors and fixes
└── templates/
    ├── Dockerfile.node           # Node.js/TypeScript multi-stage
    ├── Dockerfile.python         # Python multi-stage
    ├── Dockerfile.go             # Go multi-stage (scratch/distroless)
    ├── compose.yaml              # Local dev stack (app + postgres + redis)
    ├── dockerignore              # Universal .dockerignore template
    └── devcontainer.json         # VS Code Dev Container config
```

## Workflow

Follow these phases in order. **Stop after each phase** to confirm with the user before continuing.

---

### Phase 1: Discover

**Goal:** Understand the project stack and what needs containerizing.

1. Check for an existing project:
   ```
   Read package.json       → Node.js/TypeScript (check for build script, entry point)
   Read requirements.txt   → Python (check for gunicorn/uvicorn)
   Read go.mod             → Go (check module path)
   Read pyproject.toml     → Python (check for poetry/uv)
   Glob Dockerfile*        → existing Docker setup
   Glob compose*           → existing Compose files
   Glob .devcontainer/**   → existing Dev Container
   ```

2. Identify the key details:
   - **Language/runtime**: Node.js, Python, Go, or other
   - **Package manager**: npm/yarn/pnpm, pip/poetry/uv, go mod
   - **Build step**: Does the app need compilation? (TypeScript, Go, etc.)
   - **Entry point**: What command starts the app? (node server.js, gunicorn, ./binary)
   - **Services needed**: Database (PostgreSQL, MySQL, SQLite), cache (Redis), queue (RabbitMQ), etc.
   - **Existing Docker files**: Any Dockerfile or compose.yaml already present?

3. Choose the appropriate template from `templates/`:
   - Node.js/TypeScript → `Dockerfile.node`
   - Python → `Dockerfile.python`
   - Go → `Dockerfile.go`
   - Other → Use `references/dockerfile-patterns.md` to build from scratch

> **STOP.** Confirm the stack, entry point, and which services the user needs.

---

### Phase 2: Dockerfile

**Goal:** Create a production-grade, multi-stage Dockerfile.

1. Read the appropriate template from `templates/` and `references/dockerfile-patterns.md`.

2. Create the Dockerfile at the project root. Every Dockerfile should include:
   - **Multi-stage build**: Separate build and runtime stages
   - **Layer caching**: Copy dependency files BEFORE source code
   - **Minimal base image**: Use `-alpine` or `-slim` variants (not full `ubuntu` or `node:22`)
   - **Non-root user**: Create and switch to a non-root user
   - **Health check**: Add `HEALTHCHECK` for HTTP services
   - **Signal handling**: Use `dumb-init` or `tini` for Node.js (PID 1 problem)

3. Create `.dockerignore` from `templates/dockerignore`. Customize for the project's language.

4. Key rules from `references/dockerfile-patterns.md`:
   - Use `COPY` not `ADD` (unless extracting tar archives)
   - Use exec form for CMD: `CMD ["node", "server.js"]` not `CMD node server.js`
   - Combine `apt-get update && apt-get install && rm -rf /var/lib/apt/lists/*` in one RUN
   - Pin base image versions: `node:22-alpine` not `node:latest`
   - Use `npm ci` not `npm install` in Docker builds
   - For Go: `CGO_ENABLED=0` for static binaries that run on `scratch`

> **STOP.** Review the Dockerfile with the user. Verify it builds: `docker build -t app .`

---

### Phase 3: Compose

**Goal:** Set up Docker Compose for local development.

1. Read `references/compose-patterns.md` and `templates/compose.yaml`.

2. Create `compose.yaml` (not `docker-compose.yml` — Compose v2 convention) at the project root:
   - **App service**: Build from local Dockerfile, bind-mount source for hot reload, forward ports
   - **Database service**: PostgreSQL/MySQL with health check, named volume for data persistence
   - **Cache service** (if needed): Redis with health check
   - **depends_on with condition**: Use `condition: service_healthy` so the app waits for services to be ready

3. Health check patterns for common services:
   ```yaml
   # PostgreSQL
   healthcheck:
     test: ["CMD-SHELL", "pg_isready -U postgres"]
     interval: 10s
     timeout: 5s
     retries: 5

   # Redis
   healthcheck:
     test: ["CMD", "redis-cli", "ping"]
     interval: 10s
     timeout: 5s
     retries: 5

   # MySQL
   healthcheck:
     test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
     interval: 10s
     timeout: 5s
     retries: 5
   ```

4. Key rules:
   - Do NOT include a `version:` key — it's deprecated in Compose v2
   - Use named volumes for database data (not bind mounts)
   - Use bind mounts for application source code (enables hot reload)
   - Set environment variables via `environment:` block, not `.env` files in the image
   - Use `restart: unless-stopped` for infrastructure services

> **STOP.** Confirm the Compose setup. Verify it starts: `docker compose up`

---

### Phase 4: Dev Container (optional)

**Goal:** Add VS Code Dev Container support for reproducible dev environments.

1. Only do this phase if the user wants Dev Container support. Skip otherwise.

2. Read `templates/devcontainer.json`.

3. Create `.devcontainer/devcontainer.json` with:
   - Base image or Dockerfile reference
   - VS Code extensions to auto-install
   - Port forwarding for the app and services
   - `postCreateCommand` for dependency installation
   - `remoteUser` set to non-root
   - Features for common tools (Docker-in-Docker, CLI tools)

4. If using Compose, reference the compose file:
   ```json
   {
     "dockerComposeFile": "../compose.yaml",
     "service": "app",
     "workspaceFolder": "/app"
   }
   ```

> **STOP.** Confirm the Dev Container config. Test by reopening in container.

---

## Troubleshooting Quick Reference

Read `references/troubleshooting.md` for detailed solutions.

| Symptom | Likely Cause | Quick Fix |
|---------|-------------|-----------|
| `COPY failed: file not found` | File excluded by `.dockerignore` or wrong path | Check `.dockerignore`, verify build context |
| Image is 1GB+ | Full base image, no multi-stage | Switch to `-alpine`/`-slim`, add multi-stage |
| Container exits immediately | PID 1 signal handling, missing CMD | Use `dumb-init`, check CMD/ENTRYPOINT |
| `port is already allocated` | Port conflict on host | Change host port in compose or stop other containers |
| Build is slow despite no code changes | Cache invalidated by COPY order | Copy dependency files before source code |
| `depends_on` not waiting for DB | Missing health check condition | Add `condition: service_healthy` |
| Volume permission denied | Non-root user can't write to volume | Use `--chown` in COPY, or fix volume ownership |

## Architecture Notes

- **Multi-stage builds** are the single most impactful optimization. Build stage has compilers/tools; runtime stage has only the artifact. Typical 80-99% size reduction.
- **Layer caching** depends on instruction order. Put things that change rarely (system packages) before things that change often (source code). Copy dependency lock files before source code.
- **Compose v2** uses `docker compose` (space, not hyphen). No `version:` key needed. Health checks + `depends_on: condition: service_healthy` replaces the old `wait-for-it.sh` scripts.
- **Dev Containers** are a spec, not a VS Code feature. They work in Codespaces, DevPod, Gitpod, and any IDE that supports the spec. The `.devcontainer/` directory travels with the repo.
- **.dockerignore** is not optional. Without it, `.git/` alone can add hundreds of MB to the build context, and `.env` files may leak secrets into the image.

## Output Summary

After completing all phases, the user should have:

- [ ] Multi-stage Dockerfile at project root
- [ ] `.dockerignore` customized for the project stack
- [ ] `compose.yaml` with app + services, health checks, named volumes
- [ ] Working `docker compose up` that starts the full local stack
- [ ] (Optional) `.devcontainer/devcontainer.json` for VS Code / Codespaces
