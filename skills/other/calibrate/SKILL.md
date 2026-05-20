---
name: calibrate
description: Run an evidence-seeking calibration roundtable to realign the plan with the North Star. Use when pausing between phases, when agents disagree, when reviewing work, when the user mentions "calibrate" or "realign", or when making decisions that affect the plan.
---

# Calibrate — Orchestrator

Hard stop. Evidence-based calibration. Realign to North Star.

> **Pattern:** This skill uses the orchestrator-subagent pattern. Each phase runs in a fresh context for optimal performance. See `docs/guides/ORCHESTRATOR_SUBAGENT_PATTERN.md`.

## When This Applies

| Signal | Action |
|--------|--------|
| Phase completion | Run scheduled calibration |
| User says "calibrate" or "realign" | Run full protocol |
| Agents disagree on approach | Run challenge/synthesis |
| Drift detected | Ad-hoc calibration |
| User says "/calibrate" | Run full protocol |

---

## Tool Reference

### File Operations
| Tool | Purpose |
|------|---------|
| `Read(north_star_path)` | Read North Star Card |
| `Read(requirements_path)` | Read REQ-*/AC-* specs |
| `Write(file_path, content)` | Write phase reports |

### Beads/BV
| Command | Purpose |
|---------|---------|
| `bd list --json` | Get all beads with status |
| `bd view <id>` | View specific bead |
| `bv --robot-summary` | Dependency overview |
| `bv --robot-alerts` | Check for issues |

### Testing
| Command | Purpose |
|---------|---------|
| `pytest` | Run test suite |
| `pytest --cov` | Coverage check |
| `ubs --staged` | Security scan |

### Historical Context
| Command | Purpose |
|---------|---------|
| `cass search "calibration" --robot --limit 5` | Find past calibration decisions |
| `cass search "drift" --robot --days 30` | Find recent drift incidents |
| `cm context "calibration for <phase>" --json` | Get learned patterns |

### Evidence Types
| Type | Example |
|------|---------|
| Code | `src/auth/validator.ts:42` |
| Test | `npm test auth` → PASS |
| Doc | URL + excerpt |
| Measurement | "Response: 150ms" |
| Discriminating test | Fails A, passes B |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CALIBRATE ORCHESTRATOR                        │
│  - Creates session: sessions/calibrate-{timestamp}/              │
│  - Manages TodoWrite state                                       │
│  - Spawns subagents with minimal context                         │
│  - Passes report_path + summary between phases                   │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Coverage Agent │  │   Drift Agent   │  │ Challenge Agent │
│  agents/coverage│  │  agents/drift   │  │ agents/challenge│
│  Fresh context  │  │  Fresh context  │  │  Fresh context  │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    01_coverage.md      02_drift.md        03_challenge.md
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐
│ Synthesize Agent│  │  Report Agent   │ → Final output to user
│agents/synthesize│  │  agents/report  │
│  Fresh context  │  │  Fresh context  │
└────────┬────────┘  └────────┬────────┘
         │                    │
    04_synthesis.md     05_user_report.md
```

## Subagents

| Phase | Agent | Input | Output |
|-------|-------|-------|--------|
| 1 | `agents/coverage.md` | requirements, beads | coverage gaps |
| 2 | `agents/drift.md` | North Star, coverage report | drift items |
| 3 | `agents/challenge.md` | coverage + drift reports | test results |
| 4 | `agents/synthesize.md` | all reports | decisions + dissent |
| 5 | `agents/report.md` | synthesis | user-facing report |

---

## Philosophy

**Tests adjudicate, not rhetoric.** Pursue verifiable truth, not persuasive agreement.

> **Key insight (DebateCoder, 2025):** "Tests are the medium of disagreement, not rhetoric." Rhetorical debate degrades outcomes—voting alone beats extended debate (`research/003-debate-or-vote.md`).

| Principle | Meaning |
|-----------|---------|
| **Tests over rhetoric** | Disagreements resolved by test results, not persuasion |
| **Write discriminating tests** | Tests that PASS for one approach, FAIL for another |
| **No compromise** | Evidence decides winner; don't average opinions |
| **Preserve dissent** | If tests don't discriminate, present both positions to user |
| **User decides when value-dependent** | If the "right" answer depends on user preferences, stop and ask |

---

## Execution Flow

### 1. Setup (Orchestrator)

```markdown
1. Create session directory:
   mkdir -p sessions/calibrate-{timestamp}

2. Initialize TodoWrite with phases:
   - [ ] Phase 1: Coverage Analysis
   - [ ] Phase 2: Drift Detection
   - [ ] Phase 3: Test-Based Challenge
   - [ ] Phase 4: Synthesis
   - [ ] Phase 5: User Report

3. Gather inputs:
   - phase_name: The phase being calibrated
   - north_star_path: Path to North Star Card
   - requirements_path: Path to REQ-*/AC-* file
   - beads_status: bd list --json
