---
name: syntect
description: Syntax highlighting using Sublime Text definitions
tags: [rust, syntax-highlighting, parsing, themes]
---

# syntect

syntect is a syntax highlighting library for Rust that uses Sublime Text's `.sublime-syntax` grammar definitions. It provides high-quality syntax highlighting with support for themes and incremental parsing.

**Version**: 5.3.0  
**Docs**: https://docs.rs/syntect/latest/syntect/

## Key Types

### Parsing Module (`syntect::parsing`)

| Type | Description |
|------|-------------|
| `SyntaxSet` | Immutable collection of linked syntax definitions. Use `load_defaults_newlines()` for most cases. |
| `SyntaxReference` | Reference to a syntax within a SyntaxSet |
| `SyntaxSetBuilder` | Builder for creating custom SyntaxSets with additional syntaxes |
| `ParseState` | Mutable parser state for incremental parsing |

### Highlighting Module (`syntect::highlighting`)

| Type | Description |
|------|-------------|
| `ThemeSet` | Collection of themes. Use `load_defaults()` to get built-in themes. |
| `Theme` | A parsed `.tmTheme` file with colors and styles |
| `Style` | Foreground color, background color, and font style |
| `Color` | RGBA color struct with `r`, `g`, `b`, `a` fields |
| `FontStyle` | Bold, italic, underline flags |
| `Highlighter` | Wraps a Theme for highlighting operations |
| `HighlightState` | Maintains scope/style stack between lines |

### Easy Module (`syntect::easy`)

| Type | Description |
|------|-------------|
| `HighlightLines` | Simple API for line-by-line highlighting |
| `HighlightFile` | Convenience struct for highlighting entire files |

### Utility Module (`syntect::util`)

| Type | Description |
|------|-------------|
| `LinesWithEndings` | Iterator that preserves newlines (required for `load_defaults_newlines()`) |
| `as_24_bit_terminal_escaped()` | Convert highlighted ranges to ANSI escape codes |

## Usage in script-kit-gpui

syntect is used in `src/syntax.rs` for code syntax highlighting:

```rust
use syntect::easy::HighlightLines;
use syntect::highlighting::{Style, ThemeSet};
use syntect::parsing::SyntaxSet;
use syntect::util::LinesWithEndings;
```

### Key Implementation Details

1. **Theme**: Uses `base16-eighties.dark` theme for dark background compatibility
2. **TypeScript Handling**: Maps TypeScript to JavaScript syntax (TypeScript not in default SyntaxSet)
3. **Fallback Chain**: `find_syntax_by_name()` -> `find_syntax_by_extension()` -> JavaScript -> plain text
4. **Output Format**: Converts `Style.foreground` to `0xRRGGBB` hex u32 values

### Language Mapping

```rust
fn map_language_to_syntax(language: &str) -> &str {
    match language.to_lowercase().as_str() {
        "typescript" | "ts" => "JavaScript",  // TypeScript NOT in defaults
        "javascript" | "js" => "JavaScript",
        "markdown" | "md" => "Markdown",
        "json" => "JSON",
        "rust" | "rs" => "Rust",
        "python" | "py" => "Python",
        "html" => "HTML",
        "css" => "CSS",
        "shell" | "sh" | "bash" => "Bourne Again Shell (bash)",
        "yaml" | "yml" => "YAML",
        "toml" => "Makefile",  // TOML not in defaults either
        _ => language,
    }
}
```

## Highlighting Workflow

### Basic Line-by-Line Highlighting

