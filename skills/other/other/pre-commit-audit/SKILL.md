---
name: vibe-pre-commit-audit
description: Scans staged changes for secrets, debug statements, TODOs without references, and other common commit mistakes. Use before creating any commit.
user-invocable: true
---

# vibe-pre-commit-audit

Catch the easy mistakes before they enter history.

## When to Use This Skill

- Before creating a git commit
- When reviewing your own staged changes
- Before pushing to a shared branch

## When NOT to Use This Skill

- Commits to personal scratch branches
- When the user explicitly says to skip checks
- Auto-generated code commits (lock files, etc.)

## Checks

### 1. Secrets & Credentials
Scan for patterns:
- `API_KEY=`, `SECRET=`, `PASSWORD=`, `TOKEN=`
- AWS keys: `AKIA[0-9A-Z]{16}`
- Private keys: `-----BEGIN.*PRIVATE KEY-----`
- Connection strings with credentials
- `.env` files being staged

### 2. Debug Statements
- `console.log(`, `fmt.Println(`, `print(`, `debugger;`
- `// DEBUG`, `# DEBUG`, `/* DEBUG`
- `log.Debug` in non-debug code paths

### 3. TODOs Without References
- `TODO` without issue number: `TODO: fix this` (bad)
- `TODO(#123): fix this` (good)
- `FIXME`, `HACK`, `XXX` — flag all

### 4. Disabled Tests
- `t.Skip(`, `xit(`, `xdescribe(`, `@pytest.mark.skip`
- Commented-out test functions
- `//nolint` without justification

### 5. Large Files
- Files > 1MB
- Binary files (images, compiled assets)
- Lock files with excessive changes

### 6. Commented-Out Code
- Blocks of 3+ consecutive commented-out lines of code
- Not comments explaining code, but actual code that's commented out

## Output Format

### Pre-Commit Audit

**Status**: CLEAN / WARNINGS / BLOCKED

| Check | Status | Findings |
|-------|--------|----------|
| Secrets | ✓/✗ | X patterns found |
| Debug statements | ✓/✗ | X occurrences |
| TODOs | ✓/◐ | X without references |
| Disabled tests | ✓/✗ | X found |
| Large files | ✓/✗ | X over limit |
| Commented code | ✓/◐ | X blocks |

### Blocking Issues (must fix)
1. [Secret found in file.go:42]

### Warnings (should fix)
1. [TODO without reference in handler.ts:15]
