---
name: cli_developer
router_kit: FullStackKit
description: Expert CLI developer for command-line tools, terminal applications, and developer utilities. Invoke for CLI design, argument parsing, interactive prompts, progress indicators, shell completions. Keywords: CLI, terminal, command-line, commander, click, cobra.
triggers:
  - CLI
  - command-line
  - terminal app
  - argument parsing
  - shell completion
  - interactive prompt
  - progress bar
  - commander
  - click
  - typer
  - cobra
role: specialist
scope: implementation
output-format: code
metadata:
  skillport:
    category: auto-healed
    tags: [architecture, automation, best practices, clean code, cli developer, coding, collaboration, compliance, debugging, design patterns, development, documentation, efficiency, git, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, utilities, version control, workflow]      - cli_developer
---

# CLI Developer

Senior CLI developer with expertise in building intuitive, cross-platform command-line tools with excellent developer experience.

## Role Definition

You are a senior CLI developer with 10+ years of experience building developer tools. You specialize in creating fast, intuitive command-line interfaces across Node.js, Python, and Go ecosystems. You build tools with <50ms startup time, comprehensive shell completions, and delightful UX.

## When to Use This Skill

- Building CLI tools and terminal applications
- Implementing argument parsing and subcommands
- Creating interactive prompts and forms
- Adding progress bars and spinners
- Implementing shell completions (bash, zsh, fish)
- Optimizing CLI performance and startup time

## Core Workflow

1. **Analyze UX** - Identify user workflows, command hierarchy, common tasks
2. **Design commands** - Plan subcommands, flags, arguments, configuration
3. **Implement** - Build with appropriate CLI framework for the language
4. **Polish** - Add completions, help text, error messages, progress indicators
5. **Test** - Cross-platform testing, performance benchmarks

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Design Patterns | `references/design-patterns.md` | Subcommands, flags, config, architecture |
| Node.js CLIs | `references/node-cli.md` | commander, yargs, inquirer, chalk |
| Python CLIs | `references/python-cli.md` | click, typer, argparse, rich |
| Go CLIs | `references/go-cli.md` | cobra, viper, bubbletea |
| UX Patterns | `references/ux-patterns.md` | Progress bars, colors, help text |

## Constraints

### MUST DO
- Keep startup time under 50ms
- Provide clear, actionable error messages
- Support --help and --version flags
- Use consistent flag naming conventions
- Handle SIGINT (Ctrl+C) gracefully
- Validate user input early
- Support both interactive and non-interactive modes
- Test on Windows, macOS, and Linux

### MUST NOT DO
- Block on synchronous I/O unnecessarily
- Print to stdout if output will be piped
- Use colors when output is not a TTY
- Break existing command signatures (breaking changes)
- Require interactive input in CI/CD environments
- Hardcode paths or platform-specific logic
- Ship without shell completions

## Output Templates

When implementing CLI features, provide:
1. Command structure (main entry point, subcommands)
2. Configuration handling (files, env vars, flags)
3. Core implementation with error handling
4. Shell completion scripts if applicable
5. Brief explanation of UX decisions

## Knowledge Reference

CLI frameworks (commander, yargs, oclif, click, typer, argparse, cobra, viper), terminal UI (chalk, inquirer, rich, bubbletea), testing (snapshot testing, E2E), distribution (npm, pip, homebrew, releases), performance optimization

## Related Skills

- **Node.js Expert** - Node.js implementation details
- **Python Expert** - Python implementation details
- **Go Expert** - Go implementation details
- **DevOps Engineer** - Distribution and packaging


# Merged Content from building-clis

---
name: cli_developer
description: Build professional command-line interfaces in Python, Go, and Rust using modern frameworks like Typer, Cobra, and clap. Use when creating developer tools, automation scripts, or infrastructure management CLIs with robust argument parsing, interactive features, and multi-platform distribution.
---

# Building CLIs

Build professional command-line interfaces across Python, Go, and Rust using modern frameworks with robust argument parsing, configuration management, and shell integration.

## When to Use This Skill

Use this skill when:
- Building developer tooling or automation CLIs
- Creating infrastructure management tools (deployment, monitoring)
- Implementing API client command-line tools
- Adding CLI capabilities to existing projects
- Packaging utilities for distribution (PyPI, Homebrew, binary releases)

Common triggers: "create a CLI tool", "build a command-line interface", "add CLI arguments", "parse command-line options", "generate shell completions"

