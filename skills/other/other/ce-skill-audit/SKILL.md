---
name: ce-skill-audit
description: >
  Audit the skills catalog for frontmatter quality, trigger precision, structural
  hygiene, and registry synchronization.
---

# CE Skill Audit

Use this skill for a critical quality audit of repository skills.

Load these references first:
- `references/claude_skills_how_to_checklist.md`
- `references/trigger_phrase_catalog.md`

## Audit workflow

1. Inventory skills and required files:

```bash
Get-ChildItem .claude/skills -Directory | Select-Object -ExpandProperty Name
rg --files .claude/skills
```

2. Structural checks (per skill):
- `SKILL.md` exists
- YAML frontmatter exists
- `name` matches directory name
- `description` exists and is specific
- file length remains maintainable (`<500` lines target)

3. Trigger-quality checks:
- descriptions are specific enough to avoid accidental over-triggering
- overlapping skills have clear differentiation
- description length and style pass the strict checker:

```bash
pwsh .claude/skills/ce-skill-audit/scripts/check_skill_description_quality.ps1
```

4. Content organization checks:
- long static templates live in `assets/`
- large reference material lives in `references/`
- deterministic generators live in `scripts/`
- phrase-heavy trigger synonyms are extracted to references (not embedded in
  frontmatter descriptions)

5. Registry consistency checks:
- `CONTRIBUTOR_INSTRUCTIONS.md` section 6A
- `.claude/skills/ce-onboard/SKILL.md` section 4
- `docs/contributor/agent_skills.md`
- filesystem set equality must hold

## Output contract

Return findings first, grouped by severity:

1. blocker (breaks discoverability/routing)
2. high (likely mis-triggering or stale registry)
3. medium (maintainability issues)
4. low (style/clarity improvements)

Each finding must include:
- skill/file reference
- violated rule
- exact remediation

## Constraints

- Do not propose evaluation-skill additions in this audit.
- Do not mark audit complete while registries and filesystem differ.
