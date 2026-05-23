---
name: rust
description: Rust language expertise for writing safe, performant, production-quality Rust code. Primary language for the Loom project. Use for Rust development, ownership patterns, error handling, async/await, cargo management, CLI tools, and serialization. Triggers: rust, cargo, rustc, ownership, borrowing, lifetime, trait, impl, struct, enum, Result, Option, async, await, tokio, serde, clap, thiserror, anyhow, Arc, Mutex, RwLock, RefCell, Box, Rc, Vec, HashMap, HashSet, String, derive, macro.
---

# Rust Language Expertise

## Overview

This skill provides guidance for writing safe, efficient, and idiomatic Rust code. As the primary language for the Loom project, this skill covers:

- Ownership, borrowing, and lifetimes
- Error handling with Result, Option, thiserror, and anyhow
- Traits, generics, and type system patterns
- Async programming with tokio runtime
- CLI development with clap
- Serialization with serde (JSON, TOML, YAML)
- Common patterns and anti-patterns
- Testing strategies
- Cargo and workspace management

## Key Concepts

### Ownership, Borrowing, and Lifetimes

```rust
// Ownership rules:
// 1. Each value has exactly one owner
// 2. When the owner goes out of scope, the value is dropped
// 3. Ownership can be transferred (moved) or borrowed

// Move semantics
fn take_ownership(s: String) {
    println!("{}", s);
} // s is dropped here

fn main() {
    let s = String::from("hello");
    take_ownership(s);
    // s is no longer valid here
}

// Borrowing (references)
fn borrow(s: &String) {
    println!("{}", s);
}

fn borrow_mut(s: &mut String) {
    s.push_str(" world");
}

// Lifetimes ensure references are valid
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct with lifetime annotations
struct Parser<'a> {
    input: &'a str,
    position: usize,
}

impl<'a> Parser<'a> {
    fn new(input: &'a str) -> Self {
        Parser { input, position: 0 }
    }

    fn peek(&self) -> Option<char> {
        self.input[self.position..].chars().next()
    }
}

// Common lifetime elision patterns
impl Config {
    // fn get(&self, key: &str) -> Option<&str>
    // is short for:
    // fn get<'a, 'b>(&'a self, key: &'b str) -> Option<&'a str>
    fn get(&self, key: &str) -> Option<&str> {
        self.map.get(key).map(|s| s.as_str())
    }
}
```

### Error Handling

```rust
use std::error::Error;
use std::fmt;
use std::io;

// Using thiserror for custom errors
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] io::Error),

    #[error("Parse error at line {line}: {message}")]
    Parse { line: usize, message: String },

    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Validation failed: {0}")]
    Validation(String),
}

// Using anyhow for application code
use anyhow::{Context, Result, bail, ensure};

fn read_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read config from {}", path))?;

    let config: Config = serde_json::from_str(&content)
        .context("Failed to parse config JSON")?;

    ensure!(!config.name.is_empty(), "Config name cannot be empty");

    if config.port == 0 {
        bail!("Invalid port number");
    }

    Ok(config)
}

// The ? operator for propagating errors
fn process_file(path: &str) -> Result<Vec<Record>, AppError> {
    let content = std::fs::read_to_string(path)?; // io::Error -> AppError via From
    let records = parse_records(&content)?;
    Ok(records)
}

// Option handling
fn find_user(users: &[User], name: &str) -> Option<&User> {
    users.iter().find(|u| u.name == name)
}

fn get_user_email(users: &[User], name: &str) -> Option<String> {
    users
        .iter()
        .find(|u| u.name == name)
        .and_then(|u| u.email.clone())
}

// Converting between Option and Result
fn require_user(users: &[User], name: &str) -> Result<&User, AppError> {
    users
        .iter()
        .find(|u| u.name == name)
        .ok_or_else(|| AppError::NotFound(format!("User: {}", name)))
}
```

### Traits and Generics

