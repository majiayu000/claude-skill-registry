---
name: output-style-governance
description: Validate and govern output-style manifests under output-styles in the user workspace.
allowed-tools:
  - Read
---

## Purpose

Validate output-style manifests so that preferred output styles selected via `/output-style` remain consistent with `rules/98-output-styles.md` and `rules/98-communication-protocol.md`.
Ensure each style manifest has correct frontmatter, clearly documented behavior, and does not weaken protocol invariants around safety, correctness, or structure.

## IO Semantics

Input: Output-style manifest files under `output-styles/*.md` in the user workspace.
Output: Governance findings and suggested fixes for style manifests (for example, missing fields, protocol violations, or unclear behavior descriptions).
Side Effects: None directly; orchestration commands such as `/llm-governance` handle backups and writeback when applying suggested fixes.

## Deterministic Steps
### 1. Target Discovery

- Locate output-style manifests in:
  - `output-styles/*.md` when running inside the user workspace (`~/.claude`)

### 2. Frontmatter Validation

- Check that each manifest contains:
  - `name`: non-empty, lowercase identifier without spaces.
  - `description`: concise human-readable description of the style.
  - `keep-coding-instructions`: boolean flag.
- Flag manifests that:
  - Omit required fields.
  - Use identifiers that conflict with existing core styles or are ambiguous.

### 3. Protocol and Rule Compliance

- Scan manifest bodies for instructions that conflict with:
  - Absolute prohibitions in `rules/98-communication-protocol.md` (for example, emotional language or small talk if disallowed).
  - Invariants and constraints in `rules/98-output-styles.md` (for example, attempts to weaken safety or encourage vague answers).
- Verify that manifests explicitly treat style instructions as additive to protocol invariants rather than replacements.
- Flag any instructions that attempt to override or ignore protocol prohibitions.

### 4. Style Behavior Clarity

- Check that each style manifest:
  - States whether it builds on a core style (for example, default, explanatory, learning) or defines a new core style.
  - Describes typical interaction patterns (for example, concise coding, explanatory insights, teaching interactions).
  - Avoids unnecessary narrative unrelated to style behavior.
- Recommend improvements where style behavior is ambiguous or underspecified.

### 5. Integration with Governance Workflows

- When invoked by `agent:llm-governance` or `/llm-governance`:
  - Provide a structured list of findings per manifest (missing fields, violations, ambiguities).
  - Suggest minimal, deterministic edits that bring manifests into compliance with `rules/98-output-styles.md` and protocol rules.

## Validation Criteria

- All governed manifests include valid `name`, `description`, and `keep-coding-instructions` fields.
- No manifest contains instructions that contradict `rules/98-communication-protocol.md` or `rules/98-output-styles.md`.
- Core styles (default, explanatory, learning) are present and consistent with their rule definitions when used.
- Extended styles document their relationship to core styles and keep technical behavior aligned with protocol invariants.