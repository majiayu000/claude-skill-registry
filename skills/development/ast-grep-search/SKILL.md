---
name: ast-grep Structural Code Search & Refactoring
description: Find and replace code patterns structurally using ast-grep. Use when you need to match code by its AST structure (not just text), such as finding all functions with specific signatures, replacing API patterns across files, or detecting code anti-patterns that regex cannot reliably match.
model: haiku
compatibility: Designed for Claude Code
allowed-tools: Read Grep Glob Bash mcp__context7__resolve-library-id mcp__context7__get-library-docs
user-invocable: false
---

# ast-grep Structural Code Search & Refactoring

Structural code search and refactoring using `ast-grep` — matches code by its AST (abstract syntax tree) rather than text patterns.

## When to Use ast-grep vs Grep/ripgrep

| Use ast-grep when... | Use grep/rg when... |
|---------------------|---------------------|
| Pattern depends on code structure | Simple text or regex match |
| Need to match any number of arguments | Searching logs, docs, config |
| Refactoring across many files | One-off literal string search |
| Finding anti-patterns (empty catch, etc.) | Language doesn't matter |
| Replacing while preserving variables | Quick filename/line check |

**Decision rule**: If your search pattern contains wildcards for "any expression," "any arguments," or "any function name," use ast-grep.

## Pattern Syntax

| Pattern | Matches | Example |
|---------|---------|---------|
| `$VAR` | Single AST node | `console.log($MSG)` |
| `$$$ARGS` | Zero or more nodes | `func($$$ARGS)` |
| `$_` | Single node (no capture) | `$_ == $_` |
| `$A == $A` | Same node repeated | Finds `x == x` (not `x == y`) |

## Essential Commands

### Search for Patterns

```bash
# Find structural patterns
ast-grep -p 'console.log($$$)' --lang js
ast-grep -p 'def $FUNC($$$): $$$' --lang py
ast-grep -p 'fn $NAME($$$) -> $RET { $$$ }' --lang rs

# Search in specific directory
ast-grep -p 'import $PKG' --lang js src/

# JSON output for parsing
ast-grep -p 'pattern' --lang js --json=compact
```

### Search and Replace

```bash
# Preview changes (default - shows matches)
ast-grep -p 'var $V = $X' -r 'const $V = $X' --lang js

# Apply changes to all files
ast-grep -p 'var $V = $X' -r 'const $V = $X' --lang js -U

# Interactive review
ast-grep -p 'oldAPI($$$ARGS)' -r 'newAPI($$$ARGS)' --lang py -i

# Convert function syntax
ast-grep -p 'function($$$ARGS) { return $EXPR }' \
         -r '($$$ARGS) => $EXPR' --lang js -U

# Update import paths
ast-grep -p "import $NAME from '@old/$PATH'" \
         -r "import $NAME from '@new/$PATH'" --lang ts -U
```

### Language Codes

| Code | Language | Code | Language |
|------|----------|------|----------|
| `js` | JavaScript | `py` | Python |
| `ts` | TypeScript | `rs` | Rust |
| `jsx` | JSX | `go` | Go |
| `tsx` | TSX | `java` | Java |
| `cpp` | C++ | `rb` | Ruby |
| `c` | C | `php` | PHP |

## Common Patterns by Language

### JavaScript/TypeScript

```bash
# Find React hooks
ast-grep -p 'const [$STATE, $SETTER] = useState($INIT)' --lang jsx

# Find async functions
ast-grep -p 'async function $NAME($$$) { $$$ }' --lang js

# Find type assertions
ast-grep -p '$EXPR as $TYPE' --lang ts

# Find empty catch blocks
ast-grep -p 'try { $$$ } catch ($E) { }' --lang js

# Find eval usage (security)
ast-grep -p 'eval($$$)' --lang js

# Find innerHTML (XSS risk)
ast-grep -p '$ELEM.innerHTML = $$$' --lang js

# Find specific imports
ast-grep -p "import { $$$IMPORTS } from '$PKG'" --lang js
```

### Python

```bash
# Find class definitions
ast-grep -p 'class $NAME($$$BASES): $$$' --lang py

# Find decorated functions
ast-grep -p '@$DECORATOR\ndef $FUNC($$$): $$$' --lang py

# Find dangerous shell calls
ast-grep -p 'os.system($$$)' --lang py

# Find SQL concatenation (injection risk)
ast-grep -p '"SELECT * FROM " + $VAR' --lang py
```

