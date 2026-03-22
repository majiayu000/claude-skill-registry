---
name: ce-skill-creator
description: >
  Create or refactor skills with precise triggers, reusable assets and references,
  and synchronized registry updates.
---

# CE Skill Creator

Use this skill to add new skills or upgrade weak existing skills.

## Core asset

- `assets/skill_template.md` - canonical scaffold for new/refactored skills.
- `assets/description_style_guide.md` - strict frontmatter description rules.
- `assets/trigger_phrase_reference_template.md` - template for extracted trigger
  phrase references.

## Recommended sequence

1. Run `ce-skill-audit` to capture baseline gaps.
2. Create/refactor the target skill using the template asset.
3. Add support files as needed:
- `assets/` for templates/checklists/snippets
- `references/` for embedded standards/ADR extracts
- `scripts/` for deterministic scaffolding helpers

4. Tighten trigger wording in `description` to avoid overlap.
5. If a legacy skill has phrase-heavy descriptions, move those trigger phrases
   into `references/trigger_phrases.md` using the reference template.
6. If you changed skill inventory, invoke `ce-skill-registry-sync` and update:
- `CONTRIBUTOR_INSTRUCTIONS.md` section 6A
- `.claude/skills/ce-onboard/SKILL.md` section 4
- `docs/contributor/agent_skills.md`

7. Re-run `ce-skill-audit` and resolve blocker/high findings.
8. Run strict description quality check:

```bash
pwsh .claude/skills/ce-skill-audit/scripts/check_skill_description_quality.ps1
```

## Refactor policy for poor skills

When hardening an existing skill, preserve intent but fix structure:

- add/repair YAML frontmatter
- clarify activation cues
- separate long static content into assets/references
- add explicit output and validation expectations

## Output contract

For each created/refactored skill, provide:

1. skill name + path
2. trigger description summary
3. any added assets/references/scripts
4. registry updates completed

## Constraints

- Keep changes CE-first and repository-specific.
- Do not add evaluation-focused skill families in this workflow.
