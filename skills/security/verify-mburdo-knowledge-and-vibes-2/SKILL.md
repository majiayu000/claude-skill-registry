---
name: verify
description: Security scanning with UBS (Ultimate Bug Scanner). Use before commits, when scanning for bugs, when the user mentions "ubs", "bugs", "scan", "verify", or "security".
---

# Verify — Security Scanning

Scans for 1000+ bug patterns across multiple languages. Direct execution.

> **Design rationale:** This skill executes directly as a simple command sequence. UBS handles the analysis internally. No subagents needed.

## When This Applies

| Signal | Action |
|--------|--------|
| Before committing | `ubs --staged` |
| Scanning changes | `ubs --diff` |
| Scanning specific file | `ubs path/to/file` |
| User says "/verify" | Run security scan |
| Closing a bead | `ubs --staged` (mandatory) |

---

## Mandatory Gate

**UBS is a mandatory gate before every commit.** This is not optional.

Research shows ~40% of LLM-generated code contains security vulnerabilities. The `ubs --staged` command must pass before any commit.

---

## Pre-Commit (Required)

**Run before every commit:**

```bash
ubs --staged                       # Scan staged changes
ubs --staged --fail-on-warning     # Strict mode (exit 1 on any issue)
```

**Fix all issues before committing. Rerun until clean.**

---

## Scanning Options

```bash
# Scan current directory
ubs .

# Scan specific file
ubs path/to/file.ts

# Scan working tree changes vs HEAD
ubs --diff

# Verbose with code examples
ubs -v .
```

---

## Profiles

```bash
# Strict (fail on warnings) - for production code
ubs --profile=strict .

# Loose (skip nits) - for prototyping
ubs --profile=loose .
```

---

## Language Filters

```bash
# Single language
ubs --only=python .

# Multiple languages
ubs --only=typescript,javascript .
```

**Supported languages:**
- javascript, typescript
- python
- c, c++
- rust, go
- java, ruby

---

## Output Formats

```bash
ubs . --format=json                # JSON
ubs . --format=jsonl               # Line-delimited JSON
ubs . --format=sarif               # GitHub Code Scanning
```

---

## CI Integration

```bash
ubs --ci                           # CI mode
ubs --comparison baseline.json .   # Regression detection
```

---

## Suppressing False Positives

Add to the line:
```javascript
// ubs:ignore
const result = eval(userInput); // ubs:ignore
```

**Use sparingly.** Over-suppression defeats the purpose.

---

## Health Check

```bash
ubs doctor
ubs doctor --fix
```

---

## Workflow Integration

The standard pre-commit workflow (via /advance):

```bash
# 1. Run tests
pytest  # or npm test, etc.

# 2. Scan staged changes (MANDATORY)
ubs --staged

# 3. Fix any issues found
# 4. Re-run until clean (counts toward 3-iteration cap)
ubs --staged

# 5. Commit
git add -A && git commit
```

---

## Issue Handling

| Issue Level | Action |
|-------------|--------|
| Critical | Fix immediately, blocks commit |
| High | Fix before commit |
| Medium | Fix or document justification |
| Low | Fix if easy, otherwise note |

**Fixing UBS issues counts toward your 3-iteration cap.** If you've hit 3 iterations and still have issues, stop and escalate.

---

## Quick Reference

```bash
ubs --staged               # Pre-commit scan (required)
ubs --staged --fail-on-warning   # Strict pre-commit
ubs --diff                 # Working tree changes
ubs path/to/file           # Specific file
ubs --profile=strict .     # Production mode
ubs doctor --fix           # Health check
```

---

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Skip `ubs --staged` | Bugs slip into commits | Always run before commit |
| Ignore warnings | May be real issues | Review each warning |
| Over-suppress with `// ubs:ignore` | Defeats the purpose | Use sparingly |
| Run unlimited fix iterations | Security degrades | Max 3 iterations |

---

## See Also

- `/advance` — Bead workflow (includes verify gate)
- `/release` — Pre-ship checklist (includes full verification)
