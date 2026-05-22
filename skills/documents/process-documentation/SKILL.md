---
name: process-documentation
description: "Comprehensive documentation of all processes and changes. Templates for features, bug fixes, refactors with structured format and validation. Trigger: When completing features, fixing bugs, refactoring code, or before committing changes."
allowed-tools:
  - file-operations
  - read-file
  - write-file
---

# Process Documentation Skill

## [2026-02-04] New Skills Creation, Compliance, and Integration

- Created and integrated new skills: frontend-design, frontend-dev, backend-dev, humanizer, unit-testing, e2e-testing, next, nodejs, bun, express, nest, hono, jest, react-testing-library, react-native-testing-library, playwright, stagehand.
- All new skills follow the project compliance checklist: correct frontmatter, unique responsibility, token efficiency, decision tree, inline examples, and proper delegation to conventions/a11y/humanizer.
- No skill requires references/ (none exceeds 40 patterns or 4+ sub-topics).
- No overlap in responsibilities: each skill covers a unique domain.
- README updated and simplified in English, listing all new skills and summarizing the project objective and structure.
- All documentation and commit messages are now in English as per project policy.

## Overview

This skill ensures that all significant changes, features, bug fixes, and refactors are properly documented with context, rationale, and impact analysis.

## Objective

Enable comprehensive documentation of development processes to maintain clear project history, facilitate knowledge transfer, and support decision-making.

## Templates

### Feature Documentation

```markdown
# Feature: [Feature Name]

## Context

[Why this feature is needed]

## Implementation

[How it was implemented]

## Changes

- [File/component changed]
- [New dependencies added]
- [Configuration updates]

## Testing

[How to test this feature]

## Impact

[Performance, bundle size, breaking changes]
```

### Bug Fix Documentation

```markdown
# Bug Fix: [Issue Description]

## Problem

[What was broken]

## Root Cause

[Why it was happening]

## Solution

[How it was fixed]

## Prevention

[How to avoid this in the future]
```

### Refactor Documentation

```markdown
# Refactor: [Component/Module Name]

## Before

[Original implementation approach]

## After

[New implementation approach]

## Rationale

[Why the change was made]

## Breaking Changes

[If any]
```

## Conventions

### When to Document

- New features or capabilities
- Bug fixes (especially non-trivial ones)
- Refactors affecting multiple files
- Breaking changes
- Performance optimizations

### Documentation Location

- Feature docs: `/docs/features/`
- Bug fixes: Reference in commit messages or `/docs/fixes/`
- Refactors: `/docs/refactors/`
- ADRs: `/docs/adr/`

### Validation Checklist

- [ ] Clear context provided
- [ ] Implementation details explained
- [ ] Impact analyzed
- [ ] Testing approach defined
- [ ] Breaking changes identified
- [ ] Related files/components listed

## References

- [ADR GitHub Template](https://github.com/joelparkerhenderson/architecture-decision-record)
