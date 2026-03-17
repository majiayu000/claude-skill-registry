---
name: promote-skill
model: fast
description: Move a skill from staging to active
usage: /promote-skill <name> [category]
---

# /promote-skill

Promote a staged skill to active production location.

## Usage

```
/promote-skill <name> [category]
```

**Arguments:**
- `name` — The skill folder name in staging
- `category` — Target category (ai-chat, design-systems, backend, realtime, meta)

## Examples

```
/promote-skill pmon-design-system design-systems
/promote-skill api-patterns backend
/promote-skill chat-streaming ai-chat
```

## When to Use

- Promoting a **single skill** from staging to active
- Skill has already been validated and refined
- You know the target category for the skill
- For **bulk promotion** of multiple skills, use `/refine-staged` instead

## What It Does

1. **Locates** the skill in `ai/staging/skills/[name]/`
2. **Validates** the skill exists and has SKILL.md
3. **Checks** quality criteria (see below)
4. **Creates** target directory if needed
5. **Moves** skill to `ai/skills/[category]/[name]/`
6. **Removes** from staging
7. **Reports** success or validation failures

## Quality Criteria

Before promotion, the skill must pass:

- [ ] >70% expert knowledge (not in base model)
- [ ] <300 lines (max 500)
- [ ] Has WHAT, WHEN, KEYWORDS in description
- [ ] Includes specific NEVER Do list
- [ ] Project-agnostic (no hardcoded project names)
- [ ] Has "When to Use" section
- [ ] Has code examples (if applicable)

## Quality Gate

Run these validation checks **before** promoting a skill. All checks must pass — if any fail, do not promote until the issues are resolved.

### Automated Validation

```bash
python scripts/validate_all_skills.py --skill <name>
```

The skill must receive a **passing grade** from the validator. Fix any reported issues before proceeding.

### Manual Checks

1. **Frontmatter present and complete**
   - SKILL.md must have YAML frontmatter with `name` and `description` fields
   - `description` should include WHAT, WHEN, and KEYWORDS

2. **Minimum content threshold**
   - SKILL.md must be at least **50 lines** — anything shorter likely lacks sufficient depth

3. **No placeholder text**
   - Search for `TODO`, `FIXME`, `TBD`, `[placeholder]`, `[your-`, `lorem ipsum`
   - All template placeholders must be replaced with real content

4. **No broken internal links**
   - Verify all relative markdown links (`[text](path)`) resolve to existing files
   - Check that referenced scripts, templates, and related skills exist

### Gate Outcome

- **All checks pass** → proceed with promotion (step 4 onward in "What It Does")
- **Any check fails** → report failures, do NOT promote, suggest fixes

## Output Locations

- Promoted skill → `ai/skills/[category]/[name]/`
- Removed from → `ai/staging/skills/[name]/`

## Related

- **Full command:** `/refine-staged` (bulk promotion)
- **Validation:** `/validate-skill` (check before promoting)
- **Quality criteria:** [`ai/skills/extraction/references/skill-quality-criteria.md`](ai/skills/extraction/references/skill-quality-criteria.md)
