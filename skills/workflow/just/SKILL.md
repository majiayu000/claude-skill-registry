---
name: just
description: Just command runner for saving and running project-specific commands
---

# Just Command Runner Skill

Comprehensive assistance with Just, a handy command runner for saving and running project-specific commands. Just uses a `justfile` with `make`-inspired syntax but designed as a general-purpose task executor rather than a build system.

## When to Use This Skill

This skill should be triggered when:
- Creating or managing `justfile` recipes
- Setting up project task automation
- Replacing Make or shell scripts with Just
- Working with cross-platform command execution
- Organizing project-specific commands
- Implementing task dependencies and workflows

## Quick Reference

### Common Patterns

**Basic Recipe**:
```just
recipe-name:
  echo 'This is a recipe!'

# Silent recipe (@ suppresses echo)
silent-recipe:
  @echo 'This runs quietly'
```

**Recipe with Parameters**:
```just
build target='all':
  @echo 'Building {{target}}…'

# Variadic parameters
test *files:
  pytest {{files}}
```

**Recipe with Dependencies**:
```just
build:
  cc main.c -o main

test: build
  ./test --all
```

**Shebang Recipes** (multi-language support):
```just
python:
  #!/usr/bin/env python3
  print('Hello from Python!')

node:
  #!/usr/bin/env node
  console.log('Hello from Node!');
```

**Variables and Expressions**:
```just
compiler := 'gcc'
flags := '-Wall -O2'

build:
  {{compiler}} {{flags}} main.c -o main
```

### Common Commands

- `just` — Run default recipe
- `just RECIPE` — Run specific recipe
- `just --list` — List all recipes
- `just --show RECIPE` — Display recipe definition
- `just --choose` — Interactive recipe selector (requires fzf)
- `just --fmt` — Format justfile
- `just --dump` — Output formatted justfile

### Example Code Patterns

**Example 1** (basic justfile):
```just
# Default recipe runs when you type 'just'
[default]
build:
  cargo build --release

# Recipe with confirmation prompt
[confirm]
deploy:
  kubectl apply -f deployment.yaml

# Platform-specific recipes
[linux]
install:
  apt-get install my-package

[macos]
install:
  brew install my-package
```

**Example 2** (with variables and .env):
```just
# Load .env file
set dotenv-load

# Variables
app_name := env('APP_NAME', 'myapp')
version := `git describe --tags`

# Recipe using variables
build:
  docker build -t {{app_name}}:{{version}} .

# Conditional logic
deploy environment='staging':
  #!/usr/bin/env bash
  if [ "{{environment}}" = "production" ]; then
    echo "Deploying to production..."
  else
    echo "Deploying to staging..."
  fi
```

**Example 3** (modules and imports):
```just
# Import external justfile
import 'tasks/docker.just'

# Use module system
mod database 'tasks/db.just'

# Call module recipe
migrate: database::migrate
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **just-full-reference.md** - Complete Just documentation covering all features
- **index.md** - Quick reference guide

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the basic recipe patterns above. A simple `justfile` with a few recipes is all you need to get started. Just provides helpful error messages that point to specific issues in your justfile.

### For Specific Features
- **Task Automation**: Create recipes for common project tasks
- **Cross-Platform**: Use platform-specific attributes `[linux]`, `[macos]`, `[windows]`
- **Dependencies**: Chain recipes with dependency syntax `recipe: dep1 dep2`
- **Multi-Language**: Use shebang recipes for Python, Node, Ruby, etc.
- **Environment**: Load `.env` files with `set dotenv-load`

### For Code Examples
The quick reference section contains common patterns. For complete syntax and advanced features, consult the reference files.

## Key Features

### Core Strengths
- **Simpler than Make**: No `.PHONY` declarations needed
- **Cross-platform**: Linux, macOS, Windows, BSD support
- **Clear errors**: Specific error messages with source context
- **Static validation**: Unknown recipes and circular dependencies caught early
- **Auto .env loading**: Environment variables from `.env` files
- **Subdirectory execution**: Run from any subdirectory containing justfile

### Advanced Capabilities
- **50+ built-in functions**: Path manipulation, string operations, hashing, system info
- **Multi-language support**: Python, Node.js, Perl, Ruby, Nushell, and more
- **Module system**: Organize complex projects with submodules
- **Imports**: Include external justfiles
- **Interactive chooser**: Select recipes with `--choose` (uses fzf)
- **Recipe attributes**: `[default]`, `[private]`, `[confirm]`, platform-specific

## Installation

**Cargo** (Rust):
```bash
cargo install just
```

**Homebrew** (macOS/Linux):
```bash
brew install just
```

**Pre-built binaries**:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin
```

**Package managers**: Available via apt, pacman, dnf, chocolatey, scoop, and 15+ others

## Configuration

**Shell Settings**:
```just
# Set default shell (Unix-like)
set shell := ["bash", "-uc"]

# Windows PowerShell
set windows-shell := ["powershell.exe", "-Command"]
```

**Common Settings**:
```just
set dotenv-load          # Auto-load .env files
set export               # Export all variables as environment vars
set positional-arguments # Pass args as positional ($1, $2, etc.)
```

## Resources

### references/
Organized documentation extracted from official Just documentation and README:
- Complete syntax reference
- All built-in functions
- Recipe attributes and features
- Examples and patterns

### scripts/
Add helper scripts here for common Just automation tasks.

### assets/
Add example justfiles or templates here.

## Editor Support

Syntax highlighting available for:
- Vim/Neovim (built-in since version 9.1.1042/0.11)
- VS Code (community extension)
- Emacs (`just-mode`)
- JetBrains IDEs
- Helix (built-in since 23.05)
- Zed, Sublime Text, Kakoune, Micro

## Notes

- Just version 1.0+ guarantees backwards compatibility
- Unstable features require `--unstable` flag or `set unstable`
- Official documentation: https://just.systems/man/en/
- Examples: https://github.com/casey/just/tree/master/examples

## Updating

To refresh this skill with updated documentation:
1. Visit https://github.com/casey/just
2. Check for new features in the README and changelog
3. Update reference files with new content
