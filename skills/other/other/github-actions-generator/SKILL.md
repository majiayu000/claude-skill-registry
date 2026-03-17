---
name: github-actions-generator
type: standard
depth: full
description: >-
  Generates GitHub Actions workflows and custom actions (composite/Docker/JavaScript)
  with SHA-pinned supply chain security, SLSA attestation, OIDC federation, and
  harden-runner enforcement. Use when creating CI/CD pipelines, reusable workflows,
  monorepo CI patterns, container build/deploy orchestration, or advanced triggers
  (workflow_run, dispatch, ChatOps). Not for validating existing workflows—use
  github-actions-validator.
---

# [H1][GITHUB-ACTIONS-GENERATOR]
>**Dictum:** *Workflow generation enforces security, performance, and supply chain integrity.*

<br>

Generate production-ready GitHub Actions workflows and custom actions. Validate all output with `github-actions-validator`.

**Tasks:**
1. Gather requirements — triggers, runners, dependencies, environments, security posture.
2. Read [→best-practices.md](./references/best-practices.md) — security hardening, supply chain, performance, anti-patterns.
3. Read [→version-discovery.md](./references/version-discovery.md) — SHA resolution protocol, action index, permissions.
4. Read [→expressions-and-contexts.md](./references/expressions-and-contexts.md) — contexts, functions, injection prevention.
5. (advanced triggers) Read [→advanced-triggers.md](./references/advanced-triggers.md) — workflow_run, dispatch, ChatOps, merge queue.
6. (custom actions) Read [→custom-actions.md](./references/custom-actions.md) — composite, Docker, JavaScript action authoring.
7. Resolve action versions — `git ls-remote`, Context7 MCP, or WebSearch for latest SHA.
8. Generate — SHA-pinned actions, minimal permissions, concurrency, caching, timeouts, harden-runner.
9. Validate with `github-actions-validator`.
10. Fix and re-validate until passing.

**Scope:**
- Workflow files (`.github/workflows/*.yml`).
- Custom actions — composite, Docker, JavaScript (`.github/actions/*/action.yml`).
- Reusable workflows (`workflow_call`).
- Supply chain — SLSA attestation, SBOM, Cosign signing.
- Monorepo CI — Nx affected detection, sparse checkout, pnpm workspace caching.

**Domain Navigation Map:**

| [INDEX] | [DOMAIN]              | [REFERENCE]                                                            | [LOAD_WHEN]                                                |
| :-----: | --------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------- |
|   [1]   | **Best Practices**    | [→best-practices.md](references/best-practices.md)                     | Permissions, caching, concurrency, runners, anti-patterns. |
|   [2]   | **Version Discovery** | [→version-discovery.md](references/version-discovery.md)               | Action references, SHA pinning, supply chain integrity.    |
|   [3]   | **Expressions**       | [→expressions-and-contexts.md](references/expressions-and-contexts.md) | Conditionals, dynamic values, injection prevention.        |
|   [4]   | **Advanced Triggers** | [→advanced-triggers.md](references/advanced-triggers.md)               | Workflow chaining, dispatch, ChatOps, merge queue.         |
|   [5]   | **Custom Actions**    | [→custom-actions.md](references/custom-actions.md)                     | Composite, Docker, JavaScript action authoring.            |

[REFERENCE] [→index.md](./index.md) — Complete file listing.

---
## [1][STANDARDS]
>**Dictum:** *Mandatory standards enforce baseline quality across all generated workflows.*

<br>

Every generated workflow enforces defense-in-depth: supply chain integrity prevents compromised actions from executing, minimal permissions limit blast radius if a job is compromised, and harden-runner detects anomalous behavior at runtime. These layers are independent — failure of one leaves others intact.

[CRITICAL]:
- [ALWAYS] SHA-pin every `uses:` reference — mutable tags (`@v1`, `@main`) enable supply chain attacks. The tj-actions incident (CVE-2025-30066) compromised 23,000+ repos via tag retargeting.
- [ALWAYS] `step-security/harden-runner` as first step in every job — detected the tj-actions breach before any other tool.
- [ALWAYS] Top-level `permissions: {}` (deny-all default); grant minimal per-job permissions.
- [ALWAYS] `timeout-minutes:` on every job — prevents runaway billing on stuck workflows.

