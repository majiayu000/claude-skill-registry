---
name: rust-quality-checker
description: Validate Rust code quality with rustfmt, clippy, cargo check, and security
  analysis. Use for Rust codebases to ensure idiomatic Rust code and best practices.
allowed-tools: Read, Bash, Grep, Glob
---

# Rust Quality Checker Skill

## Purpose

This skill provides comprehensive Rust code quality validation including formatting (rustfmt), linting (clippy), compilation checks (cargo check), testing (cargo test), security analysis (cargo audit), and best practices validation. Ensures code meets Rust idioms and project standards.

## When to Use

- Validating Rust code quality before commit
- Running pre-commit quality checks
- CI/CD quality gate validation
- Code review preparation
- Ensuring idiomatic Rust code
- Security vulnerability detection
- Performance optimization validation

## Quality Check Workflow

### 1. Environment Setup

**Verify Rust Toolchain:**
```bash
# Check Rust version
rustc --version

# Check Cargo version
cargo --version

# Check rustfmt
rustfmt --version

# Check clippy
cargo clippy --version
```

**Install/Update Components:**
```bash
# Update Rust toolchain
rustup update

# Install rustfmt (if not present)
rustup component add rustfmt

# Install clippy (if not present)
rustup component add clippy

# Install cargo-audit for security checks
cargo install cargo-audit

# Install cargo-tarpaulin for coverage
cargo install cargo-tarpaulin
```

**Deliverable:** Rust toolchain ready

---

### 2. Code Formatting Check (rustfmt)

**Check Formatting:**
```bash
# Check if code is formatted
cargo fmt -- --check

# Check with edition
cargo fmt --edition 2021 -- --check

# Check specific files
rustfmt --check src/main.rs

# Check with verbose output
cargo fmt --verbose -- --check
```

**Auto-Format Code:**
```bash
# Format all code
cargo fmt

# Format with specific edition
cargo fmt --edition 2021

# Format specific file
rustfmt src/main.rs
```

**Configuration (rustfmt.toml):**
```toml
# rustfmt.toml
edition = "2021"
max_width = 100
hard_tabs = false
tab_spaces = 4
newline_style = "Unix"
use_small_heuristics = "Default"
reorder_imports = true
reorder_modules = true
remove_nested_parens = true
fn_single_line = false
where_single_line = false
imports_granularity = "Crate"
group_imports = "StdExternalCrate"
```

**Deliverable:** Formatting validation report

---

### 3. Compilation Check (cargo check)

**Fast Compilation Check:**
```bash
# Basic check
cargo check

# Check with all features
cargo check --all-features

# Check workspace
cargo check --workspace

# Check specific package
cargo check --package my-package

# Check with verbose output
cargo check --verbose
```

**Full Compilation:**
```bash
# Build project
cargo build

# Build in release mode
cargo build --release

# Build with all features
cargo build --all-features

# Build all targets
cargo build --all-targets
```

**Deliverable:** Compilation status report

---

### 4. Linting (clippy)

**Run Clippy:**
```bash
# Basic clippy check
cargo clippy

# Deny all warnings
cargo clippy -- -D warnings

# Pedantic mode (strictest)
cargo clippy -- -W clippy::pedantic

# All clippy lints
cargo clippy -- -W clippy::all

# Nursery lints (unstable but useful)
cargo clippy -- -W clippy::nursery

# Check workspace
cargo clippy --workspace
```

**Clippy with Auto-Fix:**
```bash
# Fix clippy suggestions
cargo clippy --fix

# Fix with deny warnings
cargo clippy --fix -- -D warnings
```

**Configuration (clippy.toml or .clippy.toml):**
```toml
# clippy.toml
msrv = "1.70"  # Minimum Supported Rust Version

# Allow certain lints
allow = [
    "clippy::module_name_repetitions",
]

# Warn on these
warn = [
    "clippy::all",
    "clippy::pedantic",
    "clippy::cargo",
]

# Deny these
deny = [
    "clippy::unwrap_used",
    "clippy::expect_used",
    "clippy::panic",
]
```

