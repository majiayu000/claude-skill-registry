---
name: ci-cd
description: >
  · Write/review CI/CD for GitHub Actions, GitLab, Forgejo/Gitea, Woodpecker. Triggers: 'ci/cd', 'pipeline', 'github actions', 'gitlab ci', 'runner', 'renovate', 'trivy'. Not for git workflows (use git).
license: MIT
compatibility: "Optional: gh (GitHub CLI), glab (GitLab CLI), fj (Forgejo CLI)"
paths:
  - ".github/workflows/*.yml"
  - ".gitlab-ci.yml"
  - ".forgejo/workflows/*.yml"
  - ".gitea/workflows/*.yml"
  - ".woodpecker/*.yaml"
  - ".woodpecker.yaml"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-24"
  effort: high
  argument_hint: "[platform-or-workflow]"
---

# CI/CD Pipelines: Multi-Platform Production Infrastructure

Write, review, and architect CI/CD pipelines across GitHub Actions, GitLab CI/CD, Forgejo
Actions, Gitea Actions, and Woodpecker. The goal is secure, fast, auditable pipelines that
satisfy both engineering needs and compliance requirements (PCI-DSS 4.0).

**Target versions**: May 2026 snapshot. Read `references/target-versions.md` before
pinning forge, runner, CI, or supply-chain tool versions.

This skill covers workflow design, security, compliance, cross-platform migration,
runners, dependency updates, scanning, review gates, and rollout order.

## When to use

- Writing or reviewing CI/CD pipeline configs (GitHub/Forgejo/Gitea Actions, `.gitlab-ci.yml`, `.woodpecker/*.yaml`)
- Designing pipeline architecture (stages, parallelism, caching, deployment strategies)
- Hardening pipelines against supply chain attacks (SHA pinning, image signing, provenance)
- Setting up security scanning in CI (SAST, SCA, container scanning, secret detection)
- Configuring runners (install, register, executor choice, hardening) - see `references/runners.md`
- Setting up caching strategies or artifact management
- PCI-DSS 4.0 compliance for CI/CD (Req 6.2.1, 6.2.4, 6.3.2, 6.4.2, 6.5.3)
- Migrating pipelines between platforms (GitLab -> GitHub, GitHub -> Forgejo)
- Troubleshooting failed pipelines, flaky jobs, or runner issues

## When NOT to use

- Kubernetes manifests, Helm charts, cluster architecture - use **kubernetes**
- Dockerfiles, Compose stacks, container image optimization - use **docker**
- Terraform/OpenTofu infrastructure-as-code - use **terraform**
- Ansible playbooks, configuration management - use **ansible**
- Security audits of application code (SAST findings, auth bugs) - use **security-audit**
- Code review of pipeline-adjacent code (the app itself) - use **code-review**
- The code-review skill has a `cicd-pipelines.md` reference for **bug patterns** in existing
  pipelines. This skill is for **writing and architecting** pipelines.

## AI Self-Check

AI tools consistently produce the same CI/CD mistakes. **Before returning any generated
pipeline config, verify against this list.**

**Review mode:** if auditing an existing pipeline rather than generating one, invert this
checklist - each item that fails is a finding. Work through the list top-to-bottom and report
every failure with file and line reference.

