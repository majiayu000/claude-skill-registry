---
name: github-workflows
description: Diagnose, fix, and optimize GitHub Actions workflows for Rust projects. Use when setting up CI/CD, troubleshooting workflow failures, optimizing build times with caching, or ensuring best practices for testing, linting, and releases.
---

# GitHub Workflows

Diagnose, fix, and optimize GitHub Actions workflows for Rust projects.

## Purpose

Set up robust CI/CD pipelines for Rust projects with proper caching, testing, linting, and release automation.

## Before Making Changes: Verify Current State

**ALWAYS start by checking the current workflow configuration before making any changes:**

### 1. Get Repository Information

```bash
# Get current repo info (owner, name)
gh repo view --json nameWithOwner,owner,name

# Example output: {"name":"rust-self-learning-memory","nameWithOwner":"d-o-hub/rust-self-learning-memory","owner":"d-o-hub"}
```

### 2. List Existing Workflows

```bash
# List all workflows
gh workflow list

# View workflow details
gh workflow view <workflow-name>
```

### 3. Check Recent Workflow Runs

```bash
# List recent runs
gh run list --limit 10

# View specific run details
gh run view <run-id>

# View run logs
gh run view <run-id> --log
```

### 4. Check Existing Workflow Files

```bash
# List workflow files
ls -la .github/workflows/

# Review each workflow
cat .github/workflows/*.yml
```

### 5. Check for Existing Issues

```bash
# Check for workflow-related issues
gh issue list --label ci --label github-actions --label workflow
```

**Only after understanding the current state should you suggest changes or additions.**

## Quick Reference

- **[Caching Strategies](caching-strategies.md)** - Manual cache, rust-cache, sccache, cache keys
- **[Troubleshooting](troubleshooting.md)** - Common issues, debugging, fixes
- **[Advanced Features](advanced-features.md)** - Coverage, security, benchmarking, quality gates, docs deployment
- **[Release Management](release-management.md)** - Automated releases, versioning, changelog generation, crates.io publishing

## Complete Rust CI Workflow (2025)

```yaml
name: Rust CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  CARGO_TERM_COLOR: always
  RUST_BACKTRACE: 1

jobs:
  check:
    name: Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable

      - name: Cache Rust dependencies
        uses: Swatinem/rust-cache@v2

      - name: Run cargo check
        run: cargo check --all --verbose

  fmt:
    name: Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          components: rustfmt

      - name: Check formatting
        run: cargo fmt -- --check

  clippy:
    name: Clippy
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy

      - name: Cache Rust dependencies
        uses: Swatinem/rust-cache@v2

      - name: Run clippy
        run: cargo clippy --all-targets --all-features -- -D warnings

  test:
    name: Test
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        rust: [stable]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v5

      - name: Install Rust
        uses: dtolnay/rust-toolchain@master
        with:
          toolchain: ${{ matrix.rust }}

      - name: Cache Rust dependencies
        uses: Swatinem/rust-cache@v2

      - name: Run tests
        run: cargo test --all --verbose

      - name: Run tests with all features
        run: cargo test --all-features --verbose

  coverage:
    name: Coverage
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable

      - name: Install cargo-llvm-cov
        run: cargo install cargo-llvm-cov

      - name: Generate coverage
        run: cargo llvm-cov --lcov --all-features --workspace --output-path lcov.info

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./lcov.info
          fail_ci_if_error: false
```

## Quick Start Workflows

### Minimal CI (Quick Feedback)

```yaml
name: Quick CI

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - run: cargo check --all
      - run: cargo fmt -- --check
      - run: cargo clippy -- -D warnings
      - run: cargo test --all
```

### Project-Specific: Self-Learning Memory CI

```yaml
name: Self-Learning Memory CI

on:
  push:
    branches: [main]
  pull_request:

env:
  CARGO_TERM_COLOR: always
  RUST_BACKTRACE: 1

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - run: cargo check --all --verbose

  fmt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: rustfmt
      - run: cargo fmt -- --check

  clippy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy
      - uses: Swatinem/rust-cache@v2
      - run: cargo clippy --all-targets -- -D warnings

  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    steps:
      - uses: actions/checkout@v5
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - run: cargo test --all --verbose
      - run: cargo test --all --all-features --verbose
```

## Common Tasks

### Setup Rust Toolchain

```yaml
# Stable
- uses: dtolnay/rust-toolchain@stable

# With components
- uses: dtolnay/rust-toolchain@stable
  with:
    components: rustfmt, clippy

# Specific version
- uses: dtolnay/rust-toolchain@master
  with:
    toolchain: 1.75.0
```

### Cache Dependencies

