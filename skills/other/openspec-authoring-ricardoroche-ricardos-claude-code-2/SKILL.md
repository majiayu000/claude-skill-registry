---
name: openspec-authoring
description: Enforces OpenSpec authoring conventions including metadata blocks, section ordering, requirement/scenario structure, and validation steps.
category: documentation
---

# OpenSpec Authoring Patterns

**Trigger Keywords**: openspec, proposal, change-id, tasks.md, spec delta, requirement, scenario, validation, archive

**Agent Integration**: Used by `spec-writer` and planning agents when creating or updating OpenSpec proposals, tasks, and spec files.

## Metadata & Frontmatter
- Proposals/Tasks: include `Change ID`, `Status`, `Date`, and `Author` near the top.
- Specs: start with `# Spec: <Title>` plus capability/status/related lines.
- Use verb-led, kebab-case `change-id` (e.g., `add-doc-spec-writer-agent`).
- Keep managed instruction blocks intact when present.

## Required Section Ordering
- **proposal.md**: Executive Summary → Background → Goals → Scope/Non-Goals → Approach → Risks & Mitigations → Validation → Open Questions.
- **tasks.md**: Overview → Phase/Task grouping with checklists; include validation notes where possible.
- **spec.md (delta)**: Overview → `## ADDED|MODIFIED|REMOVED Requirements` → Scenarios per requirement with Given/When/Then.

## Requirement & Scenario Patterns
- Each requirement MUST have at least one `#### Scenario:` block.
- Scenario steps use bolded **Given/When/Then** lines on their own lines.
- Keep requirements testable and behavior-focused; avoid solutions in "Then".
- Use backticks for capability or file references when helpful.

## Validation Checklist
- ✅ Run `openspec validate <change-id> --strict` when available.
- ✅ Ensure every referenced skill/agent/capability exists or is added in the change.
- ✅ Confirm paths use workspace-relative notation (`openspec/specs/...`).
- ✅ Keep documentation generic and reusable across Python projects.

## Archiving Notes
- Archive changes only after deployment, using date-prefixed folder under `openspec/archive/`.
- Use `openspec archive <id> --skip-specs --yes` only for tooling-only changes.
