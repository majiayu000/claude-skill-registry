---
name: maud-components-patterns
description: Reusable component patterns for Maud including the Render trait, function components, parameterized components, layout composition, partials, and component organization. Use when building reusable UI elements, creating component libraries, structuring templates, or implementing design systems with type-safe components.
---

# Maud Component Patterns

*Production patterns for building reusable, type-safe HTML components with Maud*

## Version Context
- **Maud**: 0.27.0
- **Rust Edition**: 2021

## When to Use This Skill

- Creating reusable UI components
- Building component libraries
- Implementing design systems in Rust
- Structuring template code for maintainability
- Composing complex layouts from smaller pieces
- Building type-safe HTML abstractions

## The Render Trait

The `Render` trait is Maud's primary mechanism for type-safe component composition.

### Basic Render Implementation

```rust
use maud::{html, Markup, Render};

struct User {
    name: String,
    email: String,
    role: UserRole,
}

enum UserRole {
    Admin,
    User,
    Guest,
}

impl Render for User {
    fn render(&self) -> Markup {
        html! {
            div.user-card {
                h3.user-name { (self.name) }
                p.user-email { (self.email) }
                span.user-role {
                    @match self.role {
                        UserRole::Admin => span.badge.admin { "Admin" }
                        UserRole::User => span.badge.user { "User" }
                        UserRole::Guest => span.badge.guest { "Guest" }
                    }
                }
            }
        }
    }
}

// Usage: automatically calls render()
let user = User {
    name: "Alice".to_string(),
    email: "alice@example.com".to_string(),
    role: UserRole::Admin,
};

html! {
    div.user-list {
        (user)  // Renders the user card
    }
}
```

### Render Trait for Domain Types

```rust
use uuid::Uuid;

#[derive(Clone, Copy, Debug)]
struct UserId(Uuid);

impl UserId {
    fn new() -> Self {
        Self(Uuid::new_v4())
    }
}

impl Render for UserId {
    fn render(&self) -> Markup {
        html! {
            span.user-id data-id=(self.0.to_string()) {
                (self.0.to_string())
            }
        }
    }
}

// Usage in templates
html! {
    div.user-info {
        "User ID: " (user_id)
    }
}
```

## Function Components

Function components are pure functions that return `Markup`. They're the most common pattern for reusable components.

### Basic Function Component

```rust
fn button(text: &str, variant: &str) -> Markup {
    html! {
        button class=(format!("btn btn-{}", variant)) {
            (text)
        }
    }
}

// Usage
html! {
    div.actions {
        (button("Save", "primary"))
        (button("Cancel", "secondary"))
    }
}
```

### Parameterized Components

```rust
fn card(
    title: &str,
    description: &str,
    image_url: Option<&str>,
    highlighted: bool,
) -> Markup {
    html! {
        div.card[highlighted] {
            @if let Some(url) = image_url {
                img.card-image src=(url) alt=(title);
            }
            div.card-content {
                h3.card-title { (title) }
                p.card-description { (description) }
            }
        }
    }
}

// Usage
html! {
    div.grid {
        (card(
            "Product 1",
            "Description here",
            Some("/images/product1.jpg"),
            true
        ))
        (card(
            "Product 2",
            "Another description",
            None,
            false
        ))
    }
}
```

### Components with Closures (Content Slots)

```rust
fn modal(title: &str, content: Markup) -> Markup {
    html! {
        div.modal {
            div.modal-overlay {}
            div.modal-content {
                header.modal-header {
                    h2 { (title) }
                    button.close-btn aria-label="Close" { "×" }
                }
                div.modal-body {
                    (content)
                }
            }
        }
    }
}

// Usage with nested content
html! {
    (modal("Confirm Action", html! {
        p { "Are you sure you want to proceed?" }
        div.modal-actions {
            button.btn-primary { "Confirm" }
            button.btn-secondary { "Cancel" }
        }
    }))
}
```

## Layout Patterns

### Base Layout

```rust
use maud::{DOCTYPE, html, Markup};

fn base_layout(
    title: &str,
    description: Option<&str>,
    content: Markup,
) -> Markup {
    html! {
        (DOCTYPE)
        html lang="en" {
            head {
                meta charset="UTF-8";
                meta name="viewport" content="width=device-width, initial-scale=1.0";
                title { (title) }

                @if let Some(desc) = description {
                    meta name="description" content=(desc);
                }

                link rel="stylesheet" href="/static/styles.css";
                script src="https://unpkg.com/htmx.org@2.0.0" {}
            }
            body {
                (content)
            }
        }
    }
}
```

