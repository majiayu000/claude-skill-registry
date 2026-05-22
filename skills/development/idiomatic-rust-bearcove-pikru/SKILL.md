---
name: idiomatic-rust
description: Idiomatic Rust patterns for pikru C port. Use when writing or reviewing Rust code ported from C. Don't write C in Rust - the goal is correct behavior, not line-by-line translation.
---

# Idiomatic Rust: Don't port C patterns

This is a Rust port of C code, but **do not write C in Rust**. The goal is correct behavior, not line-by-line translation.

## Put logic where the data lives

If a struct has all the information needed to compute something, make it a method:

```rust
// BAD: C-style function with boolean flag soup
fn text_width(text: &str, charwid: f64, is_mono: bool, font_scale: f64, is_bold: bool) -> f64

// GOOD: The type already knows its properties
impl PositionedText {
    fn width_inches(&self, charwid: f64) -> f64 {
        // self.mono, self.bold, self.big are all right here
    }
}
```

**Rationale:** Boolean flags are:
- Easy to pass in wrong order (`width(s, w, true, 1.0, false)` - which bool is which?)
- Require the caller to extract properties just to pass them back in
- Duplicate knowledge that the type already has

## Use newtypes for domain concepts

```rust
// BAD: Bare f64 everywhere, easy to mix up inches and pixels
fn convert(value: f64, scale: f64) -> f64

// GOOD: The type system catches mistakes
struct Inches(f64);
struct Pixels(f64);
fn convert(value: Inches, scale: &Scaler) -> Pixels
```

## Prefer methods over standalone functions

When you find yourself writing `foo_bar(bar, ...)`, consider `bar.foo(...)` instead. This:
- Groups related functionality
- Enables IDE autocomplete on the type
- Makes the relationship between data and operations explicit

## Enums over boolean flags

```rust
// BAD: What does `true` mean here?
render_text(text, true, false)

// GOOD: Self-documenting
enum TextAnchor { Start, Middle, End }
render_text(text, TextAnchor::Start)
```

## The C code is a spec, not a template

When porting C:
1. Understand what the C code **does** (behavior)
2. Understand **why** it does it (intent)
3. Implement that behavior idiomatically in Rust

The `// cref:` comments link to C for reference, but the Rust should stand on its own.
