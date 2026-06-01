---
name: docker
description: >
  · Write/review Dockerfiles, Compose, OCI/Podman/BuildKit builds, signing, hardening. Triggers: 'docker', 'dockerfile', 'podman', 'buildkit', 'buildah', 'skopeo', 'containerd'. Not for K8s manifests (use kubernetes).
license: MIT
compatibility: "Requires docker or podman. Optional: docker compose, buildkit, cosign, trivy"
paths:
  - "Dockerfile*"
  - "compose*.y*ml"
  - "docker-compose*.y*ml"
  - ".dockerignore"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-24"
  effort: high
  argument_hint: "[dockerfile-or-compose-or-task]"
---

# Docker & Containers: Production Infrastructure

Write, review, and architect Dockerfiles, Compose stacks, and container workflows - from single-service dev setups to multi-arch production pipelines with image signing and compliance gates. The goal is minimal, secure, reproducible images that a team can maintain and a QSA can audit.

**Target versions**: May 2026 snapshot. Read `references/target-versions.md` before
pinning Docker, Compose, BuildKit, containerd, Podman, Buildah, or runc.

This skill covers Dockerfiles, Compose, container hardening, supply chain, registry/CI
patterns, and runtime migration across Docker, Podman, Buildah, Skopeo, and containerd.

## When to use

- Writing or reviewing Dockerfiles (single or multi-stage)
- Setting up Docker Compose stacks (dev, staging, production)
- Optimizing image size, build speed, or layer caching
- Hardening containers for production or compliance
- Setting up image signing, SBOM generation, or vulnerability scanning
- Containerizing AI/ML workloads (Model Runner, GPU passthrough, model serving)
- Migrating from Docker to Podman or building with Buildah
- Reviewing container security posture for PCI-DSS 4.0 or SOC 2
- Troubleshooting container networking, volume, or build issues
- Using `docker init` to scaffold a new project

## When NOT to use

- Kubernetes manifests, Helm charts, cluster architecture (use **kubernetes**)
- CI/CD pipeline design (use **ci-cd**)
- Security audits of application code (use **security-audit**)
- Infrastructure provisioning with Terraform (use **terraform**)

## AI Self-Check

AI tools consistently produce the same Docker mistakes. **Before returning any generated Dockerfile or Compose file, verify against this list:**

