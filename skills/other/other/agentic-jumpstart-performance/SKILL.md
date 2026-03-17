---
name: "agentic-jumpstart-performance"
description: "Performance optimization guidelines for Rust CLI tools. Covers efficient command execution, parallel processing, lazy initialization, allocation minimization, config parsing, and build optimizations for cross-platform CLI applications."
---

# Performance Optimization Guidelines for Rust CLI Tools

This skill provides comprehensive performance optimization strategies for Rust-based CLI tools like Jarvy that provision development environments across macOS, Linux, and Windows platforms.

## 1. Efficient Command Execution and Output Capture

### Minimize Process Spawning Overhead

```rust
// PREFER: Reuse Command builder pattern for multiple invocations
fn run_multiple_commands(cmds: &[(&str, &[&str])]) -> Vec<Result<Output, Error>> {
    cmds.iter()
        .map(|(cmd, args)| Command::new(cmd).args(*args).output())
        .collect()
}

// AVOID: Creating new Command structs repeatedly in hot loops
for _ in 0..100 {
    Command::new("git").arg("--version").output(); // Overhead per iteration
}
```

### Efficient Output Handling

```rust
// PREFER: Use output() only when you need stdout/stderr
// Use status() when you only need exit code
fn has_command(cmd: &str) -> bool {
    Command::new(cmd)
        .arg("--version")
        .stdout(Stdio::null())  // Discard output
        .stderr(Stdio::null())
        .status()               // Cheaper than output()
        .map(|s| s.success())
        .unwrap_or(false)
}

// AVOID: Capturing output when you only check exit status
fn has_command_slow(cmd: &str) -> bool {
    Command::new(cmd)
        .arg("--version")
        .output()  // Allocates String buffers unnecessarily
        .map(|o| o.status.success())
        .unwrap_or(false)
}
```

### Use Inherited I/O for Interactive Commands

```rust
// For commands requiring user interaction, inherit stdio
Command::new("sudo")
    .args(&["apt", "install", "-y", pkg])
    .stdin(Stdio::inherit())
    .stdout(Stdio::inherit())
    .stderr(Stdio::inherit())
    .status()
```

## 2. Parallel Tool Installation

### Thread-Based Parallelism for Independent Operations

```rust
use std::thread;

fn install_tools_parallel(tools: &[(&str, &str)]) -> Vec<Result<(), Error>> {
    let handles: Vec<_> = tools
        .iter()
        .map(|(name, version)| {
            let n = name.to_string();
            let v = version.to_string();
            thread::spawn(move || install_tool(&n, &v))
        })
        .collect();

    handles.into_iter()
        .map(|h| h.join().unwrap_or_else(|_| Err(Error::ThreadPanic)))
        .collect()
}
```

### Rayon for Data Parallelism (When Appropriate)

```rust
// Add rayon only if you have many parallel tasks
// For CLI tools with 5-20 tools, std::thread is often sufficient
use rayon::prelude::*;

fn check_tools_parallel(tools: &[String]) -> Vec<bool> {
    tools.par_iter()
        .map(|t| has_command(t))
        .collect()
}
```

### Batch Package Manager Operations

```rust
// PREFER: Single package manager call with multiple packages
fn install_via_brew(packages: &[&str]) -> Result<(), Error> {
    let mut args = vec!["install"];
    args.extend(packages);
    run("brew", &args)
}

// AVOID: Multiple package manager invocations
fn install_via_brew_slow(packages: &[&str]) -> Result<(), Error> {
    for pkg in packages {
        run("brew", &["install", pkg])?;
    }
    Ok(())
}
```

## 3. Lazy Initialization Patterns

### OnceLock for Global Registries

```rust
use std::sync::{OnceLock, RwLock};
use std::collections::HashMap;

// Global registry initialized exactly once on first access
static REGISTRY: OnceLock<RwLock<HashMap<String, Handler>>> = OnceLock::new();

fn registry() -> &'static RwLock<HashMap<String, Handler>> {
    REGISTRY.get_or_init(|| RwLock::new(HashMap::new()))
}

// Benefits:
// - Zero cost if never accessed
// - Thread-safe initialization
// - No runtime mutex for read-heavy workloads
```

### Lazy Detection of System State

```rust
use std::sync::OnceLock;

// Cache expensive system queries
static LINUX_PM: OnceLock<Option<PackageManager>> = OnceLock::new();

fn detect_linux_pm() -> Option<PackageManager> {
    *LINUX_PM.get_or_init(|| {
        // Expensive: spawns multiple processes to detect package manager
        if has("apt-get") { return Some(PackageManager::Apt); }
        if has("dnf") { return Some(PackageManager::Dnf); }
        // ... more checks
        None
    })
}
```

### Avoid LazyLock for Simple Cases

