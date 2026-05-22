---
name: maud-syntax-fundamentals
description: Compile-time HTML templating with Maud using the html! macro for type-safe markup generation. Covers syntax patterns including elements, attributes, classes, IDs, content splicing, toggles, control flow (if/match/for), and DOCTYPE. Use when generating HTML in Rust, creating templates, or building server-side rendered pages.
---

# Maud Syntax Fundamentals

*Compile-time HTML templating for Rust with type safety and zero runtime overhead*

## Version Context
- **Maud**: 0.27.0 (latest stable)
- **Rust Edition**: 2021
- **Runtime**: ~100 SLoC (minimal overhead)

## When to Use This Skill

- Generating HTML from Rust code
- Building server-side rendered templates
- Creating type-safe HTML components
- Working with the `html!` macro
- Replacing runtime templating engines (Tera, Handlebars)
- Email template generation
- RSS/Atom feed generation

## Core Philosophy

1. **Compile-time validation** - Template errors caught by rustc, not at runtime
2. **Type safety** - Leverages Rust's type system for HTML generation
3. **Zero overhead** - Templates compile to optimized Rust code
4. **Auto-escaping** - All text content is HTML-escaped by default
5. **No external dependencies** - Everything links into your binary

## Syntax Formula

```
ELEMENT[.CLASS][#ID][ ATTRIBUTES] { CONTENT }
```

**Key Symbols:**
- `{}` = Container elements with content
- `;` = Void/self-closing elements
- `()` = Runtime value splicing (escaped)
- `[]` = Conditional attributes/classes (toggles)
- `@` = Control flow (if, match, for, while, let)

## Elements

### Container Elements

```rust
use maud::html;

html! {
    h1 { "Hello, world!" }
    p { "Paragraph text" }
    div { span { "Nested content" } }
    article {
        h2 { "Title" }
        p { "Content goes here" }
    }
}
```

### Void Elements (Self-Closing)

```rust
html! {
    br;
    hr;
    input type="text" name="email";
    img src="photo.jpg" alt="Description";
    link rel="stylesheet" href="styles.css";
    meta charset="UTF-8";
}
```

**Important**: Terminate with `;` - renders as `<br>` not `<br />`

### DOCTYPE Declaration

```rust
use maud::{html, DOCTYPE};

html! {
    (DOCTYPE)
    html lang="en" {
        head {
            meta charset="UTF-8";
            title { "My Page" }
        }
        body {
            h1 { "Content" }
        }
    }
}
```

## Classes and IDs

### Classes (Chainable)

```rust
html! {
    div.container { }
    div.row.justify-center { }
    p.text-lg.font-bold { "Styled text" }

    // Quoted for special characters (hyphens, numbers)
    div."col-sm-2" { }
    div."bg-blue-500" { }
}
```

### IDs (Space Required in Rust 2021+)

```rust
html! {
    div #main { }              // ✅ Rust 2021+
    section #content { }
    article #"post-123" { }    // Quoted for hyphens/numbers
}

// ❌ Error in Rust 2021+
// div#main { }  // Missing space before #
```

### Implicit Divs

```rust
html! {
    #header { }           // <div id="header">
    .container { }        // <div class="container">
    .card.shadow { }      // <div class="card shadow">
}
```

## Attributes

### Standard Attributes

```rust
html! {
    a href="https://example.com" title="Link" { "Click here" }
    input type="text" placeholder="Enter name" name="username";
    img src="photo.jpg" alt="Description" width="300";
}
```

### Boolean Attributes

```rust
html! {
    input type="checkbox" checked;
    input type="text" disabled;
    option value="1" selected;
    script src="app.js" defer;
    video controls autoplay;
}
```

### Data Attributes and ARIA

```rust
html! {
    article data-id="12345" data-category="tech" {
        h2 { "Article Title" }
    }

    button
        aria-label="Close dialog"
        aria-pressed="true"
        role="button"
    {
        "Close"
    }
}
```

### Custom Elements

