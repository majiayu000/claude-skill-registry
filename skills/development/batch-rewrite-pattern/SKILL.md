---
name: batch-rewrite-pattern
description: "Cascade the same edit pattern across N files safely. Use when applying the same refactor to multiple files (e.g. swap import paths across 11 scripts, rename a symbol, migrate a call signature). Detects the common-shape-across-files situation and turns an N-file cascade into a planned audit → apply → verify workflow instead of N sequential manual edits."
format: 2025-10-02
version: 1.0.0
status: active
updated: 2026-04-17
---

# Batch Rewrite Pattern

When the same edit needs to land in N files, the worst shape is N sequential
manual passes. Each pass collects its own errors; the hook system retriggers;
context fills with repetitive diffs. This skill captures the better shape.

## Triggers

Activate when any of these apply:

- Renaming a symbol across the tree
- Migrating a function signature (add/remove/reorder args)
- Swapping an import path across modules
- Converting between two patterns (callbacks ↔ promises, v1 ↔ v2 API)
- Any edit where you can describe the transformation as "in every file
  matching pattern X, replace Y with Z"

Typical count trigger: **≥ 4 files** warrant the batch shape.

## Workflow

1. **Characterize the transformation** in one paragraph:
   - What's the before pattern? (regex or literal)
   - What's the after pattern?
   - Are there variants? (single pattern vs family of patterns)
   - Any files that should be exempt?

2. **Enumerate candidates** with Grep/Glob:
   ```
   Grep pattern=BEFORE output=files_with_matches
   ```

3. **Dry-run the rewrite** against 1-2 candidates first. Verify:
   - The transformation is correct
   - Surrounding context isn't disturbed
   - No collateral damage

4. **Apply in a batch** — prefer a single Bash `sed`/`perl` invocation or a
   small rewrite script over N sequential Edit calls:
   ```bash
   for f in $(grep -l 'BEFORE' src/**/*.ts); do
     sed -i -e 's/BEFORE/AFTER/g' "$f"
   done
   ```
   Or write a one-shot node script that reads each file, applies the
   transformation, writes back.

5. **Verify with the test suite** if one exists, or with a grep that the
   after-pattern is uniformly present and the before-pattern is gone.

6. **Single commit** covering the whole cascade, scope line listing files.

## Anti-patterns to avoid

- **Sequential manual Edit calls** when the transformation is deterministic.
  Each Edit triggers hook re-reads and bloats context.
- **Partial cascades** — leaving some files on the old pattern because you got
  interrupted halfway. Either all or none; use `git stash` to revert if the
  cascade was wrong.
- **Branching transformations without a plan** — when "most files" follow one
  pattern but a few need a variant, enumerate the variants first and handle
  each as its own batch.

## Example — Config Adapter Cascade (v1.49 release-history work)

Situation: 11 scripts in `tools/release-history/` each had a direct
`pg.Client` instantiation and hardcoded paths. Needed to convert all 11 to use
`loadConfig()` + `openDb(cfg)`.

Right shape:
1. Wrote the adapter (`db.mjs`) once
2. Characterized the transform: replace `new pg.Client({...})` block with
   `await openDb(cfg)`; replace hardcoded paths with `cfg.*_abs`
3. Applied to each file in one Bash loop or parallel sed invocation
4. One commit

Wrong shape (what actually happened): 11 sequential Read-plus-Edit cycles,
35+ read-before-edit hook fires, recursive pattern-matching at each step.

The lesson: when you feel yourself about to do the same edit for the fourth
time, stop and batch the rest.

## Companion Tools

- `Grep` with `output_mode: files_with_matches` to enumerate candidates
- `Bash` with `sed -i` or a small rewrite script for the cascade
- `Grep` again to verify the before-pattern is gone and after-pattern is
  uniformly present

## Related

- `file-operation-patterns` — safe bulk file operations
- `decision-framework-invoker` — use when the batch is irreversible
