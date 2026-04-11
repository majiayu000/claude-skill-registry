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
- `shared/references/environment_worker_runtime_contract.md`
- `shared/references/coordinator_summary_contract.md`
- `shared/references/agent_skill_roots_contract.md`
- `shared/references/environment_state_contract.md`
- `shared/references/environment_state_schema.json`

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
| `apply_ide_override` | No | `false` | Pass-through to ln-012 Phase 6b. When `true`, ln-012 may write `claudeCode.initialPermissionMode` and `claudeCode.allowDangerouslySkipPermissions` to Cursor / VSCode user settings after explicit user consent. When `false` (default), Phase 6b is detection-only and reports drift without mutating IDE settings. |

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
- Codex skill-root discovery health: active roots, cache roots, duplicate skill names, `known_marketplaces.json` install-location drift, whether cache is visible under `~/.codex/skills`, and whether `approval_policy=never` plus `sandbox_mode=danger-full-access` are already aligned
- instruction file state
- disabled flags from `.hex-skills/environment_state.json` if present
- task management provider detection (Linear → GitHub → file)
- research tool detection (Ref → Context7 → websearch)
- git worktree availability
- Claude Code IDE extension state: glob `~/.cursor/extensions/anthropic.claude-code-*` and `~/.vscode/extensions/anthropic.claude-code-*`. For each found, read `claudeCode.initialPermissionMode` and `claudeCode.allowDangerouslySkipPermissions` from the matching IDE user settings.json. Detection-only — no writes here.

Checkpoint payload:
- `assess_summary`
### Phase 2: Dispatch Plan

Build selective dispatch plan. Only invoke workers that have work.

Dispatch precedence:
- If Codex discovery violation or Codex execution-default drift is present, `ln-013-config-syncer` becomes mandatory before Codex can be reported as healthy.

Workers:
- `ln-011-agent-installer`
- `ln-012-mcp-configurator`
- `ln-013-config-syncer`
- `ln-014-agent-instructions-manager`

Checkpoint payload:
- `dispatch_plan`

### Phase 3: Worker Execution

Invoke only selected workers. Do not re-probe the whole environment between worker calls.

Phase 1 assessment is the shared discovery snapshot. Materialize child manifests from that snapshot and pass them into managed worker runs.

For each selected worker:
- compute deterministic `child_run_id`
- compute exact `child_summary_artifact_path`
- checkpoint `child_run` metadata before delegation
- start the managed `environment-worker-runtime` child run
- invoke the worker with both `runId` and `summaryArtifactPath`
- read the artifact written by the worker
- record the structured worker summary through `environment-setup-runtime`

Each worker remains standalone-capable, but Phase 3 always uses managed transport.

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
- Codex skill discovery and execution-default status
- instruction file quality
- runtime dependency status (ripgrep, optional language servers)

Checkpoint payload:
- `verification_summary`

### Phase 5: Write Environment State

Write final durable state to:
- `.hex-skills/environment_state.json`

Includes all detected sections: agents (with sync status, Codex skill-root health, and Codex execution-default state), task_management, research, claude_md, assessment, hooks, ide_extension (Cursor / VSCode Claude Code extension state from Phase 1 plus any Phase 6b mutations from ln-012).

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
| 3 | `ln-012-mcp-configurator` | Configure MCP servers, hooks, permissions, and IDE extension permission mode (Phase 6b) |
| 3 | `ln-013-config-syncer` | Sync config to Gemini and repair Codex skill-root mapping + MCP state |
| 3 | `ln-014-agent-instructions-manager` | Create and audit instruction files |

```text
node shared/scripts/environment-worker-runtime/cli.mjs start --skill {worker} --identifier {childIdentifier} --manifest-file {childManifestPath} --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}
node shared/scripts/environment-setup-runtime/cli.mjs checkpoint --identifier {identifier} --phase PHASE_3_WORKER_EXECUTION --payload '{"child_run":{"worker":"{worker}","run_id":"{childRunId}","summary_artifact_path":"{childSummaryArtifactPath}"}}'
Skill(skill: "{worker}", args: "{workerArgs} --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}")
Read {childSummaryArtifactPath}
node shared/scripts/environment-setup-runtime/cli.mjs record-worker --identifier {identifier} --payload '{...environment worker summary...}'
```

`apply_ide_override` propagates from ln-010 input to ln-012 only. Default `false` keeps Phase 6b in detection mode and reports IDE drift as a WARN in the assessment summary; passing `true` lets ln-012 prompt the user and write Cursor / VSCode settings.

## TodoWrite format (mandatory)

```text
- Phase 1: Assess (pending)
- Phase 2: Build dispatch plan (pending)
- Phase 3: Start child runtime, checkpoint child metadata, and run selected workers (pending)
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
- [ ] Child worker run metadata checkpointed before each delegation
- [ ] Worker summaries recorded through machine-readable contract
- [ ] Verification summary checkpointed
- [ ] `.hex-skills/environment_state.json` validated and written, or explicit `DRY_RUN_PLAN`
- [ ] Self-check passed

## Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `domain-coordinator`. Run after all phases complete. Output to chat using the protocol format.

---

**Version:** 6.1.0
**Last Updated:** 2026-04-07
