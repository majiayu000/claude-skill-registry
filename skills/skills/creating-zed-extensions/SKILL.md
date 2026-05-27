---
name: creating-zed-extensions
description: Use when creating Zed extensions with custom slash commands, language support, themes, or MCP servers - provides Rust/WASM extension structure, slash command API (run_slash_command, SlashCommandOutput), and development workflow for compiled extensions
---

# Creating Zed Extensions

## Overview

Zed extensions are Rust programs compiled to WebAssembly that can provide slash commands, language support, themes, grammars, and MCP servers. Extensions implement the `zed::Extension` trait and are distributed via Zed's extension registry.

## When to Use

**Create a Zed extension when:**
- Adding custom slash commands to the Assistant (`/deploy`, `/analyze`, `/fetch-docs`)
- Providing language support (syntax highlighting, LSP, formatting)
- Creating custom color themes
- Integrating external tools via slash commands
- Providing MCP server integrations

**Don't create for:**
- Simple rules or instructions (use `.rules` files)
- One-time scripts (use terminal)
- Project-specific configuration (use `.zed/settings.json`)

## Quick Reference

### Extension Structure

```
my-extension/
├── Cargo.toml              # Rust manifest
├── extension.toml          # Extension metadata
└── src/
    └── lib.rs             # Extension implementation
```

### Minimal Slash Command Extension

```toml
# extension.toml
id = "my-commands"
name = "My Commands"
version = "0.1.0"
authors = ["Your Name"]
repository = "https://github.com/username/my-commands"
license = "MIT"

[slash_commands.echo]
description = "echoes the provided input"
requires_argument = true

[slash_commands.greet]
description = "greets the user"
requires_argument = false
```

```rust
// src/lib.rs
use zed_extension_api::{self as zed, Result, SlashCommand, SlashCommandOutput};

struct MyExtension;

impl zed::Extension for MyExtension {
    fn run_slash_command(
        &self,
        command: SlashCommand,
        args: Vec<String>,
        _worktree: Option<&zed::Worktree>,
    ) -> Result<SlashCommandOutput> {
        match command.name.as_str() {
            "echo" => {
                if args.is_empty() {
                    return Err("echo requires an argument".to_string());
                }
                Ok(SlashCommandOutput {
                    text: args.join(" "),
                    sections: vec![],
                })
            }
            "greet" => {
                Ok(SlashCommandOutput {
                    text: "Hello! How can I help you today?".to_string(),
                    sections: vec![],
                })
            }
            _ => Err(format!("Unknown command: {}", command.name)),
        }
    }
}

zed::register_extension!(MyExtension);
```

```toml
# Cargo.toml
[package]
name = "my-extension"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
zed_extension_api = "0.1.0"
```

## Implementation

### Complete Example: Documentation Fetcher

