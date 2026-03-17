---
name: file-search
description: "Modern file and content search using fd, ripgrep (rg), and fzf. Triggers on: fd, ripgrep, rg, find files, search code, fzf, fuzzy find, search codebase."
compatibility: "Requires fd, ripgrep (rg), and optionally fzf. Install: brew install fd ripgrep fzf (macOS)."
allowed-tools: "Bash"
---

# File Search

Modern file and content search.

## fd - Find Files

```bash
# Find by name
fd config                    # Files containing "config"
fd -e py                     # Python files

# By type
fd -t f config               # Files only
fd -t d src                  # Directories only

# Exclude
fd -E node_modules           # Exclude directory
fd -E "*.min.js"             # Exclude pattern

# Execute command
fd -e py -x wc -l            # Line count per file
```

## rg - Search Content

```bash
# Simple search
rg "TODO"                    # Find TODO
rg -i "error"                # Case-insensitive

# By file type
rg -t py "import"            # Python files only
rg -t js -t ts "async"       # JS and TS

# Context
rg -C 3 "function"           # 3 lines before/after

# Output modes
rg -l "TODO"                 # File names only
rg -c "TODO"                 # Count per file
```

## fzf - Interactive Selection

```bash
# Find and select
fd | fzf

# With preview
fd | fzf --preview 'bat --color=always {}'

# Multi-select
fd -e ts | fzf -m | xargs code
```

## Combined Patterns

```bash
# Find files, search content
fd -e py -x rg "async def" {}

# Search, select, open
rg -l "pattern" | fzf --preview 'rg -C 3 "pattern" {}' | xargs vim
```

## Quick Reference

| Task | Command |
|------|---------|
| Find TS files | `fd -e ts` |
| Find in src | `fd -e ts src/` |
| Search pattern | `rg "pattern"` |
| Search in type | `rg -t py "import"` |
| Files with match | `rg -l "pattern"` |
| Count matches | `rg -c "pattern"` |
| Interactive | `fd \| fzf` |
| With preview | `fd \| fzf --preview 'bat {}'` |

## Performance Tips

| Tip | Why |
|-----|-----|
| Both respect `.gitignore` | Auto-skip node_modules, dist |
| Use `-t` over `-g` | Type flags are faster |
| Narrow the path | `rg pattern src/` faster |
| Use `-F` for literals | Avoids regex overhead |

## Additional Resources

For detailed patterns, load:
- `./references/advanced-workflows.md` - Git integration, shell functions, power workflows
