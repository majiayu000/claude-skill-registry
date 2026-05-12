<!-- SOURCE-OF-TRUTH: shared/references/audit_summary_contract.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Audit Summary Contract

Audit payload rules for 6XX workers using the evaluation-worker summary envelope. Coordinators consume JSON summaries first and read markdown reports only for detailed evidence.

## Envelope

Audit workers emit the shared evaluation-worker envelope:

```json
{
  "schema_version": "1.0.0",
  "summary_kind": "evaluation-worker",
  "run_id": "ln-620-global-...",
  "identifier": "global",
  "producer_skill": "ln-621",
  "produced_at": "2026-03-27T10:00:00Z",
  "payload": {
    "worker": "ln-621",
    "status": "completed",
    "operation": "auditing",
    "warnings": [],
    "audit": {}
  }
}
```

Rules:
- `summary_kind` is `evaluation-worker`.
- `run_id` is mandatory; generate a standalone `run_id` when the caller does not pass one.
- `identifier` is stable inside the run and names the domain/target only.
- audit-specific fields live under `payload.audit`.

## Payload

Required `payload.audit` fields:

```json
{
  "category": "Security",
  "report_path": ".hex-skills/runtime-artifacts/runs/<run_id>/audit-report/ln-621--global.md",
  "score": 8.5,
  "issues_total": 3,
  "severity_counts": {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 0
  }
}
```

Allowed `payload.status`: `completed`, `skipped`, `error`. `complete` is invalid.

Optional audit fields: `diagnostic_scores`, `domain_name`, `scan_scope`, `metadata`.

## Paths

When `summaryArtifactPath` is passed, write the JSON summary to that exact path and managed filename, normally `{worker}--{identifier}.json`.

When absent, write to the standalone run-scoped path and optionally echo the same summary in structured output.

Canonical paths:
- managed: `.hex-skills/runtime-artifacts/runs/{parent_run_id}/evaluation-worker/{worker}--{identifier}.json`
- standalone: `.hex-skills/runtime-artifacts/runs/{run_id}/evaluation-worker/{worker}--{identifier}.json`

The JSON summary is the transport contract for scores, severity totals, category labels, and report location. The markdown report remains the evidence artifact for findings tables and extended data.