```rust
// src/lib.rs
use zed_extension_api::{self as zed, Result, SlashCommand, SlashCommandOutput, SlashCommandOutputSection};
use std::process::Command;

struct DocsExtension;

impl zed::Extension for DocsExtension {
    fn run_slash_command(
        &self,
        command: SlashCommand,
        args: Vec<String>,
        worktree: Option<&zed::Worktree>,
    ) -> Result<SlashCommandOutput> {
        match command.name.as_str() {
            "docs" => self.fetch_docs(args, worktree),
            "api" => self.fetch_api_reference(args),
            _ => Err(format!("Unknown command: {}", command.name)),
        }
    }

    fn complete_slash_command_argument(
        &self,
        command: SlashCommand,
        _args: Vec<String>,
    ) -> Result<Vec<zed::SlashCommandArgumentCompletion>> {
        match command.name.as_str() {
            "docs" => Ok(vec![
                zed::SlashCommandArgumentCompletion {
                    label: "rust".to_string(),
                    new_text: "rust".to_string(),
                    run_command: true,
                },
                zed::SlashCommandArgumentCompletion {
                    label: "typescript".to_string(),
                    new_text: "typescript".to_string(),
                    run_command: true,
                },
                zed::SlashCommandArgumentCompletion {
                    label: "python".to_string(),
                    new_text: "python".to_string(),
                    run_command: true,
                },
            ]),
            _ => Ok(vec![]),
        }
    }
}

impl DocsExtension {
    fn fetch_docs(
        &self,
        args: Vec<String>,
        worktree: Option<&zed::Worktree>,
    ) -> Result<SlashCommandOutput> {
        if args.is_empty() {
            return Err("docs requires a topic (e.g., /docs rust)".to_string());
        }

        let topic = args.join(" ");
        let docs_url = format!("https://docs.rs/{}", topic);

        // Use worktree context if available
        let context = if let Some(wt) = worktree {
            format!("\nProject: {}", wt.root_path())
        } else {
            String::new()
        };

        let output_text = format!(
            "Documentation for: {}\nURL: {}{}\n\nFetching latest docs...",
            topic, docs_url, context
        );

        Ok(SlashCommandOutput {
            text: output_text.clone(),
            sections: vec![
                SlashCommandOutputSection {
                    range: (0..output_text.len()),
                    label: format!("Docs: {}", topic),
                },
            ],
        })
    }

    fn fetch_api_reference(&self, args: Vec<String>) -> Result<SlashCommandOutput> {
        if args.is_empty() {
            return Err("api requires a library name".to_string());
        }

        let library = &args[0];

        // Execute external command to fetch API docs
        let output = Command::new("curl")
            .args(&["-s", &format!("https://api.github.com/repos/{}/readme", library)])
            .output()
            .map_err(|e| format!("Failed to execute curl: {}", e))?;

        if !output.status.success() {
            return Err("Failed to fetch API documentation".to_string());
        }

        let response = String::from_utf8_lossy(&output.stdout);

        Ok(SlashCommandOutput {
            text: format!("API Reference for {}\n\n{}", library, response),
            sections: vec![],
        })
    }
}

zed::register_extension!(DocsExtension);
```

### Extension Manifest with All Fields

```toml
# extension.toml
id = "docs-fetcher"
name = "Documentation Fetcher"
description = "Fetch documentation and API references via slash commands"
version = "1.0.0"
authors = ["Developer Name <dev@example.com>"]
repository = "https://github.com/username/docs-fetcher"
license = "MIT"

[slash_commands.docs]
description = "fetch documentation for a topic"
requires_argument = true

[slash_commands.api]
description = "fetch API reference for a library"
requires_argument = true

[slash_commands.help]
description = "show available documentation commands"
requires_argument = false
```

## Development Workflow

### 1. Setup

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Add WASM target
rustup target add wasm32-wasip1

# Create extension directory
mkdir -p ~/.local/share/zed/extensions/my-extension
cd ~/.local/share/zed/extensions/my-extension
```

### 2. Build

```bash
# Compile to WASM
cargo build --release --target wasm32-wasip1

# WASM output location
# target/wasm32-wasip1/release/my_extension.wasm
```

### 3. Test Locally

```bash
# Zed automatically loads extensions from:
# macOS: ~/Library/Application Support/Zed/extensions/
# Linux: ~/.local/share/zed/extensions/

# Copy extension files
cp extension.toml ~/Library/Application\ Support/Zed/extensions/my-extension/
cp target/wasm32-wasip1/release/my_extension.wasm ~/Library/Application\ Support/Zed/extensions/my-extension/extension.wasm

# Restart Zed to load extension
```

### 4. Publish

```bash
# Extensions published via PR to zed-industries/extensions
# https://github.com/zed-industries/extensions

# Fork the repository
git clone https://github.com/zed-industries/extensions
cd extensions

