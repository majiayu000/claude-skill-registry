---
name: run-todos
description: Implement [ready]-tagged TODO items with commits. Use after /list-todos has clarified requirements and marked items as ready.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, Task
---

# Run TODOs Skill

Implement TODO items that have been marked as `[ready]` in TODOS.md.

## Workflow

Copy this checklist and track progress:

```
Run TODOs Progress:
- [ ] Step 1: Directory guard check
- [ ] Step 2: Find [ready] items
- [ ] Step 3: User selection
- [ ] Step 4: Git workflow setup
- [ ] Step 5: Implementation loop (per item)
- [ ] Step 6: Update TODOS.md with completion
- [ ] Step 7: Generate summary report
```

## Directory Guard

Before starting, confirm `TODOS.md` exists in the current working directory.

- If it does not exist, **STOP** and tell the user to create TODOS.md or `cd` into their project directory.

## Context Check

**Before starting:** If context is below 40% remaining, run `/compact` first. This ensures the full command instructions remain in context throughout execution.

## Find [ready] Items

1. Read TODOS.md
2. Find all items containing the `[ready]` tag
3. Exclude items that are already checked (`- [x]`) or have `— DONE`

If no [ready] items found:
```
NO READY ITEMS
==============
No items tagged [ready] found in TODOS.md.

To mark items as ready:
1. Run /list-todos
2. Go through Q&A to clarify requirements
3. Confirm readiness when asked

Or manually add [ready] tag to items you want to implement.
```

## User Selection

Show the list of [ready] items and let user select:

```
READY ITEMS
===========
Found {N} items tagged [ready]:

1. {item title 1}
2. {item title 2}
3. {item title 3}

Which items would you like to implement?
```

Use AskUserQuestion:
```
Question: "Which items would you like to implement?"
Header: "Selection"
Options:
  - Label: "All items"
    Description: "Implement all {N} ready items in sequence (Recommended)"
  - Label: "Select specific items"
    Description: "Choose which items to implement"
  - Label: "Cancel"
    Description: "Exit without implementing"
```

If "Select specific items", use AskUserQuestion with multiSelect:
```
Question: "Select items to implement:"
Header: "Items"
Options:
  - Label: "1. {item 1 title}"
    Description: "{priority if present}"
  - Label: "2. {item 2 title}"
    Description: "{priority if present}"
  ... (up to 4 items per question, use multiple questions if more)
multiSelect: true
```

If "Cancel", exit the command.

## Git Workflow

### Check for Unpushed Commits

Before creating a branch:
```bash
CURRENT_BRANCH=$(git branch --show-current)
UNPUSHED=$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "no-upstream")
```

If `UNPUSHED` > 0, use AskUserQuestion:
```
Question: "You have {UNPUSHED} unpushed commit(s) on `{CURRENT_BRANCH}`. Push before creating todo branch?"
Header: "Unpushed"
Options:
  - Label: "Yes, push first"
    Description: "Push current commits before starting (Recommended)"
  - Label: "No, continue anyway"
    Description: "Create branch from unpushed state"
```

### Create Branch

```bash
# If working tree is dirty, stage and commit tracked changes first
git add -u && git diff --cached --quiet || git commit -m "wip: uncommitted changes before todo implementation"

# Create todo implementation branch
git checkout -b todo-impl-$(date +%Y-%m-%d)
```

**Note:** Use `git add -u` (tracked files only) to avoid accidentally staging secrets,
build artifacts, or other untracked files. If untracked files need to be included,
stage them by name.

**Verify branch creation:** Run `git branch --show-current` and confirm it matches
`todo-impl-{date}`. If the checkout failed (e.g., branch already exists), append
a suffix: `todo-impl-{date}-2`.

## Implementation Loop

For each selected item:

### 1. Show Item Context

```
IMPLEMENTING: {item title}
===========================

{Full item text from TODOS.md}

{If clarifications exist:}
Clarifications:
- {Q1}: {A1}
- {Q2}: {A2}
```

### 2. Clarity Cross-Check

Before implementing, verify the item has sufficient detail. Check for **both**:

- **Description length:** Is the item a one-liner with no context beyond the title?
- **Clarifications section:** Does a `**Clarifications (from Q&A ...)**` block exist for this item in TODOS.md?

**If the item has NEITHER a multi-sentence description NOR a clarifications section,**
flag it to the user:

```
⚠ THIN REQUIREMENTS
This item has no clarifications and a minimal description:
  "{item title}"

Implementing without clear requirements risks building the wrong thing.
```

