---
name: template-sync-check
description: Verify that all 4 Convex template locations are in sync (CLAUDE.md Rule 6)
user-invocable: false
---

You are checking that the 4 required Convex template locations are identical, as required by CLAUDE.md Rule 6.

The 4 locations that must stay in sync:
1. `packages/cli/templates/default/convex/` — CANONICAL SOURCE
2. `packages/cli/dist/default/convex/`
3. `templates/default/convex/`
4. `convex/`

Follow these steps:

**Step 1: List files in all 4 directories**

Compare the file listings across all locations. Note any files present in some locations but missing in others.

**Step 2: Diff files that exist in all locations**

For each file in the canonical source (`packages/cli/templates/default/convex/`), diff it against the other 3 copies. Flag any content differences.

**Step 3: Fix drift if found**

If any differences are detected (missing files or content drift), run:
```
pnpm sync-templates
```

Then re-run the diffs to confirm all 4 locations are now identical.

**Step 4: Report findings**

Report clearly:
- Whether all 4 locations were already in sync
- Which files (if any) had drift and between which locations
- Whether `pnpm sync-templates` was run and whether it resolved the drift
- Any files that could not be reconciled automatically
