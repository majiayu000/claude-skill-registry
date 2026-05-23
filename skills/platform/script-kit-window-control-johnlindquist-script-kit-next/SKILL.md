---
name: script-kit-window-control
description: |
  Window management APIs for Script Kit GPUI using macOS Accessibility (AX) APIs.
  Use when working with: window positioning/tiling, window state persistence, 
  display/monitor detection, window capabilities, resize coalescing, or
  Space (virtual desktop) operations. Covers modules: window_control.rs,
  window_control_enhanced/, window_manager.rs, window_ops.rs, window_resize.rs,
  window_state.rs.
---

# Script Kit Window Control

Window management system for Script Kit GPUI, built on macOS Accessibility APIs.

## Architecture Overview

```
window_control.rs          - Core AX-based window operations (list, move, resize, tile)
window_control_enhanced/   - Enhanced types: WindowBounds, capabilities, DisplayInfo, SpaceManager
window_manager.rs          - Thread-safe window registry by role (Main, Notes, AI)
window_ops.rs              - Coalesced window operations via Window::defer
window_resize.rs           - Dynamic height calculation for different view types
window_state.rs            - Window position persistence to ~/.sk/kit/window-state.json
```

## Coordinate Systems

**Critical**: Two coordinate systems are used internally:

| System | Origin | Y Direction | Used By |
|--------|--------|-------------|---------|
| AX (Accessibility) | Top-left of main screen | Grows downward | `window_control.rs`, `window_control_enhanced/` |
| AppKit (NSScreen) | Bottom-left of main screen | Grows upward | NSScreen.visibleFrame, coordinate conversion |

Conversion functions in `window_control_enhanced/coords.rs`:
- `appkit_to_ax()` / `ax_to_appkit()` - Point conversion
- `nsrect_to_bounds()` / `bounds_to_nsrect()` - Full rect conversion

## Quick Reference

### Check Accessibility Permission
```rust
use crate::window_control::{has_accessibility_permission, request_accessibility_permission};

if !has_accessibility_permission() {
    request_accessibility_permission(); // Opens System Preferences
}
```

### List Windows
```rust
use crate::window_control::list_windows;

let windows = list_windows()?;
for w in windows {
    println!("{}: {} - {}", w.id, w.app, w.title);
}
```

### Tile Window (Script Kit's Primary Use Case)
```rust
use crate::window_control::{tile_window, TilePosition, get_frontmost_window_of_previous_app};

// Get the window user was working with before invoking Script Kit
if let Some(window) = get_frontmost_window_of_previous_app()? {
    tile_window(window.id, TilePosition::LeftHalf)?;
}
```

### Window Operations
```rust
use crate::window_control::{move_window, resize_window, set_window_bounds, Bounds};

move_window(window_id, 100, 200)?;
resize_window(window_id, 800, 600)?;
set_window_bounds(window_id, Bounds::new(100, 200, 800, 600))?;
```

### Coalesced Operations (Prevents Jitter)
```rust
use crate::window_ops::{queue_resize, queue_move};

// Multiple calls coalesce - only final value executes
queue_resize(500.0, window, cx);
queue_move(bounds, window, cx);
```

### Window Registry
```rust
use crate::window_manager::{register_window, get_main_window, WindowRole};

register_window(WindowRole::Main, ns_window_id);
let main = get_main_window(); // Returns Option<id>
```

### Persistence
```rust
use crate::window_state::{save_window_bounds, load_window_bounds, WindowRole, PersistedWindowBounds};

// Save on hide/close
save_window_bounds(WindowRole::Main, PersistedWindowBounds::from_gpui(window_bounds));

// Restore on open
if let Some(bounds) = load_window_bounds(WindowRole::Main) {
    // Use bounds.to_gpui() for WindowOptions
}
```

## Reference Files

For detailed API documentation:
- [window-control-core.md](references/window-control-core.md) - Core AX operations, TilePosition, WindowInfo
- [window-control-enhanced.md](references/window-control-enhanced.md) - WindowBounds, capabilities, DisplayInfo, SpaceManager
- [window-manager.md](references/window-manager.md) - Thread-safe window registry
- [window-ops.md](references/window-ops.md) - Coalesced operations
- [window-resize.md](references/window-resize.md) - Dynamic height calculation
- [window-state.md](references/window-state.md) - Persistence APIs

## Common Patterns

### Script Kit Window Targeting

Script Kit is an LSUIElement (accessory app) that doesn't take menu bar ownership.
To act on the window the user was focused on before Script Kit:

```rust
// This returns the focused window of the menu bar owner (the previous app)
let target = get_frontmost_window_of_previous_app()?;
```

### Safe Resize During Render Cycle

Never resize directly in render callbacks - use coalescing:

```rust
// BAD: Can cause RefCell borrow panic
platform::resize_first_window_to_height(height);

// GOOD: Deferred to end of effect cycle
window_ops::queue_resize(height, window, cx);
```

### Multi-Monitor Window Restoration

```rust
use crate::window_state::{get_initial_bounds, is_bounds_visible};
use crate::platform::get_macos_displays;

let displays = get_macos_displays();
let bounds = get_initial_bounds(WindowRole::Main, default_bounds, &displays);
// Automatically clamps to visible display if saved position is offscreen
```
