---
name: plan-management
description: Apply project planning conventions when creating or organizing plans. Use when user asks to create a plan, add a feature plan, document a bug, or work with the plans/ directory.
---

# Plan Management Conventions

This project uses a structured planning system. Apply these conventions when working with plans.

## Directory Structure

| Folder | Purpose |
|--------|---------|
| `plans/model/` | Wave physics, simulation, timing |
| `plans/visuals/` | Rendering, gradients, effects |
| `plans/gameplay/` | Surfer, controls, multiplayer |
| `plans/tooling/` | Debug panel, dev tools |
| `plans/testing/` | Test strategy |
| `plans/bugfixes/` | Bug investigation and fixes |
| `plans/world/` | Environmental systems |
| `plans/reference/` | Research docs (never archive) |
| `plans/archive/` | Superseded plans |

## Numbering Convention

- Use increments of 10 (10, 20, 30...) to allow inserting related plans
- Check existing files in target folder to find next available number
- Preserve numbers when moving plans between folders

## Plan Template

```markdown
# Plan [NUMBER]: [Title]

**Status**: Proposed | In Progress | Blocked | Complete
**Category**: model | visuals | gameplay | tooling | testing | bugfixes
**Depends On**: [other plan numbers, if any]

## Problem

Clear statement of what needs to be solved.

## Proposed Solution

Technical approach and key design decisions.

## Implementation Steps

1. First step with clear acceptance criteria
2. Second step...

## Files Affected

- `src/file.js` - What changes needed

## Testing

How to verify the implementation works correctly.
```

## Updating Plans After Implementation

When completing implementation steps from a plan:

1. **Update status** - Change `**Status**: Proposed` to `**Status**: Complete` (or `In Progress` if partially done)
2. **Add completion summary** - Add a `## Completion Summary` section at the end documenting:
   - What was implemented
   - Any deviations from the original plan
   - Files that were actually modified
3. **Do this proactively** - Update the plan immediately after finishing, without waiting for user to ask

## When to Apply

Automatically apply when:
- User says "create a plan", "add a feature", "document this"
- Working with files in `plans/` directory
- User references plan numbers or categories
- Completing implementation of a plan (update status and add summary)
