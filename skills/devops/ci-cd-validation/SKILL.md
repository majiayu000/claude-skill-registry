---
name: CI/CD Validation & Merge Workflow
description: Pre-push validation checklist (cargo fmt, clippy with zero warnings, feature flag testing, test suite), CI monitoring, merge process, and release quality gates. Use when preparing to push code, validating changes before PR, running CI checks, merging PRs, or preparing releases.
---

# CI/CD Validation & Merge Workflow

This skill provides guidance on validation workflows, CI/CD processes, and merge procedures for cqlite.

## When to Use This Skill

- Running pre-push validation
- Preparing pull requests
- Monitoring CI pipeline
- Merging changes
- Preparing releases
- Troubleshooting CI failures

## Pre-Push Validation Checklist

See [validation-checklist.md](validation-checklist.md) for complete steps.

### Quick Validation

```bash
# Run all pre-push checks
./scripts/ci/validate-cleanup.sh
```

### Manual Step-by-Step

#### 1. Format Code
```bash
cargo fmt --all
git add -u
git commit -m "style: cargo fmt" || echo "No formatting needed"
```

#### 2. Clippy (Zero Warnings)
```bash
# MUST pass with -D warnings (warnings = errors)
cargo clippy --package cqlite-core --lib --all-features -- -D warnings
```

**Requirements:**
- Zero warnings
- Fix all issues before proceeding
- No `#[allow(clippy::...)]` without justification

#### 3. Build (Minimal Features)
```bash
# M1 scope: reading only, no default features
cargo build --package cqlite-core --no-default-features --features=all-compression
```

**Must succeed** - tests feature gate correctness.

#### 4. Build (All Features)
```bash
# Full feature set
cargo build --package cqlite-core --all-features
```

**Must succeed** - tests complete build.

#### 5. Run Tests (Library)
```bash
# Run all library tests
cargo test --package cqlite-core --lib --all-features
```

**Track test count** - should not decrease unexpectedly.

#### 6. Run Integration Tests
```bash
# Run integration tests
cargo test --test '*'
```

**Must pass** - validates end-to-end functionality.

#### 7. Coverage Check
```bash
# Generate coverage report
cargo tarpaulin --out Html --output-dir coverage/
```

**Target:** ≥90% coverage (PRD requirement)

## Feature Flag Testing

### M1 Feature Gates

**Core reading** (minimal):
```bash
cargo build --package cqlite-core \
    --no-default-features \
    --features=all-compression
```

**With benchmarks**:
```bash
cargo build --package cqlite-core \
    --no-default-features \
    --features=all-compression,benchmarks
```

**All features**:
```bash
cargo build --package cqlite-core --all-features
```

### Validate Feature Combinations

```bash
# Test feature matrix
for features in "all-compression" "all-compression,benchmarks" "all-features"; do
    echo "Testing: $features"
    cargo test --package cqlite-core --no-default-features --features=$features
done
```

## CI Pipeline

### GitHub Actions Workflow

Located: `.github/workflows/rust.yml`

**Jobs:**
1. **Format Check**
   - Runs `cargo fmt -- --check`
   - Fast fail if unformatted

2. **Clippy**
   - Runs with `-D warnings`
   - Zero warnings required

3. **Build Matrix**
   - Minimal features
   - All features
   - Multiple Rust versions (stable, nightly)

4. **Test Matrix**
   - Linux, macOS, Windows
   - Unit + integration tests

5. **Coverage**
   - Generates with tarpaulin
   - Uploads to Codecov
   - Gates on 90% threshold

### Monitoring CI

#### View Status
```bash
# List recent runs
gh run list --branch <branch-name> --limit 5

# View specific run
gh run view <run-id>

# Watch live
gh run watch <run-id>
```

#### Check Failures
```bash
# Download logs
gh run view <run-id> --log

# Download failed job logs
gh run view <run-id> --log-failed
```

## Merge Process

See [merge-process.md](merge-process.md) for detailed workflow.

### Prerequisites

Before merging:
- ✅ All CI checks green (10/10)
- ✅ Code review approved
- ✅ Branch up to date with main
- ✅ No conflicts
- ✅ Coverage ≥90%

### Merge Methods

**Squash merge** (default for cleanup):
```bash
gh pr merge <pr-number> --squash --delete-branch
```

**Merge commit** (for feature branches):
```bash
gh pr merge <pr-number> --merge --delete-branch
```

**Rebase** (for clean history):
```bash
gh pr merge <pr-number> --rebase --delete-branch
```

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Test additions/changes
- `docs`: Documentation
- `style`: Formatting
- `chore`: Build/tooling
- `cleanup`: Dead code removal

**Example:**
```
feat(parser): add support for duration CQL type

Implement deserialization for duration type consisting of
three VInts (months, days, nanoseconds).

- Add Duration variant to CqlType enum
- Implement parse_duration() with VInt handling
- Add property tests for edge cases

Closes #123
```

## Error Handling

### Clippy Failures

**Common issues:**
```bash
# Unused imports
cargo clippy --fix

# Unnecessary clones
# Review each and remove if safe

# Dead code warnings
# Expected for cleanup issues - document
```

