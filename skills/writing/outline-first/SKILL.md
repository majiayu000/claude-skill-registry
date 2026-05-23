---
name: outline-first
description: Create and confirm article outlines before any drafting in the AI 实践记录 workflow.
version: 0.1
---

# outline-first

This skill enforces **outline-first writing** for the **AI 实践记录 / Real World AI Log** project.

It ensures the human reviews and selects a clear outline **before any drafting** begins.

---

## When to Use

Use this skill when:

- A topic or idea has been selected
- You need to propose structure before writing
- The human wants options and tradeoffs

Do NOT use this skill for:

- Draft writing
- Style polishing
- Publishing tasks

---

## Required Workflow

### 1. Context Intake (Mandatory)

Before proposing outlines, the agent MUST:

1. Read `README.md`
2. Read `AGENTS.md`
3. Scan the latest 2–3 files in `content/published/` (if any)
4. Identify:
   - Target audience
   - Related column/series (if any)
   - Tone constraints and boundaries

Summarize understanding in **5–7 bullet points**.

STOP and wait for confirmation if understanding is unclear.

---

### 2. Outline Proposal (Mandatory)

Propose **2–3 outline options**, each with:

- Central question / problem statement
- Intended reader takeaway
- High-level section list
- Tradeoffs (why choose / not choose this outline)

The agent MUST ask the human to **choose one option**.

Do not proceed until a choice is confirmed.

---

### 3. Outline Creation & User Confirmation (Mandatory)

After an outline is selected, the agent MUST:

1. Create the outline file in `content/outlines/<slug>.md`
2. Wait for the human to:
   - Confirm the outline is ready, OR
   - Manually edit/revise the outline
3. Only after explicit user confirmation/approval, proceed to next step
4. Clarify scope limits (what the article will NOT cover)
5. Confirm the next task (typically draft writing)

**CRITICAL**: The agent MUST NOT proceed to draft writing until the human explicitly confirms the outline is finalized (either original or after manual edits).

---

## Writing Constraints

- Practice-first, not theory-first
- No authoritative tone
- Short to medium paragraphs
- No exaggerated AI claims
- Avoid tutorial-style imperatives

---

## Guardrails (Hard Rules)

- ❌ Do not draft without an approved outline
- ❌ Do not invent facts or experiences
- ❌ Do not skip confirmation steps

---

## Success Criteria

This skill is successful when:

- The human quickly selects an outline
- The scope is explicit and reviewable
- The workflow reduces decision fatigue before drafting
