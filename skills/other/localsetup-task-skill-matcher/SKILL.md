---
name: localsetup-task-skill-matcher
description: "Match user tasks to installed Localsetup skills, recommend top matches, and run single-task or batch skill-selection flow with minimal interruption. Includes top-3 complementary public-skill suggestions and public-index refresh handling."
metadata:
  version: "1.1"
---

# Task-to-skill matcher

**Purpose:** Provide one consistent flow for choosing the best installed skill for a user task. Use this when the user asks "what skill should I use?", asks to "pick the best", or when skill choice is unclear.

## When to use this skill

- User asks for skill recommendation or best-skill selection.
- Task-to-skill match is uncertain.
- User asks to auto-pick skills for a multi-step or batch run.

## Do not use this skill

- If user names a specific skill to run, load that skill directly and skip this matcher.

## Sources and scope

- Read installed-skill candidates from the **current platform's context loader/index** (see `_localsetup/docs/PLATFORM_REGISTRY.md`).
- Cursor: `.cursor/rules/localsetup-context-index.md` (or skills section of `.cursor/rules/localsetup-context.mdc`).
- Claude Code: `.claude/CLAUDE.md`.
- Codex: `AGENTS.md`.
- Other platforms: workspace context per platform registry (see PLATFORM_REGISTRY.md).
- Use public-skill suggestions from `_localsetup/docs/PUBLIC_SKILL_INDEX.yaml`.

## Mode detection

- Treat as **batch** when user request includes multiple distinct subtasks, or says "batch", "multiple steps", or "run the whole thing".
- Otherwise treat as **single task**.

## Workflow

1. **Collect intent**
   - Extract user intent and any task constraints.
   - If user already named a skill, stop matching and load that skill.

2. **Rank installed skills**
   - Compare intent against each installed skill's "when to use" text.
   - Rank by relevance (keyword and description relevance).
   - If uncertain, prepare top 3 candidates with one-line "why it fits".

3. **Single-task flow**
   - If one clear installed match exists, ask once: **"Use this skill?"**
   - Same turn: include up to 3 complementary public skills (one-line reason each).
   - If public index is missing or stale, still show match and "Use this skill?" first, then ask: **"Complementary suggestions need the public index. Want me to refresh it now so I can recommend installable skills?"**

4. **Batch / long-running flow**
   - Prompt once at start with options:
     - Auto-pick best skill for the whole run.
     - Parcel-by-parcel prompts.
     - Parcel auto-pick.
   - If auto-pick is chosen, show planned skill sequence first (best-effort), then proceed without repeated skill prompts.
   - If user chooses parcels and phases are unclear, propose one parcel (whole task), then ask prompt-vs-auto-pick for that parcel.

5. **No installed fit**
   - State that no installed skill is a good fit.
   - Offer up to 3 complementary public skills to import.
   - Optionally suggest creating a new skill with `localsetup-skill-creator`.

## Public index rules

- Stale definition: `_localsetup/docs/PUBLIC_SKILL_INDEX.yaml` missing, missing `updated`, or `updated` older than 7 days.
- For complementary suggestions: return up to 3 public skills, each with one-line fit reason.
- To import suggestions, point user to `localsetup-skill-importer` (or run it if user asks).

## Output style

- Keep outputs short, actionable, and consistently structured.
- For uncertain match: show top 3 installed candidates, each with one-line reason, then ask user to choose or say "pick the best".
- For single clear match: ask once, then show complementary public options in the same response.
- For public complementary suggestions, use available enriched fields from `_localsetup/docs/PUBLIC_SKILL_INDEX.yaml`:
  - Prefer `summary_short` over raw description.
  - Include notable `requirements` or `risk_flags` in one short line.
- Rendering fallback:
  - Rich/basic markdown: numbered list with labeled fields.
  - Plain text/ascii: numbered list with `Skill:`, `Why:`, `Risks:`.

## References

- `_localsetup/docs/TASK_SKILL_MATCHING.md`
- `_localsetup/docs/SKILLS_AND_RULES.md`
- `_localsetup/docs/PLATFORM_REGISTRY.md`
- `_localsetup/docs/PUBLIC_SKILL_INDEX.yaml`
- `localsetup-skill-importer`
- `localsetup-skill-creator`
