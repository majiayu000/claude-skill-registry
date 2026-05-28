---
name: macos-accessibility
description: macOS Accessibility APIs for automation and text selection
tags: [macos, accessibility, ax, automation, window-control, selected-text]
---

# macos-accessibility

macOS Accessibility APIs enable cross-application automation including window control, text selection reading, keyboard monitoring, and UI element inspection. Script-kit-gpui uses these APIs extensively for text expansion, window tiling, and getting selected text from other applications.

## Crate Dependencies

```toml
# Cargo.toml
get-selected-text = "0.1"      # Hybrid AX + clipboard fallback for reading selected text
macos-accessibility-client = "0.0.1"  # Permission checking for accessibility APIs
```

## Permission Requirements

### Why Accessibility Permission Is Required

Accessibility permission enables:
- **Text expansion / snippets** - Global keyboard monitoring
- **Window control** (move, resize, tile) - Cross-process window manipulation
- **Get selected text from other apps** - AXSelectedText attribute access
- **Global keyboard shortcuts** - System-wide hotkey capture

### Checking Permission

```rust
use macos_accessibility_client::accessibility;

/// Check if accessibility permissions are granted
pub fn has_accessibility_permission() -> bool {
    accessibility::application_is_trusted()
}
```

### Requesting Permission (Shows System Dialog)

```rust
use macos_accessibility_client::accessibility;

/// Request accessibility permission - opens System Preferences with prompt
pub fn request_accessibility_permission() -> bool {
    accessibility::application_is_trusted_with_prompt()
}
```

### Opening Settings Directly

```rust
use std::process::Command;

/// Open System Preferences to Accessibility pane (no prompt)
pub fn open_accessibility_settings() -> std::io::Result<()> {
    Command::new("open")
        .arg("x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility")
        .spawn()?;
    Ok(())
}
```

### Permission Flow in script-kit-gpui

See `src/permissions_wizard.rs` for the complete permission management system:
- `PermissionStatus` - Overall permission state
- `PermissionInfo` - Per-permission details with UI-ready descriptions
- `check_all_permissions()` - Main entry point

## Reading Selected Text

The `get-selected-text` crate provides a hybrid approach with automatic fallbacks:

```rust
use get_selected_text::get_selected_text as get_selected_text_impl;

pub fn get_selected_text() -> Result<String> {
    // Check permissions first
    if !has_accessibility_permission() {
        bail!("Accessibility permission required");
    }
    
    // The crate handles:
    // 1. AXSelectedText attribute (fastest, most reliable)
    // 2. AXSelectedTextRange + AXStringForRange (fallback)
    // 3. Clipboard simulation with Cmd+C (last resort)
    match get_selected_text_impl() {
        Ok(text) => Ok(text),
        Err(e) => bail!("Failed to get selected text: {}", e),
    }
}
```

### Selection Reading Strategies (in order)

1. **AXSelectedText** - Direct attribute read, fastest
2. **AXSelectedTextRange + AXStringForRange** - Range-based fallback
3. **Clipboard simulation** - Saves clipboard, sends Cmd+C, restores

The crate caches per-app behavior with an LRU cache for efficiency.

## Setting Selected Text (Replace Selection)

```rust
use arboard::Clipboard;

pub fn set_selected_text(text: &str) -> Result<()> {
    if !has_accessibility_permission() {
        bail!("Accessibility permission required");
    }
    
    let mut clipboard = Clipboard::new()?;
    
    // Save original clipboard
    let original = clipboard.get_text().ok();
    
    // Set new text
    clipboard.set_text(text)?;
    thread::sleep(Duration::from_millis(10));
    
    // Simulate Cmd+V
    simulate_paste_with_cg()?;
    thread::sleep(Duration::from_millis(50));
    
    // Restore original clipboard
    if let Some(original_text) = original {
        thread::sleep(Duration::from_millis(100));
        clipboard.set_text(&original_text)?;
    }
    
    Ok(())
}
```

### Simulating Paste with Core Graphics

