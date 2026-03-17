---
name: script-kit-actions-window
description: Actions window/dialog system for Script Kit GPUI. A Raycast-style searchable action menu supporting script context actions, file actions, path actions, and SDK-provided custom actions. Use when working with ActionsDialog, ActionsWindow, action builders, or the actions panel UI.
tags:
  - gpui
  - actions
  - dialog
  - popup
  - menu
  - vibrancy
---

# Script Kit Actions Window

Actions window/dialog system for Script Kit GPUI. A Raycast-style searchable action menu 
supporting script context actions, file actions, path actions, and SDK-provided custom actions.

**Use when:**
- Building or modifying the actions popup UI
- Adding new action types or categories
- Working with keyboard shortcut hints/keycaps
- Integrating SDK-provided custom actions
- Positioning/resizing the floating actions window

## Architecture Overview

```
src/actions/
├── mod.rs          # Public API re-exports
├── types.rs        # Action, ActionCategory, ScriptInfo, ActionCallback
├── builders.rs     # Factory functions: get_script_context_actions(), etc.
├── constants.rs    # Layout constants: POPUP_WIDTH, ACTION_ITEM_HEIGHT, etc.
├── dialog.rs       # ActionsDialog struct + rendering logic
└── window.rs       # Separate vibrancy window management
```

### Key Types

```rust
// src/actions/types.rs

/// Information about the currently focused script/item
pub struct ScriptInfo {
    pub name: String,           // Display name
    pub path: String,           // Full path (empty for built-ins)
    pub is_script: bool,        // false for built-ins like "Clipboard History"
    pub action_verb: String,    // "Run", "Launch", "Switch to"
    pub shortcut: Option<String>, // Current assigned shortcut
}

/// An action in the menu
pub struct Action {
    pub id: String,              // Unique identifier (e.g., "edit_script")
    pub title: String,           // Display text
    pub description: Option<String>,
    pub category: ActionCategory,
    pub shortcut: Option<String>, // Keyboard hint (e.g., "⌘E")
    pub has_action: bool,        // SDK routing: true = ActionTriggered, false = submit value
    pub value: Option<String>,   // Value to submit when triggered
}

pub enum ActionCategory {
    ScriptContext,  // Actions for the focused script/file
    ScriptOps,      // Edit, Create, Delete (reserved)
    GlobalOps,      // Settings, Quit (now in main menu)
}

/// Callback signature for action selection
pub type ActionCallback = Arc<dyn Fn(String) + Send + Sync>;
```

### ActionsDialog Entity

```rust
// src/actions/dialog.rs

pub struct ActionsDialog {
    pub actions: Vec<Action>,
    pub filtered_actions: Vec<usize>,  // Indices into actions (after search filter)
    pub selected_index: usize,         // Index within filtered_actions
    pub search_text: String,
    pub focus_handle: FocusHandle,
    pub on_select: ActionCallback,
    pub focused_script: Option<ScriptInfo>,
    pub scroll_handle: UniformListScrollHandle,
    pub theme: Arc<Theme>,
    pub design_variant: DesignVariant,
    pub cursor_visible: bool,          // For blinking cursor
    pub hide_search: bool,             // True when embedded in header
    pub sdk_actions: Option<Vec<ProtocolAction>>,  // SDK-provided actions
    pub context_title: Option<String>, // Header title
}
```

## Creating ActionsDialog

### For Scripts (main use case)

```rust
use crate::actions::{ActionsDialog, ScriptInfo};

// Basic - no script context
let dialog = ActionsDialog::new(focus_handle, on_select_callback, theme);

// With script context - shows script-specific actions
let script_info = ScriptInfo::new("my-script", "/path/to/my-script.ts");
let dialog = ActionsDialog::with_script(focus_handle, callback, Some(script_info), theme);

// With shortcut info (affects which shortcut actions show)
let script_info = ScriptInfo::with_shortcut(
    "my-script",
    "/path/to/script.ts", 
    Some("cmd+shift+m".to_string())  // Has shortcut → shows Update/Remove
);

// For built-in commands (limited actions - no edit, reveal, copy path)
let builtin = ScriptInfo::builtin("Clipboard History");
let dialog = ActionsDialog::with_script(focus_handle, callback, Some(builtin), theme);
```

### For File Search Results

```rust
use crate::actions::ActionsDialog;
use crate::file_search::FileInfo;

let file_info = FileInfo {
    path: "/Users/test/document.pdf".to_string(),
    name: "document.pdf".to_string(),
    file_type: FileType::Document,
    is_dir: false,
};

let dialog = ActionsDialog::with_file(focus_handle, callback, &file_info, theme);
// Actions: Open, Show in Finder, Quick Look, Open With..., Get Info, Copy Path
```

### For Path Prompt

