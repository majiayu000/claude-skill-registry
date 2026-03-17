---
name: plan-with-specs
description: Read finalized specs and generate a detailed implementation plan. Updates the plans markdown with actionable steps. Use when user has reviewed specs and wants to generate an implementation plan.
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: true
---

# Plan with Specs

## Skill Info

Part of the **spec-manager** agent. This skill generates detailed, actionable implementation plans from finalized specifications.

## Input

The user provides a task slug (or task title) as arguments: $ARGUMENTS

If no arguments are provided:
1. List all `*/specs.md` files in `specs/` directory
2. Ask the user which one to generate a plan for

If a task title (not slug) is provided, convert it to a slug to find the matching files.

## Process

### Step 1: Read All Spec Documents

1. Read `specs/{slug}/requirements.md` - for original context and goals
2. Read `specs/{slug}/specs.md` - for technical specifications
3. If either file doesn't exist or specs status is still "Pending", inform the user and suggest running the appropriate prior step

### Step 2: Validate Specs Readiness

Check that specs are sufficiently detailed for planning:
- Status is not "Pending"
- Technical specifications are defined
- Architecture section is filled in
- No critical open questions remain

If specs have unresolved open questions, warn the user and ask whether to proceed or resolve them first.

### Step 3: Analyze Codebase

Before generating the plan:
1. **Examine** the existing codebase structure (project layout, frameworks, patterns)
2. **Identify** existing files that need modification
3. **Find** reusable components, utilities, or patterns
4. **Check** test structure and conventions
5. **Review** configuration and build setup

### Step 4: Generate Implementation Plan

Update `specs/{slug}/plans.md` with the implementation plan:

```markdown
# Plans: {Original Task Title}

> Created: {original date}
> Updated: {YYYY-MM-DD}
> Status: Ready
> Requirements: [requirements.md](./requirements.md)
> Specs: [specs.md](./specs.md)

## Overview

{Brief summary of what will be implemented and the approach}

## Prerequisites

- {Any setup, dependencies, or preparatory work needed before starting}

## Implementation Steps

### Step 1: {Step Name}

- **Goal**: {What this step achieves}
- **Specs Reference**: TS-{X}
- **Files**:
  - `{path/to/file}` - {Create | Modify} - {What changes}
- **Details**:
  {Detailed implementation instructions}
- **Validation**:
  - {How to verify this step is complete}
- **Complexity**: Simple | Medium | Complex

### Step 2: {Step Name}

{Same structure}

{Continue for all steps...}

## Task Breakdown

Ordered checklist for tracking progress:

- [ ] **Step 1**: {Brief description}
- [ ] **Step 2**: {Brief description}
- [ ] ...
- [ ] **Final**: Verify all acceptance criteria

## File Change Summary

| File | Action | Step | Description |
|------|--------|------|-------------|
| `path/to/file` | Create/Modify/Delete | Step N | Brief description |

## Dependencies Between Steps

{Describe which steps depend on others and which can be parallelized}

```
Step 1 ─── Step 2 ─── Step 4
               │
           Step 3 ─── Step 5
```

## Testing Strategy

### Unit Tests
- {What to test and where}

### Integration Tests
- {What to test and where}

### Manual Verification
- {Steps to manually verify the feature works}

## Rollback Plan

{How to safely undo changes at each major checkpoint}

1. **After Step N**: {How to rollback}
2. **After Step M**: {How to rollback}

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk} | Low/Medium/High | Low/Medium/High | {How to mitigate} |

## Progress Tracking

| Step | Status | Started | Completed | Notes |
|------|--------|---------|-----------|-------|
| Step 1 | Pending | | | |
| Step 2 | Pending | | | |

## Acceptance Criteria Checklist

From requirements:
- [ ] {Criterion from FR-1}
- [ ] {Criterion from FR-2}
- [ ] ...
```

### Step 5: Report and Request Review

After generating the plan, display a summary:

```
Implementation plan generated for: "{Original Task Title}"

Updated: specs/{slug}/plans.md

Summary:
  - {N} implementation steps
  - {X} files to create, {Y} files to modify
  - Estimated complexity: {overall assessment}
  - {Z} risks identified

Please review the plan in specs/{slug}/plans.md

When ready to start implementation:
1. Follow the steps in order
2. Check off tasks as you complete them
3. Update the Progress Tracking table
```

## During Implementation

When the user is implementing and discusses progress or issues:

1. **Update Progress**: Mark steps as In Progress / Completed in the plans.md
2. **Update Specs**: If implementation reveals spec changes needed, update specs.md
3. **Track Deviations**: Log any deviations from the plan in the Notes column
4. **Adapt Plan**: If the plan needs adjustment based on discoveries during implementation, update the remaining steps

## Handling Changes

### If user requests requirement changes:

1. Update `specs/{slug}/requirements.md` with new/changed requirements
2. Re-read and update `specs/{slug}/specs.md` to reflect changes
3. Regenerate affected sections of `specs/{slug}/plans.md`
4. Clearly mark which steps changed and why
5. Preserve progress on already-completed steps

### If user requests spec changes:

1. Update `specs/{slug}/specs.md` with the changes
2. Regenerate affected sections of `specs/{slug}/plans.md`
3. Clearly mark which steps changed and why
4. Preserve progress on already-completed steps

### If implementation reveals issues:

1. Log the issue in the Progress Tracking table
2. Update affected specs in `specs/{slug}/specs.md` if needed
3. Adjust remaining plan steps
4. Add new risk entries if applicable

## Important

- Always read both requirements AND specs before generating plans
- Examine the actual codebase - plans must be grounded in the real project structure
- Steps should be ordered by dependency, not arbitrary sequence
- Each step must be independently verifiable
- Include rollback strategies for risky steps
- Keep the plan actionable - avoid vague instructions like "implement the feature"
- Reference specific file paths based on the actual project layout
- Plans should be detailed enough that another developer could follow them
