---
name: gpui-testing
description: Testing patterns for GPUI applications
tags: [rust, gpui, testing, unit-tests]
---

# gpui-testing

Comprehensive guide to testing GPUI applications based on patterns from script-kit-gpui.

## Overview

GPUI applications require specific testing patterns because they deal with:
- **UI state management** - Views, components, state machines
- **Async operations** - Background tasks, channels, spawn
- **Platform integration** - Hotkeys, system calls, OS-specific behavior
- **Serialization** - Config files, theme parsing, protocol messages

## Test File Organization

### Convention: `*_tests.rs` Files

Tests are organized in separate `*_tests.rs` files alongside their implementation:

```
src/
  theme/
    mod.rs           # Theme types and logic
    theme_tests.rs   # Theme tests
  config/
    mod.rs           # Config types
    config_tests.rs  # Config tests
  components/
    unified_list_item.rs
    unified_list_item_tests.rs
```

Import tests in the module:
```rust
// In mod.rs
#[cfg(test)]
mod theme_tests;
```

### Inline Test Modules

For smaller modules, use inline test modules:
```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_something() {
        // ...
    }
}
```

## Test Setup Patterns

### Helper Functions

Create helpers to reduce test boilerplate:

```rust
/// Helper to create a test Scriptlet with minimal required fields
fn test_scriptlet(name: &str, tool: &str, code: &str) -> Scriptlet {
    Scriptlet {
        name: name.to_string(),
        description: None,
        code: code.to_string(),
        tool: tool.to_string(),
        shortcut: None,
        expand: None,
        group: None,
        file_path: None,
        command: None,
        alias: None,
    }
}

/// Helper to wrap Vec<Script> into Vec<Arc<Script>> for tests
fn wrap_scripts(scripts: Vec<Script>) -> Vec<Arc<Script>> {
    scripts.into_iter().map(Arc::new).collect()
}

/// Helper to create a shortcut with modifiers
fn make_shortcut(key: &str, cmd: bool, shift: bool) -> Shortcut {
    Shortcut {
        key: key.to_string(),
        modifiers: Modifiers {
            cmd,
            shift,
            ..Default::default()
        },
    }
}
```

### Test Fixtures

For complex types, create fixture factories:

```rust
fn create_test_config() -> Config {
    Config {
        hotkey: HotkeyConfig {
            modifiers: vec!["meta".to_string()],
            key: "Semicolon".to_string(),
        },
        bun_path: None,
        editor: None,
        padding: None,
        // ... other fields with defaults
    }
}
```

## Testing Pure Logic (No GPUI Context)

### Default Values

```rust
#[test]
fn test_default_config() {
    let config = Config::default();
    assert_eq!(config.hotkey.modifiers, vec!["meta"]);
    assert_eq!(config.hotkey.key, "Semicolon");
    assert_eq!(config.bun_path, None);
}
```

### Serialization Roundtrip

```rust
#[test]
fn test_config_serialization() {
    let config = Config { /* ... */ };
    let json = serde_json::to_string(&config).unwrap();
    let deserialized: Config = serde_json::from_str(&json).unwrap();
    assert_eq!(deserialized.hotkey.key, config.hotkey.key);
}
```

### JSON Deserialization Edge Cases

```rust
#[test]
fn test_config_deserialization_minimal() {
    let json = r#"{
        "hotkey": {
            "modifiers": ["meta"],
            "key": "Semicolon"
        }
    }"#;
    let config: Config = serde_json::from_str(json).unwrap();
    assert_eq!(config.bun_path, None);  // Missing fields default
}

#[test]
fn test_hex_color_parse_multiple_formats() {
    assert_eq!(parse_color_string("#FBBF24").unwrap(), 0xFBBF24);
    assert_eq!(parse_color_string("0xFBBF24").unwrap(), 0xFBBF24);
    assert_eq!(parse_color_string("rgb(251, 191, 36)").unwrap(), 0xFBBF24);
}
```

## Testing State Machines

### Registry Pattern

```rust
#[test]
fn register_and_get() {
    let mut registry = ShortcutRegistry::new();
    let binding = ShortcutBinding::builtin(
        "test.action",
        "Test Action",
        make_shortcut("k", true, false),
        ShortcutContext::Global,
        ShortcutCategory::Actions,
    );
    registry.register(binding);

    let retrieved = registry.get("test.action").unwrap();
    assert_eq!(retrieved.name, "Test Action");
}

#[test]
fn user_override_takes_precedence() {
    let mut registry = ShortcutRegistry::new();
    registry.register(/* ... */);
    
    let shortcut = registry.get_shortcut("test.action").unwrap();
    assert_eq!(shortcut.key, "k");  // Default
    
    registry.set_override("test.action", Some(make_shortcut("j", true, true)));
    
    let shortcut = registry.get_shortcut("test.action").unwrap();
    assert_eq!(shortcut.key, "j");  // Overridden
}
```

