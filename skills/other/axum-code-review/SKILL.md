---
name: axum-code-review
description: Reviews axum web framework code for routing patterns, extractor usage, middleware, state management, and error handling. Use when reviewing Rust code that uses axum, tower, or hyper for HTTP services. Covers axum 0.7+ patterns including State, Path, Query, Json extractors.
---

# Axum Code Review

## Review Workflow

1. **Check Cargo.toml** — Note axum version (0.6 vs 0.7+ have different patterns), Rust edition (2021 vs 2024), tower, tower-http features. Edition 2024 changes RPIT lifetime capture in handler return types and removes the need for `async-trait` in custom extractors.
2. **Check routing** — Route organization, method routing, nested routers
3. **Check extractors** — Order matters (body extractors must be last), correct types
4. **Check state** — Shared state via `State<T>`, not global mutable state
5. **Check error handling** — `IntoResponse` implementations, error types

## Gates (before reporting findings)

Run **in order**. Do not write a finding until the step that applies has passed.

1. **Version and edition on disk** — **Pass when:** You have read the relevant `Cargo.toml` (crate or workspace root) and can state `axum` (and related tower/tower-http) versions and Rust `edition`. **Then** apply 0.6 vs 0.7+ or Edition 2024–specific checklist items only when that file supports them.

2. **Per-finding evidence** — **Pass when:** Each issue cites `[FILE:LINE]` from the **current** tree for the handler, router, layer, or type under review (not from memory, docs-only, or another branch).

3. **Category check vs protocol** — **Pass when:** For the finding type (routing conflict, extractor order, error leak, middleware order, etc.), you ran the matching checks from `beagle-rust:review-verification-protocol` (e.g. full handler signature for extractor order; surrounding error mapping before “raw error to client”). **Then** add the finding.

4. **Output shape** — **Pass when:** The report lines match **Output Format** below (severity + description).

## Output Format

Report findings as:

```text
[FILE:LINE] ISSUE_TITLE
Severity: Critical | Major | Minor | Informational
Description of the issue and why it matters.
```

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Route definitions, nesting, method routing | [references/routing.md](references/routing.md) |
| State, Path, Query, Json, body extractors | [references/extractors.md](references/extractors.md) |
| Tower middleware, layers, error handling | [references/middleware.md](references/middleware.md) |

## Review Checklist

### Routing
- [ ] Routes organized by domain (nested routers for `/api/users`, `/api/orders`)
- [ ] Fallback handlers defined for 404s
- [ ] Method routing explicit (`.get()`, `.post()`, not `.route()` with manual method matching)
- [ ] No route conflicts (overlapping paths with different extractors)

### Extractors
- [ ] Body-consuming extractors (`Json`, `Form`, `Bytes`) are the LAST parameter
- [ ] `State<T>` requires `T: Clone` — typically `Arc<AppState>` or direct `Clone` derive
- [ ] `Path<T>` parameter types match the route definition
- [ ] `Query<T>` fields are `Option` for optional query params with `#[serde(default)]`
- [ ] Custom extractors implement `FromRequestParts` (not body) or `FromRequest` (body)
- [ ] **Edition 2024**: Custom extractors use native `async fn` in trait impls (no `#[async_trait]` needed for `FromRequest`/`FromRequestParts`)

### State Management
- [ ] Application state shared via `State<T>`, not global mutable statics
- [ ] Database pool in state (not created per-request)
- [ ] State contains only shared resources (pool, config, channels), not request-specific data
- [ ] `Clone` derived or manually implemented on state type
- [ ] **Edition 2024**: Shared static state uses `LazyLock` from std (not `once_cell::sync::Lazy` or `lazy_static!`)

### Error Handling
- [ ] Handler errors implement `IntoResponse` for proper HTTP error codes
- [ ] Internal errors don't leak to clients (no raw error messages in 500 responses)
- [ ] Error responses use consistent format (JSON error body with code/message)
- [ ] `Result<impl IntoResponse, AppError>` pattern used for handlers
- [ ] **Edition 2024**: Handler return types `-> impl IntoResponse` capture all in-scope lifetimes by default; use `+ use<>` to opt out of capturing request lifetimes when returning owned data

### Middleware
- [ ] Tower layers applied in correct order (outer runs first on request, last on response)
- [ ] `tower-http` used for common concerns (CORS, compression, tracing, timeout)
- [ ] Request-scoped data passed via extensions, not global state
- [ ] Middleware errors don't panic — they return error responses
- [ ] **Edition 2024**: Middleware using `#[async_trait]` can migrate to native `async fn` in trait impls

## Severity Calibration

### Critical
- Body extractor not last in handler parameters (silently consumes body, later extractors fail)
- SQL injection via path/query parameters passed directly to queries
- Internal error details leaked to clients (stack traces, database errors)
- Missing authentication middleware on protected routes

### Major
- Global mutable state instead of `State<T>` (race conditions)
- Missing error type conversion (raw `sqlx::Error` returned to client)
- Missing request timeout (handlers can hang indefinitely)
- Route conflicts causing unexpected 405s
- **Edition 2024**: `async-trait` still used for `FromRequest`/`FromRequestParts` when native async fn works

### Minor
- Manual route method matching instead of `.get()`, `.post()`
- Missing fallback handler (default 404 is plain text, not JSON)
- Middleware applied per-route when it should be global (or vice versa)
- Missing `tower-http::trace` for request logging
- **Edition 2024**: `once_cell::sync::Lazy` or `lazy_static!` used where `std::sync::LazyLock` works

### Informational
- Suggestions to use `tower-http` layers for common concerns
- Router organization improvements
- Suggestions to add OpenAPI documentation via `utoipa` or `aide`

## Valid Patterns (Do NOT Flag)

- **`#[axum::debug_handler]` on handlers** — Debugging aid that improves compile error messages
- **`Extension<T>` for middleware-injected data** — Valid pattern for request-scoped values
- **Returning `impl IntoResponse` from handlers** — More flexible than concrete types
- **`Router::new()` per module, merged in main** — Standard organization pattern
- **`ServiceBuilder` for layer composition** — Tower pattern, not over-engineering
- **`axum::serve` with `TcpListener`** — Standard axum 0.7+ server setup
- **Native `async fn` in `FromRequest`/`FromRequestParts` impls** — `async-trait` crate no longer needed (stable since Rust 1.75)
- **`+ use<'a>` on handler return types** — Edition 2024 precise capture syntax for RPIT
- **`std::sync::LazyLock` for shared static state** — Replaces `once_cell`/`lazy_static` (stable since Rust 1.80)

## Before Submitting Findings

Complete **Gates (before reporting findings)** and load `beagle-rust:review-verification-protocol` for category-specific checks before any issue is final.
