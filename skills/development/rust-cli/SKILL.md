---
name: rust-cli
description: Build professional CLI applications with clap and TUI
sasmp_version: "1.3.0"
bonded_agent: rust-project-agent
bond_type: SECONDARY_BOND
version: "1.0.0"
---

# Rust CLI Skill

Build professional command-line applications with clap, colored output, and interactive features.

## Quick Start

### Basic CLI with Clap

```toml
[dependencies]
clap = { version = "4", features = ["derive"] }
anyhow = "1"
```

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "myapp", version, about)]
struct Cli {
    #[arg(short, long)]
    verbose: bool,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Init { name: String },
    Build { #[arg(short, long)] release: bool },
}

fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Init { name } => println!("Creating: {}", name),
        Commands::Build { release } => println!("Building..."),
    }
    Ok(())
}
```

### Colored Output

```rust
use colored::Colorize;

println!("{}", "Success!".green().bold());
println!("{}", "Error!".red());
```

### Progress Bars

```rust
use indicatif::{ProgressBar, ProgressStyle};

let pb = ProgressBar::new(100);
pb.set_style(ProgressStyle::default_bar()
    .template("{bar:40} {pos}/{len}")?);

for _ in 0..100 {
    pb.inc(1);
}
pb.finish();
```

### Interactive Prompts

```rust
use dialoguer::{Confirm, Input, Select};

let name: String = Input::new()
    .with_prompt("Project name")
    .interact_text()?;

if Confirm::new().with_prompt("Continue?").interact()? {
    // proceed
}
```

## Common Patterns

### Error Handling

```rust
fn main() {
    if let Err(e) = run() {
        eprintln!("{}: {}", "error".red(), e);
        std::process::exit(1);
    }
}
```

### Testing CLI

```rust
use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_help() {
    Command::cargo_bin("myapp").unwrap()
        .arg("--help")
        .assert()
        .success();
}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Args not parsed | Add `features = ["derive"]` |
| Colors not showing | Check terminal support |

## Resources

- [clap docs](https://docs.rs/clap)
- [Rust CLI Book](https://rust-cli.github.io/book/)
