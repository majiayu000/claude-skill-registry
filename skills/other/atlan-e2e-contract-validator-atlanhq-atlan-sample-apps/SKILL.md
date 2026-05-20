---
name: atlan-e2e-contract-validator
description: Generate and validate e2e test contracts for Atlan workflows, including API responses, output paths, and schema assertions. Use when adding or updating workflow e2e coverage.
---

# Atlan E2E Contract Validator

Define and validate e2e behavior as a machine-checkable contract.

## Workflow
1. Build `e2e_case_contract.yaml` using `../_shared/assets/e2e_case_contract.yaml`.
2. Ensure contract includes:
   - `test_workflow_args`
   - `server_config`
   - `expected_api_responses`
   - `expected_output_paths`
   - `schema_assertions`
3. Run `atlan-fact-verification-gate` if API/output behavior changed.
4. Validate contract:
   `python ../_shared/scripts/validate_e2e_case_contract.py e2e_case_contract.yaml`
5. Align generated test config and schema assertions with contract.

## Rules
- Keep API expectations aligned with `/workflows/v1` behavior.
- Keep output path assertions aligned with SDK defaults.
- Ensure both raw and transformed schema checks are explicit.

## References
- Contract checklist: `references/contract-checklist.md`
- Shared templates: `../_shared/references/artifact-templates.md`
