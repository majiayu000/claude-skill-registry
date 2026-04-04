---
description: Work on a single highest-priority feature from current_ documents, test it, update docs, and commit
---

# Ralph Once - Single Feature Implementation Cycle

You are about to execute a focused, single-feature development cycle. Follow these steps precisely:

## Step 1: Read Current Documents

Find and read ALL files in the current project that start with `current_` (e.g., `current_PROGRESS.md`, `current_PRD.json`,  or for example `current_SYSTEM-PLAN.md`, or any other `current_* files could be .txt , .json , .md or other). These contain the project roadmap, PRD, and progress tracking.

## Step 2: Identify the Highest Priority Feature

After reading all `current_*` documents, YOU decide which single feature has the highest priority. Consider:
- Dependencies (what must be built before other things can work)
- Foundation vs polish (infrastructure before features)
- Blocking issues (what's preventing progress)
- Stage progression (complete earlier stages before later ones)

Do NOT just pick the first item in a list. Use your judgment about what will provide the most value or unblock the most work.

Announce your choice and briefly explain WHY you chose it before proceeding.

## Step 3: Implement the Feature

Work on ONLY this single feature. Do not scope creep. Do not "also fix" other things. Stay focused.

## Step 4: Test the Feature

- If tests exist for this feature area, run them and ensure they pass
- If no tests exist, write appropriate tests for the feature you just implemented
- All tests must pass before proceeding

## Step 5: Update the PRD

Find the `current_*` document that serves as the PRD/plan (likely `current_PRD.md` or similar). Update it to reflect:
- Mark the completed item as done (change `"passes": false` to ` "passes": true]` if using that or change "done" to true)
- Note any design decisions made during implementation
- Update any sections that are now outdated

## Step 6: Append to Progress File

Find `current_PROGRESS.md` (or the equivalent progress journal tracking file). Append a new entry to the Session Log with:
- Today's date
- What feature was implemented
- Key implementation details
- Any issues encountered and how they were resolved
- What tests were added/run

## Step 7: Git Commit

Stage and commit all changes with a clear commit message describing the feature implemented.

Do NOT push unless explicitly asked.

---

## CRITICAL RULES

1. **ONE FEATURE ONLY** - Do not work on multiple features. Stop after completing one feature cycle.
2. **TESTS REQUIRED** - Do not skip testing. Either run existing tests or write new ones.
3. **DOCUMENT EVERYTHING** - The progress file is your memory between sessions. Be thorough.
4. **COMMIT ATOMICALLY** - Each /ralphonce invocation should result in exactly one focused commit.