```rust
// Defining traits
trait Repository<T> {
    fn get(&self, id: &str) -> Option<&T>;
    fn save(&mut self, item: T) -> Result<(), Box<dyn Error>>;

    // Default implementation
    fn exists(&self, id: &str) -> bool {
        self.get(id).is_some()
    }
}

// Trait bounds
fn process<T: Clone + Debug>(item: &T) {
    let cloned = item.clone();
    println!("{:?}", cloned);
}

// where clauses for complex bounds
fn merge<T, U, V>(a: T, b: U) -> V
where
    T: IntoIterator<Item = V>,
    U: IntoIterator<Item = V>,
    V: Ord + Clone,
{
    let mut result: Vec<V> = a.into_iter().chain(b.into_iter()).collect();
    result.sort();
    result.dedup();
    result.into_iter().next().unwrap()
}

// Associated types
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}

// Implementing traits
struct InMemoryRepo<T> {
    items: HashMap<String, T>,
}

impl<T: Clone> Repository<T> for InMemoryRepo<T> {
    fn get(&self, id: &str) -> Option<&T> {
        self.items.get(id)
    }

    fn save(&mut self, item: T) -> Result<(), Box<dyn Error>> {
        // Implementation
        Ok(())
    }
}

// Blanket implementations
impl<T: Display> ToString for T {
    fn to_string(&self) -> String {
        format!("{}", self)
    }
}
```

### Iterators

```rust
// Iterator combinators
fn process_users(users: Vec<User>) -> Vec<String> {
    users
        .into_iter()
        .filter(|u| u.active)
        .map(|u| u.email)
        .filter_map(|email| email)  // Remove None values
        .collect()
}

// Custom iterator
struct Counter {
    current: usize,
    max: usize,
}

impl Iterator for Counter {
    type Item = usize;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current < self.max {
            let val = self.current;
            self.current += 1;
            Some(val)
        } else {
            None
        }
    }
}

// Useful iterator methods
fn examples(numbers: Vec<i32>) {
    // Fold/reduce
    let sum: i32 = numbers.iter().fold(0, |acc, x| acc + x);

    // Any/all
    let has_positive = numbers.iter().any(|&x| x > 0);
    let all_positive = numbers.iter().all(|&x| x > 0);

    // Find
    let first_even = numbers.iter().find(|&&x| x % 2 == 0);

    // Partition
    let (evens, odds): (Vec<_>, Vec<_>) = numbers.iter().partition(|&&x| x % 2 == 0);

    // Enumerate
    for (index, value) in numbers.iter().enumerate() {
        println!("{}: {}", index, value);
    }

    // Zip
    let other = vec![1, 2, 3];
    let pairs: Vec<_> = numbers.iter().zip(other.iter()).collect();
}
```

## Best Practices

### Cargo and Project Structure

```toml
# Cargo.toml
[package]
name = "myproject"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"

[dependencies]
tokio = { version = "1.35", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
thiserror = "1.0"
anyhow = "1.0"

[dev-dependencies]
criterion = "0.5"
mockall = "0.12"

[features]
default = []
full = ["feature-a", "feature-b"]
feature-a = []
feature-b = ["dep:optional-dep"]

[[bench]]
name = "my_benchmark"
harness = false
```

### Workspace Structure

```
myworkspace/
├── Cargo.toml          # Workspace root
├── crates/
│   ├── core/
│   │   ├── Cargo.toml
│   │   └── src/
│   ├── api/
│   │   ├── Cargo.toml
│   │   └── src/
│   └── cli/
│       ├── Cargo.toml
│       └── src/
```

```toml
# Root Cargo.toml
[workspace]
members = ["crates/*"]
resolver = "2"

[workspace.dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1.35", features = ["full"] }
```

### CLI Applications with Clap

