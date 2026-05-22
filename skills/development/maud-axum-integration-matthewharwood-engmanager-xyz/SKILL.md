---
name: maud-axum-integration
description: Production patterns for integrating Maud HTML templates with Axum 0.8.x web services. Covers IntoResponse implementation, handler patterns, state management with templates, error pages, layouts, and server-side rendering architecture. Use when building Axum HTTP endpoints that return HTML, creating web UIs, or implementing server-side rendered applications.
---

# Maud + Axum Integration

*Production patterns for server-side rendered HTML with Maud and Axum*

## Version Context
- **Maud**: 0.27.0 (with `axum` feature)
- **Axum**: 0.8.7
- **Tokio**: 1.48.0
- **Rust Edition**: 2021

## When to Use This Skill

- Building server-side rendered web applications with Axum
- Creating HTML endpoints in Axum routers
- Implementing layouts and page templates
- Rendering error pages with proper HTTP status codes
- Combining Axum state with Maud templates
- Building MASH/HARM stack applications (Maud + Axum + SQLx + HTMX)

## Setup

### Cargo.toml

```toml
[dependencies]
# Maud with Axum integration
maud = { version = "0.27", features = ["axum"] }

# Axum and runtime
axum = { version = "0.8", features = ["macros"] }
tokio = { version = "1", features = ["full"] }

# Tower middleware
tower = "0.5"
tower-http = { version = "0.6", features = ["trace", "compression", "fs"] }

# Serialization and errors
serde = { version = "1", features = ["derive"] }
thiserror = "2"
```

## Basic Integration

### Simple Handler Returning Markup

```rust
use axum::{routing::get, Router};
use maud::{html, Markup, DOCTYPE};

async fn index() -> Markup {
    html! {
        (DOCTYPE)
        html lang="en" {
            head {
                meta charset="UTF-8";
                title { "Hello Axum + Maud" }
            }
            body {
                h1 { "Hello from Axum and Maud!" }
                p { "Server-side rendered HTML" }
            }
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let app = Router::new().route("/", get(index));

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    axum::serve(listener, app).await?;

    Ok(())
}
```

**Key**: The `axum` feature enables `Markup` to implement `IntoResponse` automatically.

### Handler with State

```rust
use axum::{
    extract::State,
    routing::get,
    Router,
};
use maud::{html, Markup};
use std::sync::Arc;

#[derive(Clone)]
struct AppState {
    app_name: String,
    version: String,
}

async fn index(State(state): State<Arc<AppState>>) -> Markup {
    html! {
        (DOCTYPE)
        html {
            head {
                title { (state.app_name) }
            }
            body {
                h1 { (state.app_name) }
                p { "Version: " (state.version) }
            }
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let state = Arc::new(AppState {
        app_name: "My App".to_string(),
        version: "1.0.0".to_string(),
    });

    let app = Router::new()
        .route("/", get(index))
        .with_state(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    axum::serve(listener, app).await?;

    Ok(())
}
```

## Layout Pattern

### Base Layout Component

```rust
use maud::{html, Markup, DOCTYPE};

pub fn base_layout(title: &str, content: Markup) -> Markup {
    html! {
        (DOCTYPE)
        html lang="en" {
            head {
                meta charset="UTF-8";
                meta name="viewport" content="width=device-width, initial-scale=1.0";
                title { (title) }
                link rel="stylesheet" href="/static/styles.css";
                // Include HTMX for dynamic interactions
                script src="https://unpkg.com/htmx.org@2.0.0" {}
            }
            body {
                header {
                    nav.navbar {
                        a.nav-link href="/" { "Home" }
                        a.nav-link href="/about" { "About" }
                        a.nav-link href="/contact" { "Contact" }
                    }
                }

                main.container {
                    (content)
                }

                footer {
                    p { "© 2025 My Application" }
                }
            }
        }
    }
}

// Usage in handlers
async fn home_page() -> Markup {
    base_layout("Home", html! {
        h1 { "Welcome Home" }
        p { "This is the home page content" }
    })
}
```

### Layout with State

