---
name: macos-core-frameworks
description: macOS Core Graphics and Core Foundation Rust bindings for display management, keyboard simulation, and event handling
tags: [macos, core-graphics, core-foundation, keyboard, display, events]
---

# macos-core-frameworks

Rust bindings to macOS Core Graphics and Core Foundation frameworks via the `core-graphics` (0.24) and `core-foundation` (0.10) crates. These provide low-level access to display information, keyboard simulation, event taps, and run loop management.

## Crate Dependencies

```toml
[dependencies]
core-graphics = "0.24"
core-foundation = "0.10"
foreign-types = "0.5"  # For ForeignType trait (CGEvent pointer access)
```

## Core Graphics

The `core-graphics` crate provides bindings to macOS Core Graphics (Quartz) framework.

### Key Modules

| Module | Purpose |
|--------|---------|
| `display` | Display enumeration, bounds, screenshots |
| `event` | CGEvent creation, posting, event taps |
| `event_source` | CGEventSource for keyboard/mouse events |
| `geometry` | CGPoint, CGSize, CGRect |

### CGEvent for Keyboard Simulation

Create and post keyboard events to simulate keystrokes system-wide.

```rust
use core_graphics::event::{CGEvent, CGEventFlags, CGEventTapLocation, CGKeyCode};
use core_graphics::event_source::{CGEventSource, CGEventSourceStateID};

/// Simulate a keystroke with optional modifiers
fn simulate_key(keycode: CGKeyCode, modifiers: CGEventFlags) -> anyhow::Result<()> {
    // Create event source - HIDSystemState is standard for synthetic events
    let source = CGEventSource::new(CGEventSourceStateID::HIDSystemState)
        .ok()
        .context("Failed to create CGEventSource")?;
    
    // Key down event
    let key_down = CGEvent::new_keyboard_event(source.clone(), keycode, true)
        .ok()
        .context("Failed to create key down event")?;
    key_down.set_flags(modifiers);
    
    // Key up event
    let key_up = CGEvent::new_keyboard_event(source, keycode, false)
        .ok()
        .context("Failed to create key up event")?;
    key_up.set_flags(modifiers);
    
    // Post to HID system (reaches all applications)
    key_down.post(CGEventTapLocation::HID);
    std::thread::sleep(std::time::Duration::from_millis(5));
    key_up.post(CGEventTapLocation::HID);
    
    Ok(())
}

// Common keycodes
const KEY_BACKSPACE: CGKeyCode = 51;
const KEY_V: CGKeyCode = 9;
const KEY_C: CGKeyCode = 8;
const KEY_TAB: CGKeyCode = 48;
const KEY_RETURN: CGKeyCode = 36;
const KEY_ESCAPE: CGKeyCode = 53;
```

### Simulating Cmd+V (Paste)

```rust
fn simulate_paste() -> anyhow::Result<()> {
    use core_graphics::event::{CGEvent, CGEventFlags, CGEventTapLocation, CGKeyCode};
    use core_graphics::event_source::{CGEventSource, CGEventSourceStateID};

    const KEY_V: CGKeyCode = 9;

    let source = CGEventSource::new(CGEventSourceStateID::HIDSystemState)
        .ok()
        .context("Failed to create CGEventSource")?;

    let key_down = CGEvent::new_keyboard_event(source.clone(), KEY_V, true)
        .ok()
        .context("Failed to create paste key down event")?;
    key_down.set_flags(CGEventFlags::CGEventFlagCommand);

    let key_up = CGEvent::new_keyboard_event(source, KEY_V, false)
        .ok()
        .context("Failed to create paste key up event")?;
    key_up.set_flags(CGEventFlags::CGEventFlagCommand);

    key_down.post(CGEventTapLocation::HID);
    std::thread::sleep(std::time::Duration::from_millis(5));
    key_up.post(CGEventTapLocation::HID);

    Ok(())
}
```

### CGEventFlags Reference

```rust
use core_graphics::event::CGEventFlags;

// Modifier flags
CGEventFlags::CGEventFlagShift      // Shift key
CGEventFlags::CGEventFlagControl    // Control key  
CGEventFlags::CGEventFlagAlternate  // Option/Alt key
CGEventFlags::CGEventFlagCommand    // Command key

// Check flags on received events
let flags = event.get_flags();
let has_cmd = flags.contains(CGEventFlags::CGEventFlagCommand);
```

### CGEventTap for Global Keyboard Monitoring

Capture keyboard events system-wide (requires Accessibility permission).

