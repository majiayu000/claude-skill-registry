---
name: quality
description: Run a comprehensive code quality review. Checks security, performance, maintainability, project conventions (CLAUDE.md), architecture, and testing. Runs rustfmt and bazel test. Use when user asks for 'review', 'check', 'validate', 'quality', 'lint', or before committing. (project)
allowed-tools: Read, Glob, Grep, Bash(bazel run:*), Bash(bazel build:*), Bash(bazel test:*), Bash(git status:*), Bash(rustfmt:*), Bash(find:*), Bash(xargs:*), Bash(cargo:*)
---

# Code Quality Review

## Activation

- [ ] EVALUATE: Does this request involve code review, quality checks, validation, or pre-commit checks?
- [ ] DECIDE: "This task requires /quality because..."
- [ ] EXECUTE: Follow the workflow below

Expert code reviewer. Comprehensive multi-pass review covering conventions, security, performance, and architecture.

## Process

### 1. Prepare

Identify target files (user-specified or git status), then run automated checks:

```bash
bazel run //:format.rust -- --check $(find . -name "*.rs" -not -path "*/bazel-*")
bazel test //...
```

Report any failures before proceeding.

### 2. Conventions

Verify against CLAUDE.md CRITICAL sections:

- **Naming**: single words, no underscores, no abbreviations
- **Module Organization**: no mod, pub use only, one-level depth
- **Code Quality**: miette errors, turbofish, no comments

Flag violations from NEVER sections immediately.

### 3. Security

Check for (see security.md for patterns):

- **Secrets**: hardcoded passwords, tokens, API keys
- **Injection**: user input in `Command::new()`, `format!()` paths, SQL strings
- **Boundaries**: external input validated before use
- **Errors**: no sensitive info (paths, connection strings) in error messages

### 4. Performance

Check for (see performance.md for patterns):

- **Allocations**: unnecessary `.clone()`, `.to_string()`
- **Iteration**: `.collect()` when streaming works, multiple passes
- **Complexity**: O(n^2) where O(n log n) possible
- **Async**: blocking in async context, sequential when parallel possible

### 5. Architecture

- Single responsibility per function/module
- No circular dependencies
- Consistent with existing patterns
- No over-abstraction

## Output Format

```markdown
## Quality Review Summary

| Category | Status | Issues |
|----------|--------|--------|
| Formatting | PASS/WARN/FAIL | N |
| Tests | PASS/WARN/FAIL | N |
| Conventions | PASS/WARN/FAIL | N |
| Security | PASS/WARN/FAIL | N |
| Performance | PASS/WARN/FAIL | N |
| Architecture | PASS/WARN/FAIL | N |

**Overall**: PASS/WARN/FAIL

## Findings

### [Category]

**[file:line]** - Issue description
**Fix**: Suggested fix
```

## Non-Negotiable Violations

Flag these immediately (from CLAUDE.md NEVER sections):

1. Underscores in identifiers
2. Comments in code
3. `mod` directive usage
4. Deep or glob re-exports
5. Type annotations instead of turbofish
6. Missing miette diagnostics
7. Hardcoded secrets
8. Unsanitized input at boundaries
