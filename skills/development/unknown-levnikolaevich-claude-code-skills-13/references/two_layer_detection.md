<!-- SOURCE-OF-TRUTH: shared/references/two_layer_detection.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Two-Layer Detection

Audit workers use two-layer detection to avoid noisy grep-only reports.

## Layer 1: Candidate Scan

Find possible issues with the cheapest reliable source:
- text search for known signatures
- project tools such as linters, type checks, dependency scanners, or audit commands
- `hex-graph audit_workspace` for structural clone/duplication candidates when indexed and relevant

Layer 1 output is only a candidate list. A candidate is not a finding until verified.

## Layer 2: Context Verification

For each material candidate:
1. Read enough surrounding code to understand scope, data flow, ownership, and lifecycle.
2. Apply the worker's domain questions and false-positive filters.
3. Classify as `confirmed`, `false_positive`, or `needs_context`.
4. Report only confirmed findings, plus `needs_context` as low-severity notes when useful.

Layer 2 is mandatory when the finding depends on scope, architecture, concurrency, lifecycle, cross-process behavior, or any pattern with high false-positive risk. It is optional for unambiguous tool findings that already include structured severity and location.

## Finding Standard

Every reported issue needs:
- precise location
- why the issue is real in context
- severity and effort
- recommendation
- evidence basis when consumed by a coordinator

---
**Version:** 1.0.0
**Last Updated:** 2026-03-04
