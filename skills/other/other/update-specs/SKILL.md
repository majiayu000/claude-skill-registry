---
name: update-specs
description: Add or update functional specification documents. Use when user says "update specs", "update specifications", "sync specs", or wants to maintain specification documents that describe what the software must do.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo 'Updating project specifications...'"
          once: true
---

# Update Specifications

Add or update functional specification documents that describe what the software must do. Specifications are implementation-agnostic requirements. From these documents alone, a team could recreate the software in any language or framework without access to the current codebase.

## Scope

Specification files live in a dedicated directory (e.g., `docs/specs/`). Each file covers a component or functional area. If the user specifies a component, only update that file. Otherwise update all spec files.

## Core Rules

- **Append and update only.** NEVER remove a specification. Specs are a living record.
- **Mark, don't delete.** If a specification no longer appears to match observed software behavior, set its status to `Warning` with a brief reason. Humans decide removal.
- **No implementation details.** No language, framework, library, file path, class name, function name, data structure, or internal architecture belongs in a spec. Describe observable behavior and contracts between components.
- **No code, pseudocode, or structural examples.**
- **Each spec is one testable requirement.** If you cannot verify whether the software satisfies a spec through its external behavior or documented contracts, it is too vague. If a spec uses "and" to join two distinct behaviors, split it.
- **Be concise.** A spec should rarely exceed two sentences. State the requirement directly.
- **Describe what, never how.** Say what outcome the system must produce, not what mechanism achieves it.

## Spec File Format

```
# [Component] Specifications

## [Functional Area]

### SPEC-[NNN]: [Short Title]
**Status**: Active | Warning
**Warning**: [reason this spec may no longer apply - only present when status is Warning]

[Single requirement statement in plain prose. No bullets, sub-items, or conditional trees.]
```

Rules:
- Numbers are sequential per file starting at SPEC-001
- Functional areas group related requirements under a shared heading
- New specs append to the end of their functional area
- New functional areas append after existing ones
- A spec's number never changes, even if specs above it receive warnings

## Workflow

### 1. Explore Current Behavior

Launch parallel Explore subagents to understand what the software currently does. Focus on observable behavior and contracts, not implementation structure.

Investigate: How components communicate, what data flows between them, what persistence guarantees exist, what the interface exposes to users, what invariants hold across the system, how errors propagate across boundaries.

### 2. Read Existing Specs

Read all existing spec files. Note every current spec number, status, and functional area. If a file does not exist, it will be created.

### 3. Compare Behavior to Specs

For each existing spec:
- Verify it still accurately describes the software. If not, set status to `Warning` with a reason.
- If accurate but the wording is incomplete or imprecise, update the requirement text.

For each observed behavior not yet covered by a spec:
- Draft a new spec with the next sequential number under the appropriate functional area.

### 4. Write Updates

- Create or update spec files.
- Preserve every existing spec. Only modify status or requirement text, never delete entries.
- New specs go at the end of their functional area.
- When creating a file for the first time, include all discovered specs organized by functional area.

### 5. Validate All Specs

After writing updates, launch one Explore subagent per spec file. Each subagent independently validates every spec in its assigned file against the actual codebase.

For each spec the subagent must determine:
- Whether the described behavior exists in the software
- Whether the spec accurately reflects that behavior as implemented

The subagent returns a list of spec numbers with a verdict: **confirmed** (behavior matches), **warning** (behavior missing, changed, or ambiguous), or **unchanged** (status already correct).

### 6. Apply Validation Results

Using the subagent findings from step 5:
- Set any spec marked **warning** to `Status: Warning` with the reason the subagent identified.
- Restore any previously warned spec marked **confirmed** back to `Status: Active` and remove the Warning line.
- Leave **unchanged** specs untouched.

This is the final write pass. No further exploration or spec additions happen after validation.

## Constraints

- NEVER modify source code, tests, or any file outside the specs directory.
- NEVER write specs about internal architecture, module layout, or code organization. Only specify behavior visible at component boundaries.
- ALWAYS explore the codebase before writing. Do not write specs from memory or assumptions.
- ALWAYS read existing spec files before making changes. Do not create duplicate specs.
- ALWAYS use the sequential numbering scheme. Never skip or reuse numbers.
