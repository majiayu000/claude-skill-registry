---
name: script-kit-platform
description: Platform integration, hotkeys, and system actions for script-kit-gpui
---

# script-kit-platform

Platform-specific functionality for script-kit-gpui including window configuration, global hotkeys, system actions, and frontmost app tracking. The codebase uses conditional compilation (`#[cfg(target_os = "macos")]`) to provide macOS-specific implementations with no-op fallbacks for other platforms.

## Key Source Files

- `src/platform.rs` - Window configuration, floating panels, vibrancy
- `src/hotkeys.rs` - Global hotkey registration and routing
- `src/system_actions.rs` - AppleScript-based system actions
- `src/frontmost_app_tracker.rs` - Track previously active application

## Window Configuration (platform.rs)

### Floating Panel Setup

Configure windows to float above normal windows and follow the active macOS space:

```rust
use crate::platform;

// Configure app as accessory (no Dock icon, no menu bar ownership)
platform::configure_as_accessory_app();

// Make window float above others and move to active space
platform::configure_as_floating_panel();
```

**Key Constants:**
- `NS_FLOATING_WINDOW_LEVEL = 3` - Float above normal windows
- `NS_WINDOW_COLLECTION_BEHAVIOR_MOVE_TO_ACTIVE_SPACE = 2` - Follow active space
- `NS_WINDOW_COLLECTION_BEHAVIOR_FULL_SCREEN_AUXILIARY = 256` - Show over fullscreen apps

### Window Visibility

```rust
// Hide main window without hiding entire app
platform::hide_main_window();

// Check if main window has focus
if platform::is_main_window_focused() {
    // Window is key window
}

// Check if app is active
if platform::is_app_active() {
    // App has focus
}

// Get window bounds (x, y, width, height) in top-left coordinates
if let Some((x, y, w, h)) = platform::get_main_window_bounds() {
    // Use bounds
}
```

### Vibrancy Configuration

The platform module handles NSVisualEffectView configuration for the frosted glass effect:

```rust
// Configure window with VibrantDark appearance + POPOVER material
platform::configure_window_vibrancy_material();

// Cycle through vibrancy materials for testing (Cmd+Shift+M)
let desc = platform::cycle_vibrancy_material();
```

**Vibrancy Materials (ns_visual_effect_material):**
- `POPOVER = 6` - Matches Electron's `vibrancy: 'popover'` (default)
- `HUD_WINDOW = 13` - Dark, high contrast
- `SIDEBAR = 7` - Standard sidebar appearance
- `SELECTION = 4` - GPUI's default (colorless)

### GPUI BlurredView Swizzle

GPUI hides the CAChameleonLayer (native tint layer). Call once at startup to preserve it:

```rust
platform::swizzle_gpui_blurred_view();
```

## Global Hotkeys (hotkeys.rs)

### Hotkey Action Types

```rust
pub enum HotkeyAction {
    Main,           // Main launcher hotkey
    Notes,          // Notes window hotkey
    Ai,             // AI window hotkey
    Script(String), // Script shortcut with path
}
```

### Starting the Hotkey Listener

```rust
use crate::hotkeys;
use crate::config;

let config = config::load_config();
hotkeys::start_hotkey_listener(config);
```

### Checking Hotkey Registration

```rust
if hotkeys::is_main_hotkey_registered() {
    // Main hotkey is active
}
```

### Registering Script Hotkeys

```rust
// Register a script hotkey
let hotkey_id = hotkeys::register_script_hotkey(
    "/path/to/script.ts",
    "cmd+shift+k"
)?;

// Unregister
hotkeys::unregister_script_hotkey("/path/to/script.ts")?;

// Update (handles add/remove/change)
hotkeys::update_script_hotkey(
    "/path/to/script.ts",
    Some("cmd+shift+k"),  // old
    Some("cmd+shift+j"),  // new
)?;
```

### Dynamic Shortcuts (shortcuts.json)

```rust
// Register a command shortcut
hotkeys::register_dynamic_shortcut(
    "scriptlet/my-scriptlet",
    "cmd+shift+p",
    "My Scriptlet"
)?;
```

### Hotkey Channels

Hotkey events are dispatched through async channels:

```rust
// Main launcher hotkey
let (tx, rx) = hotkeys::hotkey_channel();

// Script shortcuts (sends script path)
let (tx, rx) = hotkeys::script_hotkey_channel();

// Notes window hotkey
let (tx, rx) = hotkeys::notes_hotkey_channel();

// AI window hotkey
let (tx, rx) = hotkeys::ai_hotkey_channel();
```

### GCD Dispatch for Immediate Execution

