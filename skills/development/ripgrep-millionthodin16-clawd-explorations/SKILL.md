---
name: ripgrep
description: Fast line-oriented search tool. Better than grep with color output, recursive search, and smart defaults.
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["rg"]}}}
---

# ripgrep (rg) - Fast Search Tool

Fast line-oriented search tool that recursively searches the current directory for a regex pattern.

## Quick Start

```bash
rg "pattern"                    # Search for pattern
rg -l "pattern"                 # List files only
rg -t py "pattern"              # Search Python files only
rg -A 3 "pattern"               # Show 3 lines after match
rg -B 2 "pattern"               # Show 2 lines before match
rg --vimgrep "pattern"          # Output for editors
rg "pattern" /path/to/search    # Search specific path
```

## Commands

### Search Files
```bash
uv run {baseDir}/scripts/rg.py search "TODO"                 # Find TODO comments
uv run {baseDir}/scripts/rg.py search "def main" --type py   # Find functions in Python
uv run {baseDir}/scripts/rg.py files "class.*Agent"          # Find classes
```

### Find Files by Pattern
```bash
uv run {baseDir}/scripts/rg.py find "import" --type py       # Files with imports
uv run {baseDir}/scripts/rg.py count "error"                 # Count occurrences
uv run {baseDir}/scripts/rg.py hidden "secret"               # Search hidden files
```

### Git-Specific
```bash
uv run {baseDir}/scripts/rg.py staged "FIXME"                # Search staged changes
uv run {baseDir}/scripts/rg.py commits "feat:"               # Search commit messages
```

## Examples

### Find All TODO Comments
```bash
rg "TODO" -n --type md
```

### Find Function Definitions
```bash
rg "^def " --type py -n
```

### Find All Imports
```bash
rg "^import|^from" --type py -n
```

### Count Lines of Code by Language
```bash
rg -l --type py | wc -l
```

## Why ripgrep Over grep?

| Feature | grep | ripgrep |
|---------|------|---------|
| Speed | Baseline | 10x faster |
| Recursive | Need -r | Default |
| Color | Need --color | Default |
| Smart case | No | Yes |
| Filename only | -l | -l |
| File types | --include | -t |

## Installation

```bash
brew install ripgrep  # macOS
cargo install ripgrep # Linux/ARM64
```

## See Also

- **Full workflow guide:** `memory/WORKFLOW.md` - Decision tree for when to use ripgrep vs other tools
- **Tool comparison:** `memory/HIGH-IMPACT-TOOLS.md` - Why ripgrep over grep

## Files

- `scripts/rg.py` - CLI wrapper
