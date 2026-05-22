---
name: rust-github-ci
description: Set up GitHub Actions CI for Rust projects. Creates reusable workflows for clippy, rustfmt, tests, cargo-deny, and sqlx. Use when setting up CI, adding GitHub workflows, configuring Rust pipelines, or fixing CI issues in Rust projects.
---

# Rust GitHub Actions CI

Set up comprehensive CI for Rust projects using reusable workflows.

## Architecture

```
.github/workflows/
├── ci.yml           # Orchestrator - triggers on push/PR, calls reusable workflows
├── _fmt.yml         # Reusable: rustfmt check
├── _clippy.yml      # Reusable: clippy lints
├── _test.yml        # Reusable: cargo test
├── _deny.yml        # Reusable: cargo-deny bans check (optional)
├── _sqlx.yml        # Reusable: sqlx migrations + check (optional)
├── _e2e.yml         # Reusable: end-to-end tests (optional)
└── _deploy.yml      # Reusable: deployment (optional)
```

**Naming convention:** Underscore prefix (`_workflow.yml`) indicates reusable/private workflows.

## Before Creating Workflows

**Auto-detect project features:**

1. Check for `migrations/` directory → suggest `_sqlx.yml`
2. Check `Cargo.toml` for feature flags → suggest feature matrix
3. Check for `e2e/` or `tests/e2e/` directory → suggest `_e2e.yml`
4. Check if project has existing CI → offer to replace or augment

**Ask the user:**

1. Should we test multiple Rust versions (stable/nightly)?
   - If yes: nightly gets `continue-on-error: true`
2. If features detected: Should we matrix test different feature combinations?
3. Is there a deployment step after CI passes?

## Core Preferences

| Setting | Value |
|---------|-------|
| Toolchain action | `actions-rust-lang/setup-rust-toolchain@v1` (NOT dtolnay) |
| Caching | Built-in via toolchain action (uses Swatinem/rust-cache) |
| Tool installation | `cargo-binstall` for additional tools |
| Clippy strictness | Always `-D warnings` |
| Concurrency | NO `cancel-in-progress` for PRs (want full failure context) |

## CI Triggers

```yaml
on:
  push:
    branches: [main]
  pull_request:
```

All PRs trigger CI. Only pushes to main (not feature branches).

## Workflow Templates

### ci.yml (Orchestrator)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  fmt:
    uses: ./.github/workflows/_fmt.yml

  clippy:
    uses: ./.github/workflows/_clippy.yml

  test:
    uses: ./.github/workflows/_test.yml

  # Optional - add if cargo-deny is configured
  deny:
    uses: ./.github/workflows/_deny.yml

  # Optional - add if project uses sqlx
  sqlx:
    uses: ./.github/workflows/_sqlx.yml

  # Optional - add if e2e tests exist
  e2e:
    uses: ./.github/workflows/_e2e.yml
    needs: [test]  # Run after unit tests pass

  # Optional - deployment after CI passes
  deploy:
    needs: [fmt, clippy, test]  # Add other required jobs
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    uses: ./.github/workflows/_deploy.yml
    secrets: inherit
```

### _fmt.yml (Rustfmt)

```yaml
name: Rustfmt

on:
  workflow_call:

env:
  CARGO_TERM_COLOR: always

jobs:
  fmt:
    name: Check Formatting
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: actions-rust-lang/setup-rust-toolchain@v1
        with:
          toolchain: stable
          components: rustfmt

      - name: Check formatting
        run: cargo fmt --all -- --check
```

### _clippy.yml (Clippy)

```yaml
name: Clippy

on:
  workflow_call:

env:
  CARGO_TERM_COLOR: always

jobs:
  clippy:
    name: Clippy
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: actions-rust-lang/setup-rust-toolchain@v1
        with:
          toolchain: stable
          components: clippy

      - name: Run clippy
        run: cargo clippy --workspace --all-targets -- -D warnings
```

### _test.yml (Tests)

```yaml
name: Test

on:
  workflow_call:

env:
  CARGO_TERM_COLOR: always

jobs:
  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: actions-rust-lang/setup-rust-toolchain@v1
        with:
          toolchain: stable

      - name: Run tests
        run: cargo test --workspace
```

### _deny.yml (Cargo Deny)

```yaml
name: Cargo Deny

on:
  workflow_call:

jobs:
  deny:
    name: Cargo Deny
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install cargo-binstall
        run: curl -L --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/cargo-bins/cargo-binstall/main/install-from-binstall-release.sh | bash

      - name: Install cargo-deny
        run: cargo binstall --no-confirm cargo-deny

      - name: Run cargo deny
        run: cargo deny check bans
```

**Note:** Requires `deny.toml` in project root. Create minimal one:

```toml
[bans]
multiple-versions = "warn"
wildcards = "allow"
```

### _sqlx.yml (SQLx Check)

Only include if project has `migrations/` directory.

```yaml
name: SQLx Check

on:
  workflow_call:

env:
  CARGO_TERM_COLOR: always

jobs:
  sqlx:
    name: SQLx Check
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    env:
      DATABASE_URL: postgres://postgres:postgres@localhost:5432/test_db

    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: actions-rust-lang/setup-rust-toolchain@v1
        with:
          toolchain: stable

      - name: Install cargo-binstall
        run: curl -L --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/cargo-bins/cargo-binstall/main/install-from-binstall-release.sh | bash

      - name: Install sqlx-cli
        run: cargo binstall --no-confirm sqlx-cli

      - name: Run migrations
        run: sqlx migrate run

      - name: Check sqlx prepare
        run: cargo sqlx prepare --workspace --check
```

**Adjust migration path** if not in root (e.g., `cd crates/mydb && sqlx migrate run`).

## Variant: Feature Matrix

When project has multiple features worth testing separately:

```yaml
# In _test.yml or _clippy.yml
jobs:
  test:
    name: Test (${{ matrix.features-name }})
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - features-name: "all"
            features-args: "--all-features"
          - features-name: "default"
            features-args: ""
          - features-name: "no-default"
            features-args: "--no-default-features"
          # Add specific feature combos as needed:
          # - features-name: "feature-x-only"
          #   features-args: "--no-default-features --features feature-x"
    steps:
      # ... setup steps ...
      - name: Run tests
        run: cargo test --workspace ${{ matrix.features-args }}
```

## Variant: Multiple Rust Versions

When testing stable and nightly:

```yaml
# In ci.yml - call the workflow twice with different inputs
jobs:
  test-stable:
    uses: ./.github/workflows/_test.yml
    with:
      rust-version: stable

  test-nightly:
    uses: ./.github/workflows/_test.yml
    with:
      rust-version: nightly
      continue-on-error: true
```

```yaml
# In _test.yml - accept rust-version input
on:
  workflow_call:
    inputs:
      rust-version:
        required: false
        type: string
        default: stable
      continue-on-error:
        required: false
        type: boolean
        default: false

jobs:
  test:
    name: Test (${{ inputs.rust-version }})
    runs-on: ubuntu-latest
    continue-on-error: ${{ inputs.continue-on-error }}
    steps:
      - uses: actions/checkout@v4

      - name: Setup Rust
        uses: actions-rust-lang/setup-rust-toolchain@v1
        with:
          toolchain: ${{ inputs.rust-version }}

      - name: Run tests
        run: cargo test --workspace
```

## Variant: With Postgres Service (for tests)

Add to `_test.yml` when tests need a database:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    env:
      DATABASE_URL: postgres://postgres:postgres@localhost:5432/test_db

    steps:
      # ... rest of steps
```

## Variant: Deployment Skeleton

```yaml
name: Deploy

on:
  workflow_call:
    secrets:
      # Add required secrets
      DEPLOY_TOKEN:
        required: true

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Add deployment steps here
      # Common patterns:
      # - Fly.io: flyctl deploy
      # - Docker: build and push to registry
      # - AWS: deploy via CDK/Terraform
```

## Implementation Checklist

When setting up CI for a project:

1. [ ] Create `.github/workflows/` directory
2. [ ] Add `ci.yml` orchestrator
3. [ ] Add `_fmt.yml` (always)
4. [ ] Add `_clippy.yml` (always)
5. [ ] Add `_test.yml` (always)
6. [ ] Check for `migrations/` → add `_sqlx.yml` if present
7. [ ] Ask about cargo-deny → add `_deny.yml` + `deny.toml`
8. [ ] Check for e2e tests → add `_e2e.yml` if present
9. [ ] Ask about deployment → add `_deploy.yml` skeleton
10. [ ] Ask about Rust version matrix → modify workflows if needed
11. [ ] Ask about feature matrix → modify workflows if needed