```rust
use axum::extract::State;
use std::sync::Arc;

pub fn authenticated_layout(
    user_name: &str,
    page_title: &str,
    content: Markup,
) -> Markup {
    html! {
        (DOCTYPE)
        html {
            head {
                title { (page_title) " - My App" }
                link rel="stylesheet" href="/static/styles.css";
            }
            body {
                header {
                    nav {
                        span { "Welcome, " (user_name) }
                        a href="/logout" { "Logout" }
                    }
                }
                main {
                    (content)
                }
            }
        }
    }
}

#[derive(Clone)]
struct AppState {
    current_user: String,
}

async fn dashboard(State(state): State<Arc<AppState>>) -> Markup {
    authenticated_layout(
        &state.current_user,
        "Dashboard",
        html! {
            h1 { "Dashboard" }
            p { "User-specific content here" }
        },
    )
}
```

## Error Handling with IntoResponse

### Custom Error Type

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
};
use maud::{html, Markup};
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("not found")]
    NotFound,

    #[error("unauthorized")]
    Unauthorized,

    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("internal error: {0}")]
    Internal(String),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, title, message) = match self {
            AppError::NotFound => (
                StatusCode::NOT_FOUND,
                "404 - Not Found",
                "The page you're looking for doesn't exist.",
            ),
            AppError::Unauthorized => (
                StatusCode::UNAUTHORIZED,
                "401 - Unauthorized",
                "You must be logged in to view this page.",
            ),
            AppError::Database(_) => (
                StatusCode::INTERNAL_SERVER_ERROR,
                "500 - Internal Server Error",
                "A database error occurred. Please try again later.",
            ),
            AppError::Internal(_) => (
                StatusCode::INTERNAL_SERVER_ERROR,
                "500 - Internal Server Error",
                "An internal error occurred. Please try again later.",
            ),
        };

        let markup = error_page(status.as_u16(), title, message);
        (status, markup).into_response()
    }
}

fn error_page(code: u16, title: &str, message: &str) -> Markup {
    base_layout(title, html! {
        div.error-container {
            h1 { (code) }
            h2 { (title) }
            p { (message) }
            a href="/" { "← Return Home" }
        }
    })
}

// Handler using Result
async fn get_user(
    State(db): State<Arc<Database>>,
    Path(id): Path<String>,
) -> Result<Markup, AppError> {
    let user = db.find_user(&id).await?; // Automatically converts DB errors

    Ok(html! {
        div.user-profile {
            h1 { (user.name) }
            p { (user.email) }
        }
    })
}
```

## Dynamic Routes with Path Extraction

```rust
use axum::{
    extract::{Path, State},
    routing::get,
    Router,
};
use maud::{html, Markup};
use std::sync::Arc;

// Post model
#[derive(Clone)]
struct Post {
    id: u64,
    title: String,
    content: String,
    author: String,
}

#[derive(Clone)]
struct AppState {
    posts: Vec<Post>,
}

async fn post_detail(
    State(state): State<Arc<AppState>>,
    Path(id): Path<u64>,
) -> Result<Markup, AppError> {
    let post = state
        .posts
        .iter()
        .find(|p| p.id == id)
        .ok_or(AppError::NotFound)?;

    Ok(base_layout(&post.title, html! {
        article {
            h1 { (post.title) }
            p.author { "By " (post.author) }
            div.content {
                p { (post.content) }
            }
            a href="/posts" { "← Back to all posts" }
        }
    }))
}

async fn post_list(State(state): State<Arc<AppState>>) -> Markup {
    base_layout("All Posts", html! {
        h1 { "Blog Posts" }
        ul.post-list {
            @for post in &state.posts {
                li {
                    a href={ "/posts/" (post.id) } {
                        (post.title)
                    }
                    " by " (post.author)
                }
            }
        }
    })
}

fn create_router(state: Arc<AppState>) -> Router {
    Router::new()
        .route("/posts", get(post_list))
        .route("/posts/:id", get(post_detail))
        .with_state(state)
}
```

## Query Parameters

```rust
use axum::extract::Query;
use serde::Deserialize;