### Channel Testing

```rust
#[test]
fn hotkey_channels_are_independent() {
    // Clear channels
    while hotkey_channel().1.try_recv().is_ok() {}
    while script_hotkey_channel().1.try_recv().is_ok() {}

    // Send to one channel
    hotkey_channel().0.send_blocking(()).expect("send hotkey");
    
    // Verify other channel is empty
    assert!(matches!(
        script_hotkey_channel().1.try_recv(),
        Err(TryRecvError::Empty)
    ));
    
    // Verify original channel has message
    assert!(hotkey_channel().1.try_recv().is_ok());
}
```

## Testing Components

### Type Verification

```rust
#[test]
fn test_list_item_colors_is_copy() {
    // Compile-time verification that type implements Copy
    fn assert_copy<T: Copy>() {}
    assert_copy::<ListItemColors>();
}
```

### Layout Calculations

```rust
#[test]
fn test_density_comfortable_layout() {
    let layout = ListItemLayout::from_density(Density::Comfortable);
    assert_eq!(layout.height, 48.0);
    assert!(layout.padding_x >= 12.0);
}

#[test]
fn test_layout_height_is_fixed() {
    let comfortable = ListItemLayout::from_density(Density::Comfortable);
    let compact = ListItemLayout::from_density(Density::Compact);
    
    assert!(comfortable.height > 0.0);
    assert!(compact.height > 0.0);
    assert!(comfortable.height > compact.height);
}
```

### UTF-8 Safety

```rust
#[test]
fn test_split_by_ranges_emoji_safe() {
    // "a[emoji]b" - emoji is 4 bytes
    let text = "a\u{1F600}b";
    let ranges = vec![1..5];  // The emoji bytes
    
    let spans = split_by_ranges(text, &ranges);
    assert_eq!(spans[0], ("a", false));
    assert_eq!(spans[1], ("\u{1F600}", true));
    assert_eq!(spans[2], ("b", false));
}

#[test]
fn test_split_by_ranges_japanese() {
    // Each Japanese char is 3 bytes
    let text = "\u{65E5}\u{672C}\u{8A9E}";  // "nihongo"
    let ranges = vec![3..6];  // Middle character
    
    let spans = split_by_ranges(text, &ranges);
    assert_eq!(spans[1].0.chars().next().unwrap(), '\u{672C}');
}
```

## System Tests with Feature Flags

Use `#[cfg(feature = "system-tests")]` for tests that:
- Require OS permissions (accessibility, hotkeys)
- Open real windows/applications
- Interact with system services

```rust
#[cfg(feature = "system-tests")]
#[test]
fn test_handle_get_selected_text_returns_handled() {
    let msg = Message::get_selected_text("req-001".to_string());
    let result = handle_selected_text_message(&msg);
    // ...
}

// This test actually opens Finder
#[cfg(all(unix, feature = "system-tests"))]
#[test]
fn test_run_scriptlet_open() {
    let scriptlet = Scriptlet::new(
        "Open Test".to_string(),
        "open".to_string(),
        "/tmp".to_string(),
    );
    let result = run_scriptlet(&scriptlet, ScriptletExecOptions::default());
    assert!(result.is_ok());
}
```

Run system tests with:
```bash
cargo test --features system-tests
```

## Platform-Specific Tests

```rust
#[cfg(unix)]
#[test]
fn test_spawn_and_kill_process() {
    let result = spawn_script("sleep", &["10"], "[test:sleep]");
    if let Ok(mut session) = result {
        assert!(session.is_running());
        session.kill().expect("kill should succeed");
        std::thread::sleep(std::time::Duration::from_millis(100));
        assert!(!session.is_running());
    }
}

#[cfg(target_os = "macos")]
#[test]
fn test_find_conflicts_detects_os_reserved() {
    let mut registry = ShortcutRegistry::new();
    // Cmd+Tab is OS reserved on macOS
    registry.register(ShortcutBinding::builtin(
        "app.switcher",
        "App Switcher",
        make_shortcut("tab", true, false),
        ShortcutContext::Global,
        ShortcutCategory::System,
    ));
    
    let conflicts = registry.find_conflicts();
    assert!(conflicts.iter().any(|c| 
        c.conflict_type == ConflictType::Unreachable
    ));
}
```

## Environment Variable Testing

