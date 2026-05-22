---
name: tauri-rust-patterns
description: Tauri application development patterns in Rust. Command handlers, state management, IPC, plugin architecture, window management, and platform-specific workarounds. Use when building Tauri apps, implementing commands, managing state, or handling cross-platform issues. Trigger phrases include "tauri command", "tauri state", "window management", "IPC", "WSLg", or "transparent window".
---

# Tauri Rust Patterns

## Overview

Tauri enables building desktop applications with web frontends and Rust backends. This skill covers canonical patterns for Tauri development, focusing on command handlers, state management, IPC communication, and TMNL-specific configurations like transparent windows and WSLg workarounds.

**Key capabilities:**
- Type-safe IPC between frontend and backend
- Shared state management with `State<T>`
- Custom window configurations (transparency, decorations)
- Plugin architecture for modular functionality
- Cross-platform compatibility (Linux, Windows, macOS)

## Canonical Sources

**Tauri Documentation:**
- Official docs: https://tauri.app/
- Rust API: https://docs.rs/tauri
- Command guide: https://tauri.app/v1/guides/features/command
- State management: https://tauri.app/v1/guides/features/state

**TMNL Codebase:**
- `CLAUDE.md` — Tauri configuration section (lines 457-563)
- `nix/modules/tauri.nix` — Build environment configuration
- Package.json — Tauri scripts and dependencies
- Example: Transparent frameless window setup

**Related Skills:**
- `rust-effect-patterns` — Error handling in commands
- `mcp-server-development` — Similar IPC patterns

## Tauri Architecture

### Application Flow

```
┌────────────────────────────────────────────┐
│         Frontend (Web)                      │
│  ┌──────────────────────────────────────┐  │
│  │  React/Vue/Svelte Components         │  │
│  │  • UI rendering                      │  │
│  │  • User interactions                 │  │
│  └────────────┬─────────────────────────┘  │
└───────────────┼────────────────────────────┘
                │ @tauri-apps/api
                │ invoke("command", args)
                │
┌───────────────▼────────────────────────────┐
│         Tauri Core (Rust)                   │
│  ┌──────────────────────────────────────┐  │
│  │  Command Handlers                    │  │
│  │  #[tauri::command]                   │  │
│  │  async fn greet(name: String) {...}  │  │
│  └──────────────────────────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │  State Management                    │  │
│  │  State<AppState>                     │  │
│  │  Mutex<T>, RwLock<T>                 │  │
│  └──────────────────────────────────────┘  │
│  ┌──────────────────────────────────────┐  │
│  │  Window Management                   │  │
│  │  WindowBuilder, WebviewWindow        │  │
│  └──────────────────────────────────────┘  │
└───────────────────────────────────────────┘
```

## Pattern 1: Command Handlers

### Basic Command

```rust
use tauri::command;

#[command]
fn greet(name: String) -> String {
    format!("Hello, {}!", name)
}

// In main.rs
fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Frontend (TypeScript):**
```typescript
import { invoke } from "@tauri-apps/api/core";

const greeting = await invoke<string>("greet", { name: "Alice" });
console.log(greeting); // "Hello, Alice!"
```

**Pattern:** Commands are functions annotated with `#[command]`, registered via `generate_handler!`.

### Async Command with Result

```rust
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Error, Debug, Serialize)]
pub enum CommandError {
    #[error("File not found: {0}")]
    FileNotFound(String),

    #[error("IO error: {0}")]
    IoError(String),
}

// Required for Tauri IPC
impl From<std::io::Error> for CommandError {
    fn from(err: std::io::Error) -> Self {
        CommandError::IoError(err.to_string())
    }
}

#[derive(Serialize, Deserialize)]
pub struct FileContent {
    path: String,
    content: String,
    size: usize,
}

#[command]
async fn read_file(path: String) -> Result<FileContent, CommandError> {
    // Validate path
    if !std::path::Path::new(&path).exists() {
        return Err(CommandError::FileNotFound(path));
    }

    // Read file asynchronously
    let content = tokio::fs::read_to_string(&path).await?;
    let size = content.len();

    Ok(FileContent { path, content, size })
}
```

**Frontend:**
```typescript
try {
  const file = await invoke<FileContent>("read_file", {
    path: "/path/to/file.txt",
  });
  console.log(`Read ${file.size} bytes from ${file.path}`);
} catch (error) {
  console.error("Error:", error); // CommandError message
}
```

**Pattern:** Use `Result<T, E>` with `Serialize` error types, `async fn` for I/O operations.

### Command with Multiple Arguments

