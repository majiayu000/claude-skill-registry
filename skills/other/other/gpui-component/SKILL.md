---
name: gpui-component
description: Community UI component library for GPUI applications
triggers:
  - gpui_component
  - gpui-component
  - Input
  - InputState
  - InputEvent
  - Button
  - Root
  - notification
  - IconName
---

# gpui-component

A comprehensive UI component library for building desktop applications with GPUI. Provides 60+ cross-platform components inspired by macOS/Windows controls and shadcn/ui design.

**Repository**: https://github.com/longbridge/gpui-component
**Fork (script-kit-gpui)**: https://github.com/johnlindquist/gpui-component
**Docs**: https://gpui-component.longbridge.xyz/

## Installation

```toml
# In Cargo.toml - using the fork for set_selection() support
gpui-component = { git = "https://github.com/johnlindquist/gpui-component", package = "gpui-component" }

# Required for i18n support
rust-i18n = "3"
```

## Initialization (REQUIRED)

```rust
use gpui_component::Root;

fn main() {
    let app = Application::new();
    app.run(move |cx| {
        // MUST be called before using any gpui-component features
        gpui_component::init(cx);
        
        // Open windows wrapped in Root...
    });
}
```

## Available Components

### Core UI
- **Button** - Primary, secondary, ghost, link variants with icons
- **Input** - Text input with validation, masks, placeholders
- **Checkbox** - Checkable controls
- **Radio** - Radio button groups
- **Switch** - Toggle switches
- **Select** - Dropdown selection
- **Slider** - Range selection

### Layout
- **Root** - Theme/context provider wrapper (REQUIRED for all windows)
- **Dock** - Panel arrangements with resizing
- **Accordion** - Collapsible content sections
- **Collapsible** - Show/hide content
- **Divider** - Visual separators
- **GroupBox** - Grouped content with border

### Feedback
- **Notification** - Toast notifications (Success, Warning, Error, Info)
- **Alert** - Alert dialogs
- **Dialog** - Modal dialogs
- **Sheet** - Slide-in panels
- **Progress** - Progress indicators
- **Spinner** - Loading spinners
- **Skeleton** - Loading placeholders

### Data Display
- **Table** - Virtualized tables (supports 200K+ rows)
- **List** - Virtualized lists
- **Tree** - Tree views
- **Badge** - Status badges
- **Tag** - Categorization tags
- **Avatar** - User avatars
- **Rating** - Star ratings

### Navigation
- **Menu** - Context menus, dropdowns
- **Breadcrumb** - Navigation breadcrumbs
- **Tab** - Tab navigation
- **Sidebar** - Side navigation
- **Pagination** - Page navigation

### Content
- **Icon** - Lucide icons (700+ icons)
- **Label** - Text labels
- **Link** - Hyperlinks
- **Kbd** - Keyboard shortcuts display
- **Text** - Markdown/HTML rendering
- **Chart** - Data visualization

### Advanced
- **ColorPicker** - Color selection
- **DatePicker** - Date/time selection
- **Popover** - Floating content
- **Tooltip** - Hover tooltips
- **Resizable** - Resizable panels

## Usage in script-kit-gpui

### Root Wrapper Pattern
All windows MUST be wrapped in `Root` for theming and context:

```rust
use gpui_component::Root;

// Opening a window
let window: WindowHandle<Root> = cx.open_window(
    WindowOptions { ... },
    |window, cx| {
        let view = cx.new(|cx| MyApp::new(cx));
        cx.new(|cx| Root::new(view, window, cx))
    },
)?;
```

### Input Component
The most commonly used component for text input:

```rust
use gpui_component::input::{Input, InputEvent, InputState};

// Create InputState
let input_state = cx.new(|cx| 
    InputState::new(window, cx)
        .placeholder("Enter text...")
);

// Subscribe to events
cx.subscribe_in(&input_state, window, |this, _, event: &InputEvent, window, cx| {
    match event {
        InputEvent::Focus => { /* input focused */ }
        InputEvent::Blur => { /* input blurred */ }
        InputEvent::Change => { 
            let value = this.input_state.read(cx).value();
        }
        InputEvent::PressEnter { secondary } => { /* enter pressed */ }
    }
});

// Render
Input::new(input_state.clone())
    .size(Size::Medium)
    .cleanable()  // show clear button
```

### Code Editor Mode
For multi-line code editing:

```rust
let editor_state = cx.new(|cx| 
    InputState::new(window, cx)
        .code_editor(true)
        .soft_wrap(true)
        .show_line_numbers(true)
);
```

### Notifications
Toast-style notifications:

```rust
use gpui_component::notification::{Notification, NotificationType};

let notification = Notification::new()
    .title("Success!")
    .description("Operation completed")
    .notification_type(NotificationType::Success);

// NotificationList handles display automatically when using Root
```

### Button Component
```rust
use gpui_component::button::{Button, ButtonVariants};

Button::new("submit")
    .primary()
    .label("Submit")
    .icon(IconName::Check)
    .on_click(|_, window, cx| {
        // handle click
    })
```

### Icons
Uses Lucide icon set:

```rust
use gpui_component::{Icon, IconName, IconNamed};

// As element
Icon::new(IconName::Search)
    .size(px(16.))
    .color(theme.foreground)

// In buttons
Button::new("search").icon(IconName::Search)
```

### Theming Integration
Script-kit-gpui maps its theme to gpui-component's ThemeColor:

```rust
use gpui_component::theme::{Theme as GpuiTheme, ThemeColor, ThemeMode, ActiveTheme};

// Get current theme
let theme = cx.theme();
let colors = &theme.colors;

// Map custom colors
let mut theme_color = *ThemeColor::dark();
theme_color.background = hsla(...);
theme_color.foreground = hsla(...);
theme_color.accent = hsla(...);

// Apply globally
let theme = GpuiTheme::global_mut(cx);
theme.colors = theme_color;
theme.mode = ThemeMode::Dark;
```

### Sizing
Components support consistent sizing:

```rust
use gpui_component::{Sizable, Size};

Input::new(state).size(Size::Small)   // xs, sm, md, lg
Button::new("btn").size(Size::Large)
```

## Fork Modifications

The fork at `johnlindquist/gpui-component` adds two features for snippet/template support:

### 1. `set_selection()` - Programmatic Text Selection
```rust
// Select text range by byte offsets
input_state.update(cx, |state, cx| {
    state.set_selection(start_bytes, end_bytes, window, cx);
});

// Get current selection
let selection: Range<usize> = input_state.read(cx).selection();
```

**Use case**: Snippet tabstop navigation - select placeholder text when moving between tabstops.

### 2. `tab_navigation_mode` - Tab Key Propagation
```rust
let editor_state = cx.new(|cx| 
    InputState::new(window, cx)
        .tab_navigation(true)  // Tab/Shift+Tab propagate instead of indent
);

// Or set dynamically
input_state.update(cx, |state, _| {
    state.set_tab_navigation(true);
});
```

**Use case**: When in snippet mode, Tab navigates to next tabstop instead of inserting indentation.

## Key Patterns

### Window Lifecycle
```rust
// Store window handle
static MY_WINDOW: OnceLock<Mutex<Option<WindowHandle<Root>>>> = OnceLock::new();

// Open window
let handle = cx.open_window(..., |window, cx| {
    cx.new(|cx| Root::new(my_view, window, cx))
})?;

// Store handle
MY_WINDOW.get_or_init(|| Mutex::new(None))
    .lock().unwrap().replace(handle);

// Update window
if let Some(handle) = get_window_handle() {
    handle.update(cx, |root, window, cx| {
        // Access view through root
    }).ok();
}
```

### Event Subscription Pattern
```rust
// Subscribe to entity events
let subscription = cx.subscribe_in(&entity, window, |this, _, event, window, cx| {
    // Handle event
});

// Store subscription to keep it alive
self.subscriptions.push(subscription);
```

### Focus Management
```rust
// Focus input
input_state.update(cx, |state, cx| {
    state.focus(window, cx);
});

// Check focus
if input_state.read(cx).is_focused(window) { ... }
```

## Anti-patterns

### Missing Root Wrapper
```rust
// WRONG - gpui-component widgets won't theme correctly
cx.open_window(..., |window, cx| {
    cx.new(|_| MyApp::new())
});

// CORRECT - wrap in Root
cx.open_window(..., |window, cx| {
    let view = cx.new(|_| MyApp::new());
    cx.new(|cx| Root::new(view, window, cx))
});
```

### Missing init() Call
```rust
// WRONG - components may not initialize properly
app.run(move |cx| {
    cx.open_window(...);
});

// CORRECT - call init before using components
app.run(move |cx| {
    gpui_component::init(cx);  // FIRST
    cx.open_window(...);
});
```

### Forgetting to Store Subscriptions
```rust
// WRONG - subscription dropped immediately, events not received
cx.subscribe_in(&state, window, |_, _, _, _, _| { ... });

// CORRECT - store subscription
self.subscription = Some(cx.subscribe_in(&state, window, |_, _, _, _, _| { ... }));
```

### Using Char Offsets for Selection
```rust
// WRONG - set_selection uses byte offsets, not char offsets
let char_pos = 5;
state.set_selection(char_pos, char_pos + 3, window, cx);

// CORRECT - convert char to byte offset
fn char_to_byte(text: &str, char_offset: usize) -> usize {
    text.char_indices()
        .nth(char_offset)
        .map(|(i, _)| i)
        .unwrap_or(text.len())
}
let start = char_to_byte(&text, 5);
let end = char_to_byte(&text, 8);
state.set_selection(start, end, window, cx);
```

### Not Handling InputEvent Variants
```rust
// WRONG - only handling some events
match event {
    InputEvent::Change => { ... }
    _ => {}  // Missing Focus/Blur handling
}

// CORRECT - handle all relevant events
match event {
    InputEvent::Focus => { self.focused = true; cx.notify(); }
    InputEvent::Blur => { self.focused = false; cx.notify(); }
    InputEvent::Change => { self.handle_change(cx); }
    InputEvent::PressEnter { secondary } => { self.submit(cx); }
}
```

## Common Imports

```rust
// Core
use gpui_component::Root;
use gpui_component::{Sizable, Size};

// Input
use gpui_component::input::{Input, InputEvent, InputState};
use gpui_component::input::{IndentInline, OutdentInline, Position};  // For code editor

// Button
use gpui_component::button::{Button, ButtonVariants};

// Icons
use gpui_component::{Icon, IconName, IconNamed};

// Notifications
use gpui_component::notification::{Notification, NotificationType};

// Theme
use gpui_component::theme::{ActiveTheme, Theme, ThemeColor, ThemeMode};

// Window utilities
use gpui_component::WindowExt;
```

## Resources

- [Upstream Repository](https://github.com/longbridge/gpui-component)
- [Documentation](https://gpui-component.longbridge.xyz/)
- [Icon Reference (Lucide)](https://lucide.dev/icons/)
- [Fork with set_selection()](https://github.com/johnlindquist/gpui-component)