# Add your extension
mkdir extensions/my-extension
cp -r ~/path/to/my-extension/* extensions/my-extension/

# Create PR with extension metadata
git checkout -b add-my-extension
git add extensions/my-extension
git commit -m "Add my-extension: Custom slash commands"
git push origin add-my-extension
```

## License Requirements

**Required licenses (as of October 1st, 2025):**
- MIT
- Apache-2.0
- BSD-3-Clause
- GPL-3.0

Extensions with other licenses will be rejected during review.

## Slash Command API Reference

### Types

```rust
// Command input
struct SlashCommand {
    name: String,
    // Additional metadata
}

// Command output
struct SlashCommandOutput {
    text: String,
    sections: Vec<SlashCommandOutputSection>,
}

struct SlashCommandOutputSection {
    range: (usize, usize),  // Character range in text
    label: String,          // Section label for UI
}

// Argument completion
struct SlashCommandArgumentCompletion {
    label: String,        // Display in completion menu
    new_text: String,     // Insert when selected
    run_command: bool,    // Execute immediately after selection
}
```

### Methods

```rust
trait Extension {
    // Required for slash commands
    fn run_slash_command(
        &self,
        command: SlashCommand,
        args: Vec<String>,
        worktree: Option<&Worktree>,
    ) -> Result<SlashCommandOutput, String>;

    // Optional: Argument autocompletion
    fn complete_slash_command_argument(
        &self,
        command: SlashCommand,
        args: Vec<String>,
    ) -> Result<Vec<SlashCommandArgumentCompletion>, String> {
        Ok(vec![])
    }
}
```

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Wrong crate type | WASM compilation fails | Use `crate-type = ["cdylib"]` in Cargo.toml |
| Missing error handling | Extension crashes | Return `Err(String)` for failures |
| Not validating args | Silent failures | Check `args.is_empty()` for required args |
| Hardcoded paths | Extension not portable | Use relative paths or worktree context |
| Missing default case | Unhandled commands crash | Add `_ => Err(...)` in match |
| Unlicensed extension | Rejected by registry | Include approved license in extension.toml |
| Blocking operations | Freezes Zed UI | Use async or spawn threads for long operations |

## Advanced Features

### Using Worktree Context

```rust
fn run_slash_command(
    &self,
    command: SlashCommand,
    args: Vec<String>,
    worktree: Option<&zed::Worktree>,
) -> Result<SlashCommandOutput> {
    if let Some(wt) = worktree {
        let project_root = wt.root_path();
        let config_path = format!("{}/config.json", project_root);

        // Read project-specific config
        let config = std::fs::read_to_string(config_path)
            .map_err(|e| format!("Failed to read config: {}", e))?;

        // Use config in command logic
    }

    // Continue command execution
}
```

### Output Sections for Structured Results

```rust
let output_text = format!(
    "# Results\n\n## Section 1\nContent here\n\n## Section 2\nMore content"
);

Ok(SlashCommandOutput {
    text: output_text.clone(),
    sections: vec![
        SlashCommandOutputSection {
            range: (0..12),        // "# Results"
            label: "Header".to_string(),
        },
        SlashCommandOutputSection {
            range: (14..40),       // "## Section 1\nContent here"
            label: "Section 1".to_string(),
        },
        SlashCommandOutputSection {
            range: (42..output_text.len()),
            label: "Section 2".to_string(),
        },
    ],
})
```

## Real-World Impact

**Productivity**: Custom `/deploy` command deploys directly from Assistant panel

**Documentation**: `/docs rust Vec` fetches Rust Vec documentation without leaving editor

**Integration**: `/gh issue 123` fetches GitHub issue details inline

**Workflow**: `/analyze-deps` shows dependency tree and suggests updates

---

**Schema Reference**: `packages/converters/schemas/zed-extension.schema.json`

**Documentation**: https://zed.dev/docs/extensions/developing-extensions

**Example Extension**: https://github.com/zed-industries/zed/tree/main/extensions/slash-commands-example
