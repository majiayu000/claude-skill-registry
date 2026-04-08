---
name: ln-820-dependency-optimization-coordinator
description: "Upgrades dependencies across all detected package managers. Use when updating npm, NuGet, or pip packages project-wide."
disable-model-invocation: true
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-820-dependency-optimization-coordinator

**Type:** L2 Domain Coordinator
**Category:** 8XX Optimization

Runtime-backed coordinator for cross-stack dependency upgrades. Detects package managers, delegates to one worker per manager, records machine-readable worker summaries, and emits a final coordinator summary.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Project path plus optional upgrade policy |
| **Output** | Aggregated dependency upgrade report with per-worker results |
| **Workers** | ln-821 (npm), ln-822 (nuget), ln-823 (pip) |
| **Runtime** | `.hex-skills/dependency/runtime/runs/{run_id}/` |

---

## Workflow

**Phases:** Pre-flight -> Detect Package Managers -> Security Audit -> Delegate Upgrades -> Collect Results -> Verify Summary -> Report

---

## Runtime Contract

**MANDATORY READ:** Load `shared/references/ci_tool_detection.md`
**MANDATORY READ:** Load `shared/references/coordinator_runtime_contract.md`, `shared/references/dependency_runtime_contract.md`, `shared/references/coordinator_summary_contract.md`

Runtime CLI:

```bash
node shared/scripts/dependency-runtime/cli.mjs start --identifier repo-deps --manifest-file <file>
node shared/scripts/dependency-runtime/cli.mjs status --identifier repo-deps
node shared/scripts/dependency-runtime/cli.mjs checkpoint --phase PHASE_3_DELEGATE_UPGRADES --payload '{...}'
node shared/scripts/dependency-runtime/cli.mjs record-worker-result --payload '{...}'
node shared/scripts/dependency-runtime/cli.mjs record-summary --payload '{...}'
node shared/scripts/dependency-runtime/cli.mjs advance --to PHASE_4_COLLECT_RESULTS
node shared/scripts/dependency-runtime/cli.mjs complete
```

Required state fields:
- `worker_plan`
- `worker_results`
- `child_runs`
- `verification_passed`
- `report_ready`
- `summary_recorded`

Domain checkpoints:
- `PHASE_1_DETECT_PACKAGE_MANAGERS`: detected managers, indicator files, skipped managers
- `PHASE_2_SECURITY_AUDIT`: per-manager audit verdicts, blocking findings, release-age policy
- `PHASE_3_DELEGATE_UPGRADES`: one `child_run` per delegated worker with worker name, identifier, `runId`, and `summaryArtifactPath`
- `PHASE_4_COLLECT_RESULTS`: recorded worker summaries plus unresolved failures or warnings
- `PHASE_5_VERIFY_SUMMARY`: final report path, verification verdict, summary readiness

Guard rules:
- do not advance from `PHASE_3_DELEGATE_UPGRADES` until every planned worker emitted a valid `dependency-worker` summary
- do not complete until the final report checkpoint exists and the `dependency-coordinator` summary was recorded
- consume worker JSON summaries only; never infer worker status from prose output

---

## Phase 0: Pre-flight

Confirm the project is a valid candidate for dependency work before starting the runtime.

| Check | Method | Block if |
|-------|--------|----------|
| Manifest exists | Runtime `start` validation | Missing |
| Project path exists | File inspection | Missing |
| Upgrade policy provided | Manifest or defaults | No |
| Existing active run for identifier | Runtime active pointer | Conflicting active run |

Default options:

| Option | Default | Meaning |
|--------|---------|---------|
| `upgradeType` | `major` | major, minor, or patch |
| `allowBreaking` | `true` | allow major-version migrations |
| `minimumReleaseAge` | `14` | skip very recent releases unless security requires them |
| `testAfterUpgrade` | `true` | workers verify build/tests after changes |

---

## Phase 1: Detect Package Managers

Detect one worker target per package-manager family.

| Package Manager | Indicator Files | Worker |
|-----------------|-----------------|--------|
| npm | `package.json` + `package-lock.json` | ln-821 |
| yarn | `package.json` + `yarn.lock` | ln-821 |
| pnpm | `package.json` + `pnpm-lock.yaml` | ln-821 |
| nuget | `*.csproj` or `*.sln` | ln-822 |
| pip | `requirements.txt` | ln-823 |
| poetry | `pyproject.toml` + `poetry.lock` | ln-823 |
| pipenv | `Pipfile` + `Pipfile.lock` | ln-823 |

Checkpoint payload must include:
- `detected_managers`
- `indicator_paths`
- `worker_plan`
- `skipped_reasons`

---

## Phase 2: Security Audit

Perform lightweight pre-flight security and freshness checks before delegating heavy upgrade work.

| Manager Family | Command | Block Condition |
|----------------|---------|-----------------|
| Node.js | `npm audit --audit-level=high` or manager equivalent | Critical vulnerability with no allowed override |
| NuGet | `dotnet list package --vulnerable` | Critical vulnerability with no allowed override |
| Python | `pip-audit --json` or manager equivalent | Critical vulnerability with no allowed override |

Release-age gate:

| Option | Default | Description |
|--------|---------|-------------|
| `minimumReleaseAge` | `14 days` | Skip packages released too recently |
| `ignoreReleaseAge` | `false` | Override for urgent security patches |

Checkpoint payload must include:
- `audit_results`
- `blocking_findings`
- `release_age_policy`
- `managers_cleared_for_delegation`

