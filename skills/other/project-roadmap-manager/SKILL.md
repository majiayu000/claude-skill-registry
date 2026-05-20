---
name: project-roadmap-manager
description: Create and maintain a repository-root ROADMAP.md as the single source of truth for project milestones and accepted plans. Use when bootstrapping any new project, accepting/completing a plan, defining or updating milestone/version roadmaps, marking milestones as reached/changed/de-scoped, or answering where roadmap and milestone status should be referenced.
---

# Project Roadmap Manager

Maintain `ROADMAP.md` in the project root as the canonical roadmap record. Prefer updating existing sections over appending duplicates, and keep `Current Milestone` synchronized with the latest accepted plan.

## Workflow

1. Identify project root and target file:
   - Use `<project_root>/ROADMAP.md`.
   - If root is ambiguous, infer from repository root.
2. Ensure `ROADMAP.md` exists:
   - If missing, create it using the template in this skill.
3. Classify the request into one of these event types:
   - Project bootstrap.
   - Plan acceptance/completion.
   - Milestone/version roadmap set or changed.
   - Milestone reached/blocked/de-scoped.
   - Roadmap reference/query.
4. Apply the event-specific update rules.
5. Keep all sections internally consistent:
   - `Current Milestone` matches active milestone in `Milestones`.
   - `Plan History` includes accepted plan snapshots.
   - `Change Log` captures each roadmap mutation with date and reason.

## ROADMAP.md Template

Use this structure when creating a new roadmap:

```markdown
# Project Roadmap

## Current Milestone
- ID: M1
- Name: Initial Setup
- Status: Planned
- Target Version: v0.1.0
- Last Updated: YYYY-MM-DD
- Summary: One-paragraph summary of the currently accepted plan.

## Milestones
| ID | Name | Target Version | Status | Target Date | Notes |
| --- | --- | --- | --- | --- | --- |
| M1 | Initial Setup | v0.1.0 | Planned | YYYY-MM-DD | Bootstrap milestone |

## Plan History
### YYYY-MM-DD - Accepted Plan (v0.1.0 / M1)
- Scope:
- Acceptance Criteria:
- Risks/Dependencies:

## Change Log
- YYYY-MM-DD: Initialized roadmap.
```

## Event Handling Rules

### Project Bootstrap

- Create `ROADMAP.md` if absent.
- Add an initial milestone (`M1` unless user provides a different identifier).
- Add a changelog entry indicating roadmap initialization.

### Plan Acceptance or Completion

- Update `Current Milestone` to reflect the accepted plan.
- Add or update corresponding row in `Milestones`.
- Append an `Accepted Plan` entry in `Plan History` with scope and acceptance criteria.
- Add a changelog entry summarizing what changed and why.

### Milestone or Version Roadmap Set/Update

- Update existing milestone by ID/version if it exists.
- Add milestone only when no matching milestone exists.
- Avoid duplicate milestones for the same ID or target version.
- If the updated milestone is active, sync `Current Milestone`.

### Milestone Reached/Changed

- Update milestone status (`Completed`, `In Progress`, `Blocked`, `De-scoped`, or `Planned`).
- Update `Current Milestone` if active milestone changed.
- Add a dated note in `Change Log` that captures transition and reason.

### Roadmap Reference Requests

- Point explicitly to `<project_root>/ROADMAP.md`.
- Cite the relevant section name (`Current Milestone`, `Milestones`, `Plan History`, or `Change Log`).
- If file is missing, create it first, then reference it.

## Quality Bar

- Preserve existing useful roadmap content.
- Use ISO date format (`YYYY-MM-DD`) for all dated fields.
- Keep edits minimal and deterministic.
- Never leave conflicting milestone statuses across sections.

## Automation Templates

Use `$project-roadmap-manager` inside automation prompts so Codex consistently applies the roadmap update rules.

For ready-to-fill Codex App and Codex CLI (`codex exec`) templates, including bounded-edit guardrails and placeholders, use:
- `references/automation-prompts.md`

## References

- Automation prompt templates: `references/automation-prompts.md`
