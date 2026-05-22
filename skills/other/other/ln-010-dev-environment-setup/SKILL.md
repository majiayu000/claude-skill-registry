---
name: ln-010-dev-environment-setup
description: "Installs agents, configures MCP servers, aligns marketplace plugins, creates and audits instructions. Use after setup or when agents/MCP/plugins need alignment."
disable-model-invocation: true
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Dev Environment Setup

**Type:** L2 Domain Coordinator
**Category:** 0XX Shared

Runtime-backed coordinator for environment setup. The runtime is the execution SSOT. Worker outputs are standalone summaries, not chat prose.

## MANDATORY READ

Load these before execution:
- `references/coordinator_runtime_contract.md`
- `references/environment_setup_runtime_contract.md`
- `references/environment_worker_runtime_contract.md`
- `references/coordinator_summary_contract.md`
- `references/agent_skill_roots_contract.md`
- `references/environment_state_contract.md`
- `references/environment_state_schema.json`

MCP servers are targets of this workflow, not a prerequisite for starting it. If a server is disconnected or unavailable, continue with file and CLI inspection and report that surface as `disconnected` or `skipped` instead of failing the coordinator.

## When to Use

- First-time environment setup
- Agent/MCP drift after installs or updates
- Marketplace, plugin, MCP, or Codex execution-default drift across Claude and Codex
- Instruction file audit or repair

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `targets` | No | `both` | `claude`, `codex`, or `both` |
| `dry_run` | No | `false` | Plan without mutating |
| `plugins` | No | `agile-workflow` | Pass-through to ln-013. Use an explicit plugin list, or `all` to request every marketplace plugin. Optional plugins are never installed silently. |
| `auto_install_providers` | No | `false` | Pass-through to ln-013 MCP provider check. When `false`, provider checks are detection-only. |
| `apply_ide_override` | No | `false` | Pass-through to ln-012 Phase 6b. When `true`, ln-012 may write `claudeCode.initialPermissionMode` and `claudeCode.allowDangerouslySkipPermissions` to Cursor / VSCode user settings after explicit user consent. When `false` (default), Phase 6b is detection-only and reports drift without mutating IDE settings. |

## Runtime

Runtime family: `environment-setup-runtime`

Identifier:
- `targets-{normalizedTargets}`

Phases:
1. `PHASE_0_CONFIG`
2. `PHASE_1_ASSESS`
3. `PHASE_1B_PROVIDER_SELECTION`
4. `PHASE_2_DISPATCH_PLAN`
5. `PHASE_3_WORKER_EXECUTION`
6. `PHASE_4_VERIFY`
7. `PHASE_5_WRITE_ENV_STATE`
8. `PHASE_6_SELF_CHECK`

Terminal phases:
- `DONE`
- `PAUSED`

## Phase Map

### Phase 1: Assess