Use AskUserQuestion:
```
Question: "'{item title}' has minimal requirements. How should we proceed?"
Header: "Thin reqs"
Options:
  - Label: "Clarify now"
    Description: "Ask questions before implementing (Recommended)"
  - Label: "Implement anyway"
    Description: "Proceed with best judgment based on available context"
  - Label: "Skip this item"
    Description: "Move to the next item"
```

- **"Clarify now"** → ask clarifying questions via AskUserQuestion, then proceed to Step 3
- **"Implement anyway"** → proceed to Step 3
- **"Skip this item"** → record as skipped, move to next item

**If the item has a description or clarifications**, proceed directly to Step 3.

### 3. Implement

Implement the TODO item following project conventions:
- Read relevant existing code to understand patterns
- Write tests first if acceptance criteria exist
- Implement the feature/fix
- Run tests to verify

### 4. Verify (if criteria exist)

If the item has acceptance criteria or testable requirements:
- Run the relevant test suite
- Use auto-verify skill for automatable checks
- Report verification results

### 5. Update TODOS.md

After successful implementation:

1. Check the box: `- [ ]` → `- [x]`
2. Add completion suffix: `— DONE ({short_commit_hash})`

**Before:**
```markdown
- [ ] **[P1 / Medium]** Add user auth endpoint [ready]
```

**After:**
```markdown
- [x] **[P1 / Medium]** Add user auth endpoint [ready] — DONE (a1b2c3d)
```

Use the Edit tool to make this update.

### 6. Commit

Stage the specific files changed during implementation, plus `TODOS.md`:

```bash
git add {files created or modified during implementation} TODOS.md
git commit -m "todo: {item title (shortened if needed)}"
```

**Do NOT use `git add -A` or `git add .`** — stage files by name to avoid
committing secrets (`.env`), credentials, or unintended artifacts.

**Verify commit succeeded:** Check exit code of `git commit`. If it fails (e.g.,
pre-commit hook rejection), fix the issue and create a new commit — do NOT use
`--amend`.

Get the commit hash for the TODOS.md update:
```bash
COMMIT_HASH=$(git rev-parse --short HEAD)
```

### 7. Handle Failure

If implementation fails (tests don't pass, errors occur), use AskUserQuestion:

```
Question: "Implementation of '{item title}' failed. What would you like to do?"
Header: "Failed"
Options:
  - Label: "Skip this item"
    Description: "Continue with the next item (Recommended if blocked)"
  - Label: "Retry"
    Description: "Try implementing again with a different approach"
  - Label: "Abort session"
    Description: "Stop and leave remaining items for later"
```

## Summary Report

After all items are processed (or aborted):

```
RUN-TODOS COMPLETE
==================

Branch: todo-impl-{date}

Completed: {N} items
{For each completed item:}
  ✓ {item title} ({commit_hash})

{If any skipped:}
Skipped: {N} items
{For each skipped item:}
  ✗ {item title} — {reason}

{If aborted early:}
Remaining: {N} items not attempted

TODOS.md updated with completion status.

Next: Review changes, then run:
  git push origin todo-impl-{date}

Ready to open a PR? Run: /create-pr
```

## Archive Completed Items

After the summary report, count the total number of completed items (`- [x]`) in
TODOS.md (including items completed in previous sessions).

**If 10 or more completed items exist**, offer to archive:

```
Question: "TODOS.md has {N} completed items. Archive them to keep the file manageable?"
Header: "Archive"
Options:
  - Label: "Yes, archive (Recommended)"
    Description: "Move completed items to TODOS-ARCHIVE.md"
  - Label: "No, keep as-is"
    Description: "Leave completed items in TODOS.md"
```

**If "Yes, archive":**

1. Read (or create) `TODOS-ARCHIVE.md` in the project root
2. Move all `- [x]` items (and their clarifications blocks) from TODOS.md to
   TODOS-ARCHIVE.md under a dated heading:
   ```markdown
   ## Archived {YYYY-MM-DD}

   - [x] **[P1 / Medium]** Item title [ready] — DONE (a1b2c3d)
   - [x] **[P2 / Low]** Another item [ready] — DONE (e4f5g6h)
   ```
3. Remove the archived items from TODOS.md (keep section headings intact)
4. Stage and commit:
   ```bash
   git add TODOS.md TODOS-ARCHIVE.md
   git commit -m "chore: archive completed TODO items"
   ```

**If fewer than 10 completed items**, skip this step silently.

## Notes

- **Do NOT push automatically.** Leave pushing to the human after review.
- **One commit per item.** Each TODO gets its own commit for traceability.
- **Preserve [ready] tag.** The tag stays even after completion for history.
- **Short commit hashes.** Use 7-character short hash in DONE suffix.
