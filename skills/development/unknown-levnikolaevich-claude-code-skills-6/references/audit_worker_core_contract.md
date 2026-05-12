<!-- SOURCE-OF-TRUTH: shared/references/audit_worker_core_contract.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Audit Worker Core Contract

Hard envelope for audit workers that analyze one category and emit one markdown report plus one machine-readable summary.

## Inputs and Paths

Accepted inputs: `codebase_root`, `runId`, `output_dir`, `summaryArtifactPath`, `tech_stack`, `best_practices`, `domain_mode`, `current_domain`, `scan_path`.

Rules:
- `output_dir` is run-scoped runtime output, not public docs.
- Managed mode passes both `runId` and `summaryArtifactPath`.
- Standalone mode lets the worker runtime create the summary path.
- Domain-aware mode scans only `scan_path` and tags findings with `current_domain`.

## Required Runtime Refs

**MANDATORY READ:** Load `references/audit_summary_contract.md`, `references/audit_scoring.md`, and `references/templates/audit_worker_report_template.md`. Load evaluation runtime refs only when directly invoking that runtime.

## Execution Rules

- Report only unless fixes are explicitly allowed.
- Verify Layer 1 candidates before reporting.
- Use precise `file:line` locations when available.
- Apply worker-specific false-positive filters.
- Score with the shared formula.
- Write the markdown report once under `output_dir`.
- Write JSON summary to `summaryArtifactPath` or the standalone runtime path.

## Summary Payload

Minimum payload fields: `worker`, `status`, `operation=auditing`, `warnings`, `audit.category`, `audit.report_path`, `audit.score`, `audit.issues_total`, `audit.severity_counts`, optional `evidence_basis_counts`.

Default omitted finding evidence to `code_evidence`.

## Definition of Done

Input parsed; scan scope resolved; checks completed; findings include severity, location, recommendation, and effort; report and JSON summary written.
