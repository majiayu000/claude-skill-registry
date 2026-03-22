---
name: "nesting-orientation-review-gate"
description: "How to gate orientation-preference changes in the nesting heuristic without losing fit behavior or determinism"
domain: "testing"
confidence: "medium"
source: "earned"
---

## Context

Use this when a nesting or packing heuristic changes orientation preference, tie-break ordering, or rotation defaults.

## Pattern

1. Separate the **preference** case from the **necessity** case.
   - Preference: both orientations fit, but one orientation should now win.
   - Necessity: only rotation fits, so rotation must still happen.

2. Prove the rule on the real service path.
   - Assert actual placement geometry and `Rotated90`, not just a helper-level fit decision.

3. Add a preserved-rotation counterexample.
   - Show a case where the old rotate-to-fit behavior still works after the preference change.

4. Re-run the same request twice and compare placement order, coordinates, dimensions, and rotation flags.
   - Orientation tie-break changes can silently break determinism even when utilization stays the same.

5. Keep one no-fit regression check.
   - Preference changes must not rewrite impossible parts into misleading reason codes.

6. Prefer a narrow priority key over a heuristic rewrite.
   - If one explainability rule should outrank the existing orientation order only in a special case, add a dedicated leading sort key for that case and leave the rest of the ordering intact.
   - This keeps the change deterministic and prevents unrelated panels from inheriting a new rotation policy.

## Anti-Patterns

- Approving the slice because a single happy-path panel no longer rotates
- Asserting only `Success`/`Fits` without checking `Rotated90`
- Treating a tie-break tweak as low-risk without a repeat-run determinism check
