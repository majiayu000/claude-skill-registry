---
name: gpui-patterns
description: GPUI framework patterns for Script Kit. Use when writing UI code, handling keyboard events, managing state, or working with layouts. Covers layout chains, lists, themes, events, focus, and window management.
---

# GPUI Patterns

Essential patterns for building UI with GPUI in Script Kit.

## Quick Reference (Things That Break Most Often)

- **Layout chain order:** Layout (`flex*`) → Sizing (`w/h`) → Spacing (`px/gap`) → Visual (`bg/border`)
- **Lists:** `uniform_list` (fixed height **52px**) + `UniformListScrollHandle`
- **Theme colors:** use `theme.colors.*` (**never** `rgb(0x...)`)
- **Focus colors:** use `theme.get_colors(is_focused)`; re-render on focus change
- **State updates:** after render-affecting changes, **must** `cx.notify()`
- **Keyboard:** use `cx.listener()`; coalesce rapid events (20ms)
- **Arrow keys:** match both `"up"|"arrowup"`, `"down"|"arrowdown"`, etc.

## Keyboard Key Names (CRITICAL)

GPUI often sends short arrow keys on macOS. Always match both:
```rust
match key.as_str() {
  "up" | "arrowup" => self.move_up(),
  "down" | "arrowdown" => self.move_down(),
  "left" | "arrowleft" => self.move_left(),
  "right" | "arrowright" => self.move_right(),
  _ => {}
}
```

Also handle: `"enter"|"Enter"`, `"escape"|"Escape"`, `"tab"|"Tab"`

## Layout System

Chain in order: layout → sizing → spacing → visual → children.

```rust
div().flex().flex_row().items_center().gap_2();
div().flex().flex_col().w_full();
div().flex().items_center().justify_center();
div().flex_1(); // fill remaining space
```

Conditional rendering:
```rust
div().when(is_selected, |d| d.bg(selected)).when_some(desc, |d, s| d.child(s));
```

## List Virtualization

Use `uniform_list` with fixed-height rows (~52px):
```rust
uniform_list("script-list", filtered.len(), cx.processor(|this, range, _w, _cx| {
  this.render_list_items(range)
}))
.h_full()
.track_scroll(&self.list_scroll_handle);
```

Scroll to item:
```rust
self.list_scroll_handle.scroll_to_item(selected_index, ScrollStrategy::Nearest);
```

## Theme System

```rust
let colors = &self.theme.colors;
div().bg(rgb(colors.background.main)).border_color(rgb(colors.ui.border));
```

Focus-aware:
- compute `is_focused = self.focus_handle.is_focused(window)`
- if changed: update state + `cx.notify()`
- use `let colors = self.theme.get_colors(is_focused);`

For closures: extract copyable structs like `colors.list_item_colors()`.

## Events + Focus

```rust
let focus_handle = cx.focus_handle();
focus_handle.focus(window);

window.on_key_down(cx.listener(|this, e: &KeyDownEvent, window, cx| {
  let key = e.key.as_ref().map(|k| k.as_str()).unwrap_or("");
  match key {
    "up"|"arrowup" => this.move_up(cx),
    "escape"|"Escape" => this.cancel(cx),
    _ => {}
  }
}));
```

## State Management

After any state mutation affecting rendering: `cx.notify()`

Shared state: `Arc<Mutex<T>>` or channels; for async, use `mpsc` sender → UI receiver.

## References

- [Anti-Patterns](references/anti-patterns.md) - Common mistakes that cause bugs
- [Smart Pointers](references/smart-pointers.md) - Arc, Rc, Mutex patterns
- [Window Management](references/window-management.md) - Multi-monitor, floating panels
- [Scroll Performance](references/scroll-performance.md) - Rapid-key coalescing
- [Testing Patterns](references/testing-patterns.md) - GPUI test organization
