---
name: padz-output-customization
description: Guide for customizing padz CLI output using templates and stylesheets. Use when working on padz rendering, modifying how pads are displayed, changing colors/styles, editing Jinja templates, or working with the outstanding crate integration. Covers the three-layer styling architecture, template syntax, and the compile-time embedding system.
---

# Padz Output Customization

Padz uses the `outstanding` crate for terminal rendering. Output is controlled by:

1. **Stylesheets** (`src/styles/default.yaml`) - Colors and text decoration
2. **Templates** (`src/cli/templates/*.jinja`) - Layout and structure

Both are embedded at compile time via outstanding's macros.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     render.rs                                │
│  create_renderer() → Renderer with theme + templates         │
├─────────────────────────────────────────────────────────────┤
│  styles.rs                  │  templates.rs                  │
│  embed_styles!("src/styles")│  embed_templates!("src/cli/   │
│  → DEFAULT_THEME            │  templates") → TEMPLATES       │
├─────────────────────────────────────────────────────────────┤
│  src/styles/default.yaml    │  src/cli/templates/*.jinja     │
└─────────────────────────────────────────────────────────────┘
```

## Stylesheets

Styles use a **three-layer architecture**:

### Layer 1: Visual (prefix `_`)
Concrete colors - the raw building blocks:
```yaml
_primary:
  light: { fg: black }
  dark: { fg: white }

_gold:
  light: { fg: [196, 140, 0] }
  dark: { fg: [255, 214, 10] }
```

### Layer 2: Presentation (prefix `_`)
Semantic aliases for visual consistency:
```yaml
_secondary: _gray
_accent: _gold
_danger: _red
```

### Layer 3: Semantic
Template-facing names - what templates actually use:
```yaml
title:
  bold: true
  light: { fg: black }
  dark: { fg: white }

list-index: _accent
error: { bold: true, ... }
```

### Style Properties
```yaml
style-name:
  fg: cyan              # Named color
  fg: [255, 128, 0]     # RGB array
  bg: black             # Background
  bold: true
  italic: true
  underline: true
  light: { ... }        # Light mode override
  dark: { ... }         # Dark mode override
```

### Adding a New Style
1. Define visual color in Layer 1 (if needed)
2. Add presentation alias in Layer 2 (if cross-cutting)
3. Define semantic name in Layer 3
4. Use in templates: `{{ value | style("style-name") }}`

## Templates

Templates use **Jinja2 syntax** (minijinja). Located in `src/cli/templates/`.

### Template Files
| File | Purpose |
|------|---------|
| `list.jinja` | Main list view (`padz list`) |
| `full_pad.jinja` | Detailed pad view (`padz view`) |
| `text_list.jinja` | Plain text list output |
| `messages.jinja` | Success/error messages |
| `_pad_line.jinja` | Partial: single pad row |
| `_deleted_help.jinja` | Partial: deleted section help |
| `_peek_content.jinja` | Partial: content preview |
| `_match_lines.jinja` | Partial: search match lines |

### Template Syntax
```jinja
{# Apply style to text #}
{{ pad.title | style("list-title") }}

{# Column layout with fixed width #}
{{ index | style("list-index") | col(4) }}

{# Conditionals #}
{% if pad.is_pinned %}{{ "⚲" | style("pinned") }}{% endif %}

{# Loops #}
{% for pad in pads %}
  {% include "_pad_line.jinja" %}
{% endfor %}

{# Include partials #}
{% include "_deleted_help.jinja" %}
```

### Key Filters
- `style("name")` - Apply named style
- `col(width)` - Fixed column width
- `col(width, align="right")` - Right-aligned column
- `truncate(length)` - Truncate with ellipsis

### Creating a New Template
1. Create `src/cli/templates/mytemplate.jinja`
2. Access via `TEMPLATES.get_content("mytemplate")`
3. Add to renderer in `render.rs`

## Debugging Output

Use `--output=term-debug` to see style tags:
```bash
padz list --output=term-debug
# Output: [pinned]⚲[/pinned] [list-index]p1.[/list-index]...
```

## Reference

See [references/current-stylesheet.yaml](references/current-stylesheet.yaml) for the complete current stylesheet with all styles defined.

## Code Locations

| Component | File |
|-----------|------|
| Stylesheet | `crates/padz/src/styles/default.yaml` |
| Templates | `crates/padz/src/cli/templates/` |
| Style loading | `crates/padz/src/cli/styles.rs` |
| Template loading | `crates/padz/src/cli/templates.rs` |
| Renderer setup | `crates/padz/src/cli/render.rs` |

## Common Tasks

### Change a color
Edit `src/styles/default.yaml`, find the style name, modify `fg`/`bg`/`bold`.

### Add bold to existing style
```yaml
existing-style:
  bold: true
  # ... keep other properties
```

### Change list layout
Edit `src/cli/templates/list.jinja` and `_pad_line.jinja`.

### Add new output field
1. Ensure data is in the render context (check `render.rs`)
2. Add to template: `{{ new_field | style("appropriate-style") }}`