On macOS, hotkey handlers can be dispatched directly to the main thread via GCD, bypassing the async runtime for immediate response:

```rust
hotkeys::set_notes_hotkey_handler(|| {
    // Called on main thread immediately when hotkey pressed
});

hotkeys::set_ai_hotkey_handler(|| {
    // Called on main thread immediately
});
```

### Hot-Reload Support

Hotkeys support transactional updates - new hotkey is registered before unregistering old:

```rust
hotkeys::update_hotkeys(&config);
```

## System Actions (system_actions.rs)

All system actions use AppleScript via `osascript` and return `Result<(), String>`.

### Power Management

```rust
use crate::system_actions;

system_actions::lock_screen()?;     // Ctrl+Cmd+Q
system_actions::sleep()?;           // Put system to sleep
system_actions::restart()?;         // Restart (prompts to save)
system_actions::shut_down()?;       // Shutdown (prompts to save)
system_actions::log_out()?;         // Log out current user
```

### UI Controls

```rust
system_actions::toggle_dark_mode()?;    // Toggle light/dark mode
system_actions::show_desktop()?;        // Hide all windows (Cmd+F11)
system_actions::mission_control()?;     // Ctrl+Up Arrow
system_actions::launchpad()?;           // Open Launchpad
system_actions::force_quit_apps()?;     // Cmd+Option+Escape
system_actions::start_screen_saver()?;  // Activate screen saver
```

### Volume Controls

```rust
system_actions::set_volume(75)?;     // Set volume (0-100)
system_actions::volume_mute()?;      // Toggle mute

// These are #[allow(dead_code)] but available:
system_actions::volume_up()?;        // +6.25%
system_actions::volume_down()?;      // -6.25%
let level = system_actions::get_volume()?;
let muted = system_actions::is_muted()?;
```

### System Preferences Navigation

```rust
// Open to specific pane
system_actions::open_system_preferences("com.apple.preference.security")?;

// Convenience functions
system_actions::open_privacy_settings()?;
system_actions::open_display_settings()?;
system_actions::open_sound_settings()?;
system_actions::open_network_settings()?;
system_actions::open_keyboard_settings()?;
system_actions::open_bluetooth_settings()?;
system_actions::open_notifications_settings()?;
system_actions::open_system_preferences_main()?;
```

**Common Pane IDs:**
- `com.apple.preference.security` - Privacy & Security
- `com.apple.preference.displays` - Displays
- `com.apple.preference.sound` - Sound
- `com.apple.preference.network` - Network
- `com.apple.preference.keyboard` - Keyboard
- `com.apple.preference.bluetooth` - Bluetooth
- `com.apple.preference.notifications` - Notifications

### Trash Management

```rust
system_actions::empty_trash()?;
```

### Do Not Disturb

```rust
system_actions::toggle_do_not_disturb()?;  // Toggle Focus mode
```

## Frontmost App Tracking (frontmost_app_tracker.rs)

