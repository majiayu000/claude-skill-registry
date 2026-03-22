---
name: idea-scan
description: Analyze standing-intelligence pack diffs and produce scan-proposals.md for IDEAS-02 backlog updates.
---

# Scan Proposals from Pack Diffs

Analyze Layer A standing-intelligence packs for one business and produce proposal-level backlog updates for IDEAS-02.

## Operating Mode

**DIFF SCAN + PROPOSAL OUTPUT (NO BACKLOG MUTATION)**

**Allowed:**
- Read `docs/business-os/strategy/<BIZ>/idea-backlog.user.md` and its `last_scanned_pack_versions` frontmatter.
- Read current Layer A aggregate packs (`MARKET-11`, `SELL-07`, `PRODUCTS-07`, `LOGISTICS-07` when applicable).
- Compare changed pack evidence against the existing idea backlog.
- Write `docs/business-os/strategy/<BIZ>/scan-proposals.md` following the schema contract.
- Return a concise operator summary (changed packs + proposal counts by type).

**Not allowed:**
- Modifying existing cards or ideas/backlog entries.
- Creating cards directly (route accepted proposals through `/lp-do-ideas` in IDEAS-02).
- Writing legacy `docs/business-os/scans/` artifacts.
- Auto-applying `MERGE` or `SPLIT` decisions (operator confirmation is required in IDEAS-02).

## Inputs

**Required:**
- Business code `<BIZ>`
- Backlog baseline: `docs/business-os/strategy/<BIZ>/idea-backlog.user.md`

**Optional:**
- Explicit source diff artifact path (operator-provided)
- Pack scope override (subset of `MARKET-11`, `SELL-07`, `PRODUCTS-07`, `LOGISTICS-07`)
- Run mode: `incremental` (default) or `first-run`

### First-run fallback

If `last_scanned_pack_versions` is missing in the backlog frontmatter, treat the run as first-run:
- Scan all available supported packs in full.
- Emit proposals against the current backlog baseline.
- Do not assume historical scan state from git history.

## Output Contract

Primary output artifact:

```text
docs/business-os/strategy/<BIZ>/scan-proposals.md
```

Schema contract (authoritative):

```text
docs/business-os/startup-loop/ideas/scan-proposals.schema.md
```

Proposal impact types (required enum):

```text
CREATE | STRENGTHEN | WEAKEN | INVALIDATE | MERGE | SPLIT
```

Each proposal must include:
- `type`
- `evidence_ref`
- `reasoning`
- `confidence` (`low|medium|high`)

Conditional fields:
- `idea_id` required for all non-`CREATE` proposals
- `merge_target` required for `MERGE`
- `split_from` required for `SPLIT`

## Workflow

### 1. Load baseline backlog

- Read `idea-backlog.user.md` for the business.
- Parse:
  - Current idea rows
  - `last_scanned_pack_versions`
  - `Review-trigger` context if present

Fail closed if the backlog artifact is missing or unreadable.

### 2. Resolve source packs and changed scope

Determine pack inputs from supported sources:
- `MARKET-11`
- `SELL-07`
- `PRODUCTS-07`
- `LOGISTICS-07` (only when relevant and present)

Incremental mode:
- Compare pack version/date markers against `last_scanned_pack_versions`.
- Only analyze packs with detected deltas.

First-run mode:
- Analyze all available supported packs.

### 3. Extract evidence chunks

For each changed pack, extract atomic evidence chunks that can support a proposal:
- Demand shift
- Segment fit shift
- Supply/logistics constraint shift
- Channel performance shift
- Duplicate/overlapping hypothesis signal

Each chunk must have a traceable `evidence_ref` path/anchor.

### 4. Classify proposals against backlog

Map evidence chunks to one or more proposal types:
- `CREATE` when evidence introduces a new viable hypothesis not represented in backlog
- `STRENGTHEN` when evidence materially increases confidence in an existing idea
- `WEAKEN` when evidence materially decreases confidence
- `INVALIDATE` when assumptions are contradicted
- `MERGE` when two ideas are substantively duplicate and should unify
- `SPLIT` when one idea represents multiple distinct hypotheses

### 5. Apply quality bar

Reject proposals that lack any of:
- `evidence_ref`
- `reasoning`
- `confidence`

Reject invalid conditional-field combinations (for example `MERGE` without `merge_target`).

### 6. Write `scan-proposals.md`

Create/update `docs/business-os/strategy/<BIZ>/scan-proposals.md` with:
- Frontmatter fields from schema contract
- Proposal table/list with all required columns
- Accurate `Proposal-count`

### 7. Return operator summary

Return:
- Packs analyzed
- Proposals emitted by type
- Whether run was `incremental` or `first-run`
- Explicit handoff instruction: proceed to IDEAS-02 backlog update

## Integration with Other Skills

- **IDEAS-01:** `/idea-scan` produces `scan-proposals.md` only.
- **IDEAS-02:** `/lp-do-ideas` applies accepted proposal routing and emits downstream dispatch packets.
- **IDEAS-03:** `/lp-do-fact-find` starts the selected promoted idea as DO work.
- **Plan updates:** `/biz-update-plan` can consume accepted proposal outcomes plus reflection evidence.

## Validation Checklist

Before finishing, verify:
- `scan-proposals.md` exists at business strategy path.
- `Proposal-count` matches emitted proposal rows.
- Every proposal includes `evidence_ref`, `reasoning`, and `confidence`.
- No legacy `docs/business-os/scans/` paths are produced.

## Error Handling

- **Missing backlog artifact:** Fail closed and request `idea-backlog.user.md` creation/repair.
- **No changed packs in incremental mode:** Emit a valid artifact with `Proposal-count: 0` and note "no qualifying deltas".
- **Missing optional pack (for example LOGISTICS-07):** Continue with available packs; do not fail.
- **Malformed proposal rows:** Drop invalid row, log reason, continue if at least one valid proposal remains.

## Legacy Contract Deprecation

The old scan artifact set is deprecated for IDEAS pipeline work and must not be recreated:
- `docs/business-os/scans/last-scan.json`
- `docs/business-os/scans/active-docs.json`
- `docs/business-os/scans/history/*`

Canonical IDEAS-01 output is now only:
- `docs/business-os/strategy/<BIZ>/scan-proposals.md`

## Example Session

```text
User: /idea-scan --business BRIK

Agent:
Running IDEAS-01 pack diff scan for BRIK.

Baseline:
- Backlog: docs/business-os/strategy/BRIK/idea-backlog.user.md
- Mode: incremental

Changed packs detected:
- MARKET-11 (updated 2026-02-22)
- SELL-07 (updated 2026-02-22)

Generated proposals:
- CREATE: 1
- STRENGTHEN: 2
- WEAKEN: 1
- INVALIDATE: 0
- MERGE: 1
- SPLIT: 0

Output:
- docs/business-os/strategy/BRIK/scan-proposals.md

Next step:
- Run IDEAS-02 backlog update to apply accepted proposals.
```

## Success Metrics

- Proposal artifact validity: 100% schema-compliant rows
- Proposal usefulness: >=70% accepted in IDEAS-02 reviews
- Operator review friction: MERGE/SPLIT disagreements tracked and reduced over time
