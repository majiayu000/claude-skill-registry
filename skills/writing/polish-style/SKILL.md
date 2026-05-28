---
name: polish-style
description: Refine tone and readability of approved drafts in the AI 实践记录 workflow.
version: 0.1
---

# polish-style

This skill performs **style-only polishing** on an existing draft.

It does not change structure, meaning, or claims without approval.

---

## When to Use

Use this skill when:

- A draft exists and needs tone/readability refinement
- The outline and content scope are already approved

Do NOT use this skill for:

- Creating outlines or drafts
- Adding new claims or sections
- Publishing tasks

---

## Required Workflow

### 1. Preconditions Check (Mandatory)

Before polishing, the agent MUST verify:

- Draft file exists in `content/drafts/`
- The human confirms the draft is ready for style work
- Scope boundaries are still valid

If any item is missing, STOP and ask.

---

### 2. Style-Only Pass (Controlled)

The agent MUST:

- Preserve meaning and section structure
- Improve clarity, concision, and flow
- Keep tone practical and reflective
- Flag any ambiguous or weak passages as `TODO:` instead of rewriting meaning

The agent MUST NOT:

- Add new claims, examples, or conclusions
- Change the article’s scope or outline order
- Use authoritative or hype-driven language

---

### 3. Change Log & Review Prompt (Mandatory)

After polishing, the agent MUST:

- Summarize the types of edits made
- List any `TODO:` flags introduced
- Ask whether to proceed to publishing steps or further revisions

---

## Style Constraints

- Practice-first, not theory-first
- Short to medium paragraphs
- Prefer first-person when appropriate
- Avoid tutorial-style imperatives
- No exaggerated AI capability claims

---

## Guardrails (Hard Rules)

- ❌ Do not polish without a confirmed draft
- ❌ Do not rewrite meaning or add new content
- ❌ Do not publish or move files to `published/`

---

## Success Criteria

This skill is successful when:

- The draft reads smoother without changing meaning
- The human can easily review changes
- The next step decision is explicit