```rust
html! {
    tag-cloud { }
    custom-widget data-id="123" {
        "Custom content"
    }
}
```

## Dynamic Content (Splices)

### Basic Splicing

```rust
let name = "Alice";
let count = 42;

html! {
    p { "Hello, " (name) "!" }        // Hello, Alice!
    p { "Count: " (count) }            // Count: 42
}
```

**Important**: Values in `()` are automatically HTML-escaped

### Expression Blocks

```rust
html! {
    p {
        "Result: "
        ({
            let x = 10;
            let y = 20;
            x + y
        })
    }
    // Outputs: Result: 30
}
```

### Attribute Splicing

```rust
let url = "https://example.com";
let id = "post-123";

html! {
    a href=(url) { "Link" }
    div id=(id) { "Content" }
}
```

### Multiple Values in Attributes

```rust
let base_url = "https://example.com";
let path = "/page";

html! {
    a href={ (base_url) (path) } { "Link" }
    // Outputs: href="https://example.com/page"
}
```

### Class and ID Splicing

```rust
let class_name = "active";
let element_id = "main-section";

html! {
    // Class splicing (two equivalent forms)
    div.(class_name) { "Content" }
    div class=(class_name) { "Content" }

    // ID splicing
    section #(element_id) { "Content" }
}
```

## Raw HTML (PreEscaped)

```rust
use maud::PreEscaped;

html! {
    div {
        // Auto-escaped (safe)
        p { "Hello <world>" }  // Outputs: Hello &lt;world&gt;

        // Raw HTML (dangerous - use with caution)
        (PreEscaped("<strong>Bold text</strong>"))
    }
}
```

**Security Warning**: Only use `PreEscaped` with trusted, sanitized content. Never use with user input.

## Toggles (Conditional Rendering)

### Boolean Attributes

```rust
let is_checked = true;
let is_disabled = false;

html! {
    input type="checkbox" checked[is_checked];
    button disabled[is_disabled] { "Submit" }
}
```

### Conditional Classes

```rust
let is_active = true;
let has_error = false;

html! {
    div.base-class[is_active].error[has_error] { }
    // Renders: <div class="base-class active">
}
```

### Optional Attributes

```rust
let maybe_title: Option<String> = Some("Tooltip".to_string());
let no_title: Option<String> = None;

html! {
    button title=[maybe_title] { "Hover" }
    // Renders: <button title="Tooltip">

    button title=[no_title] { "No tooltip" }
    // Renders: <button> (attribute completely omitted)
}
```

## Control Flow

### If/Else Conditionals

```rust
let logged_in = true;

html! {
    @if logged_in {
        p { "Welcome back!" }
    } @else {
        p { "Please log in" }
    }
}
```

### If Let (Pattern Matching)

```rust
let user: Option<User> = Some(User { name: "Alice".to_string() });

html! {
    @if let Some(user) = &user {
        p { "Hello, " (user.name) }
    } @else {
        p { "Guest" }
    }
}
```

### Match Expressions

```rust
enum Status { Active, Pending, Inactive }
let status = Status::Active;

html! {
    @match status {
        Status::Active => {
            span.badge.green { "Active" }
        }
        Status::Pending => {
            span.badge.yellow { "Pending" }
        }
        Status::Inactive => {
            span.badge.gray { "Inactive" }
        }
    }
}
```

### For Loops

```rust
let items = vec!["Apple", "Banana", "Cherry"];

html! {
    ul {
        @for item in &items {
            li { (item) }
        }
    }
}
```

### For Loop with Index

```rust
html! {
    ol {
        @for (i, item) in items.iter().enumerate() {
            li { (i + 1) ". " (item) }
        }
    }
}
```

### While Loops

```rust
let mut count = 0;

html! {
    @while count < 5 {
        p { "Count: " (count) }
        ({ count += 1; })
    }
}
```

### Let Bindings

