---
name: code-review
description: Systematic code review with security, performance, and architecture analysis. Provides actionable fix suggestions and GitHub PR integration. Use when reviewing PRs, validating code changes, or checking code quality.
---

# Code Review

Structured review focusing on security, performance, architecture, and maintainability.

## When to Use

- PR review requests
- Pre-merge validation
- Security vulnerability detection
- Performance bottleneck identification

## MCP Workflow

```
# 1. Get PR context
gh pr view <PR> --json number,title,body,files

# 2. Check past decisions
claude-mem.search(query="<domain>", project="<project>")

# 3. Symbol overview of changed files
serena.get_symbols_overview(relative_path="changed/file")

# 4. Focus on changed functions
serena.find_symbol(name_path="ChangedClass/method", include_body=True)

# 5. Check impact scope
serena.find_referencing_symbols(name_path="ChangedClass/method")

# 6. Framework best practices
context7.get-library-docs("<framework>", topic="security")
```

## Review Checklist

### Security (Priority 1)
- [ ] SQL/NoSQL injection prevention
- [ ] Authentication/authorization checks
- [ ] Sensitive data not logged
- [ ] No hardcoded credentials

### Performance (Priority 2)
- [ ] No N+1 queries
- [ ] Pagination on list endpoints
- [ ] No blocking in async context

### Architecture (Priority 3)
- [ ] Layer boundaries respected
- [ ] No circular dependencies
- [ ] Proper abstraction levels

### Maintainability (Priority 4)
- [ ] Test coverage for changes
- [ ] Code duplication minimized
- [ ] Clear naming

## Output Format

```markdown
## Code Review: PR #[number]

| Item | Value |
|------|-------|
| Type | Feature / Bugfix / Refactor |
| Risk | Low / Medium / High |
| Files | N files (+X/-Y lines) |

### Summary
> [1-3 sentences]

### Positives
- [Well-implemented patterns]

### Critical Issues
1. **[Title]** - `file:line`
   - Problem: [description]
   - Impact: [security/performance/stability]
   - Fix: [suggestion]

### Major Issues
1. **[Title]** - `file:line` - Fix: [suggestion]

### Minor / Nitpicks
- [items]

### Verdict
- [ ] Approve (0 critical, <=2 major)
- [ ] Request Changes (1+ critical)
- [ ] Comment (need clarification)
```

## GitHub Commands

```bash
# Approve
gh pr review <PR> --approve --body "[review summary]"

# Request changes
gh pr review <PR> --request-changes --body "[issues]"

# Add inline comment
gh api repos/$REPO/pulls/<PR>/comments \
  -f body="Issue" -f path="file.ext" -f commit_id="$COMMIT" -F line=45
```

## Decision Criteria

| Condition | Action |
|-----------|--------|
| 0 Critical, 0-2 Major | Approve |
| 0 Critical, 3+ Major | Comment |
| 1+ Critical | Request Changes |
