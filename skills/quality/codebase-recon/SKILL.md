---
name: codebase-recon
description: Reconstruct a repository as cited
---
# Codebase Recon

Build a reusable, falsifiable model of a repository. This skill reports what
the tree and executable probes support; it does not edit code or issue a final
PASS/WARN/FAIL verdict.

## Constraints

- To prevent a floating recon, record the exact repository commit and local
  source-of-truth precedence.
- Because confidence is not evidence, type every material claim and cite each
  fact and inference.
- To preserve traceability, prefer a verified delta when a prior pack exists
  instead of rewriting unchanged evidence as fresh discovery.

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

## Output Specification

- **Artifact directory:** `.agents/recon/<run-id>/`
- **Filename convention:** `codebase-recon.json` with companion report
  `codebase-recon.md` in the same directory.
- **Format:** `codebase-recon.v1` JSON manifest plus an evidence-cited Markdown
  report covering the same commit, mode, flows, claims, and scope boundaries.
- **Validation command:** `skills/codebase-recon/scripts/validate-output.sh <codebase-recon.json>`
  validates the machine-readable manifest; the cited Markdown report remains
  its human-readable companion.
- **Downstream handoff:** pass both validated artifact paths to the requesting
  research, planning, review, or documentation workflow; the consumer owns any
  decision or code-change plan.

Baseline manifests carry at least one complete entry-to-test flow. Delta
manifests name an existing prior recon, prove `baseline_verified: true`, and
describe at least one changed path. Every manifest lists both inspected and
uninspected scope.

The validator is the machine boundary:

```bash
skills/codebase-recon/scripts/validate-output.sh <recon.json>
```

Evidence entries are existing file paths, optionally followed by a line number.
Delta manifests require an existing prior pack, `baseline_verified: true`, and
at least one described change.

Executable behavior:
[references/codebase-recon.feature](references/codebase-recon.feature).

## Quality

- Every fact and inference resolves to existing evidence; unknowns remain
  visibly typed and never masquerade as established behavior.
- Representative flows reach entry, domain, integration, and test surfaces,
  while inspected and uninspected scope stay explicit.
- The named validator passes before the JSON manifest and companion report are
  handed to a downstream consumer.

## Do not

- Regenerate a full replacement report when a verified delta is possible.
- Present an inference as fact or omit uninspected scope.
- Turn the recon artifact into a completion verdict or a code-change plan.