**Deliverable:** Clippy lint report

---

### 5. Testing (cargo test)

**Run Tests:**
```bash
# Run all tests
cargo test

# Run with verbose output
cargo test -- --nocapture

# Run specific test
cargo test test_name

# Run tests in specific module
cargo test module::test_name

# Run doc tests only
cargo test --doc

# Run with all features
cargo test --all-features
```

**Test with Coverage:**
```bash
# Install tarpaulin
cargo install cargo-tarpaulin

# Generate coverage
cargo tarpaulin --out Html --out Xml

# Coverage with threshold
cargo tarpaulin --fail-under 80

# Coverage for workspace
cargo tarpaulin --workspace
```

**Deliverable:** Test execution and coverage report

---

### 6. Security Analysis (cargo audit)

**Dependency Security Check:**
```bash
# Install cargo-audit
cargo install cargo-audit

# Run security audit
cargo audit

# Audit with JSON output
cargo audit --json

# Audit and fix vulnerabilities
cargo audit fix

# Check for yanked crates
cargo audit --deny yanked
```

**Update Dependencies:**
```bash
# Install cargo-outdated
cargo install cargo-outdated

# Check for outdated dependencies
cargo outdated

# Update dependencies
cargo update

# Update specific dependency
cargo update -p dependency-name
```

**Deliverable:** Security audit report

---

### 7. Dependency Analysis

**Check Dependency Tree:**
```bash
# Show dependency tree
cargo tree

# Show dependencies for specific package
cargo tree --package my-package

# Show duplicates
cargo tree --duplicates

# Show dependencies with specific features
cargo tree --features feature-name

# Invert tree (show reverse dependencies)
cargo tree --invert
```

**Check Unused Dependencies:**
```bash
# Install cargo-udeps
cargo install cargo-udeps

# Find unused dependencies
cargo +nightly udeps
```

**Deliverable:** Dependency analysis report

---

### 8. Code Quality Checks

**Check for Unsafe Code:**
```bash
# Find unsafe blocks
grep -r "unsafe" src/

# Count unsafe blocks
grep -r "unsafe" src/ | wc -l

# Use cargo-geiger for unsafe usage report
cargo install cargo-geiger
cargo geiger
```

**Check Documentation:**
```bash
# Build documentation
cargo doc

# Check for missing docs
cargo rustdoc -- -D missing_docs

# Check documentation tests
cargo test --doc
```

**Deliverable:** Code quality assessment

---

### 9. Performance Analysis

**Benchmark Tests:**
```bash
# Run benchmarks
cargo bench

# Run specific benchmark
cargo bench benchmark_name

# Use criterion for better benchmarks
# Add to Cargo.toml:
# [dev-dependencies]
# criterion = "0.5"
cargo bench
```

**Performance Profiling:**
```bash
# Build with release mode
cargo build --release

# Use flamegraph
cargo install flamegraph
cargo flamegraph

# Use perf (Linux)
perf record --call-graph dwarf ./target/release/binary
perf report
```

**Deliverable:** Performance analysis report

---

### 10. Comprehensive Quality Check

**Run All Checks:**
```bash
#!/bin/bash
# scripts/quality-check.sh

set -e  # Exit on first error

echo "=== Rust Quality Checks ==="

echo "1. Code Formatting (rustfmt)..."
cargo fmt -- --check

echo "2. Compilation Check..."
cargo check --workspace

echo "3. Linting (clippy)..."
cargo clippy --workspace -- -D warnings

echo "4. Testing..."
cargo test --workspace

echo "5. Documentation Check..."
cargo doc --no-deps --document-private-items

echo "6. Security Audit..."
cargo audit

echo "7. Unused Dependencies..."
cargo +nightly udeps || true  # Don't fail build

echo "=== All Quality Checks Passed ✅ ==="
```

