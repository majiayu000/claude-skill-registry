---
name: cli-tool
description: |
  Build command-line tools with argument parsing, subcommands, and nice UX.
  Use when: creating CLI, terminal app, command-line utility.
  Triggers: "cli", "command line", "terminal", "clap", "typer", "commander".
---

# CLI Tool Development

## Project Protection Setup

**MANDATORY before writing any code:**

```bash
# 1. Create .gitignore
cat >> .gitignore << 'EOF'
# Build
target/
node_modules/
__pycache__/
dist/

# Config with secrets
config.toml
*.key
credentials.json

# IDE
.idea/
.vscode/
.DS_Store
EOF

# 2. Setup pre-commit hooks
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: detect-private-key
      - id: check-added-large-files
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
EOF

pre-commit install
```

---

## Stack Options

| Language | Framework | Best For |
|----------|-----------|----------|
| **Rust** | clap (derive) | Fast binaries, type safety |
| **Python** | typer / click | Rapid development |
| **Node** | commander / yargs | JS ecosystem |

---

## Quick Start

### Rust (clap derive)

```toml
# Cargo.toml
[dependencies]
clap = { version = "4", features = ["derive"] }
anyhow = "1"
```

```rust
use clap::Parser;

#[derive(Parser)]
#[command(name = "mytool")]
#[command(about = "A sample CLI tool")]
struct Cli {
    /// Input file
    input: String,

    /// Output file
    #[arg(short, long, default_value = "output.txt")]
    output: String,

    /// Verbose output
    #[arg(short, long)]
    verbose: bool,
}

fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();

    if cli.verbose {
        println!("Input: {}", cli.input);
        println!("Output: {}", cli.output);
    }

    // Do work...
    Ok(())
}
```

### Python (typer)

```python
# requirements.txt
typer[all]>=0.9
```

```python
import typer

app = typer.Typer()

@app.command()
def main(
    input: str = typer.Argument(..., help="Input file"),
    output: str = typer.Option("output.txt", "--output", "-o", help="Output file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """A sample CLI tool."""
    if verbose:
        typer.echo(f"Input: {input}")
        typer.echo(f"Output: {output}")

if __name__ == "__main__":
    app()
```

### Node (commander)

```typescript
// package.json: "commander": "^12"
import { program } from 'commander';

program
  .name('mytool')
  .description('A sample CLI tool')
  .argument('<input>', 'Input file')
  .option('-o, --output <file>', 'Output file', 'output.txt')
  .option('-v, --verbose', 'Verbose output')
  .action((input, options) => {
    if (options.verbose) {
      console.log(`Input: ${input}`);
      console.log(`Output: ${options.output}`);
    }
  });

program.parse();
```

---

## Subcommands

### Rust

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "mytool")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Add a new item
    Add {
        /// Item name
        name: String,
    },
    /// List all items
    List {
        /// Show detailed info
        #[arg(short, long)]
        detailed: bool,
    },
    /// Remove an item
    Remove {
        /// Item ID
        id: u32,
    },
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Add { name } => println!("Adding: {}", name),
        Commands::List { detailed } => println!("Listing (detailed: {})", detailed),
        Commands::Remove { id } => println!("Removing: {}", id),
    }
}
```

### Python

```python
import typer

app = typer.Typer()

@app.command()
def add(name: str):
    """Add a new item."""
    typer.echo(f"Adding: {name}")

@app.command()
def list(detailed: bool = typer.Option(False, "--detailed", "-d")):
    """List all items."""
    typer.echo(f"Listing (detailed: {detailed})")

@app.command()
def remove(id: int):
    """Remove an item."""
    typer.echo(f"Removing: {id}")

if __name__ == "__main__":
    app()
```

---

## Output Formats

### Text / JSON / Table

```rust
use clap::ValueEnum;
use serde::Serialize;

#[derive(ValueEnum, Clone)]
enum OutputFormat {
    Text,
    Json,
    Table,
}

#[derive(Serialize)]
struct Item {
    id: u32,
    name: String,
}

fn output(items: &[Item], format: OutputFormat) {
    match format {
        OutputFormat::Text => {
            for item in items {
                println!("{}: {}", item.id, item.name);
            }
        }
        OutputFormat::Json => {
            println!("{}", serde_json::to_string_pretty(items).unwrap());
        }
        OutputFormat::Table => {
            println!("{:<5} {}", "ID", "Name");
            println!("{}", "-".repeat(20));
            for item in items {
                println!("{:<5} {}", item.id, item.name);
            }
        }
    }
}
```

### Python (rich)

```python
from rich.console import Console
from rich.table import Table
import json

console = Console()

def output(items: list, format: str):
    if format == "text":
        for item in items:
            console.print(f"{item['id']}: {item['name']}")
    elif format == "json":
        console.print_json(json.dumps(items))
    elif format == "table":
        table = Table()
        table.add_column("ID")
        table.add_column("Name")
        for item in items:
            table.add_row(str(item["id"]), item["name"])
        console.print(table)
```

---

## Progress Bars

### Rust (indicatif)

```rust
use indicatif::{ProgressBar, ProgressStyle};

let pb = ProgressBar::new(100);
pb.set_style(ProgressStyle::default_bar()
    .template("{spinner:.green} [{bar:40.cyan/blue}] {pos}/{len} {msg}")
    .unwrap());

for i in 0..100 {
    pb.set_position(i);
    pb.set_message(format!("Processing item {}", i));
    std::thread::sleep(std::time::Duration::from_millis(50));
}
pb.finish_with_message("Done!");
```

### Python (rich)

```python
from rich.progress import track