```rust
use crate::actions::ActionsDialog;
use crate::prompts::PathInfo;

let path_info = PathInfo {
    path: "/Users/test/folder".to_string(),
    name: "folder".to_string(),
    is_dir: true,
};

let dialog = ActionsDialog::with_path(focus_handle, callback, &path_info, theme);
// Actions: Open, Copy Path, Open in Finder, Open in Editor, Open in Terminal, etc.
```

## Window Management

The actions dialog can render in two modes:
1. **Inline overlay** (legacy) - rendered within main window
2. **Separate vibrancy window** (preferred) - floating popup with blur

### Opening the Floating Window

```rust
use crate::actions::{open_actions_window, close_actions_window, is_actions_window_open};

// Create dialog entity first
let dialog_entity = cx.new(|cx| ActionsDialog::with_script(...));

// Get main window bounds (SCREEN-RELATIVE coordinates)
let main_bounds = window.bounds();
let display_id = window.display().map(|d| d.id());

// Open floating window - positions at bottom-right of main window
match open_actions_window(cx, main_bounds, display_id, dialog_entity) {
    Ok(handle) => { /* window opened */ }
    Err(e) => { /* handle error */ }
}

// Check if open
if is_actions_window_open() { ... }

// Close window
close_actions_window(cx);
```

### Resizing After Filter Changes

```rust
use crate::actions::resize_actions_window;

// After search text changes and filtered_actions.len() changes:
resize_actions_window(cx, &dialog_entity);
// Window stays "pinned to bottom" - bottom edge stays fixed, top moves
```

### Notifying for Re-render

```rust
use crate::actions::notify_actions_window;

// After updating dialog entity state:
dialog_entity.update(cx, |dialog, cx| {
    dialog.set_cursor_visible(!dialog.cursor_visible);
    cx.notify();
});
notify_actions_window(cx);  // Also notify the window
```

## Action Builders

Factory functions that create action lists for different contexts:

```rust
// src/actions/builders.rs

/// Script context actions (most common)
/// Actions vary based on is_script and shortcut presence
pub fn get_script_context_actions(script: &ScriptInfo) -> Vec<Action>;
// Returns: Run, Add/Update/Remove Shortcut, Edit, View Logs, Reveal, Copy Path, Copy Deeplink

/// File search result actions
pub fn get_file_context_actions(file_info: &FileInfo) -> Vec<Action>;
// Returns: Open, Show in Finder, Quick Look, Open With, Get Info, Copy Path/Filename

/// Path prompt actions
pub fn get_path_context_actions(path_info: &PathInfo) -> Vec<Action>;
// Returns: Open/Select, Copy Path, Open in Finder/Editor/Terminal, Copy Filename, Move to Trash

/// Global actions (currently empty - Settings/Quit in main menu)
pub fn get_global_actions() -> Vec<Action>;
```

## SDK Actions Integration

Scripts can provide custom actions via the SDK:

```rust
// Set SDK actions (replaces built-in actions)
dialog.set_sdk_actions(vec![
    ProtocolAction {
        name: "Custom Action".to_string(),
        description: Some("Does something custom".to_string()),
        shortcut: Some("cmd+k".to_string()),
        value: Some("custom-value".to_string()),
        has_action: true,  // true = send ActionTriggered to SDK
        visible: None,     // None or Some(true) = visible
        close: None,       // Whether to close dialog after action
    },
]);

// Check if SDK actions are active
if dialog.has_sdk_actions() { ... }

// Clear SDK actions (restores built-in)
dialog.clear_sdk_actions();
```

### Action Routing Logic

```rust
// In action handler:
if action.has_action {
    // Send ActionTriggered event to SDK
    send_to_sdk(ActionTriggered { name: action.id, value: action.value });
} else {
    // Submit value directly (like selecting a choice)
    submit_value(action.value.unwrap_or(action.id));
}
```

## Layout Constants

```rust
// src/actions/constants.rs

pub const POPUP_WIDTH: f32 = 320.0;
pub const POPUP_MAX_HEIGHT: f32 = 400.0;
pub const ACTION_ITEM_HEIGHT: f32 = 44.0;  // iOS-style touch target
pub const SEARCH_INPUT_HEIGHT: f32 = 44.0;
pub const HEADER_HEIGHT: f32 = 44.0;
pub const ACTION_ROW_INSET: f32 = 6.0;     // Pill-style row padding
pub const SELECTION_RADIUS: f32 = 8.0;     // Selected row corner radius
pub const KEYCAP_MIN_WIDTH: f32 = 22.0;
pub const KEYCAP_HEIGHT: f32 = 22.0;
pub const ACCENT_BAR_WIDTH: f32 = 3.0;     // Legacy, kept for reference
```

## Keyboard Shortcut Formatting

```rust
// Convert SDK shortcut format to display symbols
ActionsDialog::format_shortcut_hint("cmd+shift+e") // → "⌘⇧E"
ActionsDialog::format_shortcut_hint("ctrl+c")      // → "⌃C"
ActionsDialog::format_shortcut_hint("enter")       // → "↵"

// Parse shortcut into individual keycaps for rendering
ActionsDialog::parse_shortcut_keycaps("⌘⇧E") // → vec!["⌘", "⇧", "E"]
```

