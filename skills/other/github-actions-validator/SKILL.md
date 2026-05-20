---
name: github-actions-validator
type: standard
depth: full
description: >-
  Validates GitHub Actions workflows via actionlint, act dry-run, and 11 security checks.
  Use when auditing CI/CD security, checking supply chain compliance (SHA pinning, harden-runner,
  OIDC), or validating workflow output. NOT for generation -- route to github-actions-generator.
---

# [H1][GITHUB-ACTIONS-VALIDATOR]
>**Dictum:** *Validation gates prevent non-compliant workflow deployment.*

<br>

Validate GitHub Actions workflows for syntax, security, and best practices. Companion to `github-actions-generator` -- validates what the generator produces.

**Tasks:**
1. Run validation on target file or directory.
2. For each error -- consult matching reference, extract fix.
3. Quote the fix -- error message, cause, applied remediation.
4. Verify public actions via version discovery protocol.
5. Provide summary -- fixes, warnings, best practice recommendations.

---
## [1][VALIDATION_PIPELINE]
>**Dictum:** *Three-stage pipeline ensures complete coverage.*

<br>

**Setup:** `bash .claude/skills/github-actions-validator/scripts/install_tools.sh`

```bash
# Full validation (actionlint + best practices + act dry-run)
bash .claude/skills/github-actions-validator/scripts/validate_workflow.sh <path>

# Selective validation
bash .claude/skills/github-actions-validator/scripts/validate_workflow.sh --lint-only <path>
bash .claude/skills/github-actions-validator/scripts/validate_workflow.sh --check-best-practices <path>
bash .claude/skills/github-actions-validator/scripts/validate_workflow.sh --test-only <path>
```

| [INDEX] | [STAGE]              | [TOOL]                     | [VALIDATES]                                                        |
| :-----: | -------------------- | -------------------------- | ------------------------------------------------------------------ |
|   [1]   | **Static Analysis**  | actionlint 1.7.10          | YAML syntax, expressions, runner labels, action inputs, CRON, globs. |
|   [2]   | **Best Practices**   | `best_practice_checks.sh`  | 11 security/performance checks (see table below).                  |
|   [3]   | **Local Execution**  | act v0.2.84                | Dry-run validation against Docker images (requires Docker).        |

---
## [2][BEST_PRACTICE_CHECKS]
>**Dictum:** *Automated checks enforce security and performance baselines aligned with generator standards.*

<br>

| [INDEX] | [CHECK]                    | [TAG]              | [DETECTS]                                                    |
| :-----: | -------------------------- | ------------------ | ------------------------------------------------------------ |
|   [1]   | **Deprecated commands**    | `[DEPRECATED-CMD]` | `::set-output`, `::save-state`, `::set-env`, `::add-path`.  |
|   [2]   | **Missing permissions**    | `[PERMISSIONS]`    | No top-level `permissions: {}` deny-all default.             |
|   [3]   | **Unpinned actions**       | `[UNPINNED]`       | Mutable tags (`@v1`, `@main`), abbreviated SHAs.             |
|   [4]   | **SHA without comment**    | `[SHA-NO-COMMENT]` | SHA-pinned but missing `# vX.Y.Z` version comment.          |
|   [5]   | **Missing timeout**        | `[TIMEOUT]`        | Jobs without `timeout-minutes:` (default is 6 hours).        |
|   [6]   | **Deprecated runners**     | `[RUNNER]`         | `ubuntu-20.04`, `macos-12`, `macos-13`, `windows-2019`.      |
|   [7]   | **Missing concurrency**    | `[CONCURRENCY]`    | No `concurrency:` group or missing `cancel-in-progress`.     |
|   [8]   | **PAT usage**              | `[APP-TOKEN]`      | PATs for cross-repo ops (use `create-github-app-token`).     |
|   [9]   | **No harden-runner**       | `[HARDEN]`         | Missing or not first step in job (CVE-2025-30066 detection). |
|  [10]   | **Expression injection**   | `[INJECTION]`      | Direct `${{ github.event.* }}` in `run:` blocks.             |
|  [11]   | **Immutable actions**      | `[IMMUTABLE]`      | Action publishing without immutable OCI (informational).     |

---
## [3][ACTIONLINT_RULES]
>**Dictum:** *Static analysis rule names enable targeted suppression.*

<br>

| [INDEX] | [RULE]                    | [CHECKS]                                                   |
| :-----: | ------------------------- | ---------------------------------------------------------- |
|   [1]   | **`syntax-check`**        | Workflow structure, YAML schema, missing keys.             |
|   [2]   | **`expression`**          | `${{ }}` type checking, function calls, context access.    |
|   [3]   | **`action`**              | Action inputs/outputs, required inputs, deprecated inputs. |
|   [4]   | **`runner-label`**        | Valid runner labels, `-arm` vs `-arm64` suffix.             |
|   [5]   | **`glob`**                | Glob patterns in paths/branches filters.                   |
|   [6]   | **`job-needs`**           | Job dependency graph, circular `needs:`.                   |
|   [7]   | **`workflow-call`**       | Reusable workflow inputs/outputs/secrets.                  |
|   [8]   | **`events`**              | Trigger event validation, CRON field ranges.               |
|   [9]   | **`credentials`**         | Hard-coded credentials detection.                          |
|  [10]   | **`permissions`**         | GITHUB_TOKEN permission scopes, `models`, `artifact-metadata`. |
|  [11]   | **`deprecated-commands`** | `set-output`, `save-state` usage.                          |
|  [12]   | **`shellcheck`**          | Shell script linting in `run:` blocks.                     |
|  [13]   | **`if-cond`**             | Constant `if: true`/`if: false` conditions.                |