```rust
use clap::{Parser, Subcommand, ValueEnum, Args};
use std::path::PathBuf;

// Main CLI structure
#[derive(Parser)]
#[command(name = "loom")]
#[command(about = "Agent orchestration CLI", long_about = None)]
#[command(version)]
struct Cli {
    /// Optional config file
    #[arg(short, long, value_name = "FILE")]
    config: Option<PathBuf>,

    /// Verbosity level (can be used multiple times: -v, -vv, -vvv)
    #[arg(short, long, action = clap::ArgAction::Count)]
    verbose: u8,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialize a new project
    Init {
        /// Project name
        name: String,

        /// Project template
        #[arg(short, long, default_value = "default")]
        template: String,

        /// Skip git initialization
        #[arg(long)]
        no_git: bool,
    },

    /// Run the orchestrator daemon
    Run {
        /// Plan file to execute
        #[arg(value_name = "PLAN")]
        plan: Option<PathBuf>,

        /// Run in foreground (don't daemonize)
        #[arg(short, long)]
        foreground: bool,
    },

    /// Stage management commands
    Stage(StageArgs),

    /// Knowledge base commands
    Knowledge {
        #[command(subcommand)]
        command: KnowledgeCommands,
    },

    /// Show status
    Status {
        /// Output format
        #[arg(short, long, value_enum, default_value = "table")]
        format: OutputFormat,

        /// Watch mode - refresh every N seconds
        #[arg(short, long, value_name = "SECONDS")]
        watch: Option<u64>,
    },
}

#[derive(Args)]
struct StageArgs {
    #[command(subcommand)]
    command: StageCommands,
}

#[derive(Subcommand)]
enum StageCommands {
    /// Mark stage as complete
    Complete {
        /// Stage ID
        stage_id: String,
    },
    /// List all stages
    List {
        /// Show only active stages
        #[arg(short, long)]
        active: bool,
    },
    /// Show stage details
    Show {
        /// Stage ID
        stage_id: String,
    },
}

#[derive(Subcommand)]
enum KnowledgeCommands {
    /// Initialize knowledge base
    Init,
    /// List knowledge files
    List,
    /// Show knowledge content
    Show {
        /// Specific file to show (entry-points, patterns, conventions)
        file: Option<String>,
    },
    /// Update knowledge file
    Update {
        /// File to update
        file: String,
        /// Content to append
        content: String,
    },
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum OutputFormat {
    /// Human-readable table
    Table,
    /// JSON output
    Json,
    /// YAML output
    Yaml,
}

// Main function
fn main() -> Result<()> {
    let cli = Cli::parse();

    // Configure logging based on verbosity
    let log_level = match cli.verbose {
        0 => log::LevelFilter::Warn,
        1 => log::LevelFilter::Info,
        2 => log::LevelFilter::Debug,
        _ => log::LevelFilter::Trace,
    };
    env_logger::Builder::new().filter_level(log_level).init();

    // Load config if provided
    let config = if let Some(config_path) = cli.config {
        Config::load(&config_path)?
    } else {
        Config::default()
    };

    // Dispatch to command handlers
    match cli.command {
        Commands::Init { name, template, no_git } => {
            commands::init(&name, &template, !no_git)?;
        }
        Commands::Run { plan, foreground } => {
            commands::run(plan.as_deref(), foreground, &config)?;
        }
        Commands::Stage(args) => match args.command {
            StageCommands::Complete { stage_id } => {
                commands::stage::complete(&stage_id)?;
            }
            StageCommands::List { active } => {
                commands::stage::list(active)?;
            }
            StageCommands::Show { stage_id } => {
                commands::stage::show(&stage_id)?;
            }
        },
        Commands::Knowledge { command } => match command {
            KnowledgeCommands::Init => commands::knowledge::init()?,
            KnowledgeCommands::List => commands::knowledge::list()?,
            KnowledgeCommands::Show { file } => {
                commands::knowledge::show(file.as_deref())?
            }
            KnowledgeCommands::Update { file, content } => {
                commands::knowledge::update(&file, &content)?
            }
        },
        Commands::Status { format, watch } => {
            if let Some(interval) = watch {
                commands::status::watch(format, interval)?;
            } else {
                commands::status::show(format)?;
            }
        }
    }

    Ok(())
}

// Custom argument validators
fn validate_stage_id(s: &str) -> Result<String, String> {
    if s.is_empty() {
        return Err("Stage ID cannot be empty".to_string());
    }
    if !s.chars().all(|c| c.is_alphanumeric() || c == '-' || c == '_') {
        return Err("Stage ID must contain only alphanumeric characters, hyphens, and underscores".to_string());
    }
    Ok(s.to_string())
}
```

### Serialization with Serde

