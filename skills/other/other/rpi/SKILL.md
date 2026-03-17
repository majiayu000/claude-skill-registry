---
name: rpi
description: 'Full RPI lifecycle orchestrator. Discovery (research+plan+pre-mortem) → Implementation (crank) → Validation (vibe+post-mortem). One command, sequential skill invocations with retry gates and fresh phase contexts.'
disable-model-invocation: true
metadata:
  tier: execution
  dependencies:
    - research    # discovery sub-step
    - plan        # discovery sub-step
    - pre-mortem  # discovery gate
    - crank       # implementation phase
    - vibe        # validation sub-step
    - post-mortem # validation sub-step
    - ratchet     # checkpoint tracking
  internal: false
---

# /rpi — Full RPI Lifecycle Orchestrator

> **Quick Ref:** One command, full lifecycle. Discovery → Implementation → Validation. The session is the lead; sub-skills manage their own teams.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

## Quick Start

```bash
/rpi "add user authentication"                        # full lifecycle
/rpi --interactive "add user authentication"          # human gates in discovery only
/rpi --from=discovery "add auth"                      # resume discovery
/rpi --from=implementation ag-23k                      # skip to crank with existing epic
/rpi --from=validation                                 # run vibe + post-mortem only
/rpi --loop --max-cycles=3 "add auth"                 # optional iterate-on-fail loop
/rpi --test-first "add auth"                          # pass --test-first to /crank
```

## CLI Toolchain Configuration

RPI control-plane command paths are configurable through `.agentops/config.yaml` or environment variables:

```yaml
rpi:
  runtime_mode: auto        # auto|direct|stream
  runtime_command: claude   # runtime process command
  ao_command: ao            # ratchet/checkpoint command
  bd_command: bd            # epic/child query command
  tmux_command: tmux        # status liveness probe command
```

Environment variable overrides:
- `AGENTOPS_RPI_RUNTIME` / `AGENTOPS_RPI_RUNTIME_MODE`
- `AGENTOPS_RPI_RUNTIME_COMMAND`
- `AGENTOPS_RPI_AO_COMMAND`
- `AGENTOPS_RPI_BD_COMMAND`
- `AGENTOPS_RPI_TMUX_COMMAND`

Safety defaults:
- `git`, `bash`, and `ps` remain fixed system tools in the RPI control plane.
- Command precedence is `flags > env > config > defaults` where flags exist.

## Architecture

```
/rpi <goal | epic-id> [--from=<phase>] [--interactive]
  │ (session = lead, no TeamCreate)
  │
  ├── Phase 1: Discovery
  │   ├── /research
  │   ├── /plan
  │   └── /pre-mortem (gate)
  │
  ├── Phase 2: Implementation
  │   └── /crank (autonomous execution)
  │
  └── Phase 3: Validation
      ├── /vibe (gate)
      └── /post-mortem (retro + flywheel)
```

**Human gates (default):** 0 — fully autonomous.
**Human gates (`--interactive`):** discovery approvals in `/research` and `/plan`.
**Retry gates:** pre-mortem FAIL → re-plan, implementation BLOCKED/PARTIAL → re-crank, vibe FAIL → re-crank (max 3 attempts each).
**Optional loop (`--loop`):** post-mortem FAIL can spawn another RPI cycle.

Read `references/phase-data-contracts.md` for the phase-to-phase artifact contract.

## Execution Steps

Given `/rpi <goal | epic-id> [--from=<phase>] [--interactive]`:

### Step 0: Setup

```bash
mkdir -p .agents/rpi
```

Determine starting phase:
- default: `discovery`
- `--from=implementation` (alias: `crank`)
- `--from=validation` (aliases: `vibe`, `post-mortem`)
- aliases `research`, `plan`, and `pre-mortem` map to `discovery`

If input looks like an epic ID (`ag-*`) and `--from` is not set, start at implementation.

Initialize state:

```
rpi_state = {
  goal: "<goal string>",
  epic_id: null,
  phase: "<discovery|implementation|validation>",
  auto: <true unless --interactive>,
  test_first: <true if --test-first>,
  complexity: null,
  cycle: 1,
  parent_epic: null,
  verdicts: {}
}
```

### Phase 1: Discovery

Discovery is one context window that runs research, planning, and pre-mortem together:

```text
/research <goal> [--auto]
/plan <goal> [--auto]
/pre-mortem
```

After discovery completes:
1. Extract epic ID from `bd list --type epic --status open` and store in `rpi_state.epic_id`.
2. Extract pre-mortem verdict (PASS/WARN/FAIL) from latest pre-mortem council report.
3. Store verdict in `rpi_state.verdicts.pre_mortem`.
4. Write summary to `.agents/rpi/phase-1-summary-YYYY-MM-DD-<goal-slug>.md`.
5. Record ratchet and telemetry:

```bash
ao ratchet record research 2>/dev/null || true
bash scripts/checkpoint-commit.sh rpi "phase-1" "discovery complete" 2>/dev/null || true
bash scripts/log-telemetry.sh rpi phase-complete phase=1 phase_name=discovery 2>/dev/null || true
```

Gate behavior:
- PASS/WARN: proceed to implementation.
- FAIL: re-run `/plan` with findings context, then `/pre-mortem` (max 3 total attempts).

Detailed retry contract: `references/gate-retry-logic.md`.

