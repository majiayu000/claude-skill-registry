---
name: keyring
description: Cross-platform secure credential storage using system keychains
---

# keyring

Cross-platform library for securely storing and retrieving passwords/credentials using the operating system's native credential storage.

## Overview

`keyring` provides a unified API to interact with platform-specific secure credential stores:
- Each credential is identified by a `(service, user)` pair
- Credentials are stored securely in the OS keychain, encrypted at rest
- The library abstracts platform differences behind the `Entry` type

## Key Types

### Entry

The main type for interacting with credentials:

```rust
use keyring::Entry;

// Create an entry for a service/user combination
let entry = keyring::Entry::new("com.myapp.service", "username")?;
```

### Error

Non-exhaustive enum covering all failure modes:

| Variant | Description |
|---------|-------------|
| `NoEntry` | No credential exists for this entry |
| `BadEncoding(Vec<u8>)` | Password is not valid UTF-8 (raw bytes attached) |
| `TooLong(String, u32)` | Attribute exceeded platform length limit |
| `Invalid(String, String)` | Invalid attribute (name, reason) |
| `Ambiguous(Vec<Credential>)` | Multiple matching credentials found |
| `PlatformFailure(Box<dyn Error>)` | Underlying platform error |
| `NoStorageAccess(Box<dyn Error>)` | Cannot access credential store (locked?) |

### Result

Type alias: `Result<T, keyring::Error>`

## Usage in script-kit-gpui

The `env.rs` module uses keyring for secure secret storage in the EnvPrompt:

```rust
// Service identifier for all script-kit secrets
const KEYRING_SERVICE: &str = "com.scriptkit.env";

// Get a secret from keyring
pub fn get_secret(key: &str) -> Option<String> {
    let entry = keyring::Entry::new(KEYRING_SERVICE, key);
    match entry {
        Ok(entry) => match entry.get_password() {
            Ok(value) => Some(value),
            Err(keyring::Error::NoEntry) => None,  // Key doesn't exist yet
            Err(e) => {
                // Log error, return None
                None
            }
        },
        Err(e) => None,  // Entry creation failed
    }
}

// Set a secret in keyring
pub fn set_secret(key: &str, value: &str) -> Result<(), String> {
    let entry = keyring::Entry::new(KEYRING_SERVICE, key)
        .map_err(|e| format!("Failed to create keyring entry: {}", e))?;
    
    entry
        .set_password(value)
        .map_err(|e| format!("Failed to store secret: {}", e))?;
    
    Ok(())
}

// Delete a secret from keyring
pub fn delete_secret(key: &str) -> Result<(), String> {
    let entry = keyring::Entry::new(KEYRING_SERVICE, key)
        .map_err(|e| format!("Failed to create keyring entry: {}", e))?;
    
    entry
        .delete_credential()
        .map_err(|e| format!("Failed to delete secret: {}", e))?;
    
    Ok(())
}
```

### EnvPrompt Flow

1. On prompt display, `check_keyring_and_auto_submit()` checks if secret exists
2. If found, auto-submits the stored value (user sees nothing)
3. If not found, prompts user for input
4. On submit, if `secret: true`, stores value in keyring via `set_secret()`

## CRUD Operations

### Create/Update: `set_password`

```rust
let entry = Entry::new("my.service", "user")?;
entry.set_password("secret_value")?;
```

For binary data (non-UTF8):

```rust
entry.set_secret(&[0x01, 0x02, 0x03])?;
```

### Read: `get_password`

```rust
let entry = Entry::new("my.service", "user")?;
match entry.get_password() {
    Ok(password) => println!("Got: {}", password),
    Err(keyring::Error::NoEntry) => println!("Not found"),
    Err(e) => eprintln!("Error: {}", e),
}
```

For binary data:

```rust
let bytes: Vec<u8> = entry.get_secret()?;
```

### Delete: `delete_credential`

```rust
let entry = Entry::new("my.service", "user")?;
entry.delete_credential()?;  // Returns NoEntry if doesn't exist
```

