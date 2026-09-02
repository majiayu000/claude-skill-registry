---
name: seed-casebook
description: 'Use when a user opens a new build cycle in a repo with an established iteration convention and wants the casebook directory to exist with real content from the first observable moment. Builds the complete seed in a temporary sibling directory and atomically renames it into place. Not for ongoing triage or multi-repo setup.'
---

# Seed iteration casebook

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User opens a new build cycle in a repo with an established iteration convention. |
| Authority | Reversible-local write of the named casebook directory and its seed files only. |
| Side effect | Creates the iteration casebook directory already containing real seed content. The directory is never observable empty and a failed write never leaves a partial directory. |
| Done | The casebook directory appeared atomically with non-empty seed content on exactly one weight path. Full path has DESIGN thesis/scope/gates, cycle-specific WORKFLOW steps, EVIDENCE gates each tracing to a DESIGN line. Lightweight path has a one-paragraph retro seed. The version token is provisional until forks resolve. |

## Inputs

- Iteration path prefix and naming scheme (required): inferred from existing casebook directories, VCS history, or project docs. Not hard-coded.
- Cycle name (required): the workname for this iteration.
- Weight context (optional): whether the cycle is a fix, hardening pass, or new direction. Defaults to lightweight when uncertain.

## Procedure

1. Classify the cycle weight before any write. Lightweight: a fix or hardening pass with no genuine design surface. Full: a cycle with a direction worth arguing through. If classification is uncertain, choose lightweight; full can be reopened by a subsequent cycle. Done when: the weight is chosen and recorded.
2. Resolve the target path. Construct the casebook directory path from the repo's established iteration convention and cycle name. If the directory already exists, stop with the conflict. Do not overwrite. Determine the version token's provisional state by checking the cycle's open forks against the repo's stated fork source: open PRs, branches, or the convention's own fork record. Encode provisional status in the path or a marker file per that convention. Done when: the target path is resolved and the provisional-version state is determined.
3. Build the complete seed in a temporary sibling directory. Create a temporary directory adjacent to the target path (for example `<target>.tmp`). Write the seed files into it:
   - Lightweight path: write `RETRO.local.md` with one paragraph naming the task and why it is lightweight. Do not write DESIGN, WORKFLOW, or EVIDENCE.
   - Full path: write three files. `DESIGN.local.md`: thesis, scope, and quality gates. When the cycle touches shippable surface, gates must include a documentation reflection gate. `WORKFLOW.local.md`: the numbered steps this specific cycle runs, specific to this build, not a restatement of generic stages. `EVIDENCE.local.md`: the gates from DESIGN listed as proof surface still to fill. Every EVIDENCE gate must trace to a DESIGN line; do not invent proof surface DESIGN did not name.
   Validate that no required file is empty. Done when: the temporary directory contains all required seed files, each non-empty, and every EVIDENCE gate traces to a DESIGN line.
4. Atomically rename the temporary directory to the final path. Use `rename(2)` or the platform equivalent to move the temporary directory into place in a single operation. The directory is never observable empty and a failed write never leaves a partial directory. On any failure during rename, remove the temporary directory and report. Do not produce a partial or empty result. Done when: the final directory exists with all seed content.
5. Report the path taken, the weight classification, and the provisional-version state. Done when: the report is emitted.

## Failure and recovery

- Already-exists: the casebook directory already exists for this cycle. Stop. Do not overwrite existing content or write a parallel directory. Report the conflict.
- Creation failure: any write or rename fails. Remove the temporary directory. Report the filesystem error. No partial directory remains at the final path.
- Empty-write: a required file would be written empty. Stop. Never create a placeholder. Remove the temporary directory.
- Wrong-path discovered mid-cycle: if the chosen weight path proves wrong, the casebook is retired by a release or retirement workflow, not overwritten or migrated by this skill.
- Version provisional: the casebook directory's version token is tentative until any open fork in the cycle resolves. Do not finalize the bump label until forks close.

## Output

A casebook directory at the repo's iteration convention path, containing either `RETRO.local.md` (lightweight) or `DESIGN.local.md` plus `WORKFLOW.local.md` plus `EVIDENCE.local.md` (full). The directory appeared atomically with non-empty content. The skill reports the path taken, the weight classification, and the provisional-version state.