[IMPORTANT]:
- [ALWAYS] OIDC federation (`id-token: write`) for cloud auth — eliminates static credentials entirely.
- [ALWAYS] `actions/create-github-app-token` for cross-repo ops — scoped, 1-hour expiry, survives offboarding.
- [ALWAYS] `>> $GITHUB_OUTPUT` for step outputs; `>> $GITHUB_STEP_SUMMARY` for job summaries.
- [NEVER] Direct `${{ }}` interpolation of untrusted input in `run:` blocks — route through `env:` indirection.

[REFERENCE] [→best-practices.md](./references/best-practices.md) — Security checklist, supply chain controls, anti-patterns.

---
## [2][TEMPLATES]
>**Dictum:** *Templates scaffold canonical workflow and action structure.*

<br>

Templates use `[PLACEHOLDER]` syntax for generation-time substitution. SHA resolution happens at generation time via the discovery protocol — templates contain placeholder SHAs, not static pins.

### [2.1][PLACEHOLDER_CONVENTION]

All templates use a unified `[UPPER_SNAKE_CASE]` placeholder convention:

| [CATEGORY]      | [PLACEHOLDERS]                                                              |
| --------------- | --------------------------------------------------------------------------- |
| **Identity**    | `[ACTION_NAME]`, `[WORKFLOW_NAME]`, `[DESCRIPTION]`, `[AUTHOR_NAME]`        |
| **Runtime**     | `[RUNTIME_VERSION]`, `[RUNTIME_ENV_KEY]`, `[ENABLE_CMD]`                    |
| **Package Mgr** | `[PACKAGE_MANAGER]`, `[INSTALL_CMD]`                                        |
| **Build/Test**  | `[BUILD_CMD]`, `[LINT_CMD]`, `[TEST_CMD]`, `[BUILD_PATH]`, `[RESULTS_PATH]` |
| **Deploy**      | `[ENV_NAME]`, `[ENV_URL]`, `[DEPLOY_CMD]`, `[VERIFY_CMD]`                   |
| **Secrets**     | `[SECRET_KEY]`, `[SECRET_NAME]`, `[REGISTRY_TOKEN]`                         |
| **Docker**      | `[BASE_IMAGE]`, `[BUILDER_IMAGE]`, `[ENTRYPOINT]`                           |

### [2.2][HARDEN_RUNNER_SCOPE]

`harden-runner` is included as the first step in every **workflow** job template (basic, reusable). **Action** templates (composite, Docker, JavaScript) do NOT include `harden-runner` — the **calling workflow** is responsible for adding it as the first step in the job that invokes the action. Actions are steps, not jobs.

### [2.3][TEMPLATE_INDEX]

| [INDEX] | [TEMPLATE]            | [PATH]                                            | [SCAFFOLDS]                                                        |
| :-----: | --------------------- | ------------------------------------------------- | ------------------------------------------------------------------ |
|   [1]   | **Basic Workflow**    | `assets/templates/workflow/basic_workflow.yml`    | CI pipeline: lint, test, build, deploy with parameterized runtime. |
|   [2]   | **Reusable Workflow** | `assets/templates/workflow/reusable_workflow.yml` | `workflow_call` with typed inputs, secrets, version extraction.    |
|   [3]   | **Composite Action**  | `assets/templates/action/composite/action.yml`    | Multi-step action with parameterized runtime and error handling.   |
|   [4]   | **Docker Action**     | `assets/templates/action/docker/action.yml`       | Container action with distroless multi-stage Dockerfile pattern.   |
|   [5]   | **JavaScript Action** | `assets/templates/action/javascript/action.yml`   | Node 24 action with pre/post lifecycle, typed error handling.      |

[REFERENCE] [→custom-actions.md](./references/custom-actions.md) — Action type selection, metadata, runtime deprecation.

---
## [3][EXAMPLES]
>**Dictum:** *Examples demonstrate production patterns for common scenarios.*

<br>

Each example demonstrates distinct patterns with minimal overlap. Load relevant examples before generation to match the target scenario.