```rust
use core_graphics::event::{CGEvent, CGEventFlags, CGEventTapLocation, CGKeyCode};
use core_graphics::event_source::{CGEventSource, CGEventSourceStateID};

pub fn simulate_paste_with_cg() -> Result<()> {
    const KEY_V: CGKeyCode = 9;  // 'v' keycode on macOS
    
    let source = CGEventSource::new(CGEventSourceStateID::HIDSystemState)
        .ok().context("Failed to create CGEventSource")?;
    
    // Key down with Cmd
    let key_down = CGEvent::new_keyboard_event(source.clone(), KEY_V, true)
        .ok().context("Failed to create key down event")?;
    key_down.set_flags(CGEventFlags::CGEventFlagCommand);
    
    // Key up with Cmd
    let key_up = CGEvent::new_keyboard_event(source, KEY_V, false)
        .ok().context("Failed to create key up event")?;
    key_up.set_flags(CGEventFlags::CGEventFlagCommand);
    
    // Post events
    key_down.post(CGEventTapLocation::HID);
    thread::sleep(Duration::from_millis(5));
    key_up.post(CGEventTapLocation::HID);
    
    Ok(())
}
```

## AXUIElement API

### FFI Declarations

```rust
#![allow(non_upper_case_globals)]

use std::ffi::c_void;

type AXUIElementRef = *const c_void;
type CFTypeRef = *const c_void;
type CFStringRef = *const c_void;
type CFArrayRef = *const c_void;

#[link(name = "ApplicationServices", kind = "framework")]
extern "C" {
    fn AXUIElementCreateSystemWide() -> AXUIElementRef;
    fn AXUIElementCreateApplication(pid: i32) -> AXUIElementRef;
    fn AXUIElementCopyAttributeValue(
        element: AXUIElementRef,
        attribute: CFStringRef,
        value: *mut CFTypeRef,
    ) -> i32;
    fn AXUIElementSetAttributeValue(
        element: AXUIElementRef,
        attribute: CFStringRef,
        value: CFTypeRef,
    ) -> i32;
    fn AXUIElementPerformAction(element: AXUIElementRef, action: CFStringRef) -> i32;
    fn AXUIElementIsAttributeSettable(
        element: AXUIElementRef,
        attribute: CFStringRef,
        settable: *mut bool,
    ) -> i32;
}

// AXError codes
const kAXErrorSuccess: i32 = 0;
const kAXErrorAPIDisabled: i32 = -25211;
const kAXErrorNoValue: i32 = -25212;
```

### Getting Attribute Values

```rust
fn get_ax_attribute(element: AXUIElementRef, attribute: &str) -> Result<CFTypeRef> {
    let attr_str = create_cf_string(attribute);
    let mut value: CFTypeRef = std::ptr::null();
    
    let result = unsafe {
        AXUIElementCopyAttributeValue(element, attr_str, &mut value as *mut CFTypeRef)
    };
    
    cf_release(attr_str);
    
    match result {
        kAXErrorSuccess => Ok(value),
        kAXErrorAPIDisabled => bail!("Accessibility API is disabled"),
        kAXErrorNoValue => bail!("No value for attribute: {}", attribute),
        _ => bail!("Failed to get attribute {}: error {}", attribute, result),
    }
}
```

### Setting Attribute Values

```rust
fn set_ax_attribute(element: AXUIElementRef, attribute: &str, value: CFTypeRef) -> Result<()> {
    let attr_str = create_cf_string(attribute);
    let result = unsafe { AXUIElementSetAttributeValue(element, attr_str, value) };
    cf_release(attr_str);
    
    match result {
        kAXErrorSuccess => Ok(()),
        kAXErrorAPIDisabled => bail!("Accessibility API is disabled"),
        _ => bail!("Failed to set attribute {}: error {}", attribute, result),
    }
}
```

### Checking Attribute Settability

```rust
pub fn is_attribute_settable(element: AXUIElementRef, attribute: &str) -> bool {
    if element.is_null() {
        return false;
    }
    
    let attr_str = create_cf_string(attribute);
    let mut settable = false;
    
    let result = unsafe {
        AXUIElementIsAttributeSettable(element, attr_str, &mut settable as *mut bool)
    };
    
    cf_release(attr_str);
    result == kAXErrorSuccess && settable
}
```

