---
name: reality-check
description: 'Compare a claimed state with observable repository evidence and report concrete gaps. Triggers: "reality check", "what is actually done", "compare claim to repo".'
practices: [design-by-contract, evidence-based-engineering]
hexagonal_role: domain
consumes: [claim, repository-evidence]
produces: [reality-check-report.v1]
context_rel:
- kind: supplier-to
  with: plan
skill_api_version: 1
user-invocable: true
metadata:
  tier: judgment
  dependencies: []
  capabilities: [compare_claim_to_evidence]
  effects: [write_advisory_gap_report]
  canonical_status: canonical
  disposition: keep_strategy
output_contract: reality-check-report.v1
---

# Reality Check

Compare an explicit claim with observable evidence. Cite every confirmed or
missing behavior with a file, command result, or artifact. Separate:

- confirmed behavior;
- concrete gap;
- incomplete evidence;
- changed assumptions.

Return the report to the caller. Plan may use concrete gaps to refine the
existing bead or caller intent. Reality Check does not create work, schedule,
claim, implement, validate, retry, or deliver.