### Rust

```bash
# Find unsafe blocks
ast-grep -p 'unsafe { $$$ }' --lang rs

# Find impl blocks
ast-grep -p 'impl $TRAIT for $TYPE { $$$ }' --lang rs

# Find public functions
ast-grep -p 'pub fn $NAME($$$) { $$$ }' --lang rs
```

### Go

```bash
# Find goroutines
ast-grep -p 'go $FUNC($$$)' --lang go

# Find defer statements
ast-grep -p 'defer $FUNC($$$)' --lang go

# Find error handling
ast-grep -p 'if err != nil { $$$ }' --lang go
```

## Common Refactoring Recipes

```bash
# Replace deprecated API calls
ast-grep -p 'oldAPI.$METHOD($$$)' -r 'newAPI.$METHOD($$$)' --lang js -U

# Rename a function across files
ast-grep -p 'oldName($$$ARGS)' -r 'newName($$$ARGS)' --lang py -U

# Remove console.log statements
ast-grep -p 'console.log($$$)' -r '' --lang js -U

# Convert require to import
ast-grep -p 'const $NAME = require($PKG)' \
         -r 'import $NAME from $PKG' --lang js -i

# Add error handling wrapper
ast-grep -p 'await $EXPR' \
         -r 'await $EXPR.catch(handleError)' --lang ts -i
```

## Command-Line Flags

| Flag | Purpose |
|------|---------|
| `-p, --pattern` | Search pattern |
| `-r, --rewrite` | Replacement pattern |
| `-l, --lang` | Target language |
| `-i, --interactive` | Review changes one by one |
| `-U, --update-all` | Apply all changes |
| `--json` | JSON output (`compact`, `stream`, `pretty`) |
| `-A N` | Lines after match |
| `-B N` | Lines before match |
| `-C N` | Lines around match |
| `--debug-query` | Debug pattern parsing |

## YAML Rules (Scan Mode)

For reusable rules, use `ast-grep scan` with YAML configuration:

```bash
# Scan with config
ast-grep scan -c sgconfig.yml

# Run specific rule
ast-grep scan -r rule-name

# Initialize a rules project
ast-grep new project my-linter
ast-grep new rule no-console-log
```

Minimal rule file:
```yaml
id: no-empty-catch
language: JavaScript
severity: warning
message: Empty catch block hides errors
rule:
  pattern: try { $$$ } catch ($E) { }
fix: |
  try { $$$ } catch ($E) { console.error($E) }
```

For comprehensive YAML rule syntax, constraints, transformations, and testing, see [REFERENCE.md](REFERENCE.md).

## Agentic Optimizations

| Context | Command |
|---------|---------|
| Quick structural search | `ast-grep -p 'pattern' --lang js --json=compact` |
| Count matches | `ast-grep -p 'pattern' --lang js --json=stream \| wc -l` |
| File list only | `ast-grep -p 'pattern' --json=stream \| jq -r '.file' \| sort -u` |
| Batch refactor | `ast-grep -p 'old' -r 'new' --lang js -U` |
| Scan with rules | `ast-grep scan --json` |
| Debug pattern | `ast-grep -p 'pattern' --debug-query --lang js` |

## Quick Reference

```bash
# 1. Search for pattern
ast-grep -p 'pattern' --lang js src/

# 2. Preview rewrite
ast-grep -p 'old' -r 'new' --lang js

# 3. Apply rewrite
ast-grep -p 'old' -r 'new' --lang js -U

# 4. Scan with rules
ast-grep scan -c sgconfig.yml

# 5. Debug pattern
ast-grep -p 'pattern' --debug-query --lang js
```

### Context7 Integration

For latest AST-Grep documentation, follow this two-step process.

Step 1: Use mcp__context7__resolve-library-id with query ast-grep to resolve the library identifier.

Step 2: Use mcp__context7__get-library-docs with the resolved library ID to fetch current documentation.

### Reference

For additional information, consult the AST-Grep Official Documentation at ast-grep.github.io, the AST-Grep GitHub Repository at github.com/ast-grep/ast-grep, the Pattern Playground at ast-grep.github.io/playground.html, and the Rule Configuration Reference at ast-grep.github.io/reference/yaml.html.