```rust
use syntect::easy::HighlightLines;
use syntect::parsing::SyntaxSet;
use syntect::highlighting::ThemeSet;
use syntect::util::LinesWithEndings;

// 1. Load syntax and theme sets (do once, reuse)
let ps = SyntaxSet::load_defaults_newlines();
let ts = ThemeSet::load_defaults();

// 2. Find syntax and create highlighter
let syntax = ps.find_syntax_by_extension("rs").unwrap();
let theme = &ts.themes["base16-ocean.dark"];
let mut h = HighlightLines::new(syntax, theme);

// 3. Highlight line by line
let code = "fn main() { println!(\"Hello\"); }";
for line in LinesWithEndings::from(code) {
    let ranges: Vec<(Style, &str)> = h.highlight_line(line, &ps)?;
    // Process (style, text) pairs
    for (style, text) in ranges {
        let fg = style.foreground;
        let color = ((fg.r as u32) << 16) | ((fg.g as u32) << 8) | (fg.b as u32);
        // Use color and text...
    }
}
```

### Finding Syntaxes

```rust
let ps = SyntaxSet::load_defaults_newlines();

// By name (exact match)
ps.find_syntax_by_name("Rust");

// By extension
ps.find_syntax_by_extension("rs");

// By token (extension first, then case-insensitive name)
ps.find_syntax_by_token("rust");

// By first line (shebangs, mode lines)
ps.find_syntax_by_first_line("#!/usr/bin/env python");

// By file path (tries extension + first line)
ps.find_syntax_for_file("src/main.rs")?;

// Fallback to plain text
ps.find_syntax_plain_text();
```

## Theme Integration

### Default Themes

```rust
let ts = ThemeSet::load_defaults();
// Available keys:
// - "base16-ocean.dark"
// - "base16-eighties.dark"  <- Used by script-kit-gpui
// - "base16-mocha.dark"
// - "base16-ocean.light"
// - "InspiredGitHub"
// - "Solarized (dark)"
// - "Solarized (light)"

let theme = &ts.themes["base16-eighties.dark"];
```

### Loading Custom Themes

```rust
// Single theme from file
let theme = ThemeSet::get_theme("/path/to/theme.tmTheme")?;

// All themes from folder
let ts = ThemeSet::load_from_folder("/path/to/themes/")?;

// Add to existing set
let mut ts = ThemeSet::load_defaults();
ts.add_from_folder("/path/to/more/themes/")?;
```

### Theme Settings

```rust
let theme: &Theme = &ts.themes["base16-ocean.dark"];

// Editor UI colors
if let Some(bg) = theme.settings.background {
    // Use as editor background
}
if let Some(fg) = theme.settings.foreground {
    // Default text color
}
if let Some(sel) = theme.settings.selection {
    // Selection highlight color
}
if let Some(caret) = theme.settings.caret {
    // Cursor color
}
```

## Performance

### Loading Strategies

```rust
// FAST: Load pre-compiled binary dumps (~200KB each)
let ps = SyntaxSet::load_defaults_newlines();  // Recommended
let ts = ThemeSet::load_defaults();

// SLOW: Parse YAML files at runtime
let ps = SyntaxSet::load_from_folder("/path/to/syntaxes/")?;
```

### Caching & Reuse

```rust
// BAD: Loading on every highlight call
fn highlight_bad(code: &str, lang: &str) -> Vec<Span> {
    let ps = SyntaxSet::load_defaults_newlines();  // Expensive!
    let ts = ThemeSet::load_defaults();             // Expensive!
    // ...
}

// GOOD: Load once, reuse
struct Highlighter {
    ps: SyntaxSet,
    ts: ThemeSet,
}

impl Highlighter {
    fn new() -> Self {
        Self {
            ps: SyntaxSet::load_defaults_newlines(),
            ts: ThemeSet::load_defaults(),
        }
    }
    
    fn highlight(&self, code: &str, lang: &str) -> Vec<Span> {
        // Reuse self.ps and self.ts
    }
}
```

### Newlines Mode

```rust
// Use load_defaults_newlines() when:
// - Lines include trailing \n (most common)
// - Using LinesWithEndings iterator

// Use load_defaults_nonewlines() when:
// - Lines are pre-split without \n
// - Using .lines() iterator
```

### Incremental Highlighting