```rust
use core_graphics::event::{
    CGEvent, CGEventTap, CGEventTapLocation, CGEventTapOptions, 
    CGEventTapPlacement, CGEventType, EventField,
};
use core_foundation::runloop::{kCFRunLoopCommonModes, CFRunLoop};

fn create_keyboard_monitor(callback: impl Fn(&CGEvent) + Send + 'static) -> Result<()> {
    let event_tap = CGEventTap::new(
        CGEventTapLocation::HID,           // Capture at HID level
        CGEventTapPlacement::HeadInsertEventTap,
        CGEventTapOptions::ListenOnly,     // Don't modify events
        vec![CGEventType::KeyDown],        // Only key down events
        move |_proxy, event_type, event: &CGEvent| {
            // Handle tap disabled events
            match event_type {
                CGEventType::TapDisabledByTimeout |
                CGEventType::TapDisabledByUserInput => {
                    // Re-enable tap (see reenable_tap pattern below)
                    return None;
                }
                _ => {}
            }
            
            // Extract key information
            let keycode = event.get_integer_value_field(
                EventField::KEYBOARD_EVENT_KEYCODE
            ) as u16;
            let is_repeat = event.get_integer_value_field(
                EventField::KEYBOARD_EVENT_AUTOREPEAT
            ) != 0;
            
            callback(event);
            None  // Return None to not modify the event
        },
    )?;
    
    // Create run loop source and add to current run loop
    let source = event_tap.mach_port.create_runloop_source(0)?;
    unsafe {
        CFRunLoop::get_current().add_source(&source, kCFRunLoopCommonModes);
    }
    event_tap.enable();
    
    Ok(())
}
```

### Getting Unicode Character from CGEvent

The `core-graphics` crate doesn't expose `CGEventKeyboardGetUnicodeString`, so use FFI:

```rust
fn get_character_from_event(event: &CGEvent) -> Option<String> {
    extern "C" {
        fn CGEventKeyboardGetUnicodeString(
            event: core_graphics::sys::CGEventRef,
            max_len: libc::c_ulong,
            actual_len: *mut libc::c_ulong,
            buffer: *mut u16,
        );
    }

    const BUFFER_SIZE: usize = 32;
    let mut buffer: [u16; BUFFER_SIZE] = [0; BUFFER_SIZE];
    let mut actual_len: libc::c_ulong = 0;

    unsafe {
        use foreign_types::ForeignType;
        let event_ptr = event.as_ptr();
        CGEventKeyboardGetUnicodeString(
            event_ptr,
            BUFFER_SIZE as libc::c_ulong,
            &mut actual_len,
            buffer.as_mut_ptr(),
        );
    }

    if actual_len > 0 && (actual_len as usize) <= BUFFER_SIZE {
        String::from_utf16(&buffer[..actual_len as usize]).ok()
    } else {
        None
    }
}
```

### Display Management

```rust
use core_graphics::display::{CGDisplay, CGRect};

/// Get all active displays
fn get_displays() -> Result<Vec<u32>> {
    CGDisplay::active_displays()
        .map_err(|e| anyhow::anyhow!("Failed to get displays: error {}", e))
}

/// Get main display
fn get_main_display() -> CGDisplay {
    CGDisplay::main()
}

/// Get display bounds
fn get_display_bounds(display_id: u32) -> CGRect {
    let display = CGDisplay::new(display_id);
    display.bounds()  // Returns CGRect with origin and size
}

/// Check if display is main
fn is_main_display(display_id: u32) -> bool {
    display_id == CGDisplay::main().id
}
```

### CGPoint and CGSize for Window Position/Size

```rust
use core_graphics::geometry::{CGPoint, CGSize};

// Create point
let point = CGPoint::new(100.0, 200.0);

// Create size  
let size = CGSize::new(800.0, 600.0);

// Used with AXValue for accessibility APIs
use std::ffi::c_void;

extern "C" {
    fn AXValueCreate(value_type: i32, value: *const c_void) -> *const c_void;
}

const kAXValueTypeCGPoint: i32 = 1;
const kAXValueTypeCGSize: i32 = 2;

let point = CGPoint::new(100.0, 200.0);
let ax_point = unsafe {
    AXValueCreate(kAXValueTypeCGPoint, &point as *const _ as *const c_void)
};
```

## Core Foundation

The `core-foundation` crate provides bindings to macOS Core Foundation framework.

### Key Modules

| Module | Purpose |
|--------|---------|
| `runloop` | CFRunLoop for event loop management |
| `mach_port` | CFMachPort for event tap sources |
| `base` | TCFType trait for CF object management |
| `string` | CFString operations |

### CFRunLoop for Event Processing

Required for CGEventTap to receive events.

```rust
use core_foundation::runloop::{
    kCFRunLoopCommonModes, kCFRunLoopDefaultMode, 
    CFRunLoop, CFRunLoopRunResult,
};
use std::time::Duration;

// Get current thread's run loop
let run_loop = CFRunLoop::get_current();

// Add event source to run loop
unsafe {
    run_loop.add_source(&run_loop_source, kCFRunLoopCommonModes);
}

// Run loop with timeout (non-blocking check)
let result = CFRunLoop::run_in_mode(
    unsafe { kCFRunLoopDefaultMode },
    Duration::from_millis(100),
    true,  // return after source handled
);

match result {
    CFRunLoopRunResult::Stopped => { /* Loop was stopped */ }
    CFRunLoopRunResult::TimedOut => { /* Timeout elapsed */ }
    CFRunLoopRunResult::HandledSource => { /* Source was handled */ }
    _ => {}
}

// Stop the run loop (from another thread)
run_loop.stop();
```

### CFMachPort for Event Tap