---

## Phase 3: Delegate Upgrades

Delegate one child run per worker family. Child runs must be deterministic and artifact-driven.

Delegate using the concrete worker identities selected by the routing table below. Do not synthesize family placeholders or guessed skill IDs in prompts.

Delegation context:

| Field | Type | Description |
|-------|------|-------------|
| `projectPath` | string | Absolute path to target project |
| `packageManager` | enum | npm, yarn, pnpm, nuget, pip, poetry, pipenv |
| `identifier` | string | Stable worker identifier inside the run |
| `runId` | string | Deterministic child run id |
| `summaryArtifactPath` | string | Exact JSON path for the worker summary |
| `options` | object | Upgrade policy, verification flags, safety flags |

Worker selection:

| Manager Family | Worker | Notes |
|----------------|--------|-------|
| npm, yarn, pnpm | ln-821-npm-upgrader | One child run per detected Node manager |
| nuget | ln-822-nuget-upgrader | One child run for .NET |
| pip, poetry, pipenv | ln-823-pip-upgrader | One child run per detected Python manager |

After launching each worker:
1. Checkpoint `child_run` under `PHASE_3_DELEGATE_UPGRADES`.
2. Wait for the emitted `dependency-worker` summary envelope.
3. Record the worker summary with `record-worker-result`.

---

## Phase 4: Collect Results

Aggregate validated worker summaries only.

Worker summary fields consumed by the coordinator:

| Field | Description |
|-------|-------------|
| `producer_skill` | worker identity (`ln-821`, `ln-822`, `ln-823`) |
| `summary_kind` | must be `dependency-worker` |
| `identifier` | stable worker identifier |
| `payload.status` | completed, partial, or failed |
| `payload.upgrades` | applied upgrades with before/after versions |
| `payload.warnings` | non-blocking issues |
| `payload.verification` | build/test verification result |
| `payload.artifact_path` | worker-owned durable report path, if any |

Collection output:
- `worker_results`
- `success_count`
- `partial_count`
- `failed_count`
- `blocking_failures`

---

## Phase 5: Verify Summary

Prepare the final durable report and verify the coordinator can finish deterministically.

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

## Phase 6: Report

Coordinator report schema:

| Field | Description |
|-------|-------------|
| `package_managers` | detected managers handled in this run |
| `workers_activated` | delegated workers |
| `total_packages` | packages analyzed across workers |
| `upgraded` | successful upgrades |
| `skipped` | already latest or policy-skipped packages |
| `failed` | packages or worker runs that failed |
| `breaking_changes` | major-version upgrades or migrations |
| `verification_passed` | aggregate verification verdict |
| `per_worker[]` | machine-readable worker result summaries |
| `warnings[]` | cross-worker warnings |

Completion sequence:
1. Write the durable report.
2. Checkpoint the report path and verification verdict.
3. Record the `dependency-coordinator` summary envelope with `record-summary`.
4. Complete runtime only after the report checkpoint and coordinator summary exist.

---

## Configuration

```yaml
Options:
  upgradeType: major          # major | minor | patch
  allowBreaking: true
  minimumReleaseAge: 14
  auditLevel: high            # none | low | moderate | high | critical
  testAfterUpgrade: true
  buildAfterUpgrade: true
  rollbackOnFailure: true
  skipDev: false
  skipOptional: true
```

---

## Error Handling

Recoverable:

| Error | Recovery |
|-------|----------|
| Peer dependency conflict | Keep worker result as partial, continue collecting |
| Build failure in one worker | Preserve failure, continue other workers |
| Network timeout | Worker retries locally, then reports failure |

Fatal:

| Error | Action |
|-------|--------|
| No package managers found | Finish with empty-result report |
| Runtime validation failure | Pause run and require intervention |
| Missing worker summary for planned child run | Do not advance from collection |

---

## References

- [breaking_changes_patterns.md](references/breaking_changes_patterns.md)
- [security_audit_guide.md](references/security_audit_guide.md)

---

**TodoWrite format (mandatory):**
```text
- Detect package managers (in_progress)
- Delegate ln-821-npm-upgrader child runs (pending)
- Delegate ln-822-nuget-upgrader child runs (pending)
- Delegate ln-823-pip-upgrader child runs (pending)
- Aggregate dependency-worker summaries (pending)
```

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|---------|
| 3 | ln-821-npm-upgrader | Isolated child run with `packageManager`, `runId`, and exact `summaryArtifactPath` |
| 3 | ln-822-nuget-upgrader | Isolated child run with `packageManager`, `runId`, and exact `summaryArtifactPath` |
| 3 | ln-823-pip-upgrader | Isolated child run with `packageManager`, `runId`, and exact `summaryArtifactPath` |

All workers: invoke through Agent tool, checkpoint the child run metadata immediately, then consume the emitted `dependency-worker` summary envelope via `record-worker-result`.

---

## Definition of Done

- [ ] Runtime started with a validated manifest and stable identifier
- [ ] Package managers detected from project indicators
- [ ] Pre-flight security and release-age checks completed
- [ ] One child run delegated per planned worker family
- [ ] Every child run emitted a valid `dependency-worker` summary
- [ ] Coordinator report aggregates per-worker upgrades, warnings, and verification results
- [ ] Final `dependency-coordinator` summary recorded before completion

---

## Phase 7: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `optimization-coordinator`. Run after all phases complete. Output to chat using the `optimization-coordinator` format.

---

**Version:** 1.1.0
**Last Updated:** 2026-01-10