Track the "last real application" active before Script Kit opened. Essential for:
- Menu bar actions (get menus from previous app)
- Window tiling (tile previous app's windows)
- Context-aware actions

### Starting the Tracker

Call once at startup:

```rust
use crate::frontmost_app_tracker;

frontmost_app_tracker::start_tracking();
```

### Getting Tracked App Info

```rust
#[derive(Debug, Clone)]
pub struct TrackedApp {
    pub pid: i32,
    pub bundle_id: String,  // e.g., "com.google.Chrome"
    pub name: String,       // e.g., "Google Chrome"
}

if let Some(app) = frontmost_app_tracker::get_last_real_app() {
    println!("Last app: {} ({}) PID {}", app.name, app.bundle_id, app.pid);
}
```

### Pre-Cached Menu Items

Menu items are fetched in the background when an app becomes active:

```rust
let menu_items = frontmost_app_tracker::get_cached_menu_items();

// Check if still fetching
if frontmost_app_tracker::is_fetching_menu() {
    // Wait or show loading state
}
```

### How It Works

1. An NSWorkspace observer watches `NSWorkspaceDidActivateApplicationNotification`
2. When an app activates:
   - If NOT Script Kit: update tracked app, fetch menu items in background
   - If IS Script Kit: ignore (keep tracking previous app)
3. Uses `menuBarOwningApplication` since Script Kit is LSUIElement (no Dock icon)
4. Tracks both bundle_id AND PID to detect app relaunches

## Platform Differences

### macOS (Full Support)
- All features implemented using AppKit, Cocoa, Objective-C runtime
- AppleScript for system actions
- NSWorkspace for app tracking
- GCD for main thread dispatch

### Windows (Stub)
- All platform functions are no-ops
- Returns sensible defaults (`true` for `is_app_active()`, etc.)

### Linux (Stub)
- All platform functions are no-ops
- Returns sensible defaults

## Thread Safety

### Main Thread Requirements

**CRITICAL**: AppKit APIs (NSApp, NSWindow, NSScreen) are NOT thread-safe and MUST be called from the main thread.

```rust
// All platform.rs functions use this assertion internally:
fn debug_assert_main_thread() {
    unsafe {
        let is_main: bool = msg_send![class!(NSThread), isMainThread];
        debug_assert!(is_main, "AppKit calls must run on the main thread");
    }
}
```

### Global State Protection

- `TRACKER_STATE` - Uses `parking_lot::RwLock` for concurrent access
- `HOTKEY_ROUTES` - Uses `std::sync::RwLock` for fast reads
- `MAIN_MANAGER` - Uses `std::sync::Mutex` for hotkey manager access

## Anti-patterns

### 1. Calling Platform APIs from Background Threads

```rust
// WRONG - will panic in debug builds
std::thread::spawn(|| {
    platform::configure_as_floating_panel(); // AppKit call from background thread!
});

// RIGHT - use GCD dispatch or call from main thread
gcd::dispatch_to_main(|| {
    platform::configure_as_floating_panel();
});
```

### 2. Not Checking for Platform Support

```rust
// WRONG - assumes macOS
let bounds = platform::get_main_window_bounds().unwrap();

// RIGHT - handle None for non-macOS
if let Some((x, y, w, h)) = platform::get_main_window_bounds() {
    // Use bounds
}
```

### 3. Ignoring Hotkey Registration Failures

```rust
// WRONG - silently fails
let _ = hotkeys::register_script_hotkey(path, shortcut);

// RIGHT - handle the error
match hotkeys::register_script_hotkey(path, shortcut) {
    Ok(id) => logging::log("HOTKEY", &format!("Registered: {}", id)),
    Err(e) => logging::log("ERROR", &format!("Failed: {}", e)),
}
```

### 4. Polling Instead of Using Channels

```rust
// WRONG - busy polling
loop {
    if hotkey_pressed.load(Ordering::Relaxed) {
        // handle
    }
    std::thread::sleep(Duration::from_millis(10));
}

// RIGHT - use async channels
let (_, rx) = hotkeys::hotkey_channel();
while let Ok(_) = rx.recv().await {
    // handle immediately when pressed
}
```

### 5. Not Handling App Relaunches

```rust
// WRONG - only checks bundle_id
if current_app.bundle_id != new_app.bundle_id {
    refresh_cache();
}

// RIGHT - also check PID (app may have been relaunched)
if current_app.bundle_id != new_app.bundle_id || current_app.pid != new_app.pid {
    refresh_cache();  // Handles relaunch case
}
```

### 6. Blocking Main Thread with System Actions

```rust
// WRONG - AppleScript can block
platform::configure_as_floating_panel();
system_actions::empty_trash()?;  // Blocks until Finder responds

// RIGHT - run potentially slow actions in background
std::thread::spawn(|| {
    let _ = system_actions::empty_trash();
});
```

### 7. Not Using Transactional Hotkey Updates

```rust
// WRONG - unregister first, may lose hotkey on failure
manager.unregister(old_hotkey)?;
manager.register(new_hotkey)?;  // If this fails, hotkey is gone!

// RIGHT - register new first (this is what update_hotkeys does)
manager.register(new_hotkey)?;   // Try new first
manager.unregister(old_hotkey);  // Only then remove old
```

## Configuration Integration

Platform hotkeys are configured via `config.ts`:

```typescript
// Main launcher hotkey
hotkey: {
  key: "Semicolon",
  modifiers: ["meta"]
}

// Notes window hotkey
notes: {
  hotkey: {
    key: "KeyN",
    modifiers: ["meta", "shift"]
  }
}

// AI window hotkey
ai: {
  hotkey: {
    key: "KeyK",
    modifiers: ["meta", "shift"]
  }
}

// Custom command shortcuts
commands: {
  "my-script": {
    shortcut: {
      key: "KeyP",
      modifiers: ["meta", "shift"]
    }
  }
}
```

## Logging

All platform modules use the centralized logging system:

```rust
use crate::logging;

logging::log("PANEL", "Configured as floating panel");
logging::log("HOTKEY", "Registered main hotkey");
logging::log("APP", "App activated: Chrome");
logging::log("VIBRANCY", "Set material to POPOVER");
```

Log prefixes:
- `PANEL` - Window configuration
- `HOTKEY` - Hotkey registration/events
- `APP` - App tracking
- `VIBRANCY` - Visual effect configuration
- `ACTIONS` - System actions
