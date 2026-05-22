---
name: frontend-htmx
description: |
  Axum + Askama + HTMX stack for single-binary web apps.
  Use when: building server-rendered UI, lightweight frontends, single deployable binary.
  Triggers: "htmx", "askama", "templates", "server-rendered", "single binary frontend".
---

# Frontend: Axum + Askama + HTMX

Single binary web apps. No node_modules, no build pipeline.

## Why This Stack

| Feature | Benefit |
|---------|---------|
| **Askama** | Templates compile into binary, type-checked |
| **HTMX** | 14kb, no JS build, hypermedia-driven |
| **Single binary** | `cargo build --release` → deploy anywhere |

## Dependencies

```toml
# Cargo.toml additions for HTMX frontend
[dependencies]
askama = "0.12"
askama_axum = "0.4"
axum-htmx = "0.6"              # HTMX header extractors
tower-http = { version = "0.6", features = ["fs"] }  # Static files (dev only)

# HTMX served from CDN or embedded
# https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js
```

## Project Structure

```
src/
├── lib.rs                 # API + create_app()
├── main.rs                # Server entry
├── error.rs               # AppError
└── templates/
    ├── mod.rs             # Template structs
    ├── base.html          # Layout with HTMX
    ├── pages/
    │   ├── index.html     # Home page
    │   └── notes.html     # Notes list page
    └── partials/
        ├── note_item.html # Single note (for HTMX swap)
        ├── note_list.html # Notes list partial
        └── note_form.html # Create/edit form
templates/                 # Askama looks here by default
└── (symlink to src/templates or copy)
```

## Base Template

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}App{% endblock %}</title>
    <script src="https://unpkg.com/htmx.org@2.0.4"></script>
    <style>
        /* Minimal CSS - extend as needed */
        body { font-family: system-ui; max-width: 800px; margin: 0 auto; padding: 1rem; }
        .htmx-request { opacity: 0.5; }
    </style>
    {% block head %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

## Template Structs (Askama)

```rust
// src/templates/mod.rs
use askama::Template;

#[derive(Template)]
#[template(path = "pages/index.html")]
pub struct IndexTemplate {
    pub title: String,
}

#[derive(Template)]
#[template(path = "pages/notes.html")]
pub struct NotesPageTemplate {
    pub notes: Vec<Note>,
}

#[derive(Template)]
#[template(path = "partials/note_item.html")]
pub struct NoteItemTemplate {
    pub note: Note,
}

#[derive(Template)]
#[template(path = "partials/note_list.html")]
pub struct NoteListTemplate {
    pub notes: Vec<Note>,
}

#[derive(Template)]
#[template(path = "partials/note_form.html")]
pub struct NoteFormTemplate {
    pub note: Option<Note>,  // None for create, Some for edit
}
```

## Page Template

```html
<!-- templates/pages/notes.html -->
{% extends "base.html" %}

{% block title %}Notes{% endblock %}

{% block content %}
<h1>Notes</h1>

<!-- Form: POST creates note, swaps into list -->
<form hx-post="/notes"
      hx-target="#notes-list"
      hx-swap="afterbegin"
      hx-on::after-request="this.reset()">
    <input type="text" name="title" placeholder="Title" required>
    <input type="text" name="content" placeholder="Content" required>
    <button type="submit">Add</button>
</form>

<!-- Notes list container -->
<div id="notes-list" hx-get="/notes/list" hx-trigger="load">
    Loading...
</div>
{% endblock %}
```

## Partial Templates

```html
<!-- templates/partials/note_item.html -->
<div id="note-{{ note.id }}" class="note">
    <strong>{{ note.title }}</strong>
    <p>{{ note.content }}</p>
    <button hx-delete="/notes/{{ note.id }}"
            hx-target="#note-{{ note.id }}"
            hx-swap="outerHTML">
        Delete
    </button>
</div>
```

```html
<!-- templates/partials/note_list.html -->
{% for note in notes %}
{% include "partials/note_item.html" %}
{% endfor %}
{% if notes.is_empty() %}
<p>No notes yet.</p>
{% endif %}
```

## Handlers

```rust
// src/lib.rs
use askama::Template;
use askama_axum::IntoResponse;
use axum::{
    extract::{Path, State},
    http::StatusCode,
    response::Html,
    routing::{delete, get, post},
    Form, Router,
};
use axum_htmx::HxRequest;

// Page handler - returns full HTML page
pub async fn notes_page() -> impl IntoResponse {
    NotesPageTemplate { notes: vec![] }
}

// Partial handler - returns HTML fragment for HTMX
pub async fn notes_list(State(db): State<AppState>) -> impl IntoResponse {
    let notes = db.get_all_notes().await;
    NoteListTemplate { notes }
}

// Create handler - returns new item partial
pub async fn create_note(
    State(db): State<AppState>,
    Form(input): Form<CreateNote>,
) -> impl IntoResponse {
    let note = db.create_note(input).await;
    (StatusCode::CREATED, NoteItemTemplate { note })
}

// Delete handler - returns empty (HTMX removes element)
pub async fn delete_note(
    State(db): State<AppState>,
    Path(id): Path<i64>,
) -> impl IntoResponse {
    db.delete_note(id).await;
    StatusCode::OK
}

// Conditional: full page vs partial based on HX-Request header
pub async fn smart_notes(
    HxRequest(is_htmx): HxRequest,
    State(db): State<AppState>,
) -> impl IntoResponse {
    let notes = db.get_all_notes().await;
    if is_htmx {
        // HTMX request - return partial
        NoteListTemplate { notes }.into_response()
    } else {
        // Full page request
        NotesPageTemplate { notes }.into_response()
    }
}

pub fn create_app() -> Router<AppState> {
    Router::new()
        // Pages
        .route("/", get(notes_page))
        // Partials (HTMX targets)
        .route("/notes/list", get(notes_list))
        // API actions
        .route("/notes", post(create_note))
        .route("/notes/:id", delete(delete_note))
}
```

## HTMX Patterns

### Swap Strategies

| Pattern | `hx-swap` | Use Case |
|---------|-----------|----------|
| Replace content | `innerHTML` (default) | Update container |
| Replace element | `outerHTML` | Update item in list |
| Add to start | `afterbegin` | New items at top |
| Add to end | `beforeend` | New items at bottom |
| Delete | `delete` | Remove element |

### Common Attributes

```html
<!-- Load on page load -->
<div hx-get="/data" hx-trigger="load">Loading...</div>

<!-- Submit form, update target -->
<form hx-post="/items" hx-target="#list" hx-swap="afterbegin">

<!-- Delete with confirmation -->
<button hx-delete="/items/1"
        hx-confirm="Are you sure?"
        hx-target="closest .item"
        hx-swap="outerHTML">

<!-- Inline editing -->
<span hx-get="/items/1/edit" hx-trigger="click" hx-swap="outerHTML">
    Click to edit
</span>

<!-- Search with debounce -->
<input type="search"
       hx-get="/search"
       hx-trigger="keyup changed delay:300ms"
       hx-target="#results">

<!-- Infinite scroll -->
<div hx-get="/items?page=2"
     hx-trigger="revealed"
     hx-swap="afterend">
```

### Response Headers (axum-htmx)

```rust
use axum_htmx::{HxRedirect, HxRefresh, HxTrigger};

// Redirect after action
pub async fn logout() -> impl IntoResponse {
    (HxRedirect("/login".parse().unwrap()), StatusCode::OK)
}

// Trigger client-side event
pub async fn save() -> impl IntoResponse {
    (HxTrigger::normal("saved"), "OK")
}

// Refresh page
pub async fn reset() -> impl IntoResponse {
    HxRefresh(true)
}
```

## Testing HTMX

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use axum_test::TestServer;

    #[tokio::test]
    async fn test_notes_page_returns_html() {
        let app = create_app();
        let server = TestServer::new(app).unwrap();

        let response = server.get("/").await;

        response.assert_status_ok();
        response.assert_text_contains("<title>Notes</title>");
        response.assert_text_contains("hx-get");
    }

    #[tokio::test]
    async fn test_htmx_partial_returns_fragment() {
        let app = create_app();
        let server = TestServer::new(app).unwrap();

        let response = server
            .get("/notes/list")
            .add_header("HX-Request", "true")
            .await;

        response.assert_status_ok();
        // Should NOT contain full HTML structure
        assert!(!response.text().contains("<!DOCTYPE"));
    }

    #[tokio::test]
    async fn test_create_note_returns_partial() {
        let app = create_app();
        let server = TestServer::new(app).unwrap();

        let response = server
            .post("/notes")
            .form(&[("title", "Test"), ("content", "Content")])
            .await;

        response.assert_status(StatusCode::CREATED);
        response.assert_text_contains("Test");
    }
}
```

## Embedding HTMX (No CDN)

For true single-binary without external dependencies:

```rust
// Download htmx.min.js to src/static/htmx.min.js
// Then serve it embedded

