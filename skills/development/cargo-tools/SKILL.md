---
name: cargo-tools
description: |
  Cargo ecosystem tools for testing (nextest), coverage (llvm-cov), and dependency analysis (machete).
  Use when running tests, measuring coverage, detecting unused dependencies, or optimizing CI pipelines.
  Triggers: "nextest", "coverage", "llvm-cov", "unused dependencies", "cargo-machete".
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
---

# Cargo Tools

Essential cargo ecosystem tools for testing, coverage, and dependency management.

## cargo-nextest (Testing)

Next-generation test runner with process isolation and parallel execution.

### Installation & Usage

```bash
cargo install cargo-nextest --locked

cargo nextest run                    # Run all tests
cargo nextest run test_name          # Run specific test
cargo nextest run -p package_name    # Run tests in package
cargo nextest run -- --ignored       # Run ignored tests
cargo nextest run --test-threads 4   # Control parallelism
```

### Test Filtering

```bash
cargo nextest run -E 'test(auth)'              # Match test name
cargo nextest run -E 'package(my_crate)'       # Match package
cargo nextest run -E 'test(auth) and not test(slow)'  # Complex filter
cargo nextest run -E 'kind(test)'              # Integration tests only
```

### Configuration (.config/nextest.toml)

```toml
[profile.default]
retries = 0
test-threads = 8
fail-fast = false
success-output = "never"
failure-output = "immediate"

[profile.ci]
retries = 2
fail-fast = true
slow-timeout = { period = "60s", terminate-after = 2 }

[profile.ci.junit]
path = "target/nextest/ci/junit.xml"

[test-groups.database]
max-threads = 1

[profile.default.overrides]
filter = 'test(db_)'
test-group = 'database'
```

### Notes

- Nextest does NOT support doctests. Run separately: `cargo test --doc`
- Each test runs in its own process for isolation
- Use profiles for different environments (default, ci, coverage)

## cargo-llvm-cov (Coverage)

Code coverage using LLVM instrumentation.

### Installation & Usage

```bash
cargo install cargo-llvm-cov
rustup component add llvm-tools-preview

cargo llvm-cov                    # Run with coverage
cargo llvm-cov --html             # Generate HTML report
cargo llvm-cov --lcov --output-path lcov.info  # LCOV format
cargo llvm-cov --json             # JSON format
cargo llvm-cov --text             # Text summary
```

### Coverage Thresholds

```bash
cargo llvm-cov --fail-under-lines 80
cargo llvm-cov --fail-under-functions 75
cargo llvm-cov --fail-under-branches 70  # Requires nightly
```

### With nextest

```bash
cargo llvm-cov nextest --html
cargo llvm-cov nextest --profile ci --lcov --output-path lcov.info
```

### Advanced Options

```bash
cargo llvm-cov --workspace --html           # All workspace members
cargo llvm-cov --all-features --html        # All features
cargo llvm-cov --ignore-filename-regex '.*generated.*'  # Exclude files
cargo llvm-cov --doc --html                 # Include doctests
cargo llvm-cov clean                        # Clean coverage data
```

### Branch Coverage (Nightly)

```bash
rustup toolchain install nightly
rustup component add llvm-tools-preview --toolchain nightly
cargo +nightly llvm-cov --branch --html
```

## cargo-machete (Unused Dependencies)

Fast detection of unused dependencies.

### Installation & Usage

```bash
cargo install cargo-machete

cargo machete                     # Check for unused deps
cargo machete --with-metadata     # Detailed output
cargo machete --fix               # Remove unused deps
cargo machete --workspace         # Check workspace
```

### Handling False Positives

Create `.cargo-machete.toml`:

```toml
[ignore]
dependencies = ["serde", "log"]

[ignore.my_crate]
dependencies = ["tokio"]
```

Or use inline comments in `Cargo.toml`:

```toml
[dependencies]
serde = "1.0"  # machete:ignore - used via derive macro
```

### Comparison with cargo-udeps

| Feature | cargo-machete | cargo-udeps |
|---------|---------------|-------------|
| Speed | Very fast | Slower |
| Accuracy | Good | Excellent |
| Rust version | Stable | Nightly required |

```bash
# Use both for best results
cargo machete                    # Fast check
cargo +nightly udeps             # Verify with udeps
```

## CI Integration

### GitHub Actions

```yaml
name: Rust CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: llvm-tools-preview

      - uses: taiki-e/install-action@v2
        with:
          tool: nextest,cargo-llvm-cov,cargo-machete

      - uses: Swatinem/rust-cache@v2

      - name: Run tests
        run: cargo nextest run --profile ci --all-features

      - name: Run doctests
        run: cargo test --doc --all-features

      - name: Check coverage
        run: |
          cargo llvm-cov nextest \
            --all-features \
            --fail-under-lines 80 \
            --lcov --output-path lcov.info

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: lcov.info
          token: ${{ secrets.CODECOV_TOKEN }}

      - name: Check unused dependencies
        run: cargo machete --with-metadata
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: cargo-nextest
        name: cargo nextest
        entry: cargo nextest run
        language: system
        pass_filenames: false
        files: \.rs$

      - id: cargo-machete
        name: cargo machete
        entry: cargo machete
        language: system
        pass_filenames: false
        files: Cargo.toml$
```

## Best Practices

**Testing:**
- Use nextest for faster parallel execution
- Run doctests separately: `cargo nextest run && cargo test --doc`
- Configure flaky test retries in CI profile
- Group resource-intensive tests with `test-groups`

**Coverage:**
- Use nextest with llvm-cov: `cargo llvm-cov nextest`
- Set coverage thresholds in CI
- Generate LCOV for coverage services (Codecov, Coveralls)
- Clean coverage data between runs: `cargo llvm-cov clean`

**Dependencies:**
- Run machete regularly in CI
- Document false positives with inline comments
- Verify critical projects with cargo-udeps
- Always run `cargo check` after `--fix`

## References

- [nextest documentation](https://nexte.st/)
- [cargo-llvm-cov](https://github.com/taiki-e/cargo-llvm-cov)
- [cargo-machete](https://github.com/bnjbvr/cargo-machete)
