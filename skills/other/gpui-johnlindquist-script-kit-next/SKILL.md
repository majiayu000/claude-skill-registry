---
name: gpui
description: Build desktop apps with GPUI, the GPU-accelerated UI framework from Zed. Covers Entity state, Render trait, div() Tailwind API, actions/keybindings, gpui-component widgets, theming. Use when building Rust desktop applications with GPUI or gpui-component.
---

# GPUI Development

GPUI is a hybrid immediate/retained mode, GPU-accelerated UI framework for Rust from Zed.

## Quick Reference

| Topic | When to Use | Reference |
|-------|-------------|-----------|
| **Fundamentals** | Starting new projects, understanding architecture | [fundamentals.md](fundamentals.md) |
| **State Management** | Entity<T>, notify(), emit(), subscribe() | [state-management.md](state-management.md) |
| **Rendering** | div() API, layout, conditional rendering | [rendering.md](rendering.md) |
| **Actions** | Keyboard shortcuts, key bindings | [actions.md](actions.md) |
| **Components** | gpui-component widgets (Button, Input, Table) | [components.md](components.md) |
| **Theming** | Colors, cx.theme(), Root view | [theming.md](theming.md) |
| **Anti-patterns** | Common mistakes to avoid | [anti-patterns.md](anti-patterns.md) |

## Critical Setup (MUST DO)

```rust
use gpui::{Application, App};
use gpui_component::Root;

fn main() {
    Application::new().run(|cx: &mut App| {
        gpui_component::init(cx);  // REQUIRED when using gpui-component
        
        cx.open_window(opts, |window, cx| {
            let view = cx.new(|cx| MyView::new(window, cx));
            cx.new(|cx| Root::new(view, window, cx))  // REQUIRED for theming
        });
    });
}
```

## Key Mental Model (React vs GPUI)

| React | GPUI | Key Difference |
|-------|------|----------------|
| `useState` | Struct fields + `cx.notify()` | State in struct, manual re-render trigger |
| Component | View (impl `Render`) | Views are Entities that render |
| Virtual DOM | GPU rendering | No diffing - rebuild elements each frame |
| Props drilling | `Entity<T>` handles | Pass entity handles, not callbacks |

## Instructions

**REQUIRED**: Before implementing GPUI code, load the relevant reference file(s) using the Read tool.

1. **Identify the task** - What are you building?
2. **Load relevant references** - Read the appropriate .md file(s) FIRST
3. **Follow patterns exactly** - Use code patterns from references
4. **Check anti-patterns** - Read [anti-patterns.md](anti-patterns.md) before writing code

### Reference Selection Guide

- **New project setup** → Read [fundamentals.md](fundamentals.md) FIRST
- **Managing state, events** → Read [state-management.md](state-management.md) FIRST
- **Building UI layouts** → Read [rendering.md](rendering.md) FIRST
- **Adding keyboard shortcuts** → Read [actions.md](actions.md) FIRST
- **Using Button, Input, Select, Table** → Read [components.md](components.md) FIRST
- **Styling, colors, themes** → Read [theming.md](theming.md) FIRST
- **Debugging issues** → Read [anti-patterns.md](anti-patterns.md) FIRST

## Cargo.toml

```toml
[dependencies]
gpui = "0.2.2"
gpui-component = "0.6.0-preview0"
```

## Common Patterns

### State Update Pattern

```rust
impl MyView {
    fn update_something(&mut self, cx: &mut Context<Self>) {
        self.value = new_value;
        cx.notify();  // ALWAYS call after state changes
    }
}
```

### Button Click Pattern

```rust
Button::new("btn-id")
    .label("Click Me")
    .on_click(|_, _, cx| {
        // handle click
    })
```

### Stateful Component Pattern

```rust
struct MyView {
    input: Entity<InputState>,  // Store entity in struct
}

impl MyView {
    fn new(window: &Window, cx: &mut Context<Self>) -> Self {
        Self {
            input: cx.new(|cx| InputState::new(window, cx)),  // Create once
        }
    }
}
```