### Layout with Header/Footer

```rust
fn page_layout(
    title: &str,
    current_page: &str,
    content: Markup,
) -> Markup {
    base_layout(
        title,
        None,
        html! {
            (header(current_page))
            main.container {
                (content)
            }
            (footer())
        }
    )
}

fn header(current_page: &str) -> Markup {
    html! {
        header.site-header {
            nav.navbar {
                a.logo href="/" { "MyApp" }
                div.nav-links {
                    (nav_link("/", "Home", current_page))
                    (nav_link("/about", "About", current_page))
                    (nav_link("/blog", "Blog", current_page))
                    (nav_link("/contact", "Contact", current_page))
                }
            }
        }
    }
}

fn footer() -> Markup {
    html! {
        footer.site-footer {
            p { "© 2025 MyApp. All rights reserved." }
            div.footer-links {
                a href="/privacy" { "Privacy" }
                a href="/terms" { "Terms" }
            }
        }
    }
}
```

### Authenticated Layout

```rust
fn authenticated_layout(
    user: &User,
    page_title: &str,
    content: Markup,
) -> Markup {
    base_layout(
        page_title,
        None,
        html! {
            header.authenticated-header {
                nav {
                    a.logo href="/dashboard" { "Dashboard" }
                    div.user-menu {
                        span.user-name { (user.name) }
                        a href="/profile" { "Profile" }
                        a href="/settings" { "Settings" }
                        form method="POST" action="/logout" {
                            button.btn-link { "Logout" }
                        }
                    }
                }
            }
            main {
                (content)
            }
        }
    )
}
```

## Common UI Components

### Navigation Link with Active State

```rust
fn nav_link(href: &str, text: &str, current_path: &str) -> Markup {
    let is_active = current_path == href || current_path.starts_with(href);

    html! {
        a.nav-link[is_active] href=(href) {
            (text)
        }
    }
}
```

### Form Field with Error

```rust
fn text_field(
    name: &str,
    label: &str,
    value: Option<&str>,
    error: Option<&str>,
    required: bool,
) -> Markup {
    html! {
        div.form-group[error.is_some()] {
            label for=(name) {
                (label)
                @if required {
                    span.required { "*" }
                }
            }
            input
                type="text"
                name=(name)
                id=(name)
                value=[value]
                required[required];

            @if let Some(err) = error {
                span.error-message { (err) }
            }
        }
    }
}

// Usage
html! {
    form method="POST" {
        (text_field("email", "Email Address", None, None, true))
        (text_field("name", "Full Name", Some("John"), Some("Name is required"), true))
    }
}
```

### Select Dropdown

```rust
fn select_field<T: AsRef<str>>(
    name: &str,
    label: &str,
    options: &[(T, T)],  // (value, display_text)
    selected: Option<&str>,
) -> Markup {
    html! {
        div.form-group {
            label for=(name) { (label) }
            select name=(name) id=(name) {
                @for (value, text) in options {
                    option
                        value=(value.as_ref())
                        selected[selected == Some(value.as_ref())]
                    {
                        (text.as_ref())
                    }
                }
            }
        }
    }
}

// Usage
let roles = vec![
    ("admin", "Administrator"),
    ("user", "Regular User"),
    ("guest", "Guest"),
];

html! {
    (select_field("role", "User Role", &roles, Some("user")))
}
```

### Alert/Message Box

```rust
enum AlertVariant {
    Info,
    Success,
    Warning,
    Error,
}

impl AlertVariant {
    fn class(&self) -> &'static str {
        match self {
            AlertVariant::Info => "alert-info",
            AlertVariant::Success => "alert-success",
            AlertVariant::Warning => "alert-warning",
            AlertVariant::Error => "alert-error",
        }
    }

    fn icon(&self) -> &'static str {
        match self {
            AlertVariant::Info => "ℹ",
            AlertVariant::Success => "✓",
            AlertVariant::Warning => "⚠",
            AlertVariant::Error => "✕",
        }
    }
}

fn alert(variant: AlertVariant, message: &str, dismissible: bool) -> Markup {
    html! {
        div.alert class=(variant.class()) role="alert" {
            span.alert-icon { (variant.icon()) }
            span.alert-message { (message) }
            @if dismissible {
                button.alert-close aria-label="Close" { "×" }
            }
        }
    }
}

// Usage
html! {
    (alert(AlertVariant::Success, "User created successfully!", true))
    (alert(AlertVariant::Error, "Failed to save changes", false))
}
```

