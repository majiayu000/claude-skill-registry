---
name: claude-mem-coded-assistant
description: >
  Entry-point skill for using claude-mem to keep CLAUDE.md and MEMORY.md
  in sync so Claude learns from past work and avoids repeating mistakes.
version: 1.1.0
---

# Claude‑Mem Coding Skill

## What This Skill Does

This skill teaches Claude how to:

- Mine **claude-mem** (via MCP) for high‑signal past work.
- Maintain a concise, high‑impact **CLAUDE.md** (~1,500 tokens).
- Maintain a curated **MEMORY.md** of lessons learned and directions, so future work is faster and less error‑prone.

It is an **entry point**, not a full manual. Detailed workflows and examples live in separate reference files that Claude can open on demand.

---

## When to Use This Skill

Claude should activate this skill when:

- A feature, refactor, or significant bugfix is completed.
- An infra/deployment change introduces new operational lessons.
- Starting work on an area with substantial history in claude-mem.
- Performing a daily “memory maintenance” pass on an active repo.

---

## Inputs and Outputs

### Inputs

Claude relies on:

- **Files** (in repo root):
  - `CLAUDE.md` – main project instructions.
  - `MEMORY.md` – curated lessons and directions.
- **claude-mem MCP tools** (already installed & connected):
  - `search` – index‑level observation search.
  - `timeline` – temporal context around observations.
  - `get_observations` – full structured details.

### Outputs

This skill produces:

- **Patch‑style edits** to:
  - `MEMORY.md` – new or updated lessons, patterns, and playbooks.
  - `CLAUDE.md` – refreshed rules while staying under ~1,500 tokens.
- No raw claude-mem transcripts are copied; only compressed, actionable guidance.

---

## How Claude Should Behave

### 1. Mine claude-mem → Update MEMORY.md

High‑level behavior (details in `claude-mem-usage.md`):

- Use **progressive disclosure** against claude-mem:
  1. `search` for recent `decision`, `bugfix`, `refactor`, `discovery`, `change` observations.
  2. `timeline` around promising IDs to see context.
  3. `get_observations` for a small set of high‑value IDs.
- From those, update `MEMORY.md` with:
  - Architectural decisions and their impact.
  - Implementation patterns and anti‑patterns.
  - Debugging playbooks and DevOps lessons.

**Constraints**

- Prefer short bullets over long prose.
- Record *why* decisions were made and how to act next time.
- Never store secrets or credentials in `MEMORY.md`.

For a full template and examples, Claude should open:

- `memory-structure-reference.md`
- `claude-mem-usage.md`

---

### 2. Distill MEMORY.md → Refresh CLAUDE.md (≈1,500 tokens)

High‑level behavior:

- Read the existing `CLAUDE.md` and approximate its size; keep the body around **1–1.5k tokens** for optimal behavior.
- Pull only **current, high‑impact** content from `MEMORY.md`:
  - Still‑valid architectural directions.
  - Frequently reused patterns and gotchas.
  - Operational guardrails that materially affect daily work.
- Rewrite historical notes as **timeless rules**, e.g.:
  - “When adding retries to DB writes, always use the shared retry helper instead of manual loops.”

- Use links instead of inlining:
  - `.clauderules/code-style.md` for style.
  - `.clauderules/testing.md` for testing.
  - `MEMORY.md` sections for deeper background.

**Token Discipline**

- If CLAUDE.md is too long:
  - Merge overlapping bullets.
  - Drop generic advice that doesn’t change behavior.
  - Replace detailed explanations with references to supporting docs.

**Diff‑First**

- Propose **minimal patches**, not full rewrites:
  - Update only sections that need change (e.g., “Architectural Directions”, “Patterns & Gotchas”).
  - Preserve stable layout and headings.
- Always leave final acceptance to human review in Git/CI.

For concrete layouts and example diffs, Claude should open:

- `claude-md-layout-reference.md`
- `example-diffs.md`

---

## Safety and Priority Rules

Claude must:

- **Always**:
  - Query claude-mem before re‑solving problems already encountered in this project.
  - Update `MEMORY.md` after meaningful work with concise, actionable lessons.
  - Keep `CLAUDE.md` focused on rules that change how work is done, not on general LLM tips.

- **Never**:
  - Overwrite `CLAUDE.md` or `MEMORY.md` entirely; always propose small diffs.
  - Paste raw claude-mem observations verbatim into either file.
  - Store secrets, API keys, or sensitive infra details in these files.

- **Conflict resolution priority**:
  1. Explicit instructions in `CLAUDE.md`.
  2. Latest curated guidance in `MEMORY.md`.
  3. Raw claude-mem observations and session summaries.
  4. Ad‑hoc reasoning in the current session.

---

## Quick “How to Call Me”

Users can invoke this skill with prompts like:

> “Use the claude-mem coding skill to:
>  1) mine claude-mem for recent work,
>  2) update MEMORY.md with lessons, and
>  3) refresh CLAUDE.md under the ~1,500‑token budget.”

Claude should then:

1. Run the claude-mem `search → timeline → get_observations` flow.
2. Draft a patch for `MEMORY.md` with new lessons.
3. Draft a patch for `CLAUDE.md` derived from `MEMORY.md`.
4. Present both patches clearly for human review and commit.

---

## External References

To keep this SKILL.md lean and within best‑practice size, Claude should open these files when more detail is needed:

- `claude-mem-usage.md` – detailed claude-mem MCP workflows, filters, and example queries.
- `memory-structure-reference.md` – full MEMORY.md templates and longer examples.
- `claude-md-layout-reference.md` – canonical CLAUDE.md section layouts and size guidance.
- `example-diffs.md` – sample before/after patches for CLAUDE.md and MEMORY.md.

