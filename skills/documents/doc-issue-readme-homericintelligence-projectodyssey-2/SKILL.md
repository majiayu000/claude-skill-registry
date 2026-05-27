---
name: doc-issue-readme
description: Post structured documentation to GitHub issue as a comment. Use when starting work on an issue to document approach and track progress.
category: doc
user-invocable: false
---

# Issue Documentation Skill

Post structured documentation to GitHub issues following ML Odyssey standards.

## When to Use

- Starting work on a GitHub issue
- Documenting implementation approach
- Tracking implementation progress
- Consolidating findings and decisions

## Quick Reference

```bash
# Post documentation to issue
gh issue comment <number> --body "$(cat <<'EOF'
## Issue Documentation

### Objective
[What this issue accomplishes]

### Approach
[Implementation approach]

### Files to Modify
- path/to/file1
- path/to/file2

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
EOF
)"
```

## Documentation Format

### Starting Work

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Implementation Started

**Branch**: `<branch-name>`

### Objective
[1-2 sentence description of what this issue accomplishes]

### Approach
[Brief description of implementation approach]

### Files to Create/Modify
- [ ] `path/to/file1.mojo` - [purpose]
- [ ] `path/to/file2.mojo` - [purpose]

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### References
- Related: #[other-issue]
- Design: [link to relevant docs]
EOF
)"
```

### Progress Update

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Progress Update

### Completed
- [x] Item 1
- [x] Item 2

### In Progress
- [ ] Item 3 (70%)

### Blockers
None / [describe blockers]

### Notes
[Any findings or decisions made]
EOF
)"
```

### Completion Summary

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Implementation Complete

**PR**: #<pr-number>

### Summary
[What was implemented]

### Files Changed
- `path/to/file1.mojo` - [change description]
- `path/to/file2.mojo` - [change description]

### Testing
- All tests pass
- Coverage: X%

### Verification
- [x] `pixi run test` passes
- [x] `just pre-commit-all` passes
EOF
)"
```

## Workflow

1. **Read issue context**: `gh issue view <number> --comments`
2. **Post documentation**: Use templates above to document approach
3. **Update as work progresses**: Post progress updates
4. **Summarize on completion**: Post completion summary with PR link

## Documentation Rules

### DO

- Keep issue-specific
- Reference related issues and docs
- Update as work progresses
- Be specific and measurable

### DON'T

- Post overly long updates (split if needed)
- Duplicate content across issues
- Leave work undocumented
- Forget completion summary

## Common Sections

### Objective

Good: "Implement tensor operations (add, multiply, matmul) with SIMD optimization"
Bad: "Work on tensors"

### Approach

Good: "Use SIMD for vectorized operations, implement lazy evaluation for chain operations"
Bad: "Code stuff"

### Success Criteria

Must be measurable checkboxes:

- "All 15 unit tests pass"
- "Coverage > 90%"
- "No new warnings"

## Error Handling

| Issue | Fix |
|-------|-----|
| Issue locked | Contact maintainer |
| Rate limited | Wait and retry |
| Content too long | Split into multiple comments |
| Missing context | Run `gh issue view <number> --comments` first |

## References

- See `.claude/shared/github-issue-workflow.md` for workflow patterns
- See `gh-read-issue-context` skill for reading issue context
- See `gh-post-issue-update` skill for posting updates