```rust
#[command]
async fn search_files(
    directory: String,
    pattern: String,
    case_sensitive: bool,
) -> Result<Vec<String>, CommandError> {
    let mut results = Vec::new();
    let regex = if case_sensitive {
        regex::Regex::new(&pattern)?
    } else {
        regex::RegexBuilder::new(&pattern)
            .case_insensitive(true)
            .build()?
    };

    for entry in walkdir::WalkDir::new(&directory) {
        let entry = entry?;
        if let Some(name) = entry.file_name().to_str() {
            if regex.is_match(name) {
                results.push(entry.path().display().to_string());
            }
        }
    }

    Ok(results)
}
```

**Frontend:**
```typescript
const matches = await invoke<string[]>("search_files", {
  directory: "/home/user/projects",
  pattern: ".*\\.rs$",
  caseSensitive: true,
});
```

**Pattern:** Arguments map to function parameters by name (camelCase ↔ snake_case).

## Pattern 2: State Management

### Basic State with Mutex

```rust
use std::sync::Mutex;
use tauri::State;

struct AppState {
    counter: Mutex<i32>,
}

#[command]
fn increment(state: State<AppState>) -> i32 {
    let mut counter = state.counter.lock().unwrap();
    *counter += 1;
    *counter
}

#[command]
fn get_count(state: State<AppState>) -> i32 {
    *state.counter.lock().unwrap()
}

fn main() {
    tauri::Builder::default()
        .manage(AppState {
            counter: Mutex::new(0),
        })
        .invoke_handler(tauri::generate_handler![increment, get_count])
        .run(tauri::generate_context!())
        .expect("error");
}
```

**Frontend:**
```typescript
await invoke("increment"); // 1
await invoke("increment"); // 2
const count = await invoke<number>("get_count"); // 2
```

**Pattern:** Use `.manage(T)` to register state, `State<T>` to access in commands.

### Shared State with RwLock

```rust
use std::collections::HashMap;
use std::sync::RwLock;

struct CacheState {
    data: RwLock<HashMap<String, String>>,
}

#[command]
fn cache_get(key: String, state: State<CacheState>) -> Option<String> {
    let data = state.data.read().unwrap();
    data.get(&key).cloned()
}

#[command]
fn cache_set(key: String, value: String, state: State<CacheState>) {
    let mut data = state.data.write().unwrap();
    data.insert(key, value);
}

#[command]
fn cache_clear(state: State<CacheState>) {
    let mut data = state.data.write().unwrap();
    data.clear();
}
```

**Pattern:** `RwLock` for read-heavy workloads (multiple readers, exclusive writer).

### Complex State with Arc

```rust
use std::sync::Arc;
use tokio::sync::RwLock;

struct DatabaseConnection {
    pool: sqlx::Pool<sqlx::Sqlite>,
}

struct AppState {
    db: Arc<RwLock<DatabaseConnection>>,
}

#[command]
async fn query_users(state: State<'_, AppState>) -> Result<Vec<User>, CommandError> {
    let db = state.db.read().await;
    let users = sqlx::query_as::<_, User>("SELECT * FROM users")
        .fetch_all(&db.pool)
        .await?;
    Ok(users)
}

#[tokio::main]
async fn main() {
    let pool = sqlx::SqlitePool::connect("sqlite:db.sqlite").await.unwrap();

    tauri::Builder::default()
        .manage(AppState {
            db: Arc::new(RwLock::new(DatabaseConnection { pool })),
        })
        .invoke_handler(tauri::generate_handler![query_users])
        .run(tauri::generate_context!())
        .expect("error");
}
```

**Pattern:** Use `Arc<RwLock<T>>` for async state, `tokio::sync::RwLock` for async locks.

## Pattern 3: Window Management

### TMNL Transparent Window Configuration

**tauri.conf.json:**
```json
{
  "tauri": {
    "windows": [
      {
        "title": "TMNL",
        "width": 1280,
        "height": 800,
        "decorations": false,
        "transparent": true,
        "macOSPrivateApi": true
      }
    ]
  }
}
```

**Capabilities (default.json):**
```json
{
  "permissions": [
    "core:window:default",
    "core:window:allow-start-dragging",
    "core:window:allow-minimize",
    "core:window:allow-maximize",
    "core:window:allow-close",
    "core:window:allow-set-decorations",
    "core:window:allow-set-always-on-top"
  ]
}
```

**Pattern:** `decorations: false` + `transparent: true` = frameless transparent window.

### Custom Window Controls (Frontend)

