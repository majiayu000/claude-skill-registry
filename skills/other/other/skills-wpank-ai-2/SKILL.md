---
name: create-skill
model: standard
description: Guided skill creation with quality criteria
usage: /create-skill <name> [category]
---

# /create-skill

Create a new skill with guided quality checks.

## Usage

```
/create-skill <name> [category]
```

**Arguments:**
- `name` — Skill name (kebab-case)
- `category` — Target category (optional, will prompt if omitted)

## Examples

```
/create-skill websocket-patterns realtime
/create-skill postgres-optimization backend
/create-skill animation-hooks design-systems
```

## What It Does

1. **Creates** skill directory at `ai/skills/[category]/[name]/`
2. **Generates** SKILL.md with template structure
3. **Prompts** for skill description (WHAT, WHEN, KEYWORDS)
4. **Asks** for "When to Use" triggers
5. **Guides** through code example creation
6. **Prompts** for NEVER Do anti-patterns
7. **Validates** against quality criteria
8. **Reports** any quality issues to fix

## Skill Template

```markdown
---
name: [name]
description: [WHAT it does], [WHEN to use], [KEYWORDS for triggers]
---

# [Name] Skill

[One-line description]

---

## When to Use

- [Trigger condition 1]
- [Trigger condition 2]

---

## Patterns

### [Pattern Name]

[Explanation]

\`\`\`typescript
// Code example
\`\`\`

---

## NEVER Do

- [Anti-pattern 1]
- [Anti-pattern 2]

---

## Related

- [Related skills]
```

## Quality Criteria

The skill must pass:

- [ ] >70% expert knowledge (not in base model)
- [ ] <300 lines (max 500)
- [ ] Description has WHAT, WHEN, KEYWORDS
- [ ] Has "When to Use" section
- [ ] Has code examples
- [ ] Has NEVER Do section
- [ ] Project-agnostic (no hardcoded names)

## Post-Creation Validation

After creating the skill, run these checks to ensure it meets quality standards and integrates properly.

### Automated Validation

```bash
python scripts/validate_all_skills.py --skill <name>
```

The newly created skill must receive a **passing grade**. Fix any reported issues immediately while context is fresh.

### Overlap Check

```bash
python scripts/search_skills.py <name>
```

Search for existing skills with similar names or descriptions. If overlapping skills are found:
- Consider merging content into the existing skill instead
- Or differentiate clearly in the description and "When to Use" section

### Catalog Registration

After the skill passes validation, add it to `SKILLS-CATALOG.md`:
- Add an entry under the appropriate category
- Include the skill name, description, and path
- This ensures the skill is discoverable by other users and agents

### Checklist

- [ ] `validate_all_skills.py --skill <name>` returns passing grade
- [ ] No significant overlap with existing skills (checked via `search_skills.py`)
- [ ] Skill added to `SKILLS-CATALOG.md`

## Output Locations

- Skill → `ai/skills/[category]/[name]/SKILL.md`

## Related

- **Validate:** `/validate-skill` (check existing skill)
- **Check overlaps:** `/check-overlaps` (find redundant skills)
- **Quality criteria:** [`ai/skills/extraction/references/skill-quality-criteria.md`](ai/skills/extraction/references/skill-quality-criteria.md)
