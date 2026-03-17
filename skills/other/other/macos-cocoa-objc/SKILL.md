---
name: macos-cocoa-objc
description: macOS Cocoa and Objective-C interop for Rust applications
triggers:
  - cocoa
  - objc
  - NSWindow
  - NSApplication
  - NSView
  - NSScreen
  - NSPasteboard
  - NSWorkspace
  - AppKit
  - vibrancy
  - window level
  - floating panel
---

# macOS Cocoa/Objective-C Interop

This skill covers using the `cocoa` and `objc` crates to interact with macOS AppKit/Cocoa APIs from Rust. Script-kit-gpui uses these extensively for window management, system integration, and native UI features.

## Crate Overview

### `cocoa` crate (v0.26.x)
- **Purpose**: Rust bindings to Cocoa/AppKit frameworks
- **Deprecated**: In favor of `objc2` crates, but still widely used
- **Modules**:
  - `cocoa::appkit` - NSApp, NSWindow, NSScreen, NSPasteboard, etc.
  - `cocoa::base` - `id`, `nil`, `YES`, `NO`, `BOOL`
  - `cocoa::foundation` - NSString, NSRect, NSPoint, NSSize, NSArray
  - `cocoa::quartzcore` - Core Animation (CALayer, etc.)

### `objc` crate (v0.2.x)
- **Purpose**: Low-level Objective-C runtime bindings
- **Key macros**: `msg_send!`, `sel!`, `class!`
- **Modules**:
  - `objc::runtime` - Class, Object, Sel, Method, objc_getClass
  - `objc::declare` - ClassDecl for creating Objective-C classes
  - `objc::rc` - autoreleasepool

## Key Concepts

### Objective-C Messaging
All Objective-C method calls use message sending. In Rust:

```rust
use objc::{msg_send, sel, sel_impl, class};
use cocoa::base::{id, nil};

unsafe {
    // [NSApp sharedApplication]
    let app: id = msg_send![class!(NSApplication), sharedApplication];
    
    // [window setLevel:3]
    let _: () = msg_send![window, setLevel: 3i64];
    
    // [window frame] - returns NSRect
    let frame: NSRect = msg_send![window, frame];
    
    // [window isKeyWindow] - returns bool
    let is_key: bool = msg_send![window, isKeyWindow];
}
```

### Selectors
Selectors are method name identifiers:

```rust
use objc::{sel, sel_impl};

let sel_frame = sel!(frame);
let sel_set_level = sel!(setLevel:);
let sel_set_frame_display = sel!(setFrame:display:);  // Multiple args
```

### The `id` Type
`id` is a pointer to any Objective-C object (`*mut objc::runtime::Object`).
- `nil` is the null pointer equivalent
- Always check for null before using

## Common AppKit Types

### NSApplication (NSApp)
```rust
use cocoa::appkit::NSApp;
use cocoa::base::id;

unsafe {
    let app: id = NSApp();
    
    // Set activation policy (0=Regular, 1=Accessory, 2=Prohibited)
    let _: () = msg_send![app, setActivationPolicy: 1i64];
    
    // Check if active
    let is_active: bool = msg_send![app, isActive];
    
    // Get all windows
    let windows: id = msg_send![app, windows];
    let count: usize = msg_send![windows, count];
}
```

### NSWindow
```rust
use cocoa::foundation::NSRect;

unsafe {
    // Window levels (NSWindowLevel)
    const NS_NORMAL_WINDOW_LEVEL: i64 = 0;
    const NS_FLOATING_WINDOW_LEVEL: i64 = 3;
    const NS_MODAL_PANEL_WINDOW_LEVEL: i64 = 8;
    const NS_POP_UP_MENU_WINDOW_LEVEL: i64 = 101;
    
    let _: () = msg_send![window, setLevel: NS_FLOATING_WINDOW_LEVEL];
    
    // Collection behaviors (bitflags)
    const MOVE_TO_ACTIVE_SPACE: u64 = 1 << 1;  // 2
    const FULL_SCREEN_AUXILIARY: u64 = 1 << 8; // 256
    const CAN_JOIN_ALL_SPACES: u64 = 1;
    const STATIONARY: u64 = 16;
    const IGNORES_CYCLE: u64 = 64;
    
    let current: u64 = msg_send![window, collectionBehavior];
    let new_behavior = current | MOVE_TO_ACTIVE_SPACE | FULL_SCREEN_AUXILIARY;
    let _: () = msg_send![window, setCollectionBehavior: new_behavior];
    
    // Frame operations
    let frame: NSRect = msg_send![window, frame];
    let _: () = msg_send![window, setFrame:new_frame display:true];
    
    // Visibility
    let _: () = msg_send![window, orderFront: nil];  // Show
    let _: () = msg_send![window, orderOut: nil];    // Hide
    let _: () = msg_send![window, makeKeyAndOrderFront: nil];
    
    // Properties
    let _: () = msg_send![window, setMovable: false];
    let _: () = msg_send![window, setOpaque: false];
    let _: () = msg_send![window, setHasShadow: true];
    let _: () = msg_send![window, setRestorable: false];
    let _: () = msg_send![window, setIgnoresMouseEvents: true];
}
```

