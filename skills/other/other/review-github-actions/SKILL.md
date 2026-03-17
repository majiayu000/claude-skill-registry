---
name: review-github-actions
description: Reviews GitHub Actions workflow files for best practices, ensuring workflows delegate commands to Makefile targets for maintainability and DRY principles. Enforces clean CI/CD patterns including proper caching, matrix strategies, and security practices.
disable-model-invocation: false
allowed-tools:
  - read_file
  - grep_search
  - semantic_search
  - replace_string_in_file
  - multi_replace_string_in_file
---

# GitHub Actions Workflow Review

This skill enforces clean GitHub Actions patterns with emphasis on delegating execution to Makefile commands rather than inline scripts.

## Project-Specific Rules

### No Windows CI

**CRITICAL**: Never use `windows-latest` in any GitHub Actions workflow for this project. Windows is not a target platform, and Windows CI is slow and expensive. Only use `ubuntu-latest` and `macos-latest` in matrix strategies.

## Core Principles

### 1. Makefile Delegation (DRY Principle)

**Standard**: Workflows orchestrate, Makefiles execute. All `run:` commands should invoke Makefile targets.

**GOOD** - Delegates to Makefile:
```yaml
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - run: make check
```

**BAD** - Inline command duplicates logic:
```yaml
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - run: cargo check --all-features --all-targets
```

**Why**: Commands defined in Makefile create single source of truth, work locally and in CI, reduce workflow complexity.

### 2. Proper Caching Strategy

**Standard**: Cache dependencies aggressively to reduce build times.

**GOOD** - Rust caching:
```yaml
steps:
  - uses: actions/checkout@v4
  - uses: dtolnay/rust-toolchain@stable
  - uses: Swatinem/rust-cache@v2
  - run: make build
```

**BAD** - No caching:
```yaml
steps:
  - uses: actions/checkout@v4
  - uses: dtolnay/rust-toolchain@stable
  - run: make build  # Rebuilds everything every time
```

**Why**: Proper caching significantly reduces CI run times and costs.

### 3. Matrix Builds for Cross-Platform

**Standard**: Use matrix strategy for testing across multiple environments. **Never include `windows-latest`** - Windows CI is slow, expensive, and not a target platform for this project.

**GOOD** - Matrix for multi-platform (no Windows):
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - run: make test
```

**BAD** - Includes Windows:
```yaml
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]  # NO! Remove windows-latest
```

**BAD** - Separate jobs per platform:
```yaml
jobs:
  test-ubuntu:
    runs-on: ubuntu-latest
    steps: [...]
  test-macos:
    runs-on: macos-latest
    steps: [...]
  test-windows:
    runs-on: windows-latest
    steps: [...]
```

**Why**: Matrix reduces duplication, easier to maintain, clearer structure. Windows is excluded due to slow builds and not being a target platform.

### 4. Fail-Fast Strategy

**Standard**: Consider fail-fast for quick feedback loops.

**GOOD** - Fail-fast for CI:
```yaml
strategy:
  fail-fast: true
  matrix:
    os: [ubuntu-latest, macos-latest]
```

**GOOD** - Continue for comprehensive testing:
```yaml
strategy:
  fail-fast: false  # Complete all matrix runs
  matrix:
    os: [ubuntu-latest, macos-latest]
```

**Why**: Fail-fast saves time in development; continuing shows full test results.

### 5. Concurrency Control

**Standard**: Cancel in-progress runs for the same branch to save resources.

**GOOD** - Branch-level concurrency:
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**BAD** - No concurrency control:
```yaml
# Multiple runs for same branch consume resources unnecessarily
```

**Why**: Prevents resource waste, faster feedback on latest changes.

### 6. Minimal Permissions

**Standard**: Grant only required permissions (principle of least privilege).

**GOOD** - Explicit minimal permissions:
```yaml
jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # Only what's needed
    steps: [...]
```

**BAD** - Excessive permissions:
```yaml
permissions: write-all  # Security anti-pattern
```

**Why**: Security best practice, limits blast radius of compromised workflows.

### 7. Environment Variables

**Standard**: Set environment variables at workflow or job level, not inline.

**GOOD** - Top-level environment:
```yaml
env:
  CARGO_TERM_COLOR: always
  RUSTFLAGS: -Dwarnings

jobs:
  check:
    steps:
      - run: make check
```

**BAD** - Inline environment:
```yaml
jobs:
  check:
    steps:
      - run: CARGO_TERM_COLOR=always RUSTFLAGS=-Dwarnings make check
```

**Why**: Centralized configuration, easier to maintain, visible to all steps.

### 8. Self-Documenting Names

**Standard**: Use descriptive job and step names that explain purpose.

**GOOD** - Clear naming:
```yaml
jobs:
  build-and-test:
    name: Build and test on ${{ matrix.os }}
    steps:
      - name: Check out repository
        uses: actions/checkout@v4
      - name: Set up Rust toolchain
        uses: dtolnay/rust-toolchain@stable
      - name: Run all tests
        run: make test
