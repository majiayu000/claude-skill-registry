---
name: Clap CLI Framework
description: Command-line argument parsing with derive macros.
metadata:
  labels: [rust, clap, cli, args]
  triggers:
    files: ['**/main.rs', '**/cli.rs']
    keywords: [clap, Parser, Subcommand, Args, command]
---

# Clap Standards

## Basic CLI

```rust
use clap::Parser;

#[derive(Parser)]
#[command(name = "myapp")]
#[command(version, about, long_about = None)]
struct Cli {
    /// Name to greet
    #[arg(short, long)]
    name: String,

    /// Number of times to greet
    #[arg(short, long, default_value_t = 1)]
    count: u8,

    /// Enable verbose output
    #[arg(short, long)]
    verbose: bool,
}

fn main() {
    let cli = Cli::parse();
    for _ in 0..cli.count {
        println!("Hello, {}!", cli.name);
    }
}
```

## Subcommands

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "git-like")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Add files to staging
    Add {
        #[arg(required = true)]
        files: Vec<String>,
    },
    /// Commit changes
    Commit {
        #[arg(short, long)]
        message: String,
    },
    /// Push to remote
    Push {
        #[arg(short, long, default_value = "origin")]
        remote: String,
    },
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Add { files } => println!("Adding: {:?}", files),
        Commands::Commit { message } => println!("Commit: {}", message),
        Commands::Push { remote } => println!("Push to {}", remote),
    }
}
```

## Argument Types

```rust
use std::path::PathBuf;
use clap::{Parser, ValueEnum};

#[derive(Copy, Clone, ValueEnum)]
enum Format {
    Json,
    Yaml,
    Toml,
}

#[derive(Parser)]
struct Cli {
    /// Input file
    #[arg(short, long, value_name = "FILE")]
    input: PathBuf,

    /// Output format
    #[arg(short, long, value_enum, default_value_t = Format::Json)]
    format: Format,

    /// Port number (1-65535)
    #[arg(short, long, value_parser = clap::value_parser!(u16).range(1..))]
    port: u16,

    /// Environment variables
    #[arg(short, long, value_parser = parse_key_val)]
    env: Vec<(String, String)>,
}

fn parse_key_val(s: &str) -> Result<(String, String), String> {
    let pos = s.find('=').ok_or("no `=` found")?;
    Ok((s[..pos].to_string(), s[pos + 1..].to_string()))
}
```

## Global Arguments

```rust
#[derive(Parser)]
struct Cli {
    #[command(flatten)]
    global: GlobalArgs,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Args)]
struct GlobalArgs {
    /// Config file path
    #[arg(short, long, global = true)]
    config: Option<PathBuf>,

    /// Verbose mode
    #[arg(short, long, global = true)]
    verbose: bool,
}
```

## Validation

```rust
use clap::Parser;

#[derive(Parser)]
struct Cli {
    /// Must be positive
    #[arg(value_parser = positive_number)]
    count: i32,

    /// Must exist
    #[arg(value_parser = existing_path)]
    path: PathBuf,
}

fn positive_number(s: &str) -> Result<i32, String> {
    let n: i32 = s.parse().map_err(|_| "not a number")?;
    if n <= 0 { return Err("must be positive".into()); }
    Ok(n)
}

fn existing_path(s: &str) -> Result<PathBuf, String> {
    let path = PathBuf::from(s);
    if !path.exists() { return Err("path does not exist".into()); }
    Ok(path)
}
```

## Environment Variables

```rust
#[derive(Parser)]
struct Cli {
    /// API key (or MYAPP_API_KEY env var)
    #[arg(short, long, env = "MYAPP_API_KEY")]
    api_key: String,

    /// Database URL
    #[arg(long, env)]  // Uses MYAPP_DATABASE_URL
    database_url: String,
}
```

## Shell Completions

```rust
use clap::CommandFactory;
use clap_complete::{generate, Shell};

fn generate_completions(shell: Shell) {
    let mut cmd = Cli::command();
    generate(shell, &mut cmd, "myapp", &mut std::io::stdout());
}

// Build script (build.rs)
fn main() {
    let outdir = std::env::var("OUT_DIR").unwrap();
    let mut cmd = Cli::command();
    for shell in [Shell::Bash, Shell::Zsh, Shell::Fish] {
        clap_complete::generate_to(shell, &mut cmd, "myapp", &outdir).unwrap();
    }
}
```

## Best Practices

1. **Derive API**: Prefer over builder for most cases
2. **Help text**: Use doc comments (`///`) for descriptions
3. **Defaults**: Provide sensible defaults with `default_value`
4. **Validation**: Use `value_parser` for custom validation
5. **Env vars**: Support config via environment with `env`