### NSScreen
```rust
use cocoa::appkit::NSScreen;

unsafe {
    // Get all screens
    let screens: id = NSScreen::screens(nil);
    let count: usize = msg_send![screens, count];
    
    // Get main screen (primary display)
    let main_screen: id = NSScreen::mainScreen(nil);
    let frame: NSRect = msg_send![main_screen, frame];
    let visible_frame: NSRect = msg_send![main_screen, visibleFrame];
}
```

### NSPasteboard (Clipboard)
```rust
use cocoa::appkit::NSPasteboard;

unsafe {
    let pasteboard: id = NSPasteboard::generalPasteboard(nil);
    
    // Efficient change detection (no payload read)
    let change_count: i64 = msg_send![pasteboard, changeCount];
}
```

### NSWorkspace
```rust
unsafe {
    let workspace: id = msg_send![class!(NSWorkspace), sharedWorkspace];
    
    // Get frontmost app
    let app: id = msg_send![workspace, frontmostApplication];
    let menu_owner: id = msg_send![workspace, menuBarOwningApplication];
    
    // App info
    let bundle_id: id = msg_send![app, bundleIdentifier];
    let name: id = msg_send![app, localizedName];
    let pid: i32 = msg_send![app, processIdentifier];
}
```

### NSColor
```rust
unsafe {
    // System colors
    let clear: id = msg_send![class!(NSColor), clearColor];
    let window_bg: id = msg_send![class!(NSColor), windowBackgroundColor];
    
    // Custom RGBA
    let color: id = msg_send![class!(NSColor),
        colorWithRed: 0.5f64
        green: 0.5f64
        blue: 0.5f64
        alpha: 0.8f64
    ];
}
```

### NSVisualEffectView (Vibrancy/Blur)
```rust
// Materials (NSVisualEffectMaterial)
const POPOVER: isize = 6;
const SIDEBAR: isize = 7;
const HUD_WINDOW: isize = 13;

// Blending modes
const BEHIND_WINDOW: isize = 0;
const WITHIN_WINDOW: isize = 1;

// States
const FOLLOWS_WINDOW: isize = 0;
const ACTIVE: isize = 1;
const INACTIVE: isize = 2;

unsafe {
    let _: () = msg_send![effect_view, setMaterial: POPOVER];
    let _: () = msg_send![effect_view, setBlendingMode: BEHIND_WINDOW];
    let _: () = msg_send![effect_view, setState: FOLLOWS_WINDOW];
    let _: () = msg_send![effect_view, setEmphasized: true];
}
```

### NSAppearance
```rust
#[link(name = "AppKit", kind = "framework")]
extern "C" {
    static NSAppearanceNameDarkAqua: id;
    static NSAppearanceNameVibrantDark: id;
    static NSAppearanceNameAqua: id;
    static NSAppearanceNameVibrantLight: id;
}

unsafe {
    let appearance: id = msg_send![
        class!(NSAppearance),
        appearanceNamed: NSAppearanceNameVibrantDark
    ];
    let _: () = msg_send![window, setAppearance: appearance];
}
```

## Usage in script-kit-gpui

### Window Level and Floating Panels
```rust
// From src/platform.rs - configure as floating panel
pub fn configure_as_floating_panel() {
    unsafe {
        let window = get_main_window()?;
        
        // Float above normal windows
        let _: () = msg_send![window, setLevel: 3i64];
        
        // Move to active space when shown
        let current: u64 = msg_send![window, collectionBehavior];
        let desired = current | 2 | 256;  // MoveToActiveSpace | FullScreenAuxiliary
        let _: () = msg_send![window, setCollectionBehavior: desired];
        
        // Disable restoration
        let _: () = msg_send![window, setRestorable: false];
    }
}
```