- [ ] **SHA pinning**: all third-party actions/images pinned to full commit SHA or digest, not mutable tags. Add `# vX.Y.Z` comment for readability.
- [ ] **Permissions**: explicit `permissions:` block on every GitHub Actions workflow (read-only default). GitLab: protected variables scoped correctly.
- [ ] **No secrets in config**: no hardcoded tokens, passwords, or API keys. Use CI/CD secret variables or vault integration.
- [ ] **No `latest` tags**: runner images, tool images, and base images pinned to specific versions or SHA256 digests.
- [ ] **Caching strategy**: dependencies cached correctly (lockfile-based keys), build outputs use artifacts (not cache).
- [ ] **Fail-fast security**: SAST, dependency scanning, and secret detection run early (not after deployment).
- [ ] **Manual gates for production**: production deployments require explicit approval (not auto-deploy on merge).
- [ ] **SBOM generation**: release pipelines generate and attach SBOMs (SPDX or CycloneDX). Required for PCI-DSS 4.0.
- [ ] **Minimal scope**: jobs have minimum required permissions, access only needed secrets, and run only needed steps.
- [ ] **No `allow_failure` without justification**: if a job can fail, explain why in a comment.
- [ ] **Version pinning on tools**: `node:22`, not `node:lts`. `python:3.13`, not `python:3`. Specific versions prevent silent breakage.
- [ ] **Trigger scoping**: `on: push` without branch/path filters runs on every push to every branch - scope to `branches: [main]` and/or `paths:` filters. Same for GitLab: `rules:` with `if` conditions, not bare `only: [pushes]`.
- [ ] **No expression injection** (GitHub Actions): `${{ }}` expressions never used directly in `run:` blocks. Assign to `env:` first. `github.event.*` is attacker-controlled. Avoid `github.ref_name` in security-sensitive contexts (injectable via crafted tag/branch names).
- [ ] **Self-hosted runners ephemeral on public/untrusted repos**: non-ephemeral shell runners on repos that accept outside PRs is the top self-hosted-runner compromise vector. Verify `--ephemeral` (GitHub, Gitea) or capacity-based single-job runners (Forgejo) + approval gates for outside contributors. See `references/runners.md`.
- [ ] **Docker socket mount scope**: `/var/run/docker.sock` mounted into a job gives it root on the host. Only acceptable for trusted internal pipelines. Public/shared runners need DinD sidecar or rootless buildkit instead.
- [ ] **Scan gate has a baseline, not a blanket block**: container/IaC/SAST scanners introduced with `exit-code 1` and zero suppression always get disabled. Use the ratchet pattern (non-blocking -> baseline -> block new only) from `references/best-practices.md`.
- [ ] **Ignore-list entries have expiry dates**: every `.trivyignore`, `.grype.yaml`, Dependabot `ignore`, or Renovate `ignoreDeps` entry includes a comment with revisit date + owner. No dates = zombie tech debt.
- [ ] **Lockfiles committed**: `package-lock.json`, `bun.lock`, `Cargo.lock`, `go.sum`, `uv.lock` belong in version control for applications. Manifest-only commits break reproducibility.
- [ ] **Auto-merge gated on tests, not just lint**: Dependabot/Renovate auto-merge without test coverage of the changed area is a supply-chain shortcut.
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Runner trust checked**: workflow advice distinguishes hosted, self-hosted, fork, and protected-branch execution
- [ ] **Mutable references controlled**: actions, images, includes, and templates are pinned where supply-chain risk matters

## Performance

- Key caches by lockfiles and toolchain versions; avoid broad caches that restore stale dependencies.
- Split quick lint/unit gates from slow integration, image, and deployment jobs.
- Use path filters and matrix limits to keep monorepo pipelines proportional to the change.

## Best Practices

- Use OIDC or short-lived federation for cloud deploys instead of long-lived static secrets.
- Keep pull-request workflows from forks read-only unless explicitly isolated.
- Generate provenance or attestations for release artifacts where the forge supports it.

## Workflow

### Step 1: Identify the platform

| Signal | Platform |
|--------|----------|
| `.github/workflows/*.yml` | GitHub Actions |
| `.gitlab-ci.yml` | GitLab CI/CD |
| `.forgejo/workflows/*.yml` | Forgejo Actions |
| `.gitea/workflows/*.yml` | Gitea Actions |
| `.woodpecker/*.yaml` or `.woodpecker.yaml` | Woodpecker (Gitea/Forgejo) |
| User says "work" / "gitlab" / `glab` | GitLab CI/CD |
| User says "home" / "forgejo" / `fj` | Forgejo Actions |
| User says "gitea" | Gitea Actions (or Woodpecker if 1.20 or older) |
| User says "github" / "ghcr" / `gh` | GitHub Actions |

If unclear, ask. The platforms have significant differences despite surface similarity.

### Step 2: Determine the domain

- **"Create a CI pipeline for my project"** -> Workflow design
- **"Harden my pipeline" / "pin actions"** -> Security
- **"Make this PCI compliant" / "SBOM"** -> Compliance
- **"Port this from GitLab to GitHub"** -> Cross-platform

### Step 3: Gather requirements

Before writing pipeline config:
- **What triggers the pipeline?** Push, PR/MR, tag, schedule, manual
- **What does it build?** Language, runtime, package manager, build tool
- **What does it test?** Unit, integration, e2e, linting, typechecking
- **Where does it deploy?** K8s, Docker registry, cloud, bare metal
- **What compliance requirements?** PCI-DSS, SOC 2, internal policies
- **Self-hosted or managed runners?** Affects available tools and caching

### Step 4: Apply platform-specific patterns

