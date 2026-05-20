---
name: explore-area
description: Use when you need to understand a module, feature, or directory before making changes.
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: Explore
argument-hint: "[directory or feature name]"
---

Explore **$ARGUMENTS** using progressive disclosure to minimize token cost.

## Progressive Disclosure (3 Layers)

### Layer 1: File Index (cheapest — start here)

Get the file list WITHOUT reading contents:

```bash
# List all files in the target area
find [target] -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | head -50
```

Or use Glob to find relevant files. From this list alone, identify:
- Entry points (index.*, main.*, app.*)
- Test files (*.test.*, *.spec.*)
- Config files
- File count and general structure

**Decision point:** Do you now have enough context? If yes, skip to Return Format. If no, proceed to Layer 2.

### Layer 2: Entry Points & Signatures (moderate cost)

Read ONLY entry points and key files. Use targeted reads:
- Read index/main files to understand exports and module structure
- Use Grep to find function signatures, class definitions, type exports
- Map imports/exports to understand dependency graph

```bash
# Find exports
grep -rn "export" [target]/index.* 2>/dev/null
# Find class/function definitions
grep -rn "^export \(class\|function\|const\|interface\)" [target]/ 2>/dev/null
```

**Decision point:** Do you understand the module's API and structure? If yes, skip to Return Format. If no, proceed to Layer 3.

### Layer 3: Deep Dive (expensive — only when needed)

Read full file contents, but only for files that are:
- Directly relevant to the user's upcoming changes
- Complex enough that signatures alone don't explain behavior
- Containing patterns the user needs to follow

Use `offset` and `limit` for large files — read the relevant section, not the whole file.

## Return Format

```
## Area: [name]

### Structure ([X] files)
- [file] → [purpose, 5 words max]

### Key Files (read these before editing)
- [file] → [what it does and why it matters]

### Dependencies
- Imports from: [external modules used]
- Exported to: [who consumes this module]

### Patterns to Follow
- [naming, structure, style patterns observed]
- [reference file] → follow this as template for new code

### Tests
- [test approach, test file locations, how to run]

### Gotchas
- [anything unusual, legacy code, known quirks]
- [things that look wrong but are intentional]
```

## Rules

- Start at Layer 1. Only go deeper when needed.
- Never read ALL files in a directory — that defeats the purpose.
- Focus on what someone needs to know BEFORE making changes.
- Be concise. The user will read the files themselves when editing.

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