## Framework Selection

### Quick Decision Guide

**Python Projects:**
- **Typer** (recommended): Modern type-safe CLIs with minimal boilerplate
- **Click**: Mature, flexible CLIs for complex command hierarchies

**Go Projects:**
- **Cobra** (recommended): Industry standard for enterprise tools (Kubernetes, Docker, GitHub CLI)
- **urfave/cli**: Lightweight alternative for simple CLIs

**Rust Projects:**
- **clap v4** (recommended): Type-safe with derive API or builder API for runtime flexibility

For detailed framework comparison and selection criteria, see [references/framework-selection.md](references/framework-selection.md).

## Core Patterns

### Arguments vs. Options vs. Flags

**Positional Arguments:**
- Primary input, identified by position
- Use for required inputs (max 2-3 arguments)
- Example: `convert input.jpg output.png`

**Options:**
- Named parameters with values
- Use for configuration and optional inputs
- Example: `--output file.txt`, `--config app.yaml`

**Flags:**
- Boolean options (presence = true)
- Use for switches and toggles
- Example: `--verbose`, `--dry-run`, `--force`

**Decision Matrix:**

| Use Case | Type | Example |
|----------|------|---------|
| Primary required input | Positional Argument | `git commit -m "message"` |
| Optional configuration | Option | `--config app.yaml` |
| Boolean setting | Flag | `--verbose`, `--force` |
| Multiple values | Variadic Argument | `files...` |

See [references/argument-patterns.md](references/argument-patterns.md) for comprehensive parsing patterns.

### Subcommand Organization

**Flat Structure (1 Level):**
```
app command1 [args]
app command2 [args]
```
Use for: Small CLIs with 5-10 operations

**Grouped Structure (2 Levels):**
```
app group subcommand [args]
```
Use for: Medium CLIs with logical groupings (10-30 commands)
Example: `kubectl get pods`, `kubectl create deployment`

**Nested Structure (3+ Levels):**
```
app group subgroup command [args]
```
Use for: Large CLIs with deep hierarchies (30+ commands)
Example: `gcloud compute instances create`

See [references/subcommand-design.md](references/subcommand-design.md) for structuring strategies.

### Configuration Management

**Standard Precedence (Highest to Lowest):**

1. CLI Arguments/Flags (explicit user input)
2. Environment Variables (session overrides)
3. Config File - Local (`./config.yaml`)
4. Config File - User (`~/.config/app/config.yaml`)
5. Config File - System (`/etc/app/config.yaml`)
6. Built-in Defaults (hardcoded)

**Best Practices:**
- Document precedence in `--help`
- Validate config files before execution
- Provide `--print-config` to show effective configuration
- Use XDG Base Directory (`~/.config/app/`) for config files

See [references/configuration-management.md](references/configuration-management.md) for implementation patterns across languages.

### Output Formatting

**Format Selection:**

| Use Case | Format | When |
|----------|--------|------|
| Human consumption | Colored text, tables | Default interactive mode |
| Machine consumption | JSON, YAML | `--output json`, piping |
| Logging/debugging | Plain text | `--verbose`, stderr |
| Progress tracking | Progress bars, spinners | Long operations |

**Best Practices:**
- Default to human-readable output
- Provide `--output` flag (json, yaml, table)
- Use stderr for logs, stdout for data
- Auto-detect TTY (disable colors if not interactive)
- Use exit codes: 0 = success, 1 = error, 2 = usage error

See [references/output-formatting.md](references/output-formatting.md) for formatting strategies.

## Language-Specific Quick Starts

### Python with Typer

**Installation:**
```bash
pip install "typer[all]"  # Includes rich for colored output
```

**Basic Example:**
```python
import typer
from typing import Annotated

app = typer.Typer()

@app.command()
def greet(
    name: Annotated[str, typer.Argument(help="Name to greet")],
    formal: Annotated[bool, typer.Option(help="Use formal greeting")] = False
):
    """Greet someone with a message."""
    greeting = "Good day" if formal else "Hello"
    typer.echo(f"{greeting}, {name}!")

if __name__ == "__main__":
    app()
```

**Key Features:**
- Type hints for automatic validation
- Minimal boilerplate with decorators
- Auto-generated help text
- Rich integration for colored output

See [examples/python/](examples/python/) for complete working examples including subcommands, config management, and interactive features.

### Go with Cobra

**Installation:**
```bash
go get -u github.com/spf13/cobra@latest
```

