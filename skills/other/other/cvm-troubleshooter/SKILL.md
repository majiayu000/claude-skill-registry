---
name: cvm-troubleshooter
description: Diagnose and unblock CVM pipeline failures quickly. Use when ingest, dbt, train, score, e2e, or drift commands fail; when outputs are missing; or when reason quality/feature availability issues appear.
---

# CVM Troubleshooter

Collect diagnostics first, then propose the smallest rerun.

## Workflow

1. Collect diagnostics using the bundled script.
- `bash skills/cvm-troubleshooter/scripts/collect_diagnostics.sh`

2. Classify failure by stage.
- Ingestion failures: raw data path, missing `raw_*.csv`, mapping errors.
- Prepare-data failures: dbt binary/path, dbt test failures, mart contracts.
- Train failures: missing target columns, empty training marts, model backend deps.
- Score failures: missing decision queue, missing signal tables, reason quality gate.

3. Propose exact fix + rerun command.
- Do not propose broad changes. Give one minimal change and rerun only affected stage.

4. Return a concise incident report.
- include root cause, fix, and verification output path.

## Playbook

Use [references/failure-playbook.md](references/failure-playbook.md).
