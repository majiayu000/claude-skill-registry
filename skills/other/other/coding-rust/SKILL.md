---
name: coding-rust
cluster: coding
description: "Rust: ownership/borrowing/lifetimes, traits, tokio async, anyhow/thiserror, cargo workspaces, unsafe"
tags: ["rust","systems","coding"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "rust ownership borrow lifetime trait async tokio cargo unsafe"
---

# coding-rust

## Purpose
This skill provides expertise in advanced Rust programming, focusing on core language features and ecosystem tools to build efficient, safe systems code.

## When to Use
- When implementing memory-safe code with ownership, borrowing, or lifetimes to prevent common errors like data races.
- For projects requiring asynchronous programming with Tokio, error handling via anyhow/thiserror, or managing multi-crate setups with Cargo workspaces.
- In scenarios involving unsafe code for performance-critical sections, or defining custom behaviors with traits.

## Key Capabilities
- Manage Rust's ownership model: Use references (&T) and lifetimes ('a) to borrow data without transferring ownership.
- Implement traits: Define and use trait objects for polymorphism, e.g., `trait Debug { fn fmt(&self); }`.
- Handle async with Tokio: Run asynchronous tasks using `tokio::main` and futures.
- Error management: Leverage anyhow for simple error wrapping and thiserror for custom error types.
- Cargo workspaces: Organize multi-package projects with `Cargo.toml` workspaces for dependency sharing.
- Unsafe operations: Use unsafe blocks for raw pointers or FFI, ensuring safety invariants are maintained.

## Usage Patterns
- To handle ownership and borrowing, always prefer borrowing over cloning: Use `&mut T` for mutable references and ensure lifetimes match, e.g., in functions like `fn borrow lifetimes<'a>(x: &'a i32) -> &'a i32`.
- For async tasks, spawn Tokio runtimes: Use `tokio::spawn` to run futures concurrently, then await results in an async main function.
- Define traits for extensibility: Create a trait and implement it for structs, e.g., `impl MyTrait for MyStruct { fn method() { ... } }`.
- Set up Cargo workspaces: In the root `Cargo.toml`, add `[workspace]` section with `members = ["crate1", "crate2"]`, then build with `cargo build --workspace`.
- Use anyhow for errors: Wrap errors with `anyhow::Result` and propagate them using `?` operator.
- Employ unsafe sparingly: Wrap unsafe code in blocks like `unsafe { *ptr = value; }` and justify with comments.

## Common Commands/API
- Cargo commands: Build with `cargo build --release` for optimized binaries; test with `cargo test --workspace` for all crates; add dependencies via `cargo add tokio --features full`.
- Tokio API: Start an async runtime with `#[tokio::main] async fn main() { tokio::spawn(async { ... }); }`; use channels for async communication, e.g., `let (tx, rx) = tokio::sync::mpsc::channel(10);`.
- Anyhow/thiserror: Define custom errors with `#[derive(thiserror::Error)] enum MyError { ... }`; handle in functions as `fn example() -> anyhow::Result<()> { ... }`.
- Ownership helpers: Use standard library functions like `std::mem::drop` to explicitly drop values, or `std::borrow::Cow` for owned/copied data.
- Config formats: Edit `Cargo.toml` for project settings, e.g., `[dependencies] tokio = { version = "1.0", features = ["full"] }`; use environment variables for secrets like `RUST_BACKTRACE=1` for debugging.

## Integration Notes
- Integrate with other tools: Use `$RUSTUP_TOOLCHAIN` env var to switch Rust versions, e.g., `export RUSTUP_TOOLCHAIN=nightly` for unstable features.
- For API keys in external integrations (e.g., if calling external services from Rust), set env vars like `$MY_API_KEY` and access via `std::env::var("MY_API_KEY").unwrap()`.
- Combine with build tools: In CI/CD, run `cargo fmt` for code formatting and `cargo clippy` for lints before builds.
- Embed in projects: Add Tokio as a dependency in `Cargo.toml`, then import in code with `use tokio::runtime::Runtime; let rt = Runtime::new().unwrap(); rt.block_on(async { ... });`.
- Handle cross-crate dependencies in workspaces: Reference crates via paths, e.g., in `Cargo.toml`, use `path = "../sibling_crate"`.

## Error Handling
- Use anyhow for quick error propagation: Return `anyhow::Result<T>` from functions and use `?` to handle errors, e.g., `fn read_file() -> anyhow::Result<String> { std::fs::read_to_string("file.txt").context("Failed to read") }`.
- Define custom errors with thiserror: Derive errors like `#[derive(thiserror::Error, Debug)] enum AppError { #[error("IO error: {0}")] Io(#[from] std::io::Error), }` and handle with match statements.
- In async contexts, use Tokio's error types: Await futures and handle errors with `.await.map_err(|e| anyhow::Error::from(e))`.
- Always check for panics in unsafe code: Use `std::panic::catch_unwind` around unsafe blocks to prevent crashes.

## Concrete Usage Examples
1. Async HTTP server with Tokio: Create a simple server by adding Tokio to `Cargo.toml`, then write: `use tokio::net::TcpListener; #[tokio::main] async fn main() -> anyhow::Result<()> { let listener = TcpListener::bind("127.0.0.1:8080").await?; loop { let (socket, _) = listener.accept().await?; tokio::spawn(handle_connection(socket)); } }`.
2. Error handling in a CLI tool: Define errors and use anyhow: In `Cargo.toml`, add `anyhow = "1.0"` and `thiserror = "1.0"`, then implement: `use thiserror::Error; #[derive(Error, Debug)] enum Error { #[error("Parse error")] Parse, } fn main() -> anyhow::Result<()> { let input = std::env::args().nth(1)?; if input.parse::<u32>().is_err() { Err(Error::Parse)?; } Ok(()) }`.

## Graph Relationships
- Related to: coding (cluster), as it shares tags like "coding" and focuses on programming skills.
- Connected via: tags ["rust", "systems"], potentially linking to other Rust or systems programming skills.
- Dependencies: May integrate with skills in "coding" cluster, such as general coding tools for broader ecosystem support.