Read the appropriate reference file:
- **GitHub Actions**: `references/github-actions.md`
- **GitLab CI/CD**: `references/gitlab-ci.md`
- **Forgejo/Gitea Actions and Woodpecker**: `references/forgejo-gitea-actions.md`
- **Self-hosted runners** (all 5 implementations): `references/runners.md`
- **Best practices** (deps, linting, scanning, review gates, rollout): `references/best-practices.md`
- **Supply chain / compliance**: `references/supply-chain.md`

For **Forgejo CI/CD**, see the Forgejo section below (smaller scope, inline).

### Step 5: Verify against AI Self-Check

Run through the checklist above before returning any generated config.

## Cross-Platform Patterns

### Stage ordering (all platforms)

```
lint -> test -> build -> scan -> deploy
```

1. **Lint** first - fastest feedback, catches formatting/syntax early
2. **Test** - unit tests, typechecking
3. **Build** - compile, bundle, create artifacts
4. **Scan** - SAST, dependency audit, container scan (on build output)
5. **Deploy** - staging auto, production manual

### Caching strategy

| What | Cache key | Platform notes |
|------|-----------|----------------|
| **npm/bun** | `${{ hashFiles('**/package-lock.json') }}` or lockb | GH: `actions/cache`. GL: `cache:key:files`. Forgejo: same as GH. |
| **pip** | `${{ hashFiles('**/requirements*.txt') }}` | GH: `setup-python` with `cache: pip`. GL: cache `~/.cache/pip`. |
| **poetry** | `${{ hashFiles('**/poetry.lock') }}` | GH: `setup-python` with `cache: poetry`. GL: cache `~/.cache/pypoetry`. |
| **uv** | `${{ hashFiles('**/uv.lock') }}` | GH: `astral-sh/setup-uv` has built-in cache. GL: cache `~/.cache/uv`. |
| **Go** | `${{ hashFiles('**/go.sum') }}` | GH: `actions/setup-go` has built-in cache. |
| **Docker layers** | BuildKit cache mount or registry cache | GH: `--cache-from type=gha`. GL: `--cache-from $CI_REGISTRY_IMAGE:cache`. |

**Rule**: cache is a speed optimization, not a correctness mechanism. Artifacts are for
inter-job data. Cache may evict at any time - pipelines must work without it.

### Secret management

| Platform | Mechanism | Scope control |
|----------|-----------|---------------|
| **GitHub** | Repository/org/environment secrets | Per-environment, per-repo, per-org. Deployment branches. |
| **GitLab** | CI/CD variables (project/group/instance) | Protected branches/tags, environments, masked in logs. |
| **Forgejo** | Repository/org secrets | Per-repo, per-org. No environment scoping yet. |

**All platforms**: never echo secrets, never pass as CLI args (visible in `ps`), never write
to artifacts. Use environment variables or file-based injection.

### Deployment gates

| Environment | Trigger | Approval |
|-------------|---------|----------|
| **Dev/Preview** | Every PR/MR push | None |
| **Staging** | Merge to main | None (auto-deploy) |
| **Production** | Tag or manual dispatch | Required reviewer(s) |

GitLab: `when: manual` + `environment:`. GitHub: `environment:` with protection rules.
Forgejo: manual dispatch (`workflow_dispatch`).

## Monorepo Patterns

When a repo contains multiple services sharing a common library:

### Path-based triggering
- **GitHub Actions**: `on.push.paths` / `on.pull_request.paths` to scope workflows per service
- **GitLab CI/CD**: `rules: changes: paths:` with `compare_to: refs/heads/main`
- **Forgejo**: same as GitHub Actions (`on.push.paths`)

### Shared library detection
If `libs/common/` changes, rebuild all services that depend on it:
- List dependent services in a matrix or trigger all service workflows
- `paths` filters accept globs: `paths: ['services/api/**', 'libs/common/**']`

### Selective builds
Build only what changed. Two approaches:
1. **Per-service workflows** with `paths:` filters (simplest, recommended)
2. **Single workflow with matrix** + change detection job that outputs which services need building

**Rule**: always rebuild when the shared lib changes. A "nothing changed" optimization that misses a shared dependency is worse than rebuilding everything.

### Python monorepo specifics (GitLab / GitHub / Forgejo)