```rust
// PREFER: OnceLock when you need the init closure to capture data
// PREFER: const/static for compile-time known values

// AVOID: LazyLock for simple constant-like values
static SUPPORTED_TOOLS: LazyLock<Vec<&str>> = LazyLock::new(|| {
    vec!["git", "docker", "node"]  // Could be const array
});

// PREFER: Compile-time array
const SUPPORTED_TOOLS: &[&str] = &["git", "docker", "node"];
```

## 4. Minimizing Allocations in Hot Paths

### String Handling

```rust
// PREFER: &str for function parameters when ownership not needed
fn register_tool(name: &str, handler: Handler) -> bool {
    let key = name.to_ascii_lowercase(); // Single allocation
    // ...
}

// AVOID: String parameters that force caller allocation
fn register_tool_slow(name: String, handler: Handler) -> bool {
    let key = name.to_ascii_lowercase();
    // ...
}
```

### Pre-allocate Collections

```rust
// PREFER: Pre-allocate when size is known
fn collect_reports(tools: &[Tool]) -> Vec<Report> {
    let mut reports = Vec::with_capacity(tools.len());
    for tool in tools {
        reports.push(generate_report(tool));
    }
    reports
}

// Also good: Iterator collect (Rust optimizes well)
fn collect_reports(tools: &[Tool]) -> Vec<Report> {
    tools.iter().map(generate_report).collect()
}
```

### Avoid Intermediate Collections

```rust
// PREFER: Iterator chains
fn find_matching_tools<'a>(tools: &'a [Tool], pattern: &str) -> impl Iterator<Item = &'a Tool> {
    tools.iter().filter(move |t| t.name.contains(pattern))
}

// AVOID: Collecting into Vec just to iterate again
fn find_matching_tools_slow(tools: &[Tool], pattern: &str) -> Vec<&Tool> {
    tools.iter()
        .filter(|t| t.name.contains(pattern))
        .collect()  // Unnecessary allocation
}
```

### Use Cow for Conditional Ownership

```rust
use std::borrow::Cow;

fn normalize_tool_name(name: &str) -> Cow<'_, str> {
    if name.chars().all(|c| c.is_ascii_lowercase()) {
        Cow::Borrowed(name)  // No allocation
    } else {
        Cow::Owned(name.to_ascii_lowercase())  // Allocate only when needed
    }
}
```

## 5. Efficient Config Parsing

### Serde Optimization

```toml
# Cargo.toml - Enable serde optimizations
[dependencies]
serde = { version = "1.0", features = ["derive"] }
toml = "0.9"
```

```rust
// PREFER: Deserialize directly into final structure
#[derive(Deserialize)]
pub struct Config {
    #[serde(rename = "provisioner")]
    tools: HashMap<String, ToolConfig>,
}

// Use #[serde(default)] to avoid Option<T> unwrapping everywhere
#[derive(Deserialize, Default)]
pub struct Settings {
    #[serde(default)]
    pub telemetry: bool,
    #[serde(default)]
    pub use_sudo: Option<bool>,
}
```

### Avoid Re-parsing

```rust
// PREFER: Parse once, pass reference
fn main() {
    let config = Config::new(&config_path);
    setup(&config);
    collect_reports(&config);
}

// AVOID: Re-reading/parsing config in each function
fn setup() {
    let config = Config::new("jarvy.toml");  // Re-parse
    // ...
}
```

### Use Borrowed Data Where Possible

```rust
// For configs that don't need ownership, use references
#[derive(Deserialize)]
pub struct ToolConfig<'a> {
    #[serde(borrow)]
    version: &'a str,  // Zero-copy from config string
}
```

## 6. Build Optimizations

### Cargo.toml Settings

```toml
[build]
jobs = 16                    # Parallel compilation jobs
rustc-wrapper = "sccache"    # Compile cache for faster rebuilds
pipelining = true            # Parallel crate compilation

[profile.dev]
opt-level = 1                # Slight optimization even in debug

[profile.release]
lto = "thin"                 # Link-time optimization (faster builds than "fat")
codegen-units = 1            # Better optimization, slower compile
panic = "abort"              # Smaller binary, no unwinding overhead
strip = true                 # Remove debug symbols from binary
```

### Feature Flags for Optional Dependencies

```rust
// Only compile telemetry when needed
#[cfg(feature = "telemetry")]
mod analytics;

// Cargo.toml
[features]
default = []
telemetry = ["opentelemetry-otlp", "opentelemetry_sdk"]
```

### Conditional Compilation for Platform-Specific Code

```rust
// Compile only relevant platform code
#[cfg(target_os = "macos")]
fn install_macos() -> Result<(), Error> { /* ... */ }

#[cfg(target_os = "linux")]
fn install_linux() -> Result<(), Error> { /* ... */ }

#[cfg(target_os = "windows")]
fn install_windows() -> Result<(), Error> { /* ... */ }
```

## 7. Profiling and Measurement

### Built-in Timing

```rust
use std::time::Instant;

fn timed_operation<T, F: FnOnce() -> T>(name: &str, f: F) -> T {
    let start = Instant::now();
    let result = f();
    eprintln!("{}: {:?}", name, start.elapsed());
    result
}
```