### Phase 2: Implementation

Requires `rpi_state.epic_id`.

```text
/crank <epic-id> [--test-first]
```

After implementation completes:
1. Check completion via crank output / epic child statuses.
2. Gate result:
   - DONE: proceed to validation
   - BLOCKED or PARTIAL: re-run `/crank` with context (max 3 total attempts)
3. Write summary to `.agents/rpi/phase-2-summary-YYYY-MM-DD-<goal-slug>.md`.
4. Record ratchet and telemetry:

```bash
ao ratchet record implement 2>/dev/null || true
bash scripts/checkpoint-commit.sh rpi "phase-2" "implementation complete" 2>/dev/null || true
bash scripts/log-telemetry.sh rpi phase-complete phase=2 phase_name=implementation 2>/dev/null || true
```

Detailed retry contract: `references/gate-retry-logic.md`.

### Phase 3: Validation

Validation runs final review and lifecycle close-out:

```text
/vibe recent            # use --quick recent for low/medium complexity
/post-mortem <epic-id>  # use --quick for low/medium complexity
```

After validation completes:
1. Extract vibe verdict and store `rpi_state.verdicts.vibe`.
2. If present, extract post-mortem verdict and store `rpi_state.verdicts.post_mortem`.
3. Gate result:
   - PASS/WARN: finish RPI
   - FAIL: re-run implementation with findings, then re-run validation (max 3 total attempts)
4. Write summary to `.agents/rpi/phase-3-summary-YYYY-MM-DD-<goal-slug>.md`.
5. Record ratchet and telemetry:

```bash
ao ratchet record vibe 2>/dev/null || true
bash scripts/checkpoint-commit.sh rpi "phase-3" "validation complete" 2>/dev/null || true
bash scripts/log-telemetry.sh rpi phase-complete phase=3 phase_name=validation 2>/dev/null || true
```

Looping and spawn-next behavior lives in `references/gate4-loop-and-spawn.md`.

### Step Final: Report

Read `references/report-template.md` for the final output format and next-work handoff pattern.

Read `references/error-handling.md` for failure semantics and retries.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--from=<phase>` | `discovery` | Start from `discovery`, `implementation`, or `validation` (aliases accepted) |
| `--interactive` | off | Enable human gates in discovery (`/research`, `/plan`) |
| `--auto` | on | Legacy flag; autonomous is default |
| `--loop` | off | Enable post-mortem FAIL loop into next cycle |
| `--max-cycles=<n>` | `1` | Max cycle count when `--loop` is enabled |
| `--spawn-next` | off | Surface harvested follow-up work after post-mortem |
| `--test-first` | off | Pass `--test-first` to `/crank` |
| `--fast-path` | auto | Force low-complexity gate mode (`--quick`) |
| `--deep` | auto | Force high-complexity gate mode (full council) |
| `--dry-run` | off | Report actions without mutating next-work queue |

## Examples

### Full Lifecycle

**User says:** `/rpi "add user authentication"`

**What happens:**
1. Discovery runs `/research`, `/plan`, `/pre-mortem` and produces epic `ag-5k2`.
2. Implementation runs `/crank ag-5k2` until children are complete.
3. Validation runs `/vibe` then `/post-mortem`, extracts learnings, and suggests next work.

### Resume from Implementation

**User says:** `/rpi --from=implementation ag-5k2`

**What happens:**
1. Skips discovery.
2. Runs `/crank ag-5k2`.
3. Runs validation (`/vibe` + `/post-mortem`).

### Interactive Discovery

**User says:** `/rpi --interactive "refactor payment module"`

**What happens:**
1. Discovery runs with human gates in `/research` and `/plan`.
2. Implementation and validation remain autonomous.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Supervisor spiraled branch count | Detached HEAD healing or legacy `codex/auto-rpi-*` naming created detached branches | Keep `--detached-heal` off for supervisor mode (default), prefer detached worktree execution, then run cleanup: `ao rpi cleanup --all --prune-worktrees --prune-branches --dry-run` to preview, then rerun without `--dry-run`. |
| Discovery retries hit max attempts | Plan has unresolved risks | Review pre-mortem findings, re-run `/rpi --from=discovery` |
| Implementation retries hit max attempts | Epic has blockers or unresolved dependencies | Inspect `bd show <epic-id>`, fix blockers, re-run `/rpi --from=implementation` |
| Validation retries hit max attempts | Vibe found critical defects repeatedly | Apply findings, re-run `/rpi --from=validation` |
| Missing epic ID at implementation start | Discovery did not produce a parseable epic | Verify latest open epic with `bd list --type epic --status open` |
| Large-repo context pressure | Too much context in one window | Use `references/context-windowing.md` and summarize phase outputs aggressively |

### Emergency control

- Cancel in-flight RPI work immediately: `ao rpi cancel --all` (or `--run-id <id>` for one run).
- Remove stale worktrees and legacy branches: `ao rpi cleanup --all --prune-worktrees --prune-branches`.

## See Also

- `skills/research/SKILL.md` — discovery exploration
- `skills/plan/SKILL.md` — discovery decomposition
- `skills/pre-mortem/SKILL.md` — discovery risk gate
- `skills/crank/SKILL.md` — implementation execution
- `skills/vibe/SKILL.md` — validation gate
- `skills/post-mortem/SKILL.md` — validation close-out
