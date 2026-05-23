---
name: massive-report-writing
description: |
  Context-efficient report synthesis for large research corpora using evidence ledgering and harness-based iteration.
  
  **USE WHEN:**
  - Corpus has ≥8 files OR ≥100K characters
  - `finalize_research` returns `recommended_mode: EVIDENCE_LEDGER`
  - Prior runs show Write tool failures or truncation warnings
  - Report scope is "comprehensive" or "deep dive"
  
  **THIS SKILL PROVIDES:**
  - Evidence ledger extraction (compresses corpus 70-85%)
  - Harness handoff patterns for multi-iteration synthesis
  - Chunked write sequences for large outputs
---

# Massive Report Writing

## Overview

Use evidence ledgering to compress large research corpora into structured, quotable material. For very large corpora, harness iteration handles multi-pass synthesis automatically.

## When to Use

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Medium corpus | 100-150K chars, 8-15 files | Build evidence ledger, write in one pass |
| Large corpus (harness mode) | >150K chars, >15 files | Ledger → harness restart → write from ledger |
| Large corpus (non-harness) | >150K chars | Suggest user enable harness mode |

---

## Workflow: Evidence Ledger Mode

### 1. Build Evidence Ledger

Call `build_evidence_ledger(session_dir, topic, task_name)` after finalize_research.

The tool extracts from each source:
- Direct quotes with attribution
- Specific numbers (percentages, counts, costs)
- Key dates and timelines
- Claims and findings

**Output:** `tasks/{task_name}/evidence_ledger.md` with EVID-XXX entries.

### 2. Read Only the Ledger

After ledger is built:
- ✅ Read `evidence_ledger.md` for synthesis
- ❌ Do NOT re-read raw corpus files
- ❌ Do NOT use `read_research_files` again

This is how you avoid context exhaustion.

### 3. Write Report from Ledger

Use EVID-XXX references when citing:
```
According to ISW (EVID-003), Russian forces gained 74 square miles...
```

---

## Harness Integration

When corpus exceeds safe limits AND harness mode is active:

1. **Iteration 1:** finalize → build ledger → ledger saved to disk → context exhaustion
2. **Harness restart:** Context cleared, handoff.json injected
3. **Iteration 2:** Read ledger from disk → write report

The harness handles multi-pass automatically. You don't need map-reduce orchestration.

---

## Chunked Write Sequence

Use when single Write calls fail or output is >30KB:

```
1) Write header + CSS + title block
2) Append executive summary
3) Append Section 1 (cite EVID-XXX)
4) Append Section 2
... repeat ...
N) Append references
```

Use `append_to_file` for sections 2-N.

---

## Templates

See [references/massive_report_templates.md](references/massive_report_templates.md) for:
- Evidence ledger entry format
- Section outline template
- Chunked write sequence

---

## Anti-Summary-of-Summary Rule

- Every claim in the final report must trace to an EVID-XXX
- If a point cannot be traced to a ledger item, drop it or re-read the source
- Batch summaries (if used) are navigation only, not source material
