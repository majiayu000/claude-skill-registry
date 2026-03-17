---
name: rust-error-handling
description: Rust error handling with anyhow and thiserror
---

# rust-error-handling

This skill covers error handling patterns in Rust using `anyhow` for application code and `thiserror` for library/domain-specific errors. Script-kit-gpui uses both crates strategically based on context.

## When to Use Each

| Crate | Use Case | Returns |
|-------|----------|---------|
| **anyhow** | Application code, internal functions, quick prototyping | `anyhow::Result<T>` |
| **thiserror** | Public APIs, domain errors, when callers need to match on variants | Custom error enum |

**Rule of thumb**: If the error needs to cross a module boundary or callers might want to handle specific cases differently, use `thiserror`. Otherwise, use `anyhow`.

## anyhow

`anyhow` provides a flexible error type for application-level error handling. It wraps any `std::error::Error` and adds context.

### Core API

```rust
use anyhow::{anyhow, bail, Context, Result};

// Result<T> is an alias for Result<T, anyhow::Error>
fn load_config() -> Result<Config> {
    let content = std::fs::read_to_string("config.json")?;
    let config: Config = serde_json::from_str(&content)?;
    Ok(config)
}
```

### Key Macros

```rust
// anyhow! - Create an ad-hoc error
return Err(anyhow!("Failed to parse shortcut: {}", shortcut));

// bail! - Early return with error (shorthand for return Err(anyhow!(...)))
if id.is_empty() {
    bail!("Entry not found: {}", id);
}

// ensure! - Return error if condition is false
ensure!(count > 0, "Count must be positive, got {}", count);
```

### Adding Context

The `Context` trait is essential for debugging. Always add context to low-level errors:

```rust
use anyhow::{Context, Result};

// .context() - Static context message
let conn = Connection::open(&db_path)
    .context("Failed to open AI chats database")?;

// .with_context() - Dynamic context (use when you need formatting)
std::fs::create_dir_all(&dir)
    .with_context(|| format!("Failed to create directory: {}", dir.display()))?;
```

**Output when error occurs:**
```
Error: Failed to open AI chats database

Caused by:
    No such file or directory (os error 2)
```

## thiserror

`thiserror` provides derive macros for implementing `std::error::Error`. Use it when you need structured, matchable errors.

### Basic Usage

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ShortcutParseError {
    #[error("shortcut string is empty")]
    Empty,
    
    #[error("shortcut has no key, only modifiers")]
    MissingKey,
    
    #[error("unknown token '{0}' in shortcut")]
    UnknownToken(String),
    
    #[error("unknown key '{0}'")]
    UnknownKey(String),
}
```

### Attributes

```rust
#[derive(Error, Debug)]
pub enum ScriptKitError {
    // Basic message
    #[error("Configuration error: {0}")]
    Config(String),
    
    // Named fields with interpolation
    #[error("Script execution failed: {message}")]
    ScriptExecution {
        message: String,
        script_path: Option<String>,
    },
    
