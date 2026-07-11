---
name: codebase-recon
description: 'Reconstruct a repository as cited entry-to-test flows, bounded claims, and a reusable baseline or verified delta. Triggers: "build a repository mental model", "trace this codebase", "refresh the prior recon".'
practices:
- legacy-code-seams
- ddd-bounded-context
- design-by-contract
hexagonal_role: supporting
consumes:
- repo-context
- existing-docs
produces:
- codebase-recon.v1
- evidence-bounded-recon-report
context_rel:
- kind: customer-of
  with: research
- kind: customer-of
  with: validate
- kind: customer-of
  with: doc
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: topic
metadata:
  tier: execution
  dependencies:
  - validate
  - doc
output_contract: codebase-recon.v1 JSON plus cited report, validated by skills/codebase-recon/scripts/validate-output.sh
---

# Codebase Recon

Build a reusable, falsifiable model of a repository. This skill reports what
the tree and executable probes support; it does not edit code or issue a final
PASS/WARN/FAIL verdict.

## Workflow

1. Record the current commit and the repository's local source-of-truth
   precedence. Search for a prior recon pack before starting.
2. If no prior pack exists, use `baseline` mode. If one exists, verify its
   still-valid claims against the current commit and use `delta` mode. Preserve
   valid evidence by reference and describe only changed paths and synthesis.
3. Trace representative paths from entry point to domain logic, integration
   boundary, and test. Prefer a few complete flows over a broad file inventory.
4. Keep four views distinct in the report: mental model, bounded audit, pattern
   evidence, and synthesis. Label each claim `fact`, `inference`, or `unknown`,
   assign confidence, and cite evidence for facts and inferences.
5. List inspected and uninspected scope. Write the JSON manifest and companion
   report, then run the validator. Missing evidence and hidden coverage gaps are
   contract failures, not prose caveats.

```bash
skills/codebase-recon/scripts/validate-output.sh <recon.json>
```

Evidence entries are existing file paths, optionally followed by a line number.
Delta manifests require an existing prior pack, `baseline_verified: true`, and
at least one described change.

Executable behavior:
[references/codebase-recon.feature](references/codebase-recon.feature).

## Do not

- Regenerate a full replacement report when a verified delta is possible.
- Present an inference as fact or omit uninspected scope.
- Turn the recon artifact into a completion verdict or a code-change plan.
