---
name: global-hotkey
description: Cross-platform global keyboard shortcuts
---

# global-hotkey

Cross-platform Rust library for registering system-wide keyboard shortcuts that work even when your application isn't focused. Part of the Tauri ecosystem.

**Crate**: [global-hotkey](https://crates.io/crates/global-hotkey) (v0.7.0)
**Docs**: https://docs.rs/global-hotkey

## Platforms Supported

- **Windows**: Requires a win32 event loop running on the thread
- **macOS**: Requires an event loop on the main thread
- **Linux**: X11 only (Wayland not supported)

## Key Types

### GlobalHotKeyManager

The central manager that handles hotkey registration with the OS.

```rust
use global_hotkey::GlobalHotKeyManager;

let manager = GlobalHotKeyManager::new().unwrap();
```

**Methods**:
- `new()` - Create a new manager (must be on correct thread per platform)
- `register(hotkey: HotKey)` - Register a single hotkey
- `unregister(hotkey: HotKey)` - Unregister a hotkey
- `register_all(&[HotKey])` - Register multiple hotkeys
- `unregister_all(&[HotKey])` - Unregister multiple hotkeys

### HotKey

Represents a keyboard shortcut (modifiers + key).

```rust
use global_hotkey::hotkey::{HotKey, Code, Modifiers};

// Programmatic construction
let hotkey = HotKey::new(Some(Modifiers::SHIFT | Modifiers::META), Code::KeyK);

// Parse from string (modifiers before key)
let hotkey: HotKey = "shift+alt+KeyQ".parse().unwrap();
```

**Fields**:
- `mods: Modifiers` - Modifier keys
- `key: Code` - The main key
- `id: u32` - Unique ID (hash of modifiers + key)

**Methods**:
- `id()` - Get the hotkey's unique ID
- `matches(modifiers, key)` - Check if modifiers/key match
- `into_string()` - Convert to string representation

### Modifiers

Bitflags for modifier keys:

```rust
use global_hotkey::hotkey::Modifiers;

let mods = Modifiers::META | Modifiers::SHIFT;
let mods = Modifiers::CONTROL | Modifiers::ALT;
let mods = Modifiers::empty(); // No modifiers
```

- `Modifiers::ALT` (Option on macOS)
- `Modifiers::CONTROL`
- `Modifiers::META` (Cmd on macOS, Win on Windows)
- `Modifiers::SHIFT`
- `Modifiers::SUPER` (alias for META)

**Constant**: `CMD_OR_CTRL` - META on macOS, CONTROL elsewhere

### Code

Physical key codes (from `keyboard-types` crate):

```rust
use global_hotkey::hotkey::Code;

// Letters
Code::KeyA, Code::KeyB, ..., Code::KeyZ

// Numbers
Code::Digit0, Code::Digit1, ..., Code::Digit9

// Function keys
Code::F1, Code::F2, ..., Code::F12

// Special keys
Code::Space, Code::Enter, Code::Tab, Code::Escape
Code::Backspace, Code::Delete
Code::ArrowUp, Code::ArrowDown, Code::ArrowLeft, Code::ArrowRight
Code::Home, Code::End, Code::PageUp, Code::PageDown

// Punctuation
Code::Semicolon, Code::Quote, Code::Comma, Code::Period
Code::Slash, Code::Backslash, Code::Minus, Code::Equal
Code::BracketLeft, Code::BracketRight, Code::Backquote
```

### GlobalHotKeyEvent

Event emitted when a hotkey is pressed or released.

```rust
use global_hotkey::{GlobalHotKeyEvent, HotKeyState};

let receiver = GlobalHotKeyEvent::receiver();

// Blocking receive
if let Ok(event) = receiver.recv() {
    if event.state == HotKeyState::Pressed {
        println!("Hotkey {} pressed", event.id);
    }
}

// Non-blocking
if let Ok(event) = receiver.try_recv() {
    // Handle event
}
```

**Fields**:
- `id: u32` - The hotkey ID that was triggered
- `state: HotKeyState` - `Pressed` or `Released`

### Error Types

```rust
use global_hotkey::Error;

match manager.register(hotkey) {
    Ok(()) => println!("Registered"),
    Err(Error::AlreadyRegistered(hk)) => {
        println!("Hotkey {} already registered", hk.id());
    }
    Err(Error::FailedToRegister(msg)) => {
        println!("System rejected: {}", msg);
    }
    Err(Error::OsError(e)) => {
        println!("OS error: {}", e);
    }
    Err(e) => println!("Other error: {}", e),
}
```

**Variants**:
- `AlreadyRegistered(HotKey)` - Another app has this hotkey
- `FailedToRegister(String)` - System rejected (reserved hotkey)
- `FailedToUnRegister(HotKey)` - Unregister failed
- `OsError(io::Error)` - Platform-specific error
- `HotKeyParseError(String)` - Invalid hotkey string
- `UnrecognizedHotKeyCode(String)` - Unknown key code

## Usage in script-kit-gpui

### File Structure

- `src/hotkeys.rs` - Main hotkey management with unified routing
- `src/shortcuts/hotkey_compat.rs` - Shortcut string parsing

### Architecture

script-kit-gpui uses a **unified routing table** pattern:

```rust
// Global manager stored in OnceLock
static MAIN_MANAGER: OnceLock<Mutex<GlobalHotKeyManager>> = OnceLock::new();

// Routing table maps hotkey ID -> action
struct HotkeyRoutes {
    routes: HashMap<u32, RegisteredHotkey>,
    script_paths: HashMap<String, u32>,  // Reverse lookup
    main_id: Option<u32>,
    notes_id: Option<u32>,
    ai_id: Option<u32>,
}
```

### Hotkey Actions

```rust
pub enum HotkeyAction {
    Main,           // Main launcher
    Notes,          // Notes window
    Ai,             // AI window
    Script(String), // Run script at path
}
```

### Registration Pattern

**Transactional rebind** - register new BEFORE unregistering old:

```rust
fn rebind_hotkey_transactional(
    manager: &GlobalHotKeyManager,
    action: HotkeyAction,
    mods: Modifiers,
    code: Code,
    display: &str,
) -> bool {
    let new_hotkey = HotKey::new(Some(mods), code);
    
    // 1. Register new first (fail-safe)
    if let Err(e) = manager.register(new_hotkey) {
        return false; // Keep existing hotkey working
    }
    
    // 2. Update routing table
    // 3. Unregister old (best-effort)
}
```

### Shortcut String Parsing

The `parse_shortcut` function supports flexible formats:

```rust
// All equivalent:
parse_shortcut("cmd shift k")      // Space-separated
parse_shortcut("cmd+shift+k")      // Plus-separated
parse_shortcut("Cmd + Shift + K")  // Mixed with spaces

// Modifier aliases:
// cmd, command, meta, super, win -> Modifiers::META
// ctrl, control, ctl -> Modifiers::CONTROL
// alt, opt, option -> Modifiers::ALT
// shift, shft -> Modifiers::SHIFT
```

### Event Loop Integration

On macOS, script-kit-gpui uses GCD dispatch for immediate main-thread execution:

```rust
#[cfg(target_os = "macos")]
mod gcd {
    pub fn dispatch_to_main<F: FnOnce() + Send + 'static>(f: F) {
        // Uses dispatch_async_f to run on main thread
        // Works even before GPUI event loop is "warmed up"
    }
}
```

### Listener Thread

```rust
pub(crate) fn start_hotkey_listener(config: Config) {
    std::thread::spawn(move || {
        let manager = GlobalHotKeyManager::new().unwrap();
        
        // Register builtin hotkeys (main, notes, ai)
        // Register script shortcuts
        
        let receiver = GlobalHotKeyEvent::receiver();
        loop {
            if let Ok(event) = receiver.recv() {
                if event.state != HotKeyState::Pressed {
                    continue;
                }
                
                // Look up action in routing table
                let action = routes().read().unwrap().get_action(event.id);
                
                match action {
                    Some(HotkeyAction::Main) => { /* toggle main window */ }
                    Some(HotkeyAction::Script(path)) => { /* run script */ }
                    // ...
                }
            }
        }
    });
}
```

## Platform Differences

### macOS

- **Thread requirement**: Manager must be created on main thread
- **Event loop**: Requires NSApplication run loop
- **Reserved shortcuts**: Some system shortcuts can't be overridden (Cmd+Tab, Cmd+Space if Spotlight enabled)
- **Accessibility**: May require accessibility permissions

### Windows

- **Thread requirement**: Manager must be on same thread as win32 event loop
- **Not necessarily main thread**: Can be any thread with a message pump
- **Reserved shortcuts**: Win+L (lock), Ctrl+Alt+Del, etc.

### Linux (X11 only)

- **Wayland**: NOT SUPPORTED - use X11
- **X11 extensions**: Requires XInput for hotkey capture
- **Root window**: Grabs are registered on root window

## Anti-patterns

### 1. Creating Manager on Wrong Thread

```rust
// WRONG on macOS - will fail silently
std::thread::spawn(|| {
    let manager = GlobalHotKeyManager::new(); // May work but events won't fire
});

// CORRECT - create on main thread, store globally
let manager = GlobalHotKeyManager::new().unwrap();
static MANAGER: OnceLock<Mutex<GlobalHotKeyManager>> = OnceLock::new();
MANAGER.set(Mutex::new(manager)).unwrap();
```

### 2. Not Storing HotKey for Unregister

```rust
// WRONG - can't unregister later
manager.register(HotKey::new(Some(mods), code));

// CORRECT - store the HotKey object
let hotkey = HotKey::new(Some(mods), code);
stored_hotkeys.insert(hotkey.id(), hotkey);
manager.register(hotkey);

// Later...
manager.unregister(stored_hotkeys.remove(&id).unwrap());
```

### 3. Ignoring Registration Errors

```rust
// WRONG - silent failure
let _ = manager.register(hotkey);

// CORRECT - handle errors
match manager.register(hotkey) {
    Ok(()) => log!("Registered {}", shortcut),
    Err(Error::AlreadyRegistered(_)) => {
        log!("Conflict: {} used by another app", shortcut);
    }
    Err(e) => log!("Failed: {}", e),
}
```

### 4. Unregistering Before New Registration

```rust
// WRONG - user loses hotkey if new registration fails
manager.unregister(old_hotkey);
if manager.register(new_hotkey).is_err() {
    // Old hotkey is gone, new didn't work - user has no hotkey!
}

// CORRECT - transactional: register new first
if manager.register(new_hotkey).is_ok() {
    manager.unregister(old_hotkey); // Safe to remove old
} else {
    // Old hotkey still works
}
```

### 5. Not Handling HotKeyState

```rust
// WRONG - fires twice (press and release)
if let Ok(event) = receiver.recv() {
    run_action(event.id);
}

// CORRECT - only handle press events
if let Ok(event) = receiver.recv() {
    if event.state == HotKeyState::Pressed {
        run_action(event.id);
    }
}
```

### 6. Blocking Main Thread with recv()

```rust
// WRONG on macOS - blocks the main thread event loop
fn main() {
    let receiver = GlobalHotKeyEvent::receiver();
    loop {
        receiver.recv(); // Blocks forever, NSApplication never runs
    }
}

// CORRECT - run listener in separate thread
std::thread::spawn(|| {
    let receiver = GlobalHotKeyEvent::receiver();
    loop {
        if let Ok(event) = receiver.recv() {
            // Dispatch to main thread
        }
    }
});
// Main thread runs the GUI event loop
```

## Feature Flags

- `serde` - Enable serialization for HotKey
- `tracing` - Add tracing instrumentation

## See Also

- [keyboard-types](https://docs.rs/keyboard-types) - Key code definitions
- [tao](https://docs.rs/tao) - Window library (Tauri)
- [winit](https://docs.rs/winit) - Alternative window library
