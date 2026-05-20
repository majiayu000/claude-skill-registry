---
name: "agentic-jumpstart-architecture"
description: "Architecture guidelines for Jarvy CLI - codebase structure, tool implementation patterns, registry system, platform-specific code organization, and module conventions."
---

# Jarvy Architecture Guidelines

This skill provides comprehensive architecture guidance for the Jarvy CLI project.

## Project Overview

Jarvy is a cross-platform CLI tool that provisions development environments from a `jarvy.toml` config file using native package managers (Homebrew, apt/dnf, winget).

## Directory Structure

```
jarvy/
├── src/
│   ├── main.rs              # CLI entry point (clap derive macros)
│   ├── lib.rs               # Public re-exports for integration tests
│   ├── config.rs            # jarvy.toml parsing with serde
│   ├── error_codes.rs       # Standardized exit codes
│   ├── analytics.rs         # OpenTelemetry/tracing setup
│   ├── posthog.rs           # PostHog analytics client
│   ├── setup.rs             # Setup command implementation
│   ├── bootstrap.rs         # Bootstrap command implementation
│   ├── init.rs              # Global initialization logic
│   ├── report.rs            # Tool status reporting
│   ├── provisioner.rs       # Core provisioning orchestration
│   ├── tools/
│   │   ├── mod.rs           # Tool module registry and re-exports
│   │   ├── registry.rs      # Global OnceLock<RwLock<HashMap>> registry
│   │   ├── common.rs        # Shared utilities
│   │   ├── _template.rs     # Scaffold template for new tools
│   │   └── {tool}/          # Tool implementations
│   │       ├── mod.rs       # Re-exports the handler
│   │       └── {tool}.rs    # Implementation
│   └── tests/               # Unit test modules
├── tests/                   # Integration tests
├── crates/
│   └── cargo-jarvy/         # Cargo subcommand for scaffolding
└── Cargo.toml
```

## Core Patterns

### 1. Tool Implementation Pattern

Every tool follows a three-layer architecture:

```rust
// src/tools/{name}/{name}.rs

use crate::tools::common::{InstallError, cmd_satisfies, has, run};
#[cfg(target_os = "linux")]
use crate::tools::common::{detect_linux_pm, PkgOps, default_use_sudo};

/// Registry adapter: allows tools::add("{name}", version) to dispatch here
pub fn add_handler(min_hint: &str) -> Result<(), InstallError> {
    ensure(min_hint)
}

/// Main entry: probe first; install if needed
pub fn ensure(min_hint: &str) -> Result<(), InstallError> {
    if cmd_satisfies("{binary}", min_hint) {
        return Ok(());
    }
    install()
}

fn install() -> Result<(), InstallError> {
    #[cfg(target_os = "macos")]
    { return install_macos(); }
    #[cfg(target_os = "linux")]
    { return install_linux(); }
    #[cfg(target_os = "windows")]
    { return install_windows(); }
    #[allow(unreachable_code)]
    Err(InstallError::Unsupported)
}

#[cfg(target_os = "macos")]
fn install_macos() -> Result<(), InstallError> {
    if !has("brew") {
        return Err(InstallError::Prereq("Homebrew not found. Install https://brew.sh"));
    }
    run("brew", &["install", "{formula}"])?;
    Ok(())
}

#[cfg(target_os = "linux")]
fn install_linux() -> Result<(), InstallError> {
    let pm = detect_linux_pm().ok_or(InstallError::Prereq(
        "No supported package manager (apt/dnf/yum/zypper/pacman/apk)"
    ))?;
    let _ = PkgOps::update(pm, default_use_sudo());
    PkgOps::install(pm, "{package}", default_use_sudo())
}

#[cfg(target_os = "windows")]
fn install_windows() -> Result<(), InstallError> {
    if !has("winget") {
        return Err(InstallError::Prereq("winget not found"));
    }
    run("winget", &["install", "-e", "--id", "{WingetId}"])?;
    Ok(())
}
```

### 2. Registry Pattern

Tools are registered in a global thread-safe registry:

```rust
// src/tools/registry.rs
use std::sync::{OnceLock, RwLock};
use std::collections::HashMap;

pub type ToolAdder = fn(version: &str) -> Result<(), InstallError>;

static REGISTRY: OnceLock<RwLock<HashMap<String, ToolAdder>>> = OnceLock::new();

fn registry() -> &'static RwLock<HashMap<String, ToolAdder>> {
    REGISTRY.get_or_init(|| RwLock::new(HashMap::new()))
}

pub fn register_tool(name: &str, handler: ToolAdder) -> bool {
    let key = name.to_ascii_lowercase();
    let mut map = registry().write().expect("registry rwlock poisoned");
    map.insert(key, handler).is_none()
}

pub fn get_tool(name: &str) -> Option<ToolAdder> {
    let key = name.to_ascii_lowercase();
    let map = registry().read().expect("registry rwlock poisoned");
    map.get(&key).copied()
}

pub fn add(name: &str, version: &str) -> Result<(), InstallError> {
    let key = name.to_ascii_lowercase();
    let map = registry().read().expect("registry rwlock poisoned");
    if let Some(handler) = map.get(&key) {
        let f = *handler;
        drop(map);
        f(version)
    } else {
        Err(InstallError::Parse("unknown tool"))
    }
}
```

### 3. Error Handling Pattern

Use `thiserror` for structured errors:

