---
name: requirement
scope: universal
description: |
  Guide requirement writing, user story creation, and feature specification.
  Use when: writing requirements, user stories, issues, feature planning.
  Keywords: requirement, user story, issue, feature, specification, 需求, 功能規劃, 規格.
---

# Requirement Assistant

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/requirement-assistant/SKILL.md)

**Version**: 1.1.0
**Last Updated**: 2026-01-28
**Applicability**: Claude Code Skills
**Core Standard**: [Requirement Engineering Standards](../../core/requirement-engineering.md)

---

## Purpose

This skill provides guidance on writing clear, complete, and actionable requirements.

## Quick Reference

### User Story Format (INVEST)

```
As a [role],
I want [feature],
So that [benefit].
```

### INVEST Criteria

| Criterion | Description | Question to Ask |
|-----------|-------------|-----------------|
| **I**ndependent | Can be delivered alone | Does this depend on other stories? |
| **N**egotiable | Details can be discussed | Is this too prescriptive? |
| **V**aluable | Provides user value | What problem does this solve? |
| **E**stimable | Can estimate effort | Do we understand the scope? |
| **S**mall | Fits in one sprint | Can we break this down? |
| **T**estable | Has clear acceptance criteria | How do we know it's done? |

### Requirement Priority Levels

| Priority | Label | Description |
|----------|-------|-------------|
| P0 | Must Have | Critical for release |
| P1 | Should Have | Important but not blocking |
| P2 | Could Have | Nice to have |
| P3 | Won't Have | Out of scope (this release) |

## Detailed Guidelines

For complete standards, see:
- [Requirement Writing Guide](./requirement-writing.md)
- [Requirement Checklist](./requirement-checklist.md)

## Quick Templates

### Simple Issue Template

```markdown
## Problem
[What problem are we solving?]

## Proposed Solution
[How should we solve it?]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
```

### Feature Request Template

```markdown
## Summary
[One-line description]

## Motivation
[Why is this needed? Who benefits?]

## Detailed Description
[Full description of the feature]

## Acceptance Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]

## Out of Scope
- [What this feature does NOT include]
```

### Bug Report Template

```markdown
## Description
[Brief description of the bug]

## Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [e.g., Windows 11]
- Version: [e.g., v1.2.3]
```

## Acceptance Criteria Guidelines

### Good Acceptance Criteria

- **Specific**: Clear, unambiguous
- **Measurable**: Can verify pass/fail
- **Achievable**: Technically feasible
- **Relevant**: Related to the requirement
- **Testable**: Can write a test for it

### Examples

**Good**:
```markdown
- [ ] User can upload files up to 10MB
- [ ] System responds within 500ms for 95th percentile
- [ ] Error message displays when upload fails
```

**Bad**:
```markdown
- [ ] System should be fast  # Not measurable
- [ ] Make it user-friendly  # Too vague
- [ ] Fix the bug            # No specific criteria
```

## Requirement Completeness Checklist

When writing requirements, ensure you cover:

- [ ] **What**: Clear description of the feature
- [ ] **Why**: Business value / problem solved
- [ ] **Who**: Target users / personas
- [ ] **When**: Priority / timeline
- [ ] **How**: High-level approach (if known)
- [ ] **Acceptance**: Criteria for completion
- [ ] **Scope**: What's NOT included

---

## Configuration Detection

This skill supports project-specific requirement templates.

### Detection Order

1. Check `CONTRIBUTING.md` for "Disabled Skills" section
   - If this skill is listed, it is disabled for this project
2. Check `CONTRIBUTING.md` for "Requirement Language" section
3. Check for `.github/ISSUE_TEMPLATE/` directory
4. Check for `docs/templates/` directory
5. If not found, **default to English** and use default templates

### First-Time Setup

If no templates found:

1. Ask the user: "This project doesn't have requirement templates. Which language should I use? (English / 中文)"
2. After user selection, suggest documenting in `CONTRIBUTING.md`:

```markdown
## Requirement Language

This project uses **[chosen option]** for requirements and issues.
<!-- Options: English | 中文 -->
```

3. Suggest appropriate template based on project type

### Configuration Example

In project's `CONTRIBUTING.md`:

```markdown
## Requirement Language

This project uses **English** for requirements and issues.
<!-- Options: English | 中文 -->

### Issue Templates Location
`.github/ISSUE_TEMPLATE/`
```

---

## Related Standards

**Core Standard (Theory & Deep Reference)**:
- [Requirement Engineering Standards](../../core/requirement-engineering.md) - Complete theoretical foundation including IEEE 830, SWEBOK v4.0, ISO 25010

**Related Standards**:
- [Spec-Driven Development](../../core/spec-driven-development.md) - Specification workflow
- [Behavior-Driven Development](../../core/behavior-driven-development.md) - Given-When-Then scenarios
- [Acceptance Test-Driven Development](../../core/acceptance-test-driven-development.md) - ATDD workshops
- [Checkin Standards](../../core/checkin-standards.md) - Code check-in requirements

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-01-28 | Added: Core Standard reference to requirement-engineering.md, expanded Related Standards section |
| 1.0.0 | 2025-12-24 | Added: Standard sections (Purpose, Related Standards, Version History, License) |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
