---
name: commit-detection
description: Detects optimal commit type from git changes. Use when analyzing commits, determining commit type, or before committing.
allowed-tools: Bash, Read, Grep
---

# Commit Type Detection Skill

Expert knowledge for detecting the optimal conventional commit type.

## Detection Algorithm

### Step 1: Gather Data

```bash
# Get modified files
git diff --name-only
git diff --staged --name-only

# Get change statistics
git diff --stat
git diff --staged --stat

# Check for keywords in diff
git diff | grep -i "fix\|bug\|error" | head -5
```

### Step 2: Categorize Files

| Category | File Patterns |
|----------|---------------|
| docs | `*.md`, `*.txt`, `*.rst`, `README*`, `CHANGELOG*` |
| test | `*.test.*`, `*.spec.*`, `__tests__/*`, `test/*` |
| config | `*.json`, `*.yml`, `*.yaml`, `*.toml`, `.*rc` |
| ci | `.github/*`, `.gitlab-ci.yml`, `Jenkinsfile` |
| build | `package.json`, `Makefile`, `webpack.*`, `vite.*` |
| style | Only whitespace, formatting changes |
| src | `*.ts`, `*.js`, `*.py`, `*.go`, `*.rs`, etc. |

### Step 3: Apply Rules

```
IF only docs files changed:
  → docs

IF only test files changed:
  → test

IF only config/build files changed:
  → chore

IF only CI files changed:
  → ci

IF diff contains "fix", "bug", "error", "issue", "resolve":
  → fix

IF new files added with business logic:
  → feat

IF files renamed/moved without logic change:
  → refactor

IF performance keywords ("optimize", "perf", "speed", "cache"):
  → perf

IF formatting only (whitespace, semicolons):
  → style

DEFAULT:
  → Use /commit-pro:commit for smart analysis
```

### Step 4: Determine Scope

Extract scope from primary directory:

```
src/components/Button.tsx → ui or button
src/api/auth.ts → auth
lib/utils/date.ts → utils
server/routes/user.ts → user
```

## Quick Reference

| Type | When |
|------|------|
| `feat` | New functionality |
| `fix` | Bug correction |
| `docs` | Documentation only |
| `style` | Formatting only |
| `refactor` | Code restructure |
| `perf` | Performance |
| `test` | Tests only |
| `build` | Build/deps |
| `ci` | CI/CD config |
| `chore` | Maintenance |

## Examples

**Example 1: Only README changed**
```
Files: README.md
→ /commit-pro:docs
```

**Example 2: New component + test**
```
Files: src/Button.tsx, src/Button.test.tsx
→ /commit-pro:feat (primary is new feature)
```

**Example 3: Fix in existing file**
```
Files: src/api/auth.ts
Diff contains: "fix login bug"
→ /commit-pro:fix
```