**Basic Example:**
```go
var rootCmd = &cobra.Command{
    Use:   "greet [name]",
    Args:  cobra.ExactArgs(1),
    Run: func(cmd *cobra.Command, args []string) {
        fmt.Printf("Hello, %s!\n", args[0])
    },
}

rootCmd.Flags().Bool("formal", false, "Use formal greeting")
rootCmd.Execute()
```

**Key Features:**
- POSIX-compliant flags
- Viper integration for configuration
- Subcommand architecture
- Shell completion generation

See [examples/go/](examples/go/) for complete working examples including Viper config and multi-level subcommands.

### Rust with clap

**Installation (Cargo.toml):**
```toml
[dependencies]
clap = { version = "4.5", features = ["derive"] }
```

**Basic Example (Derive API):**
```rust
use clap::Parser;

#[derive(Parser)]
#[command(about = "Greet someone")]
struct Cli {
    /// Name to greet
    name: String,

    /// Use formal greeting
    #[arg(long)]
    formal: bool,
}

fn main() {
    let cli = Cli::parse();
    let greeting = if cli.formal { "Good day" } else { "Hello" };
    println!("{}, {}!", greeting, cli.name);
}
```

**Key Features:**
- Compile-time type safety
- Derive API (declarative) or Builder API (programmatic)
- Comprehensive validation
- Performance optimized

See [examples/rust/](examples/rust/) for complete working examples including subcommands and builder API patterns.

## Interactive Features

### Progress Indicators

**Python (rich):**
```python
from rich.progress import track
for _ in track(range(100), description="Processing..."):
    time.sleep(0.01)
```

**Go (progressbar):**
```go
import "github.com/schollz/progressbar/v3"
bar := progressbar.Default(100)
for i := 0; i < 100; i++ {
    bar.Add(1)
}
```

**Rust (indicatif):**
```rust
use indicatif::ProgressBar;
let bar = ProgressBar::new(100);
for _ in 0..100 {
    bar.inc(1);
}
```

### Prompts and Confirmations

**Python:**
```python
confirm = typer.confirm("Are you sure?")
if not confirm:
    raise typer.Abort()
```

**Go:**
```go
reader := bufio.NewReader(os.Stdin)
fmt.Print("Are you sure? (y/n): ")
response, _ := reader.ReadString('\n')
```

**Rust:**
```rust
use dialoguer::Confirm;
if Confirm::new().with_prompt("Are you sure?").interact()? {
    // Proceed
}
```

## Shell Completion

### Generating Completions

**Python (Typer):**
```bash
_MYAPP_COMPLETE=bash_source myapp > ~/.myapp-complete.bash
_MYAPP_COMPLETE=zsh_source myapp > ~/.myapp-complete.zsh
```

**Go (Cobra):**
```go
rootCmd.AddCommand(&cobra.Command{
    Use:   "completion [bash|zsh|fish|powershell]",
    Args:  cobra.ExactArgs(1),
    Run: func(cmd *cobra.Command, args []string) {
        switch args[0] {
        case "bash":
            rootCmd.GenBashCompletion(os.Stdout)
        case "zsh":
            rootCmd.GenZshCompletion(os.Stdout)
        }
    },
})
```

**Rust (clap):**
```rust
use clap_complete::{generate, shells::Bash};
generate(Bash, &mut Cli::command(), "myapp", &mut io::stdout())
```

See [references/shell-completion.md](references/shell-completion.md) for installation instructions.

## Distribution and Packaging

### Python (PyPI)

**pyproject.toml:**
```toml
[project]
name = "myapp"
version = "1.0.0"
scripts = { myapp = "myapp.cli:app" }
```

**Publish:**
```bash
pip install build twine
python -m build
twine upload dist/*
```

### Go (Homebrew)

**Formula:**
```ruby
class Myapp < Formula
  desc "My CLI application"
  url "https://github.com/user/myapp/archive/v1.0.0.tar.gz"

  def install
    system "go", "build", "-o", bin/"myapp"
  end
end
```

### Rust (Cargo)

**Publish:**
```bash
cargo login
cargo publish
```

**Installation:**
```bash
cargo install myapp
```

See [references/distribution.md](references/distribution.md) for comprehensive packaging strategies including binary releases.

## Best Practices

### Universal CLI Conventions

**Always Provide:**
- `--help` and `-h` for usage information
- `--version` and `-V` for version display
- Clear error messages with actionable suggestions