### Common AX Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `AXPosition` | AXValue (CGPoint) | Window position |
| `AXSize` | AXValue (CGSize) | Window dimensions |
| `AXTitle` | CFString | Window title |
| `AXWindows` | CFArray | Application's windows |
| `AXFocusedWindow` | AXUIElement | Currently focused window |
| `AXMainWindow` | AXUIElement | Application's main window |
| `AXMinimized` | CFBoolean | Minimization state |
| `AXSelectedText` | CFString | Currently selected text |
| `AXSelectedTextRange` | AXValue | Selection range |
| `AXCloseButton` | AXUIElement | Close button element |
| `AXMinimizeButton` | AXUIElement | Minimize button element |
| `AXFullScreenButton` | AXUIElement | Fullscreen button element |

### Common AX Actions

| Action | Description |
|--------|-------------|
| `AXRaise` | Bring window to front |
| `AXPress` | Press a button element |

## Window Control Pattern

See `src/window_control.rs` for complete implementation.

### Listing Windows

```rust
pub fn list_windows() -> Result<Vec<WindowInfo>> {
    if !has_accessibility_permission() {
        bail!("Accessibility permission required");
    }
    
    let mut windows = Vec::new();
    
    // Iterate running applications via NSWorkspace
    unsafe {
        use objc::{msg_send, sel, sel_impl};
        use objc::runtime::{Class, Object};
        
        let workspace_class = Class::get("NSWorkspace")?;
        let workspace: *mut Object = msg_send![workspace_class, sharedWorkspace];
        let running_apps: *mut Object = msg_send![workspace, runningApplications];
        
        // For each app...
        let ax_app = AXUIElementCreateApplication(pid);
        if let Ok(windows_value) = get_ax_attribute(ax_app, "AXWindows") {
            // Iterate windows...
        }
        cf_release(ax_app);
    }
    
    Ok(windows)
}
```

### Getting Focused Window of Previous App

For LSUIElement (accessory) apps like Script Kit that don't take menu bar ownership:

```rust
pub fn get_frontmost_window_of_previous_app() -> Result<Option<WindowInfo>> {
    // Menu bar owner is the previously active app
    let target_pid = get_menu_bar_owner_pid()?;
    
    let ax_app = unsafe { AXUIElementCreateApplication(target_pid) };
    
    // Strategy 1: AXFocusedWindow (most accurate)
    // Strategy 2: AXMainWindow (fallback)
    // Strategy 3: First window in AXWindows array
    
    // ...
}

pub fn get_menu_bar_owner_pid() -> Result<i32> {
    unsafe {
        let workspace: *mut Object = msg_send![workspace_class, sharedWorkspace];
        let menu_owner: *mut Object = msg_send![workspace, menuBarOwningApplication];
        let pid: i32 = msg_send![menu_owner, processIdentifier];
        Ok(pid)
    }
}
```

### Window Capability Detection

See `src/window_control_enhanced/capabilities.rs`:

```rust
pub fn detect_window_capabilities(ax_element: *const c_void) -> WindowCapabilities {
    WindowCapabilities {
        can_move: is_attribute_settable(ax_element, "AXPosition"),
        can_resize: is_attribute_settable(ax_element, "AXSize"),
        can_minimize: has_attribute(ax_element, "AXMinimizeButton"),
        can_close: has_attribute(ax_element, "AXCloseButton"),
        can_fullscreen: has_attribute(ax_element, "AXFullScreenButton"),
        supports_space_move: false,
    }
}
```

## CoreFoundation Memory Management

**Critical**: AX functions follow CoreFoundation naming conventions:
- `AXUIElementCreate*` - Returns owned object, caller must release
- `AXUIElementCopy*` - Returns owned copy, caller must release
- `CFArrayGetValueAtIndex` - Returns borrowed reference, retain if keeping

```rust
fn cf_release(cf: CFTypeRef) {
    if !cf.is_null() {
        unsafe { CFRelease(cf); }
    }
}

fn cf_retain(cf: CFTypeRef) -> CFTypeRef {
    if !cf.is_null() {
        unsafe { CFRetain(cf) }
    } else {
        cf
    }
}
```

