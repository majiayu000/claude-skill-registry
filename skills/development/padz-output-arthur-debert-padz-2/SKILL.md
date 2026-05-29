---
name: padz-output
description: |
  Guide for customizing padz CLI output: templates, styles, and rendering.
  Use when working on: (1) Modifying templates in crates/padz/src/cli/templates/,
  (2) Adding or changing styles in styles/default.yaml, (3) Debugging output with --output flag,
  (4) Adding new commands that need rendered output, (5) Understanding the outstanding crate integration.
---

# Padz Output Customization

## Architecture Overview

Padz uses a three-layer system for CLI output, much like web appl, wher the api returns a data object, and 
the rendering system (using outstanding create) uses file based templates (minijinja) + styles to render:

1. **Templates** (Minijinja `.jinja` files) - Define structure and layout
2. **Styles** (YAML stylesheet) - Define colors and formatting
3. **Renderer** (outstanding crate) - Combines templates + styles with output mode

## Quick Reference

### Output Modes (`--output` flag)

```bash
padz list --output=auto       # Default: colors for TTY, plain for pipes
padz list --output=term       # Force ANSI colors
padz list --output=text       # Plain text, no colors
padz list --output=term-debug # Debug: shows [style-name]text[/style-name]
padz list --output=json       # Machine-readable JSON
```

### Key Files

| Purpose | Location |
| --------- | ---------- |
| Templates | `crates/padz/src/cli/templates/*.jinja` |
| Template registry | `crates/padz/src/cli/templates.rs` |
| Stylesheet | `crates/padz/src/styles/default.yaml` |
| Theme loading | `crates/padz/src/cli/styles.rs` |
| Rendering logic | `crates/padz/src/cli/render.rs` |

## Templates

Templates use Minijinja syntax. Located in `crates/padz/src/cli/templates/`.

### Main Templates

- `list.jinja` - Pad list with columns, indentation, status icons
- `full_pad.jinja` - Complete pad view (title + content)
- `text_list.jinja` - Simple line-by-line output
- `messages.jinja` - Command feedback (success/error/info)

### Partial Templates (reusable)

- `_pad_line.jinja` - Single row in list (included by list.jinja)
- `_match_lines.jinja` - Search result highlighting
- `_peek_content.jinja` - Content preview for `--peek`
- `_deleted_help.jinja` - Help text for deleted section

### Template Syntax

```jinja
{#- Whitespace-trimming comment -#}
{% for pad in pads %}
  {{- pad.title | col(width) | style("list-title") | nl -}}
{% endfor %}
```

Key filters from outstanding:

- `col(width, align='left'|'right')` - Column layout
- `style("name")` - Apply semantic style
- `nl` - Explicit newline
- `truncate_to_width()` - Truncate with ellipsis
- `indent(n)` - Add indentation

### Adding a New Template

1. Create `.jinja` file in `templates/` directory
2. Register in `templates.rs`:

   ```rust
   pub const MY_TEMPLATE: &str = include_str!("templates/my_template.jinja");
   ```

3. Add to renderer in `create_renderer()`:

   ```rust
   renderer.add_template("my_template", MY_TEMPLATE)?;
   ```

4. Call from render function:

   ```rust
   renderer.render("my_template", &data)?
   ```

## Styles (YAML Stylesheet)

Styles are defined in `crates/padz/src/styles/default.yaml` and embedded at compile time.

### Three-Layer Architecture

```yaml
# Layer 1: Visual (internal, prefixed with _)
_gold:
  light:
    fg: [196, 140, 0]
  dark:
    fg: [255, 214, 10]

# Layer 2: Presentation (aliases)
_accent: _gold

# Layer 3: Semantic (use in templates)
list-index: _accent
pinned:
  bold: true
  light:
    fg: [196, 140, 0]
  dark:
    fg: [255, 214, 10]
```

### Semantic Styles (use in templates)

**List:** `list-index`, `list-title`, `pinned`, `deleted-index`, `deleted-title`, `status-icon`

**Content:** `title`, `time`, `hint`

**Messages:** `error`, `warning`, `success`, `info`

**Search:** `highlight`, `match`

**Help:** `help-header`, `help-section`, `help-command`, `help-desc`, `help-usage`

**Misc:** `help-text`, `section-header`, `empty-message`, `preview`, `truncation`, `line-number`, `separator`

### Adding a New Style

Add to `default.yaml`:

```yaml
# Simple alias
my-style: _accent

# With modifiers
my-style:
  bold: true
  italic: true
  light:
    fg: [196, 140, 0]
  dark:
    fg: [255, 214, 10]
```

Use in templates: `{{ value | style("my-style") }}`

### Style Embedding

Styles are embedded at compile time via `embed_styles!` macro:

```rust
pub static DEFAULT_THEME: Lazy<Theme> = Lazy::new(|| {
    let mut registry = embed_styles!("src/styles");
    registry.get("default").expect("Failed to load default theme")
});
```

## Column Layout

Constants in `render.rs`:

```rust
pub const LINE_WIDTH: usize = 100;
pub const COL_LEFT_PIN: usize = 2;
pub const COL_STATUS: usize = 2;
pub const COL_INDEX: usize = 4;
pub const COL_RIGHT_PIN: usize = 2;
pub const COL_TIME: usize = 14;
```

Title width: `LINE_WIDTH - fixed_columns - indent_width`

## JSON Output

For `--output=json`, data is serialized directly (bypasses templates).

JSON types in `render.rs`: `JsonPadList`, `JsonPad`, `JsonMessages`

## Debugging Output

Use `--output=term-debug` to see style names:

```text
[pinned]⚲[/pinned] [list-index]p1.[/list-index] [list-title]My Pad[/list-title]
```

## References

- [TEMPLATE_VARIABLES.md](references/TEMPLATE_VARIABLES.md) - Variables available in each template
- [STYLE_REFERENCE.md](references/STYLE_REFERENCE.md) - Complete style reference
