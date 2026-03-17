---
name: spec
description: "Generate an implementation-ready specification from a feature idea"
argument-hint: "[feature-name-or-description]"
allowed-tools: "Read, Glob, Grep, Write, Task"
---

# Specification Generator

> PROSE constraint: **Orchestrated Composition** — transforms a high-level idea
> into an implementation-ready blueprint that bridges planning and coding.

## Purpose

Create a `.spec.md` file that serves as a deterministic contract between the
planning phase and the implementation phase. Specs ensure consistent outcomes
regardless of who (or what) implements them.

## Process

1. Parse `$ARGUMENTS` for the feature name and description
2. Research the existing codebase for related patterns and conventions
3. Identify affected layers (frontend, backend, shared types, tests)
4. Generate the spec using the template below
5. Write the spec to `docs/specs/<feature-name>.spec.md`

## Spec Template

```markdown
# Feature: [Name]

## Problem Statement
[Why this feature is needed — the user or business problem it solves]

## Approach
[High-level strategy for implementing this feature]

## Implementation Requirements

### Core Components
- [ ] [File path] — [What this file does]
- [ ] [File path] — [What this file does]

### API Contracts (if applicable)
- `METHOD /path` — [Description] → [Response shape]

### Data Model Changes (if applicable)
- [Table/collection] — [Fields added/modified]

### UI Components (if applicable)
- [Component] — [Purpose and behavior]

## Acceptance Criteria
- [ ] [Testable criterion]
- [ ] [Testable criterion]
- [ ] [Testable criterion]

## Validation Criteria
- [ ] Unit tests >90% coverage for new code
- [ ] Integration tests for all new endpoints
- [ ] No `any` types introduced
- [ ] All inputs validated at system boundaries
- [ ] Error states handled and tested

## Dependencies
- [External package or service, if any]

## Risks
- [Risk] → [Mitigation]

## Handoff Checklist
- [ ] Spec reviewed and approved
- [ ] Architecture aligns with existing patterns
- [ ] No breaking changes to existing APIs (or migration plan included)
- [ ] Ready for implementation via `/implement-feature docs/specs/<name>.spec.md`
```

## Output

Write the completed spec to `docs/specs/` and inform the user they can
implement it by running `/implement-feature docs/specs/<feature-name>.spec.md`.