```rust
// For editors with cached state per line
let mut h = HighlightLines::new(syntax, theme);

// After highlighting, save state
let (highlight_state, parse_state) = h.state();

// Later, resume from saved state
let h = HighlightLines::from_state(theme, highlight_state, parse_state);
```

## Anti-patterns

### 1. Not Handling Missing Syntaxes

```rust
// BAD: Panics on unknown syntax
let syntax = ps.find_syntax_by_name("TypeScript").unwrap();

// GOOD: Fallback chain
let syntax = ps
    .find_syntax_by_name(lang)
    .or_else(|| ps.find_syntax_by_extension(lang))
    .unwrap_or_else(|| ps.find_syntax_plain_text());
```

### 2. Assuming TypeScript/TOML Exist

```rust
// BAD: TypeScript is NOT in default SyntaxSet
let syntax = ps.find_syntax_by_extension("ts");  // Returns None!

// GOOD: Map to JavaScript
let syntax = ps.find_syntax_by_name("JavaScript");
```

### 3. Ignoring Highlighting Errors

```rust
// BAD: Silently ignore errors
let ranges = h.highlight_line(line, &ps).unwrap_or_default();

// GOOD: Handle errors gracefully
match h.highlight_line(line, &ps) {
    Ok(ranges) => process_ranges(ranges),
    Err(_) => {
        // Fall back to plain text rendering
        vec![(default_style, line)]
    }
}
```

### 4. Wrong Newlines Mode

```rust
// BAD: Mismatched modes
let ps = SyntaxSet::load_defaults_newlines();
for line in code.lines() {  // .lines() strips \n!
    h.highlight_line(line, &ps);  // May produce incorrect results
}

// GOOD: Matching modes
let ps = SyntaxSet::load_defaults_newlines();
for line in LinesWithEndings::from(code) {  // Preserves \n
    h.highlight_line(line, &ps);
}
```

### 5. Thread Safety Issues

```rust
// NOTE: HighlightLines is !Send + !Sync
// Create per-thread instances, don't share across threads

// SyntaxSet and ThemeSet ARE Send + Sync
// Safe to share via Arc<SyntaxSet>
```

## Color Conversion

### Style to Hex

```rust
fn style_to_hex(style: &Style) -> u32 {
    let fg = style.foreground;
    ((fg.r as u32) << 16) | ((fg.g as u32) << 8) | (fg.b as u32)
}
```

### Color to RGBA

```rust
fn color_to_rgba(color: Color) -> (u8, u8, u8, u8) {
    (color.r, color.g, color.b, color.a)
}
```

### Color to CSS

```rust
fn color_to_css(color: Color) -> String {
    format!("rgba({}, {}, {}, {})", color.r, color.g, color.b, color.a as f32 / 255.0)
}
```

## Adding Custom Syntaxes

```rust
use syntect::parsing::SyntaxSetBuilder;

// Start from defaults
let mut builder = SyntaxSet::load_defaults_newlines().into_builder();

// Add custom syntaxes
builder.add_from_folder("/path/to/custom/syntaxes/", true)?;

// Build immutable set
let ps = builder.build();
```

## HTML Output

```rust
use syntect::html::{highlighted_html_for_string, ClassedHTMLGenerator};

// Inline styles
let html = highlighted_html_for_string(code, &ps, syntax, theme)?;

// CSS classes (for theming)
let mut gen = ClassedHTMLGenerator::new_with_class_style(
    syntax,
    &ps,
    ClassStyle::Spaced,
);
for line in LinesWithEndings::from(code) {
    gen.parse_html_for_line_which_includes_newline(line)?;
}
let html = gen.finalize();
```

## See Also

- [syntect GitHub](https://github.com/trishume/syntect)
- [Sublime Text Syntax Reference](https://www.sublimetext.com/docs/syntax.html)
- [TextMate Themes](https://tmtheme-editor.glitch.me/)
