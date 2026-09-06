---
name: reorder
description: 'Use when asked to reorder a drifted listing under one stated principle, moving items only and rewording nothing. Not for deliberately ranked listings: use reorder-respect-deliberate.'
---

# Reorder

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Catalog/index/toc/enum/menu whose order went arbitrary, or user says reorder this / sensible order. |
| Authority | Reversible local: write only the named local artifact; VCS state is the rollback path. |
| Side effect | Repositions items in a listing (and mirrored copies) without content edits. |
| Done | Reader can name the ordering principle; every item still present, kin adjacent. |

## Refusals

- Listings with intentionally ranked items: use `reorder-respect-deliberate`. This skill does not preserve explicit ranks.
- Rewording, adding, or removing content: rejected. Items are moved only.
- **Remote, credential, publish, deploy, or irreversible changes**: rejected.

## Inputs

Only the listing and a stated principle. The listing is either supplied or identified from context. The principle may be named by the user, inferred from the existing sequence, or selected from workflow sequence, dependency order, grouping by kind, severity, frequency, or alphabetical order.

## Procedure

1. Pin the listing. Identify the ordered set in focus. Count the items to establish the full scope before any mutation. **Done when**: the item set is identified and counted.
2. Name one principle. Extract it from user input, the existing sequence, or a stated default. State it explicitly before the first move. **Done when**: the principle is stated.
3. Verify scope. Confirm every item in the listing belongs in this scope. Note any mirrored copies that must carry the identical order. **Done when**: scope membership and mirrors are confirmed.
4. Cluster kin, then sequence. Keep related items adjacent, then order the clusters by the stated principle. Maintain intra-cluster order. Do not blend incompatible sorts. **Done when**: kin are adjacent and clusters are ordered by the principle.
5. Move in place. Reposition items without rewording, adding, or removing any content. Do not rephrase labels, descriptions, or metadata. If the same set is mirrored elsewhere, apply the identical order to each. **Done when**: all items and mirrors are repositioned.
6. No-op pass. A pass that finds nothing to improve changes nothing. **Done when**: the pass is complete, whether or not changes were made.

## Failure and recovery

- Ambiguous scope: the listing boundaries or item set are unclear. Stop and ask the user to identify or supply the exact target.
- Mixed item types: the set contains items that do not share a common ordering principle. Stop and ask which subset to reorder, or which principle to apply.
- Principle unknown: surface the best guess and wait for explicit confirmation before proceeding.
- Partial fit: if the stated principle fits some items but not all, sequence the compatible subset and note the remainder as out-of-scope.

Rollback: if a reposition corrupts or loses content, restore from VCS. This authority is reversible-local; the working tree is the only mutation surface.

## Output

A repositioned listing where the reader can name the ordering principle, every item is still present, kin are adjacent, and mirrored copies carry the identical order, or the original unchanged if nothing needed reordering.
