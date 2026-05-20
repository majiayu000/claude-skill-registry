---
name: refactor-structural-duplication
license: MIT
description: >
  Identify structurally duplicate logic (pipeline-spine duplication) across semantically distinct modules.
  Use when multiple implementations share the same orchestration skeleton (e.g., bounds→shape→chunking→reduction→wrap),
  and unification may require subtle abstraction. Produces a duplication map and a safe extraction/refactor plan.
metadata:
  author: Jordan Godau
  references:
    - 01_INTENT.md
    - 02_DEFINTIONS.md
    - 03_PROCEDURE.md
    - 04_REFACTOR_PLAN_TEMPLATE.md
    - 05_OUTPUT_TEMPLATE.md
  keywords:
    - duplication
    - structural
    - pipeline
    - spine
    - extraction
    - abstraction
    - unification
    - drift
---

# Instructions

Read all references in `references/` before starting.

## Goal

Detect and report **structural duplication** across modules (not copy/paste), especially where:

- different domain concepts remain correctly separate, but
- the underlying processing pipeline is parallel/duplicated, risking drift.

When unification likely requires **subtle abstraction**, produce a **staged plan** that can be executed safely.

## Scope

- This skill **does not** enforce “thin public facades” or restructure public APIs.
- This skill **does** identify shared pipeline spines and propose extraction targets and abstraction seams.

## Signals

Activate when any of the following are true:

- Multiple modules implement similar orchestration stages (even with different operators).
- There are parallel implementations of structurally similar functionality in the codebase.
- The agent (or a developer) is about to re-implement “the same infrastructure again” for a new product.

## Procedure

Follow `references/03_PROCEDURE.md`.

## Output

Produce a single Markdown report using `references/05_OUTPUT_TEMPLATE.md`.
If abstraction is needed, include a staged plan using `references/04_REFACTOR_PLAN_TEMPLATE.md`.
