---
name: review-changes
description: Review uncommitted code changes for bugs, security issues, and style violations.
user-invocable: true
argument-hint: "[--staged | --all | <file-path>]"
context: fork
agent: reviewer
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
disable-model-invocation: true
---

# Code Review

Review uncommitted code changes for bugs, security issues, and style violations.

## Changes to Review
!`git diff --cached 2>/dev/null || echo "(nothing staged)"`
!`git diff 2>/dev/null || echo "(no unstaged changes)"`
!`git ls-files --others --exclude-standard 2>/dev/null || echo "(no untracked files)"`

## Scope

Parse `$ARGUMENTS` to determine what to review:
- `--staged` — only staged changes (git diff --cached)
- `--all` — all changes including unstaged and untracked
- `<file-path>` — review a specific file
- No args — review staged changes if any, otherwise all changes

## Review Checklist

For each changed file, evaluate:

### Correctness
- [ ] Logic errors or off-by-one mistakes
- [ ] Missing null/undefined checks at system boundaries
- [ ] Incorrect error handling (swallowed errors, wrong catch scope)
- [ ] Race conditions in async code
- [ ] Resource leaks (unclosed files, connections, watchers)

### Security
- [ ] Command injection (unsanitized input in shell commands)
- [ ] Path traversal (user input in file paths)
- [ ] Secrets or credentials in code or config
- [ ] Exposed env vars or API keys
- [ ] SQL injection (if applicable)

### Style & Conventions
- [ ] TypeScript types (no unnecessary `any`)
- [ ] Consistent naming (camelCase functions, PascalCase types)
- [ ] Import organization
- [ ] Dead code or unused variables

### AI Harness Specific
- [ ] Claude CLI spawning follows the 7 rules in CLAUDE.md
- [ ] `--` separator before prompt arguments
- [ ] CLAUDE* env vars stripped in subprocess spawning
- [ ] Disallowed tools guardrails included in Claude invocations
- [ ] File-based output pattern used (not pipes)

## Output Format

```
## Code Review: <scope>

### Summary
<1-2 sentence overview>

### Issues Found
1. **[SEVERITY]** file.ts:L42 — Description of issue
   Suggestion: <how to fix>

2. **[SEVERITY]** file.ts:L87 — Description of issue
   Suggestion: <how to fix>

### Approved
- file.ts — No issues found

### Verdict
APPROVE / REQUEST_CHANGES / NEEDS_DISCUSSION
```

Severity levels: `CRITICAL` (must fix), `WARNING` (should fix), `NITS` (optional improvement).
