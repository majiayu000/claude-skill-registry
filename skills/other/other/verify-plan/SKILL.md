---
name: verify-plan
description: Score-based convergence loop for adversarial plan verification. Spawns dynamic agent team (3 or 5 agents) that autonomously debates, researches, and iterates until plan reaches convergence threshold or max iterations (3). Invoke with /verify-plan [path]. Produces verdict (PROCEED/REVISE/RETHINK) with binary resolution tracking and quality score.
---

# Verify Plan V2

Convergence loop orchestrator for adversarial plan verification. Spawns fresh Task agents per step — no persistent agents, no agent-to-agent messaging. Main thread holds all state and serializes communication.

## Pipeline Position

```
Plan written → /verify-plan (THIS) → [structural validator, if available] → Execution
```

## Invocation

`/verify-plan [path] [--team=base|scaled] [--threshold=N]`

Path resolution order:
1. Explicit path argument (e.g., `/verify-plan .claude/plans/my-plan.md`)
2. Most recently modified file in `.claude/plans/`
3. Ask user for path

Override flags:
- `--team=base` — force 3-agent team regardless of complexity
- `--team=scaled` — force 5-agent team regardless of complexity
- `--threshold=N` — override complexity threshold (default: 7)

## Team Composition

### Base Team (complexity < 7, unknowns <= 3)

| Agent | Model | Role |
|-------|-------|------|
| plan-challenger | opus | Challenge brief + unknowns manifest |
| plan-resolver (Mode 1) / plan-researcher (Modes 2-3) | sonnet/opus | Three-mode research |
| plan-synthesizer | opus | Binary resolution tracking + convergence |

> **Fallback:** If `plan-resolver` is not available, use `general-purpose` subagent type with the same prompt.

### Scaled Team (complexity >= 7 OR unknowns > 3) — adds:

| Agent | Model | Role |
|-------|-------|------|
| plan-domain-expert | sonnet | Domain-specific challenges |
| plan-devils-advocate | opus | Black-swan scenarios |

## Execution Flow

### Step 1: Discover Plan File

Resolve path using invocation order above. Confirm file exists and is readable. Read plan content.

### Step 2: Complexity Assessment & Team Sizing

Assess plan quality (RICH / ADEQUATE / THIN / TRIVIAL) and complexity:

| Factor | Points |
|---|---|
| Steps/phases in plan | +1/step (max 3) |
| Distinct domains | +1/domain (max 3) |
| External integrations | +2/system |
| Compliance/regulatory | +2 |
| Unknown signals (TBD, TODO, unclear, etc.) | +1 each |
| 10+ referenced files | +1 |

Decision:
- **TRIVIAL plan:** Skip team entirely. Output abbreviated `PROCEED (trivial)` with 1-2 sentence note. ~2K tokens. DONE.
- **THIN plan:** Force BASE team even if complexity score suggests SCALED.
- **Score < 7 AND unknowns <= 3:** BASE team (3 agents).
- **Score >= 7 OR unknowns > 3:** SCALED team (5 agents).
- Override: `--team=base` | `--team=scaled` | `--threshold=N`

Show assessment to user: `"Complexity: N/14. Team: BASE|SCALED. Starting verification..."`

### Step 3: CONVERGENCE LOOP (max 3 iterations)

Initialize `iteration_state` per `protocol.md` schema. Each iteration runs Steps 3a-3d.

#### Step 3a: Challenge Phase

**Base team:**
Spawn `plan-challenger` agent via Task tool:
```
Read plan at [path]. Execute full analysis (Ingest → Explore → Unknowns Manifest → Challenge Brief).
Iteration state: [serialized state or "first iteration"]
Return challenge brief with all challenges in Challenge Schema format + unknowns manifest.
```

**Scaled team:**
Use TeamCreate to run 3 agents in parallel:
- **plan-challenger** — same prompt as above
- **plan-domain-expert** — `"Read plan at [path]. Produce domain-specific challenges. Challenger produced: [paste challenger's challenges to avoid overlap]. Iteration state: [state]"`
- **plan-devils-advocate** — `"Read plan at [path]. Hunt for black-swan scenarios. Other agents produced: [paste their challenges]. Iteration state: [state]"`

TeamDelete immediately after all 3 return. Merge all challenges into `iteration_state.challenges` (cap at 8 total).

#### Step 3b: Research Phase

**Mode 1 — RESOLVE (plan-resolver):**
If unknowns manifest is non-empty, spawn `plan-resolver` (or `general-purpose` if unavailable):
```
Research the following unknowns from plan at [path]:
[paste unknowns manifest]
For each, resolve as CONFIRMED/REFUTED/UNRESOLVABLE/PARTIALLY_RESOLVED.
Format: [VERIFIED: source | finding | impact]
```
Update `iteration_state.unknowns` with findings.