Handle env var tests carefully (they're global):

```rust
#[test]
fn test_get_editor_from_env() {
    // Save current value
    let original_editor = std::env::var("EDITOR").ok();
    
    // Test with custom value
    std::env::set_var("EDITOR", "emacs");
    let config = Config::default();
    assert_eq!(config.get_editor(), "emacs");
    
    // Restore original value
    match original_editor {
        Some(val) => std::env::set_var("EDITOR", val),
        None => std::env::remove_var("EDITOR"),
    }
}
```

For parallel-safe env testing, test all cases sequentially in one test:

```rust
#[test]
fn test_is_auto_submit_enabled_all_cases() {
    std::env::set_var("AUTO_SUBMIT", "true");
    assert!(is_auto_submit_enabled());
    
    std::env::set_var("AUTO_SUBMIT", "1");
    assert!(is_auto_submit_enabled());
    
    std::env::set_var("AUTO_SUBMIT", "false");
    assert!(!is_auto_submit_enabled());
    
    std::env::remove_var("AUTO_SUBMIT");
    assert!(!is_auto_submit_enabled());
}
```

## Code Audit Tests

Test invariants about the codebase itself:

```rust
#[test]
fn test_no_direct_cx_hide_in_app_execute() {
    let content = fs::read_to_string("src/app_execute.rs")
        .unwrap_or_default();
    let matches = find_lines_with_pattern(&content, "cx.hide()");
    
    assert!(
        matches.is_empty(),
        "Found forbidden cx.hide() in app_execute.rs. Use self.close_and_reset_window(cx) instead."
    );
}

#[test]
fn test_close_and_reset_window_exists() {
    let content = fs::read_to_string("src/app_impl.rs")
        .unwrap_or_default();
    let count = content.matches("fn close_and_reset_window").count();
    
    assert!(count >= 1, "close_and_reset_window() not found");
}
```

## Testing GPUI Keystroke Matching

```rust
#[test]
fn find_match_respects_context_order() {
    let mut registry = ShortcutRegistry::new();
    registry.register(ShortcutBinding::builtin(
        "editor.enter",
        "Editor Enter",
        make_shortcut("enter", false, false),
        ShortcutContext::Editor,
        ShortcutCategory::Actions,
    ));
    registry.register(ShortcutBinding::builtin(
        "global.enter",
        "Global Enter",
        make_shortcut("enter", false, false),
        ShortcutContext::Global,
        ShortcutCategory::Actions,
    ));

    let keystroke = gpui::Keystroke {
        key: "enter".to_string(),
        key_char: None,
        modifiers: gpui::Modifiers::default(),
    };

    // Editor context first - should match editor binding
    let contexts = [ShortcutContext::Editor, ShortcutContext::Global];
    assert_eq!(
        registry.find_match(&keystroke, &contexts),
        Some("editor.enter")
    );
}
```

## Testing with GlobalHotKeyManager

System hotkey tests may fail in CI (no event loop):

```rust
mod script_hotkey_manager_tests {
    fn create_test_manager() -> Option<ScriptHotkeyManager> {
        // May fail in test environment
        GlobalHotKeyManager::new()
            .ok()
            .map(ScriptHotkeyManager::new)
    }

    #[test]
    fn test_manager_creation() {
        if let Some(manager) = create_test_manager() {
            assert!(manager.hotkey_map.is_empty());
        }
        // If creation failed, test passes (expected in CI)
    }

    #[test]
    fn test_register_tracks_mapping() {
        if let Some(mut manager) = create_test_manager() {
            let result = manager.register("/test/script.ts", "cmd+shift+t");
            if result.is_ok() {
                assert!(manager.is_registered("/test/script.ts"));
            }
            // Registration may fail without event loop - that's OK
        }
    }
}
```

## Anti-patterns

### DON'T: Use `cx.run()` in Unit Tests
GPUI context methods require a running app. Unit tests should test pure logic.

### DON'T: Rely on Global State
```rust
// BAD - tests may interfere with each other
static mut COUNTER: i32 = 0;

#[test]
fn test_increment() {
    unsafe { COUNTER += 1; }
    // ...
}
```

### DON'T: Hardcode Paths
```rust
// BAD
let path = "/Users/john/.scriptkit/scripts/test.ts";

// GOOD - use temp dirs
let temp_dir = tempfile::tempdir().unwrap();
let path = temp_dir.path().join("test.ts");
```

### DON'T: Forget Platform Guards
```rust
// BAD - will fail on Windows
#[test]
fn test_unix_signals() {
    use libc::kill;
    // ...
}

// GOOD
#[cfg(unix)]
#[test]
fn test_unix_signals() {
    use libc::kill;
    // ...
}
```

### DON'T: Skip Cleanup
```rust
// BAD
#[test]
fn test_with_env() {
    std::env::set_var("MY_VAR", "value");
    // Test crashes - env var leaked
}

// GOOD
#[test]
fn test_with_env() {
    let original = std::env::var("MY_VAR").ok();
    std::env::set_var("MY_VAR", "value");
    
    // ... test code ...
    
    // Always cleanup
    match original {
        Some(v) => std::env::set_var("MY_VAR", v),
        None => std::env::remove_var("MY_VAR"),
    }
}
```

## Running Tests

```bash
# Run all tests
cargo test

# Run tests for a specific module
cargo test theme_tests

# Run tests with system features
cargo test --features system-tests

# Run tests with output
cargo test -- --nocapture

# Run a single test
cargo test test_default_config
```