```typescript
import { getCurrentWindow } from "@tauri-apps/api/window";

const appWindow = getCurrentWindow();

// Window operations
async function minimizeWindow() {
  await appWindow.minimize();
}

async function toggleMaximize() {
  await appWindow.toggleMaximize();
}

async function closeWindow() {
  await appWindow.close();
}

// Drag region (in React component)
function TitleBar() {
  return (
    <div data-tauri-drag-region className="titlebar">
      <span>TMNL</span>
      <div className="controls">
        <button onClick={minimizeWindow}>−</button>
        <button onClick={toggleMaximize}>□</button>
        <button onClick={closeWindow}>×</button>
      </div>
    </div>
  );
}
```

**CSS:**
```css
.titlebar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  background: rgba(0, 0, 0, 0.8);
  z-index: 9999;
}
```

**Pattern:** Use `data-tauri-drag-region` attribute for draggable areas.

### Programmatic Window Creation (Rust)

```rust
use tauri::{Manager, WindowBuilder, WindowUrl};

#[command]
fn create_settings_window(app: tauri::AppHandle) -> Result<(), String> {
    let settings_window = WindowBuilder::new(
        &app,
        "settings",
        WindowUrl::App("settings.html".into()),
    )
    .title("Settings")
    .inner_size(600.0, 400.0)
    .resizable(false)
    .decorations(true)
    .build()
    .map_err(|e| e.to_string())?;

    Ok(())
}
```

**Pattern:** Use `WindowBuilder` for runtime window creation.

## Pattern 4: WSLg Rendering Workaround (TMNL-Specific)

### Problem

WSLg renders Tauri windows with blank/tiny HTML content due to WebKitGTK compositing bugs.

### Solution (Automatic Detection)

**scripts/tauri-dev.sh:**
```bash
#!/bin/bash

# Detect WSLg environment
if [ -n "$WSL_DISTRO_NAME" ]; then
    echo "[tauri-dev] WSLg detected, applying WebKit workaround"
    export WEBKIT_DISABLE_COMPOSITING_MODE=1
fi

# Run Tauri dev
bun run tauri dev
```

**Nix mission-control script:**
```nix
tauri-dev = {
  description = "Run Tauri in development mode";
  exec = ''
    cd $FLAKE_ROOT/packages/tmnl
    if [ -n "$WSL_DISTRO_NAME" ]; then
      echo "[tauri-dev] WSLg detected, applying WebKit workaround"
      export WEBKIT_DISABLE_COMPOSITING_MODE=1
    fi
    bun run tauri:dev
  '';
};
```

**Pattern:** Check `$WSL_DISTRO_NAME`, set `WEBKIT_DISABLE_COMPOSITING_MODE=1` if WSLg.

### Platform-Specific Code (Rust)

```rust
#[cfg(target_os = "linux")]
fn apply_linux_fixes() {
    // WSLg detection
    if std::env::var("WSL_DISTRO_NAME").is_ok() {
        std::env::set_var("WEBKIT_DISABLE_COMPOSITING_MODE", "1");
    }
}

#[cfg(target_os = "windows")]
fn apply_windows_fixes() {
    // Windows-specific logic
}

#[cfg(target_os = "macos")]
fn apply_macos_fixes() {
    // macOS-specific logic
}

fn main() {
    #[cfg(target_os = "linux")]
    apply_linux_fixes();

    #[cfg(target_os = "windows")]
    apply_windows_fixes();

    #[cfg(target_os = "macos")]
    apply_macos_fixes();

    tauri::Builder::default()
        // ...
        .run(tauri::generate_context!())
        .expect("error");
}
```

**Pattern:** Use `#[cfg(target_os = "...")]` for platform-specific code.

## Pattern 5: Events (Backend → Frontend)

### Emitting Events from Rust

```rust
use tauri::{Emitter, Manager};

#[command]
async fn start_download(
    url: String,
    app: tauri::AppHandle,
) -> Result<(), CommandError> {
    // Emit progress events
    app.emit("download-progress", 0)?;

    for i in 1..=100 {
        tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
        app.emit("download-progress", i)?;
    }

    app.emit("download-complete", url)?;
    Ok(())
}
```

**Frontend (TypeScript):**
```typescript
import { listen } from "@tauri-apps/api/event";

// Listen for events
const unlisten = await listen<number>("download-progress", (event) => {
  console.log(`Progress: ${event.payload}%`);
});

await listen<string>("download-complete", (event) => {
  console.log(`Downloaded: ${event.payload}`);
  unlisten(); // Stop listening
});

// Trigger download
await invoke("start_download", { url: "https://example.com/file.zip" });
```

**Pattern:** Use `app.emit(event, payload)` in Rust, `listen(event, callback)` in frontend.

