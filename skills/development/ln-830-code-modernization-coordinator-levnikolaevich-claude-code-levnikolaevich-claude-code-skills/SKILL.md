---
name: ln-830-code-modernization-coordinator
description: "Modernizes codebase via OSS replacement and bundle optimization. Use when acting on audit findings to reduce custom code."
disable-model-invocation: true
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-830-code-modernization-coordinator

**Type:** L2 Domain Coordinator
**Category:** 8XX Optimization

Runtime-backed coordinator for code modernization. Delegates OSS replacement and bundle-size work to isolated child runs, records machine-readable worker summaries, and emits a final coordinator summary.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Audit report, target module, or modernization scope |
| **Output** | Aggregated modernization report with durable worker artifacts |
| **Workers** | ln-831 (OSS replacer), ln-832 (bundle optimizer) |
| **Runtime** | `.hex-skills/modernization/runtime/runs/{run_id}/` |

---

## Workflow

**Phases:** Pre-flight -> Analyze Input -> Delegate Workers -> Collect Results -> Verify Summary -> Report

---

## Runtime Contract

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md`
**MANDATORY READ:** Load `shared/references/coordinator_runtime_contract.md`, `shared/references/modernization_runtime_contract.md`, `shared/references/coordinator_summary_contract.md`

Runtime CLI:

```bash
node shared/scripts/modernization-runtime/cli.mjs start --identifier repo-modernization --manifest-file <file>
node shared/scripts/modernization-runtime/cli.mjs status --identifier repo-modernization
node shared/scripts/modernization-runtime/cli.mjs checkpoint --phase PHASE_2_DELEGATE_WORKERS --payload '{...}'
node shared/scripts/modernization-runtime/cli.mjs record-worker-result --payload '{...}'
node shared/scripts/modernization-runtime/cli.mjs record-summary --payload '{...}'
node shared/scripts/modernization-runtime/cli.mjs advance --to PHASE_3_COLLECT_RESULTS
node shared/scripts/modernization-runtime/cli.mjs complete
```

Required state fields:
- `worker_plan`
- `worker_results`
- `child_runs`
- `verification_passed`
- `report_ready`
- `summary_recorded`

Domain checkpoints:
- `PHASE_1_ANALYZE_INPUT`: target modules, worker selection, stack detection
- `PHASE_2_DELEGATE_WORKERS`: one `child_run` per delegated worker with worker name, `runId`, and `summaryArtifactPath`
- `PHASE_3_COLLECT_RESULTS`: recorded worker summaries and unresolved failures
- `PHASE_4_VERIFY_SUMMARY`: final report path, verification verdict, summary readiness

Guard rules:
- do not advance from `PHASE_2_DELEGATE_WORKERS` until every planned worker emitted a valid `modernization-worker` summary
- do not complete until the final report checkpoint exists and the `modernization-coordinator` summary was recorded
- consume worker JSON summaries only; never infer worker status from prose output

---

## Phase 0: Pre-flight

Confirm the modernization request has a valid scope and a deterministic runtime target.

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| Audit report or target module | Yes | Block modernization |
| Project path | Yes | Block modernization |
| Verification command available | Yes | Block if workers cannot verify changes |
| Existing active run for identifier | No | Pause if conflicting run exists |

---

## Phase 1: Analyze Input

Select workers based on project type and findings.

Worker selection:

| Condition | ln-831 | ln-832 |
|-----------|--------|--------|
| Audit findings include OSS candidates | Yes | No |
| JS/TS project with `package.json` | No | Yes |
| Both conditions true | Yes | Yes |
| Explicit target module only | Yes | Optional if bundle impact exists |

Stack detection:

| Indicator | Stack | ln-832 Eligible |
|-----------|-------|----------------|
| `package.json` + JS/TS files | JS/TS | Yes |
| `*.csproj` | .NET | No |
| `requirements.txt` or `pyproject.toml` | Python | No |
| `go.mod` | Go | No |

Checkpoint payload must include:
- `input_source`
- `worker_plan`
- `stack_detection`
- `skipped_reasons`

---

## Phase 2: Delegate Workers

Delegate one child run per selected worker. Child runs are deterministic and artifact-driven.

Delegate using the concrete worker identities selected by the routing rules below. Do not synthesize family placeholders or guessed skill IDs in prompts.

Delegation context:

| Field | Type | Description |
|-------|------|-------------|
| `projectPath` | string | Absolute path to the target project |
| `auditReport` | string | Path to audit output when applicable |
| `targetModule` | string | Optional focused module path |
| `identifier` | string | Stable worker identifier |
| `runId` | string | Deterministic child run id |
| `summaryArtifactPath` | string | Exact JSON path for the worker summary |
| `options` | object | Verification flags and worker-specific settings |

Delegation rules:
- launch `ln-831` before `ln-832` when both are selected
- `ln-832` consumes the project state produced by accepted modernization changes, not a guessed baseline
- checkpoint every child run before waiting on its result
- record every emitted worker summary with `record-worker-result`

---

## Phase 3: Collect Results

Aggregate validated worker summaries only.

Worker summary fields consumed by the coordinator:

| Field | Description |
|-------|-------------|
| `producer_skill` | worker identity (`ln-831` or `ln-832`) |
| `summary_kind` | must be `modernization-worker` |
| `identifier` | stable worker identifier |
| `payload.status` | completed, partial, or failed |
| `payload.changes_applied` | kept changes |
| `payload.changes_discarded` | discarded experiments |
| `payload.verification` | build/test verification result |
| `payload.artifact_path` | worker-owned durable report path |
| `payload.warnings` | non-blocking issues |

Collection output:
- `worker_results`
- `success_count`
- `partial_count`
- `failed_count`
- `warnings`

---

## Phase 4: Verify Summary

Prepare the final modernization report and verify the coordinator can finish deterministically.

Verification checklist:
- every planned worker produced one valid summary envelope
- aggregate counts match recorded worker results
- final report path exists or is ready to be written
- `report_ready` and `verification_passed` are true before completion

Failure handling:
1. Keep successful worker results intact.
2. Mark failed workers explicitly in the coordinator report.
3. Do not invent rollback actions beyond what workers already verified.

---

## Phase 5: Report

Coordinator report schema:

| Field | Description |
|-------|-------------|
| `input_source` | audit report or target module |
| `workers_activated` | delegated workers |
| `modules_replaced` | OSS replacements applied |
| `loc_removed` | custom code removed |
| `bundle_reduction` | final bundle reduction summary |
| `verification_passed` | aggregate verification verdict |
| `per_worker[]` | machine-readable worker result summaries |
| `warnings[]` | cross-worker warnings |

Completion sequence:
1. Write the durable report.
2. Checkpoint the report path and verification verdict.
3. Record the `modernization-coordinator` summary envelope with `record-summary`.
4. Complete runtime only after the report checkpoint and coordinator summary exist.

---

## Configuration

```yaml
Options:
  audit_report: "docs/project/codebase_audit.md"
  target_module: ""
  enable_oss_replacer: true
  enable_bundle_optimizer: true
  run_tests: true
  run_build: true
