---
name: github-actions-patterns
description: "Use when building GitHub Actions workflows, setting up CI/CD on GitHub, or optimizing existing Actions pipelines. Covers reusable workflows, composite actions, matrix strategies, OIDC auth, monorepo path filters, and caching."
---

# GitHub Actions Patterns

## Reusable Workflows vs Composite Actions

| | Reusable Workflow (`workflow_call`) | Composite Action |
|---|---|---|
| **Scope** | Full job(s) with multiple steps | Single step replacement |
| **Trigger** | `on: workflow_call` with inputs/secrets | `uses:` in a step |
| **Nesting** | Max 4 levels deep | Unlimited |
| **Secrets** | Must be passed explicitly or use `secrets: inherit` | Inherited from caller |
| **Use when** | Standardizing entire CI pipelines across repos | Sharing a handful of reusable steps |

### Reusable Workflow

```yaml
# .github/workflows/ci-reusable.yml
on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: "20"
    secrets:
      NPM_TOKEN:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020 # v4.4.0
        with:
          node-version: ${{ inputs.node-version }}
          cache: npm
      - run: npm ci
        env:
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
      - run: npm test
```

**Caller**: `uses: ./.github/workflows/ci-reusable.yml` with `secrets: inherit` or explicit mapping.

## Matrix Strategies

Use `strategy.matrix` for OS/version combinations. `fail-fast: false` continues siblings. `exclude` removes combos, `include` adds specific ones. 256 combo limit.

## OIDC Authentication (No Stored Secrets)

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502 # v4.0.2
    with:
      role-to-arn: arn:aws:iam::123456789:role/github-deploy
      aws-region: us-east-1
```

Works with AWS, GCP (`google-github-actions/auth`), Azure (`azure/login`). Trust policy scopes to repo + branch + environment.

## Monorepo Path Filters

Use `paths:` filter on push triggers. For PRs, use `dorny/paths-filter` action with conditional `if: needs.changes.outputs.X == 'true'`.

## Caching

| Method | When |
|--------|------|
| `actions/setup-*` built-in `cache:` param | Node, Python, Go, Ruby -- simplest |
| `actions/cache` | Custom paths, Docker layers, arbitrary artifacts |
| Docker `cache-from: type=gha` | Container builds via `docker/build-push-action` |

**Key pattern**: `hashFiles('**/package-lock.json')` for deterministic cache keys. Add OS to key for cross-platform matrices.

## Security

- **Pin to SHA**, never tags: `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` not `@v4`
- **Minimal permissions**: Set `permissions:` per job, not workflow-level
- **GITHUB_TOKEN scoping**: Default is read for PRs from forks; set explicitly
- **No secrets in logs**: Use `::add-mask::` for dynamic values
- **Concurrency groups**: Prevent parallel deploys to same environment

```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: true  # only for CI, NOT deploys
```

## Gotchas

- **256 matrix limit** -- use `include` to add specific combos rather than full cartesian product
- **Reusable workflow nesting**: max 4 levels; composite actions don't count toward this
- **`actions/checkout` fetch-depth**: defaults to 1 (shallow) -- use `fetch-depth: 0` for changelogs, version bumps, git history
- **Concurrency `cancel-in-progress`**: never use for deployment jobs (cancels mid-deploy)
- **`secrets: inherit`**: passes ALL org/repo secrets -- prefer explicit mapping in production
- **`if:` expressions**: always wrap in `${{ }}` for string comparisons; bare `if: github.ref == 'refs/heads/main'` can fail silently
- **Workflow permissions**: fork PRs get read-only `GITHUB_TOKEN` regardless of settings

## Cross-References

- **devops:pipeline-design** -- deployment strategies, DORA metrics, approval gates
- **devops:docker-patterns** -- container build optimization, multi-stage builds
- **devops:gitops-workflow** -- ArgoCD/Flux integration from Actions pipelines
