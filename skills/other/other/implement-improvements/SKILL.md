---
name: implement-improvements
description: "Plan and implement improvements from the .turbo/improvements.md backlog after validating them against the current codebase. Routes each entry by type to a direct fix, a dedicated investigation, or full planning. Use when the user asks to \"implement improvements\", \"work on improvements\", \"address improvements\", \"process improvement backlog\", \"tackle improvements\", or \"implement noted improvements\"."
---

# Implement Improvements

Validate and implement improvements from `.turbo/improvements.md`, routing each entry by its type.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Read the backlog
2. Validate and classify
3. Report findings
4. Run `/implement` skill for trivial fixes
5. Run `/investigate` skill for investigate entries
6. Run `/implement` skill for investigate fixes
7. Clean up improvements backlog
8. Run `/commit-staged` skill
9. Run `/turboplan` skill for standard entries

Step 4 is skipped if no trivial entries survive validation. Step 5 is skipped if no investigate entries survive validation. Step 6 is skipped if no investigate entries survive or if Step 5 produced no actionable fixes. Steps 7–8 are skipped if nothing was implemented in Steps 4 or 6 AND no stale entries were confirmed for removal in Step 3. Step 9 is skipped if no standard entries survive.

## Step 1: Read the Backlog

Read `.turbo/improvements.md`. If the file does not exist, tell the user there are no improvements to implement and stop.

Parse all entries, extracting for each:

- **Summary** (the `###` heading)
- **Type** (`trivial`, `investigate`, or `standard`; may be missing in older entries)
- **Category**
- **Where** (file paths or areas)
- **Why** (rationale)
- **Noted** (date)

## Step 2: Validate and Classify

Improvements can go stale: files get renamed, code gets refactored, issues get fixed as side effects of other work. Before routing, validate each improvement and classify any entry missing a Type.

### Validate

For each entry, verify whether the specific problem or opportunity described still exists. Do not rely on git log alone. Recent commits touching the same files do not mean the specific issue was addressed. Read the actual code and confirm:

1. **Files exist** — Do the referenced files/paths still exist? If not, the entry is stale.
2. **Problem persists** — Read the relevant code sections. Is the exact issue or opportunity described in the entry still present? Check the specific claims: if the entry says a function is uncalled, verify it has no callers; if it says error handling is missing, check whether it was added.

Classify each entry as:

- **Active** — The described problem or opportunity is confirmed present in the current code
- **Stale** — The referenced files no longer exist, or the specific issue has been resolved (cite evidence: what changed and where)
- **Unclear** — Cannot determine from code alone, needs user input

When in doubt, classify as Active. The cost of re-examining a resolved issue is low; dismissing a valid improvement is high.

### Classify type if missing

For any Active entry without a Type field, infer one on the fly. Base the classification on the code you just read during validation, not just the entry's one-line summary.

- **trivial** — A direct fix: typo, rename, obvious one-liner, small localized cleanup with clear scope. No investigation or plan needed.
- **investigate** — A symptom, not a fix: unclear root cause, performance question, intermittent bug, "something feels off". Needs dedicated root-cause analysis before any change.
- **standard** — Everything else: clear-scope work that warrants planning (multi-file refactor, test additions, feature work).

Do not ask the user to pick. If genuinely ambiguous, default to `standard`.

## Step 3: Report Findings

Present a summary grouped by type and status:

```
## Improvement Backlog Status

### Active (N)
**Trivial (N)**
- [summary] — [one-line reason it's still relevant]

**Investigate (N)**
- [summary] — [one-line reason it's still relevant]

**Standard (N)**
- [summary] — [one-line reason it's still relevant]

### Stale (N)
- [summary] — [one-line reason it's stale]

### Unclear (N)
- [summary] — [what's ambiguous]
```

If there are more than 10 active improvements, suggest splitting into multiple sessions.

Use `AskUserQuestion` to confirm:
1. Which active improvements to implement (default: all; suggest a subset if splitting)
2. Whether to remove stale entries from the backlog
3. Resolution for any unclear items

## Step 4: Run `/implement` Skill for Trivial Fixes

Skip if no trivial entries were confirmed. Otherwise, in the turn that invokes `/implement`, write out each trivial fix as an explicit bullet: summary + files + change description. If a trivial entry turns out to need broader scope or deeper analysis during implementation, stop and re-classify it as `investigate` or `standard`. Then run the `/implement` skill. `/implement` loads `/code-style`, applies the fixes directly, and runs `/finalize` to review, test, and commit.

## Step 5: Run `/investigate` Skill for Investigate Entries

Skip if no investigate entries were confirmed. Otherwise:

Before starting the loop, use `TaskCreate` to add one sub-task per investigate entry (e.g., `Investigate: <summary>`). Mark each sub-task `in_progress` before the corresponding `/investigate` run and `completed` after.

For each investigate entry, run the `/investigate` skill. In the problem statement passed to `/investigate`, include the entry's summary and rationale, then append a note that this is an improvement-backlog entry likely to be a symptom and that `/investigate` should run `/consult-codex` even if only 1–2 hypotheses surface initially.

If `/investigate` surfaces complexity that exceeds a single-session fix (multi-subsystem change, architectural decision), stop that entry and move it to the standard batch for Step 9 instead.

## Step 6: Run `/implement` Skill for Investigate Fixes

Skip if Step 5 produced no actionable fixes. Otherwise, in the turn that invokes `/implement`, write out each investigation's concluded fix as an explicit bullet: summary + files + change description. This is especially important here because `/investigate`'s earlier output has likely displaced continuation context. Then run the `/implement` skill. `/implement` loads `/code-style`, applies the fixes scoped to what the investigations concluded, and runs `/finalize`.

## Step 7: Clean Up Improvements Backlog

Skip if nothing was implemented in Steps 4 or 6 AND no stale entries were confirmed for removal in Step 3.

Otherwise, edit `.turbo/improvements.md` to remove entries that are now done:

- Trivial and investigate entries implemented in Steps 4 and 6
- Stale entries the user confirmed removing in Step 3

Leave standard entries in place so `/implement-plan` can execute them in a fresh session. Delete the file if no entries remain.

Stage `.turbo/improvements.md` (or its deletion) so Step 8 can commit it.

## Step 8: Run `/commit-staged` Skill

Skip if Step 7 was skipped. Otherwise, run the `/commit-staged` skill to commit the backlog cleanup as a chore commit.

## Step 9: Run `/turboplan` Skill for Standard Entries

Skip if no standard entries were confirmed. Otherwise, run the `/turboplan` skill with the standard entries as the task description. Include planning constraints:

- **Synergies** — Group improvements that touch the same files or areas
- **Dependencies** — Order so foundational changes come first
- **Conflicts** — Flag if two improvements contradict each other

`/turboplan` produces a plan file and halts. The user runs `/implement-plan` in a fresh session.
