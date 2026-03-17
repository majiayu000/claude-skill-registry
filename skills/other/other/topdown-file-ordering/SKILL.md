---
name: topdown-file-ordering
description: "Use when block order in a single file obscures the public surface or disrupts top-down comprehension. Goal: file structure exposes the public surface first and supporting details in a clear top-down flow without behavior change."
---

# Single-File Top-Down Ordering

Reorder blocks inside one file to make the public surface readable first, then unfold supporting details.

## Response Contract

- Deliverable: apply the requested changes to the target artifact.
- Chat output: no additional output beyond the deliverable.

## Ordering Model

### Block Scope

A **block** is a structural declaration unit, such as a public or exported declaration, class, function or method, and relevant type declarations.

### Dependency-After

Dependency-after is a readability ordering: when one block depends on another block in the same file, place the depended-on block later so supporting definitions appear after the behavior that uses them.

## Standards

Apply these standards throughout the edit. Each standard is single-sourced here and referenced elsewhere by its ID.

- **safety.semantics_preserve — Preserve semantics**
  Reorder only when language semantics remain correct.

- **ordering.public_first — Public surface first**
  Place public-facing blocks earlier in the file.

- **ordering.dependency_after — Dependency-after**
  For same-file blocks: if A depends on B, place A before B when a valid order exists.

- **cycles.group — Cycles as a group**
  If blocks form a dependency cycle, treat the cycle as a single group for placement.

## Workflow

1. Move public-facing blocks earlier. Apply `ordering.public_first`.
2. Order public-facing blocks:

   - If one depends on another, place the dependent earlier. Apply `ordering.dependency_after`.
   - Otherwise keep original relative order.
3. Layer supporting blocks until no new blocks are found:

   - Scan the current layer in order and collect same-file block dependencies in this order:

     1. signature and type-position references
     2. implementation and body references
   - Exclude blocks already placed and anything out of scope.
   - The newly discovered blocks form the next layer in first-encounter order across the scan.
   - If the next layer contains cycles, treat each cycle as a group and keep original relative order within the group. Apply `cycles.group`.
   - Append the next layer after the current layer and repeat.
4. Validate safety and revert any move that would violate semantics. Apply `safety.semantics_preserve`.

## Acceptance Criteria

A revision is complete only if all checks pass.

- **Response**: Output satisfies the Response Contract.
- **Standards satisfied**: `safety.semantics_preserve`, `ordering.public_first`, `ordering.dependency_after`, `cycles.group`.
