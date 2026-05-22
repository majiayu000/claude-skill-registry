---
name: implement-feature
description: "End-to-end feature implementation from spec to tested code"
argument-hint: "[spec-file-or-description]"
allowed-tools: "Read, Edit, Write, Glob, Grep, Bash, Task"
---

# Feature Implementation Workflow

> PROSE constraints: **Orchestrated Composition** (chains phases into a complete
> workflow) + **Safety Boundaries** (validation gates between phases).

## Phase 1: Context Loading

1. If `$ARGUMENTS` points to a spec file, read it
2. Review existing codebase patterns in the affected area
3. Check relevant `.claude/rules/` for applicable standards
4. Identify affected components, routes, types, and tests

## Phase 2: Planning

Before writing any code, produce a brief implementation plan:

```markdown
## Implementation Plan

### Files to Create
- [path] — [purpose]

### Files to Modify
- [path] — [what changes]

### Approach
[Brief description of the implementation strategy]
```

## Validation Gate

**STOP**: Present the plan and wait for user confirmation before proceeding.

## Phase 3: Implementation

1. Create or modify files following the plan
2. Follow all applicable rules from `.claude/rules/`
3. Maintain type safety across boundaries (`shared/types/`)
4. Handle errors at system boundaries

## Phase 4: Testing

1. Write unit tests for new functions/components
2. Write integration tests for new API endpoints
3. Run the test suite: `npm test`
4. Run the linter: `npm run lint`
5. Run type checking: `npm run typecheck`

## Phase 5: Validation Checklist

- [ ] All planned files created/modified
- [ ] Types exported and consistent across frontend/backend
- [ ] Tests pass
- [ ] Linter passes
- [ ] No `any` types introduced
- [ ] Error handling at all system boundaries
- [ ] No hardcoded secrets or credentials