### Memory Profiling with Dhat (Development)

```toml
# Cargo.toml
[dev-dependencies]
dhat = "0.3"

[features]
dhat-heap = []  # Enable heap profiling
```

```rust
#[cfg(feature = "dhat-heap")]
#[global_allocator]
static ALLOC: dhat::Alloc = dhat::Alloc;

fn main() {
    #[cfg(feature = "dhat-heap")]
    let _profiler = dhat::Profiler::new_heap();

    // ... rest of main
}
```

### Benchmarking with Criterion

```toml
[dev-dependencies]
criterion = "0.5"

[[bench]]
name = "config_parsing"
harness = false
```

```rust
// benches/config_parsing.rs
use criterion::{criterion_group, criterion_main, Criterion};

fn bench_config_parse(c: &mut Criterion) {
    let config_str = include_str!("../tests/configs/jarvy.toml");
    c.bench_function("parse_config", |b| {
        b.iter(|| toml::from_str::<Config>(config_str))
    });
}

criterion_group!(benches, bench_config_parse);
criterion_main!(benches);
```

## 8. CLI-Specific Optimizations

### Fast Startup

```rust
// Parse CLI args before any initialization
fn main() {
    let cli = Cli::parse();  // Fast, pure parsing

    // Early exit for help/version
    if matches!(&cli.command, Some(Commands::External(_))) {
        handle_unknown_command(&cli);
        return;
    }

    // Only initialize expensive resources after parsing
    let config = initialize();  // Lazy: only when needed
}
```

### Defer Expensive Operations

```rust
// PREFER: Initialize telemetry only when command needs it
fn main() {
    let cli = Cli::parse();

    match &cli.command {
        Some(Commands::Setup { .. }) => {
            init_telemetry();  // Only setup needs telemetry
            run_setup();
        }
        Some(Commands::Get { .. }) => {
            // No telemetry needed for read-only command
            run_get();
        }
        _ => {}
    }
}
```

### Exit Codes Without Panic

```rust
// PREFER: Return exit codes, don't panic
fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => {
            eprintln!("Error: {}", e);
            ExitCode::from(e.exit_code())
        }
    }
}

// AVOID: Using process::exit() or panic!() for flow control
fn main() {
    if let Err(e) = run() {
        process::exit(1);  // Skips destructors
    }
}
```

## 9. Cross-Platform Performance Considerations

### Platform-Specific Optimizations

```rust
// Windows: Prefer winget for faster installs
#[cfg(target_os = "windows")]
fn install_tool(name: &str) -> Result<(), Error> {
    // winget is generally faster than chocolatey
    run("winget", &["install", "-e", "--id", &tool_id(name)])
}

// macOS: Use brew bundle for multiple tools
#[cfg(target_os = "macos")]
fn install_tools_batch(tools: &[&str]) -> Result<(), Error> {
    // Single brew invocation is faster than multiple
    let mut args = vec!["install"];
    args.extend(tools);
    run("brew", &args)
}
```

### Avoid Platform Detection in Hot Paths

```rust
// PREFER: Compile-time platform selection
#[cfg(target_os = "linux")]
const DEFAULT_SHELL: &str = "/bin/bash";

#[cfg(target_os = "macos")]
const DEFAULT_SHELL: &str = "/bin/zsh";

#[cfg(target_os = "windows")]
const DEFAULT_SHELL: &str = "powershell.exe";

// AVOID: Runtime detection in hot paths
fn get_shell() -> &'static str {
    if cfg!(target_os = "linux") { "/bin/bash" }
    else if cfg!(target_os = "macos") { "/bin/zsh" }
    else { "powershell.exe" }
}
```

## 10. Error Handling Performance

### Use thiserror for Zero-Cost Errors

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum InstallError {
    #[error("unsupported platform")]
    Unsupported,
    #[error("prerequisite missing: {0}")]
    Prereq(&'static str),  // Static str avoids allocation
    #[error("command failed: {cmd}")]
    CommandFailed {
        cmd: String,
        #[source]
        source: std::io::Error,
    },
}
```

### Avoid String Allocation in Error Paths

```rust
// PREFER: Static strings for common errors
#[error("prerequisite missing: {0}")]
Prereq(&'static str),

// AVOID: Formatting strings in error construction
Err(InstallError::Prereq(&format!("missing {}", tool)))  // Allocation
```

## Summary Checklist

- [ ] Use `status()` instead of `output()` when only exit code matters
- [ ] Batch package manager operations where possible
- [ ] Use `OnceLock` for expensive one-time computations
- [ ] Pre-allocate collections when size is known
- [ ] Parse CLI args before expensive initialization
- [ ] Use compile-time platform selection (`#[cfg(...)]`)
- [ ] Enable `sccache` and parallel compilation in `Cargo.toml`
- [ ] Use `&str` parameters, not `String`, when ownership not needed
- [ ] Profile with `dhat` or `criterion` before optimizing
- [ ] Consider `lto = "thin"` for release builds
