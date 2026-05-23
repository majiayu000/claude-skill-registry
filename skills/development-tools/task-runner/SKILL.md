---
name: task-runner
description: "Run project commands with just. Check for justfile in project root, list available tasks, execute common operations like test, build, lint. Triggers on: run tests, build project, list tasks, check available commands, run script, project commands."
compatibility: "Requires just CLI tool. Install: brew install just (macOS) or cargo install just (cross-platform)."
allowed-tools: "Bash Glob"
---

# Task Runner

## Purpose
Execute project-specific commands using just, a modern command runner that's simpler than make and works cross-platform.

## Tools

| Tool | Command | Use For |
|------|---------|---------|
| just | `just` | List available recipes |
| just | `just test` | Run specific recipe |

## Usage Examples

### Basic Usage

```bash
# List all available recipes
just

# Run a recipe
just test
just build
just lint

# Run recipe with arguments
just deploy production

# Run specific recipe from subdirectory
just --justfile backend/justfile test
```

### Common justfile Recipes

```just
# Example justfile

# Run tests
test:
    pytest tests/

# Build project
build:
    npm run build

# Lint code
lint:
    ruff check .
    eslint src/

# Start development server
dev:
    npm run dev

# Clean build artifacts
clean:
    rm -rf dist/ build/ *.egg-info/

# Deploy to environment
deploy env:
    ./scripts/deploy.sh {{env}}
```

### Discovery

```bash
# Check if justfile exists
just --summary

# Show recipe details
just --show test

# List recipes with descriptions
just --list
```

## When to Use

- First check: `just` to see available project commands
- Running tests: `just test`
- Building: `just build`
- Any project-specific task
- Cross-platform command running

## Best Practice

Always check for a justfile when entering a new project:
```bash
just --list
```
This shows what commands are available without reading documentation.
