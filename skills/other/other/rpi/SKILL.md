---
name: rpi
description: 'Full RPI lifecycle orchestrator. Delegates to /discovery, /crank, /validation phase skills. One command, full lifecycle with complexity classification, --from routing, and optional loop. Triggers: "rpi", "full lifecycle", "research plan implement", "end to end".'
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: full
metadata:
  tier: meta
  dependencies:
    - discovery   # phase 1 orchestrator
    - crank       # phase 2 orchestrator
    - validation  # phase 3 orchestrator
    - ratchet     # checkpoint tracking
  internal: false
output_contract: ".agents/rpi/YYYY-MM-DD-*.md"
---

# /rpi — Full RPI Lifecycle Orchestrator
> **Quick Ref:** One command, full lifecycle. `/discovery` → `/crank` → `/validation`. Thin wrapper that delegates to phase orchestrators.
**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**
**THREE-PHASE RULE + FULLY AUTONOMOUS.** Read `references/autonomous-execution.md` — it defines the mandatory 3-phase lifecycle, autonomous execution rules, anti-patterns, and phase completion logging. Unless `--interactive` is set, RPI runs hands-free. Do NOT stop after Phase 2. Do NOT ask the user anything between phases.
## Quick Start
Run `/rpi "<goal>"` for the full lifecycle. For resume, loop, fast-path, and deep examples, read `references/examples.md`.
## Lifecycle Ownership
Phase orchestrators own all sub-skill sequencing, retry gates, and phase budgets. `/discovery` handles brainstorm → design (when PRODUCT.md exists) → search → research → plan → pre-mortem and writes the execution packet; `/crank` owns wave-based implementation and implementation retries; `/validation` owns vibe → post-mortem → retro → forge and validation retries. `/rpi` stays thin: it owns setup, complexity classification, phase routing, the implementation gate, the validation-fail-to-crank loop, and the final report.
## Execution Steps
### Step 0: Setup + Classify
```bash
mkdir -p .agents/rpi
```

**Determine starting phase:**
- default: `discovery`
- `--from=implementation` (aliases: `crank`) → skip to Phase 2
- `--from=validation` (aliases: `vibe`, `post-mortem`) → skip to Phase 3
- aliases `research`, `plan`, `pre-mortem`, `brainstorm` map to `discovery`
- If input is a bead ID and `--from` is not set, resolve it before routing:
  - `bd show <id>` says `issue_type=epic` → Phase 2 using that epic ID
  - child issue with `parent` → Phase 2 using the parent epic ID
- If beads are absent or the input is plain goal text:
  - preserve the goal as the lifecycle objective
  - use `.agents/rpi/execution-packet.json` as the phase-2 handoff when discovery does not yield an epic
  - default to Phase 1 unless the user explicitly set `--from`
- Do not infer epic scope from `ag-*` alone.
**Classify complexity:**

| Level | Criteria | Behavior |
|-------|----------|----------|
| `fast` | Goal <=30 chars, no complex/scope keywords | Full 3-phase. Gates use `--quick` throughout. |
| `standard` | Goal 31-120 chars, or 1 scope keyword | Full 3-phase. Gates use `--quick`. |
| `full` | Complex-operation keyword, 2+ scope keywords, or >120 chars | Full 3-phase. Gates use full council. |

**Complex-operation keywords:** `refactor`, `migrate`, `migration`, `rewrite`, `redesign`, `rearchitect`, `overhaul`, `restructure`, `reorganize`, `decouple`, `deprecate`, `split`, `extract module`, `port`

**Scope keywords:** `all`, `entire`, `across`, `everywhere`, `every file`, `every module`, `system-wide`, `global`, `throughout`, `codebase`

**Overrides:** `--deep` forces `full`. `--fast-path` forces `fast`.
Log:
```
RPI mode: rpi-phased (complexity: <level>)
```

Initialize state:
```
rpi_state = {
  goal: "<goal string>",
  epic_id: null,
  phase: "<discovery|implementation|validation>",
  complexity: "<fast|standard|full>",
  test_first: <true by default; false only when --no-test-first>,
  cycle: 1,
  max_cycles: <3 when --loop; overridden by --max-cycles>,
  verdicts: {}
}
```

### Phase 1: Discovery
Delegate to `/discovery`:
```
Skill(skill="discovery", args="<goal> [--interactive] --complexity=<level>")
```

