---
name: "agentic-jumpstart-security"
description: "Security best practices and guidelines for the Jarvy CLI codebase - a cross-platform development environment provisioning tool that executes system commands with elevated privileges"
---

# Security Guidelines for Jarvy CLI

This skill provides comprehensive security guidelines for developing and maintaining the Jarvy CLI codebase. Jarvy is a cross-platform tool that provisions development environments by executing package manager commands (brew, apt, dnf, winget, etc.) with potential privilege escalation.

## Threat Model Overview

Jarvy operates in a high-risk security context:

1. **Command Execution**: Executes external binaries (package managers, shells) with user-supplied data
2. **Privilege Escalation**: Uses `sudo` on POSIX systems for package installation
3. **Configuration Parsing**: Reads TOML files from user-specified paths
4. **Network Requests**: Makes HTTP requests to PostHog and OTLP endpoints
5. **Telemetry Collection**: Gathers machine fingerprints and usage data
6. **Shell Script Execution**: Downloads and executes installer scripts (rustup, nvm)

---

## 1. Command Injection Prevention

### The Risk

Jarvy passes user-provided tool names and versions to package manager commands. A malicious `jarvy.toml` could attempt command injection.

### CORRECT Pattern: Argument Array Separation

Always use `Command::new()` with separate arguments - NEVER shell string interpolation:

```rust
// CORRECT: Arguments are passed as separate array elements
// Each argument is escaped by the OS, preventing injection
use std::process::Command;

pub fn run(cmd: &str, args: &[&str]) -> Result<Output, InstallError> {
    Command::new(cmd)
        .args(args)  // Safe: each arg is a separate element
        .output()
        .map_err(|e| /* handle error */)
}

// Usage - safe even with untrusted input
run("brew", &["install", user_provided_package_name])?;
run("apt-get", &["install", "-y", package_name])?;
run("winget", &["install", "-e", "--id", package_id])?;
```

### ANTI-PATTERN: Shell String Interpolation

```rust
// DANGEROUS: Never concatenate user input into shell commands
let cmd = format!("brew install {}", user_input);  // VULNERABLE
Command::new("sh").args(["-c", &cmd]).output()?;   // VULNERABLE

// DANGEROUS: Using shell expansion with user data
let script = format!("curl ... | sh -s -- {}", user_version);  // VULNERABLE
```

### CORRECT Pattern: Hardcoded Package IDs

For package managers that use IDs, hardcode known-safe values:

```rust
// CORRECT: Package IDs are compile-time constants
const GIT_WINGET_ID: &str = "Git.Git";
const RUSTUP_WINGET_ID: &str = "Rustlang.Rustup";

fn install_windows() -> Result<(), InstallError> {
    run("winget", &["install", "-e", "--id", GIT_WINGET_ID])?;
    Ok(())
}
```

### CORRECT Pattern: Input Validation for Tool Names

Validate tool names against an allowlist before any operations:

```rust
// CORRECT: Only process tools registered in the known registry
pub fn add(name: &str, version: &str) -> Result<(), InstallError> {
    let key = name.to_ascii_lowercase();  // Normalize
    let map = registry().read().expect("registry rwlock poisoned");

    if let Some(handler) = map.get(&key) {
        // Only known tools can be processed
        let f = *handler;
        drop(map);
        f(version)
    } else {
        Err(InstallError::Parse("unknown tool"))  // Reject unknown tools
    }
}
```

### Version String Validation

Version hints should be validated to prevent injection via version parameters:

```rust
// CORRECT: Validate version strings contain only expected characters
fn validate_version_hint(hint: &str) -> bool {
    // Allow: digits, dots, hyphens, plus signs (semver compatible)
    hint.chars().all(|c| c.is_ascii_alphanumeric() || matches!(c, '.' | '-' | '+'))
}

// CORRECT: Use version for comparison only, not command construction
pub fn cmd_satisfies(cmd: &str, min_prefix: &str) -> bool {
    if let Ok(out) = Command::new(cmd).arg("--version").output() {
        let s = String::from_utf8_lossy(&out.stdout);
        return s.contains(min_prefix);  // Read-only comparison
    }
    false
}
```

