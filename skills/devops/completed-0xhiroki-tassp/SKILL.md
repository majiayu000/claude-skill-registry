---
name: completed
description: 'Status: Completed'
---

# Task: Doc Writer Skill

**Status:** Completed
**Updated:** 2025-11-23
**Scope:** `.factory/skills/doc-writer`

## Objective
Introduce a reusable Droid skill that can generate or update numbered task documents using the project’s canonical template (`docs/DOC_TEMPLATE.md`) and existing repository context.

## Prerequisites / Dependencies
- Repository already includes `docs/DOC_TEMPLATE.md`, `AGENTS.md`, and `PLAN.md` for reference material.
- `.factory/skills/` directory exists (per Factory CLI conventions) and is committed for team-wide sharing.
- Backend validators (`npm run lint`, `npm run test`) must remain green after any repo additions.

## Implementation Summary
1. Created `.factory/skills/doc-writer/SKILL.md` with YAML frontmatter (`name: doc-writer`, `description` describing purpose).
2. Authored instructions covering how to gather context (PLAN, AGENTS, DOC_TEMPLATE), enforce numbering, and structure every task doc (Objective, Prerequisites, Implementation Steps, Validation, Completion Criteria, Notes).
3. Documented saving conventions (correct directories and filenames) plus validation requirements (markdown structure adherence, numbering uniqueness).
4. Verified the repository by running backend lint/test commands to ensure no regressions after adding the skill files.

## Validation
- `npm --prefix "backend" run lint`
- `npm --prefix "backend" run test`

## Completion Criteria
- Skill file present under `.factory/skills/doc-writer/SKILL.md`. ✅
- Instructions explicitly reference `docs/DOC_TEMPLATE.md` and repo naming rules. ✅
- Validators pass after adding the skill. ✅

## Notes / Follow-ups
- Future doc-related tasks can reference this skill to ensure consistent formatting.
- Add additional skill variants if other documentation workflows emerge (e.g., PR templates, release notes).
