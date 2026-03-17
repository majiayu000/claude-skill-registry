---
name: mitm
description: Track and summarize man-in-the-middle mentions across local corpora and history; use for MITM audits, searches, and reporting.
---

# MITM Audit Skill

Use this skill to report MITM mentions across local history and corpora and to keep a snapshot of hit lists.

## When to use
- The user asks for MITM mention counts or audits.
- The user asks to refresh or summarize MITM hit lists.

## Stored references
- references/mitm_tally.md
- references/mitm_history_lines.txt
- references/mitm_ies_docs_hits.txt
- references/mitm_ies_code_hits.txt
- references/mitm_codex_hits.txt
- references/mitm_codex_code_hits.txt
- references/mitm_topos_hits.txt
- references/mitm_topos_code_hits.txt

## Workflow
1) Start with the latest tally in references/mitm_tally.md.
2) Use the hit list files to locate file paths and line numbers when the user asks for detail.
3) If asked to refresh, regenerate the hit lists and update references/mitm_tally.md and the list files.

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 7. Propagators

**Concepts**: propagator, cell, constraint, bidirectional, TMS

### GF(3) Balanced Triad

```
mitm (○) + SDF.Ch7 (○) + [balancer] (○) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)


### Connection Pattern

Propagators flow constraints bidirectionally. This skill propagates information.