```rust
// src/tools/common.rs
#[derive(thiserror::Error, Debug)]
pub enum InstallError {
    #[error("unsupported platform")]
    Unsupported,
    #[error("prerequisite missing: {0}")]
    Prereq(&'static str),
    #[error("invalid permissions: {0}")]
    InvalidPermissions(&'static str),
    #[error("command failed: {cmd} (code: {code:?})\n{stderr}")]
    CommandFailed { cmd: String, code: Option<i32>, stderr: String },
    #[error("io error: {0}")]
    Io(#[from] std::io::Error),
    #[error("parse error: {0}")]
    Parse(&'static str),
}
```

### 4. Platform Detection Pattern

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, serde::Deserialize, serde::Serialize)]
#[serde(rename_all = "lowercase")]
pub enum Os {
    Linux,
    Macos,
    Windows,
}

pub fn current_os() -> Os {
    #[cfg(target_os = "linux")]   { Os::Linux }
    #[cfg(target_os = "macos")]   { Os::Macos }
    #[cfg(target_os = "windows")] { Os::Windows }
}

#[cfg(target_os = "linux")]
pub fn detect_linux_pm() -> Option<PackageManager> {
    // Returns Apt, Dnf, Yum, Zypper, Pacman, or Apk
}
```

### 5. Configuration Pattern

Support both simple and detailed formats in `jarvy.toml`:

```toml
[privileges]
use_sudo = true

[privileges.per_os]
linux = true
macos = false

[provisioner]
# Simple format
git = "2.40"

# Detailed format
docker = { version = "24.0", version_manager = true, use_sudo = false }
```

Parsed with serde untagged enums:

```rust
#[derive(Deserialize)]
#[serde(untagged)]
pub enum ToolConfig {
    Detailed { version: String, version_manager: Option<bool>, use_sudo: Option<bool> },
    Simple(String),
}
```

## Adding a New Tool

### Step 1: Create the tool directory

```bash
cargo run -p cargo-jarvy -- new-tool {toolname}
# Or manually:
mkdir -p src/tools/{toolname}
```

### Step 2: Create mod.rs

```rust
// src/tools/{toolname}/mod.rs
#![allow(clippy::module_inception)]
pub mod {toolname};
```

### Step 3: Create the implementation

Use the template in `src/tools/_template.rs` as a starting point.

### Step 4: Register in src/tools/mod.rs

```rust
// Add module declaration
pub mod {toolname};

// In register_all():
let _ = register_tool("{toolname}", crate::tools::{toolname}::{toolname}::add_handler);
```

## Common Utilities Reference

### Command Execution

```rust
// Run a command and capture output
run(cmd: &str, args: &[&str]) -> Result<Output, InstallError>

// Run with optional sudo (non-Windows)
run_maybe_sudo(use_sudo: bool, cmd: &str, args: &[&str]) -> Result<Output, InstallError>

// Check if command exists on PATH
has(cmd: &str) -> bool

// Check if command output contains version prefix
cmd_satisfies(cmd: &str, min_prefix: &str) -> bool

// Require command or return error
require(cmd: &str, remediation: &'static str) -> Result<(), InstallError>

// Require one of multiple commands
require_any<'a>(candidates: &[&'a str], remediation: &'static str) -> Result<&'a str, InstallError>
```

### Package Manager Operations

```rust
// Update package lists
PkgOps::update(pm: PackageManager, use_sudo: Option<bool>) -> Result<(), InstallError>

// Install a package
PkgOps::install(pm: PackageManager, pkg: &str, use_sudo: Option<bool>) -> Result<(), InstallError>
```

## Exit Codes

| Code | Constant | Meaning |
|------|----------|---------|
| 0 | SUCCESS | Command completed successfully |
| 2 | CONFIG_ERROR | jarvy.toml missing or malformed |
| 3 | PREREQ_MISSING | Required package manager not found |
| 5 | PERMISSION_REQUIRED | Elevated privileges needed |

## CLI Structure

Commands defined with clap derive:

```rust
#[derive(Parser)]
#[clap(name = "jarvy", version, author, about)]
struct Cli {
    #[clap(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand)]
enum Commands {
    Setup { #[clap(short, long)] file: String },
    Bootstrap {},
    Configure {},
    Get { file: String, output_format: OutputFormat, output: Option<String> },
    #[clap(external_subcommand)]
    External(Vec<String>),
}
```

## Telemetry Architecture

- **PostHog**: Product analytics for usage events and errors
- **OpenTelemetry**: Structured logging via OTLP (HTTP/protobuf)
- **Configuration**: `~/.jarvy/config.toml` with `telemetry = true/false`
- **Environment**: `JARVY_OTLP_ENDPOINT` for custom collectors

## Key Dependencies

| Crate | Purpose |
|-------|---------|
| clap | CLI parsing with derive macros |
| serde/toml | Configuration parsing |
| thiserror | Structured error types |
| tracing | Logging and instrumentation |
| opentelemetry-otlp | Telemetry export |
| inquire | Interactive prompts |
| assert_cmd | Integration testing |

## Conventions

1. **Rust Edition**: 2024
2. **Commit Messages**: Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`)
3. **Formatting**: Always run `cargo fmt --all`
4. **Linting**: `cargo clippy --all-features -- -D warnings` must pass
5. **Dependencies**: Prefer stdlib and existing deps over new crates
6. **Platform Code**: Use `#[cfg(target_os = "...")]` attributes