**Modes 2-3 — SURFACE + PROBE (plan-researcher):**
On iteration 1 only (unless Synthesizer directs RE-SWEEP or RE-PROBE):
Spawn `plan-researcher`:
```
Plan at [path]. Goal: [plan goal]. Key technologies: [extracted from plan].
Iteration state: [serialized state including challenges and resolved unknowns]
Execute Mode 2 (SURFACE) then Mode 3 (PROBE).
Return surfaced contexts and probed risks in protocol schema format.
```
Merge findings into `iteration_state`. New challenges (capped at 2) added with appropriate origin tags.

#### Step 3c: Synthesis Phase

Spawn `plan-synthesizer` with FULL iteration state:
```
Evaluate all challenges, unknowns, surfaced contexts, and probed risks.
Iteration state: [full serialized state]
Produce: resolution updates, convergence check, directives (or final verdict if converging).
[If final iteration: include quality score per scoring-rubric.md]
```

#### Step 3d: Convergence Evaluation (main thread)

Read Synthesizer output. Update `iteration_state.convergence`.

| Status | Action |
|---|---|
| CONVERGED | Exit loop → Step 4 |
| BLOCKED | Pause for user: present blocking challenge + options (provide context / acknowledge risk / override / abort). Feed response into next iteration as `user_response`. |
| CONTINUE | Show progress: `"Iteration N: X resolved, Y remaining. Continuing..."` Auto-continue next iteration. |
| FORCED_EXIT | Exit loop → Step 4 |

**Between iterations (non-blocking):** Update user with progress summary.

### Step 4: Final Verdict

If converged, give Challenger ONE audit shot. Spawn `plan-challenger` (brief):
```
Audit the Synthesizer's final verdict and quality score for plan at [path].
Synthesizer verdict: [paste verdict with scores]
If you disagree with any dimension score by 2+ points, flag the discrepancy with your evidence.
Otherwise, confirm the verdict.
```

Present final output to user:
- **Verdict:** PROCEED / REVISE / RETHINK
- **Resolution table** — all challenges with final status
- **Quality score breakdown** — report-only
- **Score discrepancies** — if any from Challenger audit
- **Surfaced context summary** — relevant findings nobody asked about
- **Recommended next step:**
  - PROCEED → "Run structural validation (if available), then execute"
  - REVISE → "Update plan with changes listed, then re-run /verify-plan"
  - RETHINK → "Fundamental issues found. Do NOT proceed to execution. Rework approach first."

### Step 5: Cleanup

TeamDelete if scaled team was created during Step 3a.

## User Checkpoint Protocol

Team runs autonomously except:
1. **BLOCKING challenge** unresolvable by agents → pause, present options
2. **Convergence stall** (no progress between iterations) → pause, confirm continue
3. **Max iterations** with unresolved BLOCKING → pause, present findings
4. **Contradictory research findings** → pause, request tiebreak

Between iterations (non-blocking): `"Iteration N: X resolved, Y remaining. Continuing..."`

## Communication Topology

Main thread is the hub. No direct agent-to-agent messaging. Each agent receives full input from main thread and returns output to main thread.

```
Main Thread (orchestrator + state holder)
    ├──[spawn]──→ Challenger ──[return]──→ challenges + unknowns
    ├──[spawn]──→ Researcher ──[return]──→ findings + surfaced + probed
    ├──[spawn]──→ Synthesizer ──[return]──→ resolution state + convergence
    └──[evaluate]──→ CONVERGED? / PAUSE? / CONTINUE?
```

## Token Budget

| Scenario | Typical | Worst Case |
|---|---|---|
| Trivial plan | ~2K | ~2K |
| Base team, 1 iteration | ~45K | ~55K |
| Base team, 2 iterations | ~70K | ~90K |
| Base team, 3 iterations | ~95K | ~150K |
| Scaled team, 1 iteration | ~70K | ~85K |
| Scaled team, 2 iterations | ~110K | ~140K |
| Scaled team, 3 iterations | ~150K | ~215K |

## Integration Points

- Designed to run **before** any structural validation tool (if available in your setup)
- **RETHINK** → skip downstream validation entirely
- **REVISE** → user updates plan, optionally re-runs /verify-plan
- **PROCEED** → continue to structural validation or execution

## Anti-Patterns — Do NOT

- **Check structure** — a structural validator's job, not this skill's
- **Review code** — a dedicated code review tool's job, not this skill's
- **Use persistent agents** — fresh Task per step
- **Allow agent-to-agent messaging** — main thread serializes all state
- **Use numeric scores for loop control** — binary resolution tracking only
- **Exceed challenge caps** — 5/iteration, 8 total
- **Skip complexity assessment** — always assess before team sizing
- **Run Modes 2-3 on iterations 2-3** — unless Synthesizer directs RE-SWEEP/RE-PROBE
- **Research inside plan-challenger** — unknowns manifest only, research delegated
- **Create TeamCreate for base team** — only for scaled team's parallel challenge phase
