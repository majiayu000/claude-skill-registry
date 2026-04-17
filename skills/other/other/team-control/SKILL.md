---
name: team-control
description: Unit Circle Laboratory + sc-dev-team autonomous mission control. Provides human-in-the-loop automation layer, pipeline management, context lifecycle, stuck-state prevention. UC re-execution series and dev branch milestones. Adapted from uc-lab pattern for code plan/execute/verify/complete. Auto-activates during UC milestone work; trigger: user says 'bring up the dev team'.
format: 2025-10-02
version: 1.0.0
status: active
updated: 2026-04-15
---

# Team Control — Autonomous Mission Control

Autonomous mission-control skill with two parameterized modes for the two team branches:

- **UC Mode** — Unit Circle Laboratory, v1.50 milestone review series (formerly `uc-lab`)
- **Dev Mode** — SC Dev Team, dev branch code execution (formerly `sc-dev-team`)

Both modes share the same four-agent architecture, autonomy principles, context management, and stuck-state prevention. The mode is selected by the active branch (UC on `v1.50`, Dev on `dev`) or by explicit invocation. Either way, the team acts as the human-in-the-loop layer so the pipeline never stalls waiting for decisions.

## Team Architecture (shared)

| Agent | Model | Role | Key Responsibility |
|-------|-------|------|-------------------|
| **lab-director** | Opus | Authority | Go/no-go, plan approval, quality rubric, strategic direction |
| **flight-ops** | Opus | Operations | Pipeline management, milestone/phase spawning, error handling |
| **capcom** | Sonnet | Communications | Context lifecycle, handoffs, warm starts, continuity |
| **watchdog** | Haiku | Monitor | Stuck detection, health checks, overload alerts |

Agent definitions: `.claude/agents/lab-director.md`, `flight-ops.md`, `capcom.md`, `watchdog.md`.

## Autonomy Principles (shared)

1. **lab-director IS the human** — no waiting for external approval
2. **Auto-approve** plans that pass quality gates (TDD, tests, NASA SE or clean commits)
3. **Auto-close** milestones when enforcement checks pass
4. **Auto-handoff** context when pressure detected (>80%)
5. **Auto-scale** parallelism based on observed metrics (UC Mode)
6. **Auto-heal** stuck states via watchdog detection + flight-ops resolution

## Context Management (shared)

- **Green (0-60%):** Normal operations
- **Yellow (60-80%):** Prepare handoff materials
- **Red (80%+):** Initiate handoff immediately
- Handoffs stored at `.planning/uc-observatory/handoffs/` (UC Mode) or repo-local (Dev Mode)
- STATE.md is always the source of truth

## Stuck State Prevention (shared)

| Pattern | Detection | Resolution |
|---------|-----------|------------|
| Waiting for user | Watchdog | lab-director decides |
| Context full | Capcom | Handoff protocol |
| Agent idle | Watchdog | flight-ops reassigns |
| Repeated failure | Watchdog | flight-ops escalates |
| Lost state | Capcom | Restore from handoff |

---

## UC Mode — Unit Circle Laboratory

Autonomous mission control for the Unit Circle re-execution series (v1.50.14+). Branch-bound to `v1.50`.

### Pipeline Flow

```
QUEUE → PRE-FLIGHT → INIT → PLAN → APPROVE → EXECUTE → VERIFY → ANALYZE → RETRO → CLOSE → HANDOFF → NEXT
  ↑                                                                                                    |
  +----------------------------------------------------------------------------------------------------+
```

### Quality Rubric (UC Mode, VERBATIM)

| Dimension | Weight | Min Score |
|-----------|--------|-----------|
| Completeness | 25% | 3.0 |
| Depth | 30% | 3.0 |
| Connections | 25% | 3.0 |
| Honesty | 20% | 3.0 |

Weighted average must be >= 3.0 for auto-approval.

### Integration with Observatory

The lab team coordinates with `uc-observatory` agents:

- **Pre-milestone:** Spawns uc-brainstorm-engine, uc-skill-forger
- **Post-milestone:** Spawns uc-perf-analyst, uc-proof-engineer, uc-retro-analyst
- **Between milestones:** Reviews observatory reports for strategic decisions

### Chipset & Files (UC Mode)

- Lab chipset: `.planning/uc-observatory/lab-chipset.yaml`
- Observatory chipset: `.planning/uc-observatory/chipset.yaml`
- Handoffs: `.planning/uc-observatory/handoffs/`
- Reports: `.planning/uc-observatory/reports/`
- Metrics: `.planning/uc-observatory/metrics/`

---

## Dev Mode — SC Dev Team

Autonomous execution team for dev branch milestones. Adapted from the UC pattern for code execution (plan/execute/verify/complete). Trigger: user says "bring up the dev team" or "sc-dev-team". Branch-bound to `dev`.

### Activation

1. Read `.planning/STATE.md` for current position
2. Read `~/.claude/teams/sc-dev-team/config.json` for team state
3. Check `TaskList` for pending work
4. Create team if not exists: `TeamCreate(team_name: "sc-dev-team")`
5. Spawn agents into team:
   - `flight-ops` (opus) — drives execution
   - `lab-director` (opus) — approves, unblocks
   - `capcom` (sonnet) — context management
   - `watchdog` (haiku) — health monitoring
6. Assign first pending task to flight-ops

### Pipeline Flow (Dev Mode)

```
STATE.md → PLAN PHASE → EXECUTE PHASE → VERIFY → NEXT PHASE → ... → COMPLETE MILESTONE
```

### Key Differences from UC Mode

- **Branch:** dev (not v1.50)
- **Work type:** Code execution (not review milestones)
- **GSD commands:** `/gsd:plan-phase`, `/gsd:execute-phase`, `/gsd:complete-milestone`
- **No observatory integration** (dev milestones don't use the UC review rubric)
- **Quality gate:** Tests pass + clean commits (not the review scoring rubric above)

### Team Files (Dev Mode)

- Team config: `~/.claude/teams/sc-dev-team/config.json`
- Tasks: `~/.claude/tasks/sc-dev-team/`