**Makefile Integration:**
```makefile
# Makefile
.PHONY: check fmt lint test quality

check:
	cargo check --workspace

fmt:
	cargo fmt

fmt-check:
	cargo fmt -- --check

lint:
	cargo clippy --workspace -- -D warnings

test:
	cargo test --workspace

quality: fmt-check check lint test
	@echo "All quality checks passed ✅"
```

**Deliverable:** Comprehensive quality report

---

## Quality Standards

### Code Formatting
- [ ] All code formatted with rustfmt
- [ ] Consistent use of Rust style guide
- [ ] Proper module organization
- [ ] Imports properly grouped
- [ ] Line length ≤ 100 characters

### Compilation
- [ ] Code compiles without errors
- [ ] No compiler warnings
- [ ] All features compile
- [ ] Documentation builds
- [ ] All targets build

### Linting
- [ ] No clippy warnings (with -D warnings)
- [ ] Pedantic lints addressed
- [ ] No unwrap/expect in production code
- [ ] Proper error handling
- [ ] No panic! in library code

### Testing
- [ ] All tests passing
- [ ] Coverage ≥ 80%
- [ ] Doc tests passing
- [ ] Integration tests passing
- [ ] No ignored tests (without reason)

### Security
- [ ] No known vulnerabilities
- [ ] Dependencies up to date
- [ ] No yanked crates
- [ ] Minimal unsafe code
- [ ] Unsafe code documented

### Code Quality
- [ ] Idiomatic Rust code
- [ ] Proper lifetime annotations
- [ ] Efficient error handling
- [ ] Documentation complete
- [ ] Examples provided

---

## Quality Check Matrix

| Check | Tool | Threshold | Auto-Fix |
|-------|------|-----------|----------|
| Formatting | rustfmt | Must pass | Yes |
| Compilation | cargo check | 0 errors | No |
| Linting | clippy | 0 warnings | Partial |
| Testing | cargo test | All pass | No |
| Coverage | tarpaulin | ≥ 80% | No |
| Security | cargo audit | 0 critical | Partial |
| Unsafe code | cargo geiger | Minimize | No |

---

## Pre-commit Integration

**Setup Git Hooks:**
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running Rust quality checks..."

# Format check
if ! cargo fmt -- --check; then
    echo "❌ Code not formatted. Run: cargo fmt"
    exit 1
fi

# Clippy
if ! cargo clippy -- -D warnings; then
    echo "❌ Clippy warnings found"
    exit 1
fi

# Tests
if ! cargo test --quiet; then
    echo "❌ Tests failed"
    exit 1
fi

echo "✅ All pre-commit checks passed"
```

**Make hook executable:**
```bash
chmod +x .git/hooks/pre-commit
```

**Deliverable:** Pre-commit hooks configured

---

## CI/CD Integration

**GitHub Actions Example:**
```yaml
# .github/workflows/rust-quality.yml
name: Rust Quality Checks

on: [push, pull_request]

env:
  CARGO_TERM_COLOR: always

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Rust toolchain
        uses: actions-rs/toolchain@v1
        with:
          profile: minimal
          toolchain: stable
          components: rustfmt, clippy
          override: true

      - name: Cache cargo registry
        uses: actions/cache@v3
        with:
          path: ~/.cargo/registry
          key: ${{ runner.os }}-cargo-registry-${{ hashFiles('**/Cargo.lock') }}

      - name: Check formatting
        run: cargo fmt -- --check

      - name: Check compilation
        run: cargo check --workspace

      - name: Run clippy
        run: cargo clippy --workspace -- -D warnings

      - name: Run tests
        run: cargo test --workspace --verbose

      - name: Check documentation
        run: cargo doc --no-deps --document-private-items

      - name: Security audit
        run: |
          cargo install cargo-audit
          cargo audit

      - name: Generate coverage
        run: |
          cargo install cargo-tarpaulin
          cargo tarpaulin --out Xml --fail-under 80

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./cobertura.xml
```

**Deliverable:** CI/CD quality pipeline

---

## Quality Check Troubleshooting

### rustfmt Formatting Failures

```bash
# Check what would change
cargo fmt -- --check

