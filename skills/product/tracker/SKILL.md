---
name: tracker
description: Portfolio-level project tracker for ID8Labs. Tracks all projects through lifecycle states, enforces stage gates, calculates decay, and coordinates review rituals. The nervous system of the ID8Labs pipeline.
version: 1.0.0
mcps: [Memory]
---

# ID8TRACKER - Pipeline Nervous System

## Purpose

Track all ID8Labs projects from idea capture through exit. Enforce quality gates, calculate activity decay, trigger review rituals, and generate portfolio dashboards.

---

## Lifecycle States

```
CAPTURED → VALIDATING → VALIDATED → ARCHITECTING → BUILDING → LAUNCHING → GROWING → OPERATING → EXITING → EXITED
```

### Special States
- **ICE** - Intentionally frozen, decay paused
- **KILLED** - Failed/abandoned with lessons logged (terminal)
- **ARCHIVED** - Successfully completed (terminal)

---

## Commands

### `/tracker status [project-slug]`

**No argument:** Show portfolio dashboard
**With argument:** Show detailed project card

**Process:**
1. If no argument, read all project cards from `.id8labs/projects/active/`
2. Calculate decay for each project
3. Generate dashboard using `templates/dashboard.md`
4. Highlight any projects in warning (50-79%) or critical (80%+) decay

### `/tracker new <project-slug> <project-name>`

Create a new project in CAPTURED state.

**Process:**
1. Generate project card from `templates/project-card.md`
2. Set state to CAPTURED, created/last_activity to today
3. Save to `.id8labs/projects/active/{slug}.md`
4. Confirm creation with summary

### `/tracker update <project-slug> <new-state>`

Transition project to new state.

**Process:**
1. Load project card
2. Verify transition is valid (see `frameworks/project-states.md`)
3. Check gate requirements (see `frameworks/stage-gates.md`)
4. If gate passed:
   - Update state
   - Reset decay (state_entered = today)
   - Log transition in state history
   - Save project card
5. If gate blocked:
   - List unmet requirements
   - Suggest actions to close gaps

### `/tracker ice <project-slug> [reason]`

Freeze a project. Decay stops.

**Process:**
1. Load project card
2. Record previous state and freeze date
3. Set state to ICE
4. Log reason (required if not provided, prompt for it)
5. Move file to `.id8labs/projects/ice/`
6. Confirm freeze

### `/tracker thaw <project-slug>`

Revive a frozen project.

**Process:**
1. Load project from `.id8labs/projects/ice/`
2. Run revival questions (see `frameworks/decay-mechanics.md` REVIVAL section)
3. Restore to previous state
4. Reset decay timer
5. Move file to `.id8labs/projects/active/`
6. Confirm revival with recommitment

### `/tracker kill <project-slug> [reason]`

Terminate a project permanently.

**Process:**
1. Load project card
2. Prompt for lessons learned if not provided
3. Set state to KILLED
4. Log reason and lessons
5. Move to `.id8labs/projects/archive/`
6. Confirm kill with lessons summary

### `/tracker log <project-slug> <activity>`

Log activity to a project. Resets decay timer.

**Process:**
1. Load project card
2. Add activity to activity log with timestamp
3. Update last_activity to today
4. Save project card
5. Confirm log entry

### `/tracker pulse`

Daily 2-minute pulse check.

**Process:**
1. Load all active projects
2. Calculate decay for each
3. Use `rituals/daily-pulse.md` format
4. Show:
   - Any critical (80%+) projects
   - Any warnings (50-79%)
   - Recommended focus for today
   - Quick wins available

### `/tracker review`

Weekly 15-minute review.

**Process:**
1. Load all projects (active + ice)
2. Calculate metrics
3. Use `rituals/weekly-review.md` format
4. Walk through each active project:
   - Progress since last review
   - Blockers
   - Gate readiness
5. Generate recommendations

### `/tracker strategy`

Monthly 30-minute strategy session.

**Process:**
1. Load entire portfolio (active + ice + recent archive)
2. Use `rituals/monthly-strategy.md` format
3. Portfolio health analysis
4. Stage distribution
5. Ice box cleanup decisions
6. Pattern recognition
7. Next month intentions

### `/tracker dashboard`

Regenerate the DASHBOARD.md file.

**Process:**
1. Load all projects
2. Calculate all metrics
3. Use `templates/dashboard.md`
4. Write to `.id8labs/dashboard/DASHBOARD.md`
5. Confirm generation

### `/tracker gates <project-slug>`

Show gate requirements for next transition.

**Process:**
1. Load project card
2. Identify current state and target state
3. Load requirements from `frameworks/stage-gates.md`
4. Show checklist with current completion status