#[derive(Deserialize)]
struct Pagination {
    page: Option<u32>,
    per_page: Option<u32>,
}

async fn search_page(
    Query(params): Query<Pagination>,
) -> Markup {
    let page = params.page.unwrap_or(1);
    let per_page = params.per_page.unwrap_or(20);

    base_layout("Search Results", html! {
        h1 { "Search Results" }
        p { "Page " (page) " (showing " (per_page) " per page)" }

        nav.pagination {
            @if page > 1 {
                a href={ "?page=" (page - 1) "&per_page=" (per_page) } {
                    "← Previous"
                }
            }
            a href={ "?page=" (page + 1) "&per_page=" (per_page) } {
                "Next →"
            }
        }
    })
}
```

## Forms with POST Handlers

```rust
use axum::{
    extract::Form,
    response::Redirect,
    routing::{get, post},
};
use serde::Deserialize;

#[derive(Deserialize)]
struct CreateUserForm {
    name: String,
    email: String,
}

async fn user_form() -> Markup {
    base_layout("Create User", html! {
        h1 { "Create New User" }
        form method="POST" action="/users" {
            div.form-group {
                label for="name" { "Name" }
                input type="text" name="name" id="name" required;
            }
            div.form-group {
                label for="email" { "Email" }
                input type="email" name="email" id="email" required;
            }
            button type="submit" { "Create User" }
        }
    })
}

async fn create_user(
    State(db): State<Arc<Database>>,
    Form(form): Form<CreateUserForm>,
) -> Result<Redirect, AppError> {
    db.create_user(&form.name, &form.email).await?;

    // Redirect to success page
    Ok(Redirect::to("/users/success"))
}

fn user_routes(state: Arc<AppState>) -> Router {
    Router::new()
        .route("/users/new", get(user_form))
        .route("/users", post(create_user))
        .with_state(state)
}
```

## Production Router Setup

```rust
use axum::{
    middleware,
    routing::get,
    Router,
};
use tower::ServiceBuilder;
use tower_http::{
    compression::CompressionLayer,
    services::ServeDir,
    trace::TraceLayer,
    timeout::TimeoutLayer,
};
use std::time::Duration;

pub fn create_app(state: Arc<AppState>) -> Router {
    // API routes (return Markup)
    let api_routes = Router::new()
        .route("/", get(home_page))
        .route("/about", get(about_page))
        .route("/posts", get(post_list))
        .route("/posts/:id", get(post_detail))
        .layer(
            ServiceBuilder::new()
                .layer(TraceLayer::new_for_http())
                .layer(TimeoutLayer::new(Duration::from_secs(30)))
        );

    // Static file serving
    let static_routes = Router::new()
        .nest_service("/static", ServeDir::new("static"));

    // Combine routes
    Router::new()
        .merge(api_routes)
        .merge(static_routes)
        .layer(CompressionLayer::new())
        .with_state(state)
}
```

## Static Assets Management

### Serving CSS/JS

```rust
use tower_http::services::ServeDir;

let app = Router::new()
    .route("/", get(index))
    // Serve static files from ./static directory
    .nest_service("/static", ServeDir::new("static"))
    .with_state(state);

