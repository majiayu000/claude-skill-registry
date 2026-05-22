---
name: aads-orchestrator
description: Coordinate multi-track AADS-ULoRA work by sequencing triage, architecture decisions, domain implementation tracks, and integration gates. Use when requests span modules, require explicit handoffs, or need dependency-aware validation planning.
---

# AADS Orchestrator

## Workflow

1. Decompose into tracks.
- Split request into independent workstreams.
- Mark dependencies and parallel candidates.

2. Route tracks to skills.
- Status/scope: `aads-status-triage`
- Implementation: `aads-coder`
- Config/pipeline contracts: `aads-config-pipeline-guardrails`
- Router/OOD: `aads-router-ood-guardrails`
- Training: `aads-training-lifecycle`
- Docs/notebooks/scripts sync: `aads-colab-doc-sync`
- Architecture/contracts: `aads-architect`

3. Define checkpoints.
- Add merge checkpoints after each major track.
- Require explicit validation gate per track.
- Attach one owner file list and one owner test list per track.

4. Run integration gates.
- Choose smallest cross-track validation set that proves end-to-end safety.

5. Emit orchestration summary.
- Include track outcomes, unresolved risks, and next actions.

## Output Contract

Return sections in this order:
1. Track breakdown
2. Dependency/order map
3. Validation gates per track
4. Integration checks
5. Final risk register
6. Recommended execution order

## References

- Use `references/orchestration-matrix.md` for routing logic and gate templates.
