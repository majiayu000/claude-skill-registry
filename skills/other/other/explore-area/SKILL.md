---
name: explore-area
description: Deep exploration of a codebase area before making changes. Use when you need to understand a module, feature, or directory before editing.
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: Explore
argument-hint: "[directory or feature name]"
---

Explore **$ARGUMENTS** thoroughly and return a structured summary.

## Steps

1. **Find all files** in the target area using Glob
2. **Read entry points first** — look for index.ts, main.ts, app.ts, __init__.py
3. **Map imports/exports** — understand what depends on what
4. **Identify patterns** — naming conventions, file structure, coding style
5. **Check tests** — find related test files and understand testing approach
6. **Look for docs** — README, comments, JSDoc, docstrings

## Return Format

```
## Area: [name]

### Key Files
- [file] → [purpose]

### Dependencies
- Imports from: [list]
- Exported to: [list]

### Patterns
- [naming, structure, style patterns observed]

### Tests
- [test approach, test file locations]

### Gotchas
- [anything unusual, legacy code, known issues]
```

Be concise. Focus on what someone would need to know before making changes.

<!-- Skill by Huzefa Nalkheda Wala | claude-code-optimizer -->
