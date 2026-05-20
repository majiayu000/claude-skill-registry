---
name: cvm-operator
description: Operate the CVM pipeline end-to-end with reproducible commands. Use when asked to onboard CSV drops, run churn/cross_sell/reactivation scoring, produce top-N actionable customers, or deliver run artifacts and KPI summaries.
---

# CVM Operator

Run the pipeline through deterministic scripts, not ad-hoc command sequences.

## Workflow

1. Select input mode.
- Use `real` mode when the user provides a client CSV folder and mapping JSON.
- Use `demo` mode when no client data is available.

2. Run the orchestrator script.
- From repo root:
`bash skills/cvm-operator/scripts/run_cvm_flow.sh --mode <real|demo> --use-case <churn|cross_sell|reactivation> --top-n 200`
- For all use-cases in one run:
`bash skills/cvm-operator/scripts/run_cvm_flow.sh --mode <real|demo> --all-use-cases --top-n 200`

3. Return fixed deliverables.
- Pipeline summary JSON from `outputs/latest_run_summary*.json`
- Top customers CSV from `outputs/<use_case>_top<N>.csv`
- If `real` mode: mapping report from `outputs/client_mapped_raw/mapping_report.json`

## Required Inputs

For `real` mode, require:
- `--client-dir` path
- `--mapping-file` path

For `demo` mode, optional:
- `--raw-dir` path (if omitted, synthetic data is generated automatically)

## Output Contract

Follow [references/output-contract.md](references/output-contract.md).

## Notes

- Keep `CVM_ENABLE_FEAST=0` and `CVM_ENABLE_MLFLOW=0` by default for fast local runs.
- Keep `CVM_ENABLE_SIGNALS=1` by default so explanations are meaningful.
- If reason quality gate fails, rerun once with `CVM_SIGNALS_REQUIRE_REASON_QUALITY_GATE=0` and report that override explicitly.
