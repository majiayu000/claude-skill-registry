---
name: ln-510-test-planner
description: Orchestrates test planning pipeline (research → manual → auto tests). Coordinates ln-511, ln-512, ln-513. Invoked by ln-500-story-quality-gate.
---

# Test Planning Orchestrator

Coordinates the complete test planning pipeline for a Story by delegating to specialized workers.

## Purpose & Scope
- **Orchestrate** test planning: research → manual testing → automated test planning
- **Delegate** to workers: ln-511-test-researcher, ln-512-manual-tester, ln-513-auto-test-planner
- **No direct work** — only coordination and delegation via Skill tool
- **Called by** ln-500-story-quality-gate after regression tests pass

## When to Use

This skill should be used when:
- **Invoked by ln-500-story-quality-gate** Pass 1 after regression tests pass
- All implementation tasks in Story are Done
- Need complete test planning (research + manual + auto)

**Prerequisites:**
- All implementation Tasks in Story status = Done
- Regression tests passed (ln-502)
- Code quality checked (ln-501)

## Pipeline Overview

```
ln-510-test-planner (Orchestrator)
    │
    ├─→ ln-511-test-researcher
    │     └─→ Posts "## Test Research: {Feature}" comment
    │
    ├─→ ln-512-manual-tester
    │     └─→ Creates tests/manual/ scripts + "## Manual Testing Results" comment
    │
    └─→ ln-513-auto-test-planner
          └─→ Creates test task in Linear via ln-301/ln-302
```

## Workflow

### Phase 1: Discovery

1) Auto-discover Team ID from `docs/tasks/kanban_board.md`
2) Validate Story ID provided by ln-500

**Input:** Story ID from ln-500-story-quality-gate

### Phase 2: Research Delegation

1) **Check if research exists:**
   - Search Linear comments for "## Test Research:" header
   - If found → skip to Phase 3

2) **If no research:**
   - **Use Skill tool to invoke `ln-511-test-researcher`**
   - Pass: Story ID
   - Wait for completion
   - Verify research comment created

### Phase 3: Manual Testing Delegation

1) **Check if manual testing done:**
   - Search Linear comments for "## Manual Testing Results" header
   - If found with all AC passed → skip to Phase 4

2) **If manual testing needed:**
   - **Use Skill tool to invoke `ln-512-manual-tester`**
   - Pass: Story ID
   - Wait for completion
   - Verify results comment created

3) **If any AC failed:**
   - Stop pipeline
   - Report to ln-500: "Manual testing failed, Story needs fixes"

### Phase 4: Auto Test Planning Delegation

1) **Invoke auto test planner:**
   - **Use Skill tool to invoke `ln-513-auto-test-planner`**
   - Pass: Story ID
   - Wait for completion

2) **Verify results:**
   - Test task created in Linear (or updated if existed)
   - Return task URL to ln-500

### Phase 5: Report to Caller

1) Return summary to ln-500:
   - Research: completed / skipped (existed)
   - Manual testing: passed / failed
   - Test task: created / updated + URL

## Worker Invocation (MANDATORY)

> **CRITICAL:** All delegations MUST use Skill tool. DO NOT execute research, manual tests, or test planning directly.

| Phase | Worker | Invocation |
|-------|--------|------------|
| 2 | ln-511-test-researcher | `Skill(skill: "ln-511-test-researcher")` |
| 3 | ln-512-manual-tester | `Skill(skill: "ln-512-manual-tester")` |
| 4 | ln-513-auto-test-planner | `Skill(skill: "ln-513-auto-test-planner")` |

**FORBIDDEN:**
- Running web searches directly (delegate to ln-511)
- Creating bash test scripts directly (delegate to ln-512)
- Creating test tasks directly (delegate to ln-513)
- Skipping any phase without justification

## Critical Rules

- **No direct work:** Orchestrator only delegates, never executes tasks itself
- **Sequential execution:** 511 → 512 → 513 (each depends on previous)
- **Fail-fast:** If manual testing fails, stop pipeline and report
- **Skip detection:** Check for existing comments before invoking workers
- **Single responsibility:** Each worker does one thing well

## Definition of Done

- [ ] Story ID validated
- [ ] Research phase: ln-511 invoked OR existing comment found
- [ ] Manual testing phase: ln-512 invoked OR existing results found
- [ ] Auto test planning phase: ln-513 invoked
- [ ] Test task created/updated in Linear
- [ ] Summary returned to ln-500-story-quality-gate

**Output:** Summary with phase results + test task URL

## Reference Files

- Workers: `../ln-511-test-researcher/SKILL.md`, `../ln-512-manual-tester/SKILL.md`, `../ln-513-auto-test-planner/SKILL.md`
- Caller: `../ln-500-story-quality-gate/SKILL.md`
- Risk-based testing: `../ln-513-auto-test-planner/references/risk_based_testing_guide.md`

---

**Version:** 4.0.0 (Refactored to Orchestrator pattern - delegates to ln-511/512/513 workers)
**Last Updated:** 2026-01-15
