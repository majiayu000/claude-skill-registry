<!-- SOURCE-OF-TRUTH: shared/references/audit_output_schema.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Audit Worker Output Schema

Standard output format for all L3 audit workers in the stateful 6XX runtime.

Delivery is split between:
- JSON summary transport for optional aggregation
- temporary markdown evidence reports for detailed findings

## Runtime Output Layout

Workers write markdown reports to `.hex-skills/runtime-artifacts/runs/{run_id}/audit-report/` and JSON summaries to `.hex-skills/runtime-artifacts/runs/{run_id}/evaluation-worker/`. If the caller requested aggregation, worker markdown reports are temporary evidence inputs. In standalone worker runs, the worker markdown report remains the user-facing small report.

**Contracts:**
- JSON transport: `references/audit_summary_contract.md`
- markdown evidence template: `references/templates/audit_worker_report_template.md`
- runtime envelope: evaluation worker runtime contract when the calling skill runs the evaluation platform

### Worker Return (Fallback)

When structured output cannot be preserved in-context, worker may return a compact fallback:

```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/{worker}--global.md
Score: 7.5/10 | Issues: 5 (C:0 H:2 M:2 L:1)
```

Some specialized workers include diagnostic sub-scores:

```
Report written: .hex-skills/runtime-artifacts/runs/{run_id}/audit-report/{worker}--{identifier}.md
Score: 6.0/10 (C:72 K:85 Q:68 I:90) | Issues: 3 (H:1 M:2 L:0)
```

### Run-Scoped Runtime Artifacts

All managed audit runs use the same run-scoped layout:

| Artifact | Path |
|----------|------|
| markdown evidence | `.hex-skills/runtime-artifacts/runs/{run_id}/audit-report/{worker}--{identifier}.md` |
| JSON summary | `.hex-skills/runtime-artifacts/runs/{run_id}/evaluation-worker/{worker}--{identifier}.json` |

Public history is preserved in consolidated outputs such as `docs/project/.audit/results_log.md`, not in dated worker staging folders.

## Field Descriptions

### JSON Summary Payload

See `references/audit_summary_contract.md` for the canonical envelope and payload schema.

Key payload fields:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `completed`, `skipped`, or `error` |
| `category` | string | Audit category name (for example `Security`, `Build Health`) |
| `report_path` | string | Worker markdown report path; temporary when the caller requested aggregation, durable in standalone worker runs |
| `score` | number | 0-10 scale, calculated per `audit_scoring.md` |
| `issues_total` | integer | Sum of all severity counts |
| `severity_counts` | object | Issue counts by severity |
| `warnings` | array | Transport-safe warnings for managed aggregation |

### Checks Array

Inside the markdown report, each check represents a discrete audit rule:

| Status | Meaning |
|--------|---------|
| `passed` | No issues found |
| `failed` | Issues found and findings emitted |
| `warning` | Minor issues or incomplete check |
| `skipped` | Check not applicable for this codebase |

### Findings Table

| Column | Required | Description |
|--------|----------|-------------|
| Severity | Yes | CRITICAL, HIGH, MEDIUM, or LOW |
| Location | Yes | File path with line number (`path:line`) |
| Issue | Yes | What is wrong |
| Principle | Yes | Which rule or principle is violated |
| Recommendation | Yes | How to fix it |
| Effort | Yes | S (`< 1h`), M (`1-4h`), L (`> 4h`) |

## Domain-Aware Worker Output

For workers that scan per-domain, keep domain metadata both in the report and in the JSON payload:

```json
{
  "status": "completed",
  "category": "Architecture & Design",
  "report_path": ".hex-skills/runtime-artifacts/runs/demo/audit-report/{worker}--users.md",
  "score": 6,
  "issues_total": 4,
  "severity_counts": {
    "critical": 1,
    "high": 2,
    "medium": 1,
    "low": 0
  },
  "warnings": [],
  "domain_name": "users",
  "scan_scope": "src/users"
}
```

## Usage in SKILL.md

Reference this file instead of duplicating worker output expectations:

```markdown
## Output Format

See `references/audit_output_schema.md` and `references/audit_summary_contract.md`.

Write:
- markdown report to `output_dir`
- JSON summary to `summaryArtifactPath` when present
- compact fallback text summary only if structured output cannot be preserved
```

---
**Version:** 2.0.0
**Last Updated:** 2026-02-15
