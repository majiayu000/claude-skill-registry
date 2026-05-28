---
name: release-checklist
description: Run a final release checklist before shipping. Verifies no TODOs, no debug code, docs updated, tests passing, dependencies justified, and security reviewed.
tools: Read, Grep, Glob, Bash
user-invocable: true
---

# Release Checklist

A final quality gate before shipping code. This skill runs through everything a senior developer would check before approving a release.

## Quick Start

```
/release-checklist
```

Or specify a scope:
```
/release-checklist src/auth/
```

## The Checklist

Run through each section systematically. Any failure blocks the release.

### 1. Code Completeness

```bash
# Search for incomplete code markers
grep -r "TODO\|FIXME\|XXX\|HACK\|WIP" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.rs" --include="*.rb" --include="*.ex" src/
```

- [ ] No TODO comments remain
- [ ] No FIXME markers
- [ ] No HACK or XXX notes
- [ ] No WIP (work in progress) code
- [ ] No placeholder implementations (`throw new Error('Not implemented')`)
- [ ] No commented-out code that should be removed

### 2. Debug Code Removed

```bash
# Search for debug statements
grep -rn "console\.log\|print(\|debugger\|binding\.pry\|byebug\|IEx\.pry" --include="*.ts" --include="*.js" --include="*.py" --include="*.rb" --include="*.ex" src/
```

- [ ] No `console.log` in production code (logging libraries OK)
- [ ] No `print()` statements (Python)
- [ ] No `debugger` statements
- [ ] No `binding.pry` / `byebug` (Ruby)
- [ ] No `IEx.pry` (Elixir)
- [ ] No hardcoded test data or mock values

### 3. Documentation Updated

- [ ] README reflects current functionality
- [ ] API documentation matches implementation
- [ ] CHANGELOG has entries for all changes
- [ ] Configuration options documented
- [ ] Breaking changes clearly noted
- [ ] Migration guide if needed

### 4. Tests Passing

Run all test commands from CLAUDE.md:

```bash
# Example - adapt to your project
npm test        # or pytest, go test, etc.
npm run lint    # or ruff, golangci-lint, etc.
npm run typecheck  # or mypy, tsc, etc.
npm run build   # verify it compiles
```

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Lint checks pass (no errors)
- [ ] Type checks pass (no errors)
- [ ] Build succeeds

### 5. Dependencies Justified

For any new dependencies added:

- [ ] Each dependency has a clear reason for inclusion
- [ ] Licenses are compatible (MIT, Apache, BSD, etc.)
- [ ] Packages are actively maintained
- [ ] No known security vulnerabilities
- [ ] Versions are pinned appropriately
- [ ] Lockfile is committed

```bash
# Check for outdated or vulnerable packages
npm audit       # Node.js
pip-audit       # Python
go list -m -u all  # Go
cargo audit     # Rust
bundle audit    # Ruby
mix deps.audit  # Elixir (with mix_audit)
```

### 6. Security Review

- [ ] No hardcoded secrets, keys, or tokens
- [ ] Input validation on all external data
- [ ] SQL queries use parameterized statements
- [ ] User content is escaped before rendering
- [ ] Authentication/authorization enforced
- [ ] Sensitive data not logged
- [ ] Error messages don't leak internals

### 7. Production Readiness

- [ ] Structured logging (not print statements)
- [ ] Errors categorized appropriately
- [ ] Health check endpoint works (if applicable)
- [ ] Graceful shutdown handling
- [ ] Environment-specific config externalized
- [ ] No hardcoded URLs or environment assumptions

## Output Format

```markdown
## Release Checklist Results

### Passed
- [x] No TODO/FIXME markers
- [x] No debug statements
- [x] Tests passing
- [x] Lint passing
- [x] Build succeeds

### Failed
- [ ] CHANGELOG not updated (missing entry for new auth feature)
- [ ] Found console.log at src/api/users.ts:45

### Warnings
- [ ] New dependency 'lodash' added - verify it's needed (could use native methods)

### Verdict
**BLOCKED** - Fix the failures above before releasing.
```

## When to Use

- Before merging a feature branch
- Before cutting a release tag
- Before deploying to production
- As the final step in a wiggum loop

## Integration with Wiggum

When used as part of a wiggum loop, this checklist runs during Phase 5 (Final Verification). All items must pass before the loop can complete.

## Remember

This checklist exists because senior developers do these checks naturally. Making them explicit ensures nothing slips through, especially in automated workflows.

**If any item fails, the release is blocked.** Fix the issue and run the checklist again.
