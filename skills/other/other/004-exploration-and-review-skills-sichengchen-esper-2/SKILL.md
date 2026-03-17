---
id: 21
title: Add esper:explore skill for pre-planning investigation
status: done
type: feature
priority: 1
phase: 004-exploration-and-review-skills
branch: feature/phase-4
created: 2026-02-21
shipped_at: 2026-02-21
pr: https://github.com/sichengchen/esper/pull/8
---
# Add esper:explore skill for pre-planning investigation

## Context

The current esper workflow goes straight from idea to plan (`/esper:plan` or `/esper:fix`). There is no structured way to investigate feasibility, explore trade-offs, or brainstorm approaches before committing to a plan. The existing skills follow a consistent pattern: a `skills/esper-<name>/SKILL.md` file with frontmatter, steps, and tool usage instructions. There are currently 10 skill directories under `skills/`.

Exploration output will be saved to `.esper/explorations/` — a new directory that does not yet exist.

## Approach

1. Create `skills/esper-explore/SKILL.md` with the following workflow:
   - **Step 1: Check setup** — run `esperkit config check`, read `.esper/CONSTITUTION.md` and the current phase file for context
   - **Step 2: Interview** — use `AskUserQuestion` to understand what the user wants to explore (feature idea, architectural question, feasibility check). Ask whether they want codebase-aware exploration, open-ended brainstorming, or both
   - **Step 3: Explore** — for codebase-aware mode, use the Task tool with `subagent_type: "Explore"` to search the codebase for relevant patterns, files, and constraints. For brainstorm mode, discuss trade-offs, alternatives, and approaches conversationally
   - **Step 4: Summarize findings** — synthesize exploration into a structured markdown document
   - **Step 5: Save** — write the exploration doc to `.esper/explorations/NNN-slug.md` (use a simple incrementing ID based on existing files). Print the path and suggest next steps: `/esper:plan` to formalize, `/esper:fix` if it's a bug, or defer. Explorations are consumed during `/esper:phase` — the phase skill reads them, asks the user which ideas to include, and archives included explorations to `.esper/explorations/archived/`

2. Create `lib/exploration.js` — a module mirroring `lib/plan.js` for managing exploration files in `.esper/explorations/`. Commands:
   - `list` — list all explorations (exclude `archived/`), with optional `--format json`
   - `next-id` — scan existing explorations and return the next available zero-padded ID
   - `archive <filename>` — move an exploration to `.esper/explorations/archived/`
   - `get <filename>` — print frontmatter of a single exploration as JSON

3. Add `exploration` subcommand to `bin/cli.js` — route `esperkit exploration <list|next-id|archive|get>` to `lib/exploration.js`, following the same pattern as the `plan` subcommand.

4. Update `skills/esper-phase/SKILL.md` — add Step 3b to read explorations before the interview using `esperkit exploration list`, ask user which to include, and archive selected ones after phase is defined using `esperkit exploration archive`.

5. Update the explore skill's Step 5 to use `esperkit exploration next-id` for ID generation instead of manual file scanning.

## Files to change

- `skills/esper-explore/SKILL.md` (create — the skill definition)
- `lib/exploration.js` (create — exploration management module: list, next-id, archive, get)
- `bin/cli.js` (modify — add `exploration` subcommand routing)
- `skills/esper-phase/SKILL.md` (modify — add Step 3b using `esperkit exploration list` and `esperkit exploration archive`)

## Verification

- Run: `node --test test/`
- Expected: existing tests still pass, plus new tests for `lib/exploration.js`
- Edge cases: empty explorations dir, archiving already-archived explorations, ID generation with gaps

## Progress
- Created `skills/esper-explore/SKILL.md` with 5-step workflow (check, interview, explore, summarize, save)
- Created `lib/exploration.js` with list, next-id, get, archive commands
- Added `exploration` subcommand to `bin/cli.js`
- Updated `skills/esper-phase/SKILL.md` Step 3b to use `esperkit exploration list/archive`
- Added 11 tests in `test/exploration.test.js` — all pass
- Modified: skills/esper-explore/SKILL.md, lib/exploration.js, bin/cli.js, skills/esper-phase/SKILL.md, test/exploration.test.js
- Verification: 64/64 tests pass
