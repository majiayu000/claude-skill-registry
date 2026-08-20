---
name: ghm-status-sync
description: >
  Synchronizes README.md Command Center with current project state.
  Triggers on gate changes, EPIC status changes, or explicit `/ghm-status-sync` invocation.
  Outputs updated README.md dashboard with current lifecycle stage, blockers, and metrics.
context: inline
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Status Sync

Synchronize the README.md Command Center with the current project state after gate advancement or EPIC status changes.

## Workflow Overview

1. **Load Context** → Read README.md, PRD.md metadata, Active EPIC Session State section
2. **Extract State** → Pull lifecycle stage, blockers, metrics
3. **Update Dashboard** → Sync README sections with current truth

## Core Output Template

| Element | Definition | Evidence |
|---------|------------|----------|
| **Lifecycle Stage** | Current PRD version from PRD.md | `Current Lifecycle Gate: v0.X` |
| **Gate Status** | Visual progress indicators | 🟢 Complete / 🟡 In Progress / ⚪ Pending |
| **Active EPIC** | Current work from EPIC header | `EPIC-XX: Title` |
| **Blockers** | Open blockers from EPIC Session State section | List with severity |

## Step 1: Load Context

Read these files in order:
1. `README.md` (current state)
2. `PRD.md` (metadata block for lifecycle stage)
3. Active EPIC Session State section (blockers, progress)

### Checklist
- [ ] README.md loaded
- [ ] PRD.md metadata extracted
- [ ] Active EPIC identified and Session State section read

## Step 2: Extract Current State

Pull authoritative values:

| Field | Source |
|-------|--------|
| Lifecycle Stage | PRD.md `Current Lifecycle Gate` |
| Gate Progress | PRD.md gate table |
| Active EPIC | README.md `Active Work` section |
| Blockers | EPIC Session State section |
| Metrics | README.md Truth Table |

## Step 3: Update README Dashboard

Apply synchronization rules:

1. **Lifecycle Stage**: Update header to match PRD.md
2. **Gate Table**:
   - 🟢 = Passed gates (all criteria met)
   - 🟡 = Current gate (in progress)
   - ⚪ = Future gates (not started)
3. **Active EPIC**: Update metadata in Active Work section
4. **Blockers**: Sync from EPIC Session State section
5. **Squad Status** (Section: `squad-status`): Update agent and EPIC tables:
   - For each agent in `.claude/agents/`: check MEMORY.md mtime for "Last Active", grep EPICs for agent name for "Current EPIC"
   - For each EPIC in `epics/`: read State field, Epic Lead, and Change Log last date
   - Status values: `active` (session <2h old), `idle` (no recent activity), `blocked` (blocker in session state)

## Quality Gates

### Pass Checklist
- [ ] README lifecycle stage matches PRD.md
- [ ] Gate indicators are accurate (no 🟢 on incomplete gates)
- [ ] Active EPIC reference is current
- [ ] Blockers reflect actual state

### Testability Check
- [ ] Can be validated by comparing README to PRD.md
- [ ] Gate status is traceable to gate criteria

## Anti-Patterns

| Pattern | Example | Fix |
|---------|---------|-----|
| Stale gate status | 🟢 on gate with missing criteria | → Verify all criteria before marking complete |
| Missing blockers | EPIC has blockers, README shows none | → Always sync from EPIC Session State section |
| Wrong EPIC reference | README points to closed EPIC | → Check EPIC status before updating |

## Boundaries

**DO**:
- Status synchronization
- Link updates
- Gate progression indicators

**DON'T**:
- Content changes to descriptions
- Create new sections
- Modify PRD.md (read-only source)

## Handoff

After status sync completes:
- README.md is current and accurate
- Ready for next work session
- Gate-check skill can validate if advancing
