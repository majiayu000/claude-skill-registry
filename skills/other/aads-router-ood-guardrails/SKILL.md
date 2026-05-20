---
name: aads-router-ood-guardrails
description: Handle router, ROI, policy-taxonomy, and OOD updates in AADS-ULoRA while preserving stage-order behavior and Phase 5 latency guardrails. Use for changes under src/router, src/ood, policy regression scripts, or phase5 performance guardrail scripts and config.
---

# AADS Router and OOD Guardrails

## Workflow

1. Scope behavior impact.
- Classify change as routing logic, taxonomy/policy behavior, OOD behavior, or performance.
- Load `references/router-guardrails.md`.

2. Preserve invariants.
- Preserve stage ordering unless explicitly requested.
- Preserve focus-mode fallback semantics.
- Preserve taxonomy normalization semantics.

3. Implement with minimal churn.
- Touch only required router/OOD files.

4. Run required validation.
- Router unit tests, OOD tests, and policy regression bundle.
- Add profile sanity checks for policy profile changes.

5. Run performance gates when runtime path changed.
- Benchmark and guardrail checker.

6. Emit behavior delta summary.
- Explicitly classify changes as breaking or non-breaking.

## Output Contract

Return sections in this order:
1. Changed router/OOD surfaces
2. Invariants checked
3. Validation commands and results
4. Performance gate results (or skip reason)
5. Breaking/non-breaking classification
6. Residual risk notes

## References

- Read `references/router-guardrails.md` for invariants and command matrix.