```rust
use serde::{Deserialize, Serialize, Deserializer, Serializer};
use serde_json::Value as JsonValue;
use std::collections::HashMap;
use std::path::PathBuf;

// Basic derive macros
#[derive(Debug, Clone, Serialize, Deserialize)]
struct Config {
    name: String,
    version: String,
    #[serde(default)]
    enabled: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    description: Option<String>,
}

// Renaming fields
#[derive(Debug, Serialize, Deserialize)]
struct User {
    #[serde(rename = "userId")]
    user_id: String,
    #[serde(rename = "userName")]
    user_name: String,
    // Flatten nested structure
    #[serde(flatten)]
    metadata: HashMap<String, String>,
}

// Default values and skip
#[derive(Debug, Serialize, Deserialize)]
struct Settings {
    #[serde(default = "default_timeout")]
    timeout: u64,
    #[serde(default)]
    retries: u32,
    #[serde(skip)]
    runtime_state: Option<String>,
    #[serde(skip_serializing_if = "Vec::is_empty")]
    tags: Vec<String>,
}

fn default_timeout() -> u64 {
    30
}

// Enum representations
#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
enum Status {
    Active,
    Inactive,
    Pending,
}

// Tagged enum (externally tagged by default)
#[derive(Debug, Serialize, Deserialize)]
#[serde(tag = "type")]
enum Message {
    Text { content: String },
    Image { url: String, alt: Option<String> },
    Video { url: String, duration: u32 },
}

// Internally tagged enum
#[derive(Debug, Serialize, Deserialize)]
#[serde(tag = "kind", content = "data")]
enum Event {
    Created(String),
    Updated { id: String, changes: Vec<String> },
    Deleted(String),
}

// Untagged enum (tries each variant in order)
#[derive(Debug, Serialize, Deserialize)]
#[serde(untagged)]
enum StringOrNumber {
    Str(String),
    Num(i64),
}

// Custom serialization
#[derive(Debug)]
struct Timestamp(chrono::DateTime<chrono::Utc>);

impl Serialize for Timestamp {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        serializer.serialize_i64(self.0.timestamp())
    }
}

impl<'de> Deserialize<'de> for Timestamp {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        let timestamp = i64::deserialize(deserializer)?;
        let dt = chrono::DateTime::from_timestamp(timestamp, 0)
            .ok_or_else(|| serde::de::Error::custom("Invalid timestamp"))?;
        Ok(Timestamp(dt))
    }
}

// Using with helper functions
#[derive(Debug, Serialize, Deserialize)]
struct Task {
    id: String,
    #[serde(with = "chrono::serde::ts_seconds")]
    created_at: chrono::DateTime<chrono::Utc>,
    #[serde(serialize_with = "serialize_path")]
    #[serde(deserialize_with = "deserialize_path")]
    file_path: PathBuf,
}

fn serialize_path<S>(path: &PathBuf, serializer: S) -> Result<S::Ok, S::Error>
where
    S: Serializer,
{
    serializer.serialize_str(&path.to_string_lossy())
}

fn deserialize_path<'de, D>(deserializer: D) -> Result<PathBuf, D::Error>
where
    D: Deserializer<'de>,
{
    let s = String::deserialize(deserializer)?;
    Ok(PathBuf::from(s))
}

// Working with JSON
fn json_examples() -> Result<()> {
    let config = Config {
        name: "test".to_string(),
        version: "1.0".to_string(),
        enabled: true,
        description: Some("A test config".to_string()),
    };

    // Serialize to JSON string
    let json = serde_json::to_string(&config)?;
    let json_pretty = serde_json::to_string_pretty(&config)?;

    // Deserialize from JSON string
    let parsed: Config = serde_json::from_str(&json)?;

    // Work with generic JSON values
    let mut value: JsonValue = serde_json::from_str(&json)?;
    if let Some(obj) = value.as_object_mut() {
        obj.insert("extra".to_string(), JsonValue::Bool(true));
    }

    // Convert to specific type
    let config2: Config = serde_json::from_value(value)?;

    Ok(())
}

// Working with TOML
fn toml_examples() -> Result<()> {
    let config = Config {
        name: "test".to_string(),
        version: "1.0".to_string(),
        enabled: true,
        description: None,
    };

    // Serialize to TOML
    let toml = toml::to_string(&config)?;
    let toml_pretty = toml::to_string_pretty(&config)?;

    // Deserialize from TOML
    let parsed: Config = toml::from_str(&toml)?;

    Ok(())
}

// Working with YAML
fn yaml_examples() -> Result<()> {
    let config = Config {
        name: "test".to_string(),
        version: "1.0".to_string(),
        enabled: true,
        description: None,
    };

    // Serialize to YAML
    let yaml = serde_yaml::to_string(&config)?;

    // Deserialize from YAML
    let parsed: Config = serde_yaml::from_str(&yaml)?;

    Ok(())
}

// Generic serialization function
fn serialize_any<T: Serialize>(value: &T, format: &str) -> Result<String> {
    match format {
        "json" => Ok(serde_json::to_string_pretty(value)?),
        "toml" => Ok(toml::to_string_pretty(value)?),
        "yaml" => Ok(serde_yaml::to_string(value)?),
        _ => Err(anyhow::anyhow!("Unsupported format: {}", format)),
    }
}
```