    // #[from] - Auto-implement From trait for ? operator
    #[error("Failed to parse protocol message: {0}")]
    ProtocolParse(#[from] serde_json::Error),
    
    // #[source] - Mark the underlying error (for error chain)
    #[error("Theme loading failed for '{path}': {source}")]
    ThemeLoad {
        path: String,
        #[source]
        source: std::io::Error,
    },
}
```

### Attribute Reference

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `#[error("...")]` | Display message with interpolation | `#[error("Not found: {0}")]` |
| `#[from]` | Auto-implement `From<T>` for `?` | `Io(#[from] io::Error)` |
| `#[source]` | Mark error source for chaining | `#[source] source: io::Error` |
| `#[error(transparent)]` | Delegate Display to inner error | For wrapper types |

## Usage in script-kit-gpui

### Pattern 1: Domain Errors with thiserror

From `src/error.rs` - Application-wide error types:

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ScriptKitError {
    #[error("Script execution failed: {message}")]
    ScriptExecution {
        message: String,
        script_path: Option<String>,
    },

    #[error("Failed to parse protocol message: {0}")]
    ProtocolParse(#[from] serde_json::Error),

    #[error("Theme loading failed for '{path}': {source}")]
    ThemeLoad {
        path: String,
        #[source]
        source: std::io::Error,
    },
}

impl ScriptKitError {
    // Add helper methods for error handling
    pub fn severity(&self) -> ErrorSeverity {
        match self {
            Self::ScriptExecution { .. } => ErrorSeverity::Error,
            Self::ProtocolParse(_) => ErrorSeverity::Warning,
            // ...
        }
    }
}
```

### Pattern 2: Module-Specific Errors

From `src/keyboard_monitor.rs`:

```rust
#[derive(Error, Debug)]
pub enum KeyboardMonitorError {
    #[error("Accessibility permissions not granted. Please enable in System Preferences > Privacy & Security > Accessibility")]
    AccessibilityNotGranted,

    #[error("Failed to create event tap - this may indicate accessibility permissions issue")]
    EventTapCreationFailed,

    #[error("Monitor is already running")]
    AlreadyRunning,
}
```

### Pattern 3: anyhow with Context for Internal Functions

From `src/ai/storage.rs`:

```rust
use anyhow::{Context, Result};

pub fn create_chat(id: &str, model: &str) -> Result<()> {
    let guard = DB.read()
        .map_err(|e| anyhow::anyhow!("DB lock error: {}", e))?;
    
    let conn = guard.as_ref()
        .ok_or_else(|| anyhow::anyhow!("AI database not initialized"))?;

    conn.execute(
        "INSERT INTO chats ...",
        params![id, model],
    ).context("Failed to create chat")?;
    
    Ok(())
}
```

### Pattern 4: Error Logging Extensions

From `src/error.rs` - Extension traits for ergonomic error handling:

```rust
pub trait ResultExt<T> {
    fn log_err(self) -> Option<T>;
    fn warn_on_err(self) -> Option<T>;
}

impl<T, E: std::fmt::Debug> ResultExt<T> for Result<T, E> {
    #[track_caller]
    fn log_err(self) -> Option<T> {
        match self {
            Ok(value) => Some(value),
            Err(error) => {
                let caller = std::panic::Location::caller();
                error!(
                    error = ?error,
                    file = caller.file(),
                    line = caller.line(),
                    "Operation failed"
                );
                None
            }
        }
    }
}

// Usage:
some_fallible_op().log_err();  // Logs error, returns Option<T>
```

## Error Context

### Static Context (prefer when message is fixed)

```rust
conn.execute(sql, params)
    .context("Failed to create chat")?;
```

### Dynamic Context (when you need variables)

```rust
std::fs::write(&path, content)
    .with_context(|| format!("Failed to write script file: {}", path.display()))?;
```

### Context Stacking

Context messages stack to create a trace:

```rust
fn load_user_settings() -> Result<Settings> {
    let path = get_settings_path()?;
    let content = std::fs::read_to_string(&path)
        .with_context(|| format!("Failed to read {}", path.display()))?;
    let settings: Settings = serde_json::from_str(&content)
        .context("Failed to parse settings JSON")?;
    Ok(settings)
}
```

Output on error:
```
Error: Failed to parse settings JSON

Caused by:
    0: expected value at line 1 column 1
```

## Converting Between Types

### From thiserror to anyhow (automatic with ?)

```rust
fn process() -> anyhow::Result<()> {
    let shortcut = Shortcut::parse(input)?;  // ShortcutParseError -> anyhow::Error
    Ok(())
}
```

### From anyhow to thiserror (use #[error(transparent)])

```rust
#[derive(Error, Debug)]
pub enum MyError {
    #[error(transparent)]
    Other(#[from] anyhow::Error),
}
```

### Manual From implementations

```rust
impl From<std::io::Error> for ScriptKitError {
    fn from(err: std::io::Error) -> Self {
        ScriptKitError::FileWatch(err.to_string())
    }
}
```

## Best Practices

### 1. Choose the Right Tool

```rust
// Internal function - use anyhow
fn load_internal_config() -> anyhow::Result<Config> { ... }

// Public API - use thiserror
pub fn parse_shortcut(s: &str) -> Result<Shortcut, ShortcutParseError> { ... }
```

### 2. Always Add Context to I/O Operations

```rust
// BAD - unhelpful error message
let content = std::fs::read_to_string(path)?;

// GOOD - tells you what failed
let content = std::fs::read_to_string(path)
    .with_context(|| format!("Failed to read config from {}", path.display()))?;
```

### 3. Use bail! for Early Returns

```rust
// Instead of:
if !is_valid {
    return Err(anyhow!("Invalid input"));
}

// Use:
if !is_valid {
    bail!("Invalid input");
}
```

### 4. Make thiserror Variants Actionable

```rust
// BAD - what should the user do?
#[error("Permission error")]
PermissionError,

// GOOD - tells user how to fix it
#[error("Accessibility permissions not granted. Please enable in System Preferences > Privacy & Security > Accessibility")]
AccessibilityNotGranted,
```

### 5. Use map_err for Lock Poisoning

```rust
let guard = MANAGER.lock()
    .map_err(|e| anyhow::anyhow!("Lock poisoned: {}", e))?;
```

### 6. Add Severity/Category Methods to Domain Errors

```rust
impl ScriptKitError {
    pub fn severity(&self) -> ErrorSeverity { ... }
    pub fn user_message(&self) -> String { ... }
    pub fn is_recoverable(&self) -> bool { ... }
}
```

## Anti-patterns

### 1. Unwrapping in Library Code

```rust
// BAD
let value = some_result.unwrap();

// GOOD
let value = some_result.context("Failed to get value")?;
```

### 2. Losing Error Context

```rust
// BAD - original error is lost
.map_err(|_| anyhow!("Something failed"))

// GOOD - preserves error chain
.context("Something failed")
```

### 3. Overly Generic Error Messages

```rust
// BAD
.context("Failed")?;

// GOOD
.context("Failed to parse user configuration file")?;
```

### 4. Using String Errors

```rust
// BAD
fn risky() -> Result<(), String> {
    Err("It broke".to_string())
}

// GOOD
fn risky() -> anyhow::Result<()> {
    bail!("Operation failed: specific reason");
}
```

### 5. Matching on anyhow::Error

```rust
// BAD - anyhow is opaque
match err {
    // Can't match variants
}

// GOOD - use thiserror when you need to match
match err {
    ShortcutParseError::Empty => ...,
    ShortcutParseError::UnknownKey(k) => ...,
}
```

### 6. Ignoring Errors Silently

```rust
// BAD
let _ = some_fallible_op();

// BETTER - log it
some_fallible_op().log_err();

// BEST - propagate if caller should handle
some_fallible_op()?;
```

## Debug Macro

For "impossible" states, use the `debug_panic!` macro from `src/error.rs`:

```rust
// Panics in debug, logs in release
debug_panic!("Invariant violated: counter was {}", counter);
```
