---
name: strict-clippy-check
description: Enforces zero-tolerance code quality policy using Clippy with strict lints, all warnings treated as errors
user-invocable: true
---

# Strict Clippy Check Skill

## Purpose
Enforces Pierre's zero-tolerance code quality policy using Clippy with strict lints. All warnings are treated as errors per CLAUDE.md standards.

## CLAUDE.md Compliance
- ✅ Enforces zero tolerance for `unwrap()`, `expect()`, `panic!()`
- ✅ Validates no `anyhow::anyhow!()` usage
- ✅ Checks for proper error handling patterns
- ✅ Enforces code quality standards

## Usage
Run this skill:
- Before every commit
- Before creating pull requests
- After refactoring
- During code reviews

## Prerequisites
- Rust toolchain installed
- Clippy component (`rustup component add clippy`)

## Commands

### Standard Strict Check
```bash
# Run Clippy with strict lints (Cargo.toml configuration)
cargo clippy --all-targets --all-features -- -D warnings
```

### Explicit Strict Check (Legacy)
```bash
# Run with all lint groups enabled
cargo clippy --all-targets --all-features -- \
  -W clippy::all \
  -W clippy::pedantic \
  -W clippy::nursery \
  -D warnings
```

### Specific Lint Categories
```bash
# Check only error handling patterns
cargo clippy --all-targets -- \
  -D clippy::unwrap_used \
  -D clippy::expect_used \
  -D clippy::panic

# Check performance lints
cargo clippy --all-targets -- \
  -W clippy::clone_on_copy \
  -W clippy::redundant_clone
```

### Fix Auto-Fixable Issues
```bash
# Apply automatic fixes (use with caution)
cargo clippy --fix --all-targets --allow-dirty -- -D warnings

# Preview fixes without applying
cargo clippy --fix --all-targets --allow-dirty --dry-run -- -D warnings
```

## Linting Configuration

Pierre uses `Cargo.toml` lints configuration (eliminates need for bash script flags):

```toml
[lints.clippy]
all = { level = "deny", priority = -1 }
pedantic = { level = "deny", priority = -1 }
nursery = { level = "deny", priority = -1 }

# Critical error handling
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
```

## Common Issues & Fixes

### Issue: `unwrap()` detected
```rust
// ❌ Bad
let value = some_option.unwrap();

// ✅ Good
let value = some_option.ok_or(AppError::NotFound)?;
```

### Issue: `expect()` detected
```rust
// ❌ Bad
let config = load_config().expect("Failed to load config");

// ✅ Good
let config = load_config()
    .map_err(|e| AppError::ConfigError(e.to_string()))?;
```

### Issue: `panic!()` detected
```rust
// ❌ Bad
if user_id.is_none() {
    panic!("User ID required");
}

// ✅ Good
let user_id = user_id.ok_or(AppError::MissingUserId)?;
```

### Issue: `anyhow::anyhow!()` detected
```rust
// ❌ Bad (CLAUDE.md violation)
return Err(anyhow::anyhow!("Database connection failed"));

// ✅ Good (use structured errors)
return Err(AppError::DatabaseError(
    DatabaseError::ConnectionFailed
));
```

### Issue: Cast warnings
```rust
// ❌ Might truncate
let small = large_value as u8;

// ✅ Safe conversion
let small = u8::try_from(large_value)
    .map_err(|_| AppError::ConversionError)?;
```

### Issue: Missing documentation
```rust
// ❌ No docs
pub fn calculate_vdot(distance: f64, time: f64) -> f64 { }

// ✅ Documented
/// Calculates VDOT (running performance metric) using Daniels' formula
///
/// # Arguments
/// * `distance` - Distance in meters
/// * `time` - Time in seconds
///
/// # Returns
/// VDOT score (typically 20-85)
///
/// # Errors
/// Returns `AlgorithmError` if inputs are invalid
pub fn calculate_vdot(distance: f64, time: f64) -> Result<f64, AlgorithmError> { }
```

## Allowed Exceptions

Per CLAUDE.md, certain patterns are allowed in specific contexts:

### Test Files
```rust
// Allowed in tests/bin with "// Safe:" comment
// Safe: Test setup with known valid values
let config = load_test_config().unwrap();
```

### Binary Files
```rust
// Allowed in src/bin/ with justification
// Safe: CLI application, error printed to stderr
let args = Args::parse().expect("Failed to parse args");
```

## Integration with CI/CD

Clippy runs in GitHub Actions:
```yaml
# .github/workflows/rust.yml
- name: Clippy
  run: cargo clippy --all-targets --all-features -- -D warnings
```

## Success Criteria
- ✅ Zero Clippy warnings
- ✅ All error handling uses `Result<T, E>`
- ✅ No `unwrap()` in production code (src/)
- ✅ No `panic!()` in production code
- ✅ No `anyhow::anyhow!()` anywhere
- ✅ Public APIs documented

## Pre-Commit Integration

Install git hooks:
```bash
git config core.hooksPath .githooks
```

This runs Clippy automatically before commits.

## Troubleshooting

**Issue:** Too many warnings, can't fix all at once
```bash
# Focus on critical issues first
cargo clippy --all-targets -- \
  -D clippy::unwrap_used \
  -D clippy::expect_used \
  -D clippy::panic
```

**Issue:** False positive in generated code
```bash
# Suppress in specific context only (must justify)
#[allow(clippy::specific_lint)]  // Justification: generated code
```

**Issue:** Lint not recognized
```bash
# Update Rust/Clippy
rustup update
rustup component add clippy
```

## Related Files
- `Cargo.toml` - Lint configuration (lines 141-213)
- `scripts/ci/lint-and-test.sh` - Combined linting + testing
- `scripts/ci/architectural-validation.sh` - Pattern validation

## Related Skills
- `validate-architecture` - Architectural pattern validation
- `check-no-secrets` - Secret detection
