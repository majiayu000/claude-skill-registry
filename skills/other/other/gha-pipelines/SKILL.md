---
name: gha-pipelines
description: |
  Create and modify GitHub Actions CI/CD workflows for the homelab repository.
  Covers validation pipelines, OCI artifact promotion, and infrastructure testing.

  Use when: (1) Creating new GitHub Actions workflows, (2) Modifying existing CI/CD pipelines,
  (3) Adding validation or testing stages, (4) Debugging workflow failures,
  (5) Understanding the OCI promotion pipeline.

  Triggers: "github actions", "workflow", "ci/cd", "pipeline", "gha",
  "build artifact", "validation workflow", "ci pipeline"
user-invocable: false
---

# GitHub Actions Pipelines

## Established Patterns

This repository uses a small set of consistent patterns across all workflows. Follow these when creating or modifying workflows.

### Tool Setup

All workflows use `mise` for tool version management, ensuring CI and local dev use identical versions:

```yaml
steps:
  - uses: actions/checkout@v6
  - uses: jdx/mise-action@v3    # Installs tools at versions from .mise.toml
  - run: task k8s:validate       # Use Taskfile commands, not raw CLI
```

### Prefer Off-the-Shelf Actions

Use established actions over custom scripts:

| Need | Action | Notes |
|------|--------|-------|
| Checkout | `actions/checkout@v6` | Always pin major version |
| Tool setup | `jdx/mise-action@v3` | Reads `.mise.toml` |
| GHCR login | `docker/login-action@v3` | Use `GITHUB_TOKEN` |
| Complex logic | `actions/github-script@v7` | Prefer over raw bash for GitHub API |
| Flux CLI | `fluxcd/flux2/action@v2` | For OCI artifact operations |

### Use `github-script` Over Raw Bash

For anything involving GitHub API calls, JSON parsing, or conditional logic, prefer `actions/github-script` over shell scripts:

```yaml
- name: Discover clusters
  id: discover
  uses: actions/github-script@v7
  with:
    script: |
      // Use the GitHub API client directly
      const versions = await github.rest.packages.getAllPackageVersionsForPackageOwnedByUser({
        package_type: 'container',
        package_name: packageName,
        username: context.repo.owner,
      });
      core.setOutput('result', JSON.stringify(data));
```

### Dynamic Matrix Builds

For per-cluster or per-module validation, use a discovery job followed by matrix expansion:

```yaml
jobs:
  discover:
    outputs:
      items: ${{ steps.find.outputs.items }}
    steps:
      - id: find
        uses: actions/github-script@v7
        with:
          script: |
            // Discover items dynamically
            core.setOutput('items', JSON.stringify(items));

  validate:
    needs: discover
    strategy:
      fail-fast: false
      matrix:
        item: ${{ fromJson(needs.discover.outputs.items) }}
    steps:
      - run: task validate-${{ matrix.item }}
```

### Path-Based Triggers

Workflows only run when relevant files change:

```yaml
on:
  pull_request:
    paths:
      - "kubernetes/**"                              # Domain files
      - ".github/workflows/kubernetes-validate.yaml" # The workflow itself
      - ".mise.toml"                                  # Tool versions
      - ".taskfiles/kubernetes/**"                   # Task definitions
  workflow_dispatch:                                   # Manual trigger
```

Always include `workflow_dispatch` for manual runs.

### YAML Schema Validation

All workflow files should include the schema comment for IDE validation:

```yaml
---
# yaml-language-server: $schema=https://json.schemastore.org/github-workflow.json
name: My Workflow
```

---

## Workflow Inventory

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `kubernetes-validate.yaml` | PR (kubernetes/) | Lint, expand ResourceSets, build, template, kubeconform, pluto |
| `infrastructure-validate.yaml` | PR (infrastructure/) | Format checks, module tests (matrix per module) |
| `renovate-validate.yaml` | PR (renovate config) | Validate Renovate configuration |
| `build-platform-artifact.yaml` | Push to main (kubernetes/) | Build OCI artifact, tag for integration |
| `tag-validated-artifact.yaml` | Status event / manual | Promote validated artifact to stable semver |
| `renovate.yaml` | Scheduled (hourly) | Dependency update automation |
| `label-sync.yaml` | Scheduled / manual | Sync GitHub labels |

---

## OCI Promotion Pipeline

The promotion pipeline is the most complex workflow chain. Understand the full flow before modifying any part:

```
PR merged to main (kubernetes/ changes)
  -> build-platform-artifact.yaml
     -> flux push artifact :X.Y.Z-rc.N
     -> flux tag :sha-<short> and :integration-<short>
  -> Integration cluster polls OCIRepository (semver >= 0.0.0-0, accepts RCs)
  -> Flux reconciles, posts commit status on success
  -> tag-validated-artifact.yaml (triggered by status event)
     -> Idempotency check (skip if already validated)
     -> flux tag :validated-<short> and :X.Y.Z (stable)
  -> Live cluster polls OCIRepository (semver >= 0.0.0, stable only)
```

### Key Design Decisions

- **Semver-based polling**: Integration accepts pre-releases (`-rc.N`), live accepts stable only
- **Idempotency guard**: `tag-validated-artifact` checks for existing `validated-*` tag before re-tagging (Flux Alerts fire on every reconciliation cycle)
- **Version resolution via GHCR API**: Build workflow queries GHCR for latest stable tag, bumps patch, creates next RC

### Permissions

```yaml
permissions:
  contents: read    # For checkout
  packages: write   # For GHCR push/tag
  statuses: read    # For reading commit status events
```

Always use minimal permissions. Never use `permissions: write-all`.

---

## Creating a New Validation Workflow

### Step-by-Step

1. Create `.github/workflows/<domain>-validate.yaml`
2. Add YAML schema comment
3. Set path-based triggers including the workflow file itself
4. Use `jdx/mise-action@v3` for tool setup
5. Delegate to Taskfile commands (not raw CLI)
6. Add matrix builds for per-item validation if applicable
7. Run `task k8s:validate` locally to verify the validation commands work

### Template

```yaml
---
# yaml-language-server: $schema=https://json.schemastore.org/github-workflow.json
name: <Domain> Validate

on:
  pull_request:
    paths:
      - "<domain>/**"
      - ".github/workflows/<domain>-validate.yaml"
      - ".mise.toml"
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: jdx/mise-action@v3
      - run: task <domain>:validate
```

---

## Anti-Patterns

- **NEVER** install tools with `apt-get` or `brew` in CI — use `mise`
- **NEVER** use raw `curl` / `jq` for GitHub API — use `actions/github-script`
- **NEVER** hardcode versions in workflow files — versions come from `.mise.toml` or `versions.env`
- **NEVER** use `permissions: write-all` — specify exact permissions needed
- **NEVER** skip `workflow_dispatch` — all workflows should support manual runs

---

## Cross-References

- [.github/CLAUDE.md](../../.github/CLAUDE.md) — Declarative knowledge about workflow architecture
- [promotion-pipeline skill](../promotion-pipeline/SKILL.md) — Debugging promotion failures
- [.taskfiles/CLAUDE.md](../../.taskfiles/CLAUDE.md) — Task commands used in workflows
