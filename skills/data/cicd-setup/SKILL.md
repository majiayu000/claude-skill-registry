---
name: cicd-setup
description: Create and configure CI/CD pipelines with security-first best practices. Triggers on requests to set up CI/CD, add GitHub Actions, create pipelines, automate testing/deployment, configure workflows, add continuous integration, or automate releases.
allowed-tools: Read, Edit, Write, Task, Glob, Grep, Bash
---

# CI/CD Setup

Create secure, production-ready CI/CD pipelines following 2025-2026 best practices.

## Workflow

### 1. Detect Platform and Stack

Run these Glob patterns to identify the project:

```
Platform detection:
- .github/workflows/*.yml → GitHub Actions
- .gitlab-ci.yml → GitLab CI
- .circleci/config.yml → CircleCI

Stack detection:
- package.json, package-lock.json, yarn.lock, pnpm-lock.yaml → Node.js
- Cargo.toml, Cargo.lock → Rust
- go.mod, go.sum → Go
- pyproject.toml, requirements.txt, setup.py → Python
- Dockerfile, docker-compose.yml → Docker
```

### 2. Generate Workflows

Based on detected stack, create:

1. **CI workflow** (`.github/workflows/ci.yml`) - lint, test, build
2. **Dependabot config** (`.github/dependabot.yml`) - dependency updates
3. **CD workflow** (if deployment needed) - release/deploy

### 3. Document Setup

After creating workflows, list:
- Required secrets (if any)
- Required repository settings
- How to verify it works

## Security Requirements (Non-Negotiable)

### Pin Actions to Full SHA

After the 2025 tj-actions and reviewdog supply chain attacks, NEVER use mutable tags:

```yaml
# WRONG - tag can be hijacked
- uses: actions/checkout@v4

# CORRECT - immutable SHA
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
```

To find current SHAs: `gh api repos/actions/checkout/releases/latest --jq '.tag_name'` then check the commit.

### Use OIDC Instead of Long-Lived Secrets

Eliminate stored credentials with OIDC:

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502 # v4.0.2
    with:
      role-to-assume: arn:aws:iam::ACCOUNT:role/GitHubActionsRole
      aws-region: us-east-1
      # No AWS_ACCESS_KEY_ID needed - OIDC provides short-lived tokens
```

### Minimal Permissions

Always declare explicit permissions:

```yaml
permissions:
  contents: read      # Only what's needed
  # Default is read-all for GITHUB_TOKEN if not specified
```

### Protect Against pull_request_target

NEVER checkout PR code in `pull_request_target` workflows - this gives untrusted code access to secrets:

```yaml
# DANGEROUS - attacker can access secrets via PR code
on: pull_request_target
steps:
  - uses: actions/checkout@SHA
    with:
      ref: ${{ github.event.pull_request.head.sha }}  # BAD

# SAFE - use pull_request instead (no secrets access, read-only token)
on: pull_request
```

## Dependabot Configuration

Always include GitHub Actions in Dependabot:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      actions:
        patterns: ["*"]

  # Add for your package manager
  - package-ecosystem: "npm"  # or pip, cargo, gomod
    directory: "/"
    schedule:
      interval: "weekly"
```

## CI Workflow Template

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

      # Add setup step for your language (see patterns below)

      - name: Lint
        run: # lint command

      - name: Test
        run: # test command
```

## Language Setup Patterns

### Node.js
```yaml
- uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af # v4.1.0
  with:
    node-version-file: '.nvmrc'
    cache: 'npm'
- run: npm ci
- run: npm run lint
- run: npm test
```

### Python
```yaml
- uses: actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b # v5.3.0
  with:
    python-version-file: '.python-version'
    cache: 'pip'
- run: pip install -e ".[dev]"
- run: ruff check .
- run: pytest
```

### Rust
```yaml
- uses: dtolnay/rust-toolchain@56f84321dbccf38fb67ce29ab63e4754056677e0 # stable
  with:
    toolchain: stable
    components: clippy, rustfmt
- uses: Swatinem/rust-cache@9d47c6ad4b02e050fd481d890b2ea34778fd09d6 # v2.7.8
- run: cargo fmt --check
- run: cargo clippy -- -D warnings
- run: cargo test
```

### Go
```yaml
- uses: actions/setup-go@d35c59abb061a4a6fb18e82ac0862c26744d6ab5 # v5.5.0
  with:
    go-version-file: 'go.mod'
- run: go vet ./...
- run: go test -race ./...
```

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Using `@v4` tags | Pin to full SHA with version comment |
| Storing AWS keys as secrets | Use OIDC with `id-token: write` |
| No timeout on jobs | Add `timeout-minutes: 15` (or appropriate) |
| Running on every push | Add path filters for docs-only changes |
| Self-hosted runners on public repos | Use GitHub-hosted or private repos only |
| `pull_request_target` with checkout | Use `pull_request` trigger instead |

See `references/advanced-patterns.md` for supply chain security (SLSA, SBOM, signing), reusable workflows, and monorepo patterns.

## Output Checklist

After setup, verify:
- [ ] All actions pinned to SHA with version comment
- [ ] `permissions:` block explicitly set
- [ ] `concurrency:` prevents duplicate runs
- [ ] `timeout-minutes:` set on all jobs
- [ ] Dependabot configured for actions AND dependencies
- [ ] No long-lived credentials (use OIDC where possible)
- [ ] Tests pass locally before pushing workflow