```

**BAD** - Vague naming:
```yaml
jobs:
  job1:
    steps:
      - uses: actions/checkout@v4
      - run: make test
```

**Why**: Readable workflow runs, easier debugging, clear CI/CD pipeline.

### 9. Secrets Management

**Standard**: Use GitHub Secrets for sensitive data, never hardcode.

**GOOD** - Proper secrets:
```yaml
steps:
  - name: Deploy to production
    run: make deploy
    env:
      API_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

**BAD** - Hardcoded secrets:
```yaml
steps:
  - run: |
      export API_TOKEN="sk-1234567890abcdef"  # NEVER DO THIS
      make deploy
```

**Why**: Security, prevents credential leaks in version control.

### 10. Artifact Management

**Standard**: Use artifacts for build outputs that need to be shared or preserved.

**GOOD** - Upload/download artifacts:
```yaml
jobs:
  build:
    steps:
      - run: make build
      - uses: actions/upload-artifact@v4
        with:
          name: binary-${{ matrix.os }}
          path: target/release/ff
  
  release:
    needs: build
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: binary-${{ matrix.os }}
```

**BAD** - No artifact sharing:
```yaml
jobs:
  build:
    steps:
      - run: make build
      # Binary is lost after job completes
  
  release:
    steps:
      - run: make build  # Rebuilds unnecessarily
```

**Why**: Efficient resource usage, faster pipelines, reliable build outputs.

## Review Checklist

When reviewing workflow files, check:

1. **Project Rules**
   - [ ] **No `windows-latest`** - Only use `ubuntu-latest` and `macos-latest`
   - [ ] No Windows targets in release builds

2. **Makefile Delegation**
   - [ ] All `run:` steps use Makefile targets
   - [ ] No inline shell scripts duplicating Makefile logic
   - [ ] Complex commands are in Makefile, not YAML

3. **Efficiency**
   - [ ] Appropriate caching strategy implemented
   - [ ] Matrix builds for multi-platform testing (Linux + macOS only)
   - [ ] Concurrency control to cancel stale runs
   - [ ] Artifacts used for build output sharing

4. **Security**
   - [ ] Minimal permissions granted
   - [ ] Secrets properly used via `${{ secrets.NAME }}`
   - [ ] No hardcoded credentials or tokens
   - [ ] Actions pinned to specific versions/SHAs

5. **Maintainability**
   - [ ] Self-documenting job and step names
   - [ ] Environment variables centralized
   - [ ] DRY principle followed (no duplication)
   - [ ] Clear workflow structure

6. **Quality**
   - [ ] Fail-fast strategy considered for context
   - [ ] Branch/path filters appropriate
   - [ ] Timeout values set for long-running jobs
   - [ ] Error handling appropriate

## Common Anti-Patterns

### Inline Script Blocks

**BAD**:
```yaml
- run: |
    set -e
    cargo build --release
    strip target/release/ff
    tar czf ff-${{ matrix.target }}.tar.gz -C target/release ff
```

**GOOD**:
```yaml
- run: make package TARGET=${{ matrix.target }}
```

### Manual Environment Setup

**BAD**:
```yaml
- run: |
    curl -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
    cargo build
```

**GOOD**:
```yaml
- uses: dtolnay/rust-toolchain@stable
- run: make build
```

### Duplicated Logic Across Workflows

**BAD**:
```yaml
# In ci.yml
- run: cargo test --all-features

# In release.yml
- run: cargo test --all-features

# In nightly.yml
- run: cargo test --all-features
```

**GOOD**:
```yaml
# In all workflows
- run: make test
```

## Action Version Pinning

**Standard**: Pin actions to specific SHAs for security and reproducibility.

**GOOD** - Pinned to SHA:
```yaml
- uses: actions/checkout@8f4b7f84864484a7bf31766abe9204da3cbe65b3  # v4.0.0
```

**ACCEPTABLE** - Major version:
```yaml
- uses: actions/checkout@v4
```

**BAD** - Default branch:
```yaml
- uses: actions/checkout@main  # Unstable, may break
```

**Why**: SHA pinning prevents supply chain attacks, ensures reproducible builds.

## Workflow Triggers

**Standard**: Use appropriate triggers for workflow purpose.

**CI Workflow**:
```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
```

**Release Workflow**:
```yaml
on:
  push:
    tags: ['v*.*.*']
```

**Scheduled Workflow**:
```yaml
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
```

## Implementation Example

See [examples.md](./examples.md) for comprehensive workflow examples including:
- Complete CI pipeline
- Multi-platform release workflow
- Dependency update automation
- Security scanning integration
- Deployment workflows

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Security Hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

---

## Verification

**After every unit of work, run `make ci` before moving on.** This ensures format, clippy, tests, and docs all pass. Do not proceed to the next task until CI is green.