- [ ] Multi-stage build used when the app has a build step (TypeScript, Go, Rust, Java, C/C++)
- [ ] Dependencies copied and installed BEFORE source code (layer caching)
- [ ] Final image is slim/distroless/scratch - no build tools, no package caches
- [ ] `USER` directive present - container does NOT run as root
- [ ] No secrets in `ENV`, `ARG`, or `COPY` - use `--mount=type=secret` or runtime injection
- [ ] Base image pinned to specific version or SHA256 digest (never `:latest` except Chainguard free tier, never bare `:22`)
- [ ] `HEALTHCHECK` present for production images
- [ ] `.dockerignore` exists and excludes `.git`, `node_modules`, `.env`, `__pycache__`, etc.
- [ ] No `ADD` for local files (use `COPY` - `ADD` auto-extracts and fetches URLs)
- [ ] Compose: no `version:` field (deprecated since Compose v2, removed in spec v5)
- [ ] Compose: `depends_on` uses `condition: service_healthy`, not bare ordering
- [ ] Compose: resource limits set on production services
- [ ] Package caches cleaned in same layer: `--no-cache` (apk), `rm -rf /var/lib/apt/lists/*` (apt). For pip: use `--mount=type=cache` OR `--no-cache-dir`, not both.
- [ ] CMD uses exec form (JSON array), not shell form: `CMD ["node", "app.js"]` not `CMD node app.js`
- [ ] **HEALTHCHECK uses available tools**: probe command uses a binary present in the final image (wget in Alpine, curl in Debian, none in scratch/distroless - use the app's own health endpoint)
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Engine/Compose syntax checked**: Dockerfile, Compose, BuildKit, and runtime flags match the installed versions
- [ ] **Image provenance considered**: base images, registries, tags, SBOMs, and signatures are handled where risk warrants

## Performance

- Order Dockerfile layers from stable to volatile and use cache mounts for package-manager caches where BuildKit is available.
- Keep build contexts small with `.dockerignore`; accidental monorepo contexts dominate build time.
- Use multi-stage builds and slim runtime images, but measure startup and debug needs before stripping tools aggressively.

## Best Practices

- Pin base image digests for sensitive workloads and track rebuild cadence for security updates.
- Run as non-root and drop capabilities unless the workload genuinely needs them.
- Preview prune and volume-removal commands; persistent data must never be collateral cleanup.

## Workflow

### Step 1: Determine the domain

Based on the request:
- **"Write a Dockerfile" / "containerize this app"** -> Dockerfile
- **"Set up docker compose" / "multi-service stack"** -> Compose
- **"Harden this" / "make PCI compliant" / "scan for vulnerabilities"** -> Security
- **"Sign images" / "generate SBOM" / "CI pipeline"** -> Registry & CI
- **"Use Podman" / "rootless containers" / "daemonless builds"** -> Runtimes
- **"Review this Dockerfile/compose"** -> Apply production checklist + AI self-check

### Step 2: Gather context

Before writing anything, determine:
- **Application type**: language, framework, build system
- **Runtime**: Bun, Node.js, Python, Go, Rust, Java - determines base image and build pattern
- **Environment**: dev (hot reload, debug) vs production (minimal, hardened)
- **Base image**: Alpine (small, musl) vs Debian-slim (glibc compat) vs distroless (no shell) vs Chainguard (zero-CVE) vs scratch (static binaries)
- **Secrets**: how are they injected? (env vars, mounted files, Docker secrets, vault)
- **Compliance**: PCI CDE? Regulated? What scanning/signing is required?
- **Target registry**: Docker Hub, GHCR, private registry, OCI-compliant?
- **AI/ML**: GPU workload? Model serving? Docker Model Runner?

### Step 3: Build

Follow the domain-specific section below. Always apply the production checklist (Step 4) and AI self-check before finishing.

### Step 4: Validate

```bash
# Dockerfile
docker build --no-cache -t test-build .
docker history test-build --format "{{.Size}}\t{{.CreatedBy}}" | head -15
docker scout quickview test-build     # vulnerability overview
docker scout cves test-build          # detailed CVE list

# Compose
docker compose config                 # validate and render
docker compose --dry-run up           # dry-run startup (Compose v5)

# Security
docker scout cves --only-severity critical,high <image>
cosign verify --key <key> <image>     # verify signature
syft <image> -o spdx-json             # generate SBOM
grype <image>                         # vulnerability scan (alternative to Scout)
trivy image <image>                   # use v0.70.0+; never v0.69.4-6
```

## Dockerfile

Read `references/dockerfile-patterns.md` for complete, production-ready Dockerfile templates (Node.js/Bun, Python, Go, Rust, static site) and BuildKit syntax reference.

### Base image selection

- Need a shell or package manager: use slim Debian or Ubuntu bases.
- Need the smallest static runtime: use distroless or `scratch`.
- Need a hardened minimal userspace: use Chainguard or another verified Wolfi-style base.
- Keep builders and runtimes separate; `golang`, `rust`, and other heavy toolchain images stay in build stages only.

See `references/dockerfile-patterns.md` for the actual language-by-language base recommendations and templates.

### Key patterns

**Multi-stage builds** - the non-negotiable pattern for any compiled or transpiled language:

```dockerfile
# syntax=docker/dockerfile:1
FROM node:22-slim AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .
RUN npm run build && npm prune --omit=dev

FROM gcr.io/distroless/nodejs22-debian12
WORKDIR /app
COPY --from=build --chown=1001:1001 /app/dist ./dist
COPY --from=build --chown=1001:1001 /app/node_modules ./node_modules
USER 1001
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["node", "-e", "fetch('http://localhost:3000/health').then(r=>r.ok||process.exit(1)).catch(()=>process.exit(1))"]
CMD ["dist/index.js"]
```

**BuildKit features** (require `# syntax=docker/dockerfile:1` or `DOCKER_BUILDKIT=1`):

- **Cache mounts**: `RUN --mount=type=cache,target=/root/.npm npm ci` - persists package cache across builds, up to 70% faster rebuilds
- **Secret mounts**: `RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci` - secrets never baked into layers
- **Heredocs**: multi-line scripts without backslash hell

```dockerfile
RUN <<EOF
set -e
apt-get update
apt-get install -y --no-install-recommends ca-certificates
rm -rf /var/lib/apt/lists/*
EOF
```

- **`--check` flag**: `docker build --check .` validates Dockerfile without building (dry-run lint)
- **SLSA provenance**: `docker build --provenance=true --sbom=true .` attaches attestations

**`docker init`**: scaffolds Dockerfile + compose.yaml + .dockerignore. Good starting point, always review.

### What NOT to write

- `COPY . .` before dependency install (busts cache on every source change)
- `ADD` for local files (use `COPY` - `ADD` is only for auto-extracting `.tar.gz` archives into the image)
- `MAINTAINER` (deprecated - use `LABEL maintainer="..."`)
- `RUN cd /dir && ...` (use `WORKDIR /dir`)
- Separate `RUN` for each package install (chain with `&&`)
- `chmod 777` on anything
- Secrets in `ARG` or `ENV`
- `FROM node:latest` or `FROM python` (unpinned)
- `ENTRYPOINT` + `CMD` together unless ENTRYPOINT is the binary and CMD is overridable default args (e.g., `ENTRYPOINT ["/app"]` + `CMD ["--config", "/etc/app.yaml"]`)

## Compose

Read `references/compose-patterns.md` for complete Compose v5 templates (web+db, dev override, production hardened, AI/ML stack) and network/volume patterns.

### Compose v5

- Do not use the old `version:` field.
- Expect Bake-based builds, `watch`, dry-run validation, and newer model-oriented service wiring.
- Keep dev and prod concerns separate; override files are still the sane default.
- Treat healthchecks and dependency readiness as normal Compose design, not optional extras.

### Key patterns

**Dev/prod separation** with override files:

```yaml
# compose.yaml (base)
services:
  app:
    image: myapp:1.0.0
    healthcheck:
      test: ["CMD-SHELL", "wget -qO /dev/null http://localhost:3000/health || exit 1"]
      interval: 30s
      timeout: 5s
      start_period: 10s
      retries: 3

# compose.override.yaml (dev - auto-loaded)
services:
  app:
    build: .
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      NODE_ENV: development
    ports:
      - "9229:9229"
    command: bun run dev
```

**Secrets**: use top-level `secrets:` with `file:` or `external: true`, reference via `_FILE` env convention (e.g., `POSTGRES_PASSWORD_FILE: /run/secrets/db_pass`). Never hardcode secrets in `environment:`. See `references/compose-patterns.md` for the full template with secret wiring.

**Health-gated dependencies**: always use `depends_on:` with `condition: service_healthy` - bare `depends_on` is ordering only, no readiness guarantee.

### Compose anti-patterns

- `version: "3.8"` - dead field, remove it
- `container_name` on every service (breaks `docker compose up --scale`)
- `restart: always` without healthcheck (infinite restart of broken containers)
- `network_mode: host` when port mapping works (replace with a user-defined bridge network and explicit `ports:` mapping)
- `depends_on` without `condition:` (ordering only, no readiness)
- `volumes:` mounting entire project dir in production (dev pattern leak)
- `privileged: true` on a compose service instead of the host LXC
- 20+ inline `environment:` entries (use `env_file:`)

## Security

Read `references/security-and-compliance.md` for the full PCI-DSS 4.0 container requirements mapping, CVE reference, runtime hardening patterns, and scanning tool comparison.

### Critical vulnerabilities (2025-2026)

| CVE | Component | Severity | Impact | Fixed in |
|-----|-----------|----------|--------|----------|
| CVE-2025-9074 | Docker Desktop | 9.3 Critical | Container escape via unauthenticated Engine API | Desktop 4.44.3 |
| CVE-2025-31133 | runc | High | Container escape via /dev/null symlink race | runc 1.2.8, 1.3.3, 1.4.0-rc.3 |
| CVE-2025-52565 | runc | High | Container escape via /dev/console mount race | runc 1.2.8, 1.3.3, 1.4.0-rc.3 |
| CVE-2025-52881 | runc | High | Host procfs writes via /proc redirect (DoS/escape) | runc 1.2.8, 1.3.3, 1.4.0-rc.3 |
| CVE-2026-33634 | Trivy | Critical | Supply chain - malware in Docker Hub images (v0.69.4-6) | Trivy v0.70.0+ for new pins; v0.69.3 only as rollback |
| CVE-2026-2664 | Docker Desktop | Medium | gRPC-FUSE kernel module OOB read | Desktop 4.62.0+ |
| CVE-2025-13743 | Docker Desktop | Low | Expired Hub PATs leaked in diagnostics bundles | Desktop 4.54.0 |
| CVE-2026-28400 | Model Runner | 7.5 High | Runtime flag injection - arbitrary file overwrite, container escape | Desktop 4.61.0+ |
| CVE-2026-5843 | Model Runner (MLX) | 8.8 High | Container-to-host code execution via MLX-LM `model_file` importlib load from untrusted models | Desktop 4.71.0+ |
| CVE-2026-5817 | Model Runner (vllm-metal) | 8.8 High | Container-to-host RCE via unsandboxed `trust_remote_code` tokenizer load | Desktop 4.68.0+ |
| CVE-2026-33747 | BuildKit | High | Malicious frontend file escape outside storage root | BuildKit v0.28.1 |
| CVE-2026-33748 | BuildKit | High | Git URL validation bypass - restricted file access | BuildKit v0.28.1 |

**Action items**: upgrade runc to >= 1.4.0, BuildKit to >= 0.28.1, Docker Desktop to >= 4.66.1, never pull Trivy v0.69.4/5/6. Pin ALL CI tool images to SHA256 digests.

### Hardened Compose baseline

Every production service should start from this, relax only what's needed:

```yaml
services:
  app:
    image: myapp:1.0.0          # pinned, never :latest
    read_only: true
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add: []                 # add ONLY what's needed (see note below)
    tmpfs:
      - /tmp
    user: "1001:1001"
    healthcheck:
      test: ["CMD-SHELL", "wget -qO /dev/null http://localhost:8080/health || exit 1"]
      interval: 30s
      timeout: 5s
      start_period: 15s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

**`cap_drop: ALL` warning**: many images (LSIO, HOTIO, official redis/postgres, anything using
gosu/setpriv/su-exec) start as root and drop privileges at runtime. They need at minimum
`cap_add: ["SETUID", "SETGID"]`, and images that chown files at startup also need `"CHOWN"`.
Always read the image's entrypoint to determine required capabilities before applying blanket
drops. Blind `cap_drop: ALL` with empty `cap_add` causes CrashLoopBackOff. See the
security-audit skill's "No blanket capability drops" rule for detailed guidance.

For a hardened Dockerfile pattern, see `references/dockerfile-patterns.md` (Language Templates section).

### Supply chain security

- **Sign images** with cosign (Sigstore): `cosign sign --key cosign.key <image>@<digest>`
- **Generate SBOMs** at build time: `docker scout sbom <image>` or `syft <image> -o spdx-json`
- **Verify at deploy**: `cosign verify --key cosign.pub <image>@<digest>`
- **Pin CI tool images to SHA256 digests.** Mutable tags are a proven attack vector (Trivy March 2026, tj-actions/reviewdog March 2025).
- **Use Docker Scout** or Grype for continuous vulnerability monitoring.
- **Trivy**: use v0.70.0+ from official releases for new pins. v0.69.3 was the March 2026 rollback version. v0.69.4-6 contained credential-stealing malware. If any CI pipeline ran compromised Trivy between March 19-23, 2026, rotate ALL secrets.

### PCI-DSS 4.0 container requirements (summary)

PCI-DSS 4.0 is the only active version. Key container-specific requirements:

- **Req 1**: Network segmentation - use user-defined bridge networks, `internal: true` for backend services, never expose CDE containers on default bridge
- **Req 2.2**: Harden containers - non-root, drop caps, read-only rootfs, one process per container
- **Req 4**: Encrypt transmissions - TLS between CDE containers in Compose (mount certs, use TLS-enabled images, or front with a TLS-terminating reverse proxy)
- **Req 5.2/5.3**: Immutable images (deploy by digest), Falco for runtime detection
- **Req 6.3**: Vulnerability scanning on every image before deployment (Docker Scout, Grype, Trivy v0.70.0+)
- **Req 6.3.2**: SBOM for every production image
- **Req 8.6.2**: No hardcoded secrets in images, compose files, or env vars
- **Req 10**: Audit logging - container stdout/stderr to immutable log store
- **Req 11.5**: Image digest pinning + Falco = FIM for containers

Full mapping in `references/security-and-compliance.md`.

## Registry & CI

### CI pipeline pattern

- Build with `docker build --check` first, then `buildx` with provenance and SBOM output.
- Scan before deploy, sign by digest, and keep an SBOM artifact even if the registry also stores one.
- Pin CI-side tools and actions to immutable digests, not mutable tags.

### Docker Model Runner (AI/ML)

Docker Model Runner (Engine 29.x, Desktop 4.50+) serves AI models via OpenAI/Ollama-compatible APIs:

```yaml
# Compose integration with Model Runner
services:
  model:
    provider:
      type: model
      options:
        model: ai/llama3.2:3B-Q4_K_M
  agent:
    build: .
    environment:
      OPENAI_BASE_URL: http://model/v1
```

GPU containers: use `deploy.resources.reservations.devices` with `capabilities: [gpu]`. Start `shm_size` at `16gb` for single GPU, `32gb` for multi-GPU (vLLM needs shared memory for tensor ops). See `references/compose-patterns.md` for the full AI/ML stack template.

## Production Checklist

See AI Self-Check above for the full build-time checklist (Dockerfile correctness, Compose structure, layer caching, secrets, non-root user, healthchecks, base image pinning). The items below cover deploy-time and operational additions only.

### Deploy-time additions

- [ ] runc >= 1.4.0 (CVE-2025-31133/52565/52881 patched)
- [ ] BuildKit >= 0.28.1 (CVE-2026-33747/33748 patched)
- [ ] Docker Desktop >= 4.71.0 (adds CVE-2026-5817/5843 Model Runner container-to-host RCE fixes; floor was 4.66.1 for CVE-2025-9074/CVE-2026-28400)
- [ ] Trivy v0.70.0+ from official releases (v0.69.4-6 COMPROMISED)
- [ ] Images signed with cosign, verified at deploy
- [ ] SBOM generated for every production image
- [ ] Vulnerability scanning in CI (Docker Scout, Grype, or Trivy v0.70.0+)
- [ ] CI tools pinned to SHA256 digests (not mutable tags)
- [ ] Base images rebuilt/updated regularly (weekly minimum)
- [ ] Separate override files for dev/prod
- [ ] Logging config with rotation (`max-size`, `max-file`)
- [ ] `read_only: true` + `no-new-privileges` + `cap_drop: ALL` on production services

### Compliance (PCI-DSS 4.0)

- [ ] Containers run as non-root with minimal capabilities (Req 2.2)
- [ ] Read-only root filesystem, one process per container (Req 2.2)
- [ ] Images scanned for vulnerabilities before deployment (Req 6.3)
- [ ] SBOM generated for every CDE image (Req 6.3.2)
- [ ] No hardcoded secrets in images or compose files (Req 8.6.2)
- [ ] Image digests pinned for immutability (Req 5/11.5)
- [ ] Container logs shipped to immutable SIEM (Req 10)
- [ ] Runtime detection in place (Falco/Tetragon) (Req 5.2/5.3)
- [ ] Registry access audit-logged (Req 10.4.1.1)
- [ ] Base images from trusted, verified sources (Req 6.2.1)

## Reference Files

- `references/dockerfile-patterns.md` - Dockerfile templates and build patterns
- `references/compose-patterns.md` - Compose patterns and common stack layouts
- `references/security-and-compliance.md` - container hardening, compliance guidance, and safe public custom image publishing
- `references/alternative-runtimes.md` - Podman, Buildah, Skopeo, and related runtime patterns
- `references/target-versions.md` - May 2026 version snapshot for Docker, Compose, BuildKit, containerd, Podman, Buildah, and runc

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** DOCKER
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/docker/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **kubernetes** - for deploying containers to K8s clusters. Docker builds the image;
  kubernetes deploys it. Dockerfile optimization belongs here; K8s manifests belong there.
- **ci-cd** - for pipeline design that builds and pushes images. Docker skill covers the
  Dockerfile and Compose patterns; ci-cd covers the pipeline stages around them.
- **security-audit** - for auditing container images, scanning for CVEs, and supply chain
  risks. Docker skill covers hardening best practices; security-audit runs the actual audit.
- **ansible** - can manage containers via `community.docker`, but image building and Compose
  design belong here.
- **databases** - for database containers in Docker Compose. Docker skill owns the Compose
  pattern; databases skill owns the engine tuning within the container.
- **git** - for git tags and version control. Docker skill handles container image tagging;
  git handles git tags and release workflows.

## Rules

1. **No `:latest` tags in production.** Pin images to a specific version or SHA256 digest.
2. **Multi-stage builds for compiled/transpiled languages.** Build tools do not belong in production images.
3. **Non-root user.** Every production container must run as non-root (numeric UID for K8s compat).
4. **No secrets in layers.** Not in `ENV`, not in `ARG`, not in `COPY`. Use `--mount=type=secret` or runtime injection.
5. **Deps before source.** Copy dependency manifests first, install, then copy source. Layer cache depends on it.
6. **Healthchecks on everything.** Dockerfile `HEALTHCHECK` and Compose `healthcheck:`.
7. **Pin CI tools to SHA256 digests.** Mutable tags are compromised supply chain vectors (Trivy CVE-2026-33634 March 2026, tj-actions CVE-2025-30066 (upstream: reviewdog CVE-2025-30154) March 2025).
8. **Trivy v0.70.0+ for new pins.** v0.69.3 was the March 2026 rollback version; v0.69.4-6 contained credential-stealing malware. If you ran it, rotate secrets.
9. **Compose: no `version:` field.** It's deprecated and removed. Just delete it.
10. **Clean apt cache in the same RUN layer.** `apt-get update && apt-get install -y ... && rm -rf /var/lib/apt/lists/*` - all one `RUN`.
11. **`.dockerignore` is not optional.** `.git`, `node_modules`, `.env`, secrets, test fixtures, docs - all excluded.
12. **Resource limits on production containers.** Memory and CPU limits prevent noisy neighbors and OOM cascading.
13. **Run the AI self-check.** Every generated Dockerfile/Compose gets verified against the checklist above before returning.