### HUD Windows (Click-Through Overlays)
```rust
// From src/hud_manager.rs
unsafe {
    let _: () = msg_send![window, setLevel: 101i64];  // PopUpMenuLevel
    
    // Behaviors for HUD
    let behaviors: u64 = 1 | 16 | 64;  // CanJoinAllSpaces | Stationary | IgnoresCycle
    let _: () = msg_send![window, setCollectionBehavior: behaviors];
    
    // Click-through for non-interactive HUDs
    let _: () = msg_send![window, setIgnoresMouseEvents: true];
    
    // Show without activating
    let _: () = msg_send![window, orderFront: nil];
}
```

### Vibrancy Material Configuration
```rust
// From src/platform.rs - match Raycast/Spotlight appearance
pub fn configure_window_vibrancy_material() {
    unsafe {
        // Force VibrantDark appearance
        let appearance: id = msg_send![
            class!(NSAppearance),
            appearanceNamed: NSAppearanceNameVibrantDark
        ];
        let _: () = msg_send![window, setAppearance: appearance];
        
        // Window background for native border
        let bg: id = msg_send![class!(NSColor), windowBackgroundColor];
        let _: () = msg_send![window, setBackgroundColor: bg];
        let _: () = msg_send![window, setOpaque: false];
        let _: () = msg_send![window, setHasShadow: true];
    }
}
```

### Accessory App (No Dock Icon)
```rust
// From src/platform.rs - LSUIElement equivalent at runtime
pub fn configure_as_accessory_app() {
    unsafe {
        let app: id = NSApp();
        // NSApplicationActivationPolicyAccessory = 1
        let _: () = msg_send![app, setActivationPolicy: 1i64];
    }
}
```

## Unsafe Patterns

### Basic Pattern
```rust
#[cfg(target_os = "macos")]
pub fn do_cocoa_thing() {
    unsafe {
        // All Cocoa calls are unsafe
    }
}

#[cfg(not(target_os = "macos"))]
pub fn do_cocoa_thing() {
    // No-op on other platforms
}
```

### Null Checking
```rust
unsafe {
    let window: id = msg_send![app, keyWindow];
    if window.is_null() {
        return None;  // Handle gracefully
    }
    // Safe to use window
}
```

### Type Annotations are Required
```rust
// WRONG - compiler can't infer return type
let result = msg_send![obj, someMethod];

// CORRECT - explicit type annotation
let result: id = msg_send![obj, someMethod];
let _: () = msg_send![obj, setFoo: bar];  // void returns need ()
```

### Integer Types Matter
```rust
// NSInteger is i64 on 64-bit macOS
let _: () = msg_send![window, setLevel: 3i64];

// NSUInteger is u64
let behavior: u64 = msg_send![window, collectionBehavior];

// Some APIs use isize
let material: isize = msg_send![effect_view, material];
```

## Memory Management

### Autorelease Pools
Required when creating Objective-C objects on background threads:

```rust
use objc::rc::autoreleasepool;

std::thread::spawn(|| {
    autoreleasepool(|| unsafe {
        // Create NSStrings, etc. here
        let string: id = msg_send![class!(NSString), stringWithUTF8String: "hello"];
        // Objects are released when pool drains
    });
});
```

### When Pools are Needed
- Background threads without existing pool
- Notification callbacks
- Any code that creates many temporary Objective-C objects

### Manual Retain/Release (Rare)
```rust
unsafe {
    let obj: id = msg_send![class!(SomeClass), alloc];
    let obj: id = msg_send![obj, init];
    // obj has +1 retain count
    
    let _: () = msg_send![obj, release];  // -1 retain count
}
```

## Threading

### Main Thread Requirement
**CRITICAL**: AppKit APIs (NSApp, NSWindow, NSScreen, etc.) are NOT thread-safe and MUST be called from the main thread.

```rust
#[cfg(target_os = "macos")]
fn debug_assert_main_thread() {
    unsafe {
        let is_main: bool = msg_send![class!(NSThread), isMainThread];
        debug_assert!(
            is_main,
            "AppKit calls must run on the main thread"
        );
    }
}

pub fn some_appkit_function() {
    debug_assert_main_thread();
    unsafe {
        // Safe to call AppKit APIs
    }
}
```

### Thread-Safe Wrappers
For storing window IDs across threads:

```rust
#[derive(Debug, Clone, Copy)]
struct WindowId(usize);

impl WindowId {
    fn from_id(window: id) -> Self {
        Self(window as usize)
    }
    fn to_id(self) -> id {
        self.0 as id
    }
}

// Safe because we only store the ID, not access the window
unsafe impl Send for WindowId {}
unsafe impl Sync for WindowId {}
```

### Background Observers
For notification observers on background threads:

```rust
std::thread::spawn(|| {
    setup_workspace_observer();  // Creates run loop
});

fn setup_workspace_observer() {
    autoreleasepool(|| unsafe {
        // Create observer class
        // Register for notifications
        // Run the run loop
    });
}
```

