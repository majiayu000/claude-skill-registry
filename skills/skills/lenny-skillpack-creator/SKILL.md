---
name: "lenny-skillpack-creator"
description: "Converts a Refound/Lenny Skill into a high-density, agent-executable Skill Pack (Agent Skills standard). Output must be in English."
---

# Lenny Skillpack Creator

Your job is to refactor “insight-heavy” Refound/Lenny skills into **agent-executable skill packs**: boundary-clear, artifact-driven, and testable.

This skill is designed to be compatible with both:
- **OpenAI Codex** (Codex CLI / IDE skills)
- **Claude Code** (Agent Skills)

You are NOT writing a blog post. You are producing an installable folder with [SKILL.md](SKILL.md) + `references/` (+ optional `scripts/`).

**Language requirement:** The generated skill pack (SKILL.md and all referenced templates/checklists) must be written in **English**.

## What you produce

For a given source skill, output an installable skill directory:

- `<skill-slug>/SKILL.md` (short, executable, high-signal)
- `<skill-slug>/references/` (templates, checklists, rubrics, question bank, examples, source notes)
- `<skill-slug>/scripts/` (optional: lint, scaffolding, batch tools)
- `<skill-slug>/README.md` (install + invoke + examples)

Follow the spec in [references/SKILL_PACK_SPEC.md](references/SKILL_PACK_SPEC.md).

## Inputs you need

Ask for the minimum information needed to proceed. If missing, proceed with explicit assumptions.

Required:
1) The source skill content (SKILL.md or copied text from the Refound page)
2) The intended user / agent context (e.g., “PM agent”, “Hiring assistant”, “Founder operator”, etc.)
3) The intended outputs (what artifacts should exist at the end)

Optional but helpful:
- Tool constraints (read-only? allowed to write files? allowed to run shell?)
- House style / terminology (company-specific sections, metric names, etc.)

## Core principle: Convert insights into an execution contract

Every generated SKILL.md must include:
- **When to use / When NOT to use**
- **Input contract** (minimum inputs + missing-info strategy)
- **Output contract** (explicit deliverables)
- **Workflow** (5–9 steps; each step: inputs → actions → outputs → checks)
- **Quality gate** (checklist/rubric + “risks / open questions / next steps”)
- **Examples** (2 positive + 1 boundary/negative)

Use [references/TRANSFORMATION_RULES.md](references/TRANSFORMATION_RULES.md) as the canonical conversion playbook.

## Progressive disclosure (keep SKILL.md short)

Keep [SKILL.md](SKILL.md) operational. Move long content into `references/` and cite the files.

Heuristic:
- [SKILL.md](SKILL.md): 1–2 pages
- `references/`: everything else (templates, deep notes, long checklists)

## Safety + reliability rules

- Default to least privilege. Only request tools you need.
- Never ask for credentials or secrets.
- If the skill writes/modifies code or makes irreversible changes, require explicit confirmation and add rollback guidance.

Use [references/SECURITY_GUIDE.md](references/SECURITY_GUIDE.md).

## Packaging

If the environment supports file operations, create the folder structure and write files.
Otherwise, output a complete file tree in-chat (one file at a time), clearly labeled.

Optional helper scripts (in this skill folder):
- [scripts/init_skillpack.py](scripts/init_skillpack.py) to generate a skeleton
- [scripts/lint_skillpack.py](scripts/lint_skillpack.py) to validate structure
- [scripts/package_skillpack.py](scripts/package_skillpack.py) to zip a skill pack
- [scripts/fetch_refound_skills.py](scripts/fetch_refound_skills.py) to download Refound SKILL.md sources from a URL list/manifest
