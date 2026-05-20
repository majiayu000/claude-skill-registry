---
name: script-kit-icons
description: Unified icon system for Script Kit GPUI. Use when working with icons in the UI - rendering Lucide icons, embedded SVGs, SF Symbols (macOS), app bundle icons, or custom file/URL icons. Covers IconRef parsing, IconStyle configuration, color tokens, and the IconView rendering API.
---

# Script Kit Icons

Unified icon API that abstracts multiple icon sources into a single `IconRef` type.

## Quick Reference

```rust
use crate::icons::{IconRef, IconView, IconSize, IconColor, ColorToken, EmbeddedIcon};

// From gpui_component IconName (Lucide)
let icon = IconRef::from(gpui_component::IconName::Check);

// From string (scripts use this format)
let icon = IconRef::parse("lucide:trash").unwrap();

// Render with styling
IconView::new(icon)
    .size(IconSize::Large)
    .color(IconColor::Token(ColorToken::Accent))
    .render(theme, window)
```

## Icon Sources

| Scheme | Example | Notes |
|--------|---------|-------|
| `lucide:` | `lucide:trash` | Lucide icons via gpui_component |
| `sf:` | `sf:gear` | SF Symbols (macOS 11+) |
| `embedded:` | `embedded:terminal` | Script Kit's bundled SVGs |
| `asset:` | `asset:icons/custom.svg` | SVG from assets folder |
| `file:` | `file:icons/my.svg` | Script-relative file path |
| `url:` | `url:https://...` | Remote URL (gated) |
| `app:` | `app:com.apple.finder` | macOS app bundle icon |

## IconRef Enum

```rust
pub enum IconRef {
    Lucide(gpui_component::IconName),  // Tintable
    SFSymbol(SharedString),             // Tintable
    Embedded(EmbeddedIcon),             // Tintable
    AssetSvg(SharedString),             // Tintable
    File(PathBuf),                      // Tintable
    Url(SharedString),                  // NOT tintable
    AppBundle(SharedString),            // NOT tintable
}
```

## IconSize

| Variant | Pixels |
|---------|--------|
| `XSmall` | 12px |
| `Small` | 14px |
| `Medium` | 16px (default) |
| `Large` | 20px |
| `XLarge` | 24px |
| `Custom(f32)` | any |

## IconColor

```rust
pub enum IconColor {
    Inherit,              // From parent text style (default)
    Token(ColorToken),    // Theme color
    Fixed(Hsla),          // Exact color
    None,                 // No tint (full-color icons)
}

pub enum ColorToken {
    Primary,   // theme.foreground()
    Muted,     // theme.muted()
    Accent,    // theme.accent()
    Danger,    // theme.danger()
    Success,   // theme.success()
    Warning,   // theme.warning()
}

// Helpers
IconColor::from_hex(0xFF0000)  // Red
```

## EmbeddedIcon

Script Kit's bundled SVGs:

```rust
pub enum EmbeddedIcon {
    // Files
    File, FileCode, Folder, FolderOpen,
    // Actions
    Plus, Trash, Copy, Settings, MagnifyingGlass, Terminal, Code,
    // Status
    Check, Star, StarFilled, BoltFilled, BoltOutlined,
    // Arrows
    ArrowRight, ArrowDown, ArrowUp, ChevronRight, ChevronDown,
    // UI
    Close, Sidebar,
    // Media
    PlayFilled, PlayOutlined,
}

// Parse with aliases
EmbeddedIcon::parse("terminal")     // Terminal
EmbeddedIcon::parse("search")       // MagnifyingGlass
EmbeddedIcon::parse("lightning")    // BoltFilled
```

## IconView (Fluent Builder)

```rust
IconView::new(gpui_component::IconName::Check)
    .size(IconSize::Large)
    .color(IconColor::Token(ColorToken::Success))
    .opacity(0.8)
    .render(theme, window)  // -> AnyElement
```

## Rendering Function

```rust
pub fn render_icon(
    icon: &IconRef,
    style: &IconStyle,
    theme: &dyn ThemeColorProvider,
    window: &Window,
) -> AnyElement
```

## ThemeColorProvider Trait

Implement to provide theme colors:

```rust
pub trait ThemeColorProvider {
    fn foreground(&self) -> Hsla;
    fn muted(&self) -> Hsla;
    fn accent(&self) -> Hsla;
    fn danger(&self) -> Hsla;
    fn success(&self) -> Hsla;
    fn warning(&self) -> Hsla;
}
```

## Fallback Chain

Icons that require async loading or platform APIs fall back automatically:

| Source | Fallback |
|--------|----------|
| `SFSymbol` | Mapped Lucide equivalent |
| `AppBundle` | `Lucide::Frame` |
| `Url` | `Lucide::ExternalLink` |
| `File` | `Lucide::File` |

## Lucide Name Mapping

Supports kebab-case names and common aliases:

```rust
lucide_from_str("arrow-right")  // ArrowRight
lucide_from_str("trash")        // Delete
lucide_from_str("x")            // Close
lucide_from_str("cog")          // Settings
lucide_from_str("terminal")     // SquareTerminal
```

## File Locations

- `src/icons/mod.rs` - Module root, exports
- `src/icons/types/icon_ref.rs` - IconRef enum + parsing
- `src/icons/types/icon_style.rs` - IconSize, IconColor, IconStyle
- `src/icons/types/embedded.rs` - EmbeddedIcon enum
- `src/icons/types/lucide_mapping.rs` - String-to-Lucide mapping
- `src/icons/render.rs` - IconView + render_icon()
