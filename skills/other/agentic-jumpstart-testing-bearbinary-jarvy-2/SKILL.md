---
name: "agentic-jumpstart-testing"
description: "Testing guidelines for Jarvy CLI - unit testing patterns, integration tests with assert_cmd, test environment variables, platform-specific testing, and CI coverage strategies."
---

# Testing Guidelines

This skill provides testing patterns and strategies for the Jarvy CLI project.

## Test Organization

### Unit Tests Location

Unit tests live alongside code:

```rust
// src/tools/git/git.rs

pub fn ensure(min_hint: &str) -> Result<(), InstallError> {
    // Implementation
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ensure_parses_version() {
        // Test implementation
    }
}
```

### Integration Tests Location

```
tests/
├── cli_dispatch.rs      # Command routing
├── cli_config_errors.rs # Config error handling
├── tools_install.rs     # Tool installation
└── ...
```

## Environment Variables

### JARVY_TEST_MODE=1

Disables interactive prompts:

```rust
#[test]
fn test_setup() {
    Command::cargo_bin("jarvy")
        .unwrap()
        .env("JARVY_TEST_MODE", "1")
        .arg("setup")
        .assert()
        .success();
}
```

### JARVY_FAST_TEST

Skips external command execution:

```rust
#[test]
fn test_config_parsing() {
    Command::cargo_bin("jarvy")
        .unwrap()
        .env("JARVY_FAST_TEST", "1")
        .env("JARVY_TEST_MODE", "1")
        .arg("setup")
        .assert()
        .success();
}
```

### JARVY_RUN_EXTERNAL_CMDS_IN_TEST

Enables external commands in unit tests (use sparingly):

```rust
#[test]
#[ignore]
fn test_actual_installation() {
    std::env::set_var("JARVY_RUN_EXTERNAL_CMDS_IN_TEST", "1");
    // Test that calls real commands
}
```

## Test Utilities

### make_config() Helper

```rust
use tempfile::TempDir;
use std::fs;

fn make_config(content: &str) -> TempDir {
    let temp_dir = TempDir::new().unwrap();
    let config_path = temp_dir.path().join("jarvy.toml");
    fs::write(&config_path, content).unwrap();
    temp_dir
}

#[test]
fn test_simple_config() {
    let temp = make_config(r#"
        [provisioner]
        git = "2.40"
    "#);

    Command::cargo_bin("jarvy")
        .unwrap()
        .env("JARVY_TEST_MODE", "1")
        .env("JARVY_FAST_TEST", "1")
        .arg("setup")
        .current_dir(temp.path())
        .assert()
        .success();
}
```

## Integration Testing with assert_cmd

### Basic CLI Invocation

```rust
use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_help() {
    Command::cargo_bin("jarvy")
        .unwrap()
        .arg("--help")
        .assert()
        .success()
        .stdout(predicate::str::contains("Usage:"));
}
```

### Testing Exit Codes

```rust
#[test]
fn test_config_error() {
    let temp = make_config("invalid toml {{{{");

    Command::cargo_bin("jarvy")
        .unwrap()
        .env("JARVY_TEST_MODE", "1")
        .arg("setup")
        .current_dir(temp.path())
        .assert()
        .code(2); // CONFIG_ERROR
}
```

### Predicate Assertions

```rust
use predicates::str::{contains, is_empty};

#[test]
fn test_output() {
    Command::cargo_bin("jarvy")
        .unwrap()
        .env("JARVY_TEST_MODE", "1")
        .arg("get")
        .assert()
        .success()
        .stdout(contains("tools"));
}
```

## Platform-Specific Testing

### Conditional Test Compilation

```rust
#[test]
#[cfg(target_os = "macos")]
fn test_homebrew() {
    // macOS-specific test
}

#[test]
#[cfg(target_os = "linux")]
fn test_apt() {
    // Linux-specific test
}

#[test]
#[cfg(target_os = "windows")]
fn test_winget() {
    // Windows-specific test
}
```

### Platform Test Modules

```rust
#[cfg(test)]
mod tests {
    #[cfg(target_os = "macos")]
    mod macos_tests {
        #[test]
        fn test_brew_install() { }
    }

    #[cfg(target_os = "linux")]
    mod linux_tests {
        #[test]
        fn test_apt_install() { }
    }
}
```

## Unit Testing Patterns

### Testing Tool Handlers

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version_parsing() {
        assert!(version_satisfies("2.40.0", "2.40"));
        assert!(!version_satisfies("2.39.0", "2.40"));
    }
}
```

### Testing Config Parsing

```rust
#[test]
fn test_simple_format() {
    let config = r#"
        [provisioner]
        git = "2.40"
    "#;

    let parsed: Config = toml::from_str(config).unwrap();
    assert_eq!(parsed.tools.get("git").unwrap().version, "2.40");
}

#[test]
fn test_detailed_format() {
    let config = r#"
        [provisioner]
        node = { version = "20.0", version_manager = true }
    "#;

    let parsed: Config = toml::from_str(config).unwrap();
    let node = parsed.tools.get("node").unwrap();
    assert!(node.version_manager);
}
```

## CI Configuration

### GitHub Actions

```yaml
test:
  runs-on: ${{ matrix.os }}
  strategy:
    matrix:
      os: [ubuntu-latest, macos-latest, windows-latest]
  steps:
    - uses: actions/checkout@v4
    - uses: dtolnay/rust-toolchain@stable
    - run: cargo test --verbose -- --show-output
      env:
        JARVY_TEST_MODE: "1"
        JARVY_FAST_TEST: "1"
```

### Coverage

```bash
cargo install cargo-llvm-cov
cargo llvm-cov --all-features --workspace --lcov --output-path lcov.info
```

## Test Categories

```rust
// Fast tests (default)
#[test]
fn test_config_parsing() { }

// Slow tests (run with --ignored)
#[test]
#[ignore]
fn test_actual_installation() { }

// Platform-specific
#[test]
#[cfg(target_os = "macos")]
fn test_homebrew() { }
```

## Running Tests

```bash
# All tests
cargo test --verbose -- --show-output

# Single test file
cargo test --test cli_dispatch -- --show-output

# Tests matching pattern
cargo test config -- --show-output

# Ignored (slow) tests
cargo test -- --ignored

# All including ignored
cargo test -- --include-ignored
```

## Best Practices

1. **Always set JARVY_TEST_MODE=1** to prevent interactive prompts
2. **Use JARVY_FAST_TEST** when not testing actual installation
3. **Keep unit tests fast** by mocking external commands
4. **Use platform-specific modules** with `#[cfg(target_os)]`
5. **Test error paths** - verify exit codes and messages
6. **Use tempfile for isolation** - temporary config files
7. **Mark slow tests with #[ignore]**
8. **Test both config formats** - simple and detailed
