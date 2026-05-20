---
name: gsd-preflight
description: Use when GSD commands are failing or .planning/ artifacts look inconsistent. Run before any GSD execute-phase or verify-work attempt to catch cross-artifact mismatches early.
description-frequency: on-demand
---

# GSD Preflight Validator

Pre-flight checks on `.planning/` artifacts to catch issues before workflows fail.

## Core Artifact Checks

**PROJECT.md** — Sections: What This Is, Requirements, Constraints, Key Decisions
**ROADMAP.md** — Sequential phase numbers, each with Goal/Deliverables/Success Criteria
**STATE.md** — Current Position matches ROADMAP status, reasonable progress %
**config.json** — Valid JSON, valid enum values (mode, model_profile, depth)

## Cross-Artifact Consistency

- STATE.md phase exists in ROADMAP.md
- Completed phases have matching SUMMARY files for each PLAN
- Phase directories exist for all ROADMAP phases
- No orphaned files (PLAN without phase, SUMMARY without PLAN)

## Severity

| Level | Definition | Action |
|-------|------------|--------|
| BLOCKER | Will cause workflow failure | Must fix first |
| WARNING | May cause confusion | Should fix |
| INFO | Informational | No action needed |

## Common Fixes

- **STATE/ROADMAP out of sync:** Run /gsd:progress
- **Missing SUMMARY for completed plan:** Re-execute or mark incomplete
- **Invalid config.json:** Check for trailing commas, invalid values
- **Orphaned directories:** Add to ROADMAP or remove
