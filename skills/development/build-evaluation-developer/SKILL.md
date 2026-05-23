---
name: build-evaluation-developer
description: Guidelines for safely understanding, modifying, and extending the weapon build optimization evaluator
---

# Build Evaluation Developer Skill

Use this skill when modifying the weapon build evaluation logic in `internal/evaluator/`.

The evaluator is a high-performance DFS engine. Incorrect modifications can lead to exponential search times or suboptimal builds.

---

## Scope & Intent

Use this skill when:
- Modifying the DFS algorithm in `processSlots`
- Adding new optimization metrics (e.g. Weight, Price)
- Adjusting pruning or bounding logic
- Debugging why a "best build" isn't actually optimal

---

## Safety & Performance Invariants

1.  **Limited Run Scope**: 
    - **Full Runs**: Do NOT trigger a full evaluator run (`task evaluator:start`) unless explicitly requested. 
    - **Test Mode**: You MAY use `task evaluator:start:test-mode` for smoke tests. It uses a restricted subset of weapons and trader levels.
    - **Focused Testing**: Prefer unit tests, benchmarks, or integration tests targeting specific weapons.
2.  **Thread Safety**: `processSlots` runs in parallel worker pools. **NEVER** use global variables or mutate shared structures (like the `CandidateTree` items) during the search.
3.  **Pre-Evaluation Setup**: Before calling `FindBestBuild`, you MUST ensure the tree is initialized:
    ```go
    weapon.UpdateAllowedItems()
    weapon.UpdateAllowedItemSlots()
    ```
4.  **Branch-Local Exclusions**: `excludedItems` must be cloned (`helpers.CloneMap`) when descending into a branch where a new conflict is introduced.

---

## Algorithm Logic: `processSlots`

### Conflict Enforcement
Conflicts are enforced by the `excludedItems` map. 
- **Rule**: If an item is in `excludedItems`, it cannot be chosen for the current slot.
- **Rule**: If an item is chosen, all its `ConflictingItems` must be added to the exclusion map for all subsequent descendants and siblings in that branch.

### Tie-Breaking (`doesImproveStats`)
When comparing builds, we use primary and secondary stats:
- **Recoil Focus**: Primary is `RecoilSum` (lower is better). Tie-breaker is `ErgonomicsSum` (higher is better).
- **Ergo Focus**: Primary is `ErgonomicsSum` (higher is better). Tie-breaker is `RecoilSum` (lower is better).

---

## Pruning & Bounding

Pruning skips branches that cannot mathematically beat the current `best` build.

### Bounding Functions
- `computeRecoilLowerBound`: Sum of current recoil + minimum possible recoil from all remaining slots.
- `computeErgoUpperBound`: Sum of current ergonomics + maximum possible ergonomics from all remaining slots.

### Pruning Locations
1.  **Item Selection**: Before evaluating an item in a slot.
2.  **Empty Slot**: Before evaluating the outcome of leaving a slot empty.

---

## Caching Logic (`Cache` interface)

Caching uses memoization of "conflict-free" subtrees to avoid redundant DFS traversals.

### The "Conflict-Free" Invariant
- An item is only cacheable if it has **zero** `ConflictingItems`. 
- If an item has conflicts, its optimal subtree depends on which exclusions are active, making simple ID-based caching unsafe.

### Clean Contribution
The cache stores the **relative** contribution of a subtree, not the absolute total. This allows the same cached result to be added to different parent builds.

---

## How to Modify: Developer Checklist

When adding a new stat (e.g., `Weight`):

1.  **Update Models**: Add the stat to `Build`, `ItemEvaluation`, and `OptimalItem` in `evaluator.go`.
2.  **Implement Bounding**: Create `compute[Stat]LowerBound` or `compute[Stat]UpperBound`.
3.  **Update Comparison**: Modify `doesImproveStats` to include the new stat in the priority chain.
4.  **Integrate Pruning**: Call your new bounding function in `processSlots`.
5.  **Update Caching**: Ensure the new stat is captured in `CacheEntry` and the `Cache` implementation.
6.  **Verify**:
    - Run `go test ./internal/evaluator/ -run TestCache` to check cache correctness.
    - Run `go test ./internal/evaluator/ -bench=. -benchmem` to check for performance regressions.