```

---

## Error Handling

Recoverable:

| Error | Recovery |
|-------|----------|
| ln-831 partial result | Continue with ln-832 if still applicable |
| ln-832 failure | Preserve ln-831 result and report partial modernization |
| Build failure in one worker | Keep failure in coordinator report, continue collection |

Fatal:

| Error | Action |
|-------|--------|
| No workers activated | Finish with empty-result report |
| Runtime validation failure | Pause run and require intervention |
| Missing worker summary for planned child run | Do not advance from collection |

---

## References

- `../ln-831-oss-replacer/SKILL.md`
- `../ln-832-bundle-optimizer/SKILL.md`
- `../ln-645-open-source-replacer/SKILL.md`
- `shared/references/ci_tool_detection.md`

---

**TodoWrite format (mandatory):**
```text
- Analyze modernization input (in_progress)
- Delegate ln-831-oss-replacer child run (pending)
- Delegate ln-832-bundle-optimizer child run (pending)
- Aggregate modernization-worker summaries (pending)
```

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|---------|
| 2 | ln-831-oss-replacer | Isolated child run with `runId` and exact `summaryArtifactPath` |
| 2 | ln-832-bundle-optimizer | Isolated child run with `runId` and exact `summaryArtifactPath` |

All workers: start the child runtime, checkpoint the `child_run` metadata, then invoke the worker skill explicitly and consume the emitted `modernization-worker` summary envelope via `record-worker-result`.

```text
# Sequential per selected worker (ln-831 before ln-832 when both selected):
node shared/scripts/modernization-runtime/cli.mjs start --skill {worker} --identifier {identifier} --manifest-file {workerManifestPath} --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}
node shared/scripts/optimization-runtime/cli.mjs checkpoint --phase PHASE_2_DELEGATE --payload '{"child_run":{"worker":"{worker}","run_id":"{childRunId}","summary_artifact_path":"{childSummaryArtifactPath}"}}'
Skill(skill: "{worker}", args: "{identifier} --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}")
Read {childSummaryArtifactPath}
node shared/scripts/optimization-runtime/cli.mjs record-worker-result --payload-file {childSummaryArtifactPath}
```

Worker token substitution: `{worker}` is `ln-831-oss-replacer` or `ln-832-bundle-optimizer`.

---

## Definition of Done

- [ ] Runtime started with a validated manifest and stable identifier
- [ ] Modernization scope analyzed and workers selected from real input
- [ ] One child run delegated per selected worker
- [ ] Every child run emitted a valid `modernization-worker` summary
- [ ] Coordinator report aggregates replacements, bundle changes, warnings, and verification results
- [ ] Final `modernization-coordinator` summary recorded before completion

---

## Phase 6: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `optimization-coordinator`. Run after all phases complete. Output to chat using the `optimization-coordinator` format.

---

**Version:** 1.0.0
**Last Updated:** 2026-03-08
