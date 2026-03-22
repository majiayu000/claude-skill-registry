---
name: ai-sprint
description: "Use when planning a new sprint, running a retrospective, or tracking sprint-level goals against actual delivery."
effort: medium
argument-hint: "plan|retro|goals [--sprint <name>]"
---


# Sprint

## Purpose

Sprint lifecycle management: plan new sprints from backlog, run data-driven retrospectives comparing planned vs shipped, and track sprint-level goals. Bridges the gap between spec-level planning and day-to-day delivery.

## Trigger

- Command: `/ai-sprint plan|retro|goals`
- Context: sprint boundary (start or end of sprint), goal tracking mid-sprint.

## Pre-conditions (MANDATORY)

1. Read `.ai-engineering/manifest.yml` — `work_items` section.
2. Determine active provider (`github` or `azure_devops`).
3. Use provider-specific config:
   - **Azure DevOps**: filter by `area_path`, auto-detect current `iteration_path`
   - **GitHub**: filter by `team_label`, use milestones for sprint boundaries
4. Use all standard and custom fields the platform provides.

## Modes

### plan -- New sprint planning

1. **Review backlog** -- read open specs, GitHub Issues/Projects, and triaged items from `/ai-triage`.
2. **Assess capacity** -- count working days in sprint, factor in known absences or blockers from decision-store.
3. **Select items** -- pull highest-priority items that fit capacity. Apply RICE scores from triage.
4. **Estimate effort** -- use size labels (XS/S/M/L/XL) from issue standard. Flag items missing size estimates.
5. **Draft sprint board** -- output planned items grouped by priority:

```markdown
## Sprint: {name} ({start} - {end})

### Goals
1. {Goal 1 -- measurable outcome}
2. {Goal 2 -- measurable outcome}

### Planned Items
| # | Priority | Size | Item | Spec |
|---|----------|------|------|------|
| 1 | p1 | M | Fix hook installation on Windows | spec-054 |
| 2 | p2 | L | Add telemetry dashboard | spec-054 |
```

6. **Store** -- save sprint plan to `.ai-engineering/sprints/{name}.md`.

### retro -- Sprint retrospective

1. **Load sprint plan** -- read `.ai-engineering/sprints/{name}.md`.
2. **Collect actuals** -- scan merged PRs, completed spec tasks, and commit history for the sprint period.
3. **Compare planned vs shipped**:
   - Items completed as planned
   - Items carried over (not finished)
   - Side quests (unplanned work that entered the sprint)
   - Items descoped or deprioritized
4. **Analyze patterns**:
   - Estimation accuracy: actual effort vs estimated size
   - Side quest ratio: unplanned / total items delivered
   - Velocity trend: items completed vs previous sprints
5. **Document learnings** -- what went well, what to change, action items.
6. **Output** -- retrospective report appended to `.ai-engineering/sprints/{name}.md`.

### goals -- Sprint goal tracking

1. **Load active sprint** -- find current sprint from `.ai-engineering/sprints/`.
2. **Check goal progress** -- for each goal, assess completion signals (merged PRs, closed issues, spec task status).
3. **Report** -- traffic-light status per goal: green (on track), yellow (at risk), red (blocked/behind).

## Arguments

| Argument | Description |
|----------|-------------|
| `plan` | Start planning a new sprint |
| `retro` | Run retrospective on completed sprint |
| `goals` | Check progress on current sprint goals |
| `--sprint <name>` | Sprint identifier (e.g., `2026-w12`). Defaults to current week. |

## Quick Reference

```
/ai-sprint plan --sprint 2026-w12     # plan sprint for week 12
/ai-sprint retro --sprint 2026-w11    # retro on last sprint
/ai-sprint goals                      # check current sprint goals
```

## Storage

- Sprint files: `.ai-engineering/sprints/{name}.md`
- Naming convention: `YYYY-wNN` (ISO week) or custom names

$ARGUMENTS