```rust
html! {
    @let user_name = "Alice";
    @let greeting = format!("Hello, {}", user_name);

    h1 { (greeting) }

    @for i in 0..3 {
        @let doubled = i * 2;
        p { (i) " × 2 = " (doubled) }
    }
}
```

## Common Patterns

### Navigation Link with Active State

```rust
fn nav_link(href: &str, text: &str, is_current: bool) -> Markup {
    html! {
        a.nav-link[is_current] href=(href) { (text) }
    }
}
```

### Conditional Error Message

```rust
fn form_field(name: &str, error: Option<&str>) -> Markup {
    html! {
        div.form-group {
            input type="text" name=(name);
            @if let Some(err) = error {
                span.error { (err) }
            }
        }
    }
}
```

### List Rendering

```rust
fn render_list(items: &[String]) -> Markup {
    html! {
        ul {
            @for item in items {
                li { (item) }
            }
        }
    }
}
```

## Type Conversion

### Rendering Custom Types

Any type implementing `Display` can be spliced:

```rust
struct UserId(u64);

impl std::fmt::Display for UserId {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

let id = UserId(123);
html! {
    p { "User ID: " (id) }
}
```

## Common Gotchas

### Missing Space Before ID (Rust 2021+)

```rust
// ❌ Error
html! {
    div#myid { }
}

// ✅ Correct
html! {
    div #myid { }
}
```

### Unescaped HTML

```rust
// ❌ Wrong - outputs escaped HTML entities
html! {
    { "<b>Bold</b>" }
}
// Outputs: &lt;b&gt;Bold&lt;/b&gt;

// ✅ Correct - renders as HTML
use maud::PreEscaped;
html! {
    (PreEscaped("<b>Bold</b>"))
}
// Outputs: <b>Bold</b>
```

### Type Inference Issues

```rust
// ❌ May fail - compiler can't infer type
let items = vec![];

html! {
    @for item in &items {
        li { (item) }
    }
}

// ✅ Correct - explicit type
let items: Vec<String> = vec![];
```

## Performance Characteristics

1. **Compile-time**: Templates compile to optimized Rust code
2. **Zero allocations**: Static strings embedded in binary
3. **Minimal runtime**: ~100 SLoC runtime library
4. **No parsing**: No template parsing at runtime
5. **Type-safe**: Compiler validates all markup

## Conversion from String-Based Templates

```rust
// ❌ Runtime template (Tera, Handlebars)
// template.html: <h1>{{ title }}</h1>
// context.insert("title", &title);
// tera.render("template.html", &context)?

// ✅ Compile-time template (Maud)
html! {
    h1 { (title) }
}
```

## Integration with Rust Types

```rust
use serde::Serialize;

#[derive(Serialize)]
struct Post {
    id: u64,
    title: String,
    published: bool,
}

let post = Post {
    id: 1,
    title: "Hello".to_string(),
    published: true,
};

html! {
    article data-id=(post.id) {
        h2 { (post.title) }
        @if post.published {
            span.badge { "Published" }
        }
    }
}
```

## Best Practices

1. **Always escape user input** - Use `()` for splicing, never `PreEscaped` with untrusted data
2. **Use `@let` for complex expressions** - Improves readability
3. **Prefer pattern matching** - Use `@match` over nested `@if`
4. **Explicit types** - Specify types for collections to avoid inference issues
5. **Small, focused functions** - Break complex templates into reusable functions

## Key Advantages Over Runtime Templates

| Feature | Maud | Tera/Handlebars |
|---------|------|-----------------|
| Compile-time validation | ✅ Yes | ❌ No |
| Type safety | ✅ Yes | ❌ No |
| Runtime overhead | ✅ Minimal (~100 SLoC) | ❌ Large |
| Template hot-reload | ❌ No* | ✅ Yes |
| Learning curve | Medium | Easy |
| Binary size | ✅ Smallest | Larger |

*Can be achieved with shared library reloading in development

## References

- **Official Docs**: https://maud.lambda.xyz
- **API Docs**: https://docs.rs/maud
- **Crates.io**: https://crates.io/crates/maud