### Async/Await with Tokio

```rust
use tokio::sync::{mpsc, Mutex, RwLock};
use std::sync::Arc;
use tokio::time::{sleep, Duration, timeout};

// Basic async function
async fn fetch_data(url: &str) -> Result<String> {
    let response = reqwest::get(url).await?;
    let body = response.text().await?;
    Ok(body)
}

// Concurrent execution with join_all
async fn fetch_all(urls: Vec<String>) -> Vec<Result<String>> {
    let futures: Vec<_> = urls.iter().map(|url| fetch_data(url)).collect();
    futures::future::join_all(futures).await
}

// Select multiple futures - first to complete wins
async fn fetch_with_fallback(primary: &str, fallback: &str) -> Result<String> {
    tokio::select! {
        result = fetch_data(primary) => result,
        result = fetch_data(fallback) => result,
    }
}

// Timeout for async operations
async fn fetch_with_timeout(url: &str) -> Result<String> {
    timeout(Duration::from_secs(5), fetch_data(url))
        .await
        .context("Request timed out")?
}

// Shared state with Arc<Mutex<T>>
struct AppState {
    counter: Arc<Mutex<u64>>,
    cache: Arc<RwLock<HashMap<String, String>>>,
}

impl AppState {
    async fn increment(&self) -> u64 {
        let mut counter = self.counter.lock().await;
        *counter += 1;
        *counter
    }

    // RwLock for read-heavy workloads
    async fn get_cached(&self, key: &str) -> Option<String> {
        let cache = self.cache.read().await;
        cache.get(key).cloned()
    }

    async fn update_cache(&self, key: String, value: String) {
        let mut cache = self.cache.write().await;
        cache.insert(key, value);
    }
}

// Channel communication patterns
async fn producer_consumer() {
    let (tx, mut rx) = mpsc::channel(32);

    // Producer task
    tokio::spawn(async move {
        for i in 0..10 {
            if tx.send(i).await.is_err() {
                break; // Receiver dropped
            }
        }
    });

    // Consumer
    while let Some(value) = rx.recv().await {
        println!("Received: {}", value);
    }
}

// Multiple producers with broadcast
use tokio::sync::broadcast;

async fn broadcast_example() {
    let (tx, mut rx1) = broadcast::channel(16);
    let mut rx2 = tx.subscribe();

    tokio::spawn(async move {
        tx.send("message").unwrap();
    });

    tokio::join!(
        async { println!("rx1: {:?}", rx1.recv().await) },
        async { println!("rx2: {:?}", rx2.recv().await) },
    );
}

// Oneshot for single-value communication
use tokio::sync::oneshot;

async fn compute_task() -> i32 {
    sleep(Duration::from_secs(1)).await;
    42
}

async fn oneshot_example() {
    let (tx, rx) = oneshot::channel();

    tokio::spawn(async move {
        let result = compute_task().await;
        let _ = tx.send(result);
    });

    match rx.await {
        Ok(value) => println!("Got: {}", value),
        Err(_) => println!("Sender dropped"),
    }
}

// Spawning blocking tasks
async fn cpu_intensive_work() -> Result<String> {
    tokio::task::spawn_blocking(|| {
        // CPU-intensive operation that would block async runtime
        std::thread::sleep(Duration::from_secs(2));
        "done".to_string()
    })
    .await
    .context("Task panicked")
}

// Tokio runtime setup
fn main() {
    // Multi-threaded runtime
    let runtime = tokio::runtime::Runtime::new().unwrap();
    runtime.block_on(async {
        fetch_data("http://example.com").await.ok();
    });

    // Or use the macro
    #[tokio::main]
    async fn main() {
        // async main function
    }

    // Single-threaded runtime for lightweight apps
    #[tokio::main(flavor = "current_thread")]
    async fn main() {
        // async main with single thread
    }
}
```

## Common Patterns

### Error Handling Patterns