### Window-Specific Events

```rust
#[command]
fn notify_window(
    window: tauri::Window,
    message: String,
) -> Result<(), String> {
    window.emit("notification", message)
        .map_err(|e| e.to_string())
}
```

**Frontend:**
```typescript
import { getCurrentWindow } from "@tauri-apps/api/window";

const window = getCurrentWindow();
await window.listen<string>("notification", (event) => {
  alert(event.payload);
});
```

## Pattern 6: Plugin Architecture

### Custom Plugin Structure

```rust
use tauri::{plugin::Plugin, Runtime, AppHandle, Invoke};

pub struct DatabasePlugin<R: Runtime> {
    invoke_handler: Box<dyn Fn(Invoke<R>) + Send + Sync>,
}

impl<R: Runtime> DatabasePlugin<R> {
    pub fn new() -> Self {
        Self {
            invoke_handler: Box::new(|_| {}),
        }
    }
}

impl<R: Runtime> Plugin<R> for DatabasePlugin<R> {
    fn name(&self) -> &'static str {
        "database"
    }

    fn initialize(&mut self, app: &AppHandle<R>, _config: serde_json::Value) -> tauri::plugin::Result<()> {
        // Initialize plugin
        app.manage(DatabaseState::new());
        Ok(())
    }

    fn extend_api(&mut self, invoke: Invoke<R>) {
        (self.invoke_handler)(invoke);
    }
}

// In main.rs
fn main() {
    tauri::Builder::default()
        .plugin(DatabasePlugin::new())
        .run(tauri::generate_context!())
        .expect("error");
}
```

**Pattern:** Implement `Plugin<R>` trait for modular functionality.

## Pattern 7: Configuration and Build

### TMNL Nix Environment

**nix/modules/tauri.nix:**
```nix
{ inputs, lib, ... }:
{
  perSystem = { config, pkgs, system, lib, ... }: {
    devShells.tmnl-tauri = pkgs.mkShell {
      name = "tmnl-tauri";
      inputsFrom = [ config.devShells.tmnl-core ];

      nativeBuildInputs = with pkgs; [
        # GTK/WebKit dependencies (Linux)
        gtk3
        webkitgtk_4_1
        cairo
        pango
        harfbuzz
        glib
        atk
        librsvg
        libsoup_3

        # Cross-compilation (Windows)
        pkgsCross.mingwW64.stdenv.cc

        # Rust toolchain
        rustup
      ];

      shellHook = ''
        export PKG_CONFIG_PATH="${pkgs.gtk3}/lib/pkgconfig:${pkgs.webkitgtk_4_1}/lib/pkgconfig:$PKG_CONFIG_PATH"
        export LD_LIBRARY_PATH="${pkgs.gtk3}/lib:${pkgs.webkitgtk_4_1}/lib:$LD_LIBRARY_PATH"
        export RUST_SRC_PATH="${pkgs.rustPlatform.rustLibSrc}"
      '';
    };
  };
}
```

**Pattern:** Include GTK3, WebKitGTK, and cross-compilation toolchains in Nix shell.

### Cargo.toml Dependencies

```toml
[dependencies]
tauri = { version = "2.0", features = ["wry"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tokio = { version = "1", features = ["full"] }
thiserror = "2"
```

### Cross-Compilation (Windows on Linux)

```bash
# Install Windows target
rustup target add x86_64-pc-windows-gnu

# Build for Windows
cargo build --target x86_64-pc-windows-gnu

# Or via Tauri CLI
bun run tauri build --target x86_64-pc-windows-gnu
```

**Nix configuration:**
```nix
export CARGO_TARGET_X86_64_PC_WINDOWS_GNU_RUSTFLAGS="-C link-args=-Wl,--allow-multiple-definition"
```

## Testing Tauri Commands

### Unit Testing Commands

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_greet() {
        let result = greet("Alice".to_string());
        assert_eq!(result, "Hello, Alice!");
    }

    #[tokio::test]
    async fn test_read_file() {
        let result = read_file("test.txt".to_string()).await;
        assert!(result.is_ok());
    }

    #[test]
    fn test_error_handling() {
        let result = read_file("nonexistent.txt".to_string());
        assert!(matches!(result, Err(CommandError::FileNotFound(_))));
    }
}
```

### Integration Testing with WebDriver

```rust
// Use tauri-driver for end-to-end tests
// Requires tauri-driver binary

#[cfg(test)]
mod integration {
    use tauri_driver::Driver;

