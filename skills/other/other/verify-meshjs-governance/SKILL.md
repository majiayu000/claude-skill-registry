---
name: verify
updated: 2026-02-20
description: Pre-PR verification loop. Runs build, type check, lint, security audit, and debug statement scan. Use before creating PRs or merging.
argument-hint: [quick|full|pre-pr] (default: full)
allowed-tools: Bash, Grep, Glob, Read, TodoWrite
---

# Verify

Comprehensive verification before PRs. Runs all quality gates and produces a structured pass/fail report.

## Modes

- **quick**: Build + type check only (fastest)
- **full** (default): Build + types + lint + debug statement audit + git status
- **pre-pr**: Full + security scan (secrets, env files, API keys)

## Instructions

### Step 1: Determine Mode and Build System

Check the argument. Default to `full` if none provided.

Detect the build system:
- `package.json` → npm/yarn/pnpm (check for `build`, `typecheck`, `lint` scripts)
- `Cargo.toml` → cargo (build, clippy)
- `go.mod` → go (build, vet, lint)
- `pyproject.toml` → python (build, mypy, ruff/flake8)
- `Makefile` → make targets

### Step 2: Run Checks

Run checks sequentially. Stop early on CRITICAL failures (build, types) since later checks depend on them.

#### 2a. Build Check

```bash
<build-command> 2>&1
```

- **PASS**: Build completes without errors
- **FAIL**: Any build errors

If build fails, STOP. Report the errors and suggest running `/build-fix`.

#### 2b. Type Check (quick mode stops here)

The build usually includes type checking. For explicit type check without full build:
- TypeScript: `npx tsc --noEmit`
- Python: `mypy .` or `pyright`
- Go: `go vet ./...`
- Rust: `cargo check`

#### 2c. Lint Check

- JS/TS: `npm run lint` or `npx eslint .`
- Python: `ruff check .` or `flake8`
- Go: `golangci-lint run`
- Rust: `cargo clippy`

- **PASS**: No lint errors (warnings are OK)
- **FAIL**: Any lint errors

#### 2d. Debug Statement Audit

Search for debug statements in source files (excluding node_modules, build output, tests):

| Language | Pattern |
|----------|---------|
| JS/TS | `console.log(` |
| Python | `print(` (in non-CLI code), `breakpoint()`, `pdb.set_trace()` |
| Go | `fmt.Println(` (debug-only) |
| Rust | `dbg!(` |

- **PASS**: No debug statements
- **WARN**: Debug statements found (list file:line)

#### 2e. Security Scan (pre-pr mode only)

Search for potential secrets and sensitive data:

Use Grep tool to search across source files:
- Hardcoded API keys: `api[_-]?key\s*[:=]\s*['"][^'"]+['"]` (case insensitive)
- Hardcoded secrets: `secret\s*[:=]\s*['"][^'"]+['"]` (case insensitive)
- Hardcoded passwords: `password\s*[:=]\s*['"][^'"]+['"]` (case insensitive)
- Private keys: `-----BEGIN.*PRIVATE KEY-----`
- `.env` files committed: `git ls-files | grep '\.env'`

Also check that `.env` is in `.gitignore`.

#### 2f. Git Status

```bash
git status
git diff --stat
```

Report uncommitted changes, untracked files.

### Step 3: Report

```
VERIFICATION: [PASS/FAIL]
═══════════════════════════════
Build:        [PASS/FAIL]
Types:        [PASS/FAIL] (X errors)
Lint:         [PASS/FAIL] (X issues)
Debug stmts:  [CLEAN/X found]
Security:     [CLEAN/X issues] (pre-pr only)
Git:          [clean/X uncommitted changes]
═══════════════════════════════
Ready for PR: [YES/NO]
```

If any check fails, list the specific failures below the report with file:line references.

### Step 4: Recommendations

If verification fails:
- Build/Type errors → suggest `/build-fix`
- Lint issues → suggest auto-fix command
- Debug statements → list files to clean
- Security issues → flag as CRITICAL, do not proceed
- Uncommitted changes → suggest committing or stashing