use axum::response::Html;

const HTMX_JS: &str = include_str!("static/htmx.min.js");

pub async fn htmx_js() -> impl IntoResponse {
    (
        [("content-type", "application/javascript")],
        HTMX_JS,
    )
}

// Add route
.route("/static/htmx.js", get(htmx_js))

// Update base.html
<script src="/static/htmx.js"></script>
```

## Anti-patterns

| Don't | Do Instead |
|-------|------------|
| Full page reload on every action | Use HTMX partials |
| Complex JS state management | Keep state on server |
| Client-side routing | Server routes + HTMX |
| Manual DOM manipulation | Let HTMX handle swaps |
| Inline styles everywhere | CSS classes + minimal inline |
| `unwrap()` in template data | Handle errors before template |

## TDD for HTMX

```
1. tdd-test-writer: "test notes page returns HTML with hx-get"
2. rust-developer: implement page handler
3. tdd-test-writer: "test create note returns partial"
4. rust-developer: implement create handler
5. rust-code-reviewer: check all patterns
```

## Minimal Full Example

```rust
// src/main.rs - Complete minimal app
use askama::Template;
use axum::{routing::get, Router};

#[derive(Template)]
#[template(source = r#"
<!DOCTYPE html>
<html>
<head>
    <script src="https://unpkg.com/htmx.org@2.0.4"></script>
</head>
<body>
    <h1>{{ title }}</h1>
    <button hx-get="/click" hx-swap="outerHTML">Click me</button>
</body>
</html>
"#, ext = "html")]
struct IndexTemplate { title: String }

#[derive(Template)]
#[template(source = "<button hx-get=\"/click\" hx-swap=\"outerHTML\">Clicked {{ count }} times</button>", ext = "html")]
struct ButtonTemplate { count: i32 }

static COUNTER: std::sync::atomic::AtomicI32 = std::sync::atomic::AtomicI32::new(0);

async fn index() -> IndexTemplate {
    IndexTemplate { title: "HTMX Demo".into() }
}

async fn click() -> ButtonTemplate {
    let count = COUNTER.fetch_add(1, std::sync::atomic::Ordering::SeqCst) + 1;
    ButtonTemplate { count }
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(index))
        .route("/click", get(click));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    println!("Listening on http://localhost:3000");
    axum::serve(listener, app).await.unwrap();
}
```

Build: `cargo build --release` → 5-10MB binary with everything included.
