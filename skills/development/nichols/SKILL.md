---
name: nichols-practical-rust
description: Write Rust code in the style of Carol Nichols, co-author of The Rust Book. Emphasizes practical patterns, clear explanations, and real-world applicability. Use when writing production Rust or explaining Rust to others.
---

# Carol Nichols Style Guide

## Overview

Carol Nichols is co-author of "The Rust Programming Language," co-founder of Integer 32 (Rust consultancy), and a key contributor to crates.io. Her focus: making Rust practical and accessible for real-world use.

## Core Philosophy

> "Rust should help you ship software."

> "The best abstraction is one you don't have to think about."

Nichols believes Rust's safety guarantees should enable productivity, not hinder it. Write code that works, is safe, and can be maintained.

## Design Principles

1. **Practicality Over Purity**: Working code beats theoretically perfect code.

2. **Errors Should Help**: Error messages and types should guide resolution.

3. **Progressive Disclosure**: Simple things simple, complex things possible.

4. **Real-World Focus**: Code should solve actual problems.

## When Writing Code

### Always

- Use `thiserror` or `anyhow` for error handling in applications
- Write tests alongside code, not as an afterthought
- Use `clippy` and address its warnings
- Leverage the type system but don't over-engineer
- Profile before optimizing

### Never

- Write unsafe code without exhaustive documentation
- Ignore clippy lints without understanding them
- Over-abstract before you need to
- Sacrifice readability for micro-optimizations

### Prefer

- `anyhow` for applications, `thiserror` for libraries
- `#[derive]` over manual trait implementations
- `serde` for serialization
- Integration tests for complex systems

## Code Patterns

### Practical Error Handling

```rust
// For applications: use anyhow for easy error handling
use anyhow::{Context, Result};

fn load_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .context("Failed to read config file")?;
    
    let config: Config = toml::from_str(&content)
        .context("Failed to parse config")?;
    
    Ok(config)
}

fn main() -> Result<()> {
    let config = load_config("config.toml")?;
    run_app(config)?;
    Ok(())
}

// For libraries: use thiserror for typed errors
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DatabaseError {
    #[error("connection failed: {0}")]
    ConnectionFailed(#[source] std::io::Error),
    
    #[error("query failed: {query}")]
    QueryFailed { query: String, #[source] source: SqlError },
    
    #[error("record not found: {0}")]
    NotFound(String),
}
```

### Testing Patterns

```rust
// Unit tests in the same file
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_addition() {
        assert_eq!(add(2, 2), 4);
    }

    #[test]
    fn test_edge_case() {
        assert_eq!(add(0, 0), 0);
        assert_eq!(add(-1, 1), 0);
    }

    // Test that something panics
    #[test]
    #[should_panic(expected = "division by zero")]
    fn test_divide_by_zero() {
        divide(1, 0);
    }

    // Test Result-returning functions
    #[test]
    fn test_parse() -> Result<(), ParseError> {
        let result = parse("42")?;
        assert_eq!(result, 42);
        Ok(())
    }
}

// Integration tests in tests/ directory
// tests/integration_test.rs
use my_crate::Client;

#[test]
fn test_full_workflow() {
    let client = Client::new();
    let user = client.create_user("test@example.com").unwrap();
    let fetched = client.get_user(user.id).unwrap();
    assert_eq!(user.email, fetched.email);
    client.delete_user(user.id).unwrap();
}

// Using test fixtures
#[fixture]
fn sample_config() -> Config {
    Config {
        database_url: "postgres://test".into(),
        port: 8080,
    }
}

#[rstest]
fn test_with_config(sample_config: Config) {
    let app = App::new(sample_config);
    assert!(app.is_configured());
}
```

### Serde for Real-World Data

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct User {
    pub id: u64,
    pub email: String,
    
    // Rename for external format
    #[serde(rename = "firstName")]
    pub first_name: String,
    
    // Use default if missing
    #[serde(default)]
    pub active: bool,
    
    // Skip if None
    #[serde(skip_serializing_if = "Option::is_none")]
    pub phone: Option<String>,
    
    // Custom deserialization
    #[serde(deserialize_with = "deserialize_timestamp")]
    pub created_at: DateTime<Utc>,
}

// Reading from JSON
let user: User = serde_json::from_str(json_str)?;

// Reading from TOML config
let config: Config = toml::from_str(&std::fs::read_to_string("config.toml")?)?;

// Reading from environment
use envy;
let config: Config = envy::from_env()?;
```

### Practical Async Code

```rust
use tokio;

#[tokio::main]
async fn main() -> Result<()> {
    // Simple async operation
    let data = fetch_data().await?;
    
    // Concurrent operations
    let (users, posts) = tokio::join!(
        fetch_users(),
        fetch_posts()
    );
    
    // With timeout
    let result = tokio::time::timeout(
        Duration::from_secs(10),
        slow_operation()
    ).await??;
    
    // Spawning background tasks
    tokio::spawn(async move {
        loop {
            cleanup_old_data().await;
            tokio::time::sleep(Duration::from_secs(3600)).await;
        }
    });
    
    Ok(())
}

// Practical async function
async fn fetch_and_process(url: &str) -> Result<ProcessedData> {
    let response = reqwest::get(url).await?;
    let bytes = response.bytes().await?;
    let data = process(&bytes)?;
    Ok(data)
}
```

### CLI Applications

```rust
use clap::Parser;

/// A simple program to greet users
#[derive(Parser, Debug)]
#[command(author, version, about)]
struct Args {
    /// Name of the person to greet
    #[arg(short, long)]
    name: String,

    /// Number of times to greet
    #[arg(short, long, default_value_t = 1)]
    count: u8,

    /// Enable verbose output
    #[arg(short, long)]
    verbose: bool,
}

fn main() -> Result<()> {
    let args = Args::parse();
    
    for _ in 0..args.count {
        println!("Hello, {}!", args.name);
    }
    
    if args.verbose {
        println!("Greeted {} times", args.count);
    }
    
    Ok(())
}
```

### Logging and Observability

```rust
use tracing::{info, warn, error, instrument};

#[instrument]
async fn process_request(request_id: u64, user_id: u64) -> Result<Response> {
    info!("Processing request");
    
    let user = match get_user(user_id).await {
        Ok(user) => user,
        Err(e) => {
            warn!("User not found, using default");
            User::default()
        }
    };
    
    let result = do_work(&user).await?;
    
    info!(response_size = result.len(), "Request complete");
    Ok(result)
}

// Setup in main
fn main() {
    tracing_subscriber::fmt()
        .with_env_filter("my_app=debug,tower_http=info")
        .init();
    
    // ...
}
```

## Mental Model

Nichols approaches code by asking:

1. **Does this solve the problem?** Ship working code.
2. **Can someone else maintain this?** Write for your team.
3. **What could go wrong?** Handle it gracefully.
4. **Is this tested?** If not, how do you know it works?

## Practical Rust Checklist

- [ ] `cargo clippy` passes
- [ ] `cargo fmt` applied
- [ ] Tests cover main functionality
- [ ] Error messages are helpful
- [ ] Documentation exists for public items
- [ ] Dependencies are reasonable and maintained

