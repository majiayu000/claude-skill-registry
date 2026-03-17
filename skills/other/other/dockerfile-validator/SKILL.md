---
name: dockerfile-validator
type: complex
depth: extended
description: >-
  Validates existing Dockerfiles through 5-stage pipeline (hadolint syntax, Checkov CKV policies, secret detection, BuildKit features, optimization). Use when checking syntax, finding security issues, auditing best practices, or analyzing layer efficiency. Not for generating Dockerfiles (use dockerfile-generator instead).
---

# [H1][DOCKERFILE-VALIDATOR]
>**Dictum:** *Automated validation enforces security and build quality.*

<br>

Docker Engine 27+ | BuildKit 0.27+ | hadolint 2.14+ | Checkov latest

**Tasks:**
1. Read the target Dockerfile -- Understand context before validation
2. Run validation -- `bash scripts/dockerfile-validate.sh <Dockerfile>`
3. Read [dockerfile_reference.md](./references/dockerfile_reference.md) -- Fix patterns for reported issues
4. Summarize by severity -- critical -> high -> medium -> low
5. Propose fixes with concrete code from reference patterns
6. Offer to apply fixes to the Dockerfile

**Scope:**
- *Validation:* All Dockerfile variants (Dockerfile, Dockerfile.prod, Dockerfile.dev)
- *Not:* Generating Dockerfiles (use dockerfile-generator), building/running containers, debugging

---
## [1][VALIDATION_PIPELINE]
>**Dictum:** *Five stages catch progressively subtler issues.*

<br>

**Guidance:**<br>
- `Stage 1` -- hadolint: Instruction validation, ShellCheck on RUN, 60+ lint rules.
- `Stage 2` -- Checkov: 11 CKV_DOCKER policies + 17 CKV2_DOCKER graph checks.
- `Stage 3` -- Extended security: Secrets, sudo, cert bypass (curl/wget/pip/npm/git), chpasswd, dangerous packages.
- `Stage 4` -- Best practices: `:latest`, USER, HEALTHCHECK, STOPSIGNAL, MAINTAINER, ADD, apt, WORKDIR, shell form, cache cleanup, COPY order, BuildKit syntax, OCI labels, heredoc.
- `Stage 5` -- Optimization: Base image size, multi-stage, layer count, BuildKit features (`--mount`, `--link`, `--chmod`), heredoc opportunities, .dockerignore, Chainguard.

**Best-Practices:**<br>
- **Exit codes:** `0` all passed (warnings allowed), `1` validation failure (errors), `2` critical error
- **Auto-install:** Script installs hadolint + Checkov in temp venvs if missing, cleans up via bash trap
- **Force temp:** `FORCE_TEMP_INSTALL=true bash scripts/dockerfile-validate.sh Dockerfile`

[REFERENCE]: [→dockerfile_reference.md](./references/dockerfile_reference.md) -- Base images, security rules, hadolint/Checkov catalogs.

---
## [2][SEVERITY_CLASSIFICATION]
>**Dictum:** *Severity determines fix priority.*

<br>

**Guidance:**<br>
- `Critical` -- Hardcoded secrets in ENV/ARG, cert bypass flags, no USER directive.
- `High` -- `:latest` tag, sudo usage, SSH port (22), no HEALTHCHECK for services.
- `Medium` -- Missing version pins, cache cleanup, missing OCI labels, no `--no-install-recommends`.
- `Low` -- Style (layer count, STOPSIGNAL, heredoc opportunities).

**Best-Practices:**<br>
- **Fix order:** Critical first, then high, medium, low. Resolve all critical before moving to high.
- **Iteration cap:** Max 3 fix-validate cycles. Remaining warnings acceptable if no errors.

---
## [3][KEY_RULES]
>**Dictum:** *Rule references enable precise fix targeting.*

<br>

