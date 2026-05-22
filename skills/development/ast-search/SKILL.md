---
name: ast-search
description: This skill should be used automatically when searching for code patterns, function usages, class definitions, or syntax structures. Prefer ast-grep over grep/find/ripgrep for code-aware searching that understands language syntax. Use for finding function calls, understanding API usage, locating pattern implementations, and code exploration.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - TodoWrite
model: sonnet
---

# AST-Aware Code Search

## Overview

Use ast-grep for syntax-aware code searching that understands language structure. Unlike text-based tools (grep, ripgrep, find), ast-grep matches actual code patterns by parsing the abstract syntax tree.

## When to Use

**Prefer ast-grep over grep/find when:**
- Finding function/method calls: `ast-grep -p 'fetchData($$$)'`
- Locating class or function definitions
- Searching for specific syntax patterns (hooks, decorators, imports)
- Understanding how an API or function is used across a codebase
- Finding all implementations of a pattern

**Use grep/ripgrep instead when:**
- Searching for literal strings or comments
- Searching non-code files (markdown, config, logs)
- Simple keyword searches where syntax doesn't matter
- Languages not supported by ast-grep

## Quick Reference

```bash
# Check installation
which ast-grep || echo "Install with: brew install ast-grep"

# Basic pattern search
ast-grep --pattern 'PATTERN' --lang LANGUAGE [PATH]

# Search with context
ast-grep -p 'PATTERN' -l LANG -A 3 -B 2

# JSON output for parsing
ast-grep -p 'PATTERN' -l LANG --json
```

### Pattern Syntax

| Pattern | Matches | Example |
|---------|---------|---------|
| `$VAR` | Single AST node | `console.log($MSG)` matches `console.log("hello")` |
| `$$$ARGS` | Multiple nodes (named) | `function($$$PARAMS)` matches any function params |
| `$$$` | Any sequence of nodes | `{ $$$ }` matches any block contents |

### Supported Languages

`javascript`, `typescript`, `tsx`, `python`, `go`, `rust`, `java`, `c`, `cpp`, `csharp`, `kotlin`, `swift`, `ruby`, `php`, `lua`, `html`, `css`

## Common Search Patterns

### JavaScript/TypeScript

```bash
# Find all useState hooks
ast-grep -p 'useState($$$)' -l typescript

# Find specific function calls
ast-grep -p 'fetchUser($$$)' -l typescript

# Find async functions
ast-grep -p 'async function $NAME($$$) { $$$ }' -l typescript

# Find arrow function assignments
ast-grep -p 'const $NAME = ($$$) => $$$' -l typescript

# Find React component definitions
ast-grep -p 'function $COMPONENT($$$): JSX.Element { $$$ }' -l tsx

# Find useEffect with dependencies
ast-grep -p 'useEffect($$$)' -l typescript

# Find imports from a module
ast-grep -p "import { $$$ } from '$MODULE'" -l typescript

# Find class methods
ast-grep -p 'class $CLASS { $$$ $METHOD($$$) { $$$ } $$$ }' -l typescript
```

### Python

```bash
# Find function definitions
ast-grep -p 'def $FUNC($$$): $$$' -l python

# Find class definitions
ast-grep -p 'class $CLASS: $$$' -l python

# Find decorator usage
ast-grep -p '@$DECORATOR
def $FUNC($$$): $$$' -l python

# Find specific method calls
ast-grep -p '$OBJ.$METHOD($$$)' -l python

# Find async function definitions
ast-grep -p 'async def $FUNC($$$): $$$' -l python

# Find list comprehensions
ast-grep -p '[$EXPR for $VAR in $ITER]' -l python
```

### Go

```bash
# Find function definitions
ast-grep -p 'func $NAME($$$) $$$ { $$$ }' -l go

# Find method definitions
ast-grep -p 'func ($RECV $TYPE) $NAME($$$) $$$ { $$$ }' -l go

# Find interface definitions
ast-grep -p 'type $NAME interface { $$$ }' -l go

# Find struct definitions
ast-grep -p 'type $NAME struct { $$$ }' -l go

# Find error handling patterns
ast-grep -p 'if err != nil { $$$ }' -l go

# Find goroutine spawns
ast-grep -p 'go $FUNC($$$)' -l go
```

### Java

```bash
# Find class definitions
ast-grep -p 'class $NAME { $$$ }' -l java

# Find method definitions
ast-grep -p '$RET $METHOD($$$) { $$$ }' -l java

# Find annotations
ast-grep -p '@$ANNOTATION
$$$' -l java

# Find try-catch blocks
ast-grep -p 'try { $$$ } catch ($E) { $$$ }' -l java
```

## Workflow

### 1. Verify Installation

```bash
which ast-grep || brew install ast-grep
```

### 2. Identify Target Language

Determine the language flag needed:
- `.ts`, `.tsx` → `-l typescript` or `-l tsx`
- `.js`, `.jsx` → `-l javascript`
- `.py` → `-l python`
- `.go` → `-l go`
- `.rs` → `-l rust`
- `.java` → `-l java`

### 3. Build Search Pattern

Start simple and refine:

```bash
# Start broad
ast-grep -p 'fetchData($$$)' -l typescript

# Add specificity if too many results
ast-grep -p 'await fetchData($$$)' -l typescript

# Narrow to specific directory
ast-grep -p 'fetchData($$$)' -l typescript src/api/
```

### 4. Analyze Results

```bash
# Count matches
ast-grep -p 'PATTERN' -l LANG --json | jq length

# Get file list only
ast-grep -p 'PATTERN' -l LANG --json | jq -r '.[].file' | sort -u

# Get matches with context
ast-grep -p 'PATTERN' -l LANG -A 5 -B 2
```

## Comparison: ast-grep vs grep

| Task | ast-grep | grep/ripgrep |
|------|----------|--------------|
| Find `log("...")` calls | `ast-grep -p 'log($$$)'` - matches only function calls | `rg 'log\('` - matches comments, strings too |
| Find variable assignments | `ast-grep -p 'const $X = $Y'` - matches declarations | `rg 'const'` - matches any occurrence |
| Find function definitions | `ast-grep -p 'function $F($$$)'` - accurate | `rg 'function'` - includes comments, strings |
| Find class methods | Pattern matches syntax tree | Regex struggles with nesting |
| Search comments | Not designed for this | Better choice |
| Search config files | Won't parse non-code | Better choice |

## Troubleshooting

**Pattern doesn't match expected code:**
- Verify language flag matches file extension
- Check for whitespace sensitivity in patterns
- Try a simpler pattern first and add specificity
- Use `--json` output to debug what's matching

**Too many results:**
- Add more context to the pattern
- Narrow search to specific directories
- Use `$NAME` instead of `$$$` to match single nodes

**No results when expecting matches:**
- Verify ast-grep supports the language
- Check that files have correct extensions
- Test with a known-good pattern first
- Ensure the pattern syntax matches the language's AST

**Performance on large codebases:**
- Specify target directories instead of searching entire repo
- Use `.astgrepignore` file to exclude directories (like node_modules)

## Installation

```bash
# macOS
brew install ast-grep

# Cargo (Rust)
cargo install ast-grep --locked

# npm (less performant)
npm install -g @ast-grep/cli
```
