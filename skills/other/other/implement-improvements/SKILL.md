---
name: implement-improvements
description: "Plan and implement improvements from the .turbo/improvements.md backlog after validating them against the current codebase. Use when the user asks to \"implement improvements\", \"work on improvements\", \"address improvements\", \"process improvement backlog\", \"tackle improvements\", or \"implement noted improvements\"."
---

# Implement Improvements

Validate and implement improvements from `.turbo/improvements.md`.

## Step 1: Run `/plan-style` Skill

Run the `/plan-style` skill to load planning conventions.

## Step 2: Read the Backlog

Read `.turbo/improvements.md`. If the file does not exist, tell the user there are no improvements to implement and stop.

Parse all entries, extracting for each:

- **Summary** (the `###` heading)
- **Category**
- **Where** (file paths or areas)
- **Why** (rationale)
- **Noted** (date)

## Step 3: Validate Against Current Codebase

Improvements can go stale: files get renamed, code gets refactored, issues get fixed as side effects of other work. Before planning, validate each improvement.

For each entry, verify whether the specific problem or opportunity described in the entry still exists in the code. Do not rely on git log alone. Recent commits touching the same files do not mean the specific issue was addressed. Read the actual code and confirm:

1. **Files exist** — Do the referenced files/paths still exist? If not, the entry is stale.
2. **Problem persists** — Read the relevant code sections. Is the exact issue or opportunity described in the entry still present? This is the primary determination. Check the specific claims: if the entry says a function is uncalled, verify it has no callers; if it says error handling is missing, check whether it was added.

Classify each entry as:

- **Active** — The described problem or opportunity is confirmed present in the current code
- **Stale** — The referenced files no longer exist, or the specific issue has been resolved (cite the evidence: what changed and where)
- **Unclear** — Cannot determine from code alone, needs user input

When in doubt, classify as Active. The cost of re-examining a resolved issue is low; dismissing a valid improvement is high.

## Step 4: Report Findings

Present a summary to the user:

```
## Improvement Backlog Status

### Active (N)
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

## Step 5: Plan

Design an implementation plan that addresses all confirmed improvements together, looking for:

- **Synergies** — Improvements touching the same files or areas should be grouped
- **Dependencies** — Order improvements so that foundational changes come first
- **Conflicts** — Flag if two improvements contradict each other

The plan must include a step to clean up `.turbo/improvements.md`: remove implemented and stale entries, keep skipped or deferred ones. Delete the file if all entries are removed.
