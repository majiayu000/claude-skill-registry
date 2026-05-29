---
id: 23
title: Add esper:revise skill for user-driven document revision
status: done
type: feature
priority: 2
phase: 004-exploration-and-review-skills
branch: feature/phase-4
created: 2026-02-21
shipped_at: 2026-02-21
pr: https://github.com/sichengchen/esper/pull/8
---
# Add esper:revise skill for user-driven document revision

## Context

Plan files, phase files, and fix documents are the backbone of the esper workflow — they define what gets built and how. Currently there is no structured way for a user to give feedback on these documents and have revisions applied. An `esper:revise` skill would let the user comment on a plan or phase doc, and the agent would apply the requested changes.

This is a user-driven workflow: the user provides the feedback, and the agent makes the edits. It is NOT an auto-review skill — the agent does not evaluate quality on its own.

## Approach

1. Create `skills/esper-revise/SKILL.md` with the following workflow:
   - **Step 1: Check setup** — run `esperkit config check`, read `.esper/CONSTITUTION.md`
   - **Step 2: Identify target** — accept a plan ID, phase name, or file path as `$ARGUMENTS`. If no argument, use `AskUserQuestion` to ask which document to revise. Resolve to a file path (e.g. `.esper/plans/pending/021-explore-skill.md` or `.esper/phases/phase-4.md`)
   - **Step 3: Read and present** — read the target document and display it to the user for review
   - **Step 4: Collect feedback** — use `AskUserQuestion` to ask the user what they want to change. Accept free-form comments, specific section edits, or structural feedback. Allow multiple rounds of revision
   - **Step 5: Apply revisions** — edit the document according to the user's feedback. Show the changes made and ask if further revisions are needed
   - **Step 6: Confirm** — when the user is satisfied, confirm the document is updated and suggest next steps (`/esper:apply` to start building, `/esper:backlog` to review the queue)

2. No changes to `bin/cli.js`.

## Files to change

- `skills/esper-revise/SKILL.md` (create — the skill definition)

## Verification

- Run: `node --test test/`
- Expected: existing tests still pass
- Edge cases: handle missing or malformed frontmatter, plans that reference files that don't exist yet, and multiple rounds of user feedback

## Progress
- Created `skills/esper-revise/SKILL.md` with 6-step workflow (check, identify target, read, collect feedback, apply revisions, confirm)
- Modified: skills/esper-revise/SKILL.md
- Verification: 64/64 tests pass