For Python monorepos with multiple services sharing a common library (`libs/common/`):
- **Cache the resolver output, not the install step.** Key on `hashFiles('**/requirements*.txt')` or `**/poetry.lock`/`**/uv.lock`. With `uv` or `pip`, cache `~/.cache/uv` or `~/.cache/pip` plus each service's `.venv/` keyed on the service path + lockfile hash.
- **Install the shared lib editable** (`pip install -e libs/common`) so services import the in-repo version, not a stale wheel.
- **Scope jobs per service with path filters.** GitLab: `rules: - changes: paths: ['services/api/**', 'libs/common/**'] compare_to: refs/heads/main`. GitHub/Forgejo: `on.push.paths` / `on.pull_request.paths`. Always include `libs/common/**` in every service's filter so a shared-lib change triggers all services.
- **YAML anchors (GitLab) / reusable workflows (GitHub) for the per-service job template.** Three near-identical blocks for `api`, `worker`, `scheduler` is a maintenance trap.

See `references/gitlab-ci.md` for a full monorepo `.gitlab-ci.yml` (YAML anchors, `compare_to`, per-service change rules, shared-lib detection).

## Forgejo CI/CD

Forgejo Actions is "designed to be familiar, not designed to be compatible" with GitHub Actions.
It reuses the workflow syntax but makes no compatibility guarantees.

### Key differences from GitHub Actions

| Feature | GitHub Actions | Forgejo Actions |
|---------|---------------|-----------------|
| **`permissions:`** | Controls GITHUB_TOKEN scope | **Not enforced** - token always has full rw (read-only for fork PRs) |
| **`continue-on-error:`** (job level) | Allows job failure without failing workflow | **Not supported** - step-level only |
| **Runner images** | Managed `ubuntu-24.04` with 200+ tools | Self-hosted, typically lean Debian/Alpine |
| **Action resolution** | `actions/checkout@v4` -> github.com | Resolves from Forgejo mirror (configurable) |
| **OIDC** | `permissions: id-token: write` | `enable-openid-connect` key |
| **Workflow call defaults** | `inputs.<id>.default` populated | **Always empty** |
| **Matrix + dynamic runs-on** | Supported | Supported since v14.0 |
| **LXC execution** | Not supported | Supported (Forgejo-specific) |

### Forgejo workflow template

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    runs-on: docker                    # self-hosted runner label
    container:
      image: oven/bun:1.2             # pin to minor version minimum
    steps:
      - uses: actions/checkout@<sha>  # pin to SHA; resolves from Forgejo mirror
      - run: bun install --frozen-lockfile
      - run: bun run lint
      - run: bun run typecheck
      - run: bun run test
```

### Forgejo action SHA discovery

Forgejo resolves actions from its own mirror or a configured upstream, not from github.com.
Finding the correct SHA for a self-hosted mirror requires different steps than GitHub.

**Find the SHA on your Forgejo instance**:
```bash
# List tags and their SHAs from the Forgejo mirror
git ls-remote https://forgejo.example.com/actions/checkout.git 'refs/tags/v4*'

# Or use the Forgejo API to get a tag's commit SHA
curl -s https://forgejo.example.com/api/v1/repos/actions/checkout/git/refs/tags/v4.2.2 \
  | jq -r '.object.sha'