```

### 2. Phase 1: Coverage Analysis

**Spawn:** `agents/coverage.md`

**Input:**
```json
{
  "phase_name": "<phase>",
  "session_dir": "sessions/calibrate-{timestamp}",
  "requirements_path": "PLAN/01_requirements.md",
  "beads_status": "<bd list --json output>"
}
```

**Expected output:**
```json
{
  "report_path": "sessions/.../01_coverage_report.md",
  "p0_coverage": "4/5 (80%)",
  "gaps_summary": "1 P0 missing bead, 1 P0 missing tests"
}
```

### 3. Phase 2: Drift Detection

**Spawn:** `agents/drift.md`

**Input:**
```json
{
  "phase_name": "<phase>",
  "session_dir": "sessions/calibrate-{timestamp}",
  "north_star_path": "PLAN/00_north_star.md",
  "coverage_report_path": "<from Phase 1>"
}
```

**Expected output:**
```json
{
  "report_path": "sessions/.../02_drift_report.md",
  "alignment_summary": "5/7 ALIGNED, 1 DRIFTING, 1 OFF-TRACK",
  "drift_items": ["NS-1: Auth method", "NS-3: Mobile support"]
}
```

### 4. Phase 3: Test-Based Challenge

**Spawn:** `agents/challenge.md`

**Input:**
```json
{
  "session_dir": "sessions/calibrate-{timestamp}",
  "coverage_report_path": "<from Phase 1>",
  "drift_report_path": "<from Phase 2>"
}
```

**Expected output:**
```json
{
  "report_path": "sessions/.../03_challenge_report.md",
  "verified_claims": ["NS-1 drift", "NS-3 mobile gap"],
  "unresolved": ["API rate limit assumption"]
}
```

### 5. Phase 4: Synthesis

**Spawn:** `agents/synthesize.md`

**Input:**
```json
{
  "session_dir": "sessions/calibrate-{timestamp}",
  "coverage_report_path": "<from Phase 1>",
  "drift_report_path": "<from Phase 2>",
  "challenge_report_path": "<from Phase 3>"
}
```

**Expected output:**
```json
{
  "report_path": "sessions/.../04_synthesis_report.md",
  "decisions": [{"action": "Implement SSO", "priority": "P0"}],
  "user_questions": ["Load test timing?"],
  "preserved_dissent": ["API rate limit adequacy"]
}
```

### 6. Phase 5: User Report

**Spawn:** `agents/report.md`

**Input:**
```json
{
  "session_dir": "sessions/calibrate-{timestamp}",
  "synthesis_report_path": "<from Phase 4>",
  "north_star_path": "PLAN/00_north_star.md"
}
```

**Expected output:**
```json
{
  "report_path": "sessions/.../05_user_report.md",
  "summary": {"alignment": "5/7", "blocking": 2},
  "user_questions": ["Load test timing?", "bd-130 scope creep?"]
}
```

### 7. Finalize (Orchestrator)

1. Update TodoWrite (all phases complete)
2. Read `05_user_report.md`
3. Present to user
4. Log changes to `.beads/change-log.md` if decisions made

---

## Context Optimization

Why subagents beat monolithic calibration:

| Monolithic | Subagent Pattern |
|------------|------------------|
| All context in one window | Each phase gets fresh 200k |
| "Lost in middle" risk | No degradation |
| One failure corrupts all | Phases are isolated |
| ~3000 token prompt | ~500 tokens per phase |

**Research backing:**
- `research/056-multi-agent-orchestrator.md`: +90.2% over single-agent
- `research/004-context-length-hurts.md`: Context degradation is real

---

## Evidence Standard (All Subagents)

For any non-trivial claim, include at least one:

| Evidence Type | Example |
|---------------|---------|
| **Code evidence** | `src/auth/validator.ts:42` |
| **Test evidence** | `npm test auth` → PASS |
| **Doc evidence** | URL + relevant excerpt |
| **Measurement** | "Response time: 150ms" |
| **Discriminating test** | Test that fails one option, passes another |

---

## Status Labels

| Category | Values |
|----------|--------|
| Beads | `SOUND` / `FLAWED` / `UNCERTAIN` |
| Alignment | `ALIGNED` / `DRIFTING` / `OFF-TRACK` |
| Assumptions | `VERIFIED` / `UNVERIFIED` / `RISKY` |
| Challenges | `ACCEPTED` / `REJECTED` |

---

## Anti-Patterns

| Don't | Why |
|-------|-----|
| Compromise for harmony | Truth > harmony |
| Soften criticism | Clarity > comfort |
| Skip pre-work | Unprepared = unproductive |
| Force agreement | Preserve dissent |
| Argue by rhetoric | Evidence only |
| Pass full content between phases | Pass paths + summaries |

---

## Templates

Located in `.claude/templates/calibration/`:
- `user-report.md` — Final output to user
- `broadcast.md` — Agent analysis broadcast
- `response.md` — Challenge responses
- `decision.md` — Falsifiable decisions
- `summary.md` — Agent-to-agent summary
- `change-log-entry.md` — Plan change records

---

## See Also

- `agents/` — Subagent definitions
- `docs/guides/ORCHESTRATOR_SUBAGENT_PATTERN.md` — Pattern documentation
- `docs/workflow/IDEATION_TO_PRODUCTION.md` — Complete pipeline
- `docs/workflow/PROTOCOLS.md` — Protocol cards
