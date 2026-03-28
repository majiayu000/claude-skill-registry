---
name: gen-context
description: Use when starting a new session, the project has changed significantly, or you need a fresh context summary.
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: Explore
---

Generate a comprehensive but concise project context by analyzing the codebase.

## Steps

1. **Read package.json / pyproject.toml / Cargo.toml** → identify stack, dependencies, scripts
2. **Scan top-level structure** → `Glob("*")` then `Glob("src/*")` or equivalent
3. **Find entry points** → main files, index files, app setup files
4. **Identify framework** → Express, Next.js, FastAPI, Django, etc.
5. **Check for existing CLAUDE.md** → read current instructions
6. **Read recent git history** → `git log --oneline -10`
7. **Identify key patterns** → how routes/components/models are structured

## Return Format

```
## Project: [name]
## Stack: [framework, language, database, etc.]

### Commands
- Build: [command]
- Test: [command]
- Dev: [command]

### Entry Points
- [file] → [what it wires together]

### Structure
- [dir/] → [purpose]

### Recent Activity
- [last 5 commits summarized]

### Suggested CLAUDE.md Updates
- [anything missing from current CLAUDE.md]
```

<!-- Skill by Huzefa Nalkheda Wala | claude-code-optimizer -->
