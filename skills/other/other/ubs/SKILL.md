---
name: ubs
description: "Ultimate Bug Scanner - Pre-commit static analysis for AI coding workflows. 18 detection categories, 8 languages, 4-layer analysis engine. The AI agent's quality gate."
---

# UBS - Ultimate Bug Scanner

Static analysis tool built for AI coding workflows. Catches bugs that AI agents commonly introduce: null safety, async/await issues, security holes, memory leaks. Scans JS/TS, Python, Go, Rust, Java, C++, Ruby, Swift in 3-5 seconds.

## Why This Exists

AI agents move fast. Bugs move faster. You're shipping features in minutes, but:
- Null pointer crashes slip through
- Missing `await` causes silent failures
- XSS vulnerabilities reach production
- Memory leaks accumulate

UBS is the quality gate: scan before commit, fix before merge.

## Golden Rule

```bash
ubs <changed-files> --fail-on-warning
```

**Exit 0 = safe to commit. Exit 1 = fix and re-run.**

## Essential Commands

### Quick Scans (Use These)

```bash
ubs file.ts file2.py                    # Specific files (< 1s)
ubs $(git diff --name-only --cached)    # Staged files
ubs --staged                            # Same, cleaner syntax
ubs --diff                              # Working tree vs HEAD
```

### Full Project Scans

```bash
ubs .                                   # Current directory
ubs /path/to/project                    # Specific path
ubs --only=js,python src/               # Language filter (faster)
```

### CI/CD Mode

```bash
ubs --ci --fail-on-warning .            # Strict mode for CI
ubs --format=json .                     # Machine-readable
ubs --format=sarif .                    # GitHub code scanning
```

## Output Format

```
⚠️  Category (N errors)
    file.ts:42:5 – Issue description
    💡 Suggested fix
Exit code: 1
```

Parse: `file:line:col` → location | `💡` → how to fix | Exit 0/1 → pass/fail

## The 18 Detection Categories

### Critical (Always Fix)

| Category | What It Catches |
|----------|-----------------|
| **Null Safety** | Unguarded property access, missing null checks |
| **Security** | XSS, injection, prototype pollution, hardcoded secrets |
| **Async/Await** | Missing await, unhandled rejections, race conditions |
| **Memory Leaks** | Event listeners without cleanup, timer leaks |
| **Type Coercion** | `==` vs `===`, `parseInt` without radix, NaN comparison |

### Important (Production Risk)

| Category | What It Catches |
|----------|-----------------|
| **Division Safety** | Division without zero check |
| **Resource Lifecycle** | Unclosed files, connections, context managers |
| **Error Handling** | Empty catch blocks, swallowed errors |
| **Promise Chains** | `.then()` without `.catch()` |
| **Array Mutations** | Mutating during iteration |

### Code Quality (Contextual)

| Category | What It Catches |
|----------|-----------------|
| **Debug Code** | `console.log`, `debugger`, `print()` statements |
| **TODO Markers** | `TODO`, `FIXME`, `HACK` comments |
| **Type Safety** | TypeScript `any` usage |
| **Readability** | Complex ternaries, deep nesting |

## Language-Specific Detection

| Language | Key Patterns |
|----------|-------------|
| **JavaScript/TypeScript** | innerHTML XSS, eval(), missing await, React hooks deps |
| **Python** | eval(), open() without with, missing encoding=, None checks |
| **Go** | Nil pointer, goroutine leaks, defer symmetry, context cancel |
| **Rust** | `.unwrap()` panics, `unsafe` blocks, Option handling |
| **Java** | Resource leaks (try-with-resources), null checks, JDBC |
| **C/C++** | Buffer overflows, strcpy(), memory leaks, use-after-free |
| **Ruby** | eval(), send(), instance_variable_set |
| **Swift** | Force unwrap (!), ObjC bridging issues |

## Profiles

```bash
ubs --profile=strict .    # Fail on warnings, enforce high standards
ubs --profile=loose .     # Skip TODO/debug nits when prototyping
```

## Category Packs (Focused Scans)

```bash
ubs --category=resource-lifecycle .    # Python/Go/Java resource hygiene
```

Narrows scan to relevant languages and suppresses unrelated categories.

## Comparison Mode (Regression Detection)

```bash
# Capture baseline
ubs --ci --report-json .ubs/baseline.json .

# Compare against baseline
ubs --ci --comparison .ubs/baseline.json --report-json .ubs/latest.json .
```

Useful for CI to detect regressions vs. main branch.

## Output Formats

| Format | Flag | Use Case |
|--------|------|----------|
| **text** | (default) | Human-readable terminal output |
| **json** | `--format=json` | Machine parsing, scripting |
| **jsonl** | `--format=jsonl` | Line-delimited, streaming |
| **sarif** | `--format=sarif` | GitHub code scanning |
| **html** | `--html-report=file.html` | PR attachments, dashboards |

