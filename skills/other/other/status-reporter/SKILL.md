---
name: status-reporter
description: CORE SKILL - Must be called by ALL other skills to update project status. Maintains global project state, feature progress, and action log. Triggers on "Show status", "Project status", "What's the status".
globs: ["docs/features/**", "docs/status-log.md", "docs/project-status.md"]
---

# Status Reporter (CORE SYSTEM SKILL)

**THIS SKILL MUST BE INTEGRATED INTO ALL OTHER SKILLS.**

Every skill that modifies project state must call status-reporter functions to maintain consistent project status.

## Purpose

1. **Track global project status** in `docs/project-status.md`
2. **Track feature status** in `docs/features/_index.md`
3. **Track individual feature status** in `docs/features/FEAT-XXX/status.md`
4. **Maintain action log** in `docs/status-log.md`

## Files Managed

```
docs/
├── project-status.md      <- Global project dashboard
├── status-log.md          <- Chronological action log
└── features/
    ├── _index.md          <- All features dashboard
    └── FEAT-XXX/
        └── status.md      <- Individual feature status
```

## Integration Points

**EVERY skill must update status at these points:**

| Skill | When to Update | What to Update |
|-------|----------------|----------------|
| `project-interview` | After completing | project-status.md (Phase 0 progress) |
| `architecture-designer` | After each ADR | project-status.md (Phase 0 progress) |
| `mvp-planner` | After creating features | project-status.md, _index.md |
| `spec-architect` | After feature interview | FEAT-XXX/status.md, _index.md |
| `implementation-planner` | After generating plan | FEAT-XXX/status.md, _index.md |
| `implementer` | After EACH task | FEAT-XXX/status.md, _index.md, tasks.md |
| `fork-feature` | After creating fork | FEAT-XXX/status.md |
| `git-automator` | After PR/merge | FEAT-XXX/status.md, _index.md |

## Update Functions

**Skills should conceptually call these functions:**

### `update_task_complete(feature_id, task_description)`
1. Mark task as complete in tasks.md
2. Update progress table in tasks.md
3. Update FEAT-XXX/status.md progress
4. Update _index.md progress column
5. Update project-status.md active work
6. Append to status-log.md

### `update_phase_complete(feature_id, phase_name)`
1. Update FEAT-XXX/status.md phase table
2. Update _index.md phase column
3. Update project-status.md if all features in new phase
4. Append to status-log.md

### `update_blocker(feature_id, blocker_description)`
1. Update FEAT-XXX/status.md blockers
2. Update _index.md status to Blocked
3. Update project-status.md blockers section
4. Append to status-log.md

### `update_feature_complete(feature_id)`
1. Update FEAT-XXX/status.md to complete
2. Update _index.md status to Complete
3. Update project-status.md MVP progress
4. Append to status-log.md

## Consistency Rules

```
STATUS CONSISTENCY RULES

1. NEVER complete an action without updating status
   No orphan work - everything is tracked

2. Status updates are ATOMIC
   Update ALL relevant files in one go

3. Timestamps are required
   Every status change needs a timestamp

4. Progress must be calculable
   X/Y format, not vague "almost done"

5. Blockers are visible
   Blocked status appears in ALL dashboards

6. Log is append-only
   Never delete from status-log.md
```