### Symbol Mappings

| Input | Symbol |
|-------|--------|
| `cmd`, `command`, `meta` | ⌘ |
| `ctrl`, `control` | ⌃ |
| `alt`, `opt`, `option` | ⌥ |
| `shift` | ⇧ |
| `enter`, `return` | ↵ |
| `escape`, `esc` | ⎋ |
| `tab` | ⇥ |
| `backspace`, `delete` | ⌫ |
| `space` | ␣ |
| `up`, `arrowup` | ↑ |
| `down`, `arrowdown` | ↓ |
| `left`, `arrowleft` | ← |
| `right`, `arrowright` | → |

## Search/Filter Behavior

The dialog implements ranked fuzzy matching:

```rust
// Scoring system (higher = better match):
// - Prefix match on title: +100
// - Contains match on title: +50  
// - Fuzzy subsequence match on title: +25
// - Contains match on description: +15

dialog.refilter();  // Called automatically when search_text changes
```

## ActionsDialogHost Enum

Tracks where the actions dialog was opened from (for proper close handling):

```rust
// src/main.rs
enum ActionsDialogHost {
    MainList,      // Main script list
    ArgPrompt,     // Arg prompt
    DivPrompt,     // Div prompt
    EditorPrompt,  // Editor prompt
    TermPrompt,    // Terminal prompt
    FormPrompt,    // Form prompt
    FileSearch,    // File search results
}
```

## Rendering Pattern

```rust
impl Render for ActionsDialog {
    fn render(&mut self, window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        let colors = get_tokens(self.design_variant).colors;
        
        div()
            .w(px(POPUP_WIDTH))
            .flex()
            .flex_col()
            .bg(rgb(colors.background))
            .rounded(px(SELECTION_RADIUS))
            .shadow(/* vibrancy-compatible shadow */)
            // Optional header with context title
            .when_some(self.context_title.clone(), |el, title| {
                el.child(self.render_header(&title, &colors))
            })
            // Search input (unless hide_search)
            .when(!self.hide_search, |el| {
                el.child(self.render_search_input(&colors))
            })
            // Virtualized action list
            .child(
                uniform_list("actions-list", self.filtered_actions.len(), |this, range, _, _| {
                    this.render_action_items(range)
                })
                .track_scroll(&self.scroll_handle)
                .h(px(items_height))
            )
    }
}
```

## Common Patterns

### Opening Actions from a Prompt

```rust
// In render_prompts/arg.rs, div.rs, editor.rs, etc.
fn show_actions_popup(&mut self, host: ActionsDialogHost, window: &mut Window, cx: &mut Context<Self>) {
    let dialog = ActionsDialog::with_script(
        cx.focus_handle(),
        Arc::new(|_| {}),  // Callback handled by main app
        self.get_script_info(),
        self.theme.clone(),
    );
    
    let dialog_entity = cx.new(|_| dialog);
    let main_bounds = window.bounds();
    let display_id = window.display().map(|d| d.id());
    
    open_actions_window(cx, main_bounds, display_id, dialog_entity);
}
```

### Closing on Escape/Click Outside

```rust
// In key handler
"escape" | "Escape" => {
    if is_actions_window_open() {
        close_actions_window(cx);
    }
}

// Click-outside detection (in ActionsDialog render)
.on_mouse_down_out(cx.listener(|this, _, _, cx| {
    logging::log("ACTIONS", "dismiss-on-click-outside triggered");
    // Parent handles actual close via callback
}))
```

## Testing

```rust
#[test]
fn test_get_script_context_actions_no_shortcut() {
    let script = ScriptInfo::new("my-script", "/path/to/script.ts");
    let actions = get_script_context_actions(&script);
    
    assert!(actions.iter().any(|a| a.id == "run_script"));
    assert!(actions.iter().any(|a| a.id == "add_shortcut"));
    assert!(!actions.iter().any(|a| a.id == "update_shortcut"));
}

#[test]
fn test_get_script_context_actions_with_shortcut() {
    let script = ScriptInfo::with_shortcut("my-script", "/path", Some("cmd+m".to_string()));
    let actions = get_script_context_actions(&script);
    
    assert!(!actions.iter().any(|a| a.id == "add_shortcut"));
    assert!(actions.iter().any(|a| a.id == "update_shortcut"));
    assert!(actions.iter().any(|a| a.id == "remove_shortcut"));
}
```

## Related Files

- `src/main.rs` - ActionsDialogHost enum, action routing
- `src/app_impl.rs` - Action handling, theme propagation
- `src/render_script_list.rs` - Opening actions from script list
- `src/render_prompts/*.rs` - Opening actions from prompts
- `src/notes/actions_panel.rs` - Similar pattern for Notes window
- `src/stories/actions_window_stories.rs` - Storybook stories
