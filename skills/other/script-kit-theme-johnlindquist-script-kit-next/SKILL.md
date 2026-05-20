---
name: script-kit-theme
description: Theme and color system for script-kit-gpui
---

# script-kit-theme

A comprehensive theming system for Script Kit's GPUI interface. The theme supports:
- Dark/light mode with automatic system appearance detection
- Focus-aware color variations (dimmed colors when window loses focus)
- macOS vibrancy/translucency effects
- ANSI terminal color palette (16 colors)
- Integration with gpui-component's ThemeColor system
- Hot-reloading via file watcher

Theme configuration lives at `~/.scriptkit/kit/theme.json`.

**Important**: See `AGENTS.md` §17b for the GPUI Vibrancy Gotcha - GPUI hides the `CAChameleonLayer` so you must provide your own dark tint via theme colors at 70-85% opacity.

## Key Types

### Core Theme Types (`types.rs`)

```rust
/// Complete theme definition - the root struct
pub struct Theme {
    pub colors: ColorScheme,           // Required: base colors
    pub focus_aware: Option<FocusAwareColorScheme>,  // Optional: focus-specific overrides
    pub opacity: Option<BackgroundOpacity>,          // Window transparency settings
    pub drop_shadow: Option<DropShadow>,             // Window shadow config
    pub vibrancy: Option<VibrancySettings>,          // macOS blur effect
    pub fonts: Option<FontConfig>,                   // Font families and sizes
}

/// Color scheme with all color categories
pub struct ColorScheme {
    pub background: BackgroundColors,  // main, title_bar, search_box, log_panel
    pub text: TextColors,              // primary, secondary, tertiary, muted, dimmed
    pub accent: AccentColors,          // selected (#fbbf24 gold), selected_subtle
    pub ui: UIColors,                  // border, success, error, warning, info
    pub terminal: TerminalColors,      // 16 ANSI colors for embedded terminal
}
```

### HexColor (`hex_color.rs`)

```rust
/// Colors stored as u32 (0xRRGGBB)
pub type HexColor = u32;

// Supports multiple input formats in JSON:
// - Numbers: 1973790 (decimal)
// - Hex strings: "#1E1E1E", "1E1E1E", "0x1E1E1E"  
// - RGB/RGBA: "rgb(30, 30, 30)", "rgba(30, 30, 30, 1.0)"
```

### Opacity Settings (`types.rs`)

```rust
pub struct BackgroundOpacity {
    pub main: f32,           // Main window (0.30)
    pub title_bar: f32,      // Title bar (0.30)
    pub search_box: f32,     // Input fields (0.40)
    pub log_panel: f32,      // Log/terminal (0.40)
    pub selected: f32,       // Selected item (0.15)
    pub hover: f32,          // Hovered item (0.08)
    pub dialog: f32,         // Dialogs/popups (0.15)
    pub input: f32,          // Input backgrounds (0.30)
    pub panel: f32,          // Panels/containers (0.20)
    // ... and more state-specific opacities
}
```

### Vibrancy (`types.rs`)

```rust
pub struct VibrancySettings {
    pub enabled: bool,              // Default: true
    pub material: VibrancyMaterial, // Default: Popover
}

pub enum VibrancyMaterial {
    Hud,      // Dark, high contrast
    Popover,  // Light blur (default) - matches Electron's vibrancy:'popover'
    Menu,     // System menu style
    Sidebar,  // Sidebar blur
    Content,  // Content background
}
```

### Semantic Colors (`semantic.rs`)

Higher-level abstraction for component styling:

```rust
/// Focus-aware wrapper for any type
pub struct FocusAware<T> {
    pub focused: T,
    pub unfocused: T,
}

/// Semantic tokens (bg_*, text_*, border_*, status_*, overlay_*)
pub struct SemanticColors {
    // Backgrounds
    pub bg_primary: Hsla,
    pub bg_secondary: Hsla,
    pub bg_selected: Hsla,
    pub bg_hover: Hsla,
    // Text
    pub text_primary: Hsla,
    pub text_secondary: Hsla,
    pub text_muted: Hsla,
    pub text_accent: Hsla,
    // Status
    pub status_success: Hsla,
    pub status_error: Hsla,
    // ... and more
}

/// UI surface types for consistent styling
pub enum Surface {
    App, Sidebar, Panel, Input, Elevated, ListItem, Header
}
```

## Usage Patterns

### Loading the Theme

```rust
use crate::theme::{load_theme, Theme};

// Loads from ~/.scriptkit/kit/theme.json, falls back to defaults
let theme = load_theme();

// Get colors based on window focus state
let colors = theme.get_colors(is_focused);

// Get opacity settings (auto-reduced by 10% when unfocused)
let opacity = theme.get_opacity_for_focus(is_focused);
```

### Using Theme in Components

```rust
// Get background with proper opacity for vibrancy
let (r, g, b, a) = theme.background_rgba(BackgroundRole::Main, is_focused);
div().bg(rgba(r, g, b, a))

// Use semantic colors
let semantic = SemanticColors::dark();
div()
    .bg(semantic.bg_primary)
    .text_color(semantic.text_primary)
    .border_color(semantic.border_default)
```

### Focus-Aware Styling

```rust
use crate::theme::semantic::FocusAware;

let colors = FocusAware::new(
    SemanticColors::dark(),
    SemanticColors::dark().dimmed(),
);

// In render, pick based on window focus
let current = colors.for_focus(window.is_focused());
div().bg(current.bg_primary)
```

### Lightweight Helpers for Render Closures