### Test Failures

**Debugging:**
```bash
# Run single test with output
cargo test --test test_name -- --nocapture

# Run with backtrace
RUST_BACKTRACE=1 cargo test test_name

# Run with logging
RUST_LOG=debug cargo test test_name
```

### Build Failures

**Feature flag issues:**
```bash
# Check feature dependencies in Cargo.toml
[features]
default = ["all-compression"]
all-compression = ["lz4", "snap", "flate2"]
benchmarks = []  # NOT in default
```

**Dependency issues:**
```bash
# Clean and rebuild
cargo clean
cargo build
```

### Coverage Failures

**Below 90%:**
1. Identify uncovered lines
2. Add unit tests for uncovered code
3. Add property tests for edge cases
4. Document why coverage can't reach 90% (if applicable)

## Release Process

### Pre-Release Checklist

1. **All tests pass**
   ```bash
   cargo test --all-features
   ```

2. **Benchmarks run**
   ```bash
   cargo bench --features=benchmarks
   ```

3. **Documentation builds**
   ```bash
   cargo doc --no-deps --all-features
   ```

4. **Examples work**
   ```bash
   cargo run --example basic_usage
   ```

5. **Update CHANGELOG.md**
   ```markdown
   ## [0.1.0] - 2025-10-21
   ### Added
   - Initial release
   - Cassandra 5.0 SSTable parsing
   - All CQL types supported
   ```

6. **Update version**
   ```toml
   # Cargo.toml
   [package]
   version = "0.1.0"
   ```

### Creating Release

```bash
# Tag version
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0

# Create GitHub release
gh release create v0.1.0 \
    --title "v0.1.0 - Initial Release" \
    --notes-file RELEASE_NOTES.md \
    --draft  # Remove --draft when ready
```

## PRD Alignment

**Milestone M1** (Core Reading Library):
- 95% test coverage requirement
- Zero clippy warnings
- All CQL types validated

**Milestone M6** (Performance & Release):
- Benchmarks vs native tools
- Release packaging
- 90% codecov gate (stricter than M1)

## Common Scenarios

### Scenario 1: Pre-Push Validation

```bash
# Quick check before push
cargo fmt --all
cargo clippy --package cqlite-core --lib --all-features -- -D warnings
cargo test --package cqlite-core --lib

# If all pass:
git push origin feature/my-branch
```

### Scenario 2: CI Failure Investigation

```bash
# Check CI logs
gh run view --log

# Reproduce locally
cargo test --package cqlite-core --lib --features=all-compression

# Fix and push
git commit --amend
git push --force-with-lease origin feature/my-branch
```

### Scenario 3: Merge Blocked by Coverage

```bash
# Generate coverage report
cargo tarpaulin --out Html

# Open report
open tarpaulin-report.html

# Identify uncovered code
# Add tests
# Re-run coverage
```

## Automation

### Pre-Commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
set -e

echo "Running pre-commit checks..."

# Format
cargo fmt --all -- --check

# Clippy
cargo clippy --package cqlite-core --lib --all-features -- -D warnings

# Tests
cargo test --package cqlite-core --lib

echo "Pre-commit checks passed!"
```

### Pre-Push Hook

```bash
# .git/hooks/pre-push
#!/bin/bash
set -e

echo "Running pre-push validation..."

# Full validation
./scripts/ci/validate-cleanup.sh

echo "Pre-push validation passed!"
```

## Troubleshooting

### Tests Pass Locally, Fail in CI

**Possible causes:**
- Platform-specific issues (Windows vs Linux)
- Timing issues in async tests
- File path differences

**Solution:**
```bash
# Run in Docker matching CI environment
docker run --rm -v $(pwd):/workspace -w /workspace rust:latest \
    cargo test --all-features
```

### Clippy Different Results Locally vs CI

**Cause:** Different Rust versions

**Solution:**
```bash
# Check Rust version
rustc --version

# Use same as CI (check .github/workflows/rust.yml)
rustup install 1.70.0
rustup default 1.70.0
```

### Coverage Unstable

**Cause:** Non-deterministic code or flaky tests

**Solution:**
- Run coverage multiple times
- Identify unstable lines
- Fix flaky tests

## Best Practices

1. **Validate locally before pushing**
   - Saves CI resources
   - Faster feedback loop

2. **Fix clippy warnings immediately**
   - Don't accumulate tech debt
   - Easier to fix in context

3. **Keep PRs small**
   - Easier to review
   - Easier to revert if needed

4. **Write meaningful commit messages**
   - Helps future debugging
   - Documents intent

5. **Monitor CI actively**
   - Don't "fire and forget"
   - Fix failures promptly

## Next Steps

After validation passes:
1. Push branch
2. Create PR
3. Monitor CI
4. Address review feedback
5. Merge when green
6. Verify main CI stays green

## References

- [validation-checklist.md](validation-checklist.md) - Complete checklist
- [merge-process.md](merge-process.md) - Detailed merge workflow
- `.github/workflows/rust.yml` - CI configuration
- `scripts/ci/validate-cleanup.sh` - Validation script

