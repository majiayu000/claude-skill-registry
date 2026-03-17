---
name: script-kit-menu-bar
description: |
  macOS menu bar accessibility system for Script Kit GPUI. Covers AX-based menu reading,
  recursive menu parsing, menu action execution, and SQLite caching. Use when:
  (1) Reading application menu bars via Accessibility APIs
  (2) Executing menu actions programmatically
  (3) Caching menu structures for performance
  (4) Working with AXUIElement hierarchy (App -> MenuBar -> MenuBarItem -> Menu -> MenuItem)
  (5) Handling keyboard shortcuts and modifier flags
---

# Script Kit Menu Bar System

macOS Accessibility API-based menu bar reading and execution for Script Kit GPUI.

## Architecture Overview

```
AXApplication
    |
    +-- AXMenuBar
           |
           +-- AXMenuBarItem (File, Edit, View...)
                   |
                   +-- AXMenu (container)
                           |
                           +-- AXMenuItem (with shortcuts, children)
```

## Core Modules

| Module | Purpose | Reference |
|--------|---------|-----------|
| `menu_bar.rs` | Read menu hierarchies via AX APIs | [menu-bar-reader.md](references/menu-bar-reader.md) |
| `menu_executor.rs` | Execute menu actions via AXPress | [menu-executor.md](references/menu-executor.md) |
| `menu_cache.rs` | SQLite persistence for menu data | [menu-cache.md](references/menu-cache.md) |

## Quick Reference

### Reading Menus

```rust
use script_kit_gpui::menu_bar::{get_frontmost_menu_bar, get_menu_bar_for_pid};

// Read menu bar of current menu owner (not frontmost app!)
let items = get_frontmost_menu_bar()?;

// Read specific app's menu by PID
let items = get_menu_bar_for_pid(pid)?;
```

### Executing Actions

```rust
use script_kit_gpui::menu_executor::execute_menu_action;

// App MUST be frontmost for this to work
execute_menu_action("com.apple.Safari", &["File", "New Window"])?;
```

### Using Cache

```rust
use script_kit_gpui::menu_cache::*;

init_menu_cache_db()?;  // Call once at startup

// Check cache first
if let Some(items) = get_cached_menu("com.apple.Safari")? {
    if is_cache_valid("com.apple.Safari", 3600)? {
        return Ok(items);
    }
}

// Scan and cache
let items = scan_menu_bar()?;
set_cached_menu("com.apple.Safari", &items, Some("17.0"))?;
```

## Key Concepts

### Menu Bar Owner vs Frontmost App

Script Kit runs as `LSUIElement` (accessory app) and doesn't take menu bar ownership:

- **Menu bar owner**: App whose menus appear in system menu bar
- **Frontmost app**: App receiving keyboard/mouse input
- Use `menuBarOwningApplication` to get the correct target

### AX Element Path

Each `MenuBarItem` stores `ax_element_path: Vec<usize>` - indices to navigate back to the element:

```rust
// Path [0, 2] means: menu bar item at index 0, child at index 2
pub struct MenuBarItem {
    pub ax_element_path: Vec<usize>,
    // ...
}
```

### Keyboard Shortcuts

```rust
pub struct KeyboardShortcut {
    pub key: String,           // "S", "N", "Q"
    pub modifiers: ModifierFlags,
}

// ModifierFlags uses bitflags
ModifierFlags::COMMAND  // 256 - Cmd
ModifierFlags::SHIFT    // 512 - Shift  
ModifierFlags::OPTION   // 2048 - Option
ModifierFlags::CONTROL  // 4096 - Control
```

## Error Handling

### MenuExecutorError Variants

| Error | Cause | Solution |
|-------|-------|----------|
| `AccessibilityPermissionDenied` | No AX permission | System Preferences > Privacy > Accessibility |
| `AppNotFrontmost` | Target app not active | Activate app before executing |
| `MenuItemNotFound` | Path doesn't exist | Rescan menu, path may have changed |
| `MenuItemDisabled` | Item is grayed out | Check enabled state before executing |
| `MenuStructureChanged` | Menu differs from cache | Invalidate cache, rescan |

## Prerequisites

1. **Accessibility Permission** - Required in System Preferences > Privacy & Security > Accessibility
2. **Target App Active** - For execution, target must be frontmost (not just menu bar owner)
3. **SQLite** - For caching (rusqlite crate)
