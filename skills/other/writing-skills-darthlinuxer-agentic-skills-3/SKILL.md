---
name: writing-skills
description: Helps author concise, discoverable skills using TDD-style testing. Use
  when creating, editing, or verifying skills before deployment.
---

# Writing Skills

## Purpose

Writing skills is TDD applied to process documentation: **RED → GREEN → REFACTOR**. If you didn’t watch a baseline failure, you don’t know what to fix.

**Required background:** superpowers:test-driven-development.

## Official model (progressive disclosure)

1. **Metadata (always loaded):** YAML `name`, `description`.
2. **Instructions (on trigger):** SKILL.md body.
3. **Resources/scripts (as needed):** linked files + tools.

## What to include in a skill

- **Overview:** 1–2 sentences with the core principle.
- **When to use:** triggers/symptoms + when NOT to use.
- **Core pattern:** steps or before/after pattern.
- **Quick reference:** concise table or bullets.
- **Examples:** one excellent, runnable example.
- **Common mistakes:** failure → fix.

## Frontmatter rules (standard)

- `name`: lowercase letters/numbers/hyphens only, max 64 chars, no reserved words.
- `description`: third-person, **what + when**, max 1024 chars. Start with “Use when…”.
- Avoid workflow summaries in `description` (they become shortcuts and skip the body).

**IDE extensions** (optional): `disable-model-invocation`, `allowed-tools`, `context`, `agent`, etc. Use only when targeting another platform.

## TDD loop for skills (essentials)

- **RED:** run pressure scenario without the skill; capture rationalizations verbatim.
- **GREEN:** write minimal skill to block those rationalizations.
- **REFACTOR:** add explicit counters and retest until compliant.

Detailed testing format: see [testing-skills-with-subagents.md](testing-skills-with-subagents.md).

## Search optimization (CSO)

- Description must include **what + when** with concrete triggers.
- Use likely search terms: error strings, symptoms, tool names.
- Prefer verb-first names (e.g., `creating-skills`, `debugging-with-logs`).

## Anti-patterns (avoid)

- Narratives or one-off stories.
- Multi-language examples.
- Deep reference chains (keep all references one hop from SKILL.md).
- Time-sensitive instructions.
- Vague names or descriptions.

## Quick creation checklist

- [ ] Run baseline scenario (RED) and record failures
- [ ] Write skill addressing those exact failures (GREEN)
- [ ] Add explicit counters for new rationalizations (REFACTOR)
- [ ] Frontmatter: valid `name`, `description` (what + when)
- [ ] One excellent example, one quick reference
- [ ] Verify under pressure (retest)

## Additional references

- [anthropic-best-practices.md](anthropic-best-practices.md) — concise official guidance
- [testing-skills-with-subagents.md](testing-skills-with-subagents.md) — scenario templates and pressure testing
- [persuasion-principles.md](persuasion-principles.md) — use only for discipline skills