### Card Component

```rust
fn card_with_actions(
    title: &str,
    content: Markup,
    actions: Vec<(&str, &str)>,  // (text, href)
) -> Markup {
    html! {
        div.card {
            div.card-header {
                h3 { (title) }
            }
            div.card-body {
                (content)
            }
            div.card-footer {
                @for (text, href) in actions {
                    a.card-action href=(href) { (text) }
                }
            }
        }
    }
}

// Usage
html! {
    (card_with_actions(
        "User Profile",
        html! {
            p { "Name: Alice Johnson" }
            p { "Email: alice@example.com" }
        },
        vec![
            ("Edit", "/users/1/edit"),
            ("Delete", "/users/1/delete"),
        ]
    ))
}
```

### Table Component

```rust
fn table<T>(
    headers: &[&str],
    rows: &[T],
    render_row: impl Fn(&T) -> Markup,
) -> Markup {
    html! {
        table.data-table {
            thead {
                tr {
                    @for header in headers {
                        th { (header) }
                    }
                }
            }
            tbody {
                @for row in rows {
                    (render_row(row))
                }
            }
        }
    }
}

// Usage
struct Product {
    id: u64,
    name: String,
    price: f64,
}

let products = vec![
    Product { id: 1, name: "Widget".to_string(), price: 19.99 },
    Product { id: 2, name: "Gadget".to_string(), price: 29.99 },
];

html! {
    (table(
        &["ID", "Name", "Price", "Actions"],
        &products,
        |product| html! {
            tr {
                td { (product.id) }
                td { (product.name) }
                td { "$" (product.price) }
                td {
                    a href={"/products/" (product.id)} { "View" }
                }
            }
        }
    ))
}
```

### Pagination Component

```rust
fn pagination(current_page: u32, total_pages: u32, base_url: &str) -> Markup {
    html! {
        nav.pagination aria-label="Pagination" {
            @if current_page > 1 {
                a.page-link href={(base_url) "?page=" (current_page - 1)} {
                    "← Previous"
                }
            } @else {
                span.page-link.disabled { "← Previous" }
            }

            span.page-info {
                "Page " (current_page) " of " (total_pages)
            }

            @if current_page < total_pages {
                a.page-link href={(base_url) "?page=" (current_page + 1)} {
                    "Next →"
                }
            } @else {
                span.page-link.disabled { "Next →" }
            }
        }
    }
}
```

### Breadcrumb Navigation

```rust
struct Breadcrumb {
    label: String,
    href: Option<String>,
}

fn breadcrumbs(items: &[Breadcrumb]) -> Markup {
    html! {
        nav.breadcrumbs aria-label="Breadcrumb" {
            ol.breadcrumb-list {
                @for (i, item) in items.iter().enumerate() {
                    li.breadcrumb-item[i == items.len() - 1] {
                        @if let Some(href) = &item.href {
                            a href=(href) { (item.label) }
                        } @else {
                            span { (item.label) }
                        }

                        @if i < items.len() - 1 {
                            span.breadcrumb-separator { "/" }
                        }
                    }
                }
            }
        }
    }
}

// Usage
let crumbs = vec![
    Breadcrumb { label: "Home".to_string(), href: Some("/".to_string()) },
    Breadcrumb { label: "Products".to_string(), href: Some("/products".to_string()) },
    Breadcrumb { label: "Widget".to_string(), href: None },
];

html! {
    (breadcrumbs(&crumbs))
}
```

## Component Organization

### File Structure

```
src/
├── main.rs
├── routes/
│   ├── mod.rs
│   ├── home.rs
│   ├── users.rs
│   └── products.rs
├── templates/
│   ├── mod.rs
│   ├── layouts/
│   │   ├── mod.rs
│   │   ├── base.rs
│   │   ├── authenticated.rs
│   │   └── guest.rs
│   ├── components/
│   │   ├── mod.rs
│   │   ├── forms.rs
│   │   ├── navigation.rs
│   │   ├── cards.rs
│   │   └── tables.rs
│   └── pages/
│       ├── mod.rs
│       ├── home.rs
│       ├── about.rs
│       └── error.rs
```

### Module Organization (templates/mod.rs)