### Retain Pattern for Array Elements

```rust
// CFArrayGetValueAtIndex returns borrowed - must retain for storage
let ax_window = CFArrayGetValueAtIndex(windows_value as CFArrayRef, j);
let retained_window = cf_retain(ax_window);  // Now we own it
cache_window(window_id, retained_window as AXUIElementRef);

// Release the array when done
cf_release(windows_value);
```

## Privacy Considerations

### What Triggers Permission Dialogs

- `accessibility::application_is_trusted_with_prompt()` - Shows system dialog
- First AX API call without permission - May show dialog

### What Does NOT Trigger Dialogs

- `accessibility::application_is_trusted()` - Silent check
- Opening settings URL directly

### User Flow

1. Check permission silently at startup
2. If missing, show custom UI explaining why it's needed
3. Provide button that calls `request_accessibility_permission()`
4. Optionally show "Open Settings" button for manual enablement

## Fallback Strategies

### When AX API Fails

1. **No permission** - Guide user through permission flow
2. **App doesn't support AX** - Fall back to clipboard simulation
3. **Element not accessible** - Try parent element or alternate attribute
4. **Operation fails** - Check `AXUIElementIsAttributeSettable` first

### Clipboard Fallback for Text Operations

```rust
// Always save/restore clipboard
let original = clipboard.get_text().ok();
// ... do operation ...
if let Some(orig) = original {
    clipboard.set_text(&orig)?;
}
```

## Anti-Patterns

### Memory Leaks

```rust
// BAD: Leaks CFString
let attr = create_cf_string("AXPosition");
// ... use attr but never release ...

// GOOD: Always release
let attr = create_cf_string("AXPosition");
// ... use attr ...
cf_release(attr);
```

### Dangling References

```rust
// BAD: Using borrowed reference after array released
let window = CFArrayGetValueAtIndex(array, 0);
cf_release(array);  // window is now invalid!
do_something(window);  // CRASH

// GOOD: Retain before releasing array
let window = cf_retain(CFArrayGetValueAtIndex(array, 0));
cf_release(array);
do_something(window);  // Safe
cf_release(window);  // Clean up our retained copy
```

### Missing Permission Checks

```rust
// BAD: Will fail cryptically
pub fn get_windows() -> Vec<Window> {
    let ax_app = AXUIElementCreateApplication(pid);
    // ...
}

// GOOD: Fail fast with clear error
pub fn get_windows() -> Result<Vec<Window>> {
    if !has_accessibility_permission() {
        bail!("Accessibility permission required");
    }
    // ...
}
```

### Blocking on Permission Request

```rust
// BAD: Blocks UI thread waiting for user
let granted = request_accessibility_permission();
if !granted {
    panic!("Need permission!");
}

// GOOD: Non-blocking flow
if !has_accessibility_permission() {
    show_permission_ui();
    return; // Let user grant permission in their own time
}
```

## Key Files in script-kit-gpui

| File | Purpose |
|------|---------|
| `src/selected_text.rs` | Get/set selected text operations |
| `src/window_control.rs` | Window listing, moving, resizing, tiling |
| `src/window_control_enhanced/` | Enhanced window ops with capability detection |
| `src/permissions_wizard.rs` | Permission checking and UI data |
| `src/expand_manager.rs` | Text expansion using keyboard monitoring |
| `src/executor/selected_text.rs` | Message handlers for selected text |

## Testing Accessibility Code

```rust
#[cfg(all(test, feature = "system-tests"))]
mod system_tests {
    #[test]
    fn test_permission_check_does_not_panic() {
        let _ = has_accessibility_permission();
    }
    
    #[test]
    #[ignore] // Requires manual setup
    fn test_get_selected_text() {
        // 1. Open TextEdit, type and select text
        // 2. Run: cargo test --features system-tests test_get_selected_text -- --ignored
        let text = get_selected_text().expect("Should get selected text");
        assert!(!text.is_empty());
    }
}
```
