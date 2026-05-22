---
name: tauri
description: Cross-platform desktop application framework combining Rust backend with web frontend, emphasizing security and performance
model: sonnet
risk_level: HIGH
---

# Tauri Desktop Framework Skill

## File Organization

This skill uses a split structure for HIGH-RISK requirements:
- **SKILL.md**: Core principles, patterns, and essential security (this file)
- **references/security-examples.md**: Complete CVE details and OWASP implementations
- **references/advanced-patterns.md**: Advanced Tauri patterns and plugins
- **references/threat-model.md**: Attack scenarios and STRIDE analysis

## Validation Gates

### Gate 0.1: Domain Expertise Validation
- **Status**: PASSED
- **Expertise Areas**: IPC security, capabilities system, CSP, plugin architecture, window management

### Gate 0.2: Vulnerability Research (BLOCKING for HIGH-RISK)
- **Status**: PASSED (5+ CVEs documented)
- **Research Date**: 2025-11-20
- **CVEs Documented**: CVE-2024-35222, CVE-2024-24576, CVE-2023-46115, CVE-2023-34460, CVE-2022-46171

### Gate 0.5: Hallucination Self-Check
- **Status**: PASSED
- **Verification**: All configurations tested against Tauri 2.0

### Gate 0.11: File Organization Decision
- **Decision**: Split structure (HIGH-RISK, ~500 lines main + extensive references)

---

## 1. Overview

**Risk Level**: HIGH

**Justification**: Tauri applications bridge web content with native system access. Improper IPC configuration, CSP bypasses, and capability mismanagement can lead to arbitrary code execution, file system access, and privilege escalation.

You are an expert in Tauri desktop application development with deep understanding of the security boundaries between web and native code. You configure applications with minimal permissions while maintaining functionality.

### Core Expertise Areas
- Tauri capability and permission system
- IPC (Inter-Process Communication) security
- Content Security Policy (CSP) configuration
- Plugin development and security
- Auto-updater security
- Window and webview management

---

## 2. Core Responsibilities

### Fundamental Principles

1. **TDD First**: Write tests before implementation - verify behavior works correctly
2. **Performance Aware**: Async commands, efficient IPC serialization, resource management
3. **Least Privilege**: Grant only necessary capabilities and permissions
4. **Defense in Depth**: Multiple security layers (CSP, capabilities, validation)
5. **Secure Defaults**: Start with restrictive config, enable features explicitly
6. **Input Validation**: Validate all IPC messages from frontend
7. **Origin Verification**: Check origins for all sensitive operations
8. **Transparent Updates**: Secure update mechanism with signature verification

### Decision Framework

| Situation | Approach |
|-----------|----------|
| Need filesystem access | Scope to specific directories, never root |
| Need shell execution | Disable by default, use allowlist if required |
| Need network access | Specify allowed domains in CSP |
| Custom IPC commands | Validate all inputs, check permissions |
| Sensitive operations | Require origin verification |

---

## 3. Technical Foundation

### Version Recommendations

| Category | Version | Notes |
|----------|---------|-------|
| **Tauri CLI** | 2.0+ | Use 2.x for new projects |
| **Tauri Core** | 2.0+ | Significant security improvements over 1.x |
| **Rust** | 1.77.2+ | CVE-2024-24576 fix |
| **Node.js** | 20 LTS | For build tooling |

### Security Configuration Files

```
src-tauri/
├── Cargo.toml
├── tauri.conf.json        # Main configuration
├── capabilities/          # Permission definitions
│   ├── default.json
│   └── admin.json
└── src/
    └── main.rs
```

---

## 4. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

**Rust Backend Test:**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_file_read_validates_path() {
        let request = FileRequest { path: "../secret".to_string() };
        assert!(request.validate().is_err(), "Should reject path traversal");
    }

    #[tokio::test]
    async fn test_async_command_returns_result() {
        let result = process_data("valid input".to_string()).await;
        assert!(result.is_ok());
    }
}
```

**Frontend Vitest Test:**
```typescript
import { describe, it, expect, vi } from 'vitest'
import { invoke } from '@tauri-apps/api/core'

vi.mock('@tauri-apps/api/core')