# Apply formatting
cargo fmt

# Check specific file
rustfmt --check src/main.rs
```

### Compilation Errors

```bash
# Check with verbose output
cargo check --verbose

# Clean and rebuild
cargo clean
cargo check

# Check dependencies
cargo tree
```

### Clippy Warnings

```bash
# Show detailed warnings
cargo clippy -- -W clippy::all

# Auto-fix suggestions
cargo clippy --fix

# Ignore specific warning (last resort)
#[allow(clippy::warning_name)]
```

### Test Failures

```bash
# Run with verbose output
cargo test -- --nocapture

# Run specific test
cargo test test_name -- --exact

# Show test output
cargo test -- --show-output
```

---

## Quality Report Template

```markdown
# Rust Quality Check Report

## Summary
- **Status**: ✅ All checks passed
- **Date**: 2024-01-15
- **Project**: my-rust-project

## Checks Performed

### Formatting (rustfmt)
- **Status**: ✅ PASS
- **Files Checked**: 42
- **Issues**: 0

### Compilation (cargo check)
- **Status**: ✅ PASS
- **Workspace**: All packages compile
- **Warnings**: 0

### Linting (clippy)
- **Status**: ✅ PASS
- **Warnings**: 0
- **Pedantic**: Enabled

### Testing (cargo test)
- **Status**: ✅ PASS
- **Tests**: 156 passed
- **Doc Tests**: 23 passed

### Coverage (tarpaulin)
- **Status**: ✅ PASS
- **Coverage**: 87% (target: 80%)

### Security (cargo audit)
- **Status**: ✅ PASS
- **Vulnerabilities**: 0
- **Yanked Crates**: 0

### Documentation
- **Status**: ✅ PASS
- **Docs Build**: Success
- **Missing Docs**: 0

## Details

All Rust quality checks passed successfully. Code is well-formatted, compiles cleanly, passes all lints, has good test coverage, and is secure.

## Recommendations

- Continue maintaining high test coverage
- Keep dependencies updated
- Document all public APIs
- Minimize unsafe code usage
```

---

## Integration with Code Quality Specialist

**Input:** Rust codebase quality check request
**Process:** Run all Rust quality tools and analyze results
**Output:** Comprehensive quality report with pass/fail status
**Next Step:** Report to code-quality-specialist for consolidation

---

## Best Practices

### Development
- Run `cargo fmt` on save (IDE integration)
- Enable clippy in IDE for real-time feedback
- Use `cargo watch` for continuous checking
- Fix warnings immediately

### Pre-Commit
- Run full quality check script
- Ensure all tests pass
- Verify no clippy warnings
- Check documentation builds

### CI/CD
- Run quality checks on every PR
- Fail build on warnings
- Generate coverage reports
- Track quality metrics over time
- Cache dependencies for speed

### Code Review
- Verify quality checks passed
- Review clippy suggestions
- Check test coverage
- Validate unsafe code usage

---

## Supporting Resources

- **Rust Book**: https://doc.rust-lang.org/book
- **rustfmt**: https://rust-lang.github.io/rustfmt
- **clippy**: https://rust-lang.github.io/rust-clippy
- **cargo audit**: https://github.com/rustsec/rustsec
- **tarpaulin**: https://github.com/xd009642/tarpaulin

---

## Success Metrics

- [ ] All code formatted with rustfmt
- [ ] Compilation passes with no warnings
- [ ] Zero clippy warnings
- [ ] All tests passing
- [ ] Coverage ≥ 80%
- [ ] No security vulnerabilities
- [ ] Documentation complete