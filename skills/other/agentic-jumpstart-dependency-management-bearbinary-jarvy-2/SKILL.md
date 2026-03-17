---
name: "agentic-jumpstart-dependency-management"
description: "Dependency management guidelines for Jarvy - crate selection criteria, feature flag best practices, version management, security auditing with cargo-audit and cargo-deny."
---

# Dependency Management Guidelines

This skill provides guidance for managing Rust dependencies in the Jarvy project.

## Dependency Selection Criteria

### Prefer Standard Library First

Before adding external crates, verify stdlib cannot handle the need:

```rust
// PREFER: stdlib for simple operations
use std::fs;
use std::path::PathBuf;
use std::process::Command;

// AVOID: Adding crates for trivial functionality
```

### Evaluation Checklist

When considering a new dependency:

1. **Necessity**: Can this be implemented in <100 lines?
2. **Maintenance**: Is the crate actively maintained?
3. **Transitive deps**: How many dependencies does it bring?
4. **Compile time**: What is the build time impact?
5. **License**: Is it compatible (MIT, Apache-2.0, BSD)?

### Reuse Existing Dependencies

| Need | Use Existing |
|------|--------------|
| JSON | `serde_json` |
| YAML | `serde_yaml` |
| TOML | `toml` |
| Error types | `thiserror` |
| HTTP | `ureq` |
| Logging | `tracing` |
| CLI args | `clap` with derive |
| Interactive prompts | `inquire` |
| Unique IDs | `uuid` v7 |
| Platform dirs | `dirs` |

## Feature Flag Best Practices

### Minimize Enabled Features

```toml
# GOOD: Explicit minimal features
clap = { version = "4.5", features = ["derive"] }
uuid = { version = "1.10", features = ["v7"] }
serde = { version = "1.0", features = ["derive"] }
ureq = { version = "3.1", features = ["json"] }

# BAD: Enabling all features
# clap = { version = "4.5", features = ["full"] }
```

### Document Non-Obvious Features

```toml
# v7 provides time-ordered UUIDs for telemetry event ordering
uuid = { version = "1.10", features = ["v7"] }
```

### Disable Default Features When Appropriate

```toml
some-crate = { version = "1.0", default-features = false, features = ["needed"] }
```

## Version Management

### Version Specification

```toml
# Standard: Allow patch and minor updates
serde = "1.0"

# Specific: Pin only when necessary
opentelemetry-otlp = "0.31.0"
```

### Update Commands

```bash
# Update all dependencies
cargo update

# Update specific dependency
cargo update -p serde

# Check for outdated dependencies
cargo outdated
```

### Lockfile Management

- **Commit `Cargo.lock`**: This is an application, not a library
- **Review lockfile changes**: Check diffs for unexpected updates

## Security Auditing

### Automated Auditing

```bash
# Install audit tools
cargo install cargo-audit
cargo install cargo-deny

# Run security advisory check
cargo audit

# Comprehensive check (security, licenses, duplicates)
cargo deny check
```

### cargo-deny Configuration

Create `deny.toml`:

```toml
[advisories]
vulnerability = "deny"
unmaintained = "warn"
yanked = "deny"

[licenses]
unlicensed = "deny"
allow = ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Zlib"]

[bans]
multiple-versions = "warn"
wildcards = "deny"

[sources]
unknown-registry = "deny"
unknown-git = "deny"
```

### Security Workflow

1. **Pre-commit**: Run `cargo audit` locally
2. **CI Pipeline**: Run `cargo deny check` on every PR
3. **Weekly**: Automated dependency update PRs
4. **Release**: Full audit before publishing

## Adding New Dependencies

### Process

1. **Justify**: Document why needed
2. **Research**: Check alternatives and maintenance status
3. **Audit**: Run `cargo audit` after adding
4. **Minimize**: Enable only required features
5. **Test**: Verify compile time impact

### PR Template

```markdown
## New Dependency: `crate-name`

**Purpose**: [What functionality?]

**Alternatives Considered**:
- stdlib: [Why not sufficient?]

**Metrics**:
- Transitive dependencies: [count]
- Build time impact: [minimal/moderate/significant]
- Last updated: [date]

**Features Enabled**: [list and why]
```

## Build Optimization

### Current Build Configuration

```toml
[build]
rustc-wrapper = "sccache"
jobs = 16

[profile.dev]
opt-level = 1

[profile.release]
lto = "thin"
```

### Monitor Build Times

```bash
# Measure build time
cargo build --timings

# Generate HTML report
cargo build --timings=html
```

## Platform-Specific Dependencies

```toml
[target.'cfg(target_os = "macos")'.dependencies]
macos-crate = "1.0"

[target.'cfg(target_os = "windows")'.dependencies]
windows-crate = "1.0"
```

Verify cross-platform compilation:

```bash
cargo check --target x86_64-unknown-linux-gnu
cargo check --target x86_64-apple-darwin
cargo check --target x86_64-pc-windows-msvc
```

## Current Project Dependencies

### Runtime Dependencies

| Crate | Version | Purpose |
|-------|---------|---------|
| clap | 4.5.6 | CLI parsing |
| serde | 1.0.204 | Serialization |
| toml | 0.9.5 | Config parsing |
| thiserror | 2.0.16 | Error types |
| tracing | 0.1.40 | Logging |
| ureq | 3.1.2 | HTTP client |
| inquire | 0.9.1 | Interactive prompts |
| dirs | 6.0.0 | Platform directories |
| uuid | 1.10.0 | Unique IDs |
| machineid-rs | 1.2 | Machine fingerprint |

### Dev Dependencies

| Crate | Version | Purpose |
|-------|---------|---------|
| tempfile | 3.20.0 | Temp file handling |
| assert_cmd | 2.0.17 | CLI testing |

## Dependency Checklist

1. [ ] Checked if stdlib can handle the need
2. [ ] Reviewed existing dependencies for reuse
3. [ ] Minimized enabled features
4. [ ] Ran `cargo audit` after adding
5. [ ] Tested cross-platform compilation
6. [ ] Documented justification in PR