## Inline Suppression

When a finding is intentional:

```javascript
eval(trustedCode);  // ubs:ignore

// ubs:ignore-next-line
dangerousOperation();
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | No critical issues (safe to commit) |
| `1` | Critical issues or warnings (with `--fail-on-warning`) |
| `2` | Environment error (missing ast-grep, etc.) |

## Doctor Command

```bash
ubs doctor                # Check environment
ubs doctor --fix          # Auto-fix missing dependencies
```

Checks: curl/wget, ast-grep, ripgrep, jq, typos, Node.js + TypeScript.

## Agent Integration

UBS auto-configures hooks for coding agents during install:

| Agent | Hook Location |
|-------|---------------|
| **Claude Code** | `.claude/hooks/on-file-write.sh` |
| **Cursor** | `.cursor/rules` |
| **Codex CLI** | `.codex/rules/ubs.md` |
| **Gemini** | `.gemini/rules` |
| **Windsurf** | `.windsurf/rules` |
| **Cline** | `.cline/rules` |

### Claude Code Hook Pattern

```bash
#!/bin/bash
# .claude/hooks/on-file-write.sh
if [[ "$FILE_PATH" =~ \.(js|jsx|ts|tsx|py|go|rs|java|rb)$ ]]; then
  echo "🔬 Quality check running..."
  if ubs "${PROJECT_DIR}" --ci 2>&1 | head -30; then
    echo "✅ No critical issues"
  else
    echo "⚠️  Issues detected - review above"
  fi
fi
```

### Git Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
echo "🔬 Running bug scanner..."
if ! ubs . --fail-on-warning 2>&1 | tail -30; then
  echo "❌ Critical issues found. Fix or: git commit --no-verify"
  exit 1
fi
echo "✅ Quality check passed"
```

## Performance

```
Small (5K lines):     0.8 seconds
Medium (50K lines):   3.2 seconds
Large (200K lines):   12 seconds
Huge (1M lines):      58 seconds
```

10,000+ lines per second. Use `--jobs=N` to control parallelism.

## Speed Tips

1. **Scope to changed files**: `ubs src/file.ts` (< 1s) vs `ubs .` (30s)
2. **Use --staged or --diff**: Only scan what you're committing
3. **Language filter**: `--only=js,python` skips irrelevant scanners
4. **Skip categories**: `--skip=11,14` to skip debug/TODO markers

## Fix Workflow

```
1. Read finding → category + fix suggestion
2. Navigate file:line:col → view context
3. Verify real issue (not false positive)
4. Fix root cause (not symptom)
5. Re-run ubs <file> → exit 0
6. Commit
```

## Bug Severity Guide

- **Critical** (always fix): Null safety, XSS/injection, async/await, memory leaks
- **Important** (production): Type narrowing, division-by-zero, resource leaks
- **Contextual** (judgment): TODO/FIXME, console logs

## Common Anti-Patterns

| Don't | Do |
|-------|-----|
| Ignore findings | Investigate each |
| Full scan per edit | Scope to changed files |
| Fix symptom (`if (x) { x.y }`) | Fix root cause (`x?.y`) |
| Suppress without understanding | Verify false positive first |

## Installation

```bash
# One-liner (recommended)
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/ultimate_bug_scanner/master/install.sh?$(date +%s)" | bash -s -- --easy-mode

# Manual
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/ultimate_bug_scanner/master/ubs \
  -o /usr/local/bin/ubs && chmod +x /usr/local/bin/ubs
```

## Custom AST Rules

```bash
mkdir -p ~/.config/ubs/rules

cat > ~/.config/ubs/rules/no-console.yml <<'EOF'
id: custom.no-console
language: javascript
rule:
  pattern: console.log($$$)
severity: warning
message: "Remove console.log before production"
EOF

ubs . --rules=~/.config/ubs/rules
```

## Excluding Paths

```bash
ubs . --exclude=legacy,generated,vendor
```

Auto-ignored: `node_modules`, `.venv`, `dist`, `build`, `target`, editor caches.

## Session Logs

```bash
ubs sessions --entries 1    # View latest install session
```

## Integration with Flywheel

| Tool | Integration |
|------|-------------|
| **BV** | `--beads-jsonl=out.jsonl` exports findings for Beads |
| **CASS** | Search past sessions for similar bug patterns |
| **CM** | Extract rules from UBS findings |
| **Agent Mail** | Notify agents of scan results |
| **DCG** | UBS runs inside DCG protection |

## Troubleshooting

| Error | Fix |
|-------|-----|
| "Environment error" (exit 2) | `ubs doctor --fix` |
| "ast-grep not found" | `brew install ast-grep` or `cargo install ast-grep` |
| Too many false positives | Use `--skip=N` or `// ubs:ignore` |
| Slow scans | Scope to files: `ubs <file>` not `ubs .` |