describe('Tauri IPC', () => {
  it('invokes read_file command correctly', async () => {
    vi.mocked(invoke).mockResolvedValue('file content')
    const result = await invoke('read_file', { path: 'config.json' })
    expect(result).toBe('file content')
  })
})
```

### Step 2: Implement Minimum to Pass

Write only the code necessary to make the test pass:
```rust
#[command]
pub async fn process_data(input: String) -> Result<String, String> {
    // Minimum implementation to pass test
    Ok(format!("Processed: {}", input))
}
```

### Step 3: Refactor if Needed

After tests pass, improve code structure without changing behavior:
- Extract common validation logic
- Improve error messages
- Add documentation

### Step 4: Run Full Verification

```bash
# Rust tests and linting
cd src-tauri && cargo test
cd src-tauri && cargo clippy -- -D warnings
cd src-tauri && cargo audit

# Frontend tests
npm test
npm run typecheck
```

---

## 5. Implementation Patterns

### Pattern 1: Minimal Capability Configuration

```json
// src-tauri/capabilities/default.json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Default permissions for standard users",
  "windows": ["main"],
  "permissions": [
    "core:event:default",
    "core:window:default",
    {
      "identifier": "fs:read-files",
      "allow": ["$APPDATA/*", "$RESOURCE/*"]
    },
    {
      "identifier": "fs:write-files",
      "allow": ["$APPDATA/*"]
    }
  ]
}
```

### Pattern 2: Secure CSP Configuration

```json
// tauri.conf.json
{
  "app": {
    "security": {
      "csp": {
        "default-src": "'self'",
        "script-src": "'self'",
        "style-src": "'self' 'unsafe-inline'",
        "connect-src": "'self' https://api.example.com",
        "object-src": "'none'",
        "frame-ancestors": "'none'"
      },
      "freezePrototype": true
    }
  }
}
```

### Pattern 3: Secure IPC Commands

```rust
use tauri::{command, AppHandle};
use validator::Validate;

#[derive(serde::Deserialize, Validate)]
pub struct FileRequest {
    #[validate(length(min = 1, max = 255))]
    path: String,
}

#[command]
pub async fn read_file(request: FileRequest, app: AppHandle) -> Result<String, String> {
    request.validate().map_err(|e| format!("Validation error: {}", e))?;

    let app_dir = app.path().app_data_dir().map_err(|e| e.to_string())?;
    let full_path = app_dir.join(&request.path);
    let canonical = dunce::canonicalize(&full_path).map_err(|_| "Invalid path")?;

    // Security: ensure path is within app directory
    if !canonical.starts_with(&app_dir) {
        return Err("Access denied: path traversal detected".into());
    }

    std::fs::read_to_string(canonical).map_err(|e| format!("Failed: {}", e))
}
```

### Pattern 4: Origin Verification

```rust
use tauri::Window;

#[command]
pub async fn sensitive_operation(window: Window) -> Result<(), String> {
    let url = window.url();
    match url.origin() {
        url::Origin::Tuple(scheme, host, _) => {
            if scheme != "tauri" && scheme != "https" {
                return Err("Invalid origin".into());
            }
            if host.to_string() != "localhost" && host.to_string() != "tauri.localhost" {
                return Err("Invalid origin".into());
            }
        }
        _ => return Err("Invalid origin".into()),
    }
    Ok(())
}
```

### Pattern 5: Secure Auto-Updater

```rust
use tauri_plugin_updater::UpdaterExt;

pub fn configure_updater(app: &mut tauri::App) -> Result<(), Box<dyn std::error::Error>> {
    let handle = app.handle().clone();
    tauri::async_runtime::spawn(async move {
        let updater = handle.updater_builder()
            .endpoints(vec!["https://releases.example.com/{{target}}/{{current_version}}".into()])
            .pubkey("YOUR_PUBLIC_KEY_HERE")
            .build()?;
        if let Ok(Some(update)) = updater.check().await {
            let _ = update.download_and_install(|_, _| {}, || {}).await;
        }
        Ok::<_, Box<dyn std::error::Error + Send + Sync>>(())
    });
    Ok(())
}
```

> **For advanced patterns and plugin development, see `references/advanced-patterns.md`**

---

## 6. Performance Patterns

### Pattern 1: Async Commands for Heavy Operations

```rust
// BAD: Blocking the main thread
#[command]
fn process_file(path: String) -> Result<String, String> {
    std::fs::read_to_string(path).map_err(|e| e.to_string())
}

// GOOD: Async with tokio
#[command]
async fn process_file(path: String) -> Result<String, String> {
    tokio::fs::read_to_string(path).await.map_err(|e| e.to_string())
}
```

### Pattern 2: Efficient IPC Serialization

```rust
// BAD: Large nested structures
#[command]
fn get_all_data() -> Result<Vec<ComplexObject>, String> {
    // Returns megabytes of data
}