```rust
use thiserror::Error;
use anyhow::{Context, Result, bail, ensure};
use std::io;

// Library error types with thiserror
#[derive(Error, Debug)]
pub enum ParseError {
    #[error("IO error: {0}")]
    Io(#[from] io::Error),

    #[error("Invalid syntax at line {line}, column {column}: {message}")]
    Syntax {
        line: usize,
        column: usize,
        message: String,
    },

    #[error("Unknown token: {0}")]
    UnknownToken(String),

    #[error("Expected {expected}, found {found}")]
    Unexpected { expected: String, found: String },
}

// Application error types with context
pub type AppResult<T> = Result<T, AppError>;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Parse error")]
    Parse(#[from] ParseError),

    #[error("Configuration error: {0}")]
    Config(String),

    #[error("Stage not found: {0}")]
    StageNotFound(String),

    #[error(transparent)]
    Other(#[from] anyhow::Error),
}

// Error context chain
fn load_and_parse_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read config file: {}", path))?;

    let config: Config = toml::from_str(&content)
        .with_context(|| format!("Failed to parse TOML in {}", path))?;

    validate_config(&config)
        .context("Config validation failed")?;

    Ok(config)
}

// Early validation with ensure
fn validate_config(config: &Config) -> Result<()> {
    ensure!(!config.name.is_empty(), "Config name cannot be empty");
    ensure!(config.port > 0, "Port must be greater than 0");
    ensure!(config.port < 65536, "Port must be less than 65536");

    if config.stages.is_empty() {
        bail!("Config must have at least one stage");
    }

    Ok(())
}

// Option to Result conversion patterns
fn get_stage(id: &str) -> Result<Stage> {
    let stage = find_stage(id)
        .ok_or_else(|| AppError::StageNotFound(id.to_string()))?;
    Ok(stage)
}

// Result unwrapping strategies
fn result_handling_examples() {
    let result: Result<String> = fetch_data();

    // Propagate with ?
    let data = result?;

    // Provide default
    let data = result.unwrap_or_default();
    let data = result.unwrap_or_else(|| "fallback".to_string());

    // Convert error type
    let data = result.map_err(|e| AppError::Other(e))?;

    // Explicit handling
    let data = match result {
        Ok(d) => d,
        Err(e) => {
            log::error!("Failed to fetch: {}", e);
            return Err(e);
        }
    };

    // Inspect without consuming
    if let Err(ref e) = result {
        log::warn!("Warning: {}", e);
    }

    // Chain operations
    let processed = result
        .and_then(|data| parse(&data))
        .and_then(|parsed| validate(&parsed))
        .map(|validated| transform(validated))?;
}

// Multiple error sources
fn multiple_operations() -> Result<()> {
    let file1 = std::fs::read_to_string("file1.txt")
        .context("Failed to read file1")?;
    let file2 = std::fs::read_to_string("file2.txt")
        .context("Failed to read file2")?;

    let result = process(&file1, &file2)
        .context("Failed to process files")?;

    save_result(&result)
        .context("Failed to save result")?;

    Ok(())
}

// Collecting Results
fn process_all_files(paths: &[&str]) -> Result<Vec<Content>> {
    // Stop on first error
    paths.iter()
        .map(|path| load_file(path))
        .collect::<Result<Vec<_>>>()
}

fn process_all_files_partial(paths: &[&str]) -> Vec<Result<Content>> {
    // Continue on errors, return all results
    paths.iter()
        .map(|path| load_file(path))
        .collect()
}

fn process_all_files_separate(paths: &[&str]) -> (Vec<Content>, Vec<anyhow::Error>) {
    // Separate successes from failures
    let results: Vec<_> = paths.iter()
        .map(|path| load_file(path))
        .collect();

    let mut successes = Vec::new();
    let mut failures = Vec::new();

    for result in results {
        match result {
            Ok(content) => successes.push(content),
            Err(e) => failures.push(e),
        }
    }

    (successes, failures)
}
```

### Builder Pattern

```rust
#[derive(Default)]
pub struct RequestBuilder {
    url: Option<String>,
    method: Method,
    headers: HashMap<String, String>,
    body: Option<Vec<u8>>,
    timeout: Duration,
}

impl RequestBuilder {
    pub fn new() -> Self {
        Self {
            method: Method::GET,
            timeout: Duration::from_secs(30),
            ..Default::default()
        }
    }

    pub fn url(mut self, url: impl Into<String>) -> Self {
        self.url = Some(url.into());
        self
    }

    pub fn method(mut self, method: Method) -> Self {
        self.method = method;
        self
    }

    pub fn header(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.headers.insert(key.into(), value.into());
        self
    }

    pub fn body(mut self, body: impl Into<Vec<u8>>) -> Self {
        self.body = Some(body.into());
        self
    }

    pub fn build(self) -> Result<Request, BuildError> {
        let url = self.url.ok_or(BuildError::MissingUrl)?;
        Ok(Request {
            url,
            method: self.method,
            headers: self.headers,
            body: self.body,
            timeout: self.timeout,
        })
    }
}
```

