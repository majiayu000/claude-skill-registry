---
name: implement-improvements
description: "Validate improvements from .turbo/improvements.md and run one lane based on the user's choice: trivial fixes, investigation, or standard planning. One lane per session. Use when the user asks to \"implement improvements\", \"work on improvements\", \"address improvements\", \"process improvement backlog\", \"tackle improvements\", or \"implement noted improvements\"."
---

# Implement Improvements

Validate improvements from `.turbo/improvements.md` and run one lane per session: trivial, investigate, or standard. Mixing lanes in a single run tangles commits, so the skill processes exactly one lane each time. Entries outside the chosen lane or category filter stay in the backlog for future runs.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Read the backlog
2. Validate and classify
3. Report, confirm, and prune stale
4. Run the chosen lane
5. Prune working-set entries from the backlog

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

## Step 3: Report, Confirm, and Prune Stale

Present a summary grouped by type and status. Include each entry's category inline and a category tally across active entries so the user can narrow the working set by theme:

```
## Improvement Backlog Status

### Active (N)
Categories: refactor (N), performance (N), testing (N), docs (N)

**Trivial (N)**
- [summary] (category) — [one-line reason it's still relevant]

**Investigate (N)**
- [summary] (category) — [one-line reason it's still relevant]

**Standard (N)**
- [summary] (category) — [one-line reason it's still relevant]

### Stale (N)
- [summary] — [one-line reason it's stale]

### Unclear (N)
- [summary] — [what's ambiguous]
```

Use `AskUserQuestion` to confirm:
1. Which lane to run: trivial, investigate, or standard (if only one lane has active entries, default to it)
2. Category filter (default: all)
3. Whether to remove stale entries from the backlog
4. Resolution for any unclear items

If the user confirmed stale removal, edit `.turbo/improvements.md` to delete the stale entries.

Compute the **working set**: active entries matching the confirmed lane and category filter, after unclear resolution. If the working set is empty, stop.

## Step 4: Run the Chosen Lane

Read the reference file for the confirmed lane and follow its phases:

- **Trivial lane** — [references/trivial-lane.md](references/trivial-lane.md)
- **Investigate lane** — [references/investigate-lane.md](references/investigate-lane.md)
- **Standard lane** — [references/standard-lane.md](references/standard-lane.md)

State the chosen lane before handing off to the reference file.

## Step 5: Prune Working-Set Entries from the Backlog

Edit `.turbo/improvements.md` to delete the working-set entries that the lane processed. "Processed" means:

- **Trivial lane** — entries whose fixes were applied
- **Investigate lane** — entries whose concluded fixes were applied
- **Standard lane** — entries now captured in the plan file produced by `/turboplan`

Keep any entries the lane re-classified mid-flight (trivial → investigate/standard, or investigate → standard). These stay in the backlog for a future run. Delete the file if no entries remain.

## Rules

- `.turbo/` is gitignored. Edits to `.turbo/improvements.md` are local-only and do not need to be staged or committed.
- If the user selected a lane, do not secondarily run another lane in the same session. Other active entries stay in the backlog for a future run.