    #[test]
    fn test_window_title() {
        let driver = Driver::new().unwrap();
        let title = driver.title().unwrap();
        assert_eq!(title, "TMNL");
    }
}
```

## Anti-Patterns

### 1. Blocking I/O in Commands

**WRONG:**
```rust
#[command]
fn read_file_blocking(path: String) -> String {
    std::fs::read_to_string(path).unwrap()  // Blocks async runtime!
}
```

**RIGHT:**
```rust
#[command]
async fn read_file_async(path: String) -> Result<String, CommandError> {
    tokio::fs::read_to_string(path)
        .await
        .map_err(CommandError::from)
}
```

### 2. Unwrap in Command Handlers

**WRONG:**
```rust
#[command]
fn get_config(state: State<AppState>) -> Config {
    state.config.lock().unwrap()  // Panics if poisoned!
}
```

**RIGHT:**
```rust
#[command]
fn get_config(state: State<AppState>) -> Result<Config, CommandError> {
    state.config.lock()
        .map_err(|e| CommandError::LockPoisoned(e.to_string()))
        .map(|c| c.clone())
}
```

### 3. Non-Serializable Error Types

**WRONG:**
```rust
#[command]
fn parse_json(input: String) -> Result<Value, serde_json::Error> {
    // serde_json::Error doesn't implement Serialize!
    serde_json::from_str(&input)
}
```

**RIGHT:**
```rust
#[derive(Serialize)]
struct ParseError(String);

impl From<serde_json::Error> for ParseError {
    fn from(err: serde_json::Error) -> Self {
        ParseError(err.to_string())
    }
}

#[command]
fn parse_json(input: String) -> Result<Value, ParseError> {
    serde_json::from_str(&input).map_err(ParseError::from)
}
```

### 4. Ignoring Platform Differences

**WRONG:**
```rust
#[command]
fn open_terminal() {
    std::process::Command::new("gnome-terminal").spawn().unwrap();
    // Fails on Windows/macOS!
}
```

**RIGHT:**
```rust
#[command]
fn open_terminal() -> Result<(), String> {
    #[cfg(target_os = "linux")]
    std::process::Command::new("gnome-terminal")
        .spawn()
        .map_err(|e| e.to_string())?;

    #[cfg(target_os = "windows")]
    std::process::Command::new("cmd")
        .args(["/c", "start", "cmd"])
        .spawn()
        .map_err(|e| e.to_string())?;

    #[cfg(target_os = "macos")]
    std::process::Command::new("open")
        .args(["-a", "Terminal"])
        .spawn()
        .map_err(|e| e.to_string())?;

    Ok(())
}
```

## Quick Reference

### Command Syntax

```rust
// Sync command
#[command]
fn sync_fn(arg: String) -> String { ... }

// Async command
#[command]
async fn async_fn(arg: String) -> Result<String, Error> { ... }

// With state
#[command]
fn with_state(state: State<AppState>) -> i32 { ... }

// With window
#[command]
fn with_window(window: tauri::Window) { ... }

// With app handle
#[command]
fn with_app(app: tauri::AppHandle) { ... }
```

### Frontend Invocation

```typescript
import { invoke } from "@tauri-apps/api/core";

// Basic
const result = await invoke<string>("command_name", { arg: "value" });

// With error handling
try {
  const result = await invoke<string>("command_name", { arg: "value" });
} catch (error) {
  console.error("Command failed:", error);
}
```

### State Management

```rust
// Register state
.manage(AppState { ... })

// Access in command
fn cmd(state: State<AppState>) { ... }

// Mutex for sync
Mutex<T>

// RwLock for read-heavy
RwLock<T>

// Arc<RwLock<T>> for async
Arc<tokio::sync::RwLock<T>>
```

## TMNL Integration Checklist

- [ ] Commands use `async fn` for I/O operations
- [ ] Error types implement `Serialize` (use `thiserror`)
- [ ] State uses `Mutex`/`RwLock` appropriately
- [ ] WSLg workaround applied (check `$WSL_DISTRO_NAME`)
- [ ] Transparent window configured in `tauri.conf.json`
- [ ] Custom drag region implemented with `data-tauri-drag-region`
- [ ] Window controls use `@tauri-apps/api/window`
- [ ] Platform-specific code uses `#[cfg(target_os = "...")]`
- [ ] Nix shell includes GTK/WebKit dependencies
- [ ] Cross-compilation target configured if needed

## Further Reading

- **Tauri Docs**: https://tauri.app/
- **Rust API**: https://docs.rs/tauri
- **TMNL Tauri Config**: `CLAUDE.md` lines 457-563
- **Nix Tauri Module**: `nix/modules/tauri.nix`
- **Error Handling**: See `rust-effect-patterns` skill