### `/tracker gate-pass <project-slug> <requirement>`

Mark a gate requirement as met.

**Process:**
1. Load project card
2. Add requirement to gates_passed array
3. Save project card
4. Show updated gate status

---

## Decay Calculation

```
decay_percent = (days_since_last_activity / state_max_duration) * 100
```

### Decay Windows by State

| State | Warning (50%) | Critical (80%) | Freeze (100%) |
|-------|---------------|----------------|---------------|
| CAPTURED | 7 days | 11 days | 14 days |
| VALIDATING | 15 days | 24 days | 30 days |
| VALIDATED | 10 days | 17 days | 21 days |
| ARCHITECTING | 7 days | 11 days | 14 days |
| BUILDING | 45 days | 72 days | 90 days |
| LAUNCHING | 10 days | 17 days | 21 days |
| GROWING | 90 days | 144 days | 180 days |
| OPERATING | - | - | No decay |
| EXITING | 30 days | 48 days | 60 days |

### What Resets Decay
- Invoking any ID8Labs skill for the project
- Manual `/tracker log` entry
- State transition via `/tracker update`
- Completing a gate requirement

---

## Integration with Other Skills

When other ID8Labs skills complete work, they MUST log to tracker:

```markdown
## Handoff Pattern

After skill completion:
1. Save skill outputs
2. Call: /tracker log {project-slug} "{skill-name}: {summary}"
3. If state transition appropriate, suggest: /tracker update {project-slug} {new-state}
```

### Example Integration Points

| Skill Completes | Log Message | Suggested Transition |
|-----------------|-------------|---------------------|
| scout (BUILD) | "Scout: Validation complete - BUILD verdict" | VALIDATING → VALIDATED |
| scout (KILL) | "Scout: Validation complete - KILL verdict" | → KILLED |
| architect | "Architect: Architecture doc complete" | VALIDATED → ARCHITECTING |
| launch | "Launch: Product launched to {channel}" | BUILDING → LAUNCHING |
| growth | "Growth: Experiment {name} completed" | (no transition, activity log) |
| ops | "Ops: SOP created for {process}" | GROWING → OPERATING |
| exit | "Exit: Exit memo drafted" | OPERATING → EXITING |

---

## Memory MCP Integration

Use Memory MCP to store portfolio-level learnings:

```
Create entities for:
- Successful patterns (what works)
- Kill post-mortems (what failed)
- Review insights (strategic observations)
- Velocity benchmarks (how long things take)
```

Query Memory when:
- Starting a new project (recall similar patterns)
- Hitting a blocker (check if solved before)
- Completing a stage (log learnings)

---

## Health Status Indicators

| Symbol | Status | Decay Range | Action |
|--------|--------|-------------|--------|
| 🟢 | Healthy | 0-49% | None needed |
| 🟡 | Warning | 50-79% | Surface in pulse |
| 🔴 | Critical | 80-99% | Escalate in review |
| ⛔ | Frozen | 100% | Block transitions |
| ❄️ | Ice | N/A | Intentionally paused |
| ⚰️ | Killed | N/A | Terminal |
| ✅ | Archived | N/A | Complete |

---

## File Operations

### Reading Projects
```
Active: .id8labs/projects/active/*.md
Ice: .id8labs/projects/ice/*.md
Archive: .id8labs/projects/archive/*.md
```

### Writing Projects
- Parse YAML frontmatter for structured data
- Preserve markdown content
- Update timestamps on every write

### Dashboard Location
```
.id8labs/dashboard/DASHBOARD.md
```

---

## Error Handling

| Error | Response |
|-------|----------|
| Project not found | List available projects, suggest `/tracker new` |
| Invalid state transition | Explain valid transitions, show current state |
| Gate blocked | List unmet requirements with suggestions |
| Missing required field | Prompt for the field |
| File write error | Report error, suggest manual check |

---

## Reminder Configuration

Settings stored in `.id8labs/config/settings.yaml`:

```yaml
reminders:
  pulse_frequency: daily    # daily, every-other-day, off
  review_frequency: weekly  # weekly, biweekly, off
  strategy_frequency: monthly

nudge_style: direct         # gentle, direct, aggressive

decay:
  warn_threshold: 50
  critical_threshold: 80
  freeze_threshold: 100
```

---

## Changelog

### v1.0.0 (2025-12-21)
- Initial release
- Full lifecycle state machine
- Decay mechanics with configurable windows
- Gate verification system
- Review rituals (daily/weekly/monthly)
- Dashboard generation
- Memory MCP integration for learnings