## Platform Backends

| Platform | Backend | Feature Flag |
|----------|---------|--------------|
| macOS | Keychain Services | `apple-native` |
| iOS | Keychain Services | `apple-native` |
| Windows | Windows Credential Manager | `windows-native` |
| Linux | Secret Service (DBus) | `sync-secret-service` or `async-secret-service` |
| Linux | kernel keyutils | `linux-native` |
| Linux | keyutils + Secret Service | `linux-native-sync-persistent` |

### Cargo.toml Configuration

script-kit-gpui uses:

```toml
keyring = "3"
```

For explicit platform features:

```toml
[target.'cfg(target_os = "macos")'.dependencies]
keyring = { version = "3", features = ["apple-native"] }

[target.'cfg(target_os = "windows")'.dependencies]
keyring = { version = "3", features = ["windows-native"] }

[target.'cfg(target_os = "linux")'.dependencies]
keyring = { version = "3", features = ["sync-secret-service"] }
```

## Advanced Features

### Target-Based Entries

Distinguish entries with same service/user:

```rust
let entry = Entry::new_with_target("production", "my.service", "user")?;
```

### Attributes

Get/set metadata on credentials (platform-dependent):

```rust
use std::collections::HashMap;

let attrs = entry.get_attributes()?;

let mut updates = HashMap::new();
updates.insert("label", "My App Secret");
entry.update_attributes(&updates)?;
```

### Custom Credential Builders

Replace the default credential builder for custom storage backends:

```rust
use keyring::{set_default_credential_builder, Entry};

// Custom builder that uses your storage
set_default_credential_builder(my_custom_builder);

// Now Entry::new() uses your builder
let entry = Entry::new("service", "user")?;
```

## Anti-patterns

### Don't ignore `NoEntry` errors

```rust
// BAD: Crashes if key doesn't exist
let password = entry.get_password().unwrap();

// GOOD: Handle missing keys gracefully
match entry.get_password() {
    Ok(pw) => use_password(pw),
    Err(keyring::Error::NoEntry) => prompt_user(),
    Err(e) => handle_error(e),
}
```

### Don't create entries in hot paths

```rust
// BAD: Creates entry on every call
fn check_auth() -> bool {
    let entry = Entry::new("svc", "user").unwrap();
    entry.get_password().is_ok()
}

// GOOD: Create once, reuse
struct AuthChecker {
    entry: Entry,
}
```

### Don't assume UTF-8 passwords

Third-party apps may store binary data:

```rust
// BAD: Fails if password isn't UTF-8
let pw = entry.get_password()?;

// GOOD: Use get_secret for unknown sources
match entry.get_password() {
    Ok(pw) => use_password(pw),
    Err(keyring::Error::BadEncoding(bytes)) => {
        // Handle raw bytes
    }
    Err(e) => handle_error(e),
}
```

### Don't ignore platform limits

```rust
// BAD: May fail on some platforms
entry.set_password(&"x".repeat(10000))?;

// GOOD: Handle TooLong errors
match entry.set_password(&long_value) {
    Err(keyring::Error::TooLong(attr, limit)) => {
        eprintln!("{} exceeds {} byte limit", attr, limit);
    }
    // ...
}
```

### Don't access from multiple threads simultaneously

The underlying stores may not serialize concurrent access:

```rust
// BAD: Race condition on Windows/Linux
threads.iter().for_each(|_| {
    entry.get_password();  // May fail randomly
});

// GOOD: Serialize access or use per-thread entries
let mutex = Mutex::new(entry);
```

## Thread Safety

- `Entry` is `Send + Sync`
- However, underlying stores may not handle concurrent access
- Serialize access to the same credential from multiple threads
- Different credentials can be accessed concurrently

## References

- [docs.rs/keyring](https://docs.rs/keyring/latest/keyring/)
- [GitHub: hwchen/keyring-rs](https://github.com/hwchen/keyring-rs)
- [crates.io/crates/keyring](https://crates.io/crates/keyring)