After `/discovery` completes:
1. Check completion marker: `<promise>DONE</promise>` or `<promise>BLOCKED</promise>`
2. If BLOCKED: stop. Discovery handles its own retries (max 3 pre-mortem attempts). Manual intervention needed.
3. If DONE: read `.agents/rpi/execution-packet.json` (or the matching run archive when `run_id` is known), preserve the execution-packet objective spine, and extract `epic_id` only when it exists
4. Store `rpi_state.epic_id` when present and `rpi_state.verdicts.pre_mortem`
5. Log: `PHASE 1 COMPLETE ✓ (discovery) — proceeding to Phase 2`

### Phase 2: Implementation
If the execution packet has `epic_id`:
```
Skill(skill="crank", args="<epic-id> [--test-first] [--no-test-first]")
```

Otherwise:
```
Skill(skill="crank", args=".agents/rpi/execution-packet.json [--test-first] [--no-test-first]")
```

**Implementation gate (max 3 attempts):**
- `<promise>DONE</promise>`: proceed to validation
- `<promise>BLOCKED</promise>`: retry with block context (max 2 retries)
  - Re-invoke `/crank` on the same lifecycle objective + block reason
  - If still BLOCKED after 3 total: stop, manual intervention needed
- `<promise>PARTIAL</promise>`: retry remaining (max 2 retries)
  - Re-invoke `/crank` on the same epic or execution packet (picks up remaining work)
  - If still PARTIAL after 3 total: stop, manual intervention needed

Record:
```bash
ao ratchet record implement 2>/dev/null || true
```

Log: `PHASE 2 COMPLETE ✓ (implementation) — proceeding to Phase 3`

**DO NOT STOP HERE.** Do not ask the user to commit. Do not summarize and wait. Proceed IMMEDIATELY to Phase 3. Implementation without validation is incomplete work — the flywheel does not turn, learnings are not captured, and quality is unverified.

### Phase 3: Validation
**MANDATORY for all complexity levels.** `/validation` is the Phase 3 orchestrator — it wraps `/vibe` + `/post-mortem` + `/retro` + `/forge`. Do NOT call `/vibe` directly from `/rpi` — call `/validation` which handles the full sequence. `fast` complexity uses inline `--quick` gates inside `/validation`; it does not skip closeout.
If the execution packet has `epic_id`:
```
Skill(skill="validation", args="<epic-id> --complexity=<level> [--strict-surfaces if --quality]")
```

Otherwise:
```
Skill(skill="validation", args="--complexity=<level> [--strict-surfaces if --quality]")
```

**Validation-to-crank loop (max 3 total attempts):**
- `<promise>DONE</promise>`: finish RPI
- `<promise>FAIL</promise>`: vibe found defects
  1. Extract findings from validation output
  2. Re-invoke `/crank` on the same epic or execution packet + findings context (preserve `--test-first` / `--no-test-first` from original invocation)
  3. Re-invoke `/validation`
  4. If still FAIL after 3 total: stop, manual intervention needed

Record:
```bash
ao ratchet record vibe 2>/dev/null || true
```

Log: `PHASE 3 COMPLETE ✓ (validation) — RPI DONE`

### Step Final: Report + Loop
**Report:** Summarize all phase verdicts and epic status.
**Optional loop (`--loop`):** If validation verdict is FAIL and `cycle < max_cycles`:
1. Extract 3 concrete fixes from the post-mortem report
2. Increment `rpi_state.cycle`
3. Re-invoke `/rpi` from discovery with a tightened goal
4. PASS/WARN stops the loop

**Optional spawn-next (`--spawn-next`):** After PASS/WARN finish:
1. Read `.agents/rpi/next-work.jsonl` for harvested follow-up items
2. Report with suggested next `/rpi` command
3. Do NOT auto-invoke

Read `references/report-template.md` for full output format.
Read `references/error-handling.md` for failure semantics.
## Flags
| Flag | Default | Description |
|------|---------|-------------|
| `--from=<phase>` | `discovery` | Start from `discovery`, `implementation`, or `validation` |
| `--interactive` | off | Human gates in discovery |
| `--auto` | on | Fully autonomous (no human gates). Inverse of `--interactive`. Passed through to `/discovery` and `/plan`. |
| `--loop` | off | Post-mortem FAIL triggers new cycle |
| `--max-cycles=<n>` | `3` | Max cycles when `--loop` enabled (default 3) |
| `--spawn-next` | off | Surface follow-up work after completion |
| `--test-first` | on | Strict-quality (passed to `/crank`) |
| `--no-test-first` | off | Opt out of strict-quality |
| `--fast-path` | auto | Force fast complexity (uses quick inline gates, still runs full lifecycle) |
| `--deep` | auto | Force full complexity |
| `--quality` | off | Pass `--strict-surfaces` to `/validation`, making all 4 surface failures blocking |
| `--dry-run` | off | Report without mutating queue |
| `--no-budget` | off | Disable phase time budgets (passed to phase skills) |

