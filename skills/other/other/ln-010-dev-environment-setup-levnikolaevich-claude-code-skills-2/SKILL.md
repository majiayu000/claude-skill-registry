---
name: ln-010-dev-environment-setup
description: "Installs agents, configures MCP servers, syncs configs, creates and audits instructions. Use after setup or when agents/MCP need alignment."
disable-model-invocation: true
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Dev Environment Setup

**Type:** L2 Domain Coordinator
**Category:** 0XX Shared

Runtime-backed coordinator for environment setup. The runtime is the execution SSOT. Worker outputs are standalone summaries, not chat prose.

## MANDATORY READ

Load these before execution:
- `shared/references/coordinator_runtime_contract.md`
- `shared/references/environment_setup_runtime_contract.md`
- `shared/references/coordinator_summary_contract.md`
- `shared/references/environment_state_contract.md`
- `shared/references/environment_state_schema.json`
- `shared/references/tools_config_guide.md`

## When to Use

- First-time environment setup
- Agent/MCP drift after installs or updates
- Config sync drift across Claude, Gemini, Codex
- Instruction file audit or repair

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `targets` | No | `both` | `gemini`, `codex`, or `both` |
| `dry_run` | No | `false` | Plan without mutating |

## Runtime

Runtime family: `environment-setup-runtime`

Identifier:
- `targets-{normalizedTargets}`

Phases:
1. `PHASE_0_CONFIG`
2. `PHASE_1_ASSESS`
3. `PHASE_2_DISPATCH_PLAN`
4. `PHASE_3_WORKER_EXECUTION`
5. `PHASE_4_VERIFY`
6. `PHASE_5_WRITE_ENV_STATE`
7. `PHASE_6_SELF_CHECK`

Terminal phases:
- `DONE`
- `PAUSED`

## Phase Map

### Phase 1: Assess

Collect one environment snapshot:
- agent availability and versions
- MCP registration/connection state
- hook state
- config sync state
- instruction file state
- disabled flags from `.hex-skills/environment_state.json` if present

Checkpoint payload:
- `assess_summary`

### Phase 2: Dispatch Plan

Build selective dispatch plan. Only invoke workers that have work.

Workers:
- `ln-011-agent-installer`
- `ln-012-mcp-configurator`
- `ln-013-config-syncer`
- `ln-014-agent-instructions-manager`

Checkpoint payload:
- `dispatch_plan`

### Phase 3: Worker Execution

Invoke only selected workers. Do not re-probe the whole environment between worker calls.

Each worker:
- remains standalone-capable
- may receive `summaryArtifactPath`
- must return the same structured summary even without artifact writing

Expected summary kinds:
- `env-agent-install`
- `env-mcp-config`
- `env-config-sync`
- `env-instructions`

Record summaries with runtime `record-worker`.

### Phase 4: Verify

Run targeted verification against the post-worker state:
- health checks
- hook status
- sync status
- instruction file quality

Checkpoint payload:
- `verification_summary`

### Phase 5: Write Environment State

Write final durable state to:
- `.hex-skills/environment_state.json`

Rules:
- runtime state is not environment state
- workers never write `.hex-skills/environment_state.json`
- validate output against shared schema before persisting

Checkpoint payload:
- `env_state_written`
- `final_result`

### Phase 6: Self-Check

Confirm:
- every required phase checkpoint exists
- dispatched worker summaries were recorded
- final state file was written unless `dry_run`

Checkpoint payload:
- `pass`
- `final_result`

## Output Policy

Runtime artifacts:
- `.hex-skills/runtime-artifacts/runs/{run_id}/{summary_kind}/{identifier}.json`

Durable environment output:
- `.hex-skills/environment_state.json`

Do not mix these layers.

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|---------|
| 3 | `ln-011-agent-installer` | Install or update CLI agents |
| 3 | `ln-012-mcp-configurator` | Configure MCP servers, hooks, and permissions |
| 3 | `ln-013-config-syncer` | Sync config to Gemini and Codex |
| 3 | `ln-014-agent-instructions-manager` | Create and audit instruction files |

```text
Skill(skill: "ln-011-agent-installer", args: "{targets} {dry_run}")
Skill(skill: "ln-012-mcp-configurator", args: "{dry_run}")
Skill(skill: "ln-013-config-syncer", args: "{targets} {dry_run}")
Skill(skill: "ln-014-agent-instructions-manager", args: "{dry_run}")
```

## TodoWrite format (mandatory)

```text
- Phase 1: Assess (pending)
- Phase 2: Build dispatch plan (pending)
- Phase 3: Run selected workers (pending)
- Phase 4: Verify final state (pending)
- Phase 5: Write environment_state.json (pending)
- Phase 6: Self-check (pending)
```

## Critical Rules

- Runtime state is the execution SSOT.
- Do not rely on chat memory for resume or recovery.
- Do not run non-selected workers.
- Do not repeat full-environment discovery after every worker.
- `.hex-skills/environment_state.json` is written only in Phase 5.
- `dry_run` may end with `final_result=DRY_RUN_PLAN` and skip final state write.

## Definition of Done

- [ ] Runtime started with identifier-scoped manifest and state
- [ ] Assessment snapshot recorded
- [ ] Dispatch plan checkpointed
- [ ] Worker summaries recorded through machine-readable contract
- [ ] Verification summary checkpointed
- [ ] `.hex-skills/environment_state.json` validated and written, or explicit `DRY_RUN_PLAN`
- [ ] Self-check passed

## Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `domain-coordinator`. Run after all phases complete. Output to chat using the protocol format.

---

**Version:** 5.0.0
**Last Updated:** 2026-03-24
