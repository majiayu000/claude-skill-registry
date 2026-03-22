---
name: code-review
description: Structured code review with security, performance, and architecture checklists. Use when reviewing pull requests, code changes, or conducting architecture reviews. Provides actionable checklists for consistent review quality.
user-invocable: true
---

# Code Review

Systematic code review skill with layered checklists. Produces consistent, actionable feedback across all review types.

## When to Use

- Reviewing pull requests or merge requests
- Conducting architecture reviews
- Auditing code for security, performance, or quality
- Pre-merge quality gates

## When NOT to Use

- Writing new code (use `/feature-dev` or `/bugfix` instead)
- Validating AI asset files (use `asset-validation` skill)
- Running automated checks before commit (use `/pre-commit`)

## Review Process

### 1. Understand the Change

Before reviewing code, answer:
- **What** is being changed? (feature, bugfix, refactor, dependency update)
- **Why** is it being changed? (linked issue, PRD, bug report)
- **Scope**: How many files, which modules, what's the blast radius?

### 2. Apply Checklists

Use the appropriate checklist(s) based on change type:

| Change Type | Checklists to Apply |
|---|---|
| New feature | `review-checklist.md` + `security-checklist.md` |
| Bug fix | `review-checklist.md` (focus: root cause, regression test) |
| Refactor | `review-checklist.md` (focus: behavior preservation, tests) |
| API change | `review-checklist.md` + `security-checklist.md` |
| Infrastructure | `security-checklist.md` |
| Dependencies | `security-checklist.md` (focus: supply chain) |

### 3. Provide Feedback

Structure review comments as:

```
## Review Summary

**Verdict**: APPROVE | REQUEST_CHANGES | COMMENT

### Critical (must fix before merge)
- [ ] [file:line] Description — why it matters

### Suggestions (should fix, not blocking)
- [ ] [file:line] Description — improvement rationale

### Nits (optional, style/preferences)
- [ ] [file:line] Description
```

**Rules:**
- Every critical finding must explain **why** it's a problem and **how** to fix it
- Link to relevant documentation or standards when applicable
- Acknowledge good patterns — reinforce what works well
- Never approve code with known critical issues
- Flag missing tests for new logic paths

## Integration

- **Follows rules**: `Agent(software-engineer)` (architecture, code quality)
- **Used by workflows**: `/code-review`, `/create-pr`
- **Companion checklists**: `review-checklist.md`, `security-checklist.md`