## Phase Data Contracts
All transitions use filesystem artifacts (no in-memory coupling). The execution packet (`.agents/rpi/execution-packet.json` as the latest alias, plus `.agents/rpi/runs/<run-id>/execution-packet.json` as the per-run archive) carries the repo execution profile via `contract_surfaces`, plus `done_criteria` and queue claim/finalize metadata between phases. For detailed schemas, read `references/phase-data-contracts.md`.
## Complexity-Scaled Council Gates
### Pre-mortem
- `complexity == "low"` or `complexity == "fast"`: inline review, no spawning (`--quick`)
- `complexity == "medium"` or `complexity == "standard"`: inline fast default (`--quick`)
- `complexity == "high"` or `complexity == "full"`: full council, 2-judge minimum; retry gate max 3 total attempts

### Final Vibe
- `complexity == "low"` or `complexity == "fast"`: inline review, no spawning (`--quick`)
- `complexity == "medium"` or `complexity == "standard"`: inline fast default (`--quick`)
- `complexity == "high"` or `complexity == "full"`: full council, 2-judge minimum; retry gate max 3 total attempts

### Post-mortem (STEP 2)
- `complexity == "low"` or `complexity == "fast"`: inline review, no spawning (`--quick`)
- `complexity == "medium"` or `complexity == "standard"`: inline fast default (`--quick`)
- `complexity == "high"` or `complexity == "full"`: full council, 2-judge minimum; retry gate max 3 total attempts

## Examples
Read `references/examples.md` for full lifecycle, resume, and interactive examples. `--fast-path` still runs validation; it only forces the fast/inline gate profile.
## Troubleshooting
Read `references/troubleshooting.md` for common problems and solutions.
## Runtime Compatibility
RPI runs in three runtime modes. All must produce identical phase artifacts.
| Concern | gc (default) | Hook-capable (Claude Code) | Codex native hooks (v0.115.0+) | Hook-less fallback (Codex pre-v0.115.0) |
|---------|-------------|---------------------------|-------------------------------|----------------------------------------|
| Session start | gc controller starts session | `session-start.sh` hook fires automatically | Native hooks fire automatically | `ao codex start` called explicitly |
| Session stop | gc controller stops session | `session-end.sh` hook fires automatically | Native hooks fire automatically | `ao codex stop` called explicitly |
| Phase execution | `gcExecutor` via gc sessions | `streamExecutor` via Claude CLI | `directExecutor` via Codex CLI | `directExecutor` via Codex CLI |
| Event capture | gc event bus (`ao:phase`, `ao:gate`, `ao:failure`, `ao:metric`) | local events.jsonl (legacy) | local events.jsonl (legacy) | local events.jsonl (legacy) |
| Phase state | `.agents/rpi/phased-state.json` | `.agents/rpi/phased-state.json` | `.agents/rpi/phased-state.json` |
| Phase numbering | 1 = discovery, 2 = implementation, 3 = validation | Same | Same |
| Ratchet checkpoints | `ao ratchet check` | `ao ratchet check` | `ao ratchet check` |
| Agent health | `gc status --json` | manual / tmux inspection | manual |

**gc is the default when available.** `ao rpi` auto-selects `gcExecutor` when `gc` binary is on PATH, version >= 0.13.0, and `city.toml` exists. Falls back to `streamExecutor` otherwise. Use `--runtime stream` or `--runtime tmux` to force legacy executors.

**Minimal contract across all modes:** phase state is always written to `.agents/rpi/phased-state.json`; phase numbering stays `1=discovery`, `2=implementation`, `3=validation`; `ao ratchet check` reads that shared state unchanged; the close-loop flywheel still runs at stop time.
## Reference Documents
- [references/complexity-scaling.md](references/complexity-scaling.md)
- [references/context-windowing.md](references/context-windowing.md)
- [references/gate-retry-logic.md](references/gate-retry-logic.md)
- [references/gate4-loop-and-spawn.md](references/gate4-loop-and-spawn.md)
- [references/phase-budgets.md](references/phase-budgets.md)
- [references/phase-data-contracts.md](references/phase-data-contracts.md)
- [references/report-template.md](references/report-template.md)
- [references/error-handling.md](references/error-handling.md)
- [references/examples.md](references/examples.md)
- [references/autonomous-execution.md](references/autonomous-execution.md)
- [references/troubleshooting.md](references/troubleshooting.md)
