---
name: comment-quality
description: "Review and fix temporal references in code comments."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
routing:
  triggers:
    - "review comments"
    - "fix temporal references"
    - "comment quality"
    - "stale comments"
    - "outdated comment"
  category: code-quality
  pairs_with:
    - code-cleanup
    - systematic-code-review
---

# Comment Quality Skill

Review code comments for temporal references, development-activity language, and relative comparisons. Produces structured reports with actionable rewrites that explain WHAT the code does and WHY, only WHAT the code does and WHY. Supports `.go`, `.py`, `.js`, `.ts`, `.md`, and `.txt` files.

## Instructions

### Phase 1: SCAN

**Goal**: Identify all comments containing temporal, activity, or relative language.

**Step 1: Determine scope**

Read the repository CLAUDE.md first to pick up any project-specific comment conventions.

Scan only what was requested. If user specifies files, scan those files. If user specifies a directory, scan that directory. Honor the explicit scope -- even if you suspect other files have issues, honor the explicit scope and suggest expansion separately at the end.

If user explicitly requests auto-fix, enable it. Otherwise present findings for review. For large codebases, group findings by directory when reporting.

**Step 2: Search for temporal patterns**

Flag every instance of the following categories. No temporal word is "harmless" -- all temporal language ages poorly and must be rewritten regardless of how innocuous it seems:

- **Temporal words**: "new", "old", "previous", "current", "now", "recently", "latest", "modern"
- **Development activity**: "added", "removed", "deleted", "updated", "changed", "modified", "fixed", "improved", "enhanced", "refactored", "optimized"
- **State transitions**: "replaced", "migrated", "upgraded", "deprecated", "became", "turned into", "evolved"
- **Date references**: "as of", "since", "from", "after", "before"
- **Relative comparisons**: "better than", "faster than", "instead of", "unlike the previous"

**Step 3: Filter false positives**

Exclude from findings -- these are not developer comments and must remain untouched:
- Copyright and license headers (legal requirements, not code comments)
- `@generated` markers (tooling markers)
- `@deprecated` annotations (keep the tag, flag only temporal explanation text after it)
- Variable names or string literals that happen to contain temporal words
- TODO/FIXME items that describe future work without temporal references

When a finding appears, inspect nearby comments in the same function or block -- temporal language tends to cluster.

**Gate**: All files in scope scanned. Findings list populated with file path, line number, and matched text. Every finding listed, not just the first few. Proceed only when gate passes.

### Phase 2: ANALYZE

**Goal**: Understand context for each finding to produce meaningful rewrites.

**Step 1: Read surrounding code**

For each finding, read the function, block, or section the comment describes. Understand what the code actually does. A rewrite without code context produces vague replacements that strip temporal words without adding substance.

**Step 2: Classify the comment**

```markdown
| Finding | Type | Severity |
|---------|------|----------|
| "now uses JWT" | Temporal + Activity | High |
| "improved perf" | Activity | Medium |
| "Copyright 2024" | Legal (skip) | N/A |
```

**Step 3: Determine replacement content**

For each comment, identify:
1. What does the code do right now?
2. Why does it do it this way?
3. What value does the comment add for a future reader?

**Gate**: Every finding classified with context understood. Proceed only when gate passes.

### Phase 3: REWRITE

**Goal**: Generate specific, valuable replacement comments.

**Step 1: Draft rewrites**

For each finding, produce a structured entry with file path, line number, current text, suggested replacement, and reasoning:

```markdown
**File: `path/to/file.ext`**

Line X - [Comment type]:
  Current:   // Authentication now uses JWT tokens
  Suggested: // Authenticates requests using signed JWT tokens
  Reason:    "now uses" is temporal - describe current behavior only
```

**Step 2: Validate rewrite quality**

Each rewrite MUST pass these checks:
- [ ] Would this comment make sense in 10 years?
- [ ] Does it explain WHAT or WHY, not WHEN?
- [ ] Is it more specific than what it replaces (not just temporal word removed)?
- [ ] Does it add value for a future maintainer?

If a rewrite just removes the temporal word without adding substance, it fails validation. Simply deleting a word produces a useless comment -- `// Updated error handling` becoming `// Error handling` adds nothing. Rewrite with specific, descriptive content: `// Handles database connection errors with exponential backoff retry`.

**Gate**: All rewrites pass quality checks. No vague or empty replacements. Proceed only when gate passes.

### Phase 4: REPORT

**Goal**: Deliver structured, actionable report.

**Step 1: Generate report**

Report facts concisely with file paths and line numbers. Every finding must include the current text, suggested replacement, and reasoning -- a diagnostic-only count without rewrites creates work without providing solutions.

```markdown
## Comment Quality Review

### Summary
- Files scanned: N
- Issues found: M
- Most common pattern: [temporal word]

### Findings
[All findings with file, line, current text, suggested text, reason]

### Recommendations
1. Apply suggested changes
2. Consider adding linter rules for temporal language prevention
```

**Step 2: Apply fixes (if auto-fix enabled)**

If user requested auto-fix, apply all rewrites using Edit tool. Verify each edit succeeded. Wait for explicit user permission before auto-fixing without explicit user authorization.

**Step 3: Cleanup**

Remove any scan results, intermediate reports, or helper files created during execution.

**Gate**: Report delivered. All findings accounted for. Task complete.

## Error Handling

### Error: "No Temporal Language Found"
Cause: Files are clean or scope was too narrow
Solution:
1. Verify common files were scanned (README, main source files)
2. Report clean results -- this is a valid positive outcome
3. Suggest expanding scope if user suspects issues exist elsewhere

### Error: "Too Many Results to Display"
Cause: Large codebase with widespread temporal language
Solution:
1. Prioritize by file importance (README first, then core modules)
2. Group findings by pattern type
3. Process files by directory with grouped reports

### Error: "Comment Meaning Unclear Without History"
Cause: Comment only makes sense with development context that no longer exists
Solution:
1. Read surrounding code to infer current purpose
2. If purpose is clear from code, suggest removing the comment entirely
3. If purpose is unclear, ask user for clarification before rewriting

## References

### Reference Loading Table

Load on demand — only pull what the current task requires.

| Task Signal | Load |
|-------------|------|
| Go files (`.go`) in scope | `references/go-comment-patterns.md` |
| Error handling code (try/catch, `if err !=`, `raise`) | `references/error-handling-patterns.md` |
| Performance code (cache, pool, batch, concurrency, goroutine) | `references/performance-patterns.md` |
| General rewrite examples needed | `references/examples.md` |
| Full failure mode reference | `references/preferred-patterns.md` |
| Language-specific (Go, Python, JS/TS) or documentation (README, API) comments | `references/preferred-patterns-language-specific.md` |

### Reference Files
- `${CLAUDE_SKILL_DIR}/references/preferred-patterns.md`: Core temporal failure mode catalog (language-agnostic)
- `${CLAUDE_SKILL_DIR}/references/preferred-patterns-language-specific.md`: Language-specific and documentation-targeted failure modes
- `${CLAUDE_SKILL_DIR}/references/examples.md`: Before/after examples of comment rewrites
- `${CLAUDE_SKILL_DIR}/references/go-comment-patterns.md`: Go-specific temporal patterns with grep/rg detection commands
- `${CLAUDE_SKILL_DIR}/references/error-handling-patterns.md`: Temporal patterns in error handling code with detection commands
- `${CLAUDE_SKILL_DIR}/references/performance-patterns.md`: Temporal patterns in performance-related comments with detection commands