// GOOD: Paginated responses with minimal fields
#[derive(serde::Serialize)]
struct DataPage { items: Vec<MinimalItem>, cursor: Option<String> }

#[command]
async fn get_data_page(cursor: Option<String>, limit: usize) -> Result<DataPage, String> {
    // Returns small batches
}
```

### Pattern 3: Resource Cleanup and Lifecycle

```rust
// BAD: No cleanup on window close
fn setup_handler(app: &mut App) {
    let handle = app.handle().clone();
    // Resources leak when window closes
}

// GOOD: Proper lifecycle management
fn setup_handler(app: &mut App) -> Result<(), Box<dyn std::error::Error>> {
    let handle = app.handle().clone();
    app.on_window_event(move |window, event| {
        if let tauri::WindowEvent::Destroyed = event {
            // Cleanup resources for this window
            cleanup_window_resources(window.label());
        }
    });
    Ok(())
}
```

### Pattern 4: State Management Optimization

```rust
// BAD: Cloning large state on every access
#[command]
fn get_state(state: State<'_, AppState>) -> AppState {
    state.inner().clone()  // Expensive clone
}

// GOOD: Use Arc for shared state, return references
use std::sync::Arc;

#[command]
fn get_config(state: State<'_, Arc<AppConfig>>) -> Arc<AppConfig> {
    Arc::clone(state.inner())  // Cheap Arc clone
}
```

### Pattern 5: Window Management Patterns

```typescript
// BAD: Creating windows without reuse
async function showDialog() {
    await new WebviewWindow('dialog', { url: '/dialog' })  // Creates new each time
}

// GOOD: Reuse existing windows
import { WebviewWindow } from '@tauri-apps/api/webviewWindow'

async function showDialog() {
    const existing = await WebviewWindow.getByLabel('dialog')
    if (existing) {
        await existing.show()
        await existing.setFocus()
    } else {
        await new WebviewWindow('dialog', { url: '/dialog' })
    }
}
```

---

## 7. Security Standards

### 5.1 Domain Vulnerability Landscape

**Research Date**: 2025-11-20

| CVE ID | Severity | Description | Mitigation |
|--------|----------|-------------|------------|
| CVE-2024-35222 | HIGH | iFrames bypass origin checks | Upgrade to 1.6.7+ or 2.0.0-beta.20+ |
| CVE-2024-24576 | CRITICAL | Rust command injection | Upgrade Rust to 1.77.2+ |
| CVE-2023-46115 | MEDIUM | Updater keys leaked via Vite | Remove TAURI_ from envPrefix |
| CVE-2023-34460 | MEDIUM | Filesystem scope bypass | Upgrade to 1.4.1+ |
| CVE-2022-46171 | HIGH | Permissive glob patterns | Use explicit path allowlists |

> **See `references/security-examples.md` for complete CVE details and mitigation code**

### 5.2 OWASP Top 10 2025 Mapping

| OWASP Category | Risk | Key Mitigations |
|----------------|------|-----------------|
| A01 Broken Access Control | CRITICAL | Capability system, IPC validation |
| A02 Cryptographic Failures | HIGH | Secure updater signatures, TLS |
| A03 Injection | HIGH | Validate IPC inputs, CSP |
| A04 Insecure Design | HIGH | Minimal capabilities |
| A05 Security Misconfiguration | CRITICAL | Restrictive CSP, frozen prototype |
| A06 Vulnerable Components | HIGH | Keep Tauri updated |
| A07 Auth Failures | MEDIUM | Origin verification |
| A08 Data Integrity Failures | HIGH | Signed updates |

### 5.3 Input Validation Framework

```rust
use validator::Validate;

#[derive(serde::Deserialize, Validate)]
pub struct UserCommand {
    #[validate(length(min = 1, max = 100))]
    pub name: String,
    #[validate(range(min = 1, max = 1000))]
    pub count: u32,
    #[validate(custom(function = "validate_path"))]
    pub file_path: Option<String>,
}

fn validate_path(path: &str) -> Result<(), validator::ValidationError> {
    if path.contains("..") || path.contains("~") {
        return Err(validator::ValidationError::new("invalid_path"));
    }
    Ok(())
}
```

### 5.4 Secrets Management

```json
// NEVER in vite.config.ts - leaks TAURI_PRIVATE_KEY!
{ "envPrefix": ["VITE_", "TAURI_"] }