**Argument Handling:**
- Use `--` separator for options vs. positional args
- Support both short (`-v`) and long (`--verbose`) forms
- Validate and sanitize all user inputs

**Error Handling:**
- Exit code 0 for success
- Exit code 1 for general errors
- Exit code 2 for usage errors
- Write errors to stderr, data to stdout

**Interactivity:**
- Detect TTY (interactive vs. piped input)
- Provide `--yes`/`--force` to skip prompts for automation
- Show progress for operations longer than 2 seconds

### Configuration Best Practices

**File Formats:**
- Use YAML, TOML, or JSON consistently
- Separate files per environment (dev, staging, prod)
- Validate configuration in CI/CD with `--check-config`

**Secret Management:**
- Never commit secrets to config files
- Use environment variables or secret managers
- Document required environment variables

**Precedence:**
- CLI args > env vars > config file > defaults
- Document precedence in help text
- Provide `--print-config` to show effective configuration

## Integration with Other Skills

**testing-strategies:**
- CLI testing with mocks and fixtures
- Integration tests for end-to-end workflows
- See [examples/python/test_cli.py](examples/python/test_cli.py)

**building-ci-pipelines:**
- Binary builds for multiple platforms
- Automated releases via GitHub Actions
- See [references/distribution.md](references/distribution.md)

**api-patterns:**
- Building API client CLIs
- Authentication and token management
- Formatting API responses

**secret-management:**
- Secure credential storage
- Environment variable integration
- Vault/secrets manager integration

## Reference Files

**Decision Frameworks:**
- [framework-selection.md](references/framework-selection.md) - Which framework to choose
- [argument-patterns.md](references/argument-patterns.md) - Arguments vs. options vs. flags
- [subcommand-design.md](references/subcommand-design.md) - Structuring command hierarchies

**Implementation Guides:**
- [configuration-management.md](references/configuration-management.md) - Config files and precedence
- [output-formatting.md](references/output-formatting.md) - Human vs. machine-readable output
- [shell-completion.md](references/shell-completion.md) - Generating completions
- [distribution.md](references/distribution.md) - Packaging and releasing CLIs

**Code Examples:**
- [examples/python/](examples/python/) - Typer examples (basic, subcommands, config, interactive)
- [examples/go/](examples/go/) - Cobra examples (basic, subcommands, Viper integration)
- [examples/rust/](examples/rust/) - clap examples (derive, builder, subcommands)

## Quick Reference

**Framework Recommendations:**
- Python: Typer (modern) or Click (mature)
- Go: Cobra (enterprise) or urfave/cli (simple)
- Rust: clap v4 (derive or builder)

**Common Patterns:**
- Arguments: Primary inputs (max 2-3)
- Options: Named parameters with values
- Flags: Boolean switches
- Subcommands: Group related operations
- Config: CLI args > env vars > files > defaults

**Output Standards:**
- Default: Human-readable (colored, tables)
- Machine: JSON/YAML via `--output` flag
- Errors: stderr, data: stdout
- Exit: 0 = success, 1 = error, 2 = usage

**Distribution:**
- Python: PyPI (`pip install`)
- Go: Homebrew, binary releases
- Rust: Cargo (`cargo install`), binary releases

---

*CLI Developer v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [12 Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46)

### Aşama 1: Design & UX
- [ ] **Interface**: Komut/Alt-komut yapısını tasarla (`verb noun` pattern).
- [ ] **Flags**: Global (`--verbose`) ve local flagleri belirle.
- [ ] **Output**: `stdout` (veri) ve `stderr` (log) ayrımını planla.

### Aşama 2: Implementation
- [ ] **Skeleton**: Framework'ü kur (Cobra/Typer/Clap).
- [ ] **Logic**: Business logic'i yaz, I/O işlemlerini soyutla.
- [ ] **Interactivity**: TTY kontrolü ile renk/prompt ekle.

### Aşama 3: Polish
- [ ] **Help**: `--help` metinlerini ve örnekleri yaz.
- [ ] **Completion**: Shell completion scriptlerini üret.
- [ ] **Man Pages**: Dokümantasyon oluştur.

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Komut yapısı "tahmin edilebilir" mi? (Intuitive) |
| 2 | `myscript > file.txt` yapınca loglar dosyaya karışıyor mu? (Karışmamalı) |
| 3 | Startup time < 50ms mi? |
