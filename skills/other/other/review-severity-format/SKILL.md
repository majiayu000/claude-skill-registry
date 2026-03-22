---
name: review-severity-format
description: "Shared severity levels, issue ID format, and verdict criteria for all code reviewers. Use when performing code reviews or generating review reports. Do NOT use when writing or modifying code -- this is for review output formatting only."
durability: encoded-preference
---

# Review Severity Format

## Severity Levels

| Level | Meaning | Merge Impact |
|-------|---------|-------------|
| `must` | Blocks merge. Must be fixed before merging. | Blocks |
| `imo` | Recommended improvement. Author decides whether to fix. | Does not block |
| `nits` | Stylistic or trivial. Optional. | Does not block |

### Uncertainty Modifier

Append `?` to any level to signal reviewer uncertainty (e.g., `[imo?]`, `[must?]`). The `?` suffix does not affect verdict logic -- a `must?` still blocks merge.

### Subset Allowance

Reviewers MAY use a subset of levels when their domain warrants it (e.g., dead-code-reviewer uses `must` + `nits` only).

## Issue ID Format

Each issue uses the format `[PREFIX-NNN]` with a reviewer-specific prefix:

| Reviewer | Prefix |
|----------|--------|
| code-reviewer | CR |
| security-reviewer | SR |
| performance-reviewer | PR |
| sre-reviewer | SRE |
| database-reviewer | DR |
| dead-code-reviewer | DC |
| claude-config-reviewer | CFG |
| test-quality-reviewer | TQ |
| accessibility-reviewer | AR |

Sequential numbering starts from 001 per review session.

## Verdict Criteria

| Verdict | Condition |
|---------|-----------|
| APPROVE | No `must` issues |
| APPROVE WITH WARNINGS | `imo` issues only |
| REQUEST CHANGES | Any `must` issue found |

## Output Template

For each issue found, use checkbox format:

```
- [ ] [PREFIX-NNN] [level] Description - `file:line`
  Issue: Details
  Fix: Suggested remediation
```

### Review Summary

```markdown
## [Reviewer Name] Review Summary

**Files Reviewed:** X
**Issues Found:** Y

### By Severity
- must: X
- imo: Y
- nits: Z

### Issues

#### must
- [ ] [PREFIX-001] [must] Issue description - `file:line`

#### imo
- [ ] [PREFIX-002] [imo] Issue description - `file:line`

#### nits
- [ ] [PREFIX-003] [nits] Issue description - `file:line`

### Verdict
[APPROVE | APPROVE WITH WARNINGS | REQUEST CHANGES]
```
