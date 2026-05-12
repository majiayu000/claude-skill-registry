---
name: ln-311-review-research-worker
description: "Use when an evaluation run needs mandatory official-doc, MCP Ref, Context7, and current best-practice research with a structured research summary."
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

**Type:** L3 Worker
**Category:** 3XX Planning

# Review Research Worker

Structured research worker for validation, audit, and review flows.

## Mandatory Read

**MANDATORY READ:** Load `references/evaluation_worker_runtime_contract.md`, `references/evaluation_summary_contract.md`, `references/evaluation_research_contract.md`, `references/epistemic_protocol.md`
**MANDATORY READ:** Load `references/researchgraph_mcp_usage.md` only when the review target explicitly cites `H##`, `G##`, benchmark run IDs, or researchgraph files.

## Purpose

- gather official documentation or standards
- gather MCP Ref evidence
- gather Context7 evidence when a library or framework is involved
- gather current web best-practice evidence
- emit a compact machine-readable research summary instead of prose-only notes

## Runtime

Runtime family:
- `evaluation-worker-runtime`

Required manifest fields:
- `identifier`
- `phase_order`
- `summary_kind=review-research`
- `operation=research`

Recommended `phase_order`:
1. `PHASE_0_CONFIG`
2. `PHASE_1_RESOLVE_STACK`
3. `PHASE_2_OFFICIAL_DOCS`
4. `PHASE_3_MCP_REF`
5. `PHASE_4_CONTEXT7`
6. `PHASE_5_WEB_BEST_PRACTICES`
7. `PHASE_6_ANTI_HALLUCINATION`
8. `PHASE_7_WRITE_SUMMARY`
9. `PHASE_8_SELF_CHECK`

## Workflow

### Phase 0: Config

1. Load runtime manifest.
2. Resolve review target, stack hints, and output location.
3. Fail if target context is missing.

### Phase 1: Resolve Stack

1. Detect language, framework, libraries, and domain.
2. Build a bounded research topic list.
3. Keep topic count small and evidence-oriented.
4. If the target explicitly cites local H/G/run IDs, do a read-only researchgraph preflight to capture local context before external research. Do not replace official-doc, MCP Ref, Context7, or current-web lanes with local graph evidence.

### Phase 2: Official Docs

1. Read official docs or standards first.
2. Record source URLs and the exact topic each source supports.

### Phase 3: MCP Ref

1. Query MCP Ref for the same bounded topics.
2. Prefer primary documentation over tertiary commentary.

### Phase 4: Context7

1. If a library or framework is involved, resolve the Context7 library id.
2. Query only the libraries actually used by the target.
3. If no relevant library exists, record that explicitly.

### Phase 5: Web Best Practices

1. Perform current web research for best practices and recent changes.
2. Use current sources, not frozen heuristics.
3. Record only evidence that changes a conclusion or adds decision value.

### Phase 6: Anti-Hallucination Verification

1. Scan target artifact for factual claims across all trigger categories per `epistemic_protocol.md` Section B.
2. For each claim, check against research evidence gathered in Phases 2-5:
   - Has MCP Ref/Context7/Web evidence → mark `VERIFIED`
   - No tool evidence but claim is plausible → mark `FROM_TRAINING`
   - Contradicts tool evidence → mark `FLAGGED` (CRITICAL)
3. This step verifies against existing research. It does NOT run new searches.
4. Include verification status in summary metadata.

### Phase 7: Write Summary

Emit `summary_kind=review-research`.

Payload must include:
- `worker=ln-311`
- `status`
- `operation=research`
- `warnings`

Prefer these fields when available:
- `findings`
- `metrics.research_sources`
- `metrics.anti_hallucination_status` (VERIFIED | FLAGGED)
- `metrics.flagged_claims_count`
- `artifact_path`
- `report_path`
- `metadata`

### Phase 8: Self-Check

1. Verify all four research lanes were attempted.
2. Verify anti-hallucination verification was executed.
3. Verify skipped lanes are justified in machine-readable form.
4. Record `pass=true` only after the summary is written.

## Definition of Done

- [ ] Official-doc evidence recorded
- [ ] MCP Ref evidence recorded
- [ ] Context7 evidence recorded or justified as not applicable
- [ ] Current web best-practice evidence recorded
- [ ] Anti-hallucination verification executed (claims marked VERIFIED/FROM_TRAINING/FLAGGED)
- [ ] `review-research` summary written
- [ ] Self-check passed

**Version:** 1.0.0
**Last Updated:** 2026-04-10
