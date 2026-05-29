---
name: publish-pac
description: Prepare a publication package from a polished draft in the AI 实践记录 workflow.
version: 0.1
---

# publish-pac

This skill prepares a **publication package** from a polished draft.

It does not publish automatically or change the core content without approval.

---

## When to Use

Use this skill when:

- A polished draft is ready for final packaging
- You need metadata, title options, and publishing checklist

Do NOT use this skill for:

- Writing outlines or drafts
- Style-only polishing
- Automated posting or publishing

---

## Required Workflow

### 1. Preconditions Check (Mandatory)

Before packaging, the agent MUST verify:

- Polished draft exists in `content/drafts/` or a designated review file
- The human confirms content is ready for packaging
- Target platform(s) are confirmed (e.g., WeChat, X)

If any item is missing, STOP and ask.

---

### 2. Package Assembly (Controlled)

The agent MUST prepare a package that includes:

- 2–3 title options
- Short summary (2–4 sentences)
- Key bullets (3–5 points)
- Suggested cover image description (text only)
- Publishing checklist (links, TODOs, and required assets)

The agent MUST NOT:

- Change claims or add new sections
- Publish or schedule content automatically
- Invent metrics or results

---

### 3. Review Prompt (Mandatory)

After packaging, the agent MUST:

- Summarize what was produced
- Ask for confirmation before any publishing actions

---

## Style Constraints

- Practical, reflective tone
- No authoritative claims
- Avoid hype or certainty
- Keep summaries concise

---

## Guardrails (Hard Rules)

- ❌ Do not package without confirmed draft readiness
- ❌ Do not publish or move files to `published/`
- ❌ Do not invent assets or performance claims

---

## Success Criteria

This skill is successful when:

- The human can publish with minimal extra work
- Required assets and metadata are clearly listed
- The package is concise and reviewable