---

## 2. Privilege Escalation Security

### The Risk

Improper sudo handling can lead to privilege escalation attacks or unintended system modifications.

### CORRECT Pattern: Explicit Sudo Control

```rust
// CORRECT: Sudo is a conscious decision, not automatic
pub fn run_maybe_sudo(use_sudo: bool, cmd: &str, args: &[&str]) -> Result<Output, InstallError> {
    match current_os() {
        Os::Windows => run(cmd, args),  // No sudo on Windows
        Os::Linux | Os::Macos => {
            if use_sudo {
                // Prepend sudo as a separate command
                let mut all = Vec::with_capacity(1 + args.len());
                all.push(cmd);
                all.extend_from_slice(args);
                run("sudo", &all)  // sudo is the command, original cmd is first arg
            } else {
                run(cmd, args)
            }
        }
    }
}
```

### CORRECT Pattern: Sudo Detection and User Configuration

```rust
// CORRECT: Check if sudo is available before attempting
pub fn has(cmd: &str) -> bool {
    Command::new(cmd)
        .arg("--version")
        .output()
        .map(|o| o.status.success())
        .unwrap_or(false)
}

// CORRECT: Allow users to control sudo behavior via config
pub fn plan_sudo_attempts(use_sudo: Option<bool>, sudo_available: bool) -> Vec<bool> {
    match use_sudo {
        Some(flag) => vec![flag],  // User explicitly set preference
        None => {
            if sudo_available {
                vec![false, true]  // Try without first, then with
            } else {
                vec![false]  // No sudo available
            }
        }
    }
}
```

### ANTI-PATTERN: Unconditional Sudo

```rust
// DANGEROUS: Always using sudo without user consent
fn install_package(pkg: &str) -> Result<(), Error> {
    run("sudo", &["apt-get", "install", pkg])?;  // WRONG: No user control
    Ok(())
}

// DANGEROUS: Sudo in shell strings
let cmd = "sudo apt-get install -y package";  // WRONG: Shell injection risk
Command::new("sh").args(["-c", cmd]).output()?;
```

### Permission Error Handling

```rust
// CORRECT: Distinct error types for permission issues
#[derive(thiserror::Error, Debug)]
pub enum InstallError {
    #[error("invalid permissions: {0}")]
    InvalidPermissions(&'static str),
    // ...
}

// CORRECT: Map permission errors to specific exit codes
match e.kind() {
    std::io::ErrorKind::PermissionDenied => {
        InstallError::InvalidPermissions("operation requires elevated privileges")
    }
    // ...
}
```

---

## 3. Path Traversal Prevention

### The Risk

User-specified config file paths could access sensitive system files.

### CORRECT Pattern: Path Canonicalization

```rust
use std::path::Path;

// CORRECT: Canonicalize and validate paths
fn safe_read_config(path: &str) -> Result<String, ConfigError> {
    let path = Path::new(path);

    // Canonicalize to resolve symlinks and ../ sequences
    let canonical = path.canonicalize()
        .map_err(|_| ConfigError::InvalidPath)?;

    // Ensure file has expected extension
    if canonical.extension() != Some(std::ffi::OsStr::new("toml")) {
        return Err(ConfigError::InvalidExtension);
    }

    std::fs::read_to_string(canonical)
        .map_err(ConfigError::IoError)
}
```

### CORRECT Pattern: Restricted Config Locations

```rust
// CORRECT: Global config is always in a known location
pub fn initialize() -> CliConfig {
    let home_dir = dirs::home_dir().expect("Failed to get home directory");
    let jarvy_dir = home_dir.join(".jarvy");  // Fixed subdirectory
    let config_file_path = jarvy_dir.join("config.toml");  // Fixed filename

    // Only read from this specific path
    let config_content = fs::read_to_string(&config_file_path).unwrap_or_default();
    // ...
}
```

### ANTI-PATTERN: Unrestricted Path Access

```rust
// DANGEROUS: Directly using user path without validation
fn read_config(path: &str) -> String {
    fs::read_to_string(path).unwrap()  // WRONG: No validation
}

// DANGEROUS: String concatenation for paths
let path = format!("{}/{}", user_dir, user_filename);  // WRONG: Path injection
```