Collect one environment snapshot:
- agent availability and versions
- MCP registration/connection state
- hook state
- marketplace/plugin alignment state
- Codex skill-root discovery health: active roots, cache roots, duplicate skill names, `known_marketplaces.json` install-location drift, whether cache is visible under `~/.codex/skills`, whether `~/.codex/skills` is a whole-root junction to `~/.claude/plugins`, and whether `approval_policy=never` plus `sandbox_mode=danger-full-access` are already aligned
- graph provider dependency status: for each detected project language, check whether the corresponding graph provider binaries are installed (e.g. `basedpyright` for Python, `csharp-ls` for C#). Use `mcp__hex-graph__install_graph_providers` with `mode: "check"` if hex-graph MCP is connected
- graph index freshness: whether hex-graph is connected and the project has been indexed in this session (detection-only, no indexing here)
- instruction file state
- disabled flags from `.hex-skills/environment_state.json` if present
- task management provider availability detection (Linear MCP, gh CLI / Projects v2 readiness, file always available); explicit selection happens in Phase 1b
- research tool detection (Ref → Context7 → websearch)
- git worktree availability
- Claude Code IDE extension state: glob `~/.cursor/extensions/anthropic.claude-code-*` and `~/.vscode/extensions/anthropic.claude-code-*`. For each found, read `claudeCode.initialPermissionMode` and `claudeCode.allowDangerouslySkipPermissions` from the matching IDE user settings.json. Detection-only — no writes here.

Checkpoint payload:
- `assess_summary`

### Phase 1b: Tracker Provider Selection

User selects the task tracker provider (`linear`, `github`, `file`). Selection is persisted in `.hex-skills/environment_state.json` -> `task_management.provider` and reused by every task-related skill (`ln-200`, `ln-220`, `ln-300`, `ln-401`, `ln-130`, etc.).

**MANDATORY READ:** Load `references/tracker_provider_contract.md` before this phase.

Codex `exec --full-auto` cannot prompt the user mid-run. Selection MUST go through runtime `pause` + `pending_decision` + `record-decision` (NOT `AskUserQuestion`).

Decision tree:

1. Load Phase 1 availability data and existing `task_management` from env state.
2. Compute `available = filter([linear, github, file], byAvailability)`:
   - `linear` available iff Linear MCP server is connected.
   - `github` available iff `gh auth status` ok AND repository detected AND (no project_number yet, OR existing project has Status field with all 7 canonical options: Backlog, Todo, In Progress, To Review, To Rework, Done, Canceled).
   - `file` always available.
3. If `task_management.provider` is already set AND `task_management.status == "active"`:

```bash
node references/scripts/environment-setup-runtime/cli.mjs pause \
  --identifier {identifier} \
  --reason "Confirm tracker provider" \
  --payload '{"kind":"tracker_provider_confirmation","question":"Keep current tracker {provider}?","choices":["keep","switch"],"resume_to_phase":"PHASE_1B_PROVIDER_SELECTION"}'
```

Resume with `set-decision`. On `keep` -> reuse existing provider. On `switch` -> fall through to step 4.

4. If no current provider OR user chose `switch` AND `available.length > 1`:

```bash
node references/scripts/environment-setup-runtime/cli.mjs pause \
  --identifier {identifier} \
  --reason "Select tracker provider" \
  --payload '{"kind":"tracker_provider_selection","choices":<available>,"resume_to_phase":"PHASE_1B_PROVIDER_SELECTION"}'
```

5. If `available.length == 1`, do NOT pause. Auto-select with `selected_by: "single_option"` and write the reason (e.g. `"Only file mode available because: Linear MCP disconnected, gh CLI not authenticated"`).
6. Checkpoint Phase 1b:

```bash
node references/scripts/environment-setup-runtime/cli.mjs checkpoint \
  --identifier {identifier} \
  --phase PHASE_1B_PROVIDER_SELECTION \
  --payload '{"provider_selection":{"chosen":"<provider>","available":<available>,"reason":"<text>","selected_by":"user|single_option"}}'
```

Checkpoint payload:
- `provider_selection.chosen`
- `provider_selection.available`
- `provider_selection.reason`
- `provider_selection.selected_by`

### Phase 2: Dispatch Plan

Build selective dispatch plan. Only invoke workers that have work.

Dispatch precedence:

- If marketplace/plugin drift, Codex discovery violation (including whole-root junction), or Codex execution-default drift is present, `ln-013-config-syncer` becomes mandatory before Codex can be reported as healthy.
- If hex-graph MCP is registered and either (a) graph provider deps are missing for detected project languages, or (b) the project has not been indexed, `ln-012-mcp-configurator` becomes mandatory even when MCP registration is already complete. ln-012 owns both graph provider dependency installation (PHASE_3) and graph indexing (PHASE_5).

Workers:
- `ln-011-agent-installer`
- `ln-012-mcp-configurator`
- `ln-013-config-syncer`
- `ln-014-agent-instructions-manager`

Standalone skills packaged in setup-environment but not dispatched by ln-010:
- `ln-015-hex-line-uninstaller` remains direct-invocation only because it removes existing Claude-side integration surfaces.

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
- `env-marketplace-align`
- `env-instructions`

Record summaries with runtime `record-worker`.

### Phase 4: Verify

Run targeted verification against the post-worker state:
- health checks
- hook status
- marketplace/plugin and config alignment status
- Codex skill discovery and execution-default status (including whole-root junction detection)
- instruction file quality
- runtime dependency status (ripgrep, optional language servers)
- graph provider dependency health (basedpyright, scip-python, etc. per project languages)
- graph index status (indexed, skipped, or stale)

Checkpoint payload:
- `verification_summary`

### Phase 5: Write Environment State

Write final durable state to:
- `.hex-skills/environment_state.json`

Includes all detected sections: agents (with alignment status, marketplace plugins, Codex skill-root health, and Codex execution-default state), task_management, research, claude_md, assessment, hooks, ide_extension (Cursor / VSCode Claude Code extension state from Phase 1 plus any Phase 6b mutations from ln-012).

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

**Host Skill Invocation:** `Skill(skill: "...", args: "...")` is mandatory delegation.
- Claude: call the Skill tool exactly as shown.
- Codex: if no Skill tool exists, locate the named skill in available skills, read its `SKILL.md`, treat `args` as `$ARGUMENTS`, execute that skill workflow, then return here with its result/artifact.
- Do not inline worker logic or mark the worker complete without executing the target skill.

| Phase | Worker | Context |
|-------|--------|---------|
| 3 | `ln-011-agent-installer` | Install or update CLI agents |
| 3 | `ln-012-mcp-configurator` | Configure MCP servers, hooks, permissions, and IDE extension permission mode (Phase 6b) |
| 3 | `ln-013-config-syncer` | Install/verify Claude and Codex marketplace plugins, align MCP state, and align Codex defaults |
| 3 | `ln-014-agent-instructions-manager` | Create and audit instruction files |

```text
node references/scripts/environment-worker-runtime/cli.mjs start --skill {worker} --identifier {childIdentifier} --manifest-file {childManifestPath} --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}
node references/scripts/environment-setup-runtime/cli.mjs checkpoint --identifier {identifier} --phase PHASE_3_WORKER_EXECUTION --payload '{"child_run":{"worker":"{worker}","run_id":"{childRunId}","summary_artifact_path":"{childSummaryArtifactPath}"}}'
Skill(skill: "{worker}", args: "{workerArgs} --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}")
Read {childSummaryArtifactPath}
node references/scripts/environment-setup-runtime/cli.mjs record-worker --identifier {identifier} --payload '{...environment worker summary...}'
```

`apply_ide_override` propagates from ln-010 input to ln-012 only. Default `false` keeps Phase 6b in detection mode and reports IDE drift as a WARN in the assessment summary; passing `true` lets ln-012 prompt the user and write Cursor / VSCode settings.

`plugins` and `auto_install_providers` propagate from ln-010 input to ln-013 only. Default plugin selection is `agile-workflow`; optional plugins require an explicit list or `all`. `auto_install_providers=false` keeps MCP provider handling detection-only.

## TodoWrite format (mandatory)

```text
- Phase 1: Assess (pending)
- Phase 1b: Tracker provider selection (pending)
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
- Do not dispatch `ln-015-hex-line-uninstaller` from normal setup; it is standalone cleanup.
- Do not repeat full-environment discovery after every worker.
- `.hex-skills/environment_state.json` is written only in Phase 5.
- `dry_run` may end with `final_result=DRY_RUN_PLAN` and skip final state write.

## Definition of Done

- [ ] Runtime started with identifier-scoped manifest and state
- [ ] Assessment snapshot recorded
- [ ] Tracker provider explicitly selected by user or single-option-confirmed
- [ ] Dispatch plan checkpointed
- [ ] Child worker run metadata checkpointed before each delegation
- [ ] Worker summaries recorded through machine-readable contract
- [ ] Verification summary checkpointed
- [ ] `.hex-skills/environment_state.json` validated and written, or explicit `DRY_RUN_PLAN`
- [ ] Self-check passed

## Meta-Analysis

Optional reference: load `references/meta_analysis_protocol.md` only when the user asks for post-run meta-analysis or protocol-formatted run reflection.

Skill type: `domain-coordinator`. When requested, run after all phases complete. Output to chat using the protocol format.

---

**Version:** 6.1.0
**Last Updated:** 2026-04-07