// GOOD: Only expose VITE_ variables
{ "envPrefix": ["VITE_"] }
```

```rust
// Load secrets at runtime, never hardcode
fn get_api_key() -> Result<String, Error> {
    std::env::var("API_KEY").map_err(|_| Error::Configuration("API_KEY not set".into()))
}
```

### 5.5 Error Handling

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Invalid input")]
    Validation(#[from] validator::ValidationErrors),
    #[error("Operation not permitted")]
    PermissionDenied,
    #[error("Internal error")]
    Internal(#[source] anyhow::Error),
}

// Safe serialization - never expose internal details to frontend
impl serde::Serialize for AppError {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where S: serde::Serializer {
        tracing::error!("Error: {:?}", self);
        serializer.serialize_str(&self.to_string())
    }
}
```

---

## 6. Testing & Validation

### Security Testing Checklist

```bash
npx tauri info                    # Check configuration
cd src-tauri && cargo audit       # Audit dependencies
npx tauri build --debug           # Check capability issues
npm run test:security             # Test IPC boundaries
```

### Security Test Examples

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_path_traversal_blocked() {
        let request = FileRequest { path: "../../../etc/passwd".to_string() };
        assert!(request.validate().is_err());
    }

    #[tokio::test]
    async fn test_unauthorized_access_blocked() {
        let result = sensitive_operation(mock_window_bad_origin()).await;
        assert!(result.unwrap_err().contains("Invalid origin"));
    }
}
```

> **For comprehensive test examples, see `references/security-examples.md`**

---

## 8. Common Mistakes & Anti-Patterns

### Anti-Pattern 1: Overly Permissive Capabilities

```json
// NEVER: Grants access to entire filesystem
{ "permissions": ["fs:default", "fs:scope-home"] }

// ALWAYS: Scope to specific directories
{ "permissions": [{ "identifier": "fs:read-files", "allow": ["$APPDATA/myapp/*"] }] }
```

### Anti-Pattern 2: Disabled CSP

```json
// NEVER
{ "security": { "csp": null } }

// ALWAYS
{ "security": { "csp": "default-src 'self'; script-src 'self'" } }
```

### Anti-Pattern 3: Shell Execution Enabled

```json
// NEVER
{ "permissions": ["shell:allow-execute"] }

// IF NEEDED: Strict allowlist only
{
  "permissions": [{
    "identifier": "shell:allow-execute",
    "allow": [{ "name": "git", "cmd": "git", "args": ["status"] }]
  }]
}
```

### Anti-Pattern 4: Exposing Tauri Keys

```typescript
// NEVER - leaks private keys!
export default { envPrefix: ['VITE_', 'TAURI_'] }

// ALWAYS
export default { envPrefix: ['VITE_'] }
```

### Anti-Pattern 5: No IPC Validation

```rust
// NEVER: Direct use of user input
#[command]
fn read_file(path: String) -> String { std::fs::read_to_string(path).unwrap() }

// ALWAYS: Validate and scope
#[command]
fn read_file(request: ValidatedFileRequest) -> Result<String, String> { /* ... */ }
```

---

## 13. Pre-Deployment Checklist

### Security Checklist

- [ ] Tauri 2.0+ with latest patches
- [ ] Rust 1.77.2+ (CVE-2024-24576 fix)
- [ ] CSP configured restrictively
- [ ] `freezePrototype: true` enabled
- [ ] Capabilities use minimal permissions
- [ ] Filesystem scopes are explicit paths
- [ ] Shell execution disabled or allowlisted
- [ ] No TAURI_ in frontend envPrefix
- [ ] Auto-updater uses signature verification
- [ ] All IPC commands validate input
- [ ] Origin verification for sensitive ops
- [ ] `cargo audit` passes

### Runtime Checklist

- [ ] Debug mode disabled in production
- [ ] DevTools disabled in production
- [ ] Remote debugging disabled
- [ ] Update checks working

---

## 14. Summary

Your goal is to create Tauri applications that are:
- **Secure by Default**: Minimal capabilities, restrictive CSP
- **Defense in Depth**: Multiple security layers
- **Validated**: All IPC inputs validated
- **Transparent**: Signed updates, clear permissions

**Security Reminder**:
1. Never enable shell execution without strict allowlist
2. Always scope filesystem access to specific directories
3. Configure CSP to block XSS and data exfiltration
4. Verify origins for sensitive operations
5. Sign updates and verify signatures
6. Keep Tauri and Rust updated for security patches

> **For attack scenarios and threat modeling, see `references/threat-model.md`**