---

## 4. Telemetry Data Security

### The Risk

Telemetry could leak PII, credentials, or sensitive system information.

### CORRECT Pattern: Anonymized Identifiers

```rust
// CORRECT: Use hardware-based anonymous fingerprint
fn get_hwid_fingerprint() -> Result<String, Box<dyn std::error::Error>> {
    let mut builder = IdBuilder::new(Encryption::SHA256);

    // Components that identify the machine, not the user
    builder
        .add_component(HWIDComponent::SystemID)
        .add_component(HWIDComponent::CPUCores)
        .add_component(HWIDComponent::OSName)
        .add_component(HWIDComponent::DriveSerial);

    // Salted hash - cannot be reversed to original values
    const SALT: &str = "9f86d081884c7d659a2feaa0c55ad015...";
    builder.build(SALT)
}
```

### CORRECT Pattern: Explicit Opt-Out

```rust
// CORRECT: Allow users to disable telemetry
pub fn init(enable_analytics: bool, distinct_id: String) {
    // Environment variable override
    let env_disable = std::env::var("JARVY_ANALYTICS").ok();
    let enabled = match env_disable.as_deref() {
        Some("0") | Some("false") => false,  // Honor user preference
        _ => enable_analytics,
    };

    // Clear documentation about telemetry
    println!(r"
        Jarvy collects telemetry data to help us improve your experience.
        The data collected is anonymized...
        If you wish to opt-out, add to ~/.jarvy/config.toml:
        [settings]
        telemetry = false
    ");
}
```

### Data Minimization

```rust
// CORRECT: Only collect necessary, non-sensitive data
pub fn capture(event: &str, mut properties: serde_json::Map<String, serde_json::Value>) {
    // Safe to collect: OS type, shell type, CLI version
    properties.entry("os".to_string())
        .or_insert(serde_json::Value::String(detect_os()));
    properties.entry("shell".to_string())
        .or_insert(serde_json::Value::String(detect_shell()));
    properties.entry("version".to_string())
        .or_insert(serde_json::Value::String(env!("CARGO_PKG_VERSION").to_string()));

    // DO NOT collect: usernames, paths containing usernames, environment variables
    // containing secrets, command arguments that might contain credentials
}
```

### ANTI-PATTERN: PII in Telemetry

```rust
// DANGEROUS: Collecting potentially sensitive data
properties.insert("username", std::env::var("USER").unwrap());  // WRONG: PII
properties.insert("home_dir", dirs::home_dir().display());  // WRONG: Contains username
properties.insert("full_command", std::env::args().collect());  // WRONG: May contain secrets
properties.insert("env_vars", std::env::vars().collect());  // WRONG: Contains secrets
```

---

## 5. HTTP Request Security

### The Risk

Network requests could be intercepted (MITM) or directed to malicious endpoints.

### CORRECT Pattern: HTTPS Only with Certificate Validation

```rust
// CORRECT: Use HTTPS endpoints with proper certificate validation
// ureq performs certificate validation by default
let response = ureq::post(&format!("{}/capture/", c.host))  // host should be https://
    .header("Content-Type", "application/json")
    .send_json(payload)?;

// CORRECT: Hardcode HTTPS URLs for installers
const RUSTUP_URL: &str = "https://sh.rustup.rs";
run("bash", &["-lc",
    "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
])?;
```

### CORRECT Pattern: TLS Version Enforcement

```rust
// CORRECT: Enforce modern TLS in curl commands
"curl --proto '=https' --tlsv1.2 -sSf https://example.com"
//     ^^^^^^^^^^^^^^^ only HTTPS
//                     ^^^^^^^^^^^ TLS 1.2 minimum
```

### ANTI-PATTERN: Insecure Network Requests

```rust
// DANGEROUS: HTTP endpoints
let host = "http://api.example.com";  // WRONG: No TLS

// DANGEROUS: Disabling certificate verification
// (ureq doesn't easily allow this, but some HTTP clients do)

// DANGEROUS: Downloading scripts without verification
run("bash", &["-c", "curl http://example.com/script.sh | bash"])?;  // WRONG: HTTP + piped execution
```

