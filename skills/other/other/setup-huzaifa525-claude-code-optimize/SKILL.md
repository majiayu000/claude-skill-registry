---
name: setup
description: Use when the user wants to set up Claude Code for a project, initialize optimization, or generate CLAUDE.md.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash, Write
argument-hint: "[optional: project name]"
---

Set up Claude Code optimization for this project. Analyze the codebase and generate project-specific files.

## Steps

### 1. Detect Project Stack

Read these files (skip if not found):
- `package.json` → Node.js/JS/TS project
- `pyproject.toml` or `requirements.txt` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust
- `Gemfile` → Ruby
- `pom.xml` or `build.gradle` → Java
- `docker-compose.yml` → Docker setup
- `turbo.json` or `pnpm-workspace.yaml` → Monorepo

### 2. Find Entry Points

```
# Look for main/index files
Glob("**/index.{ts,js,tsx,jsx,py}")
Glob("**/main.{ts,js,py,go,rs}")
Glob("**/app.{ts,js,py}")
Glob("**/server.{ts,js}")
```

### 3. Find Route/API Registration

```
Grep("router|app\.(get|post|put|delete|use)|@(Get|Post|Controller)|urlpatterns|HandleFunc")
```

### 4. Detect Test Framework

```
Glob("**/*.test.*")
Glob("**/*.spec.*")
Glob("**/tests/**")
Glob("**/__tests__/**")
```

### 5. Detect Config Files

```
Glob("**/.eslintrc*")
Glob("**/.prettierrc*")
Glob("**/tsconfig.json")
Glob("**/ruff.toml")
Glob("**/.editorconfig")
```

### 6. Check Git Info

```bash
git log --oneline -5
git branch --show-current
```

### 7. Generate CLAUDE.md

Write `CLAUDE.md` to the project root with:

```markdown
# Project: [detected name or $ARGUMENTS]

## Commands
- Build: [detected from package.json scripts or Makefile]
- Test: [detected test command]
- Lint: [detected lint command]
- Dev: [detected dev command]

## Entry Points
- [detected entry files with descriptions]

## Request Flow
[detected from framework: e.g., Client → Express → Middleware → Route → Controller → Service → DB]

## Data Flow
[detected from ORM/database setup]

## Key Decisions
- [fill in — prompt user to complete this section]

## Things That Look Wrong But Aren't
- [fill in — prompt user to complete this section]

## Conventions
- [detected from linter config, existing code patterns]
- [detected test conventions]

## Code Annotations
- Search `@claude-entry` for system entry points
- Search `@claude-pattern` for examples to follow
- Search `@claude-warning` for files not to modify

## Workflow
- New feature → /plan first, then /smart-edit to implement
- Bug fix → /debug-error or /fix-issue [number]
- Before editing unfamiliar code → /explore-area [dir]
- After all changes → /review then /commit
- Ready to merge → /create-pr
- New developer → /onboard
```

### 8. Generate .claudeignore

Write `.claudeignore` based on detected stack:

- **Always include:** node_modules, .git, dist, build, *.log, .env*, coverage, *.min.js
- **Node.js:** + package-lock.json, yarn.lock, pnpm-lock.yaml, .next, .nuxt
- **Python:** + __pycache__, *.pyc, .venv, .mypy_cache, .ruff_cache, *.egg-info
- **Go:** + vendor, bin
- **Rust:** + target
- **Assets:** + *.png, *.jpg, *.gif, *.ico, *.woff, *.woff2, *.ttf, *.mp4, *.pdf

### 9. Generate .claude/settings.json (if not exists)

Only if `.claude/settings.json` doesn't already exist, copy it from the global settings:

```json
{
  "env": {
    "MAX_THINKING_TOKENS": "10000"
  },
  "hooks": {
    // ... all hooks pointing to ~/.claude/hooks/
  }
}
```

### 10. Summary

Tell the user:
```
Setup complete!

Created:
  + CLAUDE.md — edit Key Decisions and Things That Look Wrong sections
  + .claudeignore — [X] patterns for [stack]
  + .claude/settings.json — hooks wired, thinking tokens capped

Auto-detected:
  - Stack: [framework, language, database]
  - Entry points: [count] files
  - Test framework: [name]
  - Commands: build, test, lint, dev

Next: fill in the [bracketed sections] in CLAUDE.md with your project-specific details.
```

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
