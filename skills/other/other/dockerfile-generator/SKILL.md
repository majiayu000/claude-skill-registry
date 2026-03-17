---
name: dockerfile-generator
type: complex
depth: extended
description: >-
  Generates production-ready multi-stage Dockerfiles and .dockerignore files with BuildKit features, pnpm monorepo support, OCI labels, and security hardening.
  Use when creating or writing Dockerfiles for Node.js, Python, Go, Java, or Rust. Does not validate (use dockerfile-validator).
---

# [H1][DOCKERFILE-GENERATOR]
>**Dictum:** *Structured generation produces secure, minimal container images.*

<br>

Docker Engine 27+ | BuildKit 0.27+ | Dockerfile syntax 1.14 | Node 24 LTS Krypton | Alpine 3.23

**Tasks:**
1. Gather requirements -- language, version, framework, entry point, package manager
2. Read [dockerfile_knowledge.md](./references/dockerfile_knowledge.md) -- Generation patterns and language substitution
3. (framework research) Query context7 MCP or WebSearch for `"<framework> <version> dockerfile production 2026"`
4. Generate Dockerfile -- Apply universal template with language-specific substitution
5. Generate .dockerignore -- See exemplar at `examples/example.dockerignore`
6. Validate -- Invoke dockerfile-validator (hadolint + Checkov + custom)
7. Iterate -- Fix, re-validate, repeat (max 3 iterations)

**Scope:**
- *Generation:* Dockerfiles for Node.js (pnpm/npm), Python (uv), Go, Java, Rust
- *Orchestration:* docker-bake.hcl for monorepo multi-target builds
- *Not:* Validation (use dockerfile-validator), building/running containers, debugging

---
## [1][REQUIREMENTS]
>**Dictum:** *Complete requirements prevent generation rework.*

<br>

**Guidance:**<br>
- `Language` -- Language, version, framework, entry point, package manager (pnpm/npm/uv/go mod/maven/gradle)
- `Build` -- Build commands, Nx target (monorepo), compilation flags, system deps.
- `Runtime` -- Port(s), env vars, health endpoint, image size constraints, multi-arch (amd64/arm64).

**Best-Practices:**<br>
- **Base images (February 2026):** `node:24-slim-trixie` (pnpm), `node:24-alpine3.23` (npm), `python:3.14-slim-trixie`, `golang:1.24-alpine3.23`, `rust:1.84-slim-trixie`, `eclipse-temurin:21-jdk-alpine`
- **Chainguard:** `cgr.dev/chainguard/node:latest-dev` (build) / `cgr.dev/chainguard/node:latest` (runtime) -- daily CVE rebuilds, zero known vulnerabilities

[REFERENCE]: [→dockerfile_knowledge.md](./references/dockerfile_knowledge.md) -- Generation patterns, language substitution, cache mounts.

---
## [2][MANDATORY_FEATURES]
>**Dictum:** *Every generated Dockerfile includes these features.*

<br>

**Guidance:**<br>
- `Syntax` -- `# syntax=docker/dockerfile:1` as first line (enables BuildKit frontend).
- `Multi-stage` -- Named stages: `deps`, `build`, `runtime` (minimum).
- `Security` -- Non-root `USER 1001:1001`, no secrets in ENV/ARG, exec-form ENTRYPOINT.

**Best-Practices:**<br>
- **BuildKit mounts:** `--mount=type=cache` for all pkg managers, `--mount=type=secret,id=key,env=VAR` for build secrets
- **Layer optimization:** `COPY --link` on every COPY, `COPY --chmod=555` (no extra RUN chmod layer), heredoc `RUN <<EOF` for multi-line scripts
- **Metadata:** OCI labels (`org.opencontainers.image.title/source/licenses/revision/created/version`), Pulumi-injectable ARGs (`GIT_SHA`, `BUILD_DATE`, `IMAGE_VERSION`)
- **Runtime:** `HEALTHCHECK` with `--start-interval=2s` (exec-form CMD), `STOPSIGNAL SIGTERM`, non-privileged ports (>1024)

---
## [3][PNPM_MONOREPO]
>**Dictum:** *This project uses pnpm monorepo with Nx build orchestration.*

<br>

**Guidance:**<br>
- `Fetch-first` -- `pnpm fetch --frozen-lockfile` downloads to store without installing (maximizes cache hits).
- `Deploy` -- `pnpm deploy --filter=@scope/app --prod /prod/app` extracts standalone prod deployment.

**Best-Practices:**<br>
- **corepack:** `RUN corepack enable` (no global pnpm install)
- **Offline install:** `pnpm install --frozen-lockfile --offline --ignore-scripts`
- **Selective copy:** Only needed `packages/*/package.json` files (not entire workspace)
- **Base image:** `node:24-slim-trixie` (glibc, Debian 13 -- not alpine for musl compat)
- **Exemplar:** `apps/api/Dockerfile` is the production reference

[REFERENCE]: [→dockerfile_knowledge.md](./references/dockerfile_knowledge.md) -- pnpm monorepo pattern, cache mount targets.

---
## [4][DELIVERABLES]
>**Dictum:** *Output quality measured by image size and security posture.*

<br>

| [INDEX] | [LANGUAGE]                | [ESTIMATED_SIZE] |
| :-----: | ------------------------- | :--------------: |
|   [1]   | **Node.js (slim-trixie)** |    80-200 MB     |
|   [2]   | **Python (slim-trixie)**  |    50-250 MB     |
|   [3]   | **Go (distroless)**       |     5-20 MB      |
|   [4]   | **Java (JRE)**            |    200-350 MB    |

**Deliverables:** Validated Dockerfile + .dockerignore + validation summary.

**Build command with attestations:**
```bash
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --sbom=true --provenance=mode=max \
    --build-arg GIT_SHA="$(git rev-parse HEAD)" \
    --build-arg BUILD_DATE="$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    -t myapp:latest --push .
```

---
## [5][SCRIPTS]
>**Dictum:** *CLI generation enables standalone Dockerfile creation.*

<br>

`scripts/generate.sh` -- Standalone CLI for Dockerfile generation.

```bash
./generate.sh nodejs -s @scope/app -p 4000          # pnpm monorepo
./generate.sh nodejs --standalone -p 3000           # standalone npm
./generate.sh python -p 8000 -e app.py              # Python with uv
./generate.sh golang --distroless -p 8080           # Go distroless
./generate.sh golang --scratch -p 8080              # Go scratch
./generate.sh java -t maven -p 8080                 # Java Maven
./generate.sh dockerignore -l nodejs                # .dockerignore only
```

---
## [6][VALIDATION]
>**Dictum:** *Gates prevent incomplete artifacts.*

<br>

[VERIFY] Completion:
- [ ] Syntax directive: `# syntax=docker/dockerfile:1` as first line
- [ ] Multi-stage: Named stages with minimal final base
- [ ] Security: Non-root USER, no secrets in ENV/ARG, exec-form ENTRYPOINT
- [ ] BuildKit: `COPY --link`, `--mount=type=cache`, heredoc RUN
- [ ] Metadata: OCI labels, Pulumi ARGs, STOPSIGNAL, HEALTHCHECK with `--start-interval`
- [ ] dockerfile-validator invoked and all issues resolved

**Integration:**
- **dockerfile-validator** -- Validates generated Dockerfiles (REQUIRED)
- **k8s-generator** -- Kubernetes deployments for the container
- **pulumi-k8s-generator** -- Pulumi K8s resources with the container image