---

## 6. Safe External Command Output Parsing

### The Risk

Parsing command output incorrectly can lead to logic errors or information disclosure.

### CORRECT Pattern: Lossy UTF-8 Conversion

```rust
// CORRECT: Use lossy conversion to handle malformed output safely
if !out.status.success() {
    return Err(InstallError::CommandFailed {
        cmd: cmd.to_string(),
        code: out.status.code(),
        stderr: String::from_utf8_lossy(&out.stderr).into(),  // Safe conversion
    });
}

// CORRECT: Version checking with contains (not parsing)
pub fn cmd_satisfies(cmd: &str, min_prefix: &str) -> bool {
    if let Ok(out) = Command::new(cmd).arg("--version").output() {
        let s = String::from_utf8_lossy(&out.stdout);
        return s.contains(min_prefix);  // Simple substring check
    }
    false
}
```

### CORRECT Pattern: Defensive Parsing

```rust
// CORRECT: Handle parsing failures gracefully
let config: CliConfig = {
    let config_content = fs::read_to_string(&config_file_path).unwrap_or_default();
    if config_content.trim().is_empty() {
        CliConfig::default()  // Safe fallback
    } else {
        toml::from_str(&config_content).unwrap_or_default()  // Safe fallback on parse error
    }
};
```

### ANTI-PATTERN: Unsafe Parsing

```rust
// DANGEROUS: Assuming output is valid UTF-8
let output = String::from_utf8(out.stdout).unwrap();  // WRONG: Can panic

// DANGEROUS: Complex regex on untrusted output without limits
let re = Regex::new(r"version (\d+)\.(\d+)\.(\d+)").unwrap();
// Consider: What if output is 10MB of garbage?

// DANGEROUS: Executing parsed output
let version = parse_version(&output);
run("install", &[&format!("package@{}", version)])?;  // WRONG: Trusting parsed data
```

---

## 7. Script Download and Execution Security

### The Risk

Downloading and executing scripts from the internet is inherently dangerous.

### CORRECT Pattern: Pinned Versions and HTTPS

```rust
// CORRECT: Pin to specific versions when downloading scripts
const NVM_VERSION: &str = "v0.39.7";
const NVM_INSTALL_URL: &str =
    "https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh";

fn install_posix() -> Result<(), InstallError> {
    run("bash", &["-lc",
        &format!("curl -fsSL {} | bash", NVM_INSTALL_URL)
    ])?;
    Ok(())
}
```

### CORRECT Pattern: Verify Script Source

```rust
// CORRECT: Only use official, well-known installer URLs
// rustup: https://sh.rustup.rs (official Rust project)
// nvm: https://raw.githubusercontent.com/nvm-sh/nvm/... (official repo)
// Homebrew: https://raw.githubusercontent.com/Homebrew/install/...

// Document the trust chain in comments
/// Install Rust via rustup using the official installer.
/// Source: https://rustup.rs (maintained by Rust project)
fn install_unix() -> Result<(), InstallError> {
    run("bash", &["-lc",
        "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
    ])
}
```

### ANTI-PATTERN: Arbitrary Script Execution

```rust
// DANGEROUS: User-provided URLs
fn install_from_url(url: &str) -> Result<(), Error> {
    run("bash", &["-c", &format!("curl {} | bash", url)])?;  // WRONG
    Ok(())
}

// DANGEROUS: Unpinned versions
"curl -fsSL https://example.com/install.sh | bash"  // WRONG: Gets latest, could change
```

---

## 8. Error Handling and Information Disclosure

### The Risk

Detailed error messages can leak sensitive system information.

### CORRECT Pattern: Structured Errors Without Sensitive Data

```rust
// CORRECT: Error types that don't leak paths or system details
#[derive(thiserror::Error, Debug)]
pub enum InstallError {
    #[error("unsupported platform")]
    Unsupported,
    #[error("prerequisite missing: {0}")]
    Prereq(&'static str),  // Static string, not dynamic path
    #[error("invalid permissions: {0}")]
    InvalidPermissions(&'static str),
    #[error("command failed: {cmd} (code: {code:?})\n{stderr}")]
    CommandFailed {
        cmd: String,  // Command name only
        code: Option<i32>,
        stderr: String,  // May contain sensitive info - log carefully
    },
}
```