### Newtype Pattern

```rust
// Type safety through newtype
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct UserId(String);

impl UserId {
    pub fn new(id: impl Into<String>) -> Self {
        UserId(id.into())
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct OrderId(String);

// Now these are different types - can't mix them up
fn get_user(id: UserId) -> Option<User> { /* ... */ }
fn get_order(id: OrderId) -> Option<Order> { /* ... */ }
```

### Smart Pointers and Interior Mutability

```rust
use std::rc::Rc;
use std::sync::{Arc, Mutex, RwLock};
use std::cell::{RefCell, Cell};

// Box - heap allocation, single owner
fn box_example() {
    // Large value on heap instead of stack
    let large_data = Box::new([0u8; 10000]);

    // Recursive types require Box
    enum List {
        Cons(i32, Box<List>),
        Nil,
    }
}

// Rc - shared ownership (single-threaded)
fn rc_example() {
    let shared = Rc::new(vec![1, 2, 3]);
    let ref1 = Rc::clone(&shared);
    let ref2 = Rc::clone(&shared);

    println!("Reference count: {}", Rc::strong_count(&shared)); // 3

    // Check before cloning
    if Rc::strong_count(&shared) < 10 {
        let ref3 = Rc::clone(&shared);
    }
}

// Arc - shared ownership (multi-threaded)
fn arc_example() {
    let shared = Arc::new(vec![1, 2, 3]);

    let handles: Vec<_> = (0..5)
        .map(|i| {
            let data = Arc::clone(&shared);
            std::thread::spawn(move || {
                println!("Thread {}: {:?}", i, data);
            })
        })
        .collect();

    for handle in handles {
        handle.join().unwrap();
    }
}

// RefCell - interior mutability (single-threaded)
fn refcell_example() {
    let data = RefCell::new(vec![1, 2, 3]);

    // Multiple immutable borrows
    {
        let borrow1 = data.borrow();
        let borrow2 = data.borrow();
        println!("{:?}", borrow1);
    } // Borrows dropped here

    // Mutable borrow
    data.borrow_mut().push(4);

    // try_borrow for runtime check
    match data.try_borrow_mut() {
        Ok(mut b) => b.push(5),
        Err(_) => println!("Already borrowed"),
    }
}

// Cell - interior mutability for Copy types
fn cell_example() {
    let counter = Cell::new(0);

    let increment = || {
        let current = counter.get();
        counter.set(current + 1);
    };

    increment();
    increment();
    assert_eq!(counter.get(), 2);
}

// Arc<Mutex<T>> - shared mutable state (multi-threaded)
fn arc_mutex_example() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = std::thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}

// Arc<RwLock<T>> - read-heavy workloads
fn arc_rwlock_example() {
    let cache = Arc::new(RwLock::new(HashMap::new()));

    // Multiple readers
    let readers: Vec<_> = (0..5)
        .map(|i| {
            let cache = Arc::clone(&cache);
            std::thread::spawn(move || {
                let cache = cache.read().unwrap();
                if let Some(value) = cache.get(&i) {
                    println!("Read: {}", value);
                }
            })
        })
        .collect();

    // Single writer
    let writer = {
        let cache = Arc::clone(&cache);
        std::thread::spawn(move || {
            let mut cache = cache.write().unwrap();
            cache.insert(0, "value".to_string());
        })
    };

    for reader in readers {
        reader.join().unwrap();
    }
    writer.join().unwrap();
}

// Rc<RefCell<T>> - shared mutable state (single-threaded)
struct Node {
    value: i32,
    children: Vec<Rc<RefCell<Node>>>,
}

fn rc_refcell_tree() {
    let root = Rc::new(RefCell::new(Node {
        value: 1,
        children: vec![],
    }));

    let child = Rc::new(RefCell::new(Node {
        value: 2,
        children: vec![],
    }));

    root.borrow_mut().children.push(Rc::clone(&child));

    // Modify child through shared reference
    child.borrow_mut().value = 3;
}

// Weak references to prevent cycles
use std::rc::Weak;

struct Parent {
    children: Vec<Rc<RefCell<Child>>>,
}

struct Child {
    parent: Weak<RefCell<Parent>>,
}

fn weak_reference_example() {
    let parent = Rc::new(RefCell::new(Parent { children: vec![] }));

    let child = Rc::new(RefCell::new(Child {
        parent: Rc::downgrade(&parent),
    }));

    parent.borrow_mut().children.push(Rc::clone(&child));

    // Access parent from child
    if let Some(parent) = child.borrow().parent.upgrade() {
        println!("Parent exists");
    }
}

// Pattern: Interior mutability for caching
struct Database {
    cache: RefCell<HashMap<String, String>>,
}

impl Database {
    fn get(&self, key: &str) -> Option<String> {
        // Check cache with immutable self
        if let Some(value) = self.cache.borrow().get(key) {
            return Some(value.clone());
        }

        // Fetch from database
        let value = self.fetch_from_db(key)?;

        // Update cache with immutable self
        self.cache.borrow_mut().insert(key.to_string(), value.clone());

        Some(value)
    }

    fn fetch_from_db(&self, key: &str) -> Option<String> {
        // Database query
        None
    }
}
```

### Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic() {
        let result = add(2, 3);
        assert_eq!(result, 5);
    }

    #[test]
    fn test_with_result() -> Result<(), Box<dyn Error>> {
        let config = parse_config("valid config")?;
        assert_eq!(config.name, "test");
        Ok(())
    }

    #[test]
    #[should_panic(expected = "divide by zero")]
    fn test_panic() {
        divide(1, 0);
    }

    // Async tests with tokio
    #[tokio::test]
    async fn test_async_function() {
        let result = fetch_data("http://example.com").await;
        assert!(result.is_ok());
    }

    // Property-based testing with proptest
    use proptest::prelude::*;

    proptest! {
        #[test]
        fn test_parse_roundtrip(s in "[a-z]+") {
            let parsed = parse(&s)?;
            let serialized = serialize(&parsed);
            prop_assert_eq!(s, serialized);
        }
    }
}
```

## Anti-Patterns

### Avoid These Practices

```rust
// BAD: Unnecessary clone
fn process(items: &Vec<String>) {
    for item in items.clone() {  // Unnecessary allocation
        println!("{}", item);
    }
}

// GOOD: Iterate by reference
fn process(items: &[String]) {
    for item in items {
        println!("{}", item);
    }
}

// BAD: Using unwrap/expect in library code
fn parse_config(s: &str) -> Config {
    serde_json::from_str(s).unwrap()  // Panics on invalid input
}

// GOOD: Return Result and let caller handle errors
fn parse_config(s: &str) -> Result<Config, serde_json::Error> {
    serde_json::from_str(s)
}

// BAD: Excessive use of Rc<RefCell<T>>
struct Node {
    value: i32,
    children: Vec<Rc<RefCell<Node>>>,
}

// GOOD: Consider arena allocation or indices
struct Arena {
    nodes: Vec<Node>,
}
struct Node {
    value: i32,
    children: Vec<usize>,  // Indices into arena
}

// BAD: String concatenation in loops
fn build_message(parts: &[&str]) -> String {
    let mut result = String::new();
    for part in parts {
        result = result + part + ", ";  // Creates new String each iteration
    }
    result
}

// GOOD: Use push_str or collect
fn build_message(parts: &[&str]) -> String {
    parts.join(", ")
}

// BAD: Boxing errors unnecessarily
fn parse(s: &str) -> Result<Data, Box<dyn Error>> {
    // For libraries, use concrete error types
}

// GOOD: Use concrete error types in libraries
fn parse(s: &str) -> Result<Data, ParseError> {
    // thiserror for library errors, anyhow for applications
}

// BAD: Unsafe without justification
unsafe fn get_unchecked(slice: &[i32], index: usize) -> i32 {
    *slice.get_unchecked(index)
}

// GOOD: Safe by default, unsafe with clear invariants
fn get_unchecked(slice: &[i32], index: usize) -> i32 {
    // SAFETY: Caller must ensure index < slice.len()
    // Only use when bounds checking is a proven bottleneck
    debug_assert!(index < slice.len());
    unsafe { *slice.get_unchecked(index) }
}

// BAD: Ignoring must_use
let _ = fs::remove_file("temp.txt");  // Error silently ignored

// GOOD: Handle the result
fs::remove_file("temp.txt").ok();  // Explicitly ignore
// or
fs::remove_file("temp.txt")?;  // Propagate error
```