```

**If your instance mirrors from code.forgejo.org** (the default upstream):
```bash
git ls-remote https://code.forgejo.org/actions/checkout.git 'refs/tags/v4*'
```

**Verify a SHA matches what you expect**:
```bash
# Clone at the specific SHA and inspect
git clone --depth 1 https://forgejo.example.com/actions/checkout.git /tmp/checkout-verify
cd /tmp/checkout-verify
git checkout <sha>
# Review action.yml and dist/ - compare against the known-good upstream release
```

**Key differences from GitHub SHA discovery**:
- The same action (e.g., `actions/checkout`) may have different SHAs on Forgejo mirrors vs GitHub
  because Forgejo forks maintain their own commits
- `code.forgejo.org/actions/*` repos are Forgejo-maintained forks, not exact copies of GitHub repos
- Always verify SHAs against your own instance, not against github.com
- If the action repo is not mirrored yet, an admin must add it to the Forgejo mirror list

### Forgejo-specific gotchas

- **No `ubuntu-latest`** - `runs-on` maps to your registered runner labels (e.g., `docker`)
- **Missing tools** - Forgejo runner containers are lean. Add `apt-get install` for git, curl, etc.
- **TLS certs** - if Forgejo uses self-signed or internal CA certs, configure the runner's trust
  store (`GIT_SSL_CAINFO=/path/to/ca-bundle.crt`) or install the CA into the container image.
  `GIT_SSL_NO_VERIFY=true` is a last resort for dev/test only - never normalize TLS bypass in production
- **Third-party actions** - many GitHub Marketplace actions use GitHub-specific API calls and will silently fail
- **Secrets in Forgejo** - `${{ secrets.* }}` works, but no environment-level scoping
- **`permissions:` not enforced** - Forgejo parses the field but does not restrict the workflow token.
  The token always has full read-write access (read-only for fork PRs only). Don't assume
  least-privilege from `permissions:` alone - it has no effect on Forgejo.

### Managing Forgejo Actions with `fj`

The community Forgejo CLI (`fj`, v0.4.1+) covers the day-to-day Actions surface: listing
runs, dispatching workflows, and managing variables/secrets. It is much faster than the web
UI for bulk secret updates and scriptable for one-shot runs. Install and auth details live
in the **git** skill's `forge-workflows.md` reference.

```bash
# List recent runs (for a quick "is CI green on main?" check)
fj actions tasks

# Trigger a workflow_dispatch run without opening the browser
fj actions dispatch publish.yaml main --inputs version=1.2.3

# Bulk variable/secret management (writes to the repo scope)
fj actions variables create CACHE_BUCKET gs://my-bucket
fj actions secrets create REGISTRY_TOKEN "$REGISTRY_TOKEN"
```

**What `fj` does not do yet** (as of 0.4.1): stream runner logs, re-run failed jobs, cancel
running tasks. For those, use the web UI or hit `/api/v1/repos/{owner}/{repo}/actions/tasks/{id}`
directly. Log streaming across the fleet still belongs in your observability stack, not `fj`.

**On Gitea instead of Forgejo?** Use `tea` (`gitea.com/gitea/tea`) - the Gitea CLI covers
a similar surface (issues, PRs, releases) against any Gitea 1.20+ instance. Gitea Actions
lacks `fj`-equivalent CLI tooling; use the web UI or API. If you're running Forgejo,
prefer `fj` - it tracks Forgejo-specific behavior (AGit, Forgejo Actions quirks) that
`tea` does not.

### Gitea CI/CD

Gitea ships two viable CI paths: **Gitea Actions** (same `act`-based engine as Forgejo
Actions, since Gitea 1.21) and **Woodpecker CI** (separate service, container-native,
webhook-driven). Drone is legacy - do not start new installs.

Quick rule of thumb: if you are migrating from GitHub or want one service to operate,
use Gitea Actions. If you need proper matrix builds, caching primitives, or lighter
resource usage, use Woodpecker. Do not run both against the same repo.

See `references/forgejo-gitea-actions.md` for: action SHA discovery, Gitea-vs-Forgejo Actions
differences, Woodpecker YAML examples, plugin vs command steps, OAuth setup, matrix
patterns, and Drone migration guidance.

### Forgejo release workflow pattern

```yaml
name: Release
on:
  push:
    tags: ['v*']

jobs:
  build-and-push:
    runs-on: docker
    container:
      image: catthehacker/ubuntu:act-24.04    # heavier image for multi-tool needs
    # Private-forge TLS: mount your CA and set GIT_SSL_CAINFO=/path/to/ca.crt.
    # GIT_SSL_NO_VERIFY is a dev/test-only last resort - never commit it to a release pipeline.
    steps:
      - uses: actions/checkout@<sha>  # pin to SHA; resolves from Forgejo mirror
      - name: Login to registry
        env:
          TOKEN: ${{ secrets.REGISTRY_TOKEN }}
          HOST: ${{ secrets.REGISTRY_HOST }}
          USER: ${{ secrets.REGISTRY_USER }}
        run: echo "$TOKEN" | docker login "$HOST" -u "$USER" --password-stdin
      - name: Build and push
        env:
          REGISTRY: ${{ secrets.REGISTRY_HOST }}/${{ secrets.REGISTRY_IMAGE }}
          TAG: ${{ github.ref_name }}
        run: |
          docker build -t "$REGISTRY:$TAG" .
          docker push "$REGISTRY:$TAG"
```

**Note**: use secrets for registry host/image to avoid hardcoding private domains in git history.

## PCI-DSS 4.0: CI/CD Compliance Mapping

All future-dated requirements became **mandatory March 31, 2025**.

| PCI-DSS Req | What it means for CI/CD | Implementation |
|-------------|-------------------------|----------------|
| **6.2.1** | Secure development training + OWASP-aware processes | SAST on every PR/MR, dependency scanning, secret detection |
| **6.2.4** | Access control + change tracking | Branch protection, required reviewers, signed commits, audit logs |
| **6.3.2** | Software inventory (SBOM) | Generate SPDX/CycloneDX SBOM per release, attach to artifacts |
| **6.4.2** | Changes approved, documented, tested | Gated deployments, required approvals for prod, IaC audit trails |
| **6.5.3** | Consistent security controls across environments | Same scanning in dev/staging/prod, not just prod |

**Customized Approach** (v4.0.1): automated CI/CD controls can satisfy manual review requirements
if properly documented. An automated SAST/DAST/SCA gate with evidence = equivalent to manual
code review for QSA assessment.

Read `references/supply-chain.md` for detailed PCI-DSS compliance patterns.

## AI-Age Considerations

AI tools consistently generate insecure CI/CD configs: unpinned actions, missing `permissions:`
blocks, `allow_failure: true` without justification, `:latest` tags, secrets in `run:` blocks.
**Always run the AI Self-Check against AI-generated pipeline code.**

For detailed coverage of slopsquatting, AI agents in CI/CD, prompt injection in pipelines, and
the OWASP Top 10 for Agentic Applications, read `references/supply-chain.md`
(AI-Age Supply Chain Risks section).

## Template Conventions

- **`@<sha>`** in GitHub Actions templates is a placeholder. Replace with the real 40-character
  commit SHA for the indicated version. Look up SHAs on the action's releases page or use
  Dependabot to manage them automatically.
- **Image tags** in templates use floating minor versions (e.g., `oven/bun:1.2`, `docker:27.5`)
  for readability. For production, pin to a specific patch version or SHA256 digest. The templates
  show the minimum acceptable granularity, not the ideal.

## Reference Files

- `references/github-actions.md` - GitHub Actions patterns, templates, and security hardening
- `references/forgejo-gitea-actions.md` - Forgejo/Gitea Actions differences, troubleshooting, Woodpecker patterns, and Drone migration guidance
- `references/gitlab-ci.md` - GitLab CI/CD 19.x patterns, SaaS vs self-managed differences, Catalog, Components, security
- `references/runners.md` - Self-hosted runners (actions-runner, gitlab-runner, forgejo-runner, act_runner, woodpecker-agent) - install, register, executor choice, Linux vs macOS, security hardening
- `references/best-practices.md` - Dependency updates (Dependabot/Renovate), layered linting, scanning matrix (secrets/SCA/container/IaC/SAST), review gates, merge queues, rollout order
- `references/supply-chain.md` - supply chain security, incident timeline, SHA pinning, SBOM/SLSA, PCI-DSS compliance, image signing
- `references/target-versions.md` - May 2026 version snapshot for forges, runners, CI systems, and supply-chain tools

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** CI-CD
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/ci-cd/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **code-review** - has a `cicd-pipelines.md` reference for CI/CD **bug patterns** (expression
  injection, variable scoping, cache gotchas, ArgoCD sync issues)
- **security-audit** - for auditing application code, not pipeline code
- **docker** - for Dockerfile and container image optimization
- **kubernetes** - for K8s manifests and Helm charts that pipelines deploy to
- **git** - for git operations (commits, PRs/MRs, tags, releases) that trigger pipelines.
  CI/CD reacts to git events; git handles the operations that produce them.

## Rules

- **Platform-first.** Always confirm which CI/CD platform before writing config. GitHub Actions
  syntax that "mostly works" in Forgejo will silently break on edge cases.
- **SHA-pin everything.** All third-party actions, all CI tool images. Tags are mutable. SHAs are not.
  The tj-actions, reviewdog, and Trivy compromises proved this is non-negotiable.
- **Secrets are sacred.** Never log, echo, artifact, or pass as CLI arguments. Never use
  protected variables on unprotected branches.
- **Test the pipeline itself.** `act` (GitHub Actions local runner), `gitlab-ci-local`, or dry-run
  modes. Don't discover pipeline bugs in production.
- **Cache != artifact.** Cache is ephemeral speed optimization. Artifacts are guaranteed inter-job
  data. Confusing them causes intermittent failures.
- **Manual gates for prod.** No exceptions. Auto-deploy to staging is fine. Auto-deploy to
  production is how incidents happen.
- **Scan early, deploy late.** Security scanning in the first stages, deployment in the last.
  Finding a CVE after deployment is expensive.
- **PCI-DSS 4.0 is mandatory.** If the pipeline touches CDE (cardholder data environment),
  SBOM generation, signed artifacts, and gated deployments are not optional.