```rust
use core_foundation::base::TCFType;
use core_foundation::mach_port::CFMachPortRef;

// After creating CGEventTap, get mach port
let mach_port_ref = event_tap.mach_port.as_concrete_TypeRef();

// Re-enable a disabled tap
extern "C" {
    fn CGEventTapEnable(tap: CFMachPortRef, enable: bool);
}

unsafe {
    CGEventTapEnable(mach_port_ref, true);
}
```

## Usage in script-kit-gpui

### Keyboard Monitoring (`keyboard_monitor.rs`)

Global keystroke capture for text expansion triggers:

- `CGEventTap` with `CGEventTapLocation::HID` for system-wide capture
- `CFRunLoop` on dedicated background thread
- Handles tap disable/re-enable for reliability
- Extracts key codes, modifiers, and Unicode characters

### Text Injection (`text_injector.rs`)

Delete trigger text and paste replacement:

- Simulates backspace key events via `CGEvent`
- Simulates Cmd+V for clipboard paste
- Uses `CGEventSourceStateID::HIDSystemState`

### Selected Text (`selected_text.rs`)

Get/set selected text in any application:

- Simulates Cmd+C/Cmd+V with modifier flags
- Posts to `CGEventTapLocation::HID`

### Display Info (`window_control.rs`, `display.rs`)

Query display configuration:

- `CGDisplay::active_displays()` for all monitors
- `CGDisplay::bounds()` for screen dimensions
- Coordinate conversion between CG and Cocoa systems

## CGEventTapLocation Options

| Location | Description | Use Case |
|----------|-------------|----------|
| `HID` | Hardware level | Keyboard simulation, global monitoring |
| `Session` | User session | App-specific events |
| `AnnotatedSession` | With annotations | Accessibility apps |

## Anti-patterns

### Don't Use CombinedSessionState for Simulation

```rust
// WRONG - May not work reliably for simulation
let source = CGEventSource::new(CGEventSourceStateID::CombinedSessionState);

// CORRECT - Use HIDSystemState for synthetic keyboard events
let source = CGEventSource::new(CGEventSourceStateID::HIDSystemState);
```

### Don't Forget to Handle Tap Disable Events

```rust
// Event taps can be disabled by system timeout or user input
// Always handle CGEventType::TapDisabledByTimeout and TapDisabledByUserInput
match event_type {
    CGEventType::TapDisabledByTimeout |
    CGEventType::TapDisabledByUserInput => {
        // Re-enable the tap!
        unsafe { CGEventTapEnable(port, true); }
        return None;
    }
    _ => {}
}
```

### Don't Block the Main Thread with CFRunLoop

```rust
// WRONG - Blocks main thread
CFRunLoop::run_in_mode(kCFRunLoopDefaultMode, Duration::MAX, false);

// CORRECT - Run on dedicated thread with periodic checks
std::thread::spawn(move || {
    while running.load(Ordering::SeqCst) {
        CFRunLoop::run_in_mode(
            kCFRunLoopDefaultMode,
            Duration::from_millis(100),
            true,
        );
    }
});
```

### Don't Forget Key Up Events

```rust
// WRONG - Key gets stuck
let key_down = CGEvent::new_keyboard_event(source, keycode, true)?;
key_down.post(CGEventTapLocation::HID);

// CORRECT - Always send down AND up
let key_down = CGEvent::new_keyboard_event(source.clone(), keycode, true)?;
key_down.post(CGEventTapLocation::HID);
std::thread::sleep(Duration::from_millis(5));
let key_up = CGEvent::new_keyboard_event(source, keycode, false)?;
key_up.post(CGEventTapLocation::HID);
```

### Don't Forget Accessibility Permissions

Event taps require Accessibility permission:

```rust
use macos_accessibility_client::accessibility;

if !accessibility::application_is_trusted() {
    // Show permission dialog or return error
    accessibility::application_is_trusted_with_prompt();
    return Err("Accessibility permission required");
}
```

## Memory Management

Core Foundation objects follow reference counting:

```rust
// Objects from "Copy" functions are owned - must release
extern "C" {
    fn CFRelease(cf: *const c_void);
}

// Objects from "Get" functions are borrowed - don't release
// CFArrayGetValueAtIndex returns borrowed reference

// Retain to extend lifetime beyond container
extern "C" {
    fn CFRetain(cf: *const c_void) -> *const c_void;
}
```

## Common Key Codes

| Key | Code | Key | Code |
|-----|------|-----|------|
| A-Z | 0-25 (varies) | Backspace | 51 |
| Return | 36 | Tab | 48 |
| Escape | 53 | Space | 49 |
| V | 9 | C | 8 |
| X | 7 | Z | 6 |

## References

- [core-graphics crate docs](https://docs.rs/core-graphics/latest/core_graphics/)
- [core-foundation crate docs](https://docs.rs/core-foundation/latest/core_foundation/)
- [Apple CGEvent Reference](https://developer.apple.com/documentation/coregraphics/cgevent)
- [Apple CFRunLoop Reference](https://developer.apple.com/documentation/corefoundation/cfrunloop)
