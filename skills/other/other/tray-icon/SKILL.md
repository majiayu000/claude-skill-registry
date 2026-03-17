---
name: tray-icon
description: Cross-platform system tray and menu bar integration
tags: [tray, menu-bar, macos, system-tray, muda]
---

# tray-icon

Cross-platform system tray library from the Tauri ecosystem. Used in script-kit-gpui for macOS menu bar integration with a dropdown context menu.

**Crate**: [tray-icon](https://docs.rs/tray-icon/latest/tray_icon/) (v0.21.x)
**Menu System**: [muda](https://docs.rs/muda/latest/muda/) (re-exported as `tray_icon::menu`)

## Key Types

### Core Types (tray_icon)

| Type | Purpose |
|------|---------|
| `TrayIcon` | The tray icon instance. Must stay alive to keep icon visible. |
| `TrayIconBuilder` | Builder pattern for creating tray icons |
| `Icon` | RGBA pixel data for the tray icon |
| `TrayIconEvent` | Click events on the tray icon itself |
| `TrayIconEventReceiver` | Channel receiver for tray events |

### Menu Types (tray_icon::menu = muda)

| Type | Purpose |
|------|---------|
| `Menu` | Root menu (use with window menu bars) |
| `Submenu` | Submenu or context menu root (preferred for tray) |
| `MenuItem` | Basic text menu item |
| `IconMenuItem` | Menu item with icon |
| `CheckMenuItem` | Menu item with checkmark toggle |
| `PredefinedMenuItem` | OS-native items (separator, copy, paste, about, quit) |
| `MenuEvent` | Emitted when any menu item is clicked |
| `MenuEventReceiver` | Channel receiver for menu events |
| `MenuId` | Unique identifier for menu items |
| `ContextMenu` | Trait for types that can be shown as context menus |

## Usage in script-kit-gpui

### File Structure

```
src/tray.rs      # TrayManager, SVG rendering, menu creation
src/main.rs      # Event loop integration
```

### TrayManager Pattern

```rust
use tray_icon::{
    menu::{
        CheckMenuItem, ContextMenu, Icon as MenuIcon, IconMenuItem, 
        MenuEvent, MenuEventReceiver, MenuItem, PredefinedMenuItem, Submenu,
    },
    Icon, TrayIcon, TrayIconBuilder,
};

pub struct TrayManager {
    tray_icon: TrayIcon,  // Must stay alive!
    launch_at_login_item: CheckMenuItem,  // Store for later updates
}

impl TrayManager {
    pub fn new() -> Result<Self> {
        let icon = Self::create_icon_from_svg()?;
        let (menu, launch_at_login_item) = Self::create_menu()?;

        let mut builder = TrayIconBuilder::new()
            .with_icon(icon)
            .with_tooltip("Script Kit")
            .with_menu(menu);

        // macOS: Template images adapt to light/dark menu bar
        #[cfg(target_os = "macos")]
        {
            builder = builder.with_icon_as_template(true);
        }

        let tray_icon = builder.build()?;
        Ok(Self { tray_icon, launch_at_login_item })
    }
}
```

### Menu Event Receiver Pattern

```rust
impl TrayManager {
    pub fn menu_event_receiver(&self) -> &MenuEventReceiver {
        MenuEvent::receiver()  // Global receiver
    }
}
```

## Menu Building

### Use Submenu as Context Menu Root

On macOS, `Menu::append` only allows `Submenu`, but `Submenu::append` allows any item type. Use `Submenu` as your root for tray context menus:

```rust
fn create_menu() -> Result<(Box<dyn ContextMenu>, CheckMenuItem)> {
    // Submenu works cross-platform as context menu root
    let menu = Submenu::with_id("tray.root", "Script Kit", true);
    
    // Regular menu items
    let open_item = MenuItem::with_id("open", "Open App", true, None);
    menu.append(&open_item)?;
    
    // Separator
    menu.append(&PredefinedMenuItem::separator())?;
    
    // Icon menu items
    let icon = MenuIcon::from_rgba(rgba_data, 32, 32)?;
    let github_item = IconMenuItem::with_id(
        "github", 
        "Open on GitHub", 
        true,     // enabled
        Some(icon),
        None,     // no accelerator
    );
    menu.append(&github_item)?;
    
    // Check menu item (toggle state)
    let launch_item = CheckMenuItem::with_id(
        "launch_at_login",
        "Launch at Login",
        true,   // enabled
        false,  // initial checked state
        None,   // no accelerator
    );
    menu.append(&launch_item)?;
    
    // Return as ContextMenu trait object
    Ok((Box::new(menu), launch_item))
}
```

### Menu Item ID Pattern

Use string IDs for type-safe event matching:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TrayMenuAction {
    OpenApp,
    Settings,
    Quit,
}

impl TrayMenuAction {
    pub const fn id(self) -> &'static str {
        match self {
            Self::OpenApp => "tray.open_app",
            Self::Settings => "tray.settings",
            Self::Quit => "tray.quit",
        }
    }
    
    pub fn from_id(id: &str) -> Option<Self> {
        match id {
            "tray.open_app" => Some(Self::OpenApp),
            "tray.settings" => Some(Self::Settings),
            "tray.quit" => Some(Self::Quit),
            _ => None,
        }
    }
}

// Usage in menu creation:
let item = MenuItem::with_id(TrayMenuAction::OpenApp.id(), "Open", true, None);

// Usage in event handling:
pub fn action_from_event(event: &MenuEvent) -> Option<TrayMenuAction> {
    TrayMenuAction::from_id(&event.id.0)
}
```

## Icon Handling

### SVG to RGBA with usvg + resvg + tiny-skia

tray-icon requires RGBA pixel data. script-kit-gpui uses SVG rendering:

```rust
use usvg;
use tiny_skia;
use resvg;

fn render_svg_to_rgba(svg: &str, width: u32, height: u32) -> Result<Vec<u8>> {
    // Parse SVG
    let opts = usvg::Options::default();
    let tree = usvg::Tree::from_str(svg, &opts)?;

    // Create pixmap
    let mut pixmap = tiny_skia::Pixmap::new(width, height)?;

    // Calculate scale to fit
    let size = tree.size();
    let scale_x = width as f32 / size.width();
    let scale_y = height as f32 / size.height();
    let scale = scale_x.min(scale_y);
    let transform = tiny_skia::Transform::from_scale(scale, scale);

    // Render
    resvg::render(&tree, transform, &mut pixmap.as_mut());

    // Validate (catch silent rendering failures)
    let rgba = pixmap.take();
    let has_visible = rgba.chunks_exact(4).any(|px| px[3] != 0);
    if !has_visible {
        bail!("SVG rendered to fully transparent image");
    }

    Ok(rgba)
}

// Create tray icon from RGBA
fn create_icon_from_svg() -> Result<Icon> {
    let rgba = render_svg_to_rgba(LOGO_SVG, 32, 32)?;
    Icon::from_rgba(rgba, 32, 32)
}

// Create menu icon from RGBA  
fn create_menu_icon_from_svg(svg: &str) -> Option<MenuIcon> {
    render_svg_to_rgba(svg, 32, 32)
        .ok()
        .and_then(|rgba| MenuIcon::from_rgba(rgba, 32, 32).ok())
}
```

### Icon Sizes

- **Tray icon**: 32x32 (Retina: 64x64 or use template)
- **Menu icons**: 16x16 or 32x32 for Retina
- **macOS template**: Use monochrome SVGs with `with_icon_as_template(true)`

## Event Handling

### Polling Pattern (script-kit-gpui style)

```rust
// In main.rs - spawn async task for tray events
cx.spawn(async move |cx: &mut AsyncApp| {
    loop {
        Timer::after(Duration::from_millis(100)).await;
        
        // Check for menu events
        if let Ok(event) = tray_mgr.menu_event_receiver().try_recv() {
            let action = TrayManager::action_from_event(&event);
            
            match action {
                Some(TrayMenuAction::OpenApp) => {
                    let _ = cx.update(|cx| {
                        show_main_window(cx);
                    });
                }
                Some(TrayMenuAction::Quit) => {
                    let _ = cx.update(|cx| {
                        cx.quit();
                    });
                }
                _ => {}
            }
        }
    }
});
```

### Event Handler Pattern (alternative)

For winit/tao integration, use event handlers instead of polling:

```rust
use tray_icon::{TrayIconEvent, menu::MenuEvent};

// Forward to event loop
let proxy = event_loop.create_proxy();
TrayIconEvent::set_event_handler(Some(move |event| {
    proxy.send_event(UserEvent::TrayIconEvent(event));
}));

let proxy = event_loop.create_proxy();
MenuEvent::set_event_handler(Some(move |event| {
    proxy.send_event(UserEvent::MenuEvent(event));
}));
```

### Updating Menu State

```rust
// Update checkbox state
self.launch_at_login_item.set_checked(true);

// Update menu item text
menu_item.set_text("New Text");

// Enable/disable
menu_item.set_enabled(false);
```

## Platform Notes

### macOS

- **Threading**: Must create tray on main thread
- **Event loop**: Requires NSApplication run loop
- **Template images**: Use `with_icon_as_template(true)` for automatic light/dark adaptation
- **Timing**: Create after Application::new() initializes NSApplication

### Windows

- **Threading**: Create on same thread as win32 event loop
- **Accelerators**: Need `TranslateAcceleratorW` in message loop

### Linux

- **Backend**: Uses gtk + libappindicator (or libayatana-appindicator)
- **Dependencies**: `gtk3 xdotool libappindicator3-dev`

## Anti-patterns

### ❌ Dropping TrayIcon

```rust
// WRONG: Icon disappears immediately!
fn setup_tray() {
    let tray = TrayIconBuilder::new().build().unwrap();
    // tray dropped here, icon vanishes
}

// CORRECT: Store in struct
struct App {
    tray: TrayIcon,  // Lives as long as App
}
```

### ❌ Using Menu for Tray Context Menu

```rust
// WRONG: Menu::append only allows Submenu on macOS
let menu = Menu::new();
menu.append(&MenuItem::new("Item", true, None));  // Error on macOS!

// CORRECT: Use Submenu as root
let menu = Submenu::with_id("root", "Menu", true);
menu.append(&MenuItem::new("Item", true, None));  // Works everywhere
```

### ❌ Hardcoded String IDs

```rust
// WRONG: Error-prone, no compile-time checking
if event.id.0 == "open_app" { ... }  // Typo risk

// CORRECT: Enum with const IDs
if let Some(TrayMenuAction::OpenApp) = TrayMenuAction::from_id(&event.id.0) {
    // Type-safe matching
}
```

### ❌ Ignoring Icon Rendering Failures

```rust
// WRONG: Silent failure
let icon = Icon::from_rgba(rgba, 32, 32).ok();  // Swallows errors

// CORRECT: Validate and log
match render_svg_to_rgba(svg, 32, 32) {
    Ok(rgba) => MenuIcon::from_rgba(rgba, 32, 32).ok(),
    Err(e) => {
        warn!("Failed to render icon: {}", e);
        None
    }
}
```

### ❌ Blocking the Event Loop

```rust
// WRONG: Blocking poll
loop {
    if let Ok(event) = MenuEvent::receiver().recv() {  // Blocks!
        handle(event);
    }
}

// CORRECT: Non-blocking poll with timer
loop {
    Timer::after(Duration::from_millis(100)).await;
    if let Ok(event) = MenuEvent::receiver().try_recv() {  // Non-blocking
        handle(event);
    }
}
```

## Dependencies

Add to Cargo.toml:

```toml
[dependencies]
tray-icon = "0.21"

# For SVG icon rendering
usvg = "0.43"
resvg = "0.43"
tiny-skia = "0.11"
```

## See Also

- [tray-icon docs](https://docs.rs/tray-icon/latest/tray_icon/)
- [muda docs](https://docs.rs/muda/latest/muda/)
- [tauri-apps/tray-icon GitHub](https://github.com/tauri-apps/tray-icon)
