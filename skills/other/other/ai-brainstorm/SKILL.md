---
name: ai-brainstorm
description: "Use when the user wants to design, architect, or explore a feature before building it. HARD GATE: no implementation until the user approves the spec."
effort: max
argument-hint: "[feature or problem description] [optional: work item ID e.g. AB#100, #45]"
---


# Brainstorm

## Purpose

Design interrogation skill. Forces rigorous thinking BEFORE any code is written. Produces an approved spec that becomes the contract for `/ai-plan`.

HARD GATE: this skill produces a spec. No implementation happens until the user explicitly approves it.

## When to Use

- User says "I want to build...", "how should we...", "let's design..."
- New feature, architecture change, or ambiguous requirement
- Any work where jumping straight to code would be premature

## Process

1. **Load context** -- read `specs/spec.md`, `decision-store.json`, and `docs/solution-intent.md` section 7 (roadmap)
   - If a work item ID is provided (e.g., `AB#100` or `#45`):
     a. Read `.ai-engineering/manifest.yml` `work_items` section for active provider and team config
     b. Fetch work item and its hierarchy from the provider:
        - **GitHub**: `gh issue view <number> --json title,body,labels,milestone,assignees`
        - **Azure DevOps**: `az boards work-item show --id <number> --expand relations -o json`
     c. Walk the hierarchy: Feature → User Story → Tasks (follow parent/child relations)
     d. Use all standard and custom fields the platform provides
     e. Pre-fill `refs` section in the generated spec frontmatter
2. **Interrogate** -- follow `handlers/interrogate.md` for the questioning flow
3. **Propose approaches** -- present 2-3 options with trade-offs (never just one)
4. **Draft spec** -- write spec to `specs/spec.md`
5. **Review spec** -- follow `handlers/spec-review.md` for the review loop (max 3 iterations)
6. **STOP** -- present approved spec. User runs `/ai-plan` to continue.

## Quick Reference

| Step | Gate | Output |
|------|------|--------|
| Interrogate | All UNKNOWNs resolved | Requirements map |
| Propose | User selects approach | Chosen design |
| Spec draft | Written to disk | spec.md |
| Spec review | Subagent approves | Reviewed spec |
| User approval | User says "approved" | HARD GATE passed |

## Questioning Rules

- ONE question at a time. Never batch.
- Prefer multiple choice (A/B/C) over open-ended.
- Challenge vague language: "improve", "optimize", "clean up" are not requirements.
- Push back on scope creep. Ask: "Is this in scope for v1?"
- Explore edge cases the user has not mentioned.
- Max 10 questions per session. If you need more, the problem is too big -- split it.

## Common Mistakes

- Skipping interrogation and jumping to the spec.
- Proposing only one approach (always propose 2-3).
- Writing implementation details in the spec (specs describe WHAT, not HOW).
- Not challenging the user's assumptions.
- Producing a spec without the review loop.

## Integration

- **Called by**: user directly, or `/ai-plan` when requirements are unclear
- **Calls**: `handlers/interrogate.md`, `handlers/spec-review.md`
- **Transitions to**: `/ai-plan` (ONLY -- never directly to `ai-build` or `/ai-dispatch`)

$ARGUMENTS
