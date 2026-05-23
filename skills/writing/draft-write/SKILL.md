---
name: draft-write
description: Produce a first draft from an approved outline in the AI 实践记录 workflow.
version: 0.1
---

# draft-write

This skill creates a **first draft** based on an **approved outline**.

It keeps the agent in a collaborator role and enforces human checkpoints.

---

## When to Use

Use this skill when:

- An outline has been approved
- You need a draft for review and revision

Do NOT use this skill for:

- Outline creation
- Style-only polishing
- Publishing tasks

---

## Required Workflow

### 1. Preconditions Check (Mandatory)

Before drafting, the agent MUST verify:

- There is an approved outline in `content/outlines/<slug>.md`
- The human has explicitly confirmed the outline is finalized (either original or after manual edits)
- The intended draft file path is confirmed
- Scope limits are explicit

If any item is missing, STOP and ask.

---

### 2. Draft Execution (Controlled)

The agent MUST:

1. Create a draft in `content/drafts/<slug>.md`
2. Follow the outline section order
3. Use short to medium paragraphs
4. Mark any uncertain details with `TODO:` notes

The agent MUST NOT:

- Invent experiences or results
- Add new sections not in the outline without approval
- Use authoritative or conclusive tone

---

### 3. Post-Draft Summary (Mandatory)

After drafting, the agent MUST:

- Summarize what was written
- Highlight any `TODO:` items or gaps
- Ask whether to proceed to style polishing or revisions

---

## Writing Constraints

- Practice-first, not theory-first
- Prefer first-person when appropriate
- Avoid tutorial-style imperatives
- No exaggerated AI capability claims

---

## Guardrails (Hard Rules)

- ❌ Do not draft without outline approval
- ❌ Do not overwrite existing drafts without permission
- ❌ Do not auto-publish or move to `published/`

---

## Success Criteria

This skill is successful when:

- A clear, reviewable draft exists
- The draft matches the approved outline
- The human has explicit next-step choices
