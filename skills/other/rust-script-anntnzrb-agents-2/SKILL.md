---
name: rust-script
description: "Expert in rust-script for running Rust files as scripts without compilation setup. Activate when working with .rs or .ers script files, user mentions rust-script, cargo-script, or scripting Rust, writing one-off Rust scripts with dependencies, or using expr, loop, or inline dependency manifests. Proficient in idiomatic Rust patterns, error handling, async, and CLI tooling."
---

# rust-script Expert

Run Rust script files without explicit compilation, with seamless dependency management via embedded manifests.

## When This Skill Activates

- Working with `.rs` or `.ers` script files intended for rust-script
- User mentions `rust-script`, `cargo-script`, or "scripting Rust"
- Writing one-off Rust scripts with crate dependencies
- Using `--expr`, `--loop`, or inline `cargo` manifest blocks
- Debugging rust-script execution or dependency issues

## Quick Reference

### Running Scripts

```sh
# Basic execution
rust-script script.rs

# Evaluate expression (prints Debug output)
rust-script -e '1 + 1'
rust-script -e 'vec![1,2,3].iter().sum::<i32>()'

# With dependencies
rust-script -d serde -d "tokio=1" -e 'println!("deps loaded")'

# Filter stdin line-by-line
echo "hello" | rust-script -l '|line| line.to_uppercase()'

# With line numbers
cat file.txt | rust-script --count -l '|line, n| format!("{}: {}", n, line.trim())'

# Run tests
rust-script --test script.rs

# Debug build
rust-script --debug script.rs

# Force rebuild
rust-script --force script.rs

# Show cargo output
rust-script -c script.rs

# Use specific toolchain
rust-script -t nightly script.rs

# Benchmark with wrapper
rust-script --wrapper "hyperfine --runs 100" script.rs

# Debug with lldb
rust-script --debug --wrapper rust-lldb script.rs

# Generate package only (don't run)
rust-script --package script.rs
```

### Dependency Manifest Syntax

Use doc comments with a cargo code block:

```rust
#!/usr/bin/env rust-script
//! ```cargo
//! [dependencies]
//! serde = { version = "1.0", features = ["derive"] }
//! tokio = { version = "1", features = ["full"] }
//! anyhow = "1.0"
//! ```

use serde::{Serialize, Deserialize};

fn main() {
    // ...
}
```

### Including Relative Files

```rust
// Include a module relative to script location
mod helper {
    include!(concat!(env!("RUST_SCRIPT_BASE_PATH"), "/helper.rs"));
}

// Include text file
let data = include_str!(concat!(env!("RUST_SCRIPT_BASE_PATH"), "/data.txt"));
```

## Writing Idiomatic rust-script Code

### Error Handling

Return `Result` from main for clean error propagation:

```rust
#!/usr/bin/env rust-script
//! ```cargo
//! [dependencies]
//! anyhow = "1.0"
//! ```

use anyhow::Result;

fn main() -> Result<()> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        anyhow::bail!("Usage: {} <filename>", args[0]);
    }
    let content = std::fs::read_to_string(&args[1])?;
    println!("{}", content);
    Ok(())
}
```

### Async Scripts

```rust
#!/usr/bin/env rust-script
//! ```cargo
//! [dependencies]
//! tokio = { version = "1", features = ["full"] }
//! reqwest = "0.11"
//! ```

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let resp = reqwest::get("https://httpbin.org/ip").await?.text().await?;
    println!("{}", resp);
    Ok(())
}
```

### CLI Argument Parsing

```rust
#!/usr/bin/env rust-script
//! ```cargo
//! [dependencies]
//! clap = { version = "4", features = ["derive"] }
//! ```

use clap::Parser;

#[derive(Parser)]
#[command(name = "myscript")]
struct Args {
    /// Input file
    input: String,

    /// Verbose output
    #[arg(short, long)]
    verbose: bool,
}

fn main() {
    let args = Args::parse();
    if args.verbose {
        println!("Processing: {}", args.input);
    }
}
```

### Data Processing with Serde

```rust
#!/usr/bin/env rust-script
//! ```cargo
//! [dependencies]
//! serde = { version = "1.0", features = ["derive"] }
//! serde_json = "1.0"
//! ```

use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct Config {
    name: String,
    values: Vec<i32>,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let json = r#"{"name": "test", "values": [1, 2, 3]}"#;
    let config: Config = serde_json::from_str(json)?;
    println!("{:?}", config);
    Ok(())
}
```

## Troubleshooting

### Force Rebuild
If the script behaves unexpectedly after changes:
```sh
rust-script --force script.rs
```

### Clear Cache
Remove all cached compilations:
```sh
rust-script --clear-cache
```

### View Cargo Output
See compilation errors and warnings:
```sh
rust-script -c script.rs
```

### Debug Logging
Set environment variable for verbose output:
```sh
RUST_LOG=rust_script=trace rust-script script.rs
```

### Common Issues

1. **Script not rebuilding after changes**: Use `--force` or check that file modification time updated

2. **Dependencies not found**: Ensure proper manifest syntax - cargo block must be in doc comments (//! or ///)

## Research Tools

```
# gh search code for rust examples
gh search code "#[tokio::main]" --language=rust
gh search code "clap::Parser" --language=rust
gh search code "anyhow::Result" --language=rust
```

## Templates

See `templates/` directory for ready-to-use examples:
- `script.rs` - Standard script with dependencies
- `async.rs` - Async script with tokio