```rust
use crate::theme::helpers::{ListItemColors, InputFieldColors};

// Pre-compute colors (Copy type, no heap allocation)
let list_colors = theme.colors.list_item_colors();

// Use in render closure without cloning full theme
.child(list_item.map(move |item| {
    div()
        .bg(if selected { list_colors.background_selected } else { list_colors.background })
        .text_color(list_colors.text)
}))
```

## Integration

### GPUI-Component Theme Sync (`gpui_integration.rs`)

The theme syncs with gpui-component's global ThemeColor:

```rust
use crate::theme::sync_gpui_component_theme;

// Call after gpui_component::init(cx) in main.rs
// Also called automatically when theme.json changes
sync_gpui_component_theme(cx);
```

This maps Script Kit colors to gpui-component tokens: `background`, `foreground`, `accent`, `primary`, `secondary`, `muted`, `list_*`, `sidebar_*`, etc.

### Theme Service (`service.rs`)

Global file watcher that hot-reloads theme changes:

```rust
use crate::theme::service::{ensure_theme_service, theme_revision};

// Call once at app startup
ensure_theme_service(cx);

// Check theme revision for cache invalidation
let rev = theme_revision();
if self.cached_rev != rev {
    self.cached_rev = rev;
    self.recompute_styles();
}
```

Key functions:
- `ensure_theme_service(cx)` - Start the global theme watcher (idempotent)
- `theme_revision()` - Get current revision number for cache invalidation
- `is_theme_service_running()` - Check if service is active (debug/testing)

### Theme Validation (`validation.rs`)

Validate theme JSON before loading:

```rust
use crate::theme::validation::validate_theme_json;

let json: Value = serde_json::from_str(&contents)?;
let diagnostics = validate_theme_json(&json);

if diagnostics.has_errors() {
    eprintln!("{}", diagnostics.format_for_log());
}
```

## Example theme.json

```json
{
  "colors": {
    "background": {
      "main": "#1E1E1E",
      "title_bar": "#2D2D30",
      "search_box": "#3C3C3C",
      "log_panel": "#0D0D0D"
    },
    "text": {
      "primary": "#FFFFFF",
      "secondary": "#CCCCCC",
      "tertiary": "#999999",
      "muted": "#808080",
      "dimmed": "#666666"
    },
    "accent": {
      "selected": "#FBBF24",
      "selected_subtle": "#2A2A2A"
    },
    "ui": {
      "border": "#464647",
      "success": "#00FF00",
      "error": "#EF4444",
      "warning": "#F59E0B",
      "info": "#3B82F6"
    }
  },
  "opacity": {
    "main": 0.30,
    "title_bar": 0.30,
    "selected": 0.15,
    "hover": 0.08
  },
  "vibrancy": {
    "enabled": true,
    "material": "popover"
  },
  "fonts": {
    "mono_family": "JetBrains Mono",
    "mono_size": 16.0,
    "ui_family": ".SystemUIFont",
    "ui_size": 16.0
  }
}
```

## Anti-patterns

### DON'T: Clone full theme into render closures

```rust
// Bad - heap allocation on every render
let theme_clone = theme.clone();
.child(items.map(move |item| {
    let colors = theme_clone.colors.clone(); // Expensive!
    ...
}))
```

**DO**: Use lightweight helper structs:

```rust
// Good - Copy type, stack allocated
let list_colors = theme.colors.list_item_colors();
.child(items.map(move |item| {
    div().bg(list_colors.background_selected) // Zero-cost
}))
```

### DON'T: Apply opacity to UI element colors

```rust
// Bad - makes text unreadable
let bg = hex_to_hsla(colors.background.main);
let bg_with_opacity = hsla(bg.h, bg.s, bg.l, 0.3); // Wrong!
```

**DO**: Only use opacity for window-level vibrancy:

```rust
// Good - opacity is for window background, not UI elements
let main_bg = if vibrancy_enabled {
    with_vibrancy(colors.background.main, 0.37) // Tuned for vibrancy
} else {
    hex_to_hsla(colors.background.main) // Opaque when no vibrancy
};
```

### DON'T: Hardcode colors

```rust
// Bad
div().bg(rgb(0x1e1e1e))
```

**DO**: Use theme tokens:

```rust
// Good
let colors = theme.get_colors(is_focused);
div().bg(hex_to_hsla(colors.background.main))
```

### DON'T: Ignore focus state

```rust
// Bad - always same appearance
let colors = theme.colors.clone();
```

**DO**: Respect window focus:

```rust
// Good - dims when unfocused
let colors = theme.get_colors(cx.is_window_focused());
```

### DON'T: Start multiple theme watchers

```rust
// Bad - creates duplicate watchers per window
fn setup_window() {
    start_theme_watcher(cx); // Each window starts its own!
}
```

**DO**: Use the global theme service:

```rust
// Good - single watcher, broadcasts to all windows
fn main() {
    ensure_theme_service(cx); // Once at startup
}
```

## File Structure

```
src/theme/
  mod.rs              - Module exports and re-exports
  types.rs            - Theme, ColorScheme, BackgroundOpacity, VibrancySettings, FontConfig, load_theme()
  hex_color.rs        - HexColor type and serde support
  semantic.rs         - FocusAware<T>, SemanticColors, Surface, SurfaceStyle
  helpers.rs          - ListItemColors, InputFieldColors (Copy types for render closures)
  gpui_integration.rs - sync_gpui_component_theme()
  service.rs          - Global theme watcher service (ensure_theme_service, theme_revision)
  validation.rs       - Theme JSON validation with diagnostics
  theme_tests.rs      - Unit tests
  validation_tests.rs - Validation-specific tests
```
