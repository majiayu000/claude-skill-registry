---
name: script-kit-app-shell
description: |
  Build and configure the Script Kit App Shell - the unified frame/chrome system for all prompts.
  Use when: (1) Creating new prompt views that need headers, footers, or chrome
  (2) Configuring ShellSpec for layout requirements (3) Working with HeaderSpec, FooterSpec, ChromeSpec
  (4) Managing focus policies (5) Setting up keyboard bindings via KeymapSpec
  (6) Styling the shell frame. Triggers on: "app shell", "shell spec", "header spec", "footer spec",
  "chrome spec", "focus policy", "keymap spec", "shell focus".
---

# Script Kit App Shell

The App Shell is a presentational frame/chrome layer that wraps prompt content with consistent styling, focus management, and keyboard routing.

## Architecture

The shell is a *frame + chrome* layer, not another "app":
- State and lifecycle remain in the window root (e.g., `ScriptListApp`)
- Takes stable focus handles by reference (doesn't own them)
- Never allocates per-render (uses SmallVec, SharedString, action enums)

## Core Types

### ShellSpec - Main Layout Specification

```rust
ShellSpec::new()
    .header(HeaderSpec::search("Type to search..."))
    .footer(FooterSpec::new().primary("Run", "Enter"))
    .content(my_content_element)
    .chrome(ChromeSpec::full_frame())
    .focus_policy(FocusPolicy::HeaderInput)
    .keymap(KeymapSpec::new())
```

| Field | Type | Purpose |
|-------|------|---------|
| `header` | `Option<HeaderSpec>` | Header with input/buttons/logo |
| `footer` | `Option<FooterSpec>` | Footer with actions/info |
| `content` | `Option<AnyElement>` | Main content element |
| `chrome` | `ChromeSpec` | Frame styling (bg, shadow, radius) |
| `focus_policy` | `FocusPolicy` | Where focus lands on activation |
| `keymap` | `KeymapSpec` | Per-view keybindings |

### HeaderSpec - Header Configuration

```rust
// Simple search header
HeaderSpec::search("Type to filter...")

// With buttons
HeaderSpec::search("Search scripts")
    .button("Run", "Enter")
    .secondary_button("Actions", "Cmd+K")

// With path prefix
HeaderSpec::search("Enter name")
    .path_prefix("~/scripts/")
    .ask_ai_hint(true)  // Shows "Ask AI [Tab]"

// Manual input setup
HeaderSpec::new()
    .text("current input value")
    .cursor_visible(true)
    .focused(true)
    .logo(true)
```

| Field | Type | Purpose |
|-------|------|---------|
| `input` | `Option<InputSpec>` | Search input configuration |
| `buttons` | `SmallVec<[ButtonSpec; 4]>` | Action buttons (max ~4) |
| `show_logo` | `bool` | Display Script Kit logo |
| `path_prefix` | `Option<SharedString>` | Path shown before input |
| `show_ask_ai_hint` | `bool` | Show "Ask AI [Tab]" hint |

### InputSpec - Input Field State

```rust
InputSpec {
    placeholder: "Search...".into(),
    text: current_text.clone(),
    cursor_visible: true,  // For blinking animation
    is_focused: true,
}
```

### FooterSpec - Footer Configuration

```rust
FooterSpec::new()
    .primary("Run Script", "Enter")
    .secondary("Actions", "Cmd+K")
    .helper("Tab 1 of 2")
    .info("TypeScript")
    .logo(true)
```

| Field | Type | Purpose |
|-------|------|---------|
| `primary_label` | `SharedString` | Primary action text |
| `primary_shortcut` | `SharedString` | Primary shortcut hint |
| `secondary_label` | `Option<SharedString>` | Secondary action text |
| `secondary_shortcut` | `Option<SharedString>` | Secondary shortcut hint |
| `show_logo` | `bool` | Display Script Kit logo |
| `helper_text` | `Option<SharedString>` | Helper text (left side) |
| `info_label` | `Option<SharedString>` | Info label (right side) |

### ChromeSpec - Frame Styling

```rust
// Full frame (default) - rounded bg, shadow, divider
ChromeSpec::full_frame()

// Minimal - tighter styling, no divider
ChromeSpec::minimal()

// Content only - no background/shadow
ChromeSpec::content_only()

// Custom
ChromeSpec::full_frame()
    .radius(16.0)
    .padding(8.0)
    .divider(DividerSpec::Hairline)
    .opacity(0.85)
```

| Mode | Background | Shadow | Divider | Use Case |
|------|------------|--------|---------|----------|
| `FullFrame` | Yes | Yes | Hairline | ScriptList, ArgPrompt |
| `MinimalFrame` | Yes | Yes | None | HUD, compact prompts |
| `ContentOnly` | No | No | None | Custom-styled overlays |

### ChromeMode Methods

```rust
chrome.mode.shows_divider()   // true for FullFrame only
chrome.mode.has_background()  // true except ContentOnly
chrome.mode.has_shadow()      // true except ContentOnly
chrome.should_show_divider()  // combines mode + DividerSpec
```

### DividerSpec - Header/Content Separator

```rust
DividerSpec::None      // No divider
DividerSpec::Hairline  // 1px line (default)
```

## Focus Management

### FocusPolicy - Where Focus Goes

```rust
FocusPolicy::Preserve     // Don't change focus (overlays, HUD)
FocusPolicy::HeaderInput  // Focus search box (default)
FocusPolicy::Content      // Focus content area (editor, term)
```

### ShellFocus - Stable Focus Handles

Created once per window, stored in root state:

```rust
// In app initialization
let shell_focus = ShellFocus::new(cx);

// Apply policy on view transition (not every render)
shell_focus.apply_policy(spec.focus_policy, window, cx);

// Query focus state
shell_focus.is_header_focused(window)
shell_focus.is_content_focused(window)
shell_focus.is_any_focused(window)

// Manual focus control
shell_focus.focus_header(window, cx);
shell_focus.focus_content(window, cx);

// For track_focus
shell_focus.root_handle()
```

## Keyboard Routing

### ShellAction - Action Enum

```rust
ShellAction::Cancel      // Escape - cancel/close/back
ShellAction::Run         // Enter - run/submit/select
ShellAction::OpenActions // Cmd+K - actions dialog
ShellAction::FocusSearch // Focus search input
ShellAction::Next        // Down arrow - next item
ShellAction::Prev        // Up arrow - previous item
ShellAction::Tab         // Tab - next field/AI hint
ShellAction::ShiftTab    // Shift+Tab - previous field
ShellAction::Close       // Cmd+W - close window
ShellAction::Settings    // Cmd+, - open settings
ShellAction::None        // No action (key not handled)
```

### KeymapSpec - Per-View Bindings

```rust
// Add custom bindings
KeymapSpec::new()
    .bind("p", ShellAction::Prev)
    .bind("n", ShellAction::Next)

// With modifiers
KeymapSpec::new()
    .bind_with_modifiers("s", Modifiers::command(), ShellAction::Run)

// Modal (blocks global shortcuts)
KeymapSpec::modal()
    .bind("escape", ShellAction::Cancel)
```

### Default Bindings

| Key | Modifiers | Action |
|-----|-----------|--------|
| `escape` | - | Cancel |
| `enter` | - | Run |
| `k` | Cmd | OpenActions |
| `w` | Cmd | Close |
| `,` | Cmd | Settings |
| `tab` | - | Tab |
| `tab` | Shift | ShiftTab |
| `up` | - | Prev |
| `down` | - | Next |

### Routing Priority

1. View-specific KeymapSpec bindings
2. Default shell bindings (unless `modal: true`)

```rust
// Route a key event
let action = route_key(key, &modifiers, &view_keymap);
if action.is_handled() {
    // Process action
}
```

## Button System

### ButtonSpec

```rust
ButtonSpec::primary("Run", "Enter")   // Primary style
ButtonSpec::secondary("More", "...")  // Ghost style

// Custom action
ButtonSpec::primary("Submit", "Cmd+S")
    .action(ButtonAction::Custom(42))
    .variant(ButtonVariant::Icon)
```

### ButtonAction

```rust
ButtonAction::Submit       // Default primary action
ButtonAction::OpenActions  // Open actions dialog
ButtonAction::TogglePreview
ButtonAction::Cancel
ButtonAction::Custom(u32)  // Custom action by ID
```

### ButtonVariant

```rust
ButtonVariant::Primary  // Solid accent color
ButtonVariant::Ghost    // Text only
ButtonVariant::Icon     // Icon button
```

## Style Caching

### ShellStyleCache

Pre-computed styles to avoid per-render computation:

```rust
// Create from theme
let style_cache = ShellStyleCache::from_theme(&theme, revision);

// Check/update cache
if !style_cache.is_valid(new_revision) {
    style_cache.update_if_needed(&theme, new_revision);
}
```

Contains:
- `frame_bg`: Hsla with vibrancy opacity (70-85%)
- `shadows`: Vec<BoxShadow>
- `radius`: Pixels
- `header`: HeaderColors
- `footer`: FooterColors  
- `divider`: DividerColors

## Rendering

### AppShell::render

```rust
impl ScriptListApp {
    fn render_shell(&self, window: &mut Window, cx: &mut App) -> AnyElement {
        let spec = self.build_shell_spec(cx);
        let runtime = ShellRuntime {
            focus: &self.shell_focus,
            style: &self.style_cache,
            cursor_visible: self.cursor_visible,
        };
        AppShell::render(spec, &runtime, window, cx)
    }
}
```

## Common Patterns

### Script List View

```rust
ShellSpec::new()
    .header(
        HeaderSpec::search("Type to search...")
            .text(&self.search_text)
            .button("Run", "Enter")
            .secondary_button("Actions", "Cmd+K")
            .ask_ai_hint(true)
    )
    .footer(
        FooterSpec::new()
            .primary("Run Script", "Enter")
            .secondary("Actions", "Cmd+K")
            .helper(format!("{} scripts", self.scripts.len()))
    )
    .content(self.render_script_list(cx))
    .chrome(ChromeSpec::full_frame())
    .focus_policy(FocusPolicy::HeaderInput)
```

### Arg Prompt

```rust
ShellSpec::new()
    .header(
        HeaderSpec::search(&self.prompt.placeholder)
            .text(&self.input)
            .path_prefix(self.prompt.path.as_deref())
    )
    .footer(
        FooterSpec::new()
            .primary("Submit", "Enter")
            .info(&self.prompt.hint)
    )
    .content(self.render_choices(cx))
    .chrome(ChromeSpec::full_frame())
    .focus_policy(FocusPolicy::HeaderInput)
```

### HUD Notification

```rust
ShellSpec::new()
    .content(self.render_hud_content(cx))
    .chrome(ChromeSpec::minimal())
    .focus_policy(FocusPolicy::Preserve)
    .keymap(KeymapSpec::modal())
```

### Editor Prompt

```rust
ShellSpec::new()
    .header(HeaderSpec::new().logo(true))
    .footer(
        FooterSpec::new()
            .primary("Save", "Cmd+S")
            .info("TypeScript")
    )
    .content(self.render_editor(cx))
    .chrome(ChromeSpec::full_frame())
    .focus_policy(FocusPolicy::Content)
```

## File Structure

```
src/app_shell/
  mod.rs    - Module exports and re-exports
  shell.rs  - AppShell renderer (main entry point)
  spec.rs   - ShellSpec, HeaderSpec, FooterSpec, InputSpec, ButtonSpec
  chrome.rs - ChromeMode, ChromeSpec, DividerSpec
  focus.rs  - FocusPolicy, ShellFocus
  keymap.rs - KeymapSpec, ShellAction, route_key(), default_bindings()
  style.rs  - ShellStyleCache, HeaderColors, FooterColors, DividerColors
  tests.rs  - Unit tests
```

## Module Exports

```rust
pub use chrome::{ChromeMode, ChromeSpec, DividerSpec};
pub use focus::{FocusPolicy, ShellFocus};
pub use keymap::{KeymapSpec, ShellAction};
pub use shell::AppShell;
pub use spec::{ButtonSpec, FooterSpec, HeaderSpec, InputSpec, ShellSpec};
pub use style::ShellStyleCache;
```
