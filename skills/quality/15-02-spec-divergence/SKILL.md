---
name: 15-02-spec-divergence
description: Audit divergence between specs and codebase, classify discrepancies, and resolve them.
---

# 15.02 Spec Divergence Audit

## Instructions

Use subtask agents to explore the current state of divergence between spec and codebase.

For each feature area with specs:
1. Read the spec's behavior/contract/scenarios sections.
2. Read the corresponding code.
3. Report divergences: spec says X but code does Y.
4. Classify each: spec is stale, code is wrong, or intentional undocumented change.

Update specs or code to resolve divergences. Log changes via `tinychange`.