// In templates, reference as:
html! {
    link rel="stylesheet" href="/static/styles.css";
    script src="/static/app.js" {}
}
```

### Inline Styles (for Small Apps)

```rust
fn inline_styles() -> Markup {
    html! {
        style {
            (PreEscaped(r#"
                body { font-family: sans-serif; margin: 0; padding: 20px; }
                .container { max-width: 1200px; margin: 0 auto; }
                .error { color: red; }
            "#))
        }
    }
}

fn base_layout(title: &str, content: Markup) -> Markup {
    html! {
        (DOCTYPE)
        html {
            head {
                title { (title) }
                (inline_styles())
            }
            body {
                (content)
            }
        }
    }
}
```

## Production Patterns

### Health Check Endpoint

```rust
use axum::http::StatusCode;

async fn health() -> (StatusCode, Markup) {
    (StatusCode::OK, html! {
        (PreEscaped(r#"{"status":"ok"}"#))
    })
}

// Better: Return JSON for health checks
use axum::Json;
use serde_json::json;

async fn health_json() -> Json<serde_json::Value> {
    Json(json!({
        "status": "ok",
        "version": env!("CARGO_PKG_VERSION")
    }))
}
```

### Observability with Tracing

```rust
use tracing::instrument;

#[instrument(skip(state), fields(post_id = %id))]
async fn post_detail(
    State(state): State<Arc<AppState>>,
    Path(id): Path<u64>,
) -> Result<Markup, AppError> {
    tracing::info!("fetching post");

    let post = state
        .posts
        .iter()
        .find(|p| p.id == id)
        .ok_or(AppError::NotFound)?;

    tracing::info!("post found, rendering");

    Ok(base_layout(&post.title, html! {
        article { /* ... */ }
    }))
}
```

### Content Security Policy

```rust
use axum::{
    http::header,
    response::Response,
};

async fn with_csp(markup: Markup) -> Response {
    let mut response = markup.into_response();

    response.headers_mut().insert(
        header::CONTENT_SECURITY_POLICY,
        "default-src 'self'; script-src 'self' https://unpkg.com"
            .parse()
            .unwrap(),
    );

    response
}

// Or use middleware
use axum::middleware::Next;
use axum::extract::Request;

async fn add_csp_header(request: Request, next: Next) -> Response {
    let mut response = next.run(request).await;

    response.headers_mut().insert(
        header::CONTENT_SECURITY_POLICY,
        "default-src 'self'".parse().unwrap(),
    );

    response
}

let app = Router::new()
    .route("/", get(index))
    .layer(middleware::from_fn(add_csp_header));
```

## Common Patterns

### Navigation with Active State

```rust
use axum::extract::OriginalUri;
use axum::http::Uri;

fn navbar(current_path: &str) -> Markup {
    html! {
        nav.navbar {
            a.nav-link[current_path == "/"] href="/" { "Home" }
            a.nav-link[current_path.starts_with("/posts")] href="/posts" { "Posts" }
            a.nav-link[current_path == "/about"] href="/about" { "About" }
        }
    }
}

async fn with_navbar(OriginalUri(uri): OriginalUri) -> Markup {
    let path = uri.path();

    base_layout_with_nav(path, "Home", html! {
        h1 { "Welcome" }
    })
}

fn base_layout_with_nav(current_path: &str, title: &str, content: Markup) -> Markup {
    html! {
        (DOCTYPE)
        html {
            head { title { (title) } }
            body {
                (navbar(current_path))
                main { (content) }
            }
        }
    }
}
```

## Key Integration Points

1. **Markup → IntoResponse**: Automatic with `axum` feature
2. **State Management**: Use `State` extractor with `Arc<AppState>`
3. **Error Handling**: Implement `IntoResponse` for custom errors
4. **Layouts**: Function composition with `Markup` parameters
5. **Static Assets**: Use `ServeDir` from `tower-http`

## Best Practices

1. **Separate concerns**: Keep templates in dedicated module (`templates/`)
2. **Reusable layouts**: Create base layouts for consistency
3. **Type-safe errors**: Implement `IntoResponse` for all error types
4. **Use extractors**: Leverage Axum's extractors for path, query, form data
5. **Add middleware**: Use Tower layers for timeouts, compression, tracing
6. **Security headers**: Add CSP, X-Frame-Options via middleware
7. **Instrument handlers**: Use `#[instrument]` for observability

## Common Dependencies

```toml
[dependencies]
maud = { version = "0.27", features = ["axum"] }
axum = { version = "0.8", features = ["macros"] }
tokio = { version = "1", features = ["full"] }
tower = "0.5"
tower-http = { version = "0.6", features = ["trace", "compression", "fs"] }
serde = { version = "1", features = ["derive"] }
thiserror = "2"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

## References

- **Maud Docs**: https://maud.lambda.xyz
- **Axum Docs**: https://docs.rs/axum
- **HARM Stack Article**: https://nguyenhuythanh.com/posts/the-harm-stack-considered-unharmful/
