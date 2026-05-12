---
name: ln-313-review-docs-worker
description: "Use when an evaluation run needs review-driven documentation updates and a structured documentation summary."
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

**Type:** L3 Worker
**Category:** 3XX Planning

# Review Docs Worker

## Mandatory Read

**MANDATORY READ:** Load `references/evaluation_worker_runtime_contract.md`, `references/evaluation_summary_contract.md`
**MANDATORY READ:** Load `../ln-310-multi-agent-validator/references/domain_patterns.md`

## Purpose

- create missing review-required docs
- update existing docs with validated changes only
- keep documentation work separate from merge and repair

## Mode Gate

- `mode=story`: full documentation pipeline — domain extraction, pattern detection, doc generation
- `mode=plan_review`: skip unless documentation delta exists; record `docs_skipped_reason`

## Runtime

Runtime family:
- `evaluation-worker-runtime`

Required manifest fields:
- `identifier`
- `phase_order`
- `summary_kind=review-docs`
- `operation=docs`

Recommended `phase_order`:
1. `PHASE_0_CONFIG`
2. `PHASE_1_EXTRACT_DOMAINS`
3. `PHASE_2_PATTERN_DETECTION`
4. `PHASE_3_GENERATE_DOCS`
5. `PHASE_4_LINK_TO_STORY`
6. `PHASE_5_WRITE_SUMMARY`
7. `PHASE_6_SELF_CHECK`

## Workflow

### Phase 1: Extract Domains

1. Extract technical domains from Story title + Technical Notes + Implementation Tasks.
2. Build a bounded list of documentation topics.

### Phase 2: Pattern Detection

1. Load pattern registry from `domain_patterns.md`.
2. Scan Story content for pattern matches via keyword detection.
3. If multiple patterns detected, create ALL applicable docs.

### Phase 3: Generate Docs

For each detected pattern:
1. Check if document already exists at expected output path (glob `docs/{type}s/*{pattern}*.md`).
2. If missing: load template from `references/templates/` (`adr_template.md`, `guide_template.md`, `manual_template.md`).
3. Research pattern topic using available MCP tools per research methodology.
4. For ADR patterns: answer 5 ADR questions internally before generation (Context, Decision, Consequences, Alternatives, Status).
5. Generate document. Rules: NO CODE in generated docs, tables preferred over prose, 300-500 words target.
6. Save to `docs/{type}s/{naming}.md`.

### Phase 4: Link to Story

1. Add created doc links to Story Technical Notes.
2. Update runtime state with `docs_checkpoint`.

### Phase 5: Write Summary

Emit `summary_kind=review-docs`.

Payload must include:
- `worker=ln-313`
- `status`
- `operation=docs`
- `warnings`

Prefer these fields when available:
- `docs_created` (list of paths)
- `docs_updated` (list of paths)
- `docs_skipped_reason` (when applicable)
- `patterns_detected` (list of matched patterns)

### Phase 6: Self-Check

Fallback: if no pattern matched but technical aspect is missing documentation, use MCP Ref fallback per `domain_patterns.md` Fallback Strategy.

## Definition of Done

- [ ] Documentation targets resolved
- [ ] Pattern detection executed against `domain_patterns.md`
- [ ] Documentation changes applied or justified as skipped
- [ ] `review-docs` summary written
- [ ] Self-check passed

**Version:** 1.0.0
**Last Updated:** 2026-04-10
