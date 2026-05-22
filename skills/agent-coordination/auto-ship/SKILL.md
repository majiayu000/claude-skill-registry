---
name: auto-ship
description: >
  Drives a surveycore implementation plan end-to-end — TDD implementation,
  spec compliance + code quality review, changelog, commit, PR, CI monitoring,
  and squash-merge to develop — with no manual handoffs. Analyzes the plan for
  independent sections and dispatches them as parallel subagents; dependent
  sections are processed in sequence. Stops only for spec ambiguity or
  unrecoverable CI failures. Trigger when the user says "auto-ship", "ship the
  plan", "drive the plan", "drive it", "hands-off", "do it all", or "run the
  plan". Also trigger when the user says any of those phrases combined with a
  plan file path, phase number, or section description.
---

# auto-ship

Orchestrates a full plan execution loop. Delegates each section to a section
subagent (`references/section-subagent.md`) that handles the complete lifecycle:
branch → implement → review → changelog → commit → PR → CI → merge.

---

## Entry Check

```bash
git branch --show-current
```

Must be on `develop`. If on `main` or any feature branch: stop and tell the user.

---

## Step 1: Read the Plan

Ask for the implementation plan path if not provided. Read it. Extract all
unchecked `- [ ]` sections. For each, record:
- Branch name (e.g., `feature/foo` from the `- [ ] PR N:` line)
- One-line description
- Any explicit dependency markers in the text (`"requires PR N"`,
  `"depends on"`, `"after PR N"`)

If all sections are `[x]`: report "Plan complete — nothing to ship." and stop.

---

## Step 2: Baseline Check

```r
devtools::test()
devtools::check()
```

Both must pass before dispatching any subagent. If either fails: stop and
report the failure. Do not proceed.

---

## Step 3: Build Execution Order

Group the unchecked sections into **batches** using topological sort:

1. **Batch 1** — all sections with no dependencies on other unchecked sections
2. **Batch 2** — sections whose only dependencies are fully in Batch 1
3. Continue until all sections are placed

Sections with no dependency markers are assumed independent.

**Parallel safety check** — before placing two sections in the same batch,
verify they don't both modify the same shared files. A section will modify a
shared file if its spec or plan text mentions:
- New error or warning classes → modifies `plans/error-messages.md`
- New exported functions → modifies `_pkgdown.yml`

If two sections in the same batch would both modify the same shared file, move
the one with fewer dependencies to the next batch. Err on the side of
sequential — a false "conflict" costs one extra round; a false "safe" causes
a merge conflict that blocks both PRs.

Report the execution plan to the user before dispatching:

> "Found N unchecked sections. Execution order:
> - Batch 1 (parallel): feature/foo, feature/bar
> - Batch 2 (sequential): feature/baz (requires feature/foo)
>
> Starting Batch 1 now."

---

## Step 4: Dispatch Batch

For each section in the current batch, spawn a **section subagent**
(see `references/section-subagent.md`). Dispatch all sections in the batch
simultaneously using `run_in_background: true`.

Provide each subagent with:
- Full section text (copy it; do not make the subagent re-read the file)
- Branch name to create
- Spec file path(s) relevant to this section (from the plan text)
- Implementation plan file path
- Paths to rule files: `code-style.md`, `testing-surveycore.md`,
  `plans/error-messages.md`
- Today's date

---

## Step 5: Handle Results

Each subagent returns one of:

| Result | Action |
|--------|--------|
| `COMPLETE: <pr-url>` | Mark section `[x]` in the plan on `develop`; record PR URL |
| `BLOCKED: spec — <question>` | Ask the user the exact question; re-dispatch subagent with the answer |
| `BLOCKED: ci-fail — <summary>` | Report to user with full details; stop this section; continue others |
| `BLOCKED: check-fail — <summary>` | Report to user with full details; stop this section; continue others |

**Marking `[x]` in the plan:** after a section returns `COMPLETE`, check out
`develop`, pull, edit the plan file to change that section's `- [ ]` to
`- [x]`, and commit directly to `develop`:

```bash
git checkout develop
git pull origin develop
# edit plan file
git add <plan-file>
git commit -m "chore(plan): mark feature/X complete"
```

Do NOT include the [x] mark in the feature branch commit — doing it here avoids
merge conflicts when parallel subagents both modify the plan file.

When all sections in a batch are resolved (COMPLETE or BLOCKED-and-stopped),
advance to the next batch. Report any BLOCKED sections and continue — don't
let one stuck section hold up independent work.

---

## Step 6: Advance

Repeat Steps 4–5 for each remaining batch. Pull `develop` before each new
batch starts so subagents branch from the latest state.

---

## Step 7: Done

When all batches are resolved:

> "Plan complete."
>
> "Merged: [list of PR URLs]"
>
> If any sections were BLOCKED:
> "Blocked (needs attention): [list of section names and reasons]"

---

## Spec Ambiguity Protocol

When a subagent returns `BLOCKED: spec — [question]`:

1. Show the user the exact question, attributed to the section
2. Wait for the answer
3. Re-dispatch the same section subagent with the answer appended to the
   section text
4. The subagent resumes from pre-implementation checks, not from scratch