| [INDEX] | [CATEGORY]     | [CHECK]                                                               | [RULE_ID]                           |
| :-----: | -------------- | --------------------------------------------------------------------- | ----------------------------------- |
|   [1]   | **Base image** | Pin version (not `:latest`), prefer slim-trixie/distroless/Chainguard | DL3006, DL3007, CKV_DOCKER_7        |
|   [2]   | **Security**   | Non-root USER with UID/GID                                            | DL3002, CKV_DOCKER_3, CKV_DOCKER_8  |
|   [3]   | **Security**   | No secrets in ENV/ARG                                                 | Custom + CKV2_DOCKER_17             |
|   [4]   | **Security**   | No cert bypass flags                                                  | CKV2_DOCKER_2 through CKV2_DOCKER_6 |
|   [5]   | **Security**   | No sudo, no chpasswd                                                  | CKV2_DOCKER_1, DL3004               |
|   [6]   | **BuildKit**   | COPY --link on all COPY statements                                    | Custom                              |
|   [7]   | **BuildKit**   | COPY --chmod (no separate RUN chmod)                                  | Custom                              |
|   [8]   | **BuildKit**   | RUN --mount=type=cache for pkg managers                               | Custom                              |
|   [9]   | **BuildKit**   | RUN --mount=type=secret,env= (not file-based)                         | Custom                              |
|  [10]   | **BuildKit**   | RUN <<EOF heredoc for multi-line scripts                              | Custom                              |
|  [11]   | **Runtime**    | HEALTHCHECK with exec-form CMD and `--start-interval`                 | CKV_DOCKER_2, DL3047                |
|  [12]   | **Runtime**    | STOPSIGNAL for graceful shutdown                                      | Custom                              |
|  [13]   | **Runtime**    | Exec-form ENTRYPOINT/CMD (not shell form)                             | DL3025                              |
|  [14]   | **Metadata**   | OCI labels with revision/created/version                              | Custom                              |
|  [15]   | **Metadata**   | Pulumi-injectable ARGs (GIT_SHA, BUILD_DATE)                          | Custom                              |
|  [16]   | **Layers**     | Combine consecutive RUN with heredoc                                  | DL3059                              |

---
## [4][RESOURCES]
>**Dictum:** *Examples demonstrate both compliance and violations.*

<br>

| [INDEX] | [PATH]                                    | [PURPOSE]                                                                        |
| :-----: | ----------------------------------------- | -------------------------------------------------------------------------------- |
|   [1]   | **`scripts/dockerfile-validate.sh`**      | 5-stage validator with auto-install/cleanup.                                     |
|   [2]   | **`scripts/_checks.sh`**                  | Extended security, best practices, and optimization checks.                      |
|   [3]   | **`references/dockerfile_reference.md`**  | Base images, security rules, hadolint/Checkov catalogs, BuildKit version matrix. |
|   [4]   | **`examples/good-example.Dockerfile`**    | Node.js multi-stage with all best practices.                                     |
|   [5]   | **`examples/bad-example.Dockerfile`**     | 20 anti-patterns with fix references.                                            |
|   [6]   | **`examples/security-issues.Dockerfile`** | Intentional security vulns with CKV rule references.                             |

---
## [5][TOOL_INSTALLATION]
>**Dictum:** *Tools auto-installed by script; permanent install optional.*

<br>

| [INDEX] | [TOOL]       | [INSTALL]                                                                        |      [MIN_VERSION]       |
| :-----: | ------------ | -------------------------------------------------------------------------------- | :----------------------: |
|   [1]   | **hadolint** | Nix-provided on dev machines. VPS: `bash .claude/scripts/bootstrap-cli-tools.sh` |          2.14.0          |
|   [2]   | **Checkov**  | Nix-provided on dev machines. VPS: `bash .claude/scripts/bootstrap-cli-tools.sh` | latest (Python 3.9-3.14) |

**Troubleshooting:**

| [INDEX] | [ERROR]                            | [FIX]                                                         |
| :-----: | ---------------------------------- | ------------------------------------------------------------- |
|   [1]   | **FROM must be first non-comment** | Move `ARG` defining base tag before `FROM`.                   |
|   [2]   | **Unknown instruction**            | Check spelling (common: RUNS, COPIES, FRUM).                  |
|   [3]   | **COPY failed: file not found**    | Verify path relative to build context, check .dockerignore.   |
|   [4]   | **Hardcoded secrets detected**     | `--mount=type=secret,env=VAR` or runtime config.              |
|   [5]   | **COPY --link not recognized**     | `# syntax=docker/dockerfile:1` as first line, Docker 23.0+.   |
|   [6]   | **Heredoc not recognized**         | `# syntax=docker/dockerfile:1` as first line, BuildKit 0.10+. |

---
## [6][VALIDATION]
>**Dictum:** *Gates prevent incomplete validation reports.*

<br>

[VERIFY] Completion:
- [ ] Target Dockerfile read and context understood
- [ ] `scripts/dockerfile-validate.sh` executed against target
- [ ] Issues summarized by severity (critical -> high -> medium -> low)
- [ ] Fix patterns referenced from `dockerfile_reference.md`
- [ ] Concrete fix code proposed for each issue
- [ ] All critical and high issues resolved (medium/low: fix or document rationale)

**Integration:**
- **dockerfile-generator** -- Generates Dockerfiles validated by this skill
- **k8s-debug** -- Container debugging when builds fail at runtime
