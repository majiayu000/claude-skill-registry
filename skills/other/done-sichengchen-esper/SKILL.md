---
id: 22
title: Add esper:review skill for code quality review
status: done
type: feature
priority: 2
phase: 004-exploration-and-review-skills
branch: feature/phase-4
created: 2026-02-21
shipped_at: 2026-02-21
pr: https://github.com/sichengchen/esper/pull/8
---
# Add esper:review skill for code quality review

## Context

esper currently has no skill for reviewing code before shipping. The `/esper:ship` skill pushes and opens a PR, but there is no structured code review step. An `esper:review` skill would let users get code quality feedback on their branch diff before shipping, catching issues early.

The skill should work at the branch/PR level — reviewing the diff between the current branch and main, focused on code quality (bugs, style, security, complexity).

## Approach

1. Create `skills/esper-review/SKILL.md` with the following workflow:
   - **Step 1: Check setup** — run `esperkit config check`, determine current branch and base branch
   - **Step 2: Gather diff** — run `git diff main...HEAD` (or the appropriate base) to get the full branch diff. If a PR number is provided as argument, use `gh pr diff <number>` instead
   - **Step 3: Read context** — read `.esper/CONSTITUTION.md` for project principles. If there's an active plan, read it for intent context (what the code is supposed to do)
   - **Step 4: Review** — analyze the diff for:
     - Bugs and logic errors
     - Security issues (OWASP top 10)
     - Code style and consistency with existing patterns
     - Missing error handling or edge cases
     - Unnecessary complexity or dead code
   - **Step 5: Report** — print a structured review with sections for each category. Use severity levels (critical, warning, note). Include file paths and line references
   - **Step 6: Offer fixes** — if actionable issues were found, use `AskUserQuestion` to ask if the user wants to create `/esper:fix` plans for them. If yes, batch the selected issues into fix plans (one per issue or grouped by file/concern, at the user's preference)

2. No changes to `bin/cli.js` — the installer auto-discovers new skill directories.

## Files to change

- `skills/esper-review/SKILL.md` (create — the skill definition)

## Verification

- Run: `node --test test/`
- Expected: existing tests still pass
- Edge cases: handle empty diffs (nothing to review), very large diffs (summarize rather than line-by-line), and PRs with no active plan context

## Progress
- Created `skills/esper-review/SKILL.md` with 6-step workflow (check, gather diff, read context, review, report, offer fixes)
- Modified: skills/esper-review/SKILL.md
- Verification: 64/64 tests pass