for item in track(range(100), description="Processing..."):
    # Do work
    pass
```

---

## Config Files

### Rust (config crate)

```rust
use config::{Config, File};
use serde::Deserialize;

#[derive(Deserialize)]
struct Settings {
    api_key: String,
    timeout: u64,
}

fn load_config() -> anyhow::Result<Settings> {
    let settings = Config::builder()
        .add_source(File::with_name("config.toml").required(false))
        .add_source(config::Environment::with_prefix("MYTOOL"))
        .build()?;

    Ok(settings.try_deserialize()?)
}
```

```toml
# config.toml
api_key = "your-key"
timeout = 30
```

### Python

```python
import tomllib
from pathlib import Path

def load_config():
    config_path = Path.home() / ".config" / "mytool" / "config.toml"
    if config_path.exists():
        return tomllib.loads(config_path.read_text())
    return {}
```

---

## Exit Codes

```rust
use std::process::ExitCode;

fn main() -> ExitCode {
    match run() {
        Ok(_) => ExitCode::SUCCESS,
        Err(e) => {
            eprintln!("Error: {}", e);
            ExitCode::FAILURE
        }
    }
}
```

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse of command |
| 126 | Permission denied |
| 127 | Command not found |

---

## Shell Completions

### Rust (clap)

```rust
use clap::CommandFactory;
use clap_complete::{generate, Shell};

#[derive(Parser)]
struct Cli {
    #[arg(long, value_enum)]
    completions: Option<Shell>,
}

fn main() {
    let cli = Cli::parse();

    if let Some(shell) = cli.completions {
        let mut cmd = Cli::command();
        generate(shell, &mut cmd, "mytool", &mut std::io::stdout());
        return;
    }
}
```

Usage:
```bash
# Generate completions
mytool --completions bash > ~/.local/share/bash-completion/completions/mytool
mytool --completions zsh > ~/.zfunc/_mytool
```

---

## Interactive Prompts

### Rust (dialoguer)

```rust
use dialoguer::{Confirm, Input, Select};

let name: String = Input::new()
    .with_prompt("Your name")
    .interact_text()?;

let proceed = Confirm::new()
    .with_prompt("Continue?")
    .interact()?;

let options = vec!["Option 1", "Option 2", "Option 3"];
let selection = Select::new()
    .with_prompt("Choose")
    .items(&options)
    .interact()?;
```

### Python (rich)

```python
from rich.prompt import Prompt, Confirm

name = Prompt.ask("Your name")
proceed = Confirm.ask("Continue?")
```

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| No help text | Add descriptions to all args |
| Poor error messages | Use anyhow/thiserror with context |
| No colors in pipes | Detect TTY, use `--color=always` |
| Slow startup | Lazy init, avoid heavy deps |
| No config file | Support `~/.config/tool/config.toml` |

---

## Testing

### Rust (clap)

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use assert_cmd::Command;
    use predicates::prelude::*;

    #[test]
    fn test_cli_help() {
        Command::cargo_bin("mytool")
            .unwrap()
            .arg("--help")
            .assert()
            .success()
            .stdout(predicate::str::contains("Usage"));
    }

    #[test]
    fn test_cli_version() {
        Command::cargo_bin("mytool")
            .unwrap()
            .arg("--version")
            .assert()
            .success();
    }

    #[test]
    fn test_add_command() {
        Command::cargo_bin("mytool")
            .unwrap()
            .args(["add", "test-item"])
            .assert()
            .success()
            .stdout(predicate::str::contains("Added"));
    }

    #[test]
    fn test_invalid_input_fails() {
        Command::cargo_bin("mytool")
            .unwrap()
            .args(["add"])  // Missing required arg
            .assert()
            .failure();
    }
}
```

### Python (typer)

```python
from typer.testing import CliRunner
from myapp import app

runner = CliRunner()

def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output

def test_add_command():
    result = runner.invoke(app, ["add", "test-item"])
    assert result.exit_code == 0
    assert "Added" in result.output

def test_invalid_input():
    result = runner.invoke(app, ["add"])  # Missing arg
    assert result.exit_code != 0
```

### Node (commander)

```typescript
import { describe, it, expect } from 'vitest';
import { execSync } from 'child_process';

describe('CLI', () => {
  it('shows help', () => {
    const output = execSync('node dist/cli.js --help').toString();
    expect(output).toContain('Usage');
  });

  it('adds item', () => {
    const output = execSync('node dist/cli.js add test-item').toString();
    expect(output).toContain('Added');
  });
});
```

---

## TDD Workflow

```
1. Task[tdd-test-writer]: "Create 'add' subcommand"
   → Writes assert_cmd test
   → cargo test → FAILS (RED)

2. Task[rust-developer]: "Implement 'add' subcommand"
   → Implements minimal code
   → cargo test → PASSES (GREEN)

3. Repeat for each subcommand

4. Task[code-reviewer]: "Review CLI implementation"
   → Checks error messages, exit codes, edge cases
```

---

## Security Checklist

- [ ] No secrets in default config
- [ ] Config file permissions checked (600 for sensitive)
- [ ] Input sanitized before shell execution
- [ ] No command injection in subprocesses
- [ ] Secure temp file handling
- [ ] Credentials stored in OS keyring (if needed)

---

## Project Structure

```
mytool/
├── src/
│   ├── main.rs
│   ├── cli.rs      # Argument definitions
│   ├── commands/   # Subcommand implementations
│   │   ├── mod.rs
│   │   ├── add.rs
│   │   └── list.rs
│   └── config.rs
├── tests/
│   └── cli_tests.rs  # Integration tests
├── Cargo.toml
├── config.example.toml
└── README.md
```