| [INDEX] | [EXAMPLE]                                | [PATH]                                          | [DEMONSTRATES]                                                    |
| :-----: | ---------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------- |
|   [1]   | **Node.js CI**                           | `examples/workflows/nodejs-ci.yml`              | Matrix testing, caching, artifact upload, coverage, summaries.    |
|   [2]   | **Docker Build + Push**                  | `examples/workflows/docker-build-push.yml`      | Multi-platform builds, GHCR, BuildKit caching, SLSA provenance.   |
|   [3]   | **Monorepo CI**                          | `examples/workflows/monorepo-ci.yml`            | Nx affected detection, pnpm workspace, sparse checkout.           |
|   [4]   | **PR Security Gate**                     | `examples/security/dependency-review.yml`       | Multi-job security: dep review, CodeQL, Gitleaks, triage.         |
|   [5]   | **Container Supply Chain**               | `examples/security/sbom-attestation.yml`        | SBOM, Trivy severity gating, Cosign, gh attestation verify.       |
|   [6]   | **Composite Action (setup-node-cached)** | `examples/actions/setup-node-cached/action.yml` | Smart caching, corepack detection, cache-dir resolution.          |
|   [7]   | **ChatOps Dispatch**                     | `examples/workflows/chatops-dispatch.yml`       | Slash commands, injection prevention, App token, env indirection. |
|   [8]   | **Multi-Cloud OIDC Auth**                | `examples/actions/oidc-cloud-auth/action.yml`   | Composite action: AWS/GCP/Azure OIDC, output normalization.       |
|   [9]   | **Release + Deploy**                     | `examples/workflows/release-deploy.yml`         | Environment promotion, reusable workflow, concurrency groups.     |
|  [10]   | **Docker Lint + Scan**                   | `examples/actions/docker-lint-scan/action.yml`  | Composite action: Trivy scan, hadolint, SARIF output.             |
|  [11]   | **PR Change Router**                     | `examples/actions/pr-change-router/action.yml`  | Composite action: paths-filter, dynamic matrix, label sync.       |

---
## [4][ACTION_DISCOVERY]
>**Dictum:** *Runtime version resolution prevents stale SHA pins and supply chain drift.*

<br>

Static SHA catalogs decay — actions release frequently and stale pins miss security patches. Resolve versions at generation time. Never embed hardcoded SHAs in reference docs or templates.

**Resolution protocol:**
1. `git ls-remote --tags https://github.com/{owner}/{repo}` — verify tag exists.
2. `gh api repos/{owner}/{repo}/git/ref/tags/{tag} --jq '.object.sha'` — resolve tag to full SHA.
3. Format: `owner/repo@<40-char-SHA> # vX.Y.Z`.

**Fallback methods:**
- Context7 MCP: `resolve-library-id` then `get-library-docs` for action documentation.
- WebSearch: `"[owner/repo] [version] github action"` for release notes.

[IMPORTANT]:
- [ALWAYS] Verify the tag exists before pinning — deleted tags return empty results.
- [ALWAYS] Include version comment suffix (`# vX.Y.Z`) — Dependabot/Renovate parse these for automated updates.
- [NEVER] Embed static SHAs in reference files — they decay within weeks.

[REFERENCE] [→version-discovery.md](./references/version-discovery.md) — Discovery protocol, SHA pinning format, common actions index, automated maintenance.

---
## [5][VALIDATION]
>**Dictum:** *Gates prevent non-compliant workflow output.*

<br>

[VERIFY] Completion:
- [ ] Supply chain: Every `uses:` reference SHA-pinned with `# vX.Y.Z` comment suffix.
- [ ] Security: Top-level `permissions: {}`, per-job minimal grants, `harden-runner` first step.
- [ ] Injection: No direct `${{ github.event.* }}` in `run:` blocks — all through `env:` indirection.
- [ ] Performance: Caching enabled, `concurrency` groups set, `timeout-minutes:` on every job.
- [ ] Structure: Descriptive `name:` on workflow/jobs/steps, lowercase-hyphen filenames.
- [ ] Outputs: `>> $GITHUB_OUTPUT` for data, `>> $GITHUB_STEP_SUMMARY` for summaries.
- [ ] Agnosticism: No hardcoded package manager, build tool, or language-specific paths in templates.
- [ ] Harden-runner: Workflow jobs include it; action templates note caller responsibility.
- [ ] Validator: Output passed through `github-actions-validator` skill.

[REFERENCE] [→best-practices.md§ANTI_PATTERNS](./references/best-practices.md) — Known anti-patterns with specific remediations.
