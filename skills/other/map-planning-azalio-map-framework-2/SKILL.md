---
name: map-planning
version: "1.0.0"
description: Implements file-based planning for MAP Framework workflows with branch-scoped task tracking in .map/ directory. Prevents goal drift via automatic plan synchronization before tool use and validates completion state on exit.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
hooks:
  PreToolUse:
    - matcher: "Write|Edit|Bash"
      hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/show-focus.sh"
  Stop:
    - hooks:
        - type: command
          command: "${CLAUDE_PLUGIN_ROOT}/scripts/check-complete.sh"
---

# MAP Planning Skill

Implements Manus-style file-based planning adapted for MAP Framework workflows. Uses branch-scoped persistent files to track goals, tasks, progress, and learnings across agent sessions.

## Core Concept

Instead of relying solely on conversation context (limited window), this skill externalizes planning artifacts to the filesystem. The agent reads/writes structured files that survive context resets, enable progress resumption, and provide explicit traceability.

**Key Principle**: Filesystem as Extended Memory
- Plan defines "what to do" (phases, dependencies, criteria)
- Notes capture "what learned" (findings, errors, decisions)
- Progress tracked via checkboxes (visual state)
- Branch-specific scope (isolation between features/bugs)

## File Structure

All files reside in `.map/` directory with branch-based naming:

```
.map/
├── task_plan_<branch>.md    # Primary plan with phases and status
├── findings_<branch>.md     # Research findings, decisions, key files
└── progress_<branch>.md     # Action log, errors, test results
```

**Example**: On branch `feature-auth`:
- `.map/task_plan_feature-auth.md`
- `.map/findings_feature-auth.md`
- `.map/progress_feature-auth.md`

## Hook Behavior

### PreToolUse Hook (Before Write/Edit/Bash)

Runs `show-focus.sh` → extracts only the in_progress section (~200 tokens) and displays Goal + current phase. **Purpose**: Re-anchors agent to original goal before taking action, prevents goal drift.

### Stop Hook (Before Agent Exit)

Runs `check-complete.sh` → validates all phases have terminal state before allowing exit.

**Terminal States**: `complete`, `blocked`, `won't_do`, `superseded`

## Plan File Structure

```markdown
# Task Plan: <Brief Title>

## Goal
<One sentence describing end state>

## Current Phase
ST-001

## Phases

### ST-001: <Title>
**Status:** in_progress
Risk: low|medium|high
Complexity: 1-10
Files: <paths>

Validation:
- [ ] <criterion 1>
- [ ] <criterion 2>

### ST-002: <Title>
**Status:** pending
...

## Terminal State
**Status:** pending
Reason: [Not yet complete]
```

## Workflow Integration

### Initialization
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/init-session.sh
```
Creates `.map/` directory and skeleton files for current branch.

### Progress Tracking
- PreToolUse hook auto-displays focus before Write/Edit/Bash
- Update **Status:** in_progress → **Status:** complete as phases finish
- Check validation criteria checkboxes [x] when done

### 3-Strike Error Protocol
Log errors to `progress_<branch>.md` after attempt 3+. After 3 failed attempts:
1. Escalate to user (CONTINUE/SKIP/ABORT options)
2. If SKIP: mark phase `blocked`, move to next subtask
3. If ABORT: mark workflow `blocked`, exit

### Terminal State
Update `## Terminal State` with final status before exiting. Stop hook validates this.

## MAP Workflow Integration

When `/map-efficient` runs:
1. `init-session.sh` creates `.map/` skeleton
2. task-decomposer populates phases from blueprint
3. Actor implements → PreToolUse hook shows focus
4. Monitor validates → outputs `status_update` field
5. Orchestrator updates task_plan using Monitor's status_update
6. Stop hook validates terminal state before exit

`/map-fast` skips planning — hooks are no-op if plan missing.

## Single-Writer Governance

Only Monitor agent updates task_plan status (via `status_update` output field).

| Agent | Read task_plan | Write task_plan |
|-------|----------------|-----------------|
| task-decomposer | No | Yes (creates) |
| Actor | Yes | No |
| Monitor | Yes | Yes (status only) |
| Predictor | Yes | No |
| Orchestrator | Yes | No (applies Monitor output) |

**Why**: Prevents race conditions, ensures consistent state, clear ownership.

## Best Practices

- **Goal clarity**: Specific, measurable outcomes
- **Granular phases**: Each phase = 1 agent action
- **Checkpoint frequently**: Update status immediately after completion
- **Terminal state early**: Mark `blocked` as soon as blocker identified

## Error Handling

| Issue | Fix |
|-------|-----|
| Plan not found | Run `init-session.sh` |
| Stop hook warns "No terminal state" | Update `## Terminal State` section |
| Branch name with `/` | Scripts sanitize: `feature/auth` → `feature-auth` |

## Terminal States

| State | When |
|-------|------|
| `complete` | All phases finished, criteria met |
| `blocked` | Needs external input (human, resource) |
| `won't_do` | Task intentionally cancelled |
| `superseded` | Replaced by different approach |

---

**Version**: 1.0.0 (2025-01-10)

**References**:
- [planning-with-files](https://github.com/OthmanAdi/planning-with-files) - Original pattern
