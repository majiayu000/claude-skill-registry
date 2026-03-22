---
version: 1.0.0
name: doc-prd
description: >
  Generate a Product Requirements Document from template. Use when the user says
  "create a PRD", "write requirements", "product spec", or "define the feature".
disable-model-invocation: false
user-invocable: true
argument-hint: "[feature or product name]"
---

# Generate PRD

## Path Resolution

1. Read `workflow.json` in the project root
2. If it exists and `docsRepo` is `"."`: this IS the docs repo — use local paths
3. If it exists and `docsRepo` is a repo name: resolve via `pwsh .claude/skills/tool-worktree/scripts/resolve-repo.ps1 <docsRepo>` to get the docs root path. Templates at `<resolved>/templates/`, output to `<resolved>/prd/`
4. If no `workflow.json`: templates at `templates/`, output to `docs/prd/`

## Instructions

1. **Resolve paths** (see Path Resolution above)
2. **Read the template** at `<templates>/prd.md`
3. **Ask clarifying questions** if the user hasn't provided enough context:
   - What problem are we solving?
   - Who is the target user?
   - What are the key goals?
4. **Generate the PRD** by filling in the template sections based on:
   - User's description of the feature/product
   - Existing codebase context (read relevant code if applicable)
   - Domain knowledge from the project
5. **Save the PRD** to `<output>/[slug].md` (create the directory if needed)
6. **Be opinionated** — fill in non-goals, constraints, and success metrics based on what you know. The user can refine.

## Quality Checklist

- [ ] Problem statement is specific, not vague
- [ ] Goals are measurable (numbers, percentages, or clear criteria)
- [ ] Non-goals are listed (at least 2)
- [ ] User stories follow "As a... I want... So that..." format
- [ ] Requirements have acceptance criteria
- [ ] Success metrics have current vs. target values
- [ ] Open questions are flagged (don't guess — ask)

## Tips

- Link to related RFCs or ADRs if they exist
- Reference existing code patterns when defining requirements
- Keep it concise — a PRD should be scannable in 5 minutes
