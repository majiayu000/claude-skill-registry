---
name: esper:sync
description: Update spec files to match shipped implementation. Records sync notes in the increment and finishes it when complete.
---

You are synchronizing the spec tree with the shipped implementation.

## Step 1: Read context

Run `esperkit context get` to determine the current state.

If no active increment, tell the user: "No active increment to sync. Run `esper:atom` first." and stop.

## Step 2: Read the increment and specs

Read the active increment file from `.esper/increments/active/<filename>`.
Read the referenced spec files (from `spec:` field and `## Spec Impact` section).
Run `esperkit spec index` to see the full spec tree.

## Step 3: Inspect shipped implementation

Review the implementation changes:
- Read the files listed in `## Files Affected`
- Check git log for recent commits related to this increment
- Understand what was actually built vs what was planned

## Step 4: Update spec files

For each spec file that needs updating:
1. Read the current spec: `esperkit spec get <file>`
2. Compare against the shipped implementation
3. Update the spec to reflect actual behavior:
   - Add new sections for new features
   - Update existing sections where behavior changed
   - Remove sections for deprecated behavior
   - Keep the declarative, present-tense style ("The system does X")
4. Write the updated spec file

## Step 5: Record sync notes

Update the active increment's `## Spec Impact` section with what was synced:

```markdown
## Spec Impact
- [synced] product/behavior.md — updated authentication section
- [synced] interfaces/cli.md — added new command documentation
- [no-change] system/architecture.md — no updates needed
```

## Step 6: Finish the increment

Once all specs are synced:
1. Confirm with the user that the sync is complete
2. Run `esperkit increment finish <filename>`
3. Print a summary of what was updated

## Available CLI commands

- `esperkit context get` — read context
- `esperkit spec index` — show spec tree
- `esperkit spec get <file>` — read a spec
- `esperkit increment finish <file>` — finish the increment
