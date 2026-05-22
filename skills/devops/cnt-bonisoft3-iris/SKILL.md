---
name: sayt-cnt
description: >
  How to write Dockerfile + compose.yaml — the develop/integrate service
  convention, multi-stage targets, dind helpers.
  Use when containerizing a project, writing docker compose services, or setting up integration tests.
user-invocable: false
---

# launch / integrate — Docker Compose Containerization

`sayt launch` starts a containerized development environment. `sayt integrate` runs integration tests in containers. Both use Docker Compose with a specific service convention.

## How It Works

### `sayt launch`

1. Cleans up any leftover containers: `docker compose down -v --timeout 0 --remove-orphans`
2. Sets up Docker-in-Docker (dind) environment with a socat proxy
3. Runs: `docker compose run --build --service-ports develop`
4. Cleans up the socat container on exit

### `sayt integrate`

1. Cleans up: `docker compose down -v --timeout 0 --remove-orphans`
2. If `--no-cache`: builds without Docker layer cache first
3. Sets up dind environment
4. Runs: `docker compose up integrate --abort-on-container-failure --exit-code-from integrate --force-recreate --build --renew-anon-volumes --remove-orphans --attach-dependencies`
5. On success: cleans up containers
6. On failure: **leaves containers running** for inspection (run `docker compose logs` or `docker compose down -v` when done)

## The compose.yaml Convention

sayt expects two services in `compose.yaml`:

### `develop` service (for `sayt launch`)

The development service runs your app with hot reload, debugging, port mapping, etc.

```yaml
services:
  develop:
    command: ./gradlew dev -t          # Your dev command
    ports:
      - "8080:8080"                    # Expose ports to host
    build:
      network: host
      context: ../..                   # Monorepo root (or ".")
      dockerfile: services/myapp/Dockerfile
      secrets:
        - host.env
      target: debug                    # Dockerfile stage for dev
    volumes:
      - //var/run/docker.sock:/var/run/docker.sock
    entrypoint:
      - /monorepo/plugins/devserver/dind.sh
    secrets:
      - host.env
    network_mode: host
```

### `integrate` service (for `sayt integrate`)

The integration service runs your test suite in an isolated container.

```yaml
services:
  integrate:
    command: "true"                    # Overridden by Dockerfile CMD
    build:
      network: host
      context: ../..
      dockerfile: services/myapp/Dockerfile
      secrets:
        - host.env
      target: integrate               # Dockerfile stage for integration
```

### Secrets

```yaml
secrets:
  host.env:
    environment: HOST_ENV             # Injected by sayt's dind helper
```

The `HOST_ENV` secret contains Docker credentials, Kubernetes config, and dind connection info.

## Dockerfile Multi-Stage Pattern

sayt expects Dockerfiles with at least two targets:

### `debug` target (used by `develop`)

Contains the full development environment with source code, tools, and hot reload:

```dockerfile
FROM node:22 AS debug
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install
COPY . .
CMD ["pnpm", "dev"]
```

### `integrate` target (used by `integrate`)

Extends debug with integration test execution:

```dockerfile
FROM debug AS integrate
COPY tests/ tests/
CMD ["pnpm", "test:int"]
```

### Full Multi-Stage Example (JVM)

```dockerfile
# Base with tools
FROM eclipse-temurin:21 AS debug
WORKDIR /app
COPY gradlew gradlew.bat gradle.properties settings.gradle.kts build.gradle.kts ./
COPY gradle/ gradle/
RUN ./gradlew dependencies
COPY src/main/ src/main/
COPY .vscode/ .vscode/
RUN ./gradlew assemble
COPY src/test/ src/test/

# Integration tests
FROM debug AS integrate
COPY src/it/ src/it/
CMD ["./gradlew", "integrationTest"]
```

### Full Multi-Stage Example (Node.js)

```dockerfile
FROM node:22 AS debug
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile
COPY . .
RUN pnpm build
CMD ["pnpm", "dev"]

FROM debug AS integrate
CMD ["pnpm", "test:int", "--run"]
```

## Docker-in-Docker (dind) Support

sayt provides dind helpers for scenarios where containers need to talk to Docker (e.g., testcontainers):

1. **socat proxy** — A socat container is started to proxy the Docker socket over TCP
2. **Environment variables** — `DOCKER_HOST`, `TESTCONTAINERS_HOST_OVERRIDE`, and `DOCKER_AUTH_CONFIG` are injected
3. **host.env secret** — All dind connection info is passed as a build secret

This enables testcontainers-based integration tests to create sibling containers.

## Host Networking

sayt services use `network_mode: host` by default. This means:
- Services can reach each other via `localhost`
- No port mapping conflicts
- Testcontainers can connect back to the host Docker daemon
- Works on Linux natively; on macOS, Docker Desktop provides host networking emulation

## Complete compose.yaml Example

```yaml
volumes:
  root-dot-docker-cache-mount: {}

services:
  develop:
    command: ./gradlew dev -t
    ports:
      - "8080:8080"
    build:
      network: host
      context: ../..
      dockerfile: services/tracker/Dockerfile
      secrets:
        - host.env
      target: debug
    volumes:
      - //var/run/docker.sock:/var/run/docker.sock
      - ${HOME:-~}/.skaffold/cache:/root/.skaffold/cache
    entrypoint:
      - /monorepo/plugins/devserver/dind.sh
    secrets:
      - host.env
    network_mode: host

  integrate:
    command: "true"
    build:
      network: host
      context: ../..
      dockerfile: services/tracker/Dockerfile
      secrets:
        - host.env
      target: integrate

secrets:
  host.env:
    environment: HOST_ENV
```

## Cleanup Behavior

- **Success**: `sayt integrate` automatically runs `docker compose down -v` to clean up
- **Failure**: Containers are **left running** so you can inspect logs:
  ```bash
  docker compose logs          # View all logs
  docker compose logs integrate # View integration service logs
  docker compose down -v       # Clean up manually when done
  ```

## Writing Good Compose Files for sayt

1. **Always define `develop` and `integrate`** — These are the services sayt expects
2. **Use `target:` in build** — `debug` for develop, `integrate` for integrate
3. **Set `context` to monorepo root** — Usually `../..` from a service directory
4. **Include the `host.env` secret** — Required for dind and credential forwarding
5. **Use `network_mode: host`** for develop — Simplifies networking
6. **Set `command: "true"` for integrate** — Let the Dockerfile CMD handle execution

## Current flags

!`sayt help launch 2>&1 || true`
!`sayt help integrate 2>&1 || true`