---
## [4][ERROR_ROUTING]
>**Dictum:** *Error patterns map to specific reference files for resolution.*

<br>

| [INDEX] | [PATTERN]                           | [REFERENCE]                                 |
| :-----: | ----------------------------------- | ------------------------------------------- |
|   [1]   | **`runs-on`, runner labels**        | `runners.md`                                |
|   [2]   | **`cron`, `schedule`**              | `common_errors.md` -- Schedule Errors       |
|   [3]   | **`${{`, `expression`, `if:`**      | `common_errors.md` -- Expression Errors     |
|   [4]   | **`needs:`, job dependency**        | `common_errors.md` -- Job Configuration     |
|   [5]   | **`uses:`, action, input**          | `common_errors.md` -- Action Errors         |
|   [6]   | **`set-output`, `save-state`**      | `common_errors.md` -- Deprecated Commands   |
|   [7]   | **`workflow_call`, reusable**       | `modern_features.md` -- Reusable Workflows  |
|   [8]   | **SLSA, attestation, cosign, SBOM** | `supply_chain.md` -- SBOM/Provenance        |
|   [9]   | **OIDC, keyless, cloud auth**       | `supply_chain.md` -- OIDC Federation        |
|  [10]   | **immutable, OCI, GHCR action**     | `supply_chain.md` -- Immutable Actions      |
|  [11]   | **app token, PAT, cross-repo**      | `supply_chain.md` -- App Tokens             |
|  [12]   | **harden-runner, egress**           | `supply_chain.md` -- Harden Runner          |
|  [13]   | **node20, node24, runtime**         | `modern_features.md` -- Node.js Runtime     |
|  [14]   | **concurrency, cancel-in-progress** | `modern_features.md` -- Concurrency Control |
|  [15]   | **YAML anchor, alias, `<<:`**       | `modern_features.md` -- YAML Anchors        |
|  [16]   | **matrix, fail-fast**               | `modern_features.md` -- Matrix Strategy     |
|  [17]   | **permission scope**                | `common_errors.md` -- Permissions Errors    |

---
## [5][REFERENCE_FILES]
>**Dictum:** *Reference files provide authoritative error resolution.*

<br>

| [INDEX] | [FILE]                              | [CONTENT]                                                    |
| :-----: | ----------------------------------- | ------------------------------------------------------------ |
|   [1]   | **`references/act_usage.md`**       | Actionlint 1.7.10 + act v0.2.84 usage, rules, limitations.  |
|   [2]   | **`references/common_errors.md`**   | Error catalog: syntax, expression, action, job, deprecated.  |
|   [3]   | **`references/modern_features.md`** | Reusable workflows, concurrency, YAML anchors, matrix, Node. |
|   [4]   | **`references/runners.md`**         | Runner labels, deprecations, ARM64, GPU, self-hosted.        |
|   [5]   | **`references/supply_chain.md`**    | SHA pinning, OIDC, SBOM, harden-runner, tokens, dep review.  |

---
## [6][EXAMPLES]
>**Dictum:** *Examples validate the validation pipeline itself.*

<br>

| [INDEX] | [FILE]                  | [PURPOSE]                                       |
| :-----: | ----------------------- | ----------------------------------------------- |
|   [1]   | `valid-ci.yml`          | Passes all checks with zero warnings.           |
|   [2]   | `with-errors.yml`       | Triggers every best practice check (11 hits).   |
|   [3]   | `outdated-versions.yml` | Stale tags, deprecated commands, legacy Node.    |

---
## [7][TROUBLESHOOTING]
>**Dictum:** *Common issues have known resolutions.*

<br>

| [INDEX] | [ISSUE]                     | [SOLUTION]                                   |
| :-----: | --------------------------- | -------------------------------------------- |
|   [1]   | **Tools not found**         | `bash scripts/install_tools.sh`              |
|   [2]   | **Docker not running**      | Start Docker or use `--lint-only`.           |
|   [3]   | **Permission denied**       | `chmod +x scripts/*.sh`                      |
|   [4]   | **act fails, GitHub works** | See `act_usage.md` -- Limitations.           |
|   [5]   | **ARM Mac arch mismatch**   | Add `--container-architecture linux/amd64`.  |
|   [6]   | **Custom runner labels**    | Declare in `.github/actionlint.yaml`.        |

[VERIFY] Completion:
- [ ] All errors resolved with reference-backed fixes.
- [ ] Action versions verified via discovery protocol or generator examples.
- [ ] Best practice checks pass or warnings documented.
- [ ] Summary provided with fixes, warnings, and recommendations.