```rust
pub mod layouts;
pub mod components;
pub mod pages;

// Re-export commonly used items
pub use layouts::{base_layout, authenticated_layout};
pub use components::forms::{text_field, select_field};
pub use components::navigation::{nav_link, breadcrumbs};
```

### Component Module (templates/components/forms.rs)

```rust
use maud::{html, Markup};

pub fn text_field(
    name: &str,
    label: &str,
    value: Option<&str>,
    error: Option<&str>,
) -> Markup {
    html! {
        div.form-group {
            label for=(name) { (label) }
            input type="text" name=(name) id=(name) value=[value];
            @if let Some(err) = error {
                span.error { (err) }
            }
        }
    }
}

pub fn submit_button(text: &str, disabled: bool) -> Markup {
    html! {
        button.btn.btn-primary type="submit" disabled[disabled] {
            (text)
        }
    }
}
```

## Advanced Patterns

### Component Builder Pattern

```rust
pub struct CardBuilder {
    title: String,
    content: Markup,
    footer: Option<Markup>,
    variant: Option<String>,
}

impl CardBuilder {
    pub fn new(title: impl Into<String>) -> Self {
        Self {
            title: title.into(),
            content: html! {},
            footer: None,
            variant: None,
        }
    }

    pub fn content(mut self, content: Markup) -> Self {
        self.content = content;
        self
    }

    pub fn footer(mut self, footer: Markup) -> Self {
        self.footer = Some(footer);
        self
    }

    pub fn variant(mut self, variant: impl Into<String>) -> Self {
        self.variant = Some(variant.into());
        self
    }

    pub fn build(self) -> Markup {
        html! {
            div.card class=[self.variant] {
                div.card-header {
                    h3 { (self.title) }
                }
                div.card-body {
                    (self.content)
                }
                @if let Some(footer) = self.footer {
                    div.card-footer {
                        (footer)
                    }
                }
            }
        }
    }
}

// Usage
html! {
    (CardBuilder::new("User Profile")
        .content(html! { p { "User details here" } })
        .footer(html! { button { "Edit" } })
        .variant("highlighted")
        .build())
}
```

### Generic Component with Type Parameters

```rust
fn list<T>(items: &[T], render_item: impl Fn(&T) -> Markup) -> Markup {
    html! {
        ul.item-list {
            @for item in items {
                li.list-item {
                    (render_item(item))
                }
            }
        }
    }
}

// Usage
let users = vec!["Alice", "Bob", "Charlie"];

html! {
    (list(&users, |name| html! {
        span.user-name { (name) }
    }))
}
```

### Conditional Component Rendering

```rust
fn render_if(condition: bool, component: impl FnOnce() -> Markup) -> Markup {
    if condition {
        component()
    } else {
        html! {}
    }
}

// Usage
html! {
    div {
        (render_if(user.is_admin(), || {
            html! {
                button.admin-panel { "Admin Panel" }
            }
        }))
    }
}
```

## Best Practices

1. **Keep components pure**: Components should be functions without side effects
2. **Use descriptive names**: `user_profile_card` not `card1`
3. **Parameterize behavior**: Use function parameters for variations, not duplication
4. **Compose from small pieces**: Build complex components from simpler ones
5. **Type safety**: Use enums for variants instead of strings when possible
6. **Organize by domain**: Group related components together
7. **Document parameters**: Add doc comments for complex component signatures

## Component Design Guidelines

### Good Component Design

```rust
// ✅ Good: Type-safe, explicit parameters
fn button(text: &str, variant: ButtonVariant, disabled: bool) -> Markup {
    html! {
        button.btn class=(variant.class()) disabled[disabled] {
            (text)
        }
    }
}

enum ButtonVariant {
    Primary,
    Secondary,
    Danger,
}

impl ButtonVariant {
    fn class(&self) -> &'static str {
        match self {
            ButtonVariant::Primary => "btn-primary",
            ButtonVariant::Secondary => "btn-secondary",
            ButtonVariant::Danger => "btn-danger",
        }
    }
}
```

### Poor Component Design

```rust
// ❌ Bad: Stringly-typed, unclear parameters
fn button(text: &str, class: &str, attrs: &str) -> Markup {
    html! {
        button class=(class) (PreEscaped(attrs)) {
            (text)
        }
    }
}
```

## References

- **Maud Docs**: https://maud.lambda.xyz
- **Render Trait**: https://docs.rs/maud/latest/maud/trait.Render.html
- **Component Patterns**: Production patterns from MASH/HARM stack projects
