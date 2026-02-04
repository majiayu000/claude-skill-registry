---
name: script-kit-components
description: UI component patterns for Script Kit GPUI. Use when building list items, buttons, prompts, panels, or any reusable UI component. Covers ListItem, UnifiedListItem, Button, PromptContainer, panel configuration, and the Colors struct pattern. Triggers on "component", "list item", "button", "panel", "prompt container", "UI element".
---

# Script Kit UI Components

Component architecture for GPUI-based UI in Script Kit.

## Core Pattern: Colors Struct

Every component uses a pre-computed Colors struct for efficient closure use:

```rust
#[derive(Clone, Copy)]
pub struct ListItemColors {
    pub text_primary: u32,
    pub text_secondary: u32,
    pub background: u32,
    pub selected_opacity: f32,
    // ... other colors
}

impl ListItemColors {
    pub fn from_theme(theme: &Theme) -> Self { /* ... */ }
    pub fn from_design(colors: &DesignColors) -> Self { /* ... */ }
}
```

**Why**: Closures in GPUI can't clone full Theme. Extract primitive values (u32, f32) into Copy struct.

## ListItem Component

Reusable list item for virtualized lists. Fixed height (48px) for `uniform_list`.

### Basic Usage

```rust
use crate::list_item::{ListItem, ListItemColors, LIST_ITEM_HEIGHT};

let colors = ListItemColors::from_theme(&theme);

ListItem::new("Item Name", colors)
    .description("Optional description")
    .icon("📋")  // Emoji
    .shortcut("⌘O")
    .selected(is_selected)
    .hovered(is_hovered)
    .with_accent_bar(true)
```

### Icon Types

```rust
pub enum IconKind {
    Emoji(String),           // "📋", "⚡"
    Image(Arc<RenderImage>), // Pre-decoded PNG (decode ONCE, not per-render)
    Svg(String),             // Icon name: "File", "Terminal", "Code"
}

// Use builder methods:
.icon("📋")                    // Emoji shorthand
.icon_image(decoded_image)     // Pre-decoded RenderImage
.icon_kind(IconKind::Svg("File".into()))
```

**Critical**: Decode PNGs once at load time, not during render:
```rust
let render_image = decode_png_to_render_image(&png_bytes)?;
ListItem::new(name, colors).icon_image(render_image)
```

### Grouped Lists with Section Headers

For lists with sections (e.g., "Recent", "Main"):

```rust
use crate::list_item::{GroupedListItem, GroupedListState, render_section_header};

// Build items with headers
let items: Vec<GroupedListItem> = vec![
    GroupedListItem::SectionHeader("RECENT".into()),
    GroupedListItem::Item(0),
    GroupedListItem::Item(1),
    GroupedListItem::SectionHeader("MAIN".into()),
    GroupedListItem::Item(2),
];

// Create state for efficient navigation
let state = GroupedListState::from_items(&items);

// Navigate skipping headers
let next = state.next_selectable(current_idx);
let prev = state.prev_selectable(current_idx);

// Coerce selection to valid item (never lands on header)
let valid_idx = coerce_selection(&items, proposed_idx);
```

## UnifiedListItem Component

Enhanced list item with fuzzy match highlighting and flexible content slots.

### Basic Usage

```rust
use crate::components::unified_list_item::{
    UnifiedListItem, UnifiedListItemColors, TextContent,
    LeadingContent, TrailingContent, ItemState, Density
};

let colors = UnifiedListItemColors::from_theme(&theme);

UnifiedListItem::new("item-0", TextContent::plain("Title"))
    .subtitle(TextContent::plain("Subtitle"))
    .leading(LeadingContent::Emoji("📋".into()))
    .trailing(TrailingContent::Shortcut("⌘O".into()))
    .state(ItemState { is_selected: true, ..Default::default() })
    .colors(colors)
```

### Fuzzy Match Highlighting

```rust
// Highlight matched characters in title
let title = TextContent::highlighted(
    "my-script.ts",
    vec![0..2, 3..5]  // Byte ranges to highlight
);

UnifiedListItem::new("item-0", title)
```

### Content Types

```rust
// Leading (left side)
LeadingContent::Emoji("📋".into())
LeadingContent::Icon { name: "File".into(), color: None }
LeadingContent::AppIcon(arc_render_image)
LeadingContent::AppIconPlaceholder

// Trailing (right side)
TrailingContent::Shortcut("⌘O".into())
TrailingContent::Hint("Enter".into())
TrailingContent::Count(42)
TrailingContent::Chevron
TrailingContent::Checkmark
```

### Density

```rust
// 48px height (default)
.density(Density::Comfortable)

// 40px height
.density(Density::Compact)
```

## Button Component

```rust
use crate::components::{Button, ButtonColors, ButtonVariant};

let colors = ButtonColors::from_theme(&theme);

Button::new("Run", colors)
    .variant(ButtonVariant::Primary)  // Primary, Ghost, Icon
    .shortcut("⌘R")
    .on_click(Box::new(|event, window, cx| {
        // Handle click
    }))
```

## PromptContainer Component

Container for prompt windows with header/content/footer layout:

```rust
use crate::components::{PromptContainer, PromptContainerColors, PromptContainerConfig};

let colors = PromptContainerColors::from_theme(&theme);
let config = PromptContainerConfig::new()
    .rounded_corners(12.0)
    .show_divider(true)
    .background_opacity(0xE8);

PromptContainer::new(colors)
    .config(config)
    .header(header_element)
    .content(content_element)
    .footer(footer_element)
    // Or use hint shorthand:
    .hint("Press Enter to select")
```

## Panel Configuration

Window-level settings for macOS floating panels:

```rust
use crate::panel::{WindowVibrancy, PlaceholderConfig, CursorStyle};

// Vibrancy (blur effect)
WindowVibrancy::Blurred   // macOS vibrancy (default, recommended)
WindowVibrancy::Opaque    // Solid background
WindowVibrancy::Transparent

// Header layout constants
use crate::panel::{HEADER_PADDING_X, HEADER_PADDING_Y, HEADER_TOTAL_HEIGHT};

// Cursor styling for inputs
let cursor = CursorStyle::large();  // For .text_lg()
let cursor = CursorStyle::medium(); // For .text_md()
let cursor = CursorStyle::small();  // For .text_sm()
```

## Component Design Rules

1. **Colors struct**: Always Copy/Clone, use `from_theme()` and `from_design()`
2. **Builder pattern**: Fluent API with `.method()` chaining
3. **IntoElement trait**: Implement `RenderOnce` for GPUI compatibility
4. **Fixed heights**: Use constants for virtualized lists (LIST_ITEM_HEIGHT = 48px)
5. **Pre-decode images**: Never decode PNGs during render
6. **Hover states**: Use GPUI's `.hover()` for instant feedback, state for tracked hover

## File Structure

```
src/
├── list_item.rs          # ListItem, IconKind, GroupedListItem
├── panel.rs              # Window config, placeholders, cursor
└── components/
    ├── mod.rs            # Re-exports
    ├── button.rs         # Button component
    ├── prompt_container.rs
    ├── prompt_header.rs
    ├── prompt_footer.rs
    ├── unified_list_item/
    │   ├── mod.rs
    │   ├── types.rs      # TextContent, LeadingContent, etc.
    │   └── render.rs     # UnifiedListItem, SectionHeader
    └── ...
```
