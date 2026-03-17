---
name: alto-feature-setup
description: Use when starting a new feature - running /alto-feature-setup, updating objective.md, or running alto-new-run. Interactive workflow for feature initialization.
---

# ALTO Feature Setup

Interactive skill for starting a new feature.

## Flow

### 1. Analyze Current State

First, invoke `alto-feature-finder` agent to understand:
- What features are completed
- What's currently in progress
- What should be next

```
Use the alto-feature-finder agent to analyze the project
```

### 2. Mark Previous Feature Complete (if needed)

If there's a completed feature that hasn't been marked done:

- Update `objective.md`:
  - Mark Definition of Done items as `[x]`
  - Add completion note: `**Completed:** run/NNN (YYYY-MM-DD)`

### 3. Discuss New Feature

Have a conversation with the user:
- What feature to work on next?
- Any clarifications on scope?
- Any constraints or preferences?

Then update `objective.md` with the feature definition:
- Goal statement
- Requirements (numbered: N.1, N.2, etc.)
- Definition of Done (checkboxes)

### 4. Run Mechanical Setup

Tell the user to run:

```bash
# Clean previous artifacts
alto-clean

# Create new run branch
alto-new-run
```

Or they can do it manually if they prefer different branch naming.

### 5. Handoff

Tell user:

> Feature setup complete. Run `claude` in a new terminal.
> Say "continue" to start the architecture phase.

---

## Devenv Scripts Reference

| Script | Purpose |
|--------|---------|
| `alto-setup` | First-time project initialization |
| `alto-feature` | Quick reminder of this flow |
| `alto-new-run` | Create run branch, reset state |
| `alto-clean` | Clean previous run artifacts |
| `alto-status` | Show current ALTO status |

## Notes

- This skill is INTERACTIVE - follow it WITH the user
- Use `alto-feature-finder` agent for codebase analysis
- Mechanical tasks are scripts, not manual commands
- After setup, user starts NEW session for autonomous work