## Creating Objective-C Classes

For notification observers or delegates:

```rust
use objc::declare::ClassDecl;
use objc::runtime::{Class, Object, Sel};

unsafe {
    let superclass = Class::get("NSObject").unwrap();
    
    // Check if class already exists
    let observer_class = if let Some(existing) = Class::get("MyObserver") {
        existing
    } else {
        let mut decl = ClassDecl::new("MyObserver", superclass).unwrap();
        
        // Add method
        extern "C" fn handle_notification(
            _this: &Object,
            _sel: Sel,
            notification: *mut Object,
        ) {
            let _ = std::panic::catch_unwind(|| {
                autoreleasepool(|| unsafe {
                    // Handle notification
                });
            });
        }
        
        decl.add_method(
            sel!(handleNotification:),
            handle_notification as extern "C" fn(&Object, Sel, *mut Object),
        );
        
        decl.register()
    };
}
```

## NSString Conversion

### Rust String to NSString
```rust
unsafe fn rust_to_nsstring(s: &str) -> id {
    let c_str = std::ffi::CString::new(s).unwrap();
    msg_send![class!(NSString), stringWithUTF8String: c_str.as_ptr()]
}
```

### NSString to Rust String
```rust
unsafe fn nsstring_to_rust(nsstring: id) -> Option<String> {
    if nsstring.is_null() {
        return None;
    }
    let c_str: *const std::os::raw::c_char = msg_send![nsstring, UTF8String];
    if c_str.is_null() {
        return None;
    }
    Some(std::ffi::CStr::from_ptr(c_str).to_string_lossy().into_owned())
}
```

## Anti-patterns

### Don't Use keyWindow During Startup
```rust
// WRONG - keyWindow may be nil during startup
let window: id = msg_send![app, keyWindow];

// CORRECT - use a window registry
let window = window_manager::get_main_window()?;
```

### Don't Forget Return Type Annotations
```rust
// WRONG - won't compile
msg_send![window, setLevel: 3];

// CORRECT
let _: () = msg_send![window, setLevel: 3i64];
```

### Don't Call AppKit from Background Threads
```rust
// WRONG - will crash or produce undefined behavior
std::thread::spawn(|| {
    let app: id = NSApp();  // BAD!
});

// CORRECT - use main thread
cx.spawn(|mut cx| async move {
    cx.update(|cx| {
        // AppKit calls here are on main thread
    });
});
```

### Don't Ignore Platform Checks
```rust
// WRONG - won't compile on other platforms
use cocoa::base::id;  // Only exists on macOS

// CORRECT
#[cfg(target_os = "macos")]
use cocoa::base::id;

#[cfg(target_os = "macos")]
pub fn macos_only_function() { ... }

#[cfg(not(target_os = "macos"))]
pub fn macos_only_function() {
    // No-op or appropriate fallback
}
```

### Don't Swizzle Without Checking
```rust
// WRONG - may swizzle multiple times
pub fn swizzle_method() {
    // swizzle code
}

// CORRECT - use atomic flag
static SWIZZLE_DONE: AtomicBool = AtomicBool::new(false);

pub fn swizzle_method() {
    if SWIZZLE_DONE.swap(true, Ordering::SeqCst) {
        return;  // Already done
    }
    // swizzle code
}
```

## Coordinate System

macOS uses a bottom-left origin coordinate system, opposite of most UI frameworks:

```rust
/// Convert from AppKit (bottom-left origin) to top-left origin
fn flip_y(screen_height: f64, y: f64, height: f64) -> f64 {
    screen_height - y - height
}

/// Get primary screen height for coordinate conversion
fn primary_screen_height() -> Option<f64> {
    unsafe {
        let screens: id = NSScreen::screens(nil);
        if screens.is_null() { return None; }
        let primary: id = msg_send![screens, objectAtIndex: 0usize];
        if primary.is_null() { return None; }
        let frame: NSRect = msg_send![primary, frame];
        Some(frame.size.height)
    }
}
```

## Quick Reference

| Task | Code |
|------|------|
| Get app | `NSApp()` |
| Get window | `msg_send![app, keyWindow]` |
| Set level | `msg_send![window, setLevel: 3i64]` |
| Show window | `msg_send![window, orderFront: nil]` |
| Hide window | `msg_send![window, orderOut: nil]` |
| Get frame | `msg_send![window, frame]` -> NSRect |
| Is main thread | `msg_send![class!(NSThread), isMainThread]` -> bool |
| Null check | `if obj.is_null() { return; }` |
| Platform guard | `#[cfg(target_os = "macos")]` |
