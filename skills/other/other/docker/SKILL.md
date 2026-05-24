---
name: docker
description: "ALWAYS activate when the user's query involves Docker in any way — even if it also matches other skills. If the words docker, Dockerfile, docker-compose, compose.yml, container, or image appear in the query, this skill MUST be used. Covers: writing or editing Dockerfiles and compose files, adding services (postgres, redis, etc.) to compose, volume mounts and data persistence, docker build failures (layer caching, npm install issues), healthchecks and service startup ordering (depends_on), environment variables in containers, port mapping, container crashes and exit codes (OOM/137), non-root users, multi-stage builds, image optimization, .dockerignore, and deploying to container runtimes. Takes priority over general implementation or debugging skills when Docker infrastructure is the subject."
---

# Docker

Project-specific containerization patterns for Dockerfile and Docker Compose.

## Architecture Decisions

### Image Building
1. **Minimal base images** — Use slim/alpine variants; pin to digest for reproducibility.
2. **Multi-stage builds** — Separate build dependencies from runtime.
3. **Layer optimization** — Combine RUN commands; place frequently changed files last.
4. **COPY over ADD** — ADD only for tar extraction or remote URLs.

### Security
5. **Non-root users** — Always use UID >10000; never run as root in production.
6. **No secrets in images** — Use Docker secrets or runtime env injection.
7. **.dockerignore required** — Exclude .git, .env, node_modules, build artifacts.

### Runtime
8. **One process per container** — Single responsibility principle.
9. **Healthchecks required** — Define HEALTHCHECK in Dockerfile or Compose.
10. **Resource limits** — Always set mem_limit and cpus in production.

### Compose
11. **Network segmentation** — Dedicated networks per service group.
12. **Named volumes** — Never use anonymous volumes in production.
13. **depends_on with healthchecks** — Use `condition: service_healthy`.
14. **Environment separation** — Use override files for dev/staging/prod.

## Gotchas

- `COPY . .` before `RUN npm install` busts the cache on EVERY code change. Copy `package*.json` first, install, THEN copy source.
- Alpine uses musl libc, not glibc. Python packages with C extensions (numpy, pandas, cryptography) may fail to install or need `apk add` build dependencies. Consider `-slim` variants if you hit this.
- `ENTRYPOINT ["python", "app.py"]` (exec form) handles signals correctly. `ENTRYPOINT python app.py` (shell form) wraps in `/bin/sh -c` and PID 1 won't receive SIGTERM — containers take 10s to stop.
- Docker layer cache is invalidated from the FIRST changed layer downward. A changed `COPY` near the top rebuilds everything below it.
- `depends_on` without `condition: service_healthy` only waits for container START, not readiness. Your app will crash connecting to a database that's still initializing.
- `host.docker.internal` works on Docker Desktop (Mac/Windows) but NOT on Linux. Use `--network host` or explicit container networking on Linux.
- Build args (`ARG`) are NOT available after `FROM` in multi-stage builds unless re-declared. Each stage starts fresh.
- `docker compose up` reuses existing containers. After changing `Dockerfile`, you need `docker compose up --build` or `docker compose build` first.
- Volume mounts override the container's filesystem — if your `node_modules` are built inside the container but you mount `.:/app`, the host's (possibly empty) `node_modules` shadows them. Use a named volume for `node_modules`.
- `EXPOSE` is documentation only — it does NOT publish the port. You still need `-p 8080:8080` or `ports:` in compose.
- Docker's default bridge network does NOT provide DNS resolution between containers. Use a custom network or compose's default network.

## References

| When you need... | Read |
|------------------|------|
| Dockerfile patterns, CMD vs ENTRYPOINT | [dockerfile.md](./references/dockerfile.md) |
| Compose services, networks, volumes | [compose.md](./references/compose.md) |
| Security hardening | [security.md](./references/security.md) |
| Production deployment | [production.md](./references/production.md) |