### CORRECT Pattern: Safe Error Logging to Telemetry

```rust
// CORRECT: Sanitize errors before sending to telemetry
pub fn capture_exception(
    message: &str,
    exception_type: &str,
    stack_trace: Option<String>,
    context: serde_json::Map<String, serde_json::Value>,
) {
    // Filter or redact sensitive information from stack traces
    let safe_stack = stack_trace.map(|s| redact_paths(&s));

    // Don't include full file paths in telemetry
    let mut safe_context = context.clone();
    safe_context.remove("full_path");
    safe_context.remove("home_directory");

    // Send sanitized data
    capture("$exception", props);
}
```

### ANTI-PATTERN: Verbose Error Messages

```rust
// DANGEROUS: Including full paths in errors
eprintln!("Failed to read: {}", full_path);  // WRONG: Exposes filesystem structure

// DANGEROUS: Including environment in errors
eprintln!("Error with env: {:?}", std::env::vars());  // WRONG: Leaks secrets

// DANGEROUS: Stack traces to users
panic!("Unexpected error: {:?}", e);  // WRONG: May contain sensitive info
```

---

## 9. Dependency Security

### Guidelines

1. **Minimize Dependencies**: Prefer stdlib over external crates when feasible
2. **Audit Dependencies**: Use `cargo audit` and `cargo deny` regularly
3. **Pin Versions**: Use exact versions in Cargo.toml for security-critical dependencies
4. **Review Features**: Only enable necessary crate features

### Current Dependencies Security Notes

```toml
# Security-relevant dependencies in Jarvy:

# ureq - HTTP client
# - Uses rustls by default (no OpenSSL dependency issues)
# - Certificate validation enabled by default
ureq = { version = "3.1.2", features = ["json"] }

# serde/toml - Config parsing
# - Well-audited, widely used
# - Deserialize untrusted input with care
serde = { version = "1.0.204", features = ["derive"] }
toml = "0.9.5"

# machineid-rs - Hardware fingerprinting
# - Review what data it collects
# - Ensure it doesn't collect PII
machineid-rs = "1.2"
```

---

## 10. Testing Security

### CORRECT Pattern: Test Mode Isolation

```rust
// CORRECT: Disable dangerous operations in tests
pub fn run(cmd: &str, args: &[&str]) -> Result<Output, InstallError> {
    // Fast tests skip external commands entirely
    if std::env::var_os("JARVY_FAST_TEST").is_some() {
        return Err(InstallError::Prereq("skipped in fast test mode"));
    }

    // Unit tests don't run external commands by default
    #[cfg(test)]
    {
        if std::env::var_os("JARVY_RUN_EXTERNAL_CMDS_IN_TEST").is_none() {
            return Err(InstallError::Prereq("external commands disabled in tests"));
        }
    }

    // Actual command execution...
}

// CORRECT: Test mode avoids interactive prompts
fn user_select() {
    if std::env::var("JARVY_TEST_MODE").as_deref() == Ok("1") {
        println!("TEST: user_select invoked");
        return;  // Skip interactive UI
    }
    // ...
}
```

---

## Security Checklist for Code Reviews

When reviewing PRs, verify:

- [ ] No user input is interpolated into shell command strings
- [ ] All `Command::new()` calls use argument arrays, not concatenated strings
- [ ] Sudo usage is controlled by user configuration
- [ ] Config file paths are validated/canonicalized
- [ ] Telemetry events don't contain PII or secrets
- [ ] HTTP requests use HTTPS with certificate validation
- [ ] Downloaded scripts are from pinned, official sources
- [ ] Error messages don't leak sensitive paths or environment data
- [ ] New dependencies are audited for security
- [ ] Tests don't execute real system commands without explicit opt-in

---

## Reporting Security Issues

If you discover a security vulnerability in Jarvy:

1. **Do not** open a public GitHub issue
2. Email security concerns to the maintainers privately
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested fix (if any)