```yaml
# Recommended: Use rust-cache (automatic)
- uses: Swatinem/rust-cache@v2
  with:
    shared-key: "stable"
    save-if: ${{ github.ref == 'refs/heads/main' }}

# Alternative: Manual cache
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/registry/index
      ~/.cargo/registry/cache
      target
    key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
    restore-keys: |
      ${{ runner.os }}-cargo-
    save-always: true
```

See **[caching-strategies.md](caching-strategies.md)** for detailed caching options.

### Run Tests

```yaml
# All tests
- run: cargo test --all

# With verbose output
- run: cargo test --all --verbose

# With all features
- run: cargo test --all-features

# With backtrace
- run: RUST_BACKTRACE=1 cargo test --all

# Single-threaded (for race conditions)
- run: cargo test --all -- --test-threads=1
```

### Build Project

```yaml
# Development build
- run: cargo build --all

# Release build
- run: cargo build --release --all

# With timing info
- run: cargo build --release --timings
```

### Lint and Format

### Using cargo-llvm-cov (Recommended)
```yaml
- name: Install llvm-cov
  run: cargo install cargo-llvm-cov

- name: Generate coverage
  run: cargo llvm-cov --all-features --workspace --lcov --output-path lcov.info

- name: Upload to Codecov
  uses: codecov/codecov-action@v4
  with:
    files: lcov.info
    token: ${{ secrets.CODECOV_TOKEN }}
```

### Alternative: Generate multiple formats
```yaml
- name: Install llvm-cov
  run: cargo install cargo-llvm-cov

- name: Generate coverage (HTML + LCOV)
  run: |
    cargo llvm-cov --all-features --workspace --lcov --output-path lcov.info
    cargo llvm-cov --all-features --workspace --html --output-dir coverage

# Run clippy with fix
- run: cargo clippy --fix
```

## Best Practices (2025)

### DO:
✓ Use `actions/cache@v4` with `save-always: true`
✓ Use `hashFiles('**/Cargo.lock')` for cache keys
✓ Implement `restore-keys` for cache fallback
✓ Use `dtolnay/rust-toolchain` (not deprecated actions-rs)
✓ Split large caches to avoid 2GB limit
✓ Test on multiple platforms (matrix)
✓ Use `Swatinem/rust-cache@v2` for simplicity
✓ Cache both registry and target directory
✓ Set `CARGO_TERM_COLOR: always` for readable logs
✓ Use `continue-on-error` for experimental builds

### DON'T:
✗ Use deprecated `actions-rs/*` actions
✗ Create monolithic cache entries >2GB
✗ Cache without `restore-keys`
✗ Forget `save-always: true` for partial builds
✗ Cache `target/` across different jobs without unique keys
✗ Run expensive operations on every PR
✗ Use `actions/cache@v3` and `@v4` inconsistently
✗ Hardcode Rust version (use rust-toolchain file)

## Common Issues

Quick reference - see **[troubleshooting.md](troubleshooting.md)** for full details:

1. **Cache not saved on failure** → Use `save-always: true`
2. **Cache key mismatch** → Use `hashFiles()` and `restore-keys`
3. **Deprecated actions-rs** → Use `dtolnay/rust-toolchain`
4. **tar creation errors** → Use `rust-cache` or exclude problematic paths
5. **Files >2GB** → Split into smaller caches
6. **Workflow permissions** → Set `permissions:` in workflow
7. **Flaky tests** → Add retries with `nick-fields/retry@v2`

## Detailed Documentation

- **[Caching Strategies](caching-strategies.md)** - All caching methods, cache keys, performance tips
- **[Troubleshooting](troubleshooting.md)** - Issues, fixes, debugging, monitoring
- **[Advanced Features](advanced-features.md)** - Releases, coverage, security, multi-platform

## Integration with Project

**Before suggesting workflow changes:**
1. Run `gh repo view --json nameWithOwner,owner,name` to get actual repo info
2. Use the actual owner/repo names in all workflow examples
3. Check existing workflows with `gh workflow list`
4. Review current workflow files in `.github/workflows/`

**For this project (d-o-hub/rust-self-learning-memory):**
- The workflows ensure all `memory-core`, `memory-storage-turso`, and `memory-storage-redb` crates are tested across platforms
- Quality gates enforce 90% code coverage threshold
- Benchmarks track performance regressions
- Supply chain security with cargo-deny and cargo-audit

## Quick Checklist

Before committing workflow changes:
- [ ] Uses `actions/cache@v4` or `Swatinem/rust-cache@v2`
- [ ] Has `save-always: true` for caches
- [ ] Uses `dtolnay/rust-toolchain` (not actions-rs)
- [ ] Caches are <2GB each
- [ ] Has `restore-keys` for fallback
- [ ] Tests on multiple platforms (if needed)
- [ ] Clippy runs with `-D warnings`
- [ ] Format check included
- [ ] Permissions set appropriately
