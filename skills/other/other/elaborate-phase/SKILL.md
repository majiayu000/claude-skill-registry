---
name: elaborate-phase
description: Elaborate a migration plan phase into a complete self-contained implementation plan. Use when user says "elaborate phase", "elaborate phase N", or "phase elaboration". Assesses codebase, writes detailed phase plan, then validates with dry walkthrough.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '📝 [SKILL: elaborate-phase] Elaborating migration phase into self-contained plan...'"
          once: true
---

# Phase Elaboration Skill

Elaborate a single phase from a high-level migration plan into a complete, self-contained implementation plan. The plan should contain all background context needed for implementation.

## When to Use

- User says "elaborate phase", "elaborate phase 0", "elaborate phase 1", etc.
- User wants to create a detailed implementation plan for a specific migration phase
- User says "phase elaboration" or "detail phase N"
- After implementing a phase, when ready to elaborate the next one

## Critical Constraints

**NEVER:**
- Modify any source code files
- Implement any part of the plan
- Add backward compatibility to the plan (unless a cleanup phase explicitly removes it)
- Add fallback mechanisms that hide bugs
- Add deprecation notes, stubs, warnings
- Include rollback mechanisms
- Add stakeholder sections or PR breakdowns
- Elaborate multiple phases at once - one phase per invocation
- Make assumptions about codebase state without verifying
- Read previous `Phase#.md` files unless you have a specific question that requires looking up a detail

**ALWAYS:**
- Assess current codebase state with subagents FIRST
- Write output to the plan directory (e.g., `{plan_dir}/Phase#.md`)
- Run `/autoskillit:dry-walkthrough` on the written `Phase#.md` to validate
- Make the plan self-contained with all background context needed
- Include verification commands and success criteria
- Report findings to terminal output
- Update the master plan if dry walkthrough reveals issues affecting subsequent phases

## Plan Directory Structure

All plans live in a dedicated directory:
```
{plan_directory}/
├── {master_plan_name}.md    # Unique name (e.g., feature_migration_plan.md)
├── Phase0.md                # Elaborated phase 0 (if exists)
├── Phase1.md                # Elaborated phase 1 (if exists)
├── Phase2.md                # etc.
└── ...
```

- **Master plan**: Has a unique descriptive name, contains the high-level multi-phase plan
- **Phase plans**: All named `Phase#.md`, contain detailed implementation instructions

## Understanding Phase Types

### First Phase (Phase 0 or Phase 1)

When elaborating the first phase:
- No previous phase `.md` files exist in the directory
- No previous phases have been implemented
- Assess the current (original) state of the codebase
- The master plan describes the starting state

User message example:
```
Here's the plan directory: {plan_dir}/ with master plan {master_plan}.md. Elaborate phase 0.
```

### Subsequent Phases (Phase 1, 2, 3, ...)

When elaborating subsequent phases:
- Previous phases have been implemented
- The codebase has changed since the master plan was written
- Must assess the CURRENT state (post-implementation)
- Do NOT read previous `Phase#.md` files - assess from codebase directly

User message example:
```
Same directory. Phase 0 is implemented. Elaborate phase 1.
```

## Workflow

### Step 1: Parse User Request

Extract from user message:
1. **Phase number** to elaborate (0, 1, 2, etc.)
2. **Plan directory** containing the master plan and phase plans
3. **Master plan filename** (the unique-named high-level plan)
4. **Is this the first phase?** (no existing `Phase#.md` files)

### Step 2: Read the Master Plan

Load and understand:
- **Master plan**: The complete high-level migration plan
- Identify the specific phase to elaborate
- Understand dependencies on previous phases
- Note files and systems affected

**IMPORTANT:** Do NOT read previous `Phase#.md` files. They exist in the directory but reading them wastes context. Only look up a specific detail from a previous phase if you encounter a concrete question during assessment that cannot be answered from the codebase itself.

### Step 3: Assess Current Codebase State

Launch **parallel Explore subagents** to understand the current state:

```
Subagent 1: Affected Files Assessment
  - Read all files that will be touched by this phase
  - Document their current state (structure, dependencies, imports)
  - Identify any deviations from what the master plan expected

Subagent 2: Dependency Analysis
  - Trace imports and dependencies for affected files
  - Identify all consumers of code being moved/changed
  - Map the dependency graph

Subagent 3: Test Coverage
  - Find tests related to affected code
  - Understand what test changes will be needed
  - Identify any integration tests that may break

Subagent 4: Pattern Discovery
  - Search for similar patterns in the codebase
  - Identify conventions that should be followed
  - Note any existing utilities that should be reused

Subagent 5: State Verification (for subsequent phases)
  - Verify previous phases were implemented correctly
  - Check that expected files/directories exist
  - Confirm imports were updated as planned
```

Output assessment summary to terminal:
```
## Codebase Assessment Complete

### Current State
- {component}: {current status}
- {file}: {current location and state}

### Key Findings
- {finding that affects the plan}
- {deviation from master plan expectations}

### Dependencies Mapped
- {affected file} imports: {list of imports}
- {affected file} imported by: {list of consumers}
```

### Step 4: Write Elaborated Phase Plan

Create a **complete implementation plan** at the output location. The plan should include all necessary background context.

