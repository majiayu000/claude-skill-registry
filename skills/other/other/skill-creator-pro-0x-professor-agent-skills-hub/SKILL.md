---
name: skill-creator-pro
description: Create and evolve production-ready skills with reusable scripts, references, and validation. Use for new skill creation, skill upgrades, and enforcing consistent metadata and structure.
---

# Skill Creator Pro

## Overview

Create skills that are immediately usable by AI agents and maintainable across a shared repository.

Use this skill to enforce:
- Trigger-quality `description` fields in frontmatter.
- Consistent `agents/openai.yaml` metadata.
- Reusable scripts/references/assets per domain.
- Validation and smoke-test readiness before publishing.

## Workflow

1. Clarify skill intent with two or three concrete user prompts.
2. Select one primary workflow pattern (task-based, workflow-based, or capability-based).
3. Define reusable resources before writing final `SKILL.md` prose.
4. Generate starter layout with `scripts/generate_skill_starter.py`.
5. Edit `SKILL.md` and references to keep core instructions concise.
6. Validate the entire pack with `scripts/validate_skill_pack.py`.

## Use Bundled Resources

- Read `references/workflow.md` for quality gates and review checklist.
- Read `references/category-guides.md` for domain-specific starter guidance.
- Reuse templates in `assets/templates/` to avoid rewriting boilerplate.
- Run `scripts/generate_skill_starter.py` to generate category starter output.
- Run `scripts/validate_skill_pack.py` after edits and before publishing.

## Output Standards

When creating or updating a skill:
- Keep frontmatter keys minimal (`name`, `description`).
- Keep descriptions explicit about trigger conditions.
- Keep scripts deterministic and compatible with `--dry-run`.
- Keep examples safe, especially for cybersecurity content.
