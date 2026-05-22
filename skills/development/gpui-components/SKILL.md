---
name: gpui-components
description: Generates Rust code for GPUI desktop UI components following Zed editor patterns. Use when building desktop applications with gpui crate, creating themed UI components, implementing autocomplete/completions, building command palettes, or working with the gpui-component library. Covers RenderOnce components, Entity state management, theming with ActiveTheme, and Zed-style UI patterns.
---

# GPUI Components Skill

Generates production-ready Rust code for GPUI desktop UI components following patterns from Zed editor and gpui-component library.

## When to Use This Skill

- Building desktop UI applications with GPUI framework
- Creating custom components using `RenderOnce` or `Render` traits
- Implementing themed components with `ActiveTheme`
- Building autocomplete/completion menus
- Creating command palettes and popup menus
- Working with `gpui-component` crate

## Core GPUI Concepts

### Application Setup

```rust
use gpui::{Application, Window, Context, div, px, rgb};
use gpui_component::{init, Root, Theme};

fn main() {
    Application::new().run(|cx| {
        // Initialize gpui-component
        gpui_component::init(cx);
        
        cx.open_window(
            WindowOptions::default(),
            |window, cx| Root::new(MyApp::new(cx), window, cx)
        );
    });
}
```

### Component Patterns

#### RenderOnce (Stateless)
```rust
use gpui::{IntoElement, RenderOnce, Styled, div};

#[derive(IntoElement)]
pub struct MyButton {
    label: SharedString,
    variant: ButtonVariant,
}

impl RenderOnce for MyButton {
    fn render(self, window: &mut Window, cx: &mut App) -> impl IntoElement {
        div()
            .px_3()
            .py_2()
            .bg(cx.theme().primary)
            .text_color(cx.theme().primary_foreground)
            .rounded_md()
            .child(self.label)
    }
}
```

#### Render with Entity (Stateful)
```rust
use gpui::{Entity, Render, Context};

pub struct Counter {
    count: i32,
}

impl Render for Counter {
    fn render(&mut self, window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        div()
            .flex()
            .gap_2()
            .child(Button::new("dec").on_click(cx.listener(|this, _, _, cx| {
                this.count -= 1;
                cx.notify();
            })))
            .child(format!("Count: {}", self.count))
            .child(Button::new("inc").on_click(cx.listener(|this, _, _, cx| {
                this.count += 1;
                cx.notify();
            })))
    }
}
```

## Available Components (gpui-component)

### Form Components
- `Button` - Buttons with variants (primary, danger, ghost, link)
- `Input` - Text input with LSP completion support
- `NumberInput` - Numeric input with step controls
- `Checkbox` - Checkbox with label
- `Switch` - Toggle switch
- `Radio` - Radio button groups
- `Select` - Dropdown select
- `Slider` - Range slider

### Layout Components
- `Dialog` - Modal dialogs
- `Popover` - Popup popovers
- `Menu` / `PopupMenu` - Menus and context menus
- `Tab` - Tab navigation
- `Accordion` - Collapsible sections
- `Sidebar` - Sidebar navigation
- `Dock` - Dockable panels

### Display Components
- `Badge` - Status badges
- `Avatar` - User avatars
- `Icon` - Icon display (IconName enum)
- `Label` - Text labels
- `Tooltip` - Tooltips
- `Notification` - Toast notifications

### Data Components
- `Table` - Data tables
- `List` / `VirtualList` - Scrollable lists
- `Tree` - Tree view
- `Chart` - Charts and plots

## Theming

### Accessing Theme
```rust
use gpui_component::ActiveTheme;

fn render(&mut self, window: &mut Window, cx: &mut App) -> impl IntoElement {
    div()
        .bg(cx.theme().background)
        .text_color(cx.theme().foreground)
        .border_1()
        .border_color(cx.theme().border)
}
```

### Theme Colors
```rust
// Background colors
cx.theme().background      // Primary background
cx.theme().secondary       // Secondary background  
cx.theme().muted          // Muted background
cx.theme().card           // Card background

// Foreground colors
cx.theme().foreground     // Primary text
cx.theme().muted_foreground // Muted text

// Semantic colors
cx.theme().primary        // Primary accent
cx.theme().destructive    // Danger/error
cx.theme().success        // Success
cx.theme().warning        // Warning

// Border colors
cx.theme().border         // Default border
cx.theme().ring           // Focus ring
```

## Component Examples

### Button Usage
```rust
use gpui_component::button::{Button, ButtonVariants};

Button::new("save")
    .label("Save")
    .icon(IconName::Save)
    .primary()
    .on_click(cx.listener(|this, _, window, cx| {
        this.save(window, cx);
    }))
```

### Input with State
```rust
use gpui_component::input::{Input, InputState};

// Create state
let input_state = cx.new(|cx| InputState::new(cx));

// In render:
Input::new(&self.input_state)
    .placeholder("Enter text...")
    .cleanable(true)
```

### PopupMenu / Command Palette
```rust
use gpui_component::menu::{PopupMenu, PopupMenuItem};

let menu = cx.new(|cx| {
    PopupMenu::build(cx, |menu, window, cx| {
        menu.menu_item(PopupMenuItem::new("New File")
            .icon(IconName::FilePlus)
            .action(Box::new(NewFile)))
        .separator()
        .menu_item(PopupMenuItem::new("Save")
            .icon(IconName::Save)
            .action(Box::new(Save)))
    })
});
```

### Completion Provider
```rust
use gpui_component::input::{CompletionProvider, InputState};

struct MyCompletionProvider;

impl CompletionProvider for MyCompletionProvider {
    fn completions(
        &self,
        text: &Rope,
        offset: usize,
        trigger: CompletionContext,
        window: &mut Window,
        cx: &mut Context<InputState>,
    ) -> Task<Result<CompletionResponse>> {
        let items = vec![
            CompletionItem {
                label: "option1".into(),
                ..Default::default()
            },
        ];
        Task::ready(Ok(CompletionResponse::Array(items)))
    }
    
    fn is_completion_trigger(
        &self,
        offset: usize,
        new_text: &str,
        cx: &mut Context<InputState>,
    ) -> bool {
        new_text == "/" || new_text == "@"
    }
}
```

## Reference Files

For detailed patterns, read:
- `reference/components.md` - Full component API
- `reference/theming.md` - Theme system details
- `reference/input-lsp.md` - Input with completions
- `reference/menus.md` - Menu and command palette

## Project Setup

### Cargo.toml
```toml
[dependencies]
gpui = "0.2"
gpui-component = { version = "0.4", features = ["webview"] }
```

### Basic App Structure
```rust
use gpui::*;
use gpui_component::*;

struct App {
    // state
}

impl Render for App {
    fn render(&mut self, window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        Root::new(
            div()
                .size_full()
                .flex()
                .flex_col()
                .bg(cx.theme().background)
                .child(self.render_toolbar(window, cx))
                .child(self.render_content(window, cx)),
            window,
            cx
        )
    }
}

fn main() {
    Application::new().run(|cx| {
        gpui_component::init(cx);
        cx.open_window(WindowOptions::default(), |window, cx| {
            cx.new(|cx| App::new(cx))
        });
    });
}
```