**Plan Structure:**
```markdown
# Phase {N}: {Phase Name}

## Executive Summary

{2-3 sentences describing what this phase accomplishes and why}

{Any critical changes from the original master plan, with rationale}

---

## Prerequisites

Before starting Phase {N}:

- [ ] {Prerequisite check}
- [ ] {Required state verification}
- [ ] Previous phases implemented
- [ ] All tests pass: run the project's test suite
- [ ] No uncommitted changes: `git status`

---

## Background Context

{Everything the implementer needs to know that isn't in other sections}

### Relevant Code Locations

| Component | Current Location | Purpose |
|-----------|------------------|---------|
| {component} | {path} | {brief description} |

### Key Dependencies

{Description of important dependencies and why they matter}

---

## Phase {N} Tasks

### Task {N}.1: {Task Name}

{Description of what this task accomplishes}

**Files to Modify:**
- `{path}`: {what changes}

**Implementation Steps:**
1. {Specific action with details}
2. {Specific action with details}

**Verification:**
```bash
{command to verify task completion}
```

### Task {N}.2: {Task Name}

{Same structure as above}

---

## Verification Checklist

After completing Phase {N}, verify:

- [ ] {Verification item}
- [ ] Run linting and formatting checks
- [ ] All tests pass: run the project's test suite

---

## Files Created/Modified in Phase {N}

| Path | Type | Purpose |
|------|------|---------|
| {path} | {Created/Modified/Moved/Deleted} | {purpose} |

---

## What Phase {N} Does NOT Do

Phase {N} explicitly avoids:

1. {Thing that might be expected but isn't done here}
2. {Clarification of scope boundaries}

---

## Implementation Guidelines

{Project-specific guidelines relevant to this phase}

1. **No useless comments** - Do not use the codebase as a notepad
2. **No backward compatibility code** - unless cleanup is explicitly planned
3. **Clean cuts only** - Move code completely, update all imports atomically

---

## Next Phase Preview

**Phase {N+1}: {Name}**

{Brief description of what comes next, so implementer understands boundaries}
```

### Step 5: Dry Walkthrough

Invoke `/autoskillit:dry-walkthrough` on the `Phase{N}.md` file just written.

### Step 6: Update Master Plan (If Required)

If the dry walkthrough reveals issues that affect subsequent phases:
1. Update the master plan to reflect corrections
2. Report changes to terminal

### Step 7: Report to Terminal

After writing the plan, output summary:
```
## Phase Elaboration Complete

**Phase:** {N} - {Phase Name}
**Plan Directory:** {plan_directory}
**Output:** Phase{N}.md
**Status:** {READY / REVISED from master plan}

### Changes from Master Plan
{List any modifications made during elaboration}
- {change}: {reason}

### Master Plan Updates
{If master plan was updated due to downstream impact}
- {subsequent phase}: {what was changed}
OR
- No updates required

### Key Implementation Notes
- {Important note for implementer}
- {Gotcha to watch out for}

Ready for implementation.
```

## Output Location

Phase plans are written to the same directory as the master plan:
```
{plan_directory}/Phase{N}.md
```

Where `{N}` is replaced with the phase number (0, 1, 2, etc.).

Example directory after elaborating phases 0 and 1:
```
/path/to/plans/
├── feature_migration_plan.md   # Master plan
├── Phase0.md                     # Elaborated phase 0
└── Phase1.md                     # Elaborated phase 1
```

## Backward Compatibility Policy

**Backward compatibility code is only acceptable when:**
1. There is an explicit cleanup phase in the migration plan
2. The cleanup phase explicitly lists removal of the compatibility code
3. The compatibility code is clearly marked for removal

**If not planned for cleanup, do NOT add:**
- Import shims or re-exports for old paths
- Deprecation warnings
- Compatibility adapters
- Fallback mechanisms

## Example Usage

### First Phase Example

**User:** "Here's the plan directory: /path/to/plans/ with master plan feature_migration_plan.md. Elaborate phase 0."

**Process:**
1. Read master plan from `/path/to/plans/feature_migration_plan.md`
2. No existing `Phase#.md` files (first phase)
3. Launch subagents to assess current codebase state
4. Write elaborated plan to `/path/to/plans/Phase0.md`
5. Run `/autoskillit:dry-walkthrough` on `Phase0.md`
6. Update master plan if dry walkthrough reveals downstream issues
7. Report findings and status

### Subsequent Phase Example

**User:** "Same directory. Phase 0 is implemented. Elaborate phase 1."

**Process:**
1. Read master plan from `/path/to/plans/feature_migration_plan.md`
2. Launch subagents to assess:
   - Current state (post Phase 0 implementation)
   - Files touched by Phase 1
   - Dependencies and consumers
3. Write elaborated plan to `/path/to/plans/Phase1.md`
4. Run `/autoskillit:dry-walkthrough` on `Phase1.md`
5. Update master plan if dry walkthrough reveals downstream issues
6. Report findings and status

## Related Skills

- **`/autoskillit:dry-walkthrough`** - Used internally for validation
- **`/autoskillit:make-plan`** - Creates new plans (this skill elaborates existing ones)
- **`/autoskillit:implement-worktree`** - Implements elaborated plans
